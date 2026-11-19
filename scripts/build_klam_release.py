"""Build Klam from rights-cleared source text with traceable records."""
import argparse
import gzip
import hashlib
import io
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = ROOT / "datasets/klam"
SOURCE_REGISTRY = INPUT_ROOT / "sources.json"
RECORD_ROOT = INPUT_ROOT / "records"
SHARD_RECORDS = 50_000
CC_BY_4 = "https://creativecommons.org/licenses/by/4.0/"
CC0_1 = "https://creativecommons.org/publicdomain/zero/1.0/"


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def read_sources():
    from jsonschema import Draft202012Validator, FormatChecker

    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    entries = registry.get("sources")
    if not isinstance(entries, list):
        raise ValueError("Klam source registry must contain a sources list")
    schema = json.loads(
        (ROOT / "schemas/klam-source.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    sources = {}
    for source in entries:
        errors = sorted(validator.iter_errors(source), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise ValueError("invalid Klam source registry entry: " + details)
        source_id = source.get("source_id")
        if not source_id or source_id in sources:
            raise ValueError("Klam source IDs must be present and unique")
        if source.get("rights_status") != "approved":
            raise ValueError(f"{source_id}: source rights have not been approved")
        if source.get("rights_basis") not in {
            "original", "contributor_permission", "public_domain", "cc0"
        }:
            raise ValueError(f"{source_id}: unsupported rights_basis")
        if not source.get("source_version") or not source.get("rights_evidence_url"):
            raise ValueError(f"{source_id}: version and rights evidence are required")
        if not source.get("attribution"):
            raise ValueError(f"{source_id}: attribution text is required")
        if source["rights_basis"] in {"original", "contributor_permission"}:
            if source.get("license") != "CC-BY-4.0" or source.get("license_url") != CC_BY_4:
                raise ValueError(f"{source_id}: original/submitted text must use CC BY 4.0")
            if source.get("permission_evidence_recorded") is not True:
                raise ValueError(f"{source_id}: permission record is missing")
        elif source["rights_basis"] == "cc0":
            if source.get("license") != "CC0-1.0" or source.get("license_url") != CC0_1:
                raise ValueError(f"{source_id}: CC0 source must use the CC0 1.0 URL")
            if source.get("permission_evidence_recorded") is not True:
                raise ValueError(f"{source_id}: CC0 dedication evidence is missing")
        elif source.get("license") != "Public-Domain":
            raise ValueError(f"{source_id}: public-domain source must be labeled Public-Domain")
        sources[source_id] = source
    return registry, sources


def normalize_row(row, sources):
    source_id = row.get("source_id")
    source = sources.get(source_id)
    if source is None:
        raise ValueError(f"record refers to an unapproved source: {source_id!r}")
    text = row.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("record text must be a nonempty string")
    record_id = row.get("source_record_id")
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("source_record_id must be a stable, nonempty string")
    title = row.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"title is required for {record_id}")
    script = row.get("script")
    if script not in {"Arabic", "Latin", "Mixed"}:
        raise ValueError(f"invalid script for {record_id}: {script!r}")
    task = row.get("task")
    if not isinstance(task, str) or not task.strip():
        raise ValueError(f"task is required for {record_id}")
    review_status = row.get("review_status", "unreviewed")
    if review_status not in {"unreviewed", "human_reviewed"}:
        raise ValueError(f"invalid review_status for {record_id}")
    reviewer_id = row.get("reviewer_id", "")
    review_date = row.get("review_date", "")
    review_scope = row.get("review_scope", "")
    if review_status == "human_reviewed" and not all((reviewer_id, review_date, review_scope)):
        raise ValueError(f"human-reviewed record lacks review evidence: {record_id}")
    digest_input = source_id + "\0" + record_id + "\0" + canonical(text)
    return {
        "id": sha256_bytes(digest_input.encode("utf-8")),
        "title": title,
        "text": text,
        "language": "ur",
        "script": script,
        "task": task,
        "label": str(row.get("label") or ""),
        "split": str(row.get("split") or ""),
        "source_id": source_id,
        "source_version": source["source_version"],
        "source_record_id": record_id,
        "source_locator": str(row.get("source_locator") or ""),
        "rights_basis": source["rights_basis"],
        "license": source["license"],
        "license_url": source.get("license_url", ""),
        "rights_evidence_url": source["rights_evidence_url"],
        "attribution": source["attribution"],
        "review_status": review_status,
        "reviewer_id": reviewer_id,
        "review_date": review_date,
        "review_scope": review_scope,
    }


def write_shard(output, index, rows):
    relative = f"data/klam-{index:05d}.jsonl.gz"
    path = output / relative
    with (path.open("wb") as raw,
          gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped,
          io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as stream):
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    payload = path.read_bytes()
    return {
        "path": relative,
        "records": len(rows),
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def build(output):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    registry, sources = read_sources()
    files = sorted([*RECORD_ROOT.glob("*.jsonl"), *RECORD_ROOT.glob("*.jsonl.gz")])
    if not sources or not files:
        return {
            "ready": False,
            "reason": "No approved Klam-originated or contributor-permissioned records are available.",
            "records": 0,
        }
    rows_by_id = set()
    texts = set()
    input_files = []
    output.mkdir(parents=True)
    (output / "data").mkdir()
    shards = []
    batch = []
    record_count = token_count = reviewed_count = 0
    for path in files:
        payload_hash = sha256_bytes(path.read_bytes())
        file_records = 0
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    raise ValueError(f"blank line in {path}:{line_number}")
                source_row = json.loads(line)
                row = normalize_row(source_row, sources)
                if row["id"] in rows_by_id:
                    raise ValueError(f"duplicate Klam record ID: {row['id']}")
                text_key = canonical(row["text"])
                if text_key in texts:
                    raise ValueError(f"duplicate Klam text at {path}:{line_number}")
                rows_by_id.add(row["id"])
                texts.add(text_key)
                batch.append(row)
                record_count += 1
                file_records += 1
                token_count += len(row["text"].split())
                reviewed_count += row["review_status"] == "human_reviewed"
                if len(batch) >= SHARD_RECORDS:
                    shards.append(write_shard(output, len(shards) + 1, batch))
                    batch = []
        input_files.append({
            "name": path.name,
            "records": file_records,
            "sha256": payload_hash,
        })
    if batch:
        shards.append(write_shard(output, len(shards) + 1, batch))
    (output / "sources.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksums = [
        f'{item["sha256"]}  {item["path"]}' for item in shards
    ]
    sources_hash = sha256_bytes((output / "sources.json").read_bytes())
    checksums.append(f"{sources_hash}  sources.json")
    (output / "checksums.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    manifest = {
        "dataset": "Klam (کلام)",
        "schema_version": "1.0",
        "format": "JSONL.GZ",
        "record_count": record_count,
        "whitespace_delimited_tokens": token_count,
        "human_reviewed_records": reviewed_count,
        "review_status": "mixed" if 0 < reviewed_count < record_count else (
            "human_reviewed" if reviewed_count == record_count else "unreviewed"),
        "license": "Per record: CC-BY-4.0, CC0-1.0, or verified public domain; see row rights fields and sources.json",
        "source_policy": "original, contributor-permissioned, CC0-dedicated, or rights-verified public-domain material only",
        "sources": registry["sources"],
        "input_files": input_files,
        "shards": shards,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "LICENSE").write_text(
        "# Klam data rights\n\n"
        "Original and contributor-permissioned records are released under CC BY 4.0. "
        "Verified public-domain records remain public domain. Every row carries its "
        "rights basis, applicable license, evidence link, and attribution.\n",
        encoding="utf-8")
    (output / "SOURCES.md").write_text(
        "# Klam sources\n\n"
        "Only original, explicitly permissioned, or rights-verified public-domain "
        "records are included. See sources.json for source versions and rights evidence.\n",
        encoding="utf-8")
    (output / "DATASET_CARD.md").write_text(
        "# Klam (کلام)\n\n"
        f"Klam contains {record_count:,} records in one consistent schema.\n\n"
        f"Native-speaker reviewed records: {reviewed_count:,}. "
        "Records without review evidence remain marked unreviewed.\n",
        encoding="utf-8")
    return {"ready": True, **manifest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = build(args.output)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

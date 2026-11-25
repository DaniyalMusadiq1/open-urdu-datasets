"""Build one normalized Klam release from pinned, rights-cleared Urdu sources."""
import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import sqlite3
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = ROOT / "datasets/klam"
SOURCE_REGISTRY = INPUT_ROOT / "sources.json"
RECORD_ROOT = INPUT_ROOT / "records"
PHASE2_ROOT = Path(os.environ.get("PHASE2_RELEASE_ROOT", ROOT / "artifacts/phase2-release"))
SHARD_RECORDS = 50_000
CC_BY_4 = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_SA_4 = "https://creativecommons.org/licenses/by-sa/4.0/"
CC0_1 = "https://creativecommons.org/publicdomain/zero/1.0/"
LICENSE_RULES = {
    "original": ("CC-BY-4.0", CC_BY_4),
    "contributor_permission": ("CC-BY-4.0", CC_BY_4),
    "cc_by": ("CC-BY-4.0", CC_BY_4),
    "cc_by_2_fr": ("CC-BY-2.0-FR", "https://creativecommons.org/licenses/by/2.0/fr/"),
    "cc_by_sa": ("CC-BY-SA-4.0", CC_BY_SA_4),
    "cc0": ("CC0-1.0", CC0_1),
    "public_domain": ("Public-Domain", ""),
}
EXTRA_SOURCES = {"tatoeba-urdu", "wikivoyage-urdu-phrasebook"}


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def read_sources():
    from jsonschema import Draft202012Validator, FormatChecker

    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    entries = registry.get("sources")
    if not isinstance(entries, list):
        raise TypeError("Klam source registry must contain a sources list")
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
        rights_basis = source.get("rights_basis")
        expected_license = LICENSE_RULES.get(rights_basis)
        if expected_license is None:
            raise ValueError(f"{source_id}: unsupported rights_basis")
        if (source.get("license"), source.get("license_url", "")) != expected_license:
            raise ValueError(f"{source_id}: license does not match rights_basis")
        if not source.get("source_version") or not source.get("rights_evidence_url"):
            raise ValueError(f"{source_id}: version and rights evidence are required")
        if not source.get("attribution"):
            raise ValueError(f"{source_id}: attribution text is required")
        if (rights_basis in {"original", "contributor_permission", "cc0"}
                and source.get("permission_evidence_recorded") is not True):
            raise ValueError(f"{source_id}: permission/dedication evidence is missing")
        sources[source_id] = source
    return registry, sources


def script_for(text):
    arabic = sum("\u0600" <= char <= "\u06ff" and char.isalpha() for char in text)
    latin = sum(char.isalpha() and char.isascii() for char in text)
    if arabic and latin:
        return "Mixed"
    return "Arabic" if arabic else "Latin"


def normalize_row(row, source_id, source, *, source_record_id=None,
                  source_locator="", task="text", label=None,
                  paired_text=None, paired_script=None):
    text = row.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("record text must be a nonempty string")
    record_id = source_record_id or str(row.get("source_record_id") or row.get("id") or "")
    if not record_id:
        raise ValueError(f"{source_id}: source_record_id must be stable and nonempty")
    title = row.get("title")
    if title is None:
        title = ""
    if not isinstance(title, str):
        title = str(title)
    review_status = row.get("review_status", "unreviewed")
    if review_status not in {"unreviewed", "human_reviewed"}:
        raise ValueError(f"invalid review_status for {record_id}")
    reviewer_id = row.get("reviewer_id", "")
    review_date = row.get("review_date", "")
    review_scope = row.get("review_scope", "")
    if review_status == "human_reviewed" and not all((reviewer_id, review_date, review_scope)):
        raise ValueError(f"human-reviewed record lacks review evidence: {record_id}")
    if paired_text is not None and (
            not isinstance(paired_text, str) or not paired_text.strip() or not paired_script):
        raise ValueError(f"invalid paired text for {record_id}")
    if task == "transliteration_pair" and paired_text is None:
        raise ValueError(f"transliteration pair lacks paired text: {record_id}")
    split = str(row.get("split") or "train")
    if split in {"dev", "valid"}:
        split = "validation"
    if split not in {"train", "validation", "test"}:
        raise ValueError(f"unsupported split for {record_id}: {split}")
    digest_input = source_id + "\0" + record_id + "\0" + canonical(text)
    normalized = {
        "id": sha256_bytes(digest_input.encode("utf-8")),
        "title": title,
        "text": text,
        "language": "ur",
        "script": row.get("script") or script_for(text),
        "task": task,
        "label": str(label if label is not None else row.get("label") or ""),
        "split": split,
        "source_id": source_id,
        "source_version": source["source_version"],
        "source_record_id": record_id,
        "source_locator": source_locator or str(row.get("source_locator") or ""),
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
    if paired_text is not None:
        normalized["paired_text"] = paired_text
        normalized["paired_script"] = paired_script
    return normalized


def dedup_key(row):
    text = canonical(row["text"])
    paired = canonical(row["paired_text"]) if row.get("paired_text") else ""
    digest = sha256_bytes((text + "\0" + paired).encode("utf-8"))
    return digest, row["task"], row["label"]


def adapt_source_row(source_id, row, source):
    if source_id == "tatoeba-urdu":
        author = row["author"].strip()
        if not author:
            raise ValueError("Tatoeba sentences require an author")
        record = normalize_row(row, source_id, source)
        record["attribution"] += f" {author}."
        return record
    if source_id == "wikivoyage-urdu-phrasebook":
        return normalize_row(
            row, source_id, source, task="transliteration_pair", label="phrase",
            paired_text=row["paired_text"], paired_script=script_for(row["paired_text"]))
    if source_id == "ghalib-kulliyat-cc0":
        return normalize_row(row, source_id, source)
    if source_id == "dakshina-urdu-sentence-pairs":
        return normalize_row(
            row, source_id, source, task="transliteration_pair", label="sentence",
            paired_text=row["paired_text"], paired_script=script_for(row["paired_text"]))
    if source_id == "dakshina-urdu-bulk":
        details = row.get("source") or {}
        member = details.get("member", "")
        line = details.get("line", "")
        locator = details.get("revision_url") or details.get("page_url") or ""
        if locator.startswith("http://"):
            locator = "https://" + locator.removeprefix("http://")
        if row.get("record_type") == "romanization_pair":
            return normalize_row(
                row, source_id, source,
                source_record_id=f"{member}:{line}:{row.get('id', '')}",
                source_locator=locator, task="transliteration_pair",
                paired_text=row.get("roman"), paired_script="Latin", label="")
        return normalize_row(
            row, source_id, source,
            source_record_id=f"{member}:{line}:{row.get('id', '')}",
            source_locator=locator, label=row.get("record_type", ""))
    if source_id == "uci-roman-urdu-sentiment":
        source_record = f"{row.get('source_id', '')}:{row.get('source_row', '')}"
        return normalize_row(
            row, source_id, source, source_record_id=source_record,
            source_locator=row.get("source_url", ""), task="sentiment_classification",
            label=row.get("source_label", row.get("sentiment", "")))
    if source_id == "urwikisource-pd-old":
        return normalize_row(
            row, source_id, source,
            source_record_id=f"{row.get('source_url', '')}@{row.get('revision_id', '')}",
            source_locator=row.get("revision_url", ""), label="")
    if source_id == "urwiki-articles":
        return normalize_row(
            row, source_id, source,
            source_record_id=f"{row.get('page_id', '')}@{row.get('revision_id', '')}",
            source_locator=row.get("revision_url", ""), label="encyclopedia")
    if source_id in {"sangraha-verified-urdu-r1", "sangraha-verified-urdu-r2"}:
        source_file = str(row.get("source_file") or "")
        doc_id = str(row.get("source_doc_id") or row.get("id") or "")
        revision = source["source_version"]
        locator = (
            "https://huggingface.co/datasets/ai4bharat/sangraha/tree/"
            + revision + "/" + source_file
        )
        return normalize_row(
            row, source_id, source,
            source_record_id=f"{source_file}:{doc_id}",
            source_locator=locator, label=row.get("source_type", ""))
    raise ValueError(f"no Klam source adapter for {source_id}")


def manifest_files(root):
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("review_status") == "human_reviewed" and not manifest.get("human_verified_records"):
        raise ValueError(f"inconsistent review metadata in {manifest_path}")
    files = []
    for shard in manifest.get("shards", []):
        path = root / shard["path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        payload_hash = sha256_bytes(path.read_bytes())
        if payload_hash != shard.get("sha256"):
            raise ValueError(f"source shard checksum mismatch: {path}")
        files.append((path, payload_hash))
    if not files:
        raise ValueError(f"no data shards in {manifest_path}")
    return manifest, files


def source_inputs(phase2_root):
    dakshina_root = phase2_root / "dakshina-urdu-bulk"
    if not dakshina_root.is_dir():
        dakshina_root = ROOT / "datasets/corpora/dakshina-urdu-bulk"
    roots = [
        ("dakshina-urdu-bulk", dakshina_root),
        ("urwikisource-pd-old", ROOT / "datasets/corpora/urwikisource-pd-old"),
        ("uci-roman-urdu-sentiment", ROOT / "datasets/classification/uci-roman-urdu-sentiment"),
        ("urwiki-articles", phase2_root / "urwiki-articles"),
        ("sangraha-verified-urdu-r1", phase2_root / "sangraha-verified-urdu"),
        ("sangraha-verified-urdu-r1", phase2_root / "sangraha-verified-urdu-data-1"),
    ]
    roots.extend(
        ("sangraha-verified-urdu-r2", phase2_root / f"sangraha-verified-urdu-data-{index}")
        for index in range(2, 27)
    )
    result = []
    for source_id, root in roots:
        manifest, files = manifest_files(root)
        result.extend((source_id, path, digest, manifest) for path, digest in files)
    tracked_sources = {
        "dakshina-urdu-sentence-pairs.jsonl.gz": "dakshina-urdu-sentence-pairs",
        "ghalib-cc0.jsonl.gz": "ghalib-kulliyat-cc0",
    }
    tracked_sources.update({f"{source_id}.jsonl.gz": source_id for source_id in sorted(EXTRA_SOURCES)})
    for filename, source_id in tracked_sources.items():
        path = RECORD_ROOT / filename
        result.append((source_id, path, sha256_bytes(path.read_bytes()), None))
    return result


def write_shard(output, index, rows, split):
    relative = f"data/{split}/klam-{index:05d}.jsonl.gz"
    path = output / relative
    path.parent.mkdir(parents=True, exist_ok=True)
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
        "split": split,
    }


def build(output, phase2_root=PHASE2_ROOT, cleanup_phase2_inputs=False):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    registry, sources = read_sources()
    inputs = source_inputs(Path(phase2_root))
    extra_digests = set()
    for source_id, path, _, _ in inputs:
        if source_id in EXTRA_SOURCES:
            with gzip.open(path, "rt", encoding="utf-8") as stream:
                for line in stream:
                    row = adapt_source_row(source_id, json.loads(line), sources[source_id])
                    extra_digests.add(dedup_key(row)[0])
    seen_path = output / ".dedup.sqlite3"
    seen_db = sqlite3.connect(seen_path)
    seen_db.execute("PRAGMA journal_mode=OFF")
    seen_db.execute("PRAGMA synchronous=OFF")
    seen_db.execute("CREATE TABLE seen_text (digest TEXT, task TEXT, label TEXT, PRIMARY KEY (digest, task, label))")
    seen_db.execute("CREATE TABLE seen_ids (id TEXT PRIMARY KEY)")
    cursor = seen_db.cursor()
    input_files = []
    shards = []
    batches = {}
    shard_indices = {}
    record_count = token_count = paired_token_count = reviewed_count = duplicate_count = 0
    records_by_task = {}
    records_by_source = {}
    duplicates_by_source = {}
    licenses = {}
    for input_index, (source_id, path, payload_hash, _manifest) in enumerate(inputs, 1):
        file_read = file_kept = 0
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    raise ValueError(f"blank line in {path}:{line_number}")
                source_row = json.loads(line)
                row = adapt_source_row(source_id, source_row, sources[source_id])
                file_read += 1
                key = dedup_key(row)
                digest = key[0]
                if source_id in EXTRA_SOURCES and digest not in extra_digests:
                    duplicate_count += 1
                    duplicates_by_source[source_id] = duplicates_by_source.get(source_id, 0) + 1
                    continue
                extra_digests.discard(digest)
                cursor.execute("INSERT OR IGNORE INTO seen_text VALUES (?, ?, ?)", key)
                if cursor.rowcount == 0:
                    duplicate_count += 1
                    duplicates_by_source[source_id] = duplicates_by_source.get(source_id, 0) + 1
                    continue
                cursor.execute("INSERT OR IGNORE INTO seen_ids VALUES (?)", (row["id"],))
                if cursor.rowcount == 0:
                    raise ValueError(f"duplicate Klam record ID: {row['id']}")
                batch = batches.setdefault(row["split"], [])
                batch.append(row)
                record_count += 1
                file_kept += 1
                token_count += len(row["text"].split())
                paired_token_count += len(row.get("paired_text", "").split())
                records_by_task[row["task"]] = records_by_task.get(row["task"], 0) + 1
                reviewed_count += row["review_status"] == "human_reviewed"
                records_by_source[source_id] = records_by_source.get(source_id, 0) + 1
                licenses[row["license"]] = licenses.get(row["license"], 0) + 1
                if len(batch) >= SHARD_RECORDS:
                    shard_indices[row["split"]] = shard_indices.get(row["split"], 0) + 1
                    shards.append(write_shard(
                        output, shard_indices[row["split"]], batch, row["split"]))
                    batches[row["split"]] = []
                if record_count % 10_000 == 0:
                    seen_db.commit()
        input_files.append({
            "source_id": source_id,
            "name": path.name,
            "records_read": file_read,
            "records_kept": file_kept,
            "sha256": payload_hash,
        })
        if cleanup_phase2_inputs and path.is_relative_to(Path(phase2_root)):
            path.unlink(missing_ok=True)
    for split, batch in sorted(batches.items()):
        if batch:
            shard_indices[split] = shard_indices.get(split, 0) + 1
            shards.append(write_shard(output, shard_indices[split], batch, split))
    seen_db.close()
    seen_path.unlink(missing_ok=True)
    seen_path.with_name(seen_path.name + "-journal").unlink(missing_ok=True)
    sources_path = output / "sources.json"
    sources_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksums = [f'{item["sha256"]}  {item["path"]}' for item in shards]
    checksums.append(f'{sha256_bytes(sources_path.read_bytes())}  sources.json')
    (output / "checksums.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    split_counts = {
        split: sum(shard["records"] for shard in shards if shard["split"] == split)
        for split in sorted({shard["split"] for shard in shards})
    }
    manifest = {
        "dataset": "Klam (کلام)",
        "schema_version": "1.1",
        "format": "JSONL.GZ",
        "record_count": record_count,
        "exact_duplicate_records_removed": duplicate_count,
        "whitespace_delimited_tokens": token_count,
        "paired_whitespace_delimited_tokens": paired_token_count,
        "task_record_counts": records_by_task,
        "split_record_counts": split_counts,
        "human_reviewed_records": reviewed_count,
        "review_status": "mixed" if 0 < reviewed_count < record_count else (
            "human_reviewed" if reviewed_count == record_count else "unreviewed"),
        "license": "Mixed; the license and license_url on each record are authoritative. Klam preserves source terms and does not relicense source text.",
        "source_policy": "Pinned source records with explicit CC0, CC BY, CC BY-SA, or public-domain rights evidence",
        "source_record_counts": records_by_source,
        "exact_duplicates_removed_by_source": duplicates_by_source,
        "license_record_counts": licenses,
        "sources": registry["sources"],
        "input_files": input_files,
        "shards": shards,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "LICENSE").write_text(
        "# Klam data rights\n\n"
        "Klam is a mixed-license collection. Each record carries its own license, license URL, "
        "rights evidence and attribution. Keep those fields with the text when redistributing. "
        "CC BY-SA records retain their share-alike obligations. CC BY records require attribution. "
        "CC0 records remain under CC0; public-domain records remain public domain. Klam does "
        "not replace or remove any source license.\n",
        encoding="utf-8")
    source_lines = ["# Klam sources", "", "The release combines the listed pinned sources in one record format.", ""]
    for source in registry["sources"]:
        count = records_by_source.get(source["source_id"], 0)
        source_lines.extend([
            f"## {source['title']}",
            "",
            f"- Klam records: {count:,}",
            f"- Version: `{source['source_version']}`",
            f"- License: {source['license']}",
            f"- Source: {source['source_url']}",
            f"- Rights evidence: {source['rights_evidence_url']}",
            f"- Attribution: {source['attribution']}",
            "",
        ])
    (output / "SOURCES.md").write_text("\n".join(source_lines), encoding="utf-8")
    source_table = "\n".join(
        f"| {source['title']} | {records_by_source.get(source['source_id'], 0):,} | {source['license']} |"
        for source in registry["sources"])
    task_table = "\n".join(
        f"| `{task}` | {count:,} |" for task, count in sorted(records_by_task.items()))
    (output / "DATASET_CARD.md").write_text(
        "# Klam (کلام)\n\n"
        f"Klam contains {record_count:,} deduplicated Urdu records from "
        f"{len(registry['sources'])} traceable sources, all in one schema.\n\n"
        f"Transliteration pairs: {records_by_task.get('transliteration_pair', 0):,}. "
        "For these rows, `text` is the source side and `paired_text` is the linked "
        "Roman Urdu side; check `script` and `paired_script` for direction. The `sentence` "
        "label identifies full Dakshina sentence pairs.\n\n"
        f"Records by split: {', '.join(f'{name} {count:,}' for name, count in split_counts.items())}.\n\n"
        "Source train, validation, and test rows are packaged into separate Hugging Face "
        "splits. Validation and test rows are excluded from the train split. "
        "Dakshina sentence pairs originate from Wikipedia. Their Urdu text may overlap "
        "other source corpora, so the splits do not establish contamination-free evaluation.\n\n"
        f"Native-speaker reviewed records: {reviewed_count:,}. Records without evidence "
        "remain `unreviewed`. Duplicate records with matching task and label were removed "
        "after NFC normalization and whitespace collapse; similar text may remain.\n\n"
        "## Tasks\n\n| Task | Records |\n| --- | ---: |\n"
        + task_table + "\n\n## Sources\n\n"
        "| Source | Records | License |\n| --- | ---: | --- |\n"
        + source_table + "\n",
        encoding="utf-8")
    if cleanup_phase2_inputs:
        phase2_root = Path(phase2_root).resolve()
        for child in phase2_root.iterdir():
            if child.resolve() == output.resolve():
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    return {"ready": True, **manifest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--phase2-root", default=str(PHASE2_ROOT))
    parser.add_argument("--cleanup-phase2-inputs", action="store_true")
    args = parser.parse_args()
    result = build(args.output, args.phase2_root, args.cleanup_phase2_inputs)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()


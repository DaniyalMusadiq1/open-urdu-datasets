"""Validate a complete local Klam release, including provenance and row counts."""
import argparse
import gzip
import json
import sqlite3
import tempfile
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

if __package__:
    from scripts.build_klam_release import canonical, dedup_key, sha256_bytes
else:
    from build_klam_release import canonical, dedup_key, sha256_bytes


ROOT = Path(__file__).resolve().parents[1]


def validate(folder):
    folder = Path(folder).resolve()
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    registry = json.loads((folder / "sources.json").read_text(encoding="utf-8"))
    if registry.get("sources") != manifest.get("sources"):
        raise ValueError("manifest and sources.json differ")
    source_map = {source["source_id"]: source for source in registry["sources"]}
    schema = json.loads((ROOT / "schemas/klam-record.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    records = Counter()
    tokens = paired_tokens = 0
    checksums = {}
    checksum_path = folder / "checksums.sha256"
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if relative in checksums:
            raise ValueError("duplicate checksum entry: " + relative)
        checksums[relative] = digest
    expected_paths = {item["path"] for item in manifest["shards"]} | {"sources.json"}
    if set(checksums) != expected_paths:
        raise ValueError("checksum paths do not match manifest")
    if sha256_bytes((folder / "sources.json").read_bytes()) != checksums["sources.json"]:
        raise ValueError("source registry checksum mismatch")
    reviewed_records = 0
    with tempfile.TemporaryDirectory() as directory:
        db = sqlite3.connect(str(Path(directory) / "dedup.sqlite"))
        db.execute("CREATE TABLE seen (digest TEXT, task TEXT, label TEXT, "
                   "PRIMARY KEY (digest, task, label))")
        db.execute("CREATE TABLE seen_ids (id TEXT PRIMARY KEY)")
        try:
            for shard in manifest["shards"]:
                relative = Path(shard["path"])
                path = (folder / relative).resolve()
                if not path.is_relative_to(folder) or not path.is_file():
                    raise ValueError("unsafe or missing shard: " + str(relative))
                payload_hash = sha256_bytes(path.read_bytes())
                if (payload_hash != shard["sha256"]
                        or checksums[str(relative)] != payload_hash
                        or path.stat().st_size != shard["bytes"]):
                    raise ValueError("shard checksum mismatch: " + str(relative))
                shard_records = 0
                with gzip.open(path, "rt", encoding="utf-8") as stream:
                    for line in stream:
                        row = json.loads(line)
                        validator.validate(row)
                        source = source_map.get(row["source_id"])
                        if source is None:
                            raise ValueError("record has unknown source_id")
                        for field in ("source_version", "rights_basis", "license",
                                      "license_url", "rights_evidence_url", "attribution"):
                            if row[field] != source.get(field, ""):
                                raise ValueError(f"source metadata mismatch: {field}")
                        expected_id = sha256_bytes((
                            row["source_id"] + "\0" + row["source_record_id"] + "\0"
                            + canonical(row["text"])
                        ).encode("utf-8"))
                        if row["id"] != expected_id:
                            raise ValueError("invalid record ID")
                        if (row["review_status"] == "human_reviewed"
                                and not all((row["reviewer_id"], row["review_date"],
                                             row["review_scope"]))):
                            raise ValueError("human-reviewed record lacks review evidence")
                        try:
                            db.execute("INSERT INTO seen_ids VALUES (?)", (row["id"],))
                        except sqlite3.IntegrityError as error:
                            raise ValueError("repeated record ID") from error
                        key = dedup_key(row)
                        try:
                            db.execute("INSERT INTO seen VALUES (?, ?, ?)", key)
                        except sqlite3.IntegrityError as error:
                            raise ValueError("exact duplicate record remains") from error
                        records["total"] += 1
                        records["source:" + row["source_id"]] += 1
                        records["task:" + row["task"]] += 1
                        records["license:" + row["license"]] += 1
                        if row["split"] != shard["split"]:
                            raise ValueError("record split differs from shard split")
                        records["split:" + row["split"]] += 1
                        reviewed_records += row["review_status"] == "human_reviewed"
                        count = len(row["text"].split())
                        tokens += count
                        if row.get("paired_text"):
                            paired_count = len(row["paired_text"].split())
                            paired_tokens += paired_count
                        shard_records += 1
                if shard_records != shard["records"]:
                    raise ValueError("shard record count mismatch: " + str(relative))
        finally:
            db.close()
    if records["total"] != manifest["record_count"]:
        raise ValueError("manifest record count mismatch")
    if reviewed_records != manifest["human_reviewed_records"]:
        raise ValueError("human-review count differs from manifest")
    if tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("main-text token count mismatch")
    if paired_tokens != manifest.get("paired_whitespace_delimited_tokens", 0):
        raise ValueError("paired-text token count mismatch")
    if {key.removeprefix("source:"): value for key, value in records.items()
            if key.startswith("source:")} != manifest["source_record_counts"]:
        raise ValueError("source counts differ from manifest")
    if {key.removeprefix("task:"): value for key, value in records.items()
            if key.startswith("task:")} != manifest.get("task_record_counts", {}):
        raise ValueError("task counts differ from manifest")
    if {key.removeprefix("license:"): value for key, value in records.items()
            if key.startswith("license:")} != manifest["license_record_counts"]:
        raise ValueError("license counts differ from manifest")
    if {key.removeprefix("split:"): value for key, value in records.items()
            if key.startswith("split:")} != manifest["split_record_counts"]:
        raise ValueError("split counts differ from manifest")
    return {
        "records": records["total"],
        "whitespace_delimited_tokens": tokens,
        "paired_whitespace_delimited_tokens": paired_tokens,
        "tasks": {key.removeprefix("task:"): value for key, value in records.items()
                  if key.startswith("task:")},
        "splits": {key.removeprefix("split:"): value for key, value in records.items()
                   if key.startswith("split:")},
        "integrity": "ok",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.release), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

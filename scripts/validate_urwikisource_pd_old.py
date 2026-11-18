"""Validate the file-level integrity and record invariants of the Wikisource release."""
import gzip
import hashlib
import json
import sys
from pathlib import Path


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def validate(root):
    root = Path(root)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("review_status") != "unreviewed" or manifest.get("human_verified_records") != 0:
        raise ValueError("review status must remain explicitly unreviewed")
    if manifest.get("status") not in {"local_unpublished", "published"}:
        raise ValueError("unexpected corpus status")
    lines = (root / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    expected_checksums = {}
    for line in lines:
        digest, path = line.split("  ", 1)
        if path in expected_checksums:
            raise ValueError("duplicate checksum entry: " + path)
        expected_checksums[path] = digest
    shard_paths = {item["path"] for item in manifest["shards"]}
    if shard_paths != set(expected_checksums):
        raise ValueError("manifest and checksum shard lists differ")
    seen = set()
    records = tokens = 0
    for shard in manifest["shards"]:
        path = root / shard["path"]
        if sha256(path) != shard["sha256"] or shard["sha256"] != expected_checksums[shard["path"]]:
            raise ValueError("checksum mismatch: " + shard["path"])
        shard_records = shard_tokens = 0
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if row.get("work_status") != "PD-old" or row.get("license") != "CC-BY-SA-4.0":
                    raise ValueError("rights metadata mismatch")
                if row.get("review_status") != "unreviewed":
                    raise ValueError("records must remain unreviewed")
                for field in ("source_url", "revision_url", "history_url"):
                    if not row.get(field, "").startswith("https://ur.wikisource.org/"):
                        raise ValueError("missing HTTPS provenance: " + field)
                identity = row["id"]
                if identity in seen:
                    raise ValueError("duplicate text identity: " + identity)
                seen.add(identity)
                if row["token_count_whitespace"] != len(row["text"].split()):
                    raise ValueError("token count mismatch")
                shard_records += 1
                shard_tokens += row["token_count_whitespace"]
        if shard_records != shard["records"] or shard_tokens != shard["tokens"]:
            raise ValueError("shard count mismatch: " + shard["path"])
        records += shard_records
        tokens += shard_tokens
    if records != manifest["record_count"] or tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("manifest total mismatch")
    print(json.dumps({"records": records, "whitespace_delimited_tokens": tokens,
                      "shards": len(manifest["shards"]), "integrity": "ok"}))


if __name__ == "__main__":
    try:
        validate(sys.argv[1])
    except (IndexError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"Wikisource release validation failed: {error}") from error

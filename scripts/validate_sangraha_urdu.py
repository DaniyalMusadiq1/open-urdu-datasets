"""Validate integrity, license metadata, and language-filter provenance."""
import gzip
import hashlib
import json
import sys
import unicodedata
from pathlib import Path


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def validate(root):
    root = Path(root)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    seen, records, tokens = set(), 0, 0
    for shard in manifest["shards"]:
        path = root / shard["path"]
        if digest(path) != shard["sha256"]:
            raise ValueError("shard SHA-256 mismatch: " + shard["path"])
        shard_records = shard_tokens = 0
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = row["text"]
                identity = hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()
                if identity != row["id"] or identity in seen:
                    raise ValueError("identity mismatch or duplicate text")
                seen.add(identity)
                if row.get("license") != "CC-BY-4.0" or row.get("review_status") != "unreviewed":
                    raise ValueError("license or review status is missing/incorrect")
                if (not str(row.get("language_id", "")).endswith(":ur")
                        or row.get("language_id_confidence", 0) < 0.70):
                    raise ValueError("language identification provenance is invalid")
                if not row.get("source_doc_id") or not row.get("source_type"):
                    raise ValueError("upstream document attribution fields are missing")
                count = len(text.split())
                if count != row.get("token_count_whitespace"):
                    raise ValueError("record token count mismatch")
                shard_records += 1
                shard_tokens += count
        if shard_records != shard["records"] or shard_tokens != shard["tokens"]:
            raise ValueError("shard counts mismatch")
        records += shard_records
        tokens += shard_tokens
    if records != manifest["record_count"] or tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("manifest totals mismatch")
    print(json.dumps({"records": records, "whitespace_delimited_tokens": tokens,
                      "shards": len(manifest["shards"]), "integrity": "ok"}))


if __name__ == "__main__":
    try:
        validate(sys.argv[1])
    except (IndexError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"Sangraha Urdu release validation failed: {error}") from error

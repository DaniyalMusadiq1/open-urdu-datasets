"""Validate integrity and record provenance for the Urdu Wikipedia release."""
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
    if manifest.get("review_status") != "unreviewed" or manifest.get("human_verified_records") != 0:
        raise ValueError("review status must remain explicitly unreviewed")
    if manifest.get("status") not in {"local_unpublished", "published"}:
        raise ValueError("unexpected corpus status")
    check_lines = (root / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    checksums = {}
    for line in check_lines:
        value, path = line.split("  ", 1)
        if path in checksums:
            raise ValueError("duplicate checksum entry")
        checksums[path] = value
    if set(checksums) != {item["path"] for item in manifest["shards"]}:
        raise ValueError("checksum and manifest shard lists differ")
    seen = set()
    records = tokens = 0
    for shard in manifest["shards"]:
        path = root / shard["path"]
        if digest(path) != shard["sha256"] or checksums[shard["path"]] != shard["sha256"]:
            raise ValueError("checksum mismatch: " + shard["path"])
        row_count = token_count = 0
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if row.get("license") != "CC-BY-SA-4.0":
                    raise ValueError("license metadata mismatch")
                if row.get("review_status") != "unreviewed":
                    raise ValueError("records must remain unreviewed")
                for field in ("source_url", "revision_url", "history_url"):
                    if not row.get(field, "").startswith("https://ur.wikipedia.org/"):
                        raise ValueError("missing source attribution link: " + field)
                if row.get("source_markup_removed") is not True:
                    raise ValueError("modification disclosure missing")
                normalized = canonical(row["text"]).encode("utf-8")
                identity = hashlib.sha256(normalized).hexdigest()
                if identity != row["id"] or identity in seen:
                    raise ValueError("identity mismatch or duplicate")
                seen.add(identity)
                if row["token_count_whitespace"] != len(row["text"].split()):
                    raise ValueError("token count mismatch")
                row_count += 1
                token_count += row["token_count_whitespace"]
        if row_count != shard["records"] or token_count != shard["tokens"]:
            raise ValueError("shard counts mismatch")
        records += row_count
        tokens += token_count
    if records != manifest["record_count"] or tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("manifest totals mismatch")
    print(json.dumps({"records": records, "whitespace_delimited_tokens": tokens,
                      "shards": len(manifest["shards"]), "integrity": "ok"}))


if __name__ == "__main__":
    try:
        validate(sys.argv[1])
    except (IndexError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"Urdu Wikipedia release validation failed: {error}") from error

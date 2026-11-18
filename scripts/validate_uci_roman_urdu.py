"""Verify the UCI Roman Urdu release's counts, identity, provenance, and hashes."""
import gzip
import hashlib
import argparse
import json
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FOLDER = ROOT / "datasets/classification/uci-roman-urdu-sentiment"


def main(folder=DEFAULT_FOLDER):
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    seen = set()
    labels = Counter()
    count = tokens = 0
    shard_records = Counter()
    shard_tokens = Counter()
    for shard in manifest["shards"]:
        path = folder / shard["path"]
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != shard["sha256"]:
            raise ValueError("shard checksum mismatch")
        if len(payload) != shard["bytes"]:
            raise ValueError("shard byte count mismatch")
        shard_count = shard_token_count = 0
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                for field in ("text", "id", "source_id", "source_row", "source_doi", "source_url", "license", "sentiment", "source_label", "review_status", "token_count_whitespace"):
                    if field not in row:
                        raise ValueError(f"missing field: {field}")
                canonical = " ".join(unicodedata.normalize("NFC", row["text"]).split())
                identity = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
                if identity != row["id"]:
                    raise ValueError("record identity mismatch")
                if row["id"] in seen:
                    raise ValueError("duplicate record")
                seen.add(row["id"])
                if row["license"] != "CC-BY-4.0" or row["review_status"] != "unreviewed":
                    raise ValueError("unapproved license or review claim")
                if row["sentiment"] != row["source_label"].lower():
                    raise ValueError("source label changed")
                expected = {"UCI-458": "10.24432/C58325", "UCI-854": "10.24432/C59046"}
                if row["source_id"] not in expected or row["source_doi"] != expected[row["source_id"]]:
                    raise ValueError("unknown source provenance")
                actual_tokens = len(row["text"].split())
                if row["token_count_whitespace"] != actual_tokens:
                    raise ValueError("token count mismatch")
                count += 1
                tokens += actual_tokens
                shard_count += 1
                shard_token_count += actual_tokens
                shard_records[row["source_id"]] += 1
                shard_tokens[row["source_id"]] += actual_tokens
                labels[(row["source_id"], row["source_label"])] += 1
        if shard_count != shard["records"] or shard_token_count != shard["tokens"]:
            raise ValueError("shard count mismatch")
    if count != manifest["record_count"] or tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("manifest total mismatch")
    expected_sources = {"458": 16713, "854": 10393}
    if shard_records != Counter({"UCI-458": expected_sources["458"], "UCI-854": expected_sources["854"]}):
        raise ValueError("source-level record totals differ")
    print(json.dumps({"records": count, "whitespace_delimited_tokens": tokens,
                      "source_records": dict(shard_records),
                      "labels": {f"{source}:{label}": value
                                for (source, label), value in labels.items()},
                      "human_verified_records": 0, "errors": 0}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=str(DEFAULT_FOLDER))
    main(parser.parse_args().folder)

"""Stream every bulk record through its schema, identity and content checks."""
import gzip
import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

from urdu_data.bulk import flags, identity
from urdu_data.core import sha256, verify_checksums

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "datasets/corpora/dakshina-urdu-bulk"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/dakshina-bulk.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    seen = set()
    counts = Counter()
    words = Counter()
    for shard in manifest["shards"]:
        path = (folder / shard["path"]).resolve()
        if not path.is_relative_to(folder.resolve()) or path.stat().st_size >= 20_000_000:
            raise ValueError("unsafe or oversized bulk shard")
        if sha256(path) != shard["sha256"]:
            raise ValueError("bulk shard checksum mismatch")
        records = 0
        with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
            for line in stream:
                row = json.loads(line)
                validator.validate(row)
                if row["record_type"] != shard["kind"] or row["split"] != shard["split"]:
                    raise ValueError("shard type/split mismatch")
                key = identity(row["record_type"], row["text"], row["roman"])
                if key != row["id"] or key in seen:
                    raise ValueError("invalid or duplicate content identity")
                if flags(row["text"] + (" " + row["roman"] if row["roman"] else "")):
                    raise ValueError("contact-pattern filter was not applied")
                seen.add(key)
                counts[row["record_type"] + "/" + row["split"]] += 1
                words[row["record_type"]] += len(row["text"].split())
                records += 1
        if records != shard["records"]:
            raise ValueError("shard count mismatch")
        print(json.dumps({"shard": shard["path"], "records": records}), flush=True)
    if dict(counts) != manifest["retained_by_type_split"]:
        raise ValueError("bulk split counts differ")
    if dict(words) != manifest["whitespace_delimited_tokens_by_type"]:
        raise ValueError("bulk word counts differ")
    if len(seen) != manifest["retained_records"]:
        raise ValueError("bulk retained count differs")
    if (folder / "checksums.sha256").exists():
        verify_checksums(folder / "checksums.sha256")
    print(json.dumps({"bulk_records": len(seen), "whitespace_tokens": dict(words),
                      "human_reviewed_records": 0, "errors": 0}), flush=True)


if __name__ == "__main__":
    main()

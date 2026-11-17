"""Validate separately scoped derived samples without inflating upstream counts."""
import json
from pathlib import Path

from urdu_data.core import read_records, sha256, validate, verify_checksums

ROOT = Path(__file__).resolve().parents[1]


def main():
    entries = read_records(ROOT / "catalog/hosted-samples.json")
    schema = json.loads((ROOT / "schemas/catalog-entry.schema.json").read_text(encoding="utf-8"))
    errors = validate(entries, schema)
    if errors:
        raise ValueError(errors)
    vocab = json.loads((ROOT / "schemas/vocabulary.schema.json").read_text(encoding="utf-8"))
    count = 0
    for entry in entries:
        if entry["license"] != "CC-BY-SA-4.0" or not entry["hosted"]:
            raise ValueError("unexpected sample hosting/license")
        if entry["redistribution_status"] != "explicitly_permitted":
            raise ValueError("redistribution permission not established")
        folder = ROOT / entry["local_path"]
        if not folder.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("unsafe path")
        verify_checksums(folder / "checksums.sha256")
        data_path = folder / "data/vocabulary.jsonl"
        if sha256(data_path) != entry["verification_evidence"]["data_sha256"]:
            raise ValueError("sample hash mismatch")
        rows = read_records(data_path)
        if validate(rows, vocab):
            raise ValueError("vocabulary schema failed")
        if len(rows) != entry["size_record_count"]["value"]:
            raise ValueError("sample count mismatch")
        if any(row["review_status"] != "unreviewed" for row in rows):
            raise ValueError("unexpected claim of human review")
        count += len(rows)
    print(json.dumps({"derived_samples": len(entries), "records": count,
                      "human_reviewed_records": 0, "errors": 0}))


if __name__ == "__main__":
    main()

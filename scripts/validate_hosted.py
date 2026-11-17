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
        if entry["id"] == "dakshina-ur-sample":
            filename, schema_name = "vocabulary.jsonl", "vocabulary.schema.json"
        elif entry["id"] == "belebele-ur-en-eval-sample":
            filename, schema_name = "pairs.jsonl", "evaluation-pair.schema.json"
        else:
            raise ValueError("unsupported hosted sample type")
        sample_schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        data_path = folder / "data" / filename
        if sha256(data_path) != entry["verification_evidence"]["data_sha256"]:
            raise ValueError("sample hash mismatch")
        rows = read_records(data_path)
        if validate(rows, sample_schema):
            raise ValueError("sample schema failed")
        if len(rows) != entry["size_record_count"]["value"]:
            raise ValueError("sample count mismatch")
        if any(row["review_status"] != "unreviewed" for row in rows):
            raise ValueError("unexpected claim of human review")
        count += len(rows)
    print(json.dumps({"derived_samples": len(entries), "records": count,
                      "human_reviewed_records": 0, "errors": 0}))


if __name__ == "__main__":
    main()

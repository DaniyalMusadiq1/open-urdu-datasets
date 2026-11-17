"""Validate catalog, typed CSV parity, hosting gates, UTF-8 and file limits."""
import json
from pathlib import Path

from urdu_data.core import decode_csv_cells, read_records, validate, verify_checksums

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"CC0-1.0", "CC-BY-2.0-FR", "CC-BY-3.0", "CC-BY-4.0",
           "CC-BY-SA-3.0", "CC-BY-SA-4.0", "ODbL-1.0"}


def main():
    rows = read_records(ROOT / "catalog/datasets.json")
    schema = json.loads((ROOT / "schemas/catalog-entry.schema.json").read_text(encoding="utf-8"))
    errors = validate(rows, schema)
    if errors:
        raise ValueError("\n".join(errors))
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("duplicate catalog IDs")
    if decode_csv_cells(read_records(ROOT / "catalog/datasets.csv")) != rows:
        raise ValueError("catalog CSV differs from JSON")
    hosted = []
    for row in rows:
        if row["verification_status"] == "verified":
            if not row["verification_evidence"].get("data_sha256"):
                raise ValueError("verified entry lacks data checksum")
        if not row["hosted"]:
            continue
        if row["license"] not in ALLOWED or row["redistribution_status"] != "explicitly_permitted":
            raise ValueError("hosting license gate failed")
        if row["verification_status"] == "unverified":
            raise ValueError("unverified data must not be hosted")
        path = ROOT / row["local_path"]
        if not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("dataset path escapes repository")
        for required in ["DATASET_CARD.md", "LICENSE", "SOURCES.md", "checksums.sha256", "data"]:
            if not (path / required).exists():
                raise ValueError(f"missing {required}")
        verify_checksums(path / "checksums.sha256")
        hosted.extend(path.glob("data/*.jsonl"))
    record_count = 0
    vocab_schema = json.loads((ROOT / "schemas/vocabulary.schema.json").read_text(encoding="utf-8"))
    for path in hosted:
        data = read_records(path)
        errors = validate(data, vocab_schema)
        if errors:
            raise ValueError("\n".join(errors))
        record_count += len(data)
    for parent in ["src", "tests", "scripts", "examples", "catalog", "schemas", "docs", "datasets", ".github"]:
        for path in (ROOT / parent).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                if path.stat().st_size >= 100_000_000:
                    raise ValueError(f"file too large: {path}")
                path.read_text(encoding="utf-8")
    print(json.dumps({"catalog_entries": len(rows), "hosted_files": len(hosted),
                      "hosted_records": record_count, "errors": 0}))


if __name__ == "__main__":
    main()

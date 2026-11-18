"""Report exact text collisions across processed corpora added in this phase."""
import gzip
import argparse
import hashlib
import json
import os
import unicodedata
from pathlib import Path


def identity(text):
    canonical = " ".join(unicodedata.normalize("NFC", text).split())
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def rows(root):
    for path in sorted(root.rglob("*.jsonl*")):
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if isinstance(row, dict):
                    yield row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--existing-root", default="datasets")
    parser.add_argument("--corpora", nargs="+", default=None)
    args = parser.parse_args()
    release_root = Path(os.environ.get("PHASE2_RELEASE_ROOT", "datasets/corpora"))
    roots = ([Path(item) for item in args.corpora] if args.corpora else [
        release_root / "urwiki-articles", release_root / "sangraha-verified-urdu",
        release_root / "sangraha-verified-urdu-data-1"])
    excluded = {path.resolve() for path in roots}
    seen, existing_rows = set(), 0
    for path in Path(args.existing_root).rglob("*.jsonl*"):
        if any(parent in path.resolve().parents for parent in excluded):
            continue
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                existing_rows += 1
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    seen.update(identity(value) for value in row.values()
                                if isinstance(value, str) and value.strip())
    collisions, current, total = [], set(), 0
    for root in roots:
        for row in rows(root):
            total += 1
            text = row.get("text")
            if not isinstance(text, str):
                continue
            key = identity(text)
            if key in seen or key in current:
                collisions.append({"root": str(root), "id": row.get("id"), "hash": key})
            current.add(key)
    print(json.dumps({"new_corpus_records": total, "existing_records_scanned": existing_rows,
                      "exact_cross_corpus_collisions": len(collisions),
                      "collision_examples": collisions[:20]}, indent=2))
    if collisions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

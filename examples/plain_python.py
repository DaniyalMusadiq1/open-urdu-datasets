"""Read the UTF-8 catalog and real hosted samples without network access."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / "catalog/datasets.json").read_text(encoding="utf-8"))
print({"upstream_catalog_entries": len(rows), "full_upstream_datasets_hosted": sum(r["hosted"] for r in rows)})
samples = ["datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl",
           "datasets/translation/belebele-urdu-english-eval-sample/data/pairs.jsonl"]
for sample in samples:
    data = [json.loads(line) for line in (root / sample).read_text(encoding="utf-8").splitlines()]
    print({"sample": sample, "records": len(data),
           "locally_unreviewed": sum(row["review_status"] == "unreviewed" for row in data)})

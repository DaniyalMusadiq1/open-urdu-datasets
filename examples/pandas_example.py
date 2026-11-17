"""Typed CSV: decode each JSON-valued cell before constructing a DataFrame."""
import csv
import json
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
with (root / "catalog/datasets.csv").open(encoding="utf-8", newline="") as stream:
    rows = [{k: json.loads(v) for k, v in row.items()} for row in csv.DictReader(stream)]
frame = pd.DataFrame(rows)
print(frame[["id", "license", "verification_status", "hosted"]].to_string(index=False))
for relative in ["datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl",
                 "datasets/translation/belebele-urdu-english-eval-sample/data/pairs.jsonl"]:
    sample = pd.read_json(root / relative, lines=True, encoding="utf-8")
    print({"sample": relative, "records": len(sample),
           "review_status": sample["review_status"].value_counts().to_dict()})

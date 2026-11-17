"""Load local catalog strings; does not run remote scripts or download corpora."""
from pathlib import Path

from datasets import load_dataset

root = Path(__file__).resolve().parents[1]
# CSV keeps cells as JSON strings; use Python's json.loads to decode individual cells.
data = load_dataset("csv", data_files=str(root / "catalog/datasets.csv"), split="train")
print({"catalog_entries": len(data), "columns": data.column_names})
for relative in ["datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl",
                 "datasets/translation/belebele-urdu-english-eval-sample/data/pairs.jsonl"]:
    sample = load_dataset("json", data_files=str(root / relative), split="train")
    print({"sample": relative, "records": len(sample), "columns": sample.column_names})

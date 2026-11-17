"""Read the UTF-8 discovery catalog without third-party data access."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / "catalog/datasets.json").read_text(encoding="utf-8"))
print({"catalog_entries": len(rows), "hosted_entries": sum(r["hosted"] for r in rows)})

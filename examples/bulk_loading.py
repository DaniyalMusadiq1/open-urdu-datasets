"""Stream real bulk records with standard Python; no external downloads or training."""
import gzip
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "datasets/corpora/dakshina-urdu-bulk"
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
print({"bulk_records": manifest["retained_records"],
       "native_whitespace_tokens": manifest["whitespace_delimited_tokens_by_type"]["native_sentence"]})
for shard in manifest["shards"]:
    with gzip.open(root / shard["path"], "rt", encoding="utf-8") as stream:
        first = json.loads(next(stream))
        assert first["review_status"] == "unreviewed"
    print({"shard": shard["path"], "records": shard["records"]})

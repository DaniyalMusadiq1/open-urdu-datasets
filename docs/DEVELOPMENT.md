# Development and examples

From the repository root, use Python 3.10 or later:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev,examples]'
python scripts/validate_repo.py
python -m pytest
python -m ruff check src tests scripts examples
python examples/plain_python.py
python examples/pandas_example.py
python examples/huggingface_example.py
urdu-data stats catalog/datasets.json
urdu-data duplicates catalog/datasets.json --fields id
urdu-data validate catalog/datasets.json schemas/catalog-entry.schema.json
urdu-data validate catalog/datasets.csv schemas/catalog-entry.schema.json --typed-csv
urdu-data links catalog/datasets.json
```

Link checks use HEAD, a 15-second timeout and no gated-download retries. HTTP 403/405/429 and timeouts are unresolved, not assertions that data is unavailable. The command returns nonzero for any unresolved URL. It does not update catalog statuses. Never interpret a successful HEAD as license or content verification.

Use `urdu-data convert input.jsonl new.csv` to create a typed CSV: every cell is JSON-encoded, including strings and nulls, so nested provenance can round-trip. Decode with `--typed-csv` only for this format. Arbitrary CSV is read as text. Empty datasets have no inferred CSV columns. Output paths must not exist.

`urdu-data normalize input.jsonl new.jsonl --field urdu --nfc` preserves source fields and adds an audit. See [normalization policy](NORMALIZATION.md). Fixtures in tests are synthetic Unicode sequences or English tokens, not Urdu language data.

The examples load the catalog and both hosted samples and do not fetch remote data or execute remote dataset scripts. Dataset-specific loading examples belong in dataset cards once records are cleared for hosting.

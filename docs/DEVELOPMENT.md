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

## Bulk corpus

Run `python examples/bulk_loading.py` to stream an example from each local compressed shard. `python scripts/validate_bulk.py` checks every bulk record against the JSON schema, source-preserving content identity, duplicate constraints, filter rules, counts and checksums. This is separate from the small sample checks. The bulk workflow runs it on GitHub.

To reproduce, download the official Dakshina v1.0 archive linked in the dataset source card, then run `python scripts/import_dakshina_bulk.py ARCHIVE NEW_OUTPUT NEW_WORK.sqlite`. The importer requires the pinned complete-archive SHA-256 and refuses existing outputs. No source scraping, normalization, model generation or training is performed.

## Maintainer workflow and review status

Apply authorized maintenance directly on `main`; do not create task branches unless the maintainer requests one. Run the applicable validations before pushing.

Record review statuses are `unreviewed` and `verified` (formerly `human_verified`). Set `verified` only after an identified human reviewer confirms the specific records; record reviewer, date and reviewed scope in the dataset documentation. Source attestations and automated checks alone do not establish human review. Catalog `verification_status` describes technical source/data verification separately.

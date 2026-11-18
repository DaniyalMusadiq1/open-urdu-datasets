# AI4Bharat Sangraha: verified Urdu shard

This release contains **187,767 records and 114,197,395 whitespace-delimited
tokens**, retained from `verified/urd/data-0.parquet` at the pinned revision in
`manifest.json`. These are mechanically counted whitespace units, not model
tokens. No synthetic or translated partition is included.

The upstream dataset card declares CC BY 4.0. Each row preserves the upstream
document ID and type, pinned dataset revision and file, and that license. The
upstream rows do not expose their original page URLs or creator names, so this
release can attribute records to Sangraha but cannot provide page-level
attribution. Review the source card and assess suitability before reuse.

The import keeps nonempty text with an Arabic-script ratio of at least 0.55,
then retains only fastText `lid.176` Urdu predictions at confidence 0.70 or
higher. This is automated language routing, not Urdu human verification. Short
text and email-pattern matches were excluded as triage; this is not a privacy
guarantee. Text was not corrected or translated. All records remain
`review_status: unreviewed`; native Urdu review is pending.

Exact duplicates were removed by SHA-256 after NFC normalization and whitespace
collapse, against source records already present in the repository and within
this shard. This does not detect semantic or near duplicates. Keep the
record-level license and source fields when redistributing the data.

## Reproduce

Install the `ingest` extra, obtain the source Parquet file and fastText model
listed by SHA-256 in `manifest.json`, then run:

```sh
python scripts/import_sangraha_urdu.py SOURCE.parquet lid.176.ftz OUTPUT_DIR
python scripts/validate_sangraha_urdu.py OUTPUT_DIR
```

The importer refuses unpinned inputs and refuses to overwrite an existing
output directory.

# AI4Bharat Sangraha: verified Urdu shard 1

This release contains **187,578 records and 113,895,936 whitespace-delimited
tokens** retained from `verified/urd/data-1.parquet` at the pinned revision in
`manifest.json`. Whitespace units are not model tokens. No synthetic or
translated partition is included.

The upstream dataset card declares CC BY 4.0. Rows preserve the upstream
document ID and type, pinned dataset revision and file, and that license. The
Parquet rows do not expose original page URLs or creator names, so attribution
is to Sangraha at dataset level. Consult the source card before reuse.

Text is filtered by Arabic-script ratio and fastText `lid.176` Urdu prediction
with confidence of at least 0.70. These are automated filters, not native Urdu
review. Short text and email-pattern matches were excluded as triage, not as a
privacy guarantee. Text was not corrected or translated; every record remains
`review_status: unreviewed` and native review is pending.

Exact duplicates were removed after NFC normalization and whitespace collapse
against repository text available during import and within this source shard.
Semantic or near-duplicate overlap may remain. Preserve row-level license and
source fields on redistribution.

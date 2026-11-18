# Urdu corpus expansion — current status

- Long-range target: 200,000,000,000 whitespace-delimited tokens
- Current separately tracked hosted corpora: 183,472 records / 4,765,116 tokens
- Remaining: 199,995,234,884 whitespace-delimited tokens
- Included sources: Dakshina Urdu native text, UCI Roman Urdu sentiment, and Urdu Wikisource `PD-old` transcriptions
- Human/native-speaker verified records: 0; review remains pending
- Licensing: source-specific; see each corpus card and license notice
- Deduplication: exact NFC-normalized, whitespace-collapsed text only; semantic and near-duplicate overlap may remain
- Quality: reproducible source hashes, per-record provenance, deterministic shards, checksums and mechanical filters; no human linguistic verification

Only the 6,366 Wikisource pages carrying an explicit `{{PD-old}}` tag in the pinned 2026-11-01 export were retained for that source. See the [dataset card](corpora/urwikisource-pd-old/DATASET_CARD.md), [manifest](corpora/urwikisource-pd-old/manifest.json), and [source/license information](corpora/urwikisource-pd-old/SOURCES.md).

The long-range target is not achieved. Public access alone is not permission to republish. Future materials require source-specific redistribution evidence, provenance, deduplication, and quality review. No completeness claim is made for online books or internet data. The count is whitespace-delimited and not a model-token estimate.

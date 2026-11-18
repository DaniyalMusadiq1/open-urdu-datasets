# Corpus expansion status

## Targets and publication state

- Phase milestone: **200,000,000 whitespace-delimited tokens**.
- Overall project target: **1,300,000,000 whitespace-delimited tokens**.
- Currently published corpus total: **183,472 records / 4,765,116 tokens**.
- Validated release candidate addition: **913,295 records / 324,510,494 tokens**.
- Candidate combined total after publication: **1,096,767 records / 329,275,610 tokens**.
- Candidate phase progress: **164.64%**, or **129,275,610 tokens beyond the milestone**.
- Overall target remaining after publication: **970,724,390 tokens**.
- Native Urdu human-verified records: **0**; review remains pending.

The currently published total remains unchanged while the release candidate is
uploaded. The phase milestone will be marked achieved only after GitHub Actions
has rebuilt the pinned sources, uploaded the corpus to Hugging Face and verified
remote file hashes. All counts are whitespace-delimited units, not model-token
counts.

| Source | Records | Whitespace tokens | License |
| --- | ---: | ---: | --- |
| Urdu Wikipedia, 2026-11-01 dump | 537,950 | 96,417,163 | CC BY-SA 4.0 |
| AI4Bharat Sangraha verified Urdu, data-0 | 187,767 | 114,197,395 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-1 | 187,578 | 113,895,936 | CC BY 4.0 declared upstream |

## Source filters and limits

The Wikipedia source is the pinned official 2026-11-01 Urdu Wikipedia export. It
preserves page, revision and history links; filters redirects, common explicit
rights-exception templates and low Arabic-script-ratio pages; and strips
MediaWiki markup. This release is rebuilt from the complete pinned dump. See the
[Wikipedia card](../datasets/corpora/urwiki-articles/DATASET_CARD.md).

The Sangraha additions use only the pinned `verified/urd/data-0.parquet` and
`data-1.parquet` files. The upstream dataset card declares CC BY 4.0. Rows
provide a source document ID and type but no original page URL or creator name.
Text was filtered using Arabic-script ratio and fastText Urdu language
identification at confidence 0.70 or above. This is automated routing, not
native-speaker verification. See the [data-0 card](../datasets/corpora/sangraha-verified-urdu/DATASET_CARD.md)
and [data-1 card](../datasets/corpora/sangraha-verified-urdu-data-1/DATASET_CARD.md).

Exact duplicate checks use SHA-256 over NFC-normalized text after whitespace
collapse. Exact duplicates are removed; semantic or near-duplicate overlap may
remain. Contact-pattern filters are triage only and do not prove that text has
no personal information. No text was corrected or represented as human
verified.

## Reproducing the additions

```sh
python -m pip install -e '.[ingest]'
python scripts/build_phase2_release.py
```

The build downloads only pinned inputs and checks their SHA-256 before import.
It runs per-source validators and a cross-corpus exact-duplicate audit. CI then
publishes the generated records and manifests to Hugging Face and verifies
remote hashes. Native Urdu review remains pending.

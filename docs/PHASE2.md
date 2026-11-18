# Corpus expansion status

## Targets and publication state

- Phase milestone: **1,000,000,000 whitespace-delimited tokens — achieved (100.69%).**
- Overall project target: **1,300,000,000 whitespace-delimited tokens.**
- Published corpus total: **2,217,970 records / 1,006,902,795 whitespace-delimited tokens.**
- Remaining to overall target: **293,097,205 whitespace-delimited tokens.**
- Hugging Face dataset: [Daniyal643/open-urdu-datasets](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets)
- Verified corpus release revision: `1585f7eae6416f6fe5ee8a05e1a2c2731ccd13da`.
- Native Urdu human-verified records: **0**; review remains pending.

Counts are whitespace-delimited units, not model-token counts. GitHub Actions completed the build, validation, upload and remote hash verification. The file-level release manifest records exact source hashes and output checksums.

| Source | Records | Whitespace tokens | License |
| --- | ---: | ---: | --- |
| Urdu Wikipedia, 2026-11-01 dump | 543,011 | 96,417,163 | CC BY-SA 4.0 |
| AI4Bharat Sangraha verified Urdu, data-0 | 187,767 | 114,197,395 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-1 | 187,578 | 113,895,936 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-2 | 187,694 | 114,148,226 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-3 | 187,541 | 113,690,963 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-4 | 178,367 | 107,933,097 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-5 | 187,373 | 113,570,525 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-6 | 187,528 | 113,357,092 | CC BY 4.0 declared upstream |
| AI4Bharat Sangraha verified Urdu, data-7 | 187,639 | 114,927,282 | CC BY 4.0 declared upstream |

## Source filters and limits

The Wikipedia source is the pinned official 2026-11-01 Urdu Wikipedia export. The release preserves page, revision and history links; applies documented rights and language filters; and strips MediaWiki markup. See the [Wikipedia card](../datasets/corpora/urwiki-articles/DATASET_CARD.md).

The Sangraha additions use the pinned upstream revision `654c02de6fa4cff1e3ade4e5c9242bedc7ad7629` and files `verified/urd/data-0.parquet` through `data-7.parquet`. The upstream dataset card declares CC BY 4.0. Some source rows lack original page URLs or creator names; see each release manifest and source notes. Arabic-script and Urdu-language filters are automated routing, not native-speaker verification.

Exact duplicate checks use SHA-256 over NFC-normalized text after whitespace collapse. Semantic or near-duplicate overlap may remain. Contact-pattern filters are triage only and do not prove that text contains no personal information. No text is represented as human-verified.

## Reproducing the additions

```sh
python -m pip install -e '.[ingest]'
python scripts/build_phase2_release.py
```

The build downloads pinned inputs and checks their SHA-256 before import, runs per-source validators and performs a cross-corpus exact-duplicate audit. CI publishes generated records and manifests to Hugging Face and checks remote file hashes.

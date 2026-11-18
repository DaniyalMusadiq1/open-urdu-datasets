# Large corpus release status

This page records the current published bulk corpus. It is an inventory of data and validation evidence, not a data-quality certification.

- Published total: **2,217,970 records / 1,006,902,795 whitespace-delimited tokens**
- Dataset: [Daniyal643/open-urdu-datasets](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets)
- Native Urdu human-verified records: **0**; review remains pending
- Counts are whitespace-delimited, not model-token counts

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

The published corpus also includes the earlier Dakshina, UCI Roman Urdu and Wikisource releases listed in the [processed-corpora registry](../catalog/processed-corpora.json). Source cards and manifests define each subset's provenance and transformations.

## Quality and limits

The Sangraha inputs use pinned upstream files. Their upstream dataset card declares CC BY 4.0. Automated Arabic-script and Urdu language-identification filters are routing checks, not native-speaker verification. Some upstream rows do not expose original page URLs or creator names.

Exact duplicate checks use SHA-256 over NFC-normalized text after whitespace collapse. Near-duplicate, quoted and semantically overlapping text may remain. Contact-pattern filters are triage, not a privacy guarantee. Review the license, attribution fields, card and manifest before reuse.

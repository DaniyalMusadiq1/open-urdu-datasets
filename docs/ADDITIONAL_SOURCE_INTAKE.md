# Phase 2 additional distinct source intake (2026-11-18)

These are **candidate sources, not published corpus records**. Their listed row counts
are publisher-reported, not local validation or unique counts. No data from this
list is included in the published token total until separately downloaded,
rights-audited, filtered, deduplicated against the existing corpus, and uploaded.

| Source | Domain | Declared license | Source | Intake status |
|---|---|---|---|---|
| UCI Roman Urdu Data Set (Zareen Sharf) | Roman Urdu sentiment | CC BY 4.0 | https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set | Pending download, provenance/PII and duplicate review |
| RUEmoCorp (Khubaib01) | Roman Urdu emotion | CC BY 4.0 (dataset card) | https://huggingface.co/datasets/Khubaib01/RUEmoCorp | Pending original-data rights and record-level provenance review |
| ALIF Urdu Corpus preview (Orature AI) | Urdu general text | CC BY-SA 4.0 (dataset card) | https://huggingface.co/datasets/orature/ALIF_Urdu_Corpus_AUC | Pending upstream underlying-text rights audit |
| FLORES-200 Urdu | Translation evaluation | CC BY-SA 4.0 (catalog) | https://huggingface.co/datasets/facebook/flores | Pending upstream source and benchmark-leakage assessment |
| Belebele Urdu | Reading comprehension | CC BY-SA 4.0 (catalog) | https://huggingface.co/datasets/facebook/belebele | Pending benchmark-leakage and derivative rights review |

Do not treat similarly licensed aggregations as cleared unless **each underlying
source** allows redistribution. Do not republish Makhzan restricted raw text,
noncommercial datasets, private chat messages, or unclear-license web scrapes.
Roman Urdu is a separate script/category; do not use an Arabic-script heuristic
to label Latin-script records as non-Urdu. Preserve the original labels and
source revisions; never label machine-generated text as native verified.

Priority: UCI Roman Urdu sentiment and RUEmoCorp for new *task types*, then
ALIF for a different *domain*. Task/domain diversity does not imply unique text.
Exact cross-source deduplication and independent audit are required before
publication. All new records begin with `review_status: unreviewed`.

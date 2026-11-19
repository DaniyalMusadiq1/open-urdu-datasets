# Klam-Urdu-Roman initial audit

Audit date: 2026-11-19. This audit uses the repository catalog and release workflow at commit 86242bdb90b4230d2d46b949f209c65e1dbf4b11.

## Current state

The repository currently has a 307-record Klam Ghalib starter release. The checked-in, previously processed input catalogs list 2,217,970 records across Dakshina, Urdu Wikisource, UCI Roman Urdu sentiment, Urdu Wikipedia, and Sangraha shards 0-7. Those counts are input-corpus counts, not a deduplicated Klam release count. The expanded build for Sangraha shards 0-26 is running; its final Klam manifest and record count are not available yet.

The current catalogs report zero human-reviewed records. The default Klam format already carries source, version, license, attribution, and review status per record. It deduplicates exact matching normalized text, task, and label; it does not claim near-duplicate removal.

## Gap against the uploaded brief

| Brief target | Evidence in repository now | Gap / status |
|---|---|---|
| 5M Nastaliq pretraining records | Existing inputs total 2,217,970 records across scripts/tasks; expanded Sangraha build pending | Not yet measured as a Klam split; 5M target unproven |
| 2M Roman Urdu pretraining records | UCI Roman Urdu sentiment contributes 27,106 Roman-script rows; Dakshina contains Romanization data but its script/task split needs a Klam manifest | Large shortfall; exact Roman count pending |
| 200k Nastaliq SFT pairs | No published Klam SFT split identified | Not met; open, rights-cleared pair count not established |
| 100k Roman Urdu SFT pairs | No published Klam Roman SFT split identified | Not met; do not manufacture rows to meet the number |
| 500k aligned Nastaliq/Roman or Urdu/English pairs | No Klam parallel split identified | Not met; source and alignment audit required |
| 5,000 held-out evaluation rows | No Klam evaluation split identified | Not met; source licensing and train/eval isolation required |
| Record-level source and license provenance | Present in the current Klam schema and source registry | Keep each source’s terms; there is no single data license for all Klam text |
| MinHash near-deduplication at Jaccard 0.8 | Current Klam builder does exact deduplication | Not implemented or measured |
| 10,000 native-speaker verified records | Current catalogs report 0 human-reviewed records | Not met; recruit reviewers and keep all other rows unreviewed |
| Gopher-style filters and discard-rate report | Current source importers have source-specific filters, not the complete brief checklist | Not met; add measured, reproducible checks before claiming them |
| Rebuild from scripts/run_all.sh | Existing pinned-source build workflow exists; the requested complete Roman/SFT/eval pipeline does not | Partial; this file set adds a Stage A fetcher and a deliberately gated orchestrator |

## Source and rights decisions

- Sangraha verified Urdu is declared CC BY 4.0 by its publisher. The source card reports 3.6581 billion verified Urdu tokens; this is an upstream token statistic, not Klam’s record or token count.
- Dakshina declares CC BY-SA 4.0. Keep attribution and share-alike obligations with the applicable records.
- Wikimedia text is subject to CC BY-SA terms; preserve revision links and attribution.
- Makhzan raw text is excluded. Its repository says the text files are copyrighted and may not be republished without the relevant rights holder’s permission.
- Aya is listed as a candidate source only. Its collection card declares Apache 2.0, but the exact Urdu subset, underlying dataset licenses, and row-level provenance still need an audit before ingestion.
- Social-platform and news scraping, unlicensed OCR, GPL-only corpora, synthetic instructions, and AI-generated evaluation rows are not included in Stage A.

## Release status

Klam-Urdu-Roman is not ready as a v1.0 dataset under the uploaded release gates. Do not claim the size, SFT share, parallel count, near-dedup rate, or native-speaker verification until a generated release manifest and reviewer log support those figures.
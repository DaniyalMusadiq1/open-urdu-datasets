# Klam build plan

Klam is one user-facing dataset. The build keeps source IDs, versions, licenses, attribution, and review status on each record. The targets in the uploaded brief are goals, not achieved counts.

## Stages

| Stage | Existing / updated files | Expected output and count basis | External need | Status |
|---|---|---|---|---|
| A. Pin and fetch inputs | configs/sources.yaml; scripts/build_phase2_release.py; scripts/import_dakshina_bulk.py; scripts/import_sangraha_urdu.py; scripts/import_urwiki_articles.py | Counts come from importer manifests. Dakshina's historical full-build manifest reports 622,805 rows; the current published copy is only 150,000. Sangraha source record counts are measured per shard; no upstream token total is substituted for Klam totals. | Network access to official source archives and Hugging Face | Rebuild wired; result pending |
| B. Extract and normalize | Source-specific importers; scripts/build_klam_release.py | Unicode NFC/whitespace normalization is used for identities. Original text is preserved in each record. | None beyond build dependencies | Implemented |
| C. Quality checks | Source-specific validation scripts and import filters | Each importer records its own accepted/rejected rows; the complete brief's Gopher rule set is not implemented | FastText model is pinned for Urdu language routing | Partial |
| D. Deduplicate | scripts/build_klam_release.py; scripts/validate_klam_release.py | Exact dedup uses normalized primary text plus paired text, task, and label. Similar records may remain. | Disk space for SQLite dedup index | Exact dedup implemented; MinHash pending |
| E. SFT | No SFT synthesis step | No target count is claimed. Translation/self-instruct generation is not part of this build. | Native contributors needed for authentic authored SFT; any synthetic-text plan requires separate review | Not implemented |
| F. Parallel records | scripts/import_dakshina_bulk.py; scripts/build_klam_release.py | Keep source Urdu/Roman pairs linked in paired_text; historical Dakshina full-build manifest reports 127,201 pairs before cross-source dedup. | None | Implemented for Dakshina; 500k goal not met |
| G. Rights and provenance | datasets/klam/sources.json; schemas/klam-record.schema.json; scripts/validate_klam_release.py | Validate each row against its approved source version, license, evidence URL, and attribution | Rights review for any new source | Implemented |
| H. Package and publish | scripts/run_all.sh; scripts/build_klam_release.py; scripts/validate_klam_release.py; datasets/HUGGINGFACE_README.md; .github/workflows/huggingface-sync.yml | Deterministic JSONL.GZ shards and separate train/validation/test splits; final counts from manifest only | GitHub Actions HF_TOKEN for automatic hosted sync | Implemented; new full build pending |

## What the next rebuild will do

1. Download the checksummed Dakshina v1.0 archive and import its full native and transliteration records.
2. Build Urdu Wikipedia and Sangraha revisions 0–26 through their pinned source importers.
3. Preserve source validation/test data outside the Hugging Face train split.
4. Merge inputs into Klam, remove exact duplicates, generate a manifest and source/license documentation, then validate every row and shard.
5. Publish Klam through the existing Hugging Face workflow when the repository build succeeds.

## Counts and release gates

The last published corpus snapshot is 2,217,970 records / 1,006,902,795 whitespace-delimited tokens. It is not the next Klam count. The in-progress expanded build may change this total; Klam's final manifest is authoritative. Record counts from source cards, historical manifests, or upstream token estimates are not added to the published Klam count.

Still open: 2M Roman Urdu pretraining docs, 200k Nastaliq SFT pairs, 100k Roman Urdu SFT pairs, 500k parallel pairs, a 5k held-out eval suite, MinHash near-deduplication, all required quality filters, and 10k native-speaker-verified rows. No record becomes human-verified without reviewer evidence.

## Needs people or credentials

- GitHub Actions needs the repository's existing HF_TOKEN secret to publish automatically.
- Native Urdu and Roman Urdu reviewers must be recruited for human quality checks.
- Rights holders or stronger provenance evidence are required before adding restricted or unclear-license sources.
- GPT/API keys are not needed; this plan does not generate synthetic or translated text.


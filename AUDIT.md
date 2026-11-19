# Klam-Urdu-Roman audit

Audit date: 2026-11-19

This audit separates the last published counts from the next full pinned rebuild. Counts from source cards or historical manifests are not Klam release counts.

## Published snapshot before the current rebuild

The repository reports **2,217,970 records and 1,006,902,795 whitespace-delimited tokens** across its hosted corpus releases. These are whitespace counts, not model-token estimates. The expanded build for Sangraha shards 0–26 and a complete Dakshina import must finish before a new Klam total is available.

A historical full Dakshina import manifest reports 622,805 retained rows, including 127,201 Urdu–Roman transliteration pairs. The currently hosted Dakshina copy contains only 150,000 native training sentences; it does not include the full import or those pairs. The updated build now fetches the pinned official archive, keeps both sides of pair records, and separates train, validation, and test.

## Gap against the brief

| Brief target | Current evidence | Status |
|---|---|---|
| 5M Nastaliq pretraining records | Published sources total 2.22M records across scripts and tasks; expanded 27-shard build is pending | Not yet established as 5M Klam pretraining records |
| 2M Roman Urdu pretraining documents | 27,106 hosted UCI Roman Urdu records are sentiment data, not pretraining text; Dakshina adds linked transliteration pairs, not standalone Roman documents | Not met |
| 200k Nastaliq SFT pairs | No cleared Klam SFT split | Not met; no synthetic rows are being generated |
| 100k Roman Urdu SFT pairs | No cleared Klam Roman SFT split | Not met; no synthetic rows are being generated |
| 500k parallel pairs | Historical full Dakshina import reports 127,201 pairs before Klam cross-source deduplication | Below target; exact rebuilt count pending |
| 5,000 held-out evaluation rows | Dakshina source validation/test rows are retained in separate Klam splits; no Klam eval suite exists | Not met |
| Per-record source and license | Klam rows carry source ID/version, locator, license, evidence, attribution, and review status | Implemented; new validator checks these fields |
| Exact duplicate removal | NFC and whitespace-collapsed exact dedup includes task, label, and both pair sides | Implemented |
| MinHash near-deduplication | No MinHash index or measured near-duplicate rate | Not implemented |
| Native-speaker verification | Current reported count is 0 | Not met; rows remain unreviewed |
| Full Gopher-style filter and discard report | Source-specific filters and language routing exist; the whole brief's filter set is not implemented | Partial |
| One-command reproducible build | Pinned importers, normalized Klam packager, validator, and HF workflow are wired through the build runner | Implemented; full build is long and requires network access |

## Rights and source decisions

- Include only sources with explicit redistribution rights and pinned source evidence. Keep the source license on every record; Klam does not apply one license to all text.
- Makhzan raw text stays excluded because its repository does not grant permission to republish those files.
- Aya remains a candidate until the exact Urdu subset and its component provenance are audited.
- News/social scraping and private messages are excluded. Public availability is not a license.
- GPT-generated instructions, translations, and evaluation records are not being added. No AI-written text is represented as human-authored or human-verified.
- Roman-Urdu-Parl-split is a promising large parallel source, but its third-party card's Apache declaration and underlying source-rights chain need review before intake. It is not counted in Klam.

Klam is not ready for v1.0 under the brief's release gates. Do not claim the targets, near-dedup coverage, SFT coverage, or native verification until the generated release manifest and reviewer evidence support them.


# Klam-Urdu-Roman staged plan

Goal: grow Klam to cover both Urdu Arabic-script text and Roman Urdu while preserving one easy-to-load dataset and record-level source rights. The target counts in the brief are goals, not estimates or release claims.

| Stage | Work | Output | Count estimate / dependency |
|---|---|---|---|
| A. Fetch | Download only approved, pinned, open sources; record URL, revision, license, SHA-256, and fetch date | data/raw plus manifest.json | Three sources can be staged now: Sangraha, Dakshina, Urdu Wikipedia. Full source bytes are large; Sangraha’s upstream verified Urdu statistic is 3.6581B tokens, not a Klam record count. |
| B. Extract and normalize | Preserve source text; add script-aware fields and separate raw/normalized Roman forms; document every transformation | normalized JSONL shards | Record totals after extraction and filters; do not infer them from archive size |
| C. Quality | Run schema, script, language-ID, length, repeated n-gram, and PII triage; report each discard reason | quality report and flags | No current all-source discard-rate estimate |
| D. Deduplicate | Keep exact deduplication; add a disk-backed near-duplicate pass only after threshold, memory use, and false-positive behavior are documented | duplicate audit and retained rows | Current Klam handles exact duplicates only; no MinHash count yet |
| E. Instruction data | Add only openly licensed, traceable human or publisher-authored prompt/response data after component-level rights review | klam-sft split | No verified count established. AI-generated or machine-translated text is excluded unless separately authorized, licensed, labeled, and reviewed |
| F. Parallel data | Use source-provided parallel rows or explicitly labeled transliteration outputs; never present derived transliteration as human-authored | klam-parallel split | Count unknown until sources are licensed and alignment checks run |
| G. Rights and review | Require source, version, license, attribution, and evidence for every row; keep review status unreviewed unless reviewer evidence exists | manifest and reviewer log | Current repository catalogs report 0 human-reviewed records |
| H. Package and release | Generate one JSONL.GZ dataset with task/script subsets, counts, licenses, checksums, card, and loading examples | GitHub metadata and Hugging Face release | Full release must pass schema, license, leakage, dedup, and split-isolation checks |

## First implementation

- AUDIT.md records current counts and release-gate gaps.
- configs/sources.yaml is a JSON-compatible YAML registry; the fetcher uses only the Python standard library.
- scripts/01_fetch_sources.py downloads three approved pinned source families and writes a checksum manifest under data/raw/.
- docs/VERIFICATION.md defines review labels and a blank reviewer log.
- scripts/run_all.sh runs Stage A and stops at the first not-yet-implemented stage. It does not pretend the full pipeline exists.

## Scope limits

Makhzan’s raw text is not copied: its publisher prohibits republishing that text absent specific rights-holder permission. No scraping of news, Reddit, YouTube, or X is part of this plan. The project’s earlier rule against fabricated and AI-generated dataset records remains in force. Aya remains a candidate until the exact Urdu subset and its source-level licensing are checked.

## Human and service dependencies

- Human reviewers: required before any native-speaker verification claim; none is presumed available.
- Hugging Face: the existing repository workflow uses the configured HF_TOKEN secret for publication. A full rebuild is large and must finish before a final count can be reported.
- GPT API: not required for the approved ingestion path. No synthetic instruction/evaluation records are generated.
- Additional licenses or rights-holder permissions: required before adding sources whose public pages do not grant redistribution rights.
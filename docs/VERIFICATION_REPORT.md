# Verification report — unreleased draft, 2026-11-17

## Outcome

28 upstream resources: 1 technically verified scoped dataset, 2 pending review, 25 unverified (includes one catalog-only embeddings resource). The target of 25 verified datasets is unmet. Two separately scoped CC-BY-SA-4.0 samples are hosted: 25 vocabulary records and 5 Urdu–English evaluation passage pairs. They are not independent additions to the discovery count. All 30 hosted records are locally unreviewed. Human-verified record count: 0. No v0.1.0 tag or release.

## Data verification actually performed

- Belebele: all 900 English, 900 Urdu Arabic-script and 900 Romanized Urdu JSONL rows downloaded at pinned publisher revision `7899cdfa4e1e0d733fd77c848e2c273cb1d32be2`. All rows passed UTF-8, field/type, dialect, answer-ID and identifier checks. All 900 question IDs and correct-answer IDs align across the three files. `ds` dates differ by language; alignment uses source-page link + question number. Source license explicitly covers the evaluation data and its full license was retrieved. The training mixture is excluded. Scope is those complete publisher files, not every language in Belebele and not a native accuracy audit.
- The 1,800 Urdu variant rows cover the same 900 underlying questions; they must not be counted as 1,800 independent evaluation examples. English rows are not counted as Urdu records.
- Five unique English passages aligned to Urdu were copied exactly into the derived evaluation-only sample. Source URLs, SHA-256, lines and original-page links are retained per record. No translations or Urdu examples were generated. Historical-conflict content warning included; no training or model-selection validation use.
- Dakshina: complete Urdu training member retrieved from official archive, 2,185,405 bytes, 106,260 romanization rows and 25,000 native word types. Locally computed SHA-256 and byte-range evidence recorded. The complete 2 GB archive was not downloaded/hashed. The 25-record sample reproduced byte-for-byte from the member, retaining upstream lines/attestations. Glosses, POS and example fields are null rather than guessed. The broader Dakshina entry remains unverified because other components were not checked.
- UCI Roman Urdu: complete ZIP retrieved; UTF-8 CSV parsed as 20,229 rows with three columns, versus the rounded source description of 20,000. One `Neative` label and seven nonempty third-column values require review. Source values were not corrected or republished.
- UCI RUSAD: complete ZIP retrieved; UTF-8 TSV parsed as 11,000 rows/two columns, with one blank label. Pending review; source values were not corrected or republished.
- Full file hashes, counts, checks and label counts are in `catalog/data-verification.json`; no UCI raw reviews are included in this repository.

## Tooling checks

- Pytest: 13 passed; one environment plugin deprecation warning unrelated to project behavior.
- Ruff: passed.
- Catalog JSON schema, UTF-8, required fields, unique IDs and typed CSV parity: passed (28 entries).
- Both hosted sample schemas, SHA-256 manifests and counts: passed (30 locally unreviewed records).
- Plain Python, pandas and Hugging Face catalog examples executed successfully after approved dependency fixes. JSON/YAML parse, file-size and Git whitespace checks passed. All files remain below 100 MB; no LFS used.
- GitHub Actions on prior tooling-only commit d76a20e2fff449fc482b9b8676591b4ab4e55a78: Quality success, Hosted samples success, Link checks failure. These are historical results, not claims about a subsequent data-update commit. Check the current PR head for current CI.

## Links and source rights

The initial metadata HEAD batch had 63 OK and one unresolved Tatoeba documentation URL (503), which also returned 503 on a focused recheck. `catalog/current-link-check-results.json` reconciles that snapshot with HEAD checks of new catalog URLs; results are dated and identify reused versus new checks. GET results, source metadata and independent data verification are separate evidence. HTTP accessibility is not a license clearance or human language check.

No Makhzan raw content, NC/research-only corpus files, private records or secrets are intentionally included. Makhzan forbids raw republication; XNLI is NC, UD Urdu UDTB and XL-Sum are NC, LDC requires an agreement. All remain link-only. OSCAR's packaging CC0 does not clear underlying web text. Mixed/unspecified rights and copyright-sensitive sources remain link-only unless explicit permissions cover the exact files. Both hosted samples have explicit publisher CC-BY-SA evaluation/lexicon licensing and retained attribution; the project MIT license does not relicense them.

## Remaining limitations and next contributions

Not release-ready. Need 24 more verified independent datasets, broader coverage in docs/COVERAGE.md, native Urdu review of README.ur.md and all sample records, source-specific rights and PII/toxicity review, and resolution of link-check failures. No human correctness or PII-free claim is made. Review the source label anomalies rather than silently repairing them. Do not treat the evaluation pair sample as training data or a representative translation corpus.

The maintainer-approved README/dependency/tooling patch has been applied. The retained proposed patch/README preview are historical review artifacts, not pending permissions. No main merge or release is claimed. Approvals do not substitute for successful checks or native review.

## Source catalog license labels

Labels describe publisher claims and do not clear every underlying document. The two derived samples each retain CC-BY-SA-4.0 and are excluded from upstream counts.

| License | Upstream entries |
|---|---:|
| Apache-2.0 | 2 |
| CC-BY-2.0-FR | 1 |
| CC-BY-4.0 | 3 |
| CC-BY-NC-4.0 | 1 |
| CC-BY-NC-SA-4.0 | 2 |
| CC-BY-SA-3.0 | 1 |
| CC-BY-SA-4.0 | 4 |
| CC0-1.0 | 2 |
| ODC-By-1.0 | 2 |
| unspecified | 10 |

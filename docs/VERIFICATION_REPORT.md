# Verification report — unreleased draft, 2026-11-17

## Outcome

28 upstream resources: 2 technically verified scoped datasets, 2 pending review, 24 unverified (includes one catalog-only embeddings resource). The target of 25 verified datasets is unmet. PR #1 was merged into main at 527f9bf251e1eea529c8f1cb949906ade6ce5be6 under the maintainer’s explicit merge request. Two separately scoped CC-BY-SA-4.0 samples are hosted: 25 vocabulary records and 5 Urdu–English evaluation passage pairs. They are not independent additions to the discovery count. All 30 hosted sample records and all 622,805 bulk records are locally unreviewed. The 25-word sample overlaps the bulk lexicon, so these counts must not be summed as unique data. Human-verified record count: 0. No v0.1.0 tag or release.

## Data verification actually performed

- Belebele: all 900 English, 900 Urdu Arabic-script and 900 Romanized Urdu JSONL rows downloaded at pinned publisher revision `7899cdfa4e1e0d733fd77c848e2c273cb1d32be2`. All rows passed UTF-8, field/type, dialect, answer-ID and identifier checks. All 900 question IDs and correct-answer IDs align across the three files. `ds` dates differ by language; alignment uses source-page link + question number. Source license explicitly covers the evaluation data and its full license was retrieved. The training mixture is excluded. Scope is those complete publisher files, not every language in Belebele and not a native accuracy audit.
- The 1,800 Urdu variant rows cover the same 900 underlying questions; they must not be counted as 1,800 independent evaluation examples. English rows are not counted as Urdu records.
- Five unique English passages aligned to Urdu were copied exactly into the derived evaluation-only sample. Source URLs, SHA-256, lines and original-page links are retained per record. No translations or Urdu examples were generated. Historical-conflict content warning included; no training or model-selection validation use.
- Dakshina: complete Urdu training member retrieved from official archive, 2,185,405 bytes, 106,260 romanization rows and 25,000 native word types. Locally computed SHA-256 and byte-range evidence recorded. At the initial sample-creation stage the complete archive was not downloaded; it has now been downloaded and hashed for the bulk addition below. The 25-record sample reproduced byte-for-byte from the member, retaining upstream lines/attestations. Glosses, POS and example fields are null rather than guessed. The current Dakshina entry is technically verified only for its named Urdu native-text and word-lexicon scope; no claim covers other languages/components.
- UCI Roman Urdu: complete ZIP retrieved; UTF-8 CSV parsed as 20,229 rows with three columns, versus the rounded source description of 20,000. One `Neative` label and seven nonempty third-column values require review. Source values were not corrected or republished.
- UCI RUSAD: complete ZIP retrieved; UTF-8 TSV parsed as 11,000 rows/two columns, with one blank label. Pending review; source values were not corrected or republished.
- Full file hashes, counts, checks and label counts are in `catalog/data-verification.json`; no UCI raw reviews are included in this repository.

## Tooling checks

- Pytest: 15 passed; one environment plugin deprecation warning unrelated to project behavior.
- Ruff: passed.
- Catalog JSON schema, UTF-8, required fields, unique IDs and typed CSV parity: passed (28 entries).
- Both hosted sample schemas, SHA-256 manifests and counts: passed (30 locally unreviewed records).
- Plain Python, pandas and Hugging Face catalog examples executed successfully after approved dependency fixes. JSON/YAML parse, file-size and Git whitespace checks passed. All files remain below 100 MB; no LFS used.
- GitHub Actions on prior tooling-only commit d76a20e2fff449fc482b9b8676591b4ab4e55a78: Quality success, Hosted samples success, Link checks failure. These are historical results, not claims about a subsequent data-update commit. Check the current PR head for current CI.

## Links and source rights

The initial metadata HEAD batch had 63 OK and one unresolved Tatoeba documentation URL (503), which also returned 503 on a focused recheck. `catalog/current-link-check-results.json` reconciles that snapshot with HEAD checks of new catalog URLs; results are dated and identify reused versus new checks. GET results, source metadata and independent data verification are separate evidence. HTTP accessibility is not a license clearance or human language check.

No Makhzan raw content, NC/research-only corpus files, private records or secrets are intentionally included. Makhzan forbids raw republication; XNLI is NC, UD Urdu UDTB and XL-Sum are NC, LDC requires an agreement. All remain link-only. OSCAR's packaging CC0 does not clear underlying web text. Mixed/unspecified rights and copyright-sensitive sources remain link-only unless explicit permissions cover the exact files. Both hosted samples have explicit publisher CC-BY-SA evaluation/lexicon licensing and retained attribution; the project MIT license does not relicense them.

## Remaining limitations and next contributions

Not release-ready. Need 23 more verified independent datasets, broader coverage in docs/COVERAGE.md, native Urdu review of README.ur.md and all sample records, source-specific rights and PII/toxicity review, and resolution of link-check failures. No human correctness or PII-free claim is made. Review the source label anomalies rather than silently repairing them. Do not treat the evaluation pair sample as training data or a representative translation corpus.

The maintainer-approved README/dependency/tooling patch has been applied. The retained proposed patch/README preview are historical review artifacts, not pending permissions. The first PR is merged; the bulk addition is handled through a second branch and PR. No release is claimed. Approvals do not substitute for successful checks or native review.

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

## Large-corpus verification update

Complete official Dakshina archive: 2,008,340,480 bytes, SHA-256 `83530bec211893d9df429298f42e63c350c25ad56f9f5172f85edb0575ee5b03`. This supersedes the initial range-only archive scope for the new bulk addition, not the historical sample retrieval method. Only named Urdu native-text and lexicon components are audited; other languages/components are not promoted as verified.

Retained 622,805 records: 495,604 native text units and 127,201 romanization word pairs. Native whitespace-delimited tokens: 8,948,752. Exact native duplicate rows removed: 37,422, including 10,975 cross-split occurrences; validation was processed first to retain shared strings there. One email-like row was excluded; only a source coordinate, hash and reason are retained in the exclusion audit. Filtering is limited triage, not proof of PII absence.

The 16 compressed shards total 63,998,560 bytes; largest 6,037,940 bytes, below both browser upload and GitHub file limits. They retain exact publisher text, original article/revision URLs for native units, source member/line, archive/member hashes, license and unreviewed status. The 25-record vocabulary sample overlaps the full lexicon; no unique-total claim is made by summing samples and corpus. Human-reviewed records remain zero. Dataset license is CC-BY-SA-4.0; original authors/contributors and changes are documented per dataset.

Validation streams every record through its schema, content identity, duplicate rules, retained filter checks, and independently recounts words and rows. The bulk manifest records input flags, source counts, named members and every shard digest. All 622,805 local records passed the full streaming schema/identity/filter/count validation. Remote bytes are checked separately after upload before merging the bulk PR. No v0.1.0 release is made while verification and native-review gaps persist.

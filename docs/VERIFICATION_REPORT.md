# Verification report — draft, 2026-11-17

## Outcome

Not release-ready. 28 upstream discovery entries (27 dataset/corpus resources and 1 pretrained-vector resource), all `unverified`; target of 25 verified datasets not met. A separate derived Dakshina sample has 25 technically validated records, all `review_status: unreviewed`. Human-verified record count: 0. No v0.1.0 tag or release.

## Checks actually run

- Catalog JSON schema, UTF-8, required fields, unique IDs and typed CSV parity: pass (28 entries).
- Derived sample schema, manifest SHA-256 and record count: pass (25 records).
- Sample reproduction from the complete upstream member: byte-for-byte match.
- Complete upstream Urdu training member: 2,185,405 bytes; 106,260 rows; 25,000 native word types; locally computed SHA-256 recorded. Whole 2 GB archive not downloaded/hashed.
- Approved README replacement applied on the feature branch; the project LICENSE is unchanged.
- Plain Python, pandas and Hugging Face catalog examples: all executed successfully (28 entries).
- Pytest after the approved dependency fix: 10 passed. `jsonschema[format-nongpl]` now declares the URI-format checker dependency. One environment plugin deprecation warning is unrelated to this project.
- Ruff: all checks passed after applying the approved import/style/exception fixes.
- Every pending added file was below 100 MB; no LFS or large binary artifact used.
- No Makhzan raw files or NC corpus files were downloaded into the repository. The only included language data is the attributed CC-BY-SA Dakshina sample. AI-drafted Urdu documentation and Unicode software fixtures are marked; no synthetic data is represented as human-reviewed.
- Automated sample email/URL-pattern triage: 0 matches. This is not a PII/toxicity audit or a language-quality guarantee.

## Link evidence

Source metadata GET outcomes are in `catalog/source-checks.json`. The separate HEAD batch is recorded in `catalog/link-check-results.json` (63 OK, 1 unresolved Tatoeba documentation URL returning 503 in the initial batch). Source metadata accessibility never promotes data verification. Shell GET 403 responses affected Wikimedia, current Common Voice, fastText and the CC legalcode endpoint; alternate official web evidence is identified separately. Gated sources were not accessed or new permissions requested.

## Rights and exclusions

Makhzan raw republication is forbidden. XNLI is CC-BY-NC-4.0; UD Urdu UDTB and XL-Sum are CC-BY-NC-SA-4.0 (XL-Sum also research-only). LDC requires its agreement. OSCAR's packaging CC0 does not clear underlying documents. Web corpora, unknown licenses, copyright-sensitive content and mixed-license instruction compilations remain link-only. Original source licenses are retained; no dataset is relicensed MIT.

## Approval and remaining work

The maintainer approved the proposed README/dependency/tooling patch. It has been applied and locally validated. `docs/proposed-updates.diff` and `README.proposed.md` are historical review artifacts; they do not indicate pending approval. No main merge or release is claimed.

The catalog and sample have separate manifests. `scripts/validate_repo.py` covers upstream entries; `scripts/validate_hosted.py` covers the sample. All three catalog loading examples passed after the dependency update.

Remaining release blockers: fewer than 25 verified datasets; incomplete task coverage and Urdu-English pair hosting; source-level rights/distribution checks and native Urdu review are incomplete; GitHub Actions results must be checked on the updated commit. The earlier commit had Quality failure, Link checks failure, and Hosted samples success; these results do not describe the updated code.

Next: resolve any link-check failures, independently verify scoped distributions and rights, obtain native Urdu review of spellings/romanizations and README.ur.md, and source permitted Urdu-English pairs and reviewed glosses/POS/examples. See docs/COVERAGE.md. Keep v0.1.0 unpublished while release blockers remain.

## Upstream catalog license labels (source claims, not cleared underlying rights)

| License | Entries |
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

The derived sample is separately CC-BY-SA-4.0 and is not added to upstream dataset counts.

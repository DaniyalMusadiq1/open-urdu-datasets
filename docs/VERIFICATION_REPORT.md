# Verification report — draft, 2026-11-17

## Outcome

Not release-ready. 28 upstream discovery entries (27 dataset/corpus resources and 1 pretrained-vector resource), all `unverified`; target of 25 verified datasets not met. A separate derived Dakshina sample has 25 technically validated records, all `review_status: unreviewed`. Human-verified record count: 0. No v0.1.0 tag or release.

## Checks actually run

- Catalog JSON schema, UTF-8, required fields, unique IDs and typed CSV parity: pass (28 entries).
- Derived sample schema, manifest SHA-256 and record count: pass (25 records).
- Sample reproduction from the complete upstream member: byte-for-byte match.
- Complete upstream Urdu training member: 2,185,405 bytes; 106,260 rows; 25,000 native word types; locally computed SHA-256 recorded. Whole 2 GB archive not downloaded/hashed.
- Existing README and LICENSE exactly match the approved main branch.
- Plain Python, pandas and Hugging Face catalog examples: all executed successfully (28 entries).
- Pytest: 9 passed, 1 failed. The URI-format rejection test fails because `jsonschema` alone does not install its optional URI checker. Proposed dependency is `jsonschema[format-nongpl]`.
- Ruff: failed, 5 findings across import ordering, nested conditional style, exception type and one unused import. Proposed patch addresses these; it has not been applied or retested.
- Every pending added file was below 100 MB; no LFS or large binary artifact used.
- No Makhzan raw files or NC corpus files were downloaded into the repository. The only included language data is the attributed CC-BY-SA Dakshina sample. AI-drafted Urdu documentation and Unicode software fixtures are marked; no synthetic data is represented as human-reviewed.
- Automated sample email/URL-pattern triage: 0 matches. This is not a PII/toxicity audit or a language-quality guarantee.

## Link evidence

Source metadata GET outcomes are in `catalog/source-checks.json`. The separate HEAD batch is recorded in `catalog/link-check-results.json` when complete. Source metadata accessibility never promotes data verification. Shell GET 403 responses affected Wikimedia, current Common Voice, fastText and the CC legalcode endpoint; alternate official web evidence is identified separately. Gated sources were not accessed or new permissions requested.

## Rights and exclusions

Makhzan raw republication is forbidden. XNLI is CC-BY-NC-4.0; UD Urdu UDTB and XL-Sum are CC-BY-NC-SA-4.0 (XL-Sum also research-only). LDC requires its agreement. OSCAR's packaging CC0 does not clear underlying documents. Web corpora, unknown licenses, copyright-sensitive content and mixed-license instruction compilations remain link-only. Original source licenses are retained; no dataset is relicensed MIT.

## Approval and remaining work

`docs/proposed-updates.diff` is a concrete proposal to update README.md, pyproject.toml, core/CLI, one test and two scripts. It declares URI format dependencies, fixes lint and updates the README with actual draft counts and the catalog table. It has not overwritten the source files. `README.proposed.md` previews the replacement README. Applying these changes requires maintainer approval under the no-overwrite rule. CI success is not claimed.

The catalog and sample deliberately have separate manifests; the existing generic validator covers upstream entries and `scripts/validate_hosted.py` covers the sample. The original README still describes initialization; consult CATALOG.md and this report until its proposed replacement is approved.

Next: approve and apply the proposed updates; rerun checks; reconcile unresolved URLs; review dataset licenses and full distributions individually; obtain native Urdu review of spellings, romanizations and README.ur.md; source permitted Urdu–English pairs and reviewed glosses/POS/examples; fill task gaps in docs/COVERAGE.md. Do not merge to main or tag until separate approval and passing checks.

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

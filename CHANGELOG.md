# Changelog

## Unreleased

- Approved repository initialization with README and MIT project license.
- Draft catalog, licensing policy, schema validation and conservative Unicode tools.
- Catalog/source inspection does not imply data or native-speaker verification.
- v0.1.0 has not been tagged or released.

- Applied approved README and tooling updates; 10 local tests, lint, schema/checksum validation and catalog examples passed. Dataset verification and native-review gaps remain.

- Verified scoped Belebele publisher evaluation files, added five attributed Urdu–English evaluation passage pairs, and recorded UCI label/column anomalies without changing source data. Local suite now has 13 passing tests; no human language review is claimed.

- Merged PR #1 as requested; prepared a full Dakshina build, of which only three shards were uploaded, preserving source provenance and unreviewed status. Added stream validation, pattern triage, exact content identity and bulk-loading tools.

- Audited the partial upload: corrected all published counts to 150,000 native training records and 2,935,498 whitespace tokens; preserved full-build metadata separately. Renamed the human-review status to `verified` without promoting unreviewed records.

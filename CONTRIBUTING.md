# Contributing

Use a branch and pull request. Keep one dataset or one tooling change per PR. Never push directly to main without maintainer approval. Open an issue before large downloads or Git LFS; files must remain below 100 MB.

Submit original source and download URLs, a dated license statement and license URL, collection and annotation methods, language/script, version, count with its unit and source, citation, content risks, and limitations. Unknown values must be null or `unspecified`, never guesses. Do not substitute a mirror's license for upstream rights. A GitHub code license does not automatically license included data.

`unverified` means data was not fully downloaded and validated, or provenance/license evidence is incomplete. `pending_review` means technical checks exist but an identified review remains. `verified` requires complete checks of the explicitly scoped distribution, source/licensing/attribution evidence, checksum and count evidence. It never means every language annotation was checked by a human. Record that separately.

To host data, provide explicit redistribution permission under the documented allowlist, a dataset card, full applicable license, attribution, source version, reproduction steps and SHA-256 manifest. Retain source text and record-level provenance. Do not contribute NC, ND, research-only, unspecified or ToS-restricted raw data, Makhzan raw text, secrets, private data, or scraped material without permission. Copyright-sensitive news, poetry, books and religious translations are link-only unless explicitly cleared.

Human review must identify who reviewed which records and what was checked. AI drafts remain `review_status: unreviewed` until the maintainer confirms them. Never add invented translations, glosses, POS tags, examples or counts. Do not train models as part of this repository.

To contribute original Urdu text to the Klam core, follow [`docs/KLAM_CONTRIBUTION.md`](docs/KLAM_CONTRIBUTION.md). The Klam source registry is currently empty; do not add records until their source rights are approved.

Run the commands in `docs/DEVELOPMENT.md`. Include the exact results and any failures. Source-page accessibility and source-reported sizes are not local data validation. Gated downloads require a separate permission decision; do not request access automatically.

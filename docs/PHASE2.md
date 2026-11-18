# Phase 2 — rights-cleared Urdu bulk ingestion (preparation)

**Step 1 milestone: 200,000,000 published whitespace-delimited tokens.**
The published baseline across separately tracked corpora is 3,464,441 tokens;
the milestone gap is **196,535,559 tokens**. This includes 528,943 tokens from
the separately licensed and deduplicated UCI Roman Urdu sentiment release.
Do not report this milestone achieved until actual hosted shards and remote hashes
are verified. This is a milestone, not an assertion of data availability.


**Target:** 1,400,000,000 whitespace-delimited tokens (not records).
**Published baseline:** 150,000 Dakshina native-text records / 2,935,498 tokens,
plus 27,106 UCI Roman Urdu sentiment records / 528,943 tokens (3,464,441 total).
**Gap:** 1,396,535,559 tokens. No bulk Phase 2 shards are published as of this commit.
**Human-reviewed records:** 0. Native Urdu review remains pending.

## Source intake

Sources are not approved by category or website alone. Each input record must carry:
`text`, `category` (news/books/wikipedia/web/conversation/roman_urdu/speech_transcript),
`script` (urdu_arabic/roman_urdu), `license`, `source_url`, `source_version`,
`rights_evidence_url`, `document_id`, `revision`, and `redistribution_cleared: true`.
The rights clearance flag must be supplied only after an independent human source-specific
rights audit. The pipeline cannot verify legal rights from that flag.

Allowed SPDX IDs in this initial gate: CC0-1.0, CC-BY-3.0, CC-BY-4.0,
CC-BY-SA-3.0, CC-BY-SA-4.0, ODC-By-1.0. Other versions require explicit review
and code changes. ODC-By may not cover underlying source text; do not use it
without confirming rights for the actual records. Source URLs and rights evidence
must use HTTPS. Use actual revision/version identifiers; never invent them.

## Local commands

```sh
python -m pip install -e '.[dev]'
python scripts/phase2_ingest.py input.jsonl phase2-output
python scripts/phase2_validate.py phase2-output
python -m pytest tests/test_phase2.py
```

Output is a new directory with JSONL.GZ shards, SHA-256 checksums and
`manifest.json` with **local_unpublished** status. Existing output is never
overwritten. Deduplication uses NFC normalization and whitespace collapse for SHA-256 keys,
while preserving original source text. This removes identical and whitespace-equivalent
records within a run, not semantic paraphrases or near-duplicates. SQLite stores
dedup keys on disk for large runs; validator keys are also disk-backed.
Whitespace token counts are not model-token counts. Script-ratio heuristics are
not reliable Urdu language identification; Roman Urdu can include English.
The contact-pattern filter is limited triage, not a PII guarantee. Add language
classification, near-duplicate detection, safety sampling, corpus-specific
license review and independent quality audits before production-scale ingest.
Do not label heuristic-passing text linguistically verified.

## Hugging Face publication — separate explicit action

Install `huggingface_hub` in the publishing environment. The uploader
requires an existing HF dataset repository, `HF_TOKEN` and explicit
`--confirm-upload`:

```sh
python scripts/phase2_publish.py phase2-output --repo-id ORG/DATASET --confirm-upload
```

This command is **not** run by CI. Do not put tokens in Git or logs. It uploads
into the `phase2/` prefix, then reports the local validated count. Before
changing published totals, independently list remote files, compare each remote
SHA-256, record immutable repository revision and attribution/license notices,
and reconcile the publication manifest. Do not count an attempted upload.

## Known gaps

No new licensed source has been ingested or published. Existing Dakshina
historical build shards are not assumed present. No rights clearance for
news, books, speech or conversational sources is implied by this scaffolding.
This initial pipeline is preparation, not a billion-token crawler, verified
language classifier, comprehensive deduplicator, or a native review process.

# Corpus expansion status

## Target and current progress

**Phase milestone: 200,000,000 whitespace-delimited tokens. Overall target:
1,300,000,000 whitespace-delimited tokens.** The three
separately tracked, hosted corpora total **183,472 records / 4,765,116 tokens**:

- Dakshina Urdu native-text subset: 150,000 records / 2,935,498 tokens.
- UCI Roman Urdu sentiment task corpus: 27,106 records / 528,943 tokens.
- Urdu Wikisource `PD-old` pages: 6,366 records / 1,300,675 tokens.

That is **2.38% of this phase milestone**, with **195,234,884 tokens remaining
for the phase**. The overall target is **0.37% complete**, with **1,295,234,884
tokens remaining**. These are whitespace-delimited counts, not model-token counts.
The goal is not complete, and these sources do not represent all Urdu books or
publicly accessible data. Native-speaker review is pending; human-verified
records: **0**.

## Intake and deduplication

Public availability by itself does not grant redistribution rights. Each source
must have source-specific evidence that permits redistribution. The Wikisource
addition was limited to main-namespace pages carrying the explicit `{{PD-old}}`
tag in the pinned monthly export. Other public-domain tags and pages without an
explicit clear tag were excluded. Source page, revision, timestamp, export hash,
license and record-level review status are preserved.

Exact duplicate detection uses SHA-256 over NFC-normalized text after whitespace
collapse. This removes exact and whitespace-equivalent text; it does not detect
near duplicates, alternate editions, quotations, or paraphrases. The new batch
was scanned against text fields in current repository JSONL and JSONL.GZ files.
Automated script-ratio and contact-pattern filters are triage only and cannot
prove Urdu language identity or absence of personal data.

## Reproducing the Wikisource addition

```sh
python -m pip install -e '.[wikimedia]'
python scripts/import_urwikisource_pd_old.py DUMP.xml.bz2 OUTPUT_DIR
python scripts/validate_urwikisource_pd_old.py OUTPUT_DIR
```

The importer checks a pinned official dump SHA-256 and refuses to overwrite an
existing output directory. It extracts MediaWiki markup while preserving the
source text and makes no linguistic corrections. The release manifest lists
record rejects, shard counts and hashes.

## Publishing and future intake

For GitHub publication, add the rights-cleared files and metadata to `main`.
GitHub Actions validates the repo and mirrors the approved release to the
existing Hugging Face dataset; it verifies each remote file hash and reports the
immutable revision. Do not increase published counts unless that sync succeeds.
The sync uses the configured `HF_TOKEN` secret and must never expose it.

Future source batches need rights evidence, provenance, exact and near-duplicate
checks, source-specific quality review, privacy review, checksums and a clear
review status before inclusion. Human/native-speaker review must remain marked
pending until a reviewer completes it. No data should be fabricated or
misrepresented to reach a numeric target.

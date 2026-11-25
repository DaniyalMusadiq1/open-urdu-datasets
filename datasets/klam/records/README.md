# Klam record intake

Klam accepts material only after its source and redistribution rights are documented in [sources.json](../sources.json). Approved sources may be original or permissioned text, CC0, CC BY, CC BY-SA, or evidenced public-domain content.

Add one UTF-8 JSON object per line in a `.jsonl` or `.jsonl.gz` file. Each input row should contain:

```json
{"title":"<title or empty string>","text":"<source text>","source_id":"<approved source ID>","source_record_id":"<stable source record ID>","source_locator":"<page or source location>","script":"Arabic","task":"text","label":"","split":"","review_status":"unreviewed"}
```

Use only real source text. Do not add synthetic or AI-generated text, unclear-rights material, or silent spelling edits. Klam output fills in the pinned source version, rights, license, attribution, and stable ID.

Mark a record `human_reviewed` only when reviewer ID, date, and review scope are present. Automated filtering is not human review.

## Dakshina Urdu sentence pairs

Recreate the tracked shard from the official Dakshina v1.0 archive by running
the following command from the repository root. The importer checks the archive
SHA-256 before reading it.

```bash
python -m pip install -e .
python scripts/prepare_dakshina_sentence_pairs.py dakshina_dataset_v1.0.tar /tmp/dakshina-urdu-sentence-pairs.jsonl.gz
cmp /tmp/dakshina-urdu-sentence-pairs.jsonl.gz datasets/klam/records/dakshina-urdu-sentence-pairs.jsonl.gz
```

Both sides retain the upstream text. Klam maps `dev` to `validation` and keeps
`test` as `test`. It retains the first exact normalized pair, with test taking
precedence, and excludes blank sides, text matching the project's contact and
credential filters, and prompts without an unambiguous Wikipedia revision.

## Additional Urdu and Roman Urdu text

The Tatoeba Urdu detailed export and Wikivoyage Urdu phrasebook revision
`5320526` are pinned by SHA-256 in the source registry. To reproduce the inputs,
pass those exact snapshots to the importer from the repository root.

```bash
python scripts/prepare_klam_extra_text.py urd_sentences_detailed.tsv.bz2 phrasebook.wiki /tmp
```

Tatoeba sentences without an author are skipped. The author and sentence URL are
preserved. Wikivoyage rows retain only explicitly paired Urdu phrases and Latin
pronunciations. Pronunciation guides are informal and sometimes mark stress.
Both sources go into training with `unreviewed` status. The release keeps only
new exact normalized text or pair matches after processing the earlier sources,
regardless of task label.

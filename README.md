# open-urdu-datasets

A community Urdu and Roman Urdu dataset hub with provenance, license tracking and reproducible quality tools.

**Unreleased draft.** 150,000 published bulk records containing 2,935,498 native whitespace-delimited tokens, plus overlapping demonstration samples. 28 upstream discovery entries (including one embeddings resource), 2 technically verified scoped datasets, 2 pending-review datasets, 24 unverified resources, and two separately scoped hosted samples (25 vocabulary records + 5 evaluation passage pairs) awaiting local native-speaker review. The target of 25 verified datasets is not met. No v0.1.0 release has been published.

[اردو تعارف — unreviewed](README.ur.md) · [Contributing](CONTRIBUTING.md) · [Licensing and removal](docs/LICENSE_POLICY.md) · [Coverage gaps](docs/COVERAGE.md)

## Verification and counts

An accessible source page is not data verification. Dakshina’s named Urdu native-text/lexicon components and Belebele’s scoped Urdu Arabic/Latin evaluation files are technically verified against the publisher version and explicit dataset license; 2 UCI downloads remain `pending_review` due to label/column anomalies, and 24 resources remain `unverified`. “Verified” does not mean native annotation review. Counts below identify source-reported versus locally-counted values, may overlap and must not be summed as unique records. Both derived samples are excluded from independent-dataset counts.

The sample's complete upstream lexicon member was downloaded from the official archive: 106,260 romanization rows, 25,000 distinct native-script words. Its SHA-256 is recorded in SOURCES.md. The original small sample used a byte-range retrieval; the bulk addition now has the complete official archive downloaded and SHA-256 checked. Structure, provenance, count and sample checksum checks passed; every sample record remains `review_status: unreviewed`. English meanings, POS and examples are null, not generated.

## Catalog

| Dataset | Category/task | Language/script | Records or size | Format | License | Source | Status |
|---|---|---|---|---|---|---|---|
| XNLI — Urdu | NLI / evaluation | Urdu Arabic script (font unspecified) | 400202 records (source_reported) | See versioned distribution file list; not independently validated | CC-BY-NC-4.0 | [source](https://huggingface.co/datasets/facebook/xnli) | unverified; full data link-only |
| FLORES-200 — Urdu | translation / evaluation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/facebook/flores) | unverified; full data link-only |
| Belebele — Urdu Arabic and Latin scripts | QA / reading comprehension / evaluation | Urdu Arabic and Roman (Latin) | 1800 Urdu question rows across two script variants (locally_counted) | JSONL | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/facebook/belebele) | verified; full data link-only |
| SIB-200 — Urdu | text classification / evaluation | Urdu Arabic script (font unspecified) | unknown | TSV | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/Davlan/sib200) | unverified; full data link-only |
| WikiANN — Urdu | NER | Urdu Arabic script (font unspecified) | 22000 records (source_reported) | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/unimelb-nlp/wikiann) | unverified; full data link-only |
| OPUS-100 — English–Urdu | parallel translation | Urdu Arabic script (font unspecified) | 757913 records (source_reported) | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/Helsinki-NLP/opus-100) | unverified; full data link-only |
| FLEURS — Urdu Pakistan | ASR / speech evaluation | Urdu Arabic script (font unspecified) | 2675 records (source_reported) | TSV / WAV archives / Parquet | CC-BY-4.0 | [source](https://huggingface.co/datasets/google/fleurs) | unverified; full data link-only |
| mC4 — Urdu | web corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | ODC-By-1.0 | [source](https://huggingface.co/datasets/allenai/c4) | unverified; full data link-only |
| NLLB mined bitext — Urdu | parallel translation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | ODC-By-1.0 | [source](https://huggingface.co/datasets/allenai/nllb) | unverified; full data link-only |
| OSCAR 23.01 — Urdu | web corpus | Urdu Arabic script (font unspecified) | 887004 documents (source_reported) | See versioned distribution file list; not independently validated | CC0-1.0 | [source](https://huggingface.co/datasets/oscar-corpus/OSCAR-2301) | unverified; full data link-only |
| CC-100 — Urdu | web corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/statmt/cc100) | unverified; full data link-only |
| Glot500 — Urdu | multilingual corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/cis-lmu/Glot500) | unverified; full data link-only |
| Aya Dataset — Urdu | instruction / conversation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | Apache-2.0 | [source](https://huggingface.co/datasets/CohereLabs/aya_dataset) | unverified; full data link-only |
| Aya Collection — Urdu | instruction / conversation | Urdu Arabic script (font unspecified) | 4458535 records (source_reported) | See versioned distribution file list; not independently validated | Apache-2.0 | [source](https://huggingface.co/datasets/CohereLabs/aya_collection_language_split) | unverified; full data link-only |
| IndicSentiment — Urdu | sentiment / translated text | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/ai4bharat/IndicSentiment) | unverified; full data link-only |
| XL-Sum — Urdu | news / summarization | Urdu Arabic script (font unspecified) | 84581 article-summary pairs (source_reported) | See versioned distribution file list; not independently validated | CC-BY-NC-SA-4.0 | [source](https://huggingface.co/datasets/csebuetnlp/xlsum) | unverified; full data link-only |
| Makhzan | edited text corpus | Urdu Arabic script (font unspecified) | 6.26 million words (source_reported) | annotated text; see source | unspecified | [source](https://github.com/zeerakahmed/makhzan) | unverified; full data link-only |
| Dakshina — Urdu native text (published subset) | native text corpus | Urdu Arabic script | 150000 deduplicated native text units (locally_counted) | JSONL.GZ | CC-BY-SA-4.0 | [source](https://github.com/google-research-datasets/dakshina) | verified; scoped data hosted |
| UD Urdu UDTB | POS / tokenization / morphology / dependency parsing | Urdu Arabic script (font unspecified) | unknown | CoNLL-U | CC-BY-NC-SA-4.0 | [source](https://github.com/UniversalDependencies/UD_Urdu-UDTB) | unverified; full data link-only |
| Roman Urdu Data Set | Roman Urdu / sentiment | Roman Urdu (Latin) | 20229 parsed data rows (locally_counted) | CSV | CC-BY-4.0 | [source](https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set) | pending_review; full data link-only |
| Roman Urdu Sentiment Analysis Dataset (RUSAD) | Roman Urdu / sentiment | Roman Urdu (Latin) | 11000 parsed data rows (locally_counted) | TSV | CC-BY-4.0 | [source](https://archive.ics.uci.edu/dataset/854/roman+urdu+sentiment+analysis+dataset+(rusad)) | pending_review; full data link-only |
| Tatoeba — Urdu sentences and translation links | sentences / parallel translation | Urdu Arabic script (font unspecified) | unknown | TSV compressed exports | CC-BY-2.0-FR | [source](https://tatoeba.org/en/downloads) | unverified; full data link-only |
| Urdu Wikipedia dumps | encyclopedic corpus / documents | Urdu Arabic script (font unspecified) | unknown | compressed XML dumps | unspecified | [source](https://dumps.wikimedia.org/urwiki/) | unverified; full data link-only |
| Common Voice Scripted Speech 27.0 — Urdu | ASR / speech | Urdu Arabic script (font unspecified) | unknown | MP3 / metadata | CC0-1.0 | [source](https://mozilladatacollective.com/datasets/cmu5x1w3400cyo107st8cgsoq) | unverified; full data link-only |
| fastText Common Crawl/Wikipedia — Urdu vectors | pretrained embeddings (catalog only) | Urdu Arabic script (font unspecified) | unknown | binary / text vectors | CC-BY-SA-3.0 | [source](https://fasttext.cc/docs/en/crawl-vectors.html) | unverified; full data link-only |
| ARL Urdu Speech Database, Training Data | ASR / speaker metadata | Urdu Arabic script (font unspecified) | 200 speakers (source_reported) | PCM speech / transcripts | unspecified | [source](https://catalog.ldc.upenn.edu/LDC2007S03) | unverified; full data link-only |
| CAMIO Transcription Languages | printed OCR / document layout | Urdu Arabic script (font unspecified) | unknown | images / XML annotations | unspecified | [source](https://catalog.ldc.upenn.edu/LDC2022T07) | unverified; full data link-only |
| IIIT-Urdu OCR | printed Nastaliq OCR | Urdu Nastaliq | 1610 text-line images (source_reported) | images / transcriptions; exact distribution not checked | unspecified | [source](https://ilocr.iiit.ac.in/dataset/38/) | unverified; full data link-only |

Machine-readable [JSON](catalog/datasets.json) and [typed CSV](catalog/datasets.csv) contain per-entry evidence and nullable unknowns. [Derived samples](catalog/hosted-samples.json) have a separate manifest so they do not inflate the upstream target.

## Large hosted Urdu corpus

**150,000 deduplicated native training records**, containing **2,935,498 whitespace-delimited tokens** in three compressed JSONL.GZ files (17,762,005 bytes).

This is a partial publication: 13 of the 16 files listed in the earlier full build were never uploaded. Bulk romanization pairs and the validation split are not hosted. The historical 622,805-record build is recorded separately in `full-build-manifest.json`; `manifest.json` describes only available files. Do not count missing records or tokens as published data.

CC BY-SA 4.0 and original article/revision provenance are preserved. Every record remains `review_status: unreviewed`.

[Dataset card](datasets/corpora/dakshina-urdu-bulk/DATASET_CARD.md) · [source/license attribution](datasets/corpora/dakshina-urdu-bulk/SOURCES.md) · [data shards](datasets/corpora/dakshina-urdu-bulk/data) · [manifest and counts](datasets/corpora/dakshina-urdu-bulk/manifest.json) · [streaming example](examples/bulk_loading.py)

## Hosted samples

[Dataset card](datasets/vocabulary/dakshina-urdu-sample/DATASET_CARD.md) · [Source and attribution](datasets/vocabulary/dakshina-urdu-sample/SOURCES.md) · [Data](datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl)

```python
import json
from pathlib import Path
path = Path('datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl')
rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
assert len(rows) == 25
```

[Urdu–English evaluation pairs: dataset card](datasets/translation/belebele-urdu-english-eval-sample/DATASET_CARD.md) · [source attribution](datasets/translation/belebele-urdu-english-eval-sample/SOURCES.md) · [five paired passages](datasets/translation/belebele-urdu-english-eval-sample/data/pairs.jsonl). These are copied publisher evaluation passages, joined by source IDs; no translations were generated. Every pair is locally unreviewed and evaluation-only. Do not use these held-out passages for training or model-selection validation.

[Verification evidence](catalog/data-verification.json) records complete publisher-file hashes, counts and checks. Belebele’s 1,800 Urdu script-variant rows cover 900 underlying questions, not 1,800 independent examples. Human-reviewed record count remains zero.

## Tools and examples

Python 3.10+; see [development commands](docs/DEVELOPMENT.md). Tools validate UTF-8/schema/required fields, find duplicates, convert typed CSV/JSON/JSONL, generate stats, check links and verify checksums. [Normalization](docs/NORMALIZATION.md) is opt-in, preserves original text and logs applied changes; joiners, diacritics and Heh Doachashmee are retained.

Loading examples: [plain Python](examples/plain_python.py), [pandas](examples/pandas_example.py), [Hugging Face Datasets](examples/huggingface_example.py). These examples load the local catalog and both hosted samples and do not download remote corpora or execute remote scripts.

## Rights, ethics and current limits

Code and original documentation are MIT. Each dataset retains its own license; the hosted corpus and samples are CC BY-SA 4.0 with attribution and share-alike requirements. No Makhzan raw text, NC/research-only corpus, restricted source text, secrets or private records are intentionally included. Web-corpus packaging licenses do not clear all original-content rights. See the license policy for the hosting allowlist and removal process.

No model training or unauthorized source scraping is performed. Native-speaker review is needed for the Urdu introduction, sample spellings, romanizations and future glosses. Five licensed evaluation-only Urdu–English passage pairs are hosted; broader translation coverage remains incomplete. Many task categories remain discovery gaps. Local tests, lint, schema validation and examples pass after the approved fixes. Unresolved link checks and incomplete dataset verification remain release blockers; see [the verification report](docs/VERIFICATION_REPORT.md). Source metadata is not language validation.

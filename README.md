# open-urdu-datasets

A community Urdu and Roman Urdu dataset hub with provenance, license tracking and reproducible quality tools.

**Unreleased draft.** 28 upstream discovery entries (including one embeddings resource), 0 fully verified upstream datasets, and a separate 25-record Dakshina romanization sample awaiting local native-speaker review. The target of 25 verified datasets is not met. No v0.1.0 release has been published.

[اردو تعارف — unreviewed](README.ur.md) · [Contributing](CONTRIBUTING.md) · [Licensing and removal](docs/LICENSE_POLICY.md) · [Coverage gaps](docs/COVERAGE.md)

## Verification and counts

An accessible source page is not data verification. All 28 discovery entries remain `unverified` because full scoped distributions and rights have not been independently checked. Counts below are explicitly source-reported, may overlap and must not be summed as unique records. The derived sample is excluded from independent-dataset counts.

The sample's complete upstream lexicon member was downloaded from the official archive: 106,260 romanization rows, 25,000 distinct native-script words. Its SHA-256 is recorded in SOURCES.md. The complete archive was not downloaded or hashed. Structure, provenance, count and sample checksum checks passed; every sample record remains `review_status: unreviewed`. English meanings, POS and examples are null, not generated.

## Catalog

| Dataset | Category/task | Language/script | Records or size | Format | License | Source | Status |
|---|---|---|---|---|---|---|---|
| XNLI — Urdu | NLI / evaluation | Urdu Arabic script (font unspecified) | 400202 records (source_reported) | See versioned distribution file list; not independently validated | CC-BY-NC-4.0 | [source](https://huggingface.co/datasets/facebook/xnli) | unverified; link-only |
| FLORES-200 — Urdu | translation / evaluation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/facebook/flores) | unverified; link-only |
| Belebele — Urdu Arabic and Latin scripts | QA / reading comprehension / evaluation | Urdu Arabic and Roman (Latin) | unknown | JSONL | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/facebook/belebele) | unverified; link-only |
| SIB-200 — Urdu | text classification / evaluation | Urdu Arabic script (font unspecified) | unknown | TSV | CC-BY-SA-4.0 | [source](https://huggingface.co/datasets/Davlan/sib200) | unverified; link-only |
| WikiANN — Urdu | NER | Urdu Arabic script (font unspecified) | 22000 records (source_reported) | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/unimelb-nlp/wikiann) | unverified; link-only |
| OPUS-100 — English–Urdu | parallel translation | Urdu Arabic script (font unspecified) | 757913 records (source_reported) | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/Helsinki-NLP/opus-100) | unverified; link-only |
| FLEURS — Urdu Pakistan | ASR / speech evaluation | Urdu Arabic script (font unspecified) | 2675 records (source_reported) | TSV / WAV archives / Parquet | CC-BY-4.0 | [source](https://huggingface.co/datasets/google/fleurs) | unverified; link-only |
| mC4 — Urdu | web corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | ODC-By-1.0 | [source](https://huggingface.co/datasets/allenai/c4) | unverified; link-only |
| NLLB mined bitext — Urdu | parallel translation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | ODC-By-1.0 | [source](https://huggingface.co/datasets/allenai/nllb) | unverified; link-only |
| OSCAR 23.01 — Urdu | web corpus | Urdu Arabic script (font unspecified) | 887004 documents (source_reported) | See versioned distribution file list; not independently validated | CC0-1.0 | [source](https://huggingface.co/datasets/oscar-corpus/OSCAR-2301) | unverified; link-only |
| CC-100 — Urdu | web corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/statmt/cc100) | unverified; link-only |
| Glot500 — Urdu | multilingual corpus | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/cis-lmu/Glot500) | unverified; link-only |
| Aya Dataset — Urdu | instruction / conversation | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | Apache-2.0 | [source](https://huggingface.co/datasets/CohereLabs/aya_dataset) | unverified; link-only |
| Aya Collection — Urdu | instruction / conversation | Urdu Arabic script (font unspecified) | 4458535 records (source_reported) | See versioned distribution file list; not independently validated | Apache-2.0 | [source](https://huggingface.co/datasets/CohereLabs/aya_collection_language_split) | unverified; link-only |
| IndicSentiment — Urdu | sentiment / translated text | Urdu Arabic script (font unspecified) | unknown | See versioned distribution file list; not independently validated | unspecified | [source](https://huggingface.co/datasets/ai4bharat/IndicSentiment) | unverified; link-only |
| XL-Sum — Urdu | news / summarization | Urdu Arabic script (font unspecified) | 84581 article-summary pairs (source_reported) | See versioned distribution file list; not independently validated | CC-BY-NC-SA-4.0 | [source](https://huggingface.co/datasets/csebuetnlp/xlsum) | unverified; link-only |
| Makhzan | edited text corpus | Urdu Arabic script (font unspecified) | 6.26 million words (source_reported) | annotated text; see source | unspecified | [source](https://github.com/zeerakahmed/makhzan) | unverified; link-only |
| Dakshina — Urdu | vocabulary / transliteration / sentences | Urdu Arabic and Roman (Latin) | 25000 native-script training word types (source_reported) | TSV / TXT / GZIP within TAR | CC-BY-SA-4.0 | [source](https://github.com/google-research-datasets/dakshina) | unverified; link-only |
| UD Urdu UDTB | POS / tokenization / morphology / dependency parsing | Urdu Arabic script (font unspecified) | unknown | CoNLL-U | CC-BY-NC-SA-4.0 | [source](https://github.com/UniversalDependencies/UD_Urdu-UDTB) | unverified; link-only |
| Roman Urdu Data Set | Roman Urdu / sentiment | Roman Urdu (Latin) | 20000 records (source_reported) | review-label text; exact downloadable file not validated | CC-BY-4.0 | [source](https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set) | unverified; link-only |
| Roman Urdu Sentiment Analysis Dataset (RUSAD) | Roman Urdu / sentiment | Roman Urdu (Latin) | 11000 records (source_reported) | review-label text; exact downloadable file not validated | CC-BY-4.0 | [source](https://archive.ics.uci.edu/dataset/854/roman+urdu+sentiment+analysis+dataset+(rusad)) | unverified; link-only |
| Tatoeba — Urdu sentences and translation links | sentences / parallel translation | Urdu Arabic script (font unspecified) | unknown | TSV compressed exports | CC-BY-2.0-FR | [source](https://tatoeba.org/en/downloads) | unverified; link-only |
| Urdu Wikipedia dumps | encyclopedic corpus / documents | Urdu Arabic script (font unspecified) | unknown | compressed XML dumps | unspecified | [source](https://dumps.wikimedia.org/urwiki/) | unverified; link-only |
| Common Voice Scripted Speech 27.0 — Urdu | ASR / speech | Urdu Arabic script (font unspecified) | unknown | MP3 / metadata | CC0-1.0 | [source](https://mozilladatacollective.com/datasets/cmu5x1w3400cyo107st8cgsoq) | unverified; link-only |
| fastText Common Crawl/Wikipedia — Urdu vectors | pretrained embeddings (catalog only) | Urdu Arabic script (font unspecified) | unknown | binary / text vectors | CC-BY-SA-3.0 | [source](https://fasttext.cc/docs/en/crawl-vectors.html) | unverified; link-only |
| ARL Urdu Speech Database, Training Data | ASR / speaker metadata | Urdu Arabic script (font unspecified) | 200 speakers (source_reported) | PCM speech / transcripts | unspecified | [source](https://catalog.ldc.upenn.edu/LDC2007S03) | unverified; link-only |
| CAMIO Transcription Languages | printed OCR / document layout | Urdu Arabic script (font unspecified) | unknown | images / XML annotations | unspecified | [source](https://catalog.ldc.upenn.edu/LDC2022T07) | unverified; link-only |
| IIIT-Urdu OCR | printed Nastaliq OCR | Urdu Nastaliq | 1610 text-line images (source_reported) | images / transcriptions; exact distribution not checked | unspecified | [source](https://ilocr.iiit.ac.in/dataset/38/) | unverified; link-only |


Machine-readable [JSON](catalog/datasets.json) and [typed CSV](catalog/datasets.csv) contain per-entry evidence and nullable unknowns. [Derived samples](catalog/hosted-samples.json) have a separate manifest so they do not inflate the upstream target.

## Hosted sample

[Dataset card](datasets/vocabulary/dakshina-urdu-sample/DATASET_CARD.md) · [Source and attribution](datasets/vocabulary/dakshina-urdu-sample/SOURCES.md) · [Data](datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl)

```python
import json
from pathlib import Path
path = Path('datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl')
rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
assert len(rows) == 25
```

## Tools and examples

Python 3.10+; see [development commands](docs/DEVELOPMENT.md). Tools validate UTF-8/schema/required fields, find duplicates, convert typed CSV/JSON/JSONL, generate stats, check links and verify checksums. [Normalization](docs/NORMALIZATION.md) is opt-in, preserves original text and logs applied changes; joiners, diacritics and Heh Doachashmee are retained.

Loading examples: [plain Python](examples/plain_python.py), [pandas](examples/pandas_example.py), [Hugging Face Datasets](examples/huggingface_example.py). These examples load the local catalog and do not download remote corpora or execute remote scripts.

## Rights, ethics and current limits

Code and original documentation are MIT. Each dataset retains its own license; the hosted sample is CC BY-SA 4.0 with attribution and share-alike requirements. No Makhzan raw text, NC/research-only corpus, restricted source text, secrets or private records are intentionally included. Web-corpus packaging licenses do not clear all original-content rights. See the license policy for the hosting allowlist and removal process.

No model training or unauthorized source scraping is performed. Native-speaker review is needed for the Urdu introduction, sample spellings, romanizations and future glosses. No Urdu–English pairs are hosted yet. Many task categories remain discovery gaps. Local tests, lint, schema validation and examples pass after the approved fixes. Unresolved link checks and incomplete dataset verification remain release blockers; see [the verification report](docs/VERIFICATION_REPORT.md). Source metadata is not language validation.

---
language:
- ur
pretty_name: Klam (کلام)
dataset_info:
- config_name: klam
  features:
  - name: id
    dtype: string
  - name: text
    dtype: string
  - name: language
    dtype: string
  - name: script
    dtype: string
  - name: task
    dtype: string
  - name: label
    dtype: string
  - name: split
    dtype: string
  - name: source_id
    dtype: string
  - name: source_version
    dtype: string
  - name: source_record_id
    dtype: string
  - name: source_locator
    dtype: string
  - name: rights_basis
    dtype: string
  - name: license
    dtype: string
  - name: license_url
    dtype: string
  - name: rights_evidence_url
    dtype: string
  - name: attribution
    dtype: string
  - name: review_status
    dtype: string
  - name: reviewer_id
    dtype: string
  - name: review_date
    dtype: string
  - name: review_scope
    dtype: string
  - name: title
    dtype: string
  - name: paired_text
    dtype: string
  - name: paired_script
    dtype: string
configs:
- config_name: klam
  default: true
  data_files:
  - split: train
    path: "klam-original/data/train/*.jsonl.gz"
  - split: validation
    path: "klam-original/data/validation/*.jsonl.gz"
  - split: test
    path: "klam-original/data/test/*.jsonl.gz"
- config_name: klam-chat
  data_files:
  - split: train
    path: "github-sync/training/klam-chat/train.jsonl"
  - split: validation
    path: "github-sync/training/klam-chat/validation.jsonl"
  - split: test
    path: "github-sync/training/klam-chat/test.jsonl"
---

# Klam (کلام)

Klam is one easy-to-use Urdu dataset in a single normalized JSONL.GZ format. It brings together the project's approved, pinned sources and removes duplicate records with the same normalized text, task, and label. Every row includes its source, source version, license, attribution, and review status.

The release includes rights-cleared Urdu text from Dakshina (including word and sentence transliterations), Urdu Wikisource works tagged PD-old, Urdu Wikipedia, UCI Roman Urdu sentiment datasets, AI4Bharat Sangraha verified Urdu, and a CC0 Ghalib transcription. Klam preserves the applicable source terms: licenses can differ by row. See `klam-original/DATASET_CARD.md` and `klam-original/SOURCES.md` for actual release counts, source details, and license summaries.

No automated filter counts as native-speaker review. Records without reviewer evidence are marked `unreviewed`.

## Dataset contents

| Task | Main field | Related fields |
| --- | --- | --- |
| `text` | Urdu text | `title`, `label` when supplied |
| `transliteration_pair` | Urdu-script text | `paired_text` for Roman Urdu, `label=sentence` for full sentences |
| `sentiment_classification` | Roman Urdu text | `label` for the source sentiment |

Dakshina sentence pairs follow the publisher's development and test assignments, exposed
as `validation` and `test`. The Urdu prompts come from Wikipedia and may appear in
other corpora. Exact record deduplication does not measure this evaluation overlap.

The release also includes Tatoeba Urdu sentences with author attribution and
Wikivoyage Urdu phrases paired with the source's Latin-script pronunciation
guides (`label=phrase`). These guides retain the source spelling and stress
notation.

## Load Klam

The `klam` configuration declares a shared schema across all tasks. For rows without a paired form, `paired_text` and `paired_script` load as null.

```bash
python -m pip install "datasets>=3,<5"
```

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)
for row in data.take(3):
    print(row["text"], row["license"], row["source_id"])
```

Users can load this one dataset without selecting upstream datasets or managing their revisions. Per-record provenance and license fields carry those details inside Klam.

See the [quick start](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/QUICKSTART.md) and [license policy](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/LICENSE_POLICY.md).


## Load Klam Chat

Select the `klam-chat` configuration for Urdu-script and Roman Urdu supervised fine-tuning examples. It provides separate train, validation, and test splits. Each row has a `messages` array with alternating `user` and `assistant` turns. The `script` field uses `Arab` for Urdu script and `Latn` for Roman Urdu.

```python
from datasets import load_dataset

chat = load_dataset("Daniyal643/open-urdu-datasets", "klam-chat")
print(chat["train"][0]["messages"])
```

The chat examples are AI-generated and unreviewed. They are intended for small fine-tuning trials. See the [Klam Chat dataset card](github-sync/training/klam-chat/README.md) for split counts, license information, and limitations.

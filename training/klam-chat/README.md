# Klam Chat

A starter supervised fine-tuning dataset for Urdu-script and Roman Urdu assistants. Each JSONL record has a `messages` array with alternating `user` and `assistant` turns. The corpus for continued pretraining lives in the [Klam Hugging Face release](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets).

| Split | Urdu script | Roman Urdu |
| --- | ---: | ---: |
| Train | 35 | 35 |
| Validation | 3 | 3 |
| Test | 3 | 3 |

All examples were generated for this project, are marked unreviewed, and are offered under [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). The two script variants share a `group_id` and always remain in the same split. The examples cover writing, planning, basic reasoning, explanation, summarization, and other everyday requests.

## Load the dataset

Install `datasets` with `python -m pip install datasets`. The example loads the dataset directly from GitHub. On Hugging Face, use `load_dataset("Daniyal643/open-urdu-datasets", "klam-chat")` to get all three splits. Use a commit SHA in place of `main` to reproduce a particular snapshot.

```python
from datasets import load_dataset

splits = ("train", "validation", "test")
base = "https://raw.githubusercontent.com/DaniyalMusadiq1/open-urdu-datasets/main"
data = load_dataset(
    "json",
    data_files={split: f"{base}/training/klam-chat/{split}.jsonl" for split in splits},
)
roman_urdu = data["train"].filter(lambda row: row["script"] == "Latn")
print(roman_urdu[0]["messages"])
```

Feed `messages` into your instruction model's chat template. Use train for fitting, validation for tuning, and test for a final check. Run `python scripts/validate_klam_chat.py` from a checkout with the project's Python dependencies installed.

The 82 rows are suitable for testing an SFT pipeline. A chatbot training release still needs broader task coverage, more multi-turn conversations, native-speaker review of both scripts, and a larger independent evaluation set.

## Export source-backed transliteration examples

```bash
python examples/klam_transliteration_sft.py validation transliteration-validation.jsonl
```

The exporter streams sentence pairs from a pinned Hugging Face revision and preserves the upstream split, attribution, license, and review status. It excludes word-level and pronunciation-guide rows. A split without eligible sentence pairs exports zero rows. Keep the original evaluation splits separate from training and check overlap against any pretraining corpus. These examples train or evaluate transliteration, while the chat starter exercises general instruction formatting.

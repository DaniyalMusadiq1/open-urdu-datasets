"""Export a Klam split as supervised Urdu-to-Roman-Urdu transliteration JSONL."""
import argparse
import json
from pathlib import Path

from datasets import load_dataset

DATASET = "Daniyal643/open-urdu-datasets"
REVISION = "4eccca724753a83a6b4088b26258f9e694d3a3d6"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("split", choices=("train", "validation", "test"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = load_dataset(DATASET, "klam", revision=REVISION, split=args.split, streaming=True)
    count = 0
    with args.output.open("x", encoding="utf-8") as output:
        for row in rows:
            if row["task"] != "transliteration_pair" or row["label"] != "sentence":
                continue
            if not row["text"].strip() or not row["paired_text"].strip():
                continue
            example = {
                "id": row["id"],
                "source_id": row["source_id"],
                "source_version": row["source_version"],
                "license": row["license"],
                "license_url": row["license_url"],
                "attribution": row["attribution"],
                "review_status": row["review_status"],
                "dataset_revision": REVISION,
                "source_split": args.split,
                "messages": [
                    {"role": "user", "content": "Is jumlay ko Roman Urdu mein likhein:\n"
                     + row["text"]},
                    {"role": "assistant", "content": row["paired_text"]},
                ],
            }
            output.write(json.dumps(example, ensure_ascii=False) + "\n")
            count += 1
    print(f"{args.split}: {count} sentence pairs exported")


if __name__ == "__main__":
    main()

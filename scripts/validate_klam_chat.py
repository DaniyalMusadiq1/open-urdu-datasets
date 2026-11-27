"""Validate the Klam Chat starter dataset."""
import json
import unicodedata
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPLITS = ("train", "validation", "test")


def main():
    schema = json.loads((ROOT / "training/klam-chat/schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    ids = set()
    groups = {}
    prompts = set()
    for split in SPLITS:
        path = ROOT / "training/klam-chat" / f"{split}.jsonl"
        rows = 0
        scripts = set()
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                validator.validate(row)
                rows += 1
                script = row["script"]
                scripts.add(script)
                row_id = row["id"]
                group_id = row["group_id"]
                if row_id in ids or row_id != f"{group_id}-{script}":
                    raise ValueError(f"Invalid or duplicate row ID: {row_id}")
                ids.add(row_id)
                if groups.setdefault(group_id, split) != split:
                    raise ValueError(f"Conversation group crosses splits: {group_id}")
                messages = row["messages"]
                if len(messages) % 2:
                    raise ValueError(f"Conversation must end with assistant: {row_id}")
                for index, message in enumerate(messages):
                    expected = "assistant" if index % 2 else "user"
                    if message["role"] != expected:
                        raise ValueError(f"Invalid role order: {row_id}")
                prompt = " ".join(
                    unicodedata.normalize("NFKC", messages[0]["content"]).casefold().split()
                )
                if prompt in prompts:
                    raise ValueError(f"Repeated opening prompt: {row_id}")
                prompts.add(prompt)
        if scripts != {"Arab", "Latn"}:
            raise ValueError(f"Both scripts are required in {split}")
        print(f"{split}: {rows} conversations")
    for group_id in groups:
        if not {f"{group_id}-Arab", f"{group_id}-Latn"}.issubset(ids):
            raise ValueError(f"Incomplete script pair: {group_id}")


if __name__ == "__main__":
    main()

"""Check that the published Klam card loads mixed JSONL shards without streaming."""
import gzip
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from huggingface_hub import DatasetCard

from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]


def main():
    card_path = ROOT / "datasets/HUGGINGFACE_README.md"
    schema_path = ROOT / "schemas/klam-record.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    card = DatasetCard.load(card_path)
    infos = card.data["dataset_info"]
    features = next(info["features"] for info in infos if info["config_name"] == "klam")
    names = [feature["name"] for feature in features]
    if len(names) != len(set(names)) or set(names) != set(schema["properties"]):
        raise ValueError("The published Klam features must match the normalized record schema")

    plain = dict.fromkeys(schema["required"], "")
    plain.update(id="a" * 64, text="کتاب", language="ur", script="Arabic", task="text",
                 split="train")
    paired = {
        **plain,
        "id": "b" * 64,
        "text": "یہ ایک کتاب ہے۔",
        "task": "transliteration_pair",
        "paired_text": "Yeh aik kitab hai.",
        "paired_script": "Latin",
    }
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "README.md").write_bytes(card_path.read_bytes())
        for split, rows in (
            ("train", [plain, paired]),
            ("validation", [paired]),
            ("test", [paired]),
        ):
            directory = root / "klam-original/data" / split
            directory.mkdir(parents=True)
            for index, row in enumerate(rows):
                with gzip.open(directory / f"part-{index}.jsonl.gz", "wt",
                               encoding="utf-8") as output:
                    output.write(json.dumps({**row, "split": split}, ensure_ascii=False) + "\n")

        chat_dir = root / "github-sync/training/klam-chat"
        chat_dir.mkdir(parents=True)
        for split in ("train", "validation", "test"):
            source = ROOT / "training/klam-chat" / f"{split}.jsonl"
            (chat_dir / source.name).write_bytes(source.read_bytes())

        loaded = load_dataset(str(root), "klam", cache_dir=str(root / "cache"))
        assert set(loaded) == {"train", "validation", "test"}
        assert len(loaded["train"]) == 2
        assert loaded["train"][0]["paired_text"] is None
        assert loaded["train"][0]["paired_script"] is None
        assert loaded["train"][1]["paired_text"] == paired["paired_text"]
        assert loaded["train"][1]["paired_script"] == paired["paired_script"]

        chat = load_dataset(str(root), "klam-chat", cache_dir=str(root / "cache"))
        assert set(chat) == {"train", "validation", "test"}
        assert chat["train"][0]["messages"][0]["role"] == "user"
    print("Klam corpus and chat both load with Arrow using the published dataset card.")


if __name__ == "__main__":
    main()

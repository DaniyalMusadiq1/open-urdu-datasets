"""Convert two checksummed public snapshots into Klam source inputs."""
import argparse
import bz2
import gzip
import io
import json
import re
from pathlib import Path

from build_klam_release import script_for

from urdu_data.bulk import flags
from urdu_data.core import sha256

TATOEBA_SHA = "871ad465167baa731cf9b541f1041958d48df60d5811edd3da2b46ae173548e1"
PHRASEBOOK_SHA = "9b52aaf63dd2ad8b3970d15cee3a89ff7beb5deb17bacb822a7384a90d6763f3"
PHRASEBOOK_URL = "https://en.wikivoyage.org/w/index.php?title=Urdu_phrasebook&oldid=5320526"
LANG_TEMPLATE = re.compile(r"\{\{lang\|ur\|([^{}|]+)\}\}", re.IGNORECASE)
PAIR = re.compile(r"(.+?)\s+\(([^()]*)\)\s*$")


def tatoeba_rows(path):
    with bz2.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            sentence_id, language, text, author, _, _ = line.rstrip("\r\n").split("\t")
            if language != "urd":
                raise ValueError("expected the Urdu Tatoeba export")
            if not author or author == r"\N" or script_for(text) != "Arabic" or flags(text):
                continue
            yield {
                "text": text,
                "source_record_id": sentence_id,
                "source_locator": f"https://tatoeba.org/en/sentences/show/{sentence_id}",
                "author": author,
            }


def phrasebook_rows(path):
    in_phrases = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line == "===Basics===":
            in_phrases = True
        if not in_phrases:
            continue
        if line.startswith("; ") and " : " in line:
            content = line.split(" : ", 1)[1]
        elif line.startswith(": "):
            content = line[2:]
        else:
            continue
        content = LANG_TEMPLATE.sub(r"\1", content).replace("''", "").strip()
        if any(char in content for char in "{}[]<>|/") or "___" in content:
            continue
        match = PAIR.fullmatch(content)
        if match is None:
            continue
        text, roman = (side.strip().strip('"') for side in match.groups())
        if script_for(text) != "Arabic" or script_for(roman) != "Latin":
            continue
        if not re.search(r"[A-Za-z]", roman) or flags(text + " " + roman):
            continue
        yield {
            "text": text,
            "paired_text": roman,
            "source_record_id": f"5320526:{number}",
            "source_locator": PHRASEBOOK_URL,
        }


def prepare(tatoeba, phrasebook, output):
    if sha256(tatoeba) != TATOEBA_SHA or sha256(phrasebook) != PHRASEBOOK_SHA:
        raise ValueError("source snapshot checksum mismatch")
    for name, rows in (
        ("tatoeba-urdu", tatoeba_rows(tatoeba)),
        ("wikivoyage-urdu-phrasebook", phrasebook_rows(phrasebook)),
    ):
        with (output / f"{name}.jsonl.gz").open("xb") as raw, gzip.GzipFile(
            filename="", fileobj=raw, mode="wb", mtime=0
        ) as compressed, io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tatoeba", type=Path)
    parser.add_argument("phrasebook", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prepare(args.tatoeba, args.phrasebook, args.output)

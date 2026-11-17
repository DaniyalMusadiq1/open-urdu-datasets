"""Reproduce vocabulary JSONL from an existing, checksum-verified upstream member.

Usage: python scripts/select_vocabulary_sample.py /path/to/ur.translit.sampled.train.tsv new.jsonl
No downloads or overwriting. See SOURCES.md for the official archive and byte range.
"""
import argparse
import json

from urdu_data.core import sha256, write_records

EXPECTED = "41f4f4109e60813f578a70a75b19189acb907e800a862401b7205f6f4a51e7f2"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    if sha256(args.source) != EXPECTED:
        raise ValueError("upstream member checksum differs")
    words = {}
    with open(args.source, encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            native, roman, count = line.rstrip("\n").split("\t")
            words.setdefault(native, []).append((line_number, roman, int(count)))
    rows = []
    for native, options in list(words.items())[:25]:
        line, roman, count = max(options, key=lambda item: item[2])
        rows.append({"urdu": native, "roman": roman, "english": None, "pos": None,
                     "example": None, "source": {
                         "url": "https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar",
                         "version": "1.0",
                         "member": "dakshina_dataset_v1.0/ur/lexicons/ur.translit.sampled.train.tsv",
                         "line": line, "upstream_sha256": EXPECTED},
                     "license": "CC-BY-SA-4.0", "review_status": "unreviewed",
                     "attestations": count})
    write_records(args.output, rows)


if __name__ == "__main__":
    main()

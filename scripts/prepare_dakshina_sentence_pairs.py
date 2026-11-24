"""Prepare Klam's Dakshina sentence pairs from the pinned official archive."""
import argparse
import gzip
import json
import tarfile
from collections import Counter, defaultdict
from pathlib import Path

from build_klam_release import canonical
from import_dakshina_bulk import ARCHIVE_SHA256, PREFIX

from urdu_data.bulk import flags
from urdu_data.core import sha256


def prepare(archive, output):
    if sha256(archive) != ARCHIVE_SHA256:
        raise ValueError("Dakshina archive checksum mismatch")

    counts = Counter()
    rows = []
    seen = set()
    with tarfile.open(archive) as tar:
        wiki = PREFIX + "native_script_wikipedia/"
        with gzip.GzipFile(fileobj=tar.extractfile(wiki + "ur.wiki-full.urls.tsv.gz")) as urls:
            revisions = {}
            for line in urls:
                page, _revision, _url, revision_url = line.decode("utf-8").rstrip("\r\n").split("\t")
                revisions[page] = revision_url.replace("http://", "https://", 1)

        locators = defaultdict(set)
        member = wiki + "ur.wiki-filt.valid.text.sorted.tsv.gz"
        with gzip.GzipFile(fileobj=tar.extractfile(member)) as prompts:
            for line in prompts:
                page, _, _, _, _, _, text = line.decode("utf-8").rstrip("\r\n").split("\t", 6)
                locators[canonical(text)].add(revisions[page])

        for upstream_split, split in (("test", "test"), ("dev", "validation")):
            stem = PREFIX + f"romanized/ur.romanized.rejoined.{upstream_split}"
            with tar.extractfile(stem + ".native.txt") as native, tar.extractfile(
                stem + ".roman.txt"
            ) as roman:
                for number, (left, right) in enumerate(zip(native, roman, strict=True), 1):
                    text = left.decode("utf-8").rstrip("\r\n")
                    paired_text = right.decode("utf-8").rstrip("\r\n")
                    counts["input"] += 1
                    if not text.strip() or not paired_text.strip() or flags(text + " " + paired_text):
                        counts["excluded_text"] += 1
                        continue
                    key = canonical(text), canonical(paired_text)
                    urls = locators.get(key[0], set())
                    if len(urls) != 1:
                        counts["missing_or_ambiguous_attribution"] += 1
                        continue
                    if key in seen:
                        counts["duplicates"] += 1
                        continue
                    seen.add(key)
                    rows.append({
                        "text": text,
                        "paired_text": paired_text,
                        "source_record_id": f"{stem}:{number}",
                        "source_locator": next(iter(urls)),
                        "split": split,
                        "review_status": "unreviewed",
                    })
                    counts[split] += 1
    if not counts["test"] or not counts["validation"]:
        raise ValueError("Expected attributed sentence pairs in both upstream splits")
    with output.open("xb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
        for row in rows:
            out.write((json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
    return dict(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.archive, args.output), sort_keys=True))

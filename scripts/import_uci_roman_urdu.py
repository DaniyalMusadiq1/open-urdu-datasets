"""Build an auditable Roman Urdu sentiment release from two official UCI archives."""
import argparse
import csv
import glob
import gzip
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path

SOURCES = {
    "458": {
        "member": "Roman Urdu DataSet.csv",
        "delimiter": ",",
        "url": "https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set",
        "archive_url": "https://archive.ics.uci.edu/static/public/458/roman+urdu+data+set.zip",
        "archive_sha256": "78e7cd1d7b0dc8e960a52c9151fc3114c70a3809111d3421581bbad931a6f5a8",
        "member_sha256": "d9b54d3685b6ef691cb4a2cc0783fc189dcfa0560cca9afec1099b015c798c7c",
        "text_col": 0,
        "label_col": 1,
        "valid_labels": {"Positive", "Neutral", "Negative"},
        "doi": "10.24432/C58325",
    },
    "854": {
        "member": "Dataset 11000 Reviews.tsv",
        "delimiter": "\t",
        "url": "https://archive.ics.uci.edu/dataset/854/roman+urdu+sentiment+analysis+dataset+(rusad)",
        "archive_url": "https://archive.ics.uci.edu/static/public/854/roman+urdu+sentiment+analysis+dataset+(rusad).zip",
        "archive_sha256": "4fe3618d9353abe27fb94414f2741b8ed634a4467cec056be4a10732ec9a0be5",
        "member_sha256": "da1241192b8a39f68a8482e890120fd2fbc03aab3ae1617ee4ccd168671a4e9e",
        "text_col": 1,
        "label_col": 0,
        "valid_labels": {"pos", "neg"},
        "doi": "10.24432/C59046",
    },
}
CONTACT = re.compile(
    r"(?i)(?:[\w.+-]+@[\w.-]+\.[a-z]{2,}|(?:\+?\d[\d\s().-]{8,}\d)|"
    r"https?://\S+|@[A-Za-z0-9_]{2,})"
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def read_source(source_id, archive):
    meta = SOURCES[source_id]
    raw_archive = archive.read_bytes()
    if sha256(raw_archive) != meta["archive_sha256"]:
        raise ValueError(f"{source_id}: archive checksum mismatch")
    with zipfile.ZipFile(archive) as zf:
        names = [name for name in zf.namelist() if not name.endswith("/")]
        if names != [meta["member"]]:
            raise ValueError(f"{source_id}: unexpected archive members: {names}")
        raw = zf.read(meta["member"])
    if sha256(raw) != meta["member_sha256"]:
        raise ValueError(f"{source_id}: source member checksum mismatch")
    rows = csv.reader(raw.decode("utf-8-sig").splitlines(), delimiter=meta["delimiter"])
    accepted, rejected, seen = [], {}, set()
    source_records = 0
    for row_no, row in enumerate(rows, start=1):
        source_records += 1
        def reject(reason):
            rejected[reason] = rejected.get(reason, 0) + 1
        if len(row) < 2 or (len(row) > 2 and any(value.strip() for value in row[2:])):
            reject("malformed_row")
            continue
        text = row[meta["text_col"]].strip()
        label = row[meta["label_col"]].strip()
        if label not in meta["valid_labels"]:
            reject("invalid_label")
            continue
        if len(text) < 20:
            reject("short_text_under_20_chars")
            continue
        if CONTACT.search(text):
            reject("contact_pattern_triage")
            continue
        identity = sha256(canonical(text).encode("utf-8"))
        if identity in seen:
            reject("exact_duplicate_within_source")
            continue
        seen.add(identity)
        accepted.append({
            "id": identity,
            "text": text,
            "sentiment": label.lower(),
            "source_label": label,
            "source_id": f"UCI-{source_id}",
            "source_row": row_no,
            "source_doi": meta["doi"],
            "source_url": meta["url"],
            "license": "CC-BY-4.0",
            "review_status": "unreviewed",
            "token_count_whitespace": len(text.split()),
        })
    return accepted, {
        "archive_sha256": sha256(raw_archive),
        "source_member_sha256": sha256(raw),
        "source_rows": source_records,
        "accepted_records": len(accepted),
        "accepted_whitespace_tokens": sum(row["token_count_whitespace"] for row in accepted),
        "rejected": rejected,
        "accepted_labels": {
            label: sum(row["source_label"] == label for row in accepted)
            for label in sorted({row["source_label"] for row in accepted})
        },
    }


def published_text_hashes(root, excluded):
    """Collect hashes of published text fields before cross-source deduplication."""
    excluded = [Path(path).resolve() for path in excluded]
    hashes = set()
    seen_records = 0
    paths = sorted(glob.glob(str(root / "**/*.jsonl"), recursive=True)
                   + glob.glob(str(root / "**/*.jsonl.gz"), recursive=True))
    for name in paths:
        path = Path(name)
        if any(path.resolve() == folder or folder in path.resolve().parents
               for folder in excluded):
            continue
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                try:
                    row = json.loads(line)
                except (ValueError, TypeError):
                    continue
                seen_records += 1
                if isinstance(row, dict):
                    for value in row.values():
                        if isinstance(value, str) and value.strip():
                            hashes.add(sha256(canonical(value).encode("utf-8")))
    return hashes, seen_records


def build(archives, out, existing_root=Path("datasets"), shard_records=1000,
          excluded_existing=(Path("datasets/classification/uci-roman-urdu-sentiment"),)):
    out = Path(out)
    if out.exists():
        raise FileExistsError(out)
    if shard_records < 1:
        raise ValueError("shard_records must be positive")
    all_rows, source_results = [], {}
    for source_id, archive in archives.items():
        rows, result = read_source(source_id, Path(archive))
        all_rows.extend(rows)
        source_results[source_id] = result
    excluded_existing = list(dict.fromkeys([*excluded_existing, out]))
    existing_hashes, existing_records_scanned = published_text_hashes(existing_root, excluded_existing)
    new_seen = set()
    unique_rows, cross_source_duplicates = [], 0
    existing_duplicates = 0
    for row in all_rows:
        if row["id"] in existing_hashes:
            existing_duplicates += 1
            continue
        if row["id"] in new_seen:
            cross_source_duplicates += 1
            continue
        new_seen.add(row["id"])
        unique_rows.append(row)
    out.mkdir(parents=True)
    data_dir = out / "data"
    data_dir.mkdir()
    shards = []
    for shard_no, start in enumerate(range(0, len(unique_rows), shard_records), start=1):
        rows = unique_rows[start:start + shard_records]
        relative = f"data/train-{shard_no:04d}.jsonl.gz"
        data_path = out / relative
        with (data_path.open("wb") as raw_output,
              gzip.GzipFile(fileobj=raw_output, mode="wb", filename="", mtime=0) as zipped,
              io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as stream):
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        payload = data_path.read_bytes()
        shards.append({"path": relative, "records": len(rows),
                       "tokens": sum(r["token_count_whitespace"] for r in rows),
                       "bytes": len(payload), "sha256": sha256(payload)})
    token_total = sum(r["token_count_whitespace"] for r in unique_rows)
    manifest = {
        "status": "published_candidate",
        "dataset": "UCI Roman Urdu sentiment datasets 458 and 854",
        "license": "CC-BY-4.0",
        "record_count": len(unique_rows),
        "whitespace_delimited_tokens": token_total,
        "human_verified_records": 0,
        "review_status": "unreviewed",
        "sources": source_results,
        "cross_source_exact_duplicates_removed": cross_source_duplicates,
        "existing_published_exact_duplicates_removed": existing_duplicates,
        "existing_published_records_scanned": existing_records_scanned,
        "existing_published_text_field_hashes_scanned": len(existing_hashes),
        "existing_corpus_exclusions": [str(path) for path in excluded_existing],
        "deduplication": "SHA-256 of NFC-normalized text with repeated whitespace collapsed; exact only",
        "pii_screening": "Email, phone-like, URL and @handle patterns rejected as triage; not a privacy guarantee",
        "shards": shards,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (out / "checksums.sha256").write_text(
        "".join(f'{item["sha256"]}  {item["path"]}\n' for item in shards), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uci458", required=True)
    parser.add_argument("--uci854", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--existing-root", default="datasets")
    parser.add_argument("--shard-records", type=int, default=1000)
    parser.add_argument("--exclude-existing-path", action="append", default=[])
    args = parser.parse_args()
    exclusions = [Path("datasets/classification/uci-roman-urdu-sentiment"),
                  *[Path(path) for path in args.exclude_existing_path]]
    print(json.dumps(build({"458": args.uci458, "854": args.uci854}, args.out,
                           Path(args.existing_root), args.shard_records, exclusions), indent=2))


if __name__ == "__main__":
    main()

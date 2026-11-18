"""Build a reproducible, rights-filtered corpus from a pinned Urdu Wikisource dump."""
import argparse
import bz2
import glob
import gzip
import hashlib
import io
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import quote

import mwparserfromhell

DUMP_URL = (
    "https://dumps.wikimedia.org/other/mediawiki_content_current/urwikisource/"
    "2026-11-01/xml/bzip2/urwikisource-2026-11-01-p1p13930.xml.bz2"
)
DUMP_SHA256 = "91d115f44f561366acdeead2d83f7e4b2426c77d527abe0eb1f124fd5c56cb60"
NAMESPACE = "{http://www.mediawiki.org/xml/export-0.11/}"
CONTACT = re.compile(
    r"(?i)(?:[\w.+-]+@[\w.-]+\.[a-z]{2,}|(?:\+?\d[\d\s().-]{8,}\d)|"
    r"https?://\S+|@[A-Za-z0-9_]{2,})"
)
CONFLICTING_LICENSE_MARKERS = (
    "no license", "noncommercial", "non-commercial", "non commercial",
    "no derivatives", "no-derivatives", "fair use", "copyrighted",
)


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def published_hashes(root, excluded):
    excluded = [Path(path).resolve() for path in excluded]
    hashes, records = set(), 0
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
                records += 1
                if isinstance(row, dict):
                    for value in row.values():
                        if isinstance(value, str) and value.strip():
                            hashes.add(digest_bytes(canonical(value).encode("utf-8")))
    return hashes, records


def extract_page(title, revision, timestamp, wikitext):
    code = mwparserfromhell.parse(wikitext)
    templates = {
        str(template.name).strip().replace("_", " ").casefold()
        for template in code.filter_templates(recursive=True)
    }
    if "pd-old" not in templates:
        return None, "missing_explicit_pd_old"
    if any(marker in name for name in templates for marker in CONFLICTING_LICENSE_MARKERS):
        return None, "conflicting_license_marker"
    text = code.strip_code(normalize=True, collapse=True)
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    letters = sum(char.isalpha() for char in text)
    arabic_letters = sum("\u0600" <= char <= "\u06ff" for char in text)
    if len(text) < 100 or letters < 40:
        return None, "short_or_empty_after_extraction"
    if arabic_letters / max(1, letters) < 0.60:
        return None, "low_urdu_arabic_script_ratio"
    if CONTACT.search(text):
        return None, "contact_pattern_triage"
    page = quote(title.replace(" ", "_"), safe="()!$&'*+,;=:@-._~")
    page_url = "https://ur.wikisource.org/wiki/" + page
    revision_url = (
        "https://ur.wikisource.org/w/index.php?title=" + page + "&oldid=" + str(revision)
    )
    history_url = (
        "https://ur.wikisource.org/w/index.php?title=" + page + "&action=history"
    )
    identity = digest_bytes(canonical(text).encode("utf-8"))
    return {
        "id": identity,
        "text": text,
        "title": title,
        "source_url": page_url,
        "revision_id": int(revision),
        "revision_timestamp": timestamp,
        "revision_url": revision_url,
        "history_url": history_url,
        "work_status": "PD-old",
        "license": "CC-BY-SA-4.0",
        "review_status": "unreviewed",
        "token_count_whitespace": len(text.split()),
    }, None


def build(dump, out, existing_root=Path("datasets"), shard_records=200,
          excluded_existing=(Path("datasets/corpora/urwikisource-pd-old"),)):
    dump, out = Path(dump), Path(out)
    if out.exists():
        raise FileExistsError(out)
    if shard_records < 1:
        raise ValueError("shard_records must be positive")
    dump_sha = hashlib.file_digest(dump.open("rb"), "sha256").hexdigest()
    if dump_sha != DUMP_SHA256:
        raise ValueError("dump checksum mismatch")
    excluded = list(dict.fromkeys([*excluded_existing, out]))
    existing, existing_records = published_hashes(existing_root, excluded)
    counts, rejected, new_seen, rows = Counter(), Counter(), set(), []
    with bz2.open(dump, "rb") as stream:
        for _, element in ET.iterparse(stream, events=("end",)):
            if element.tag == NAMESPACE + "page":
                namespace = element.findtext(NAMESPACE + "ns", default="-1")
                if namespace == "0":
                    counts["main_namespace_pages"] += 1
                    title = element.findtext(NAMESPACE + "title", default="")
                    revision = element.find(NAMESPACE + "revision")
                    if revision is None:
                        rejected["missing_revision"] += 1
                    else:
                        revision_id = revision.findtext(NAMESPACE + "id", default="")
                        timestamp = revision.findtext(NAMESPACE + "timestamp", default="")
                        text_element = revision.find(NAMESPACE + "text")
                        wikitext = text_element.text or "" if text_element is not None else ""
                        row, reason = extract_page(title, revision_id, timestamp, wikitext)
                        if reason:
                            rejected[reason] += 1
                        else:
                            counts["explicit_pd_old_pages"] += 1
                            identity = row["id"]
                            if identity in existing:
                                rejected["duplicate_existing_published_text"] += 1
                            elif identity in new_seen:
                                rejected["exact_duplicate_new_source"] += 1
                            else:
                                new_seen.add(identity)
                                rows.append(row)
                element.clear()

    out.mkdir(parents=True)
    data_dir = out / "data"
    data_dir.mkdir()
    shards = []
    for index, start in enumerate(range(0, len(rows), shard_records), start=1):
        batch = rows[start:start + shard_records]
        relative = f"data/pages-{index:04d}.jsonl.gz"
        path = out / relative
        with (path.open("wb") as raw,
              gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped,
              io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as text_stream):
            for row in batch:
                text_stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        payload = path.read_bytes()
        shards.append({"path": relative, "records": len(batch),
                       "tokens": sum(row["token_count_whitespace"] for row in batch),
                       "bytes": len(payload), "sha256": digest_bytes(payload)})
    total_tokens = sum(row["token_count_whitespace"] for row in rows)
    manifest = {
        "status": "local_unpublished",
        "source": {"url": DUMP_URL, "sha256": dump_sha,
                   "snapshot_date": "2026-11-01", "pages_in_dump_main_namespace": counts["main_namespace_pages"]},
        "rights_filter": "Only main-namespace revisions containing the explicit {{PD-old}} tag; worldwide public-domain tag per Wikisource copyright policy",
        "record_count": len(rows),
        "whitespace_delimited_tokens": total_tokens,
        "human_verified_records": 0,
        "review_status": "unreviewed",
        "counts": dict(counts),
        "rejected": dict(rejected),
        "existing_published_records_scanned": existing_records,
        "existing_published_text_field_hashes_scanned": len(existing),
        "existing_corpus_exclusions": [str(path) for path in excluded],
        "deduplication": "Exact SHA-256 of NFC-normalized text after whitespace collapse; exact record matches only",
        "text_extraction": "mwparserfromhell strip_code(normalize=True, collapse=True); blank lines removed; original Unicode text not corrected or translated",
        "pii_screening": "Email, phone-like, URL and @handle patterns rejected as triage only; not a privacy guarantee",
        "shards": shards,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (out / "checksums.sha256").write_text(
        "".join(f'{item["sha256"]}  {item["path"]}\n' for item in shards), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dump")
    parser.add_argument("out")
    parser.add_argument("--existing-root", default="datasets")
    parser.add_argument("--shard-records", type=int, default=200)
    parser.add_argument("--exclude-existing-path", action="append", default=[])
    args = parser.parse_args()
    excluded = [Path("datasets/corpora/urwikisource-pd-old"),
                *[Path(path) for path in args.exclude_existing_path]]
    print(json.dumps(build(args.dump, args.out, Path(args.existing_root),
                           args.shard_records, excluded), indent=2))


if __name__ == "__main__":
    main()

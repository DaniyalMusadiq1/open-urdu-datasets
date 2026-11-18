"""Import a pinned Urdu Wikipedia article dump with attribution and deduplication."""
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
    "https://dumps.wikimedia.org/urwiki/20261101/"
    "urwiki-20261101-pages-articles.xml.bz2"
)
DUMP_SHA256 = "5cf02a04981c9efe8698ad880b09ca74e6404513a3c7cdb4eea9291ab8e52d0d"
NAMESPACE = "{http://www.mediawiki.org/xml/export-0.11/}"
EMAIL = re.compile(r"(?i)[\w.+-]+@[\w.-]+\.[a-z]{2,}")
RESTRICTED_TEMPLATE_MARKERS = (
    "copyright violation", "copyvio", "non-free text", "non free text",
    "fair use text", "permission pending", "permission required",
    "no permission", "copyrighted material", "کاپی رائٹ کی خلاف ورزی",
)


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def published_hashes(root):
    hashes, records = set(), 0
    paths = sorted(glob.glob(str(root / "**/*.jsonl"), recursive=True)
                   + glob.glob(str(root / "**/*.jsonl.gz"), recursive=True))
    for name in paths:
        path = Path(name)
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


def extract_page(title, page_id, revision_id, timestamp, wikitext):
    if wikitext.lstrip().casefold().startswith("#redirect"):
        return None, "redirect"
    code = mwparserfromhell.parse(wikitext)
    templates = {
        str(template.name).strip().replace("_", " ").casefold()
        for template in code.filter_templates(recursive=True)
    }
    if any(marker in name for name in templates for marker in RESTRICTED_TEMPLATE_MARKERS):
        return None, "rights_exception_template"
    text = code.strip_code(normalize=True, collapse=True)
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    letters = sum(char.isalpha() for char in text)
    arabic_letters = sum("\u0600" <= char <= "\u06ff" for char in text)
    if len(text) < 250 or letters < 100:
        return None, "short_or_empty_after_extraction"
    if arabic_letters / max(1, letters) < 0.55:
        return None, "low_urdu_arabic_script_ratio"
    if EMAIL.search(text):
        return None, "email_pattern_triage"
    slug = quote(title.replace(" ", "_"), safe="()!$&'*+,;=:@-._~")
    page_url = "https://ur.wikipedia.org/wiki/" + slug
    revision_url = (
        "https://ur.wikipedia.org/w/index.php?title=" + slug + "&oldid=" + str(revision_id)
    )
    history_url = "https://ur.wikipedia.org/w/index.php?title=" + slug + "&action=history"
    identity = digest_bytes(canonical(text).encode("utf-8"))
    return {
        "id": identity,
        "text": text,
        "title": title,
        "page_id": int(page_id),
        "source_url": page_url,
        "revision_id": int(revision_id),
        "revision_timestamp": timestamp,
        "revision_url": revision_url,
        "history_url": history_url,
        "license": "CC-BY-SA-4.0",
        "review_status": "unreviewed",
        "source_markup_removed": True,
        "token_count_whitespace": len(text.split()),
    }, None


def write_shard(out, index, batch):
    relative = f"data/articles-{index:04d}.jsonl.gz"
    path = out / relative
    with (path.open("wb") as raw,
          gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped,
          io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as text_stream):
        for row in batch:
            text_stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    payload = path.read_bytes()
    return {"path": relative, "records": len(batch),
            "tokens": sum(row["token_count_whitespace"] for row in batch),
            "bytes": len(payload), "sha256": digest_bytes(payload)}


def build(dump, out, existing_root=Path("datasets"), shard_records=3000):
    dump, out = Path(dump), Path(out)
    if out.exists():
        raise FileExistsError(out)
    if not DUMP_SHA256:
        raise ValueError("pin DUMP_SHA256 before importing")
    if shard_records < 1:
        raise ValueError("shard_records must be positive")
    with dump.open("rb") as stream:
        dump_sha = hashlib.file_digest(stream, "sha256").hexdigest()
    if dump_sha != DUMP_SHA256:
        raise ValueError("dump checksum mismatch")
    existing, existing_records = published_hashes(existing_root)
    out.mkdir(parents=True)
    (out / "data").mkdir()
    counts, rejected, new_seen = Counter(), Counter(), set()
    rows, shards, total_tokens = [], [], 0
    total_records = 0
    with bz2.open(dump, "rb") as stream:
        context = ET.iterparse(stream, events=("start", "end"))
        root = None
        for event, element in context:
            if event == "start":
                if root is None:
                    root = element
                continue
            if element.tag == NAMESPACE + "page":
                namespace = element.findtext(NAMESPACE + "ns", default="-1")
                if namespace == "0":
                    counts["main_namespace_pages"] += 1
                    title = element.findtext(NAMESPACE + "title", default="")
                    page_id = element.findtext(NAMESPACE + "id", default="")
                    revision = element.find(NAMESPACE + "revision")
                    if revision is None:
                        rejected["missing_revision"] += 1
                    else:
                        revision_id = revision.findtext(NAMESPACE + "id", default="")
                        timestamp = revision.findtext(NAMESPACE + "timestamp", default="")
                        text_element = revision.find(NAMESPACE + "text")
                        wikitext = text_element.text or "" if text_element is not None else ""
                        row, reason = extract_page(title, page_id, revision_id,
                                                   timestamp, wikitext)
                        if reason:
                            rejected[reason] += 1
                        else:
                            counts["rights_filtered_urdu_candidates"] += 1
                            identity = row["id"]
                            if identity in existing:
                                rejected["duplicate_existing_published_text"] += 1
                            elif identity in new_seen:
                                rejected["exact_duplicate_new_source"] += 1
                            else:
                                new_seen.add(identity)
                                total_records += 1
                                rows.append(row)
                                if len(rows) >= shard_records:
                                    shard = write_shard(out, len(shards) + 1, rows)
                                    shards.append(shard)
                                    total_tokens += shard["tokens"]
                                    rows.clear()
                if counts["main_namespace_pages"] and counts["main_namespace_pages"] % 100000 == 0:
                    print(json.dumps({"pages_scanned": counts["main_namespace_pages"],
                                      "records_written": len(new_seen),
                                      "shards_written": len(shards)}), flush=True)
                element.clear()
                root.clear()

    if rows:
        shard = write_shard(out, len(shards) + 1, rows)
        shards.append(shard)
        total_tokens += shard["tokens"]
    manifest = {
        "status": "local_unpublished",
        "source": {"url": DUMP_URL, "sha256": dump_sha,
                   "snapshot_date": "2026-11-01",
                   "pages_in_dump_main_namespace": counts["main_namespace_pages"]},
        "rights_filter": "Urdu Wikipedia text terms; main namespace only; pages with common explicit rights-exception templates excluded. Page/revision URLs retained for attribution.",
        "record_count": total_records,
        "whitespace_delimited_tokens": total_tokens,
        "human_verified_records": 0,
        "review_status": "unreviewed",
        "counts": dict(counts),
        "rejected": dict(rejected),
        "existing_published_records_scanned": existing_records,
        "existing_published_text_field_hashes_scanned": len(existing),
        "deduplication": "Exact SHA-256 of NFC-normalized text after whitespace collapse; exact matches only",
        "text_extraction": "mwparserfromhell strip_code(normalize=True, collapse=True); blank lines removed; original Urdu wording is not corrected or translated",
        "privacy_screening": "Email-pattern triage only; not a privacy guarantee",
        "attribution": "Each record links to the page, exact revision and page history per Wikimedia attribution terms",
        "modifications": ["MediaWiki markup removed", "page restricted to Urdu-script text by mechanical ratio filter"],
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
    parser.add_argument("--shard-records", type=int, default=3000)
    args = parser.parse_args()
    print(json.dumps(build(args.dump, args.out, Path(args.existing_root),
                           args.shard_records), indent=2))


if __name__ == "__main__":
    main()

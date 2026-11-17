"""Import only explicitly named Urdu members from the verified official archive.

Creates a NEW output directory and a separate work database. No source scraping,
normalization, model training, invented translations, or replacement of files.
"""
import argparse
import gzip
import hashlib
import io
import json
import sqlite3
import tarfile
from collections import Counter
from pathlib import Path

from urdu_data.bulk import flags, identity
from urdu_data.core import sha256

ARCHIVE_URL = "https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar"
ARCHIVE_SHA256 = "83530bec211893d9df429298f42e63c350c25ad56f9f5172f85edb0575ee5b03"
PREFIX = "dakshina_dataset_v1.0/ur/"


def run(archive, output, work_db, shard_rows=50000):
    archive, output, work_db = Path(archive), Path(output), Path(work_db)
    if output.exists() or work_db.exists():
        raise FileExistsError("output directory and work database must be new")
    if sha256(archive) != ARCHIVE_SHA256:
        raise ValueError("official archive SHA-256 differs; do not continue")
    if not 1 <= shard_rows <= 50000:
        raise ValueError("shard_rows must be between 1 and 50000")
    output.mkdir(parents=True)
    data_dir = output / "data"
    data_dir.mkdir()
    db = sqlite3.connect(work_db)
    db.execute("CREATE TABLE pages (id TEXT PRIMARY KEY, revision TEXT, url TEXT, revision_url TEXT)")
    db.execute("CREATE TABLE records (id TEXT PRIMARY KEY, kind TEXT, split TEXT, text TEXT, "
               "roman TEXT, source TEXT, attestations INTEGER, occurrences INTEGER, ordinal INTEGER)")
    stats = Counter()
    excluded = Counter()
    member_evidence = []
    ordinal = 0
    exclusions_path = output / "excluded-source-rows.jsonl"
    with tarfile.open(archive) as tar, exclusions_path.open("x", encoding="utf-8") as rejected:
        members = {member.name: member for member in tar.getmembers()}

        def lines(name, compressed):
            member = members[name]
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError("missing file stream")
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
            stream.close()
            checksum = digest.hexdigest()
            member_evidence.append({"member": name, "bytes": member.size, "sha256": checksum})
            stream = tar.extractfile(member)
            if compressed:
                stream = gzip.GzipFile(fileobj=stream)
            return io.TextIOWrapper(stream, encoding="utf-8", newline=""), checksum

        url_member = PREFIX + "native_script_wikipedia/ur.wiki-full.urls.tsv.gz"
        stream, _ = lines(url_member, True)
        with stream, db:
            for line in stream:
                fields = line.removesuffix("\n").split("\t")
                if len(fields) != 4:
                    raise ValueError("invalid page attribution row")
                page, revision, url, revision_url = fields
                if not page.isdigit() or not revision.isdigit():
                    raise ValueError("invalid page/revision identifier")
                if not all(u.startswith(("https://ur.wikipedia.org/", "http://ur.wikipedia.org/"))
                           for u in [url, revision_url]):
                    raise ValueError("unexpected article attribution host")
                db.execute("INSERT INTO pages VALUES (?,?,?,?)", fields)
                stats["attribution_pages"] += 1
        print("loaded attribution pages", stats["attribution_pages"], flush=True)

        def keep(kind, split, text, roman, source, attestations=None):
            nonlocal ordinal
            stats["candidate_" + kind] += 1
            reasons = flags(text + (" " + roman if roman else ""))
            if not text or (roman is not None and not roman):
                reasons.append("empty_text")
            if reasons:
                for reason in reasons:
                    excluded[reason] += 1
                rejected.write(json.dumps({"member": source["member"], "line": source["line"],
                                           "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                                           "reasons": reasons}) + "\n")
                stats["excluded_rows"] += 1
                return
            key = identity(kind, text, roman)
            previous = db.execute("SELECT text,roman,split FROM records WHERE id=?", (key,)).fetchone()
            if previous:
                if previous[:2] != (text, roman):
                    raise ValueError("hash collision")
                db.execute("UPDATE records SET occurrences=occurrences+1 WHERE id=?", (key,))
                stats["duplicate_rows_" + kind] += 1
                if previous[2] != split:
                    stats["cross_split_duplicates_" + kind] += 1
                return
            ordinal += 1
            db.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?)", (
                key, kind, split, text, roman, json.dumps(source, ensure_ascii=False),
                attestations, 1, ordinal))

        # Validation first: exact duplicates shared with training remain in validation.
        for split, source_split in [("validation", "valid"), ("train", "train")]:
            name = PREFIX + f"native_script_wikipedia/ur.wiki-filt.{source_split}.text.sorted.tsv.gz"
            stream, checksum = lines(name, True)
            with stream, db:
                for number, line in enumerate(stream, 1):
                    stats["raw_native_rows"] += 1
                    fields = line.removesuffix("\n").split("\t", 6)
                    if len(fields) != 7 or fields[4] not in {"0", "1"}:
                        raise ValueError("invalid native text row")
                    page, section, string, sentence, include, frequency, text = fields
                    if include == "0":
                        stats["upstream_excluded_native_rows"] += 1
                        continue
                    attribution = db.execute("SELECT revision,url,revision_url FROM pages WHERE id=?",
                                             (page,)).fetchone()
                    if attribution is None:
                        raise ValueError("missing original article attribution")
                    source = {"archive_url": ARCHIVE_URL, "archive_sha256": ARCHIVE_SHA256,
                              "member": name, "member_sha256": checksum, "line": number,
                              "page_id": page, "revision_id": attribution[0],
                              "page_url": attribution[1], "revision_url": attribution[2],
                              "section_index": int(section), "string_index": int(string),
                              "sentence_index": int(sentence), "input_frequency": int(frequency)}
                    keep("native_sentence", split, text, None, source)
            print("processed native split", split, flush=True)
        for split in ["train", "dev", "test"]:
            name = PREFIX + f"lexicons/ur.translit.sampled.{split}.tsv"
            stream, checksum = lines(name, False)
            with stream, db:
                for number, line in enumerate(stream, 1):
                    fields = line.removesuffix("\n").split("\t")
                    if len(fields) != 3 or not fields[2].isdigit() or int(fields[2]) < 1:
                        raise ValueError("invalid lexicon row")
                    text, roman, count = fields
                    source = {"archive_url": ARCHIVE_URL, "archive_sha256": ARCHIVE_SHA256,
                              "member": name, "member_sha256": checksum, "line": number,
                              "page_id": None, "revision_id": None, "page_url": None,
                              "revision_url": None, "section_index": None, "string_index": None,
                              "sentence_index": None, "input_frequency": None}
                    keep("romanization_pair", split, text, roman, source, int(count))
            print("processed lexicon split", split, flush=True)

    shards = []
    split_counts = Counter()
    word_counts = Counter()

    def close_shard(writer, raw, current_path, current_rows, kind, split):
        if writer is None:
            return
        writer.close()
        raw.close()
        size = current_path.stat().st_size
        if size >= 20_000_000:
            raise ValueError("shard exceeds browser-friendly 20 MB limit; use fewer rows")
        shards.append({"path": current_path.relative_to(output).as_posix(),
                       "records": current_rows, "bytes": size,
                       "sha256": sha256(current_path), "kind": kind, "split": split})

    for kind, split in db.execute("SELECT DISTINCT kind,split FROM records ORDER BY kind,split"):
        writer = None
        raw = None
        index = 0
        current_rows = 0
        current_path = None

        query = "SELECT id,text,roman,source,attestations,occurrences FROM records " \
                "WHERE kind=? AND split=? ORDER BY ordinal"
        for key, text, roman, source, attestations, occurrences in db.execute(query, (kind, split)):
            if current_rows == shard_rows or writer is None:
                close_shard(writer, raw, current_path, current_rows, kind, split)
                index += 1
                current_path = data_dir / f"{kind}-{split}-{index:04d}.jsonl.gz"
                raw = current_path.open("xb")
                writer = gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6)
                current_rows = 0
            row = {"id": key, "record_type": kind, "split": split, "text": text,
                   "roman": roman, "attestations": attestations, "source": json.loads(source),
                   "license": "CC-BY-SA-4.0", "review_status": "unreviewed",
                   "duplicate_source_occurrences": occurrences}
            writer.write((json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
            current_rows += 1
            split_counts[kind + "/" + split] += 1
            word_counts[kind] += len(text.split())
        close_shard(writer, raw, current_path, current_rows, kind, split)
    db.close()
    result = {"source": {"url": ARCHIVE_URL, "sha256": ARCHIVE_SHA256,
                         "bytes": archive.stat().st_size, "version": "1.0"},
              "date_accessed": "2026-11-17", "members": member_evidence,
              "source_counts": dict(stats), "exclusion_rule_hits": dict(excluded),
              "retained_by_type_split": dict(split_counts),
              "retained_records": sum(split_counts.values()),
              "whitespace_delimited_tokens_by_type": dict(word_counts),
              "human_reviewed_records": 0, "shards": shards,
              "notes": ["Text copied without local Unicode normalization or translation.",
                        "Exact duplicates removed globally within each record type; first source retained.",
                        "Validation processed before training to retain cross-split duplicates in validation.",
                        "Contact/credential-like pattern filtering is limited triage, not a privacy guarantee.",
                        "Word counts are whitespace-delimited tokens, not model tokens or unique words."]}
    with (output / "manifest.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in ["retained_records", "retained_by_type_split",
                                                  "whitespace_delimited_tokens_by_type"]}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("work_db", type=Path)
    parser.add_argument("--shard-rows", type=int, default=50000)
    args = parser.parse_args()
    run(args.archive, args.output, args.work_db, args.shard_rows)


if __name__ == "__main__":
    main()

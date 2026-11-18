"""Offline, fail-closed ingestion of explicitly cleared Urdu source JSONL."""
import gzip
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ALLOWED = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "CC-BY-SA-4.0",
           "CC-BY-SA-3.0", "ODC-By-1.0"}
ARABIC = re.compile(r"[\u0600-\u06ff]")
LATIN = re.compile(r"[A-Za-z]")
CONTACT = re.compile(r"(?i)(?:[\w.+-]+@[\w.-]+\.[a-z]{2,}|(?:\+?\d[\d\s().-]{8,}\d))")
CATEGORIES = {"news", "books", "wikipedia", "web", "conversation", "roman_urdu",
              "speech_transcript"}
SCRIPTS = {"urdu_arabic", "roman_urdu"}


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def accept(row):
    """Return reason, or None. Script heuristics are triage, not linguistic verification."""
    if not isinstance(row, dict):
        return "invalid_record"
    required = ("text", "category", "script", "license", "source_url", "source_version",
                "rights_evidence_url", "document_id", "revision")
    if any(not isinstance(row.get(k), str) or not row[k].strip() for k in required):
        return "missing_provenance"
    if row["license"] not in ALLOWED:
        return "license_not_allowlisted"
    if row.get("redistribution_cleared") is not True:
        return "rights_not_cleared"
    if row["category"] not in CATEGORIES or row["script"] not in SCRIPTS:
        return "invalid_category_or_script"
    if not all(row[k].startswith("https://") for k in ("source_url", "rights_evidence_url")):
        return "invalid_evidence_url"
    value = row["text"]
    if len(value) < 20 or len(value) > 100000 or "\ufffd" in value or "\x00" in value:
        return "broken_or_out_of_range"
    if any(ord(c) < 32 and c not in "\n\t\r" for c in value):
        return "control_character"
    if CONTACT.search(value):
        return "contact_pattern"
    letters = sum(c.isalpha() for c in value)
    if letters < 8:
        return "insufficient_letters"
    if row["script"] == "urdu_arabic":
        if sum(bool(ARABIC.fullmatch(c)) for c in value) / letters < 0.6:
            return "script_mismatch"
    elif sum(bool(LATIN.fullmatch(c)) for c in value) / letters < 0.6:
        return "script_mismatch"
    return None


def build(source, output, *, max_records_per_shard=50000):
    """Build new local shards atomically at the directory level; never overwrite."""
    source, output = Path(source), Path(output)
    if not source.is_file() or output.exists():
        raise ValueError("source must exist and output must not exist")
    if max_records_per_shard < 1:
        raise ValueError("max_records_per_shard must be positive")
    # A distinct staging directory prevents presenting partial output as published.
    staging = output.with_name(output.name + ".staging")
    if staging.exists():
        raise FileExistsError(staging)
    staging.mkdir(parents=True)
    db = sqlite3.connect(staging / "seen.sqlite")
    db.execute("CREATE TABLE seen (id TEXT PRIMARY KEY)")
    counts, rejected, shards = {}, {}, []
    total = tokens = 0
    handle = None
    shard_count = 0
    try:
        with source.open("r", encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                try:
                    row = json.loads(line)
                except (ValueError, TypeError):
                    rejected["invalid_json"] = rejected.get("invalid_json", 0) + 1
                    continue
                reason = accept(row)
                if reason:
                    rejected[reason] = rejected.get(reason, 0) + 1
                    continue
                # Exact dedup across all categories; no unsubstantiated near-dedup claim.
                identity = digest(row["text"])
                try:
                    db.execute("INSERT INTO seen VALUES (?)", (identity,))
                except sqlite3.IntegrityError:
                    rejected["exact_duplicate"] = rejected.get("exact_duplicate", 0) + 1
                    continue
                if handle is None or shard_count == max_records_per_shard:
                    if handle:
                        handle.close()
                    name = f"part-{len(shards):05d}.jsonl.gz"
                    handle = gzip.open(staging / name, "wt", encoding="utf-8", newline="\n",
                                       compresslevel=6, mtime=None) if False else None
                    # gzip.open has no mtime parameter; use stable records, not a deterministic gzip claim.
                    handle = gzip.open(staging / name, "wt", encoding="utf-8", newline="\n")
                    shards.append({"path": name, "records": 0, "tokens": 0})
                    shard_count = 0
                clean = {k: row[k] for k in ("text", "category", "script", "license",
                          "source_url", "source_version", "rights_evidence_url",
                          "document_id", "revision")}
                clean["id"] = identity
                clean["review_status"] = "unreviewed"
                clean["token_count_whitespace"] = len(row["text"].split())
                handle.write(json.dumps(clean, ensure_ascii=False, sort_keys=True) + "\n")
                shard_count += 1
                total += 1
                tokens += clean["token_count_whitespace"]
                shards[-1]["records"] += 1
                shards[-1]["tokens"] += clean["token_count_whitespace"]
                key = row["category"]
                counts[key] = counts.get(key, 0) + 1
        if handle:
            handle.close()
            handle = None
        db.close()
        db = None
        (staging / "seen.sqlite").unlink()
        for shard in shards:
            data = (staging / shard["path"]).read_bytes()
            shard["sha256"] = hashlib.sha256(data).hexdigest()
            shard["bytes"] = len(data)
        manifest = {"status": "local_unpublished", "record_count": total,
                    "whitespace_delimited_tokens": tokens, "human_verified_records": 0,
                    "categories": counts, "rejected": rejected, "shards": shards,
                    "deduplication": "exact original text SHA-256",
                    "source_file_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        (staging / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staging / "checksums.sha256").write_text(
            "".join(f'{s["sha256"]}  {s["path"]}\n' for s in shards), encoding="utf-8")
        staging.rename(output)
        return manifest
    finally:
        if handle:
            handle.close()
        if db:
            db.close()

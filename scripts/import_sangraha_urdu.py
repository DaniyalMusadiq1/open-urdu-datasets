"""Import the pinned, CC-BY-4.0 Sangraha verified Urdu Parquet shard."""
import argparse
import glob
import gzip
import hashlib
import io
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

# fasttext-wheel releases predating NumPy 2 pass copy=False to np.array; keep
# the safe NumPy 2 equivalent so the pinned ingest can run on current Python.
if int(np.__version__.split(".", maxsplit=1)[0]) >= 2:
    _numpy_array = np.array

    def _numpy2_compat_array(obj, *args, **kwargs):
        if kwargs.get("copy") is False:
            kwargs.pop("copy")
            return np.asarray(obj, *args, **kwargs)
        return _numpy_array(obj, *args, **kwargs)

    np.array = _numpy2_compat_array

import fasttext
import pyarrow.parquet as pq

SOURCE_REPO = "ai4bharat/sangraha"
SOURCE_REVISION = "8b813c3f62d37b2fa174d68c31e8b35ae2fe85e8"
EXPANSION_REVISION = "654c02de6fa4cff1e3ade4e5c9242bedc7ad7629"
SOURCE_PATH = "verified/urd/data-0.parquet"
SOURCE_SHA256 = "0220cd62b7dde5d12fa52c6c40f47f7e06df3e7ccb659576488fd8a83b110d48"
SOURCE_FILES = {
    "verified/urd/data-0.parquet": SOURCE_SHA256,
    "verified/urd/data-1.parquet": "41d73f33b6efc3124cfce6b36f825510ea125fdbbe7761d17911319f1cb08125",
}
for _shard_number in range(2, 27):
    SOURCE_FILES[f"verified/urd/data-{_shard_number}.parquet"] = None
LID_MODEL_SHA256 = "8f3472cfe8738a7b6099e8e999c3cbfae0dcd15696aac7d7738a8039db603e83"
EMAIL = re.compile(r"(?i)[\w.+-]+@[\w.-]+\.[a-z]{2,}")


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def canonical(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def text_hash(text):
    return hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()


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
                            hashes.add(text_hash(value))
    return hashes, records


def write_shard(out, index, batch):
    relative = f"data/docs-{index:04d}.jsonl.gz"
    path = out / relative
    with (path.open("wb") as raw,
          gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped,
          io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as text_stream):
        for row in batch:
            text_stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    payload = path.read_bytes()
    return {"path": relative, "records": len(batch),
            "tokens": sum(row["token_count_whitespace"] for row in batch),
            "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def build(parquet, lid_model, out, existing_root=Path("datasets"),
          shard_records=3000, min_lid_confidence=0.70, classify_chars=5000,
          source_path=SOURCE_PATH, source_revision=SOURCE_REVISION,
          source_sha256=None):
    parquet, lid_model, out = Path(parquet), Path(lid_model), Path(out)
    if out.exists():
        raise FileExistsError(out)
    expected_source_sha = SOURCE_FILES.get(source_path)
    if source_path not in SOURCE_FILES:
        raise ValueError("source file must be a pinned verified/urd shard")
    source_sha = source_sha256 or sha256(parquet)
    if expected_source_sha and source_sha != expected_source_sha:
        raise ValueError("Sangraha Parquet SHA-256 mismatch")
    if sha256(parquet) != source_sha:
        raise ValueError("Sangraha Parquet SHA-256 mismatch")
    if sha256(lid_model) != LID_MODEL_SHA256:
        raise ValueError("fastText model SHA-256 mismatch")
    if shard_records < 1 or not 0 < min_lid_confidence <= 1 or classify_chars < 100:
        raise ValueError("invalid shard, confidence, or classifier window setting")
    existing, existing_records = published_hashes(existing_root)
    model = fasttext.load_model(str(lid_model))
    parquet_file = pq.ParquetFile(parquet)
    out.mkdir(parents=True)
    (out / "data").mkdir()
    counts, rejected, new_seen = Counter(), Counter(), set()
    batch, shards, total_tokens = [], [], 0
    for record in parquet_file.iter_batches(batch_size=1000, columns=["doc_id", "type", "text"]):
        for row in record.to_pylist():
            counts["source_rows_read"] += 1
            text = row.get("text") or ""
            canonical_text = canonical(text)
            if len(canonical_text) < 100 or sum(ch.isalpha() for ch in canonical_text) < 40:
                rejected["short_or_empty"] += 1
                continue
            letters = sum(ch.isalpha() for ch in canonical_text)
            arabic_letters = sum("\u0600" <= ch <= "\u06ff" for ch in canonical_text)
            if arabic_letters / max(1, letters) < 0.55:
                rejected["low_arabic_script_ratio"] += 1
                continue
            if EMAIL.search(canonical_text):
                rejected["email_pattern_triage"] += 1
                continue
            classifier_input = canonical_text[:classify_chars]
            labels, probabilities = model.predict(classifier_input, k=1)
            language = labels[0].removeprefix("__label__")
            confidence = float(probabilities[0])
            if language != "ur" or confidence < min_lid_confidence:
                rejected["language_id_rejected"] += 1
                continue
            counts["urdu_lid_candidates"] += 1
            identity = text_hash(text)
            if identity in existing:
                rejected["duplicate_existing_published_text"] += 1
                continue
            if identity in new_seen:
                rejected["exact_duplicate_source_text"] += 1
                continue
            new_seen.add(identity)
            batch.append({
                "id": identity,
                "text": text,
                "source_dataset": SOURCE_REPO,
                "source_revision": source_revision,
                "source_file": source_path,
                "source_doc_id": str(row.get("doc_id") or ""),
                "source_type": str(row.get("type") or "unknown"),
                "source_url": "https://huggingface.co/datasets/ai4bharat/sangraha",
                "license": "CC-BY-4.0",
                "language_id": "fastText lid.176:ur",
                "language_id_confidence": confidence,
                "review_status": "unreviewed",
                "token_count_whitespace": len(text.split()),
            })
            if len(batch) >= shard_records:
                shard = write_shard(out, len(shards) + 1, batch)
                shards.append(shard)
                total_tokens += shard["tokens"]
                batch.clear()
        if counts["source_rows_read"] % 10000 == 0:
            print(json.dumps({"source_rows_read": counts["source_rows_read"],
                              "urdu_candidates": counts["urdu_lid_candidates"],
                              "records_written": len(new_seen),
                              "whitespace_tokens_written": total_tokens}), flush=True)
    if batch:
        shard = write_shard(out, len(shards) + 1, batch)
        shards.append(shard)
        total_tokens += shard["tokens"]
    manifest = {
        "status": "local_unpublished",
        "source": {"repository": SOURCE_REPO,
                   "url": "https://huggingface.co/datasets/ai4bharat/sangraha",
                   "revision": source_revision, "file": source_path,
                   "file_sha256": source_sha, "declared_license": "CC-BY-4.0"},
        "record_count": len(new_seen),
        "whitespace_delimited_tokens": total_tokens,
        "human_verified_records": 0,
        "review_status": "unreviewed",
        "counts": dict(counts),
        "rejected": dict(rejected),
        "existing_published_records_scanned": existing_records,
        "existing_published_text_field_hashes_scanned": len(existing),
        "deduplication": "Exact SHA-256 of NFC-normalized text after whitespace collapse; exact matches only",
        "language_filter": {"model": "fastText supervised lid.176", "model_sha256": LID_MODEL_SHA256,
                            "accepted_label": "ur", "minimum_confidence": min_lid_confidence,
                            "classified_prefix_characters": classify_chars,
                            "arabic_script_ratio_minimum": 0.55,
                            "note": "Automated routing only; not human/native-speaker verification"},
        "attribution": "AI4Bharat Sangraha; preserve license, source dataset URL, pinned revision, source file, document ID and type",
        "limitations": "The upstream rows provide document IDs and type labels, but not original page URLs or creator names; all retained text remains unreviewed.",
        "shards": shards,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (out / "checksums.sha256").write_text(
        "".join(f'{item["sha256"]}  {item["path"]}\n' for item in shards), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("parquet")
    parser.add_argument("lid_model")
    parser.add_argument("out")
    parser.add_argument("--existing-root", default="datasets")
    parser.add_argument("--shard-records", type=int, default=3000)
    parser.add_argument("--min-lid-confidence", type=float, default=0.70)
    parser.add_argument("--source-path", choices=sorted(SOURCE_FILES), default=SOURCE_PATH)
    parser.add_argument("--source-revision", default=SOURCE_REVISION)
    parser.add_argument("--source-sha256")
    args = parser.parse_args()
    print(json.dumps(build(args.parquet, args.lid_model, args.out,
                           Path(args.existing_root), args.shard_records,
                           args.min_lid_confidence, source_path=args.source_path,
                           source_revision=args.source_revision,
                           source_sha256=args.source_sha256), indent=2))


if __name__ == "__main__":
    main()

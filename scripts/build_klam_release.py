"""Build the single, normalized Klam release from approved hosted corpora."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARD_RECORDS = 50_000
LICENSE_URLS = {
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}
SOURCES = {
    "urdu-wikipedia": {
        "root": "urwiki-articles",
        "display": "Urdu Wikipedia contributors",
        "license": "CC-BY-SA-4.0",
        "source_url": "https://dumps.wikimedia.org/urwiki/",
    },
    "sangraha-urdu": {
        "root": "sangraha-verified-urdu",
        "display": "AI4Bharat Sangraha",
        "license": "CC-BY-4.0",
        "source_url": "https://huggingface.co/datasets/ai4bharat/sangraha",
    },
    "dakshina-urdu": {
        "root": "datasets/corpora/dakshina-urdu-bulk",
        "display": "Google Research Dakshina",
        "license": "CC-BY-SA-4.0",
        "source_url": "https://github.com/google-research-datasets/dakshina",
    },
    "roman-urdu-sentiment": {
        "root": "datasets/classification/uci-roman-urdu-sentiment",
        "display": "UCI Roman Urdu datasets",
        "license": "CC-BY-4.0",
        "source_url": "https://archive.ics.uci.edu/",
    },
    "urdu-wikisource": {
        "root": "datasets/corpora/urwikisource-pd-old",
        "display": "Urdu Wikisource contributors",
        "license": "CC-BY-SA-4.0",
        "source_url": "https://ur.wikisource.org/",
    },
}


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def stable_source_id(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_roots(release_root):
    roots = [
        ("urdu-wikipedia", release_root / "urwiki-articles"),
        ("sangraha-urdu", release_root / "sangraha-verified-urdu"),
    ]
    roots.extend(("sangraha-urdu", path) for path in sorted(
        release_root.glob("sangraha-verified-urdu-data-*")))
    roots.extend([
        ("dakshina-urdu", ROOT / SOURCES["dakshina-urdu"]["root"]),
        ("roman-urdu-sentiment", ROOT / SOURCES["roman-urdu-sentiment"]["root"]),
        ("urdu-wikisource", ROOT / SOURCES["urdu-wikisource"]["root"]),
    ])
    return roots


def record_attribution(source_key, row, profile):
    urls = []
    if profile.get("source_url"):
        urls.append(profile["source_url"])
    for key in ("revision_url", "source_url", "page_url", "history_url"):
        value = row.get(key)
        if isinstance(value, str) and value.startswith("https://"):
            urls.append(value)
    nested = row.get("source")
    if isinstance(nested, dict):
        for key in ("revision_url", "page_url", "archive_url"):
            value = nested.get(key)
            if isinstance(value, str) and value.startswith("https://"):
                urls.append(value)
    doi = row.get("source_doi")
    if isinstance(doi, str) and doi:
        urls.append("https://doi.org/" + doi)
    link = next(iter(dict.fromkeys(urls)), "")
    return profile["display"] + " — " + row["license"] + ((" — " + link) if link else "")


def normalized_record(source_key, version, row, profile):
    if not isinstance(row, dict) or not isinstance(row.get("text"), str) or not row["text"]:
        raise ValueError(f"{source_key}: every record must contain nonempty text")
    license_name = row.get("license")
    if license_name != profile["license"] or license_name not in LICENSE_URLS:
        raise ValueError(f"{source_key}: unexpected or missing record license")
    review_status = row.get("review_status")
    if review_status not in {"unreviewed", "verified", "human_reviewed"}:
        raise ValueError(f"{source_key}: missing review status")
    original_id = str(row.get("id", ""))
    if not original_id:
        raise ValueError(f"{source_key}: record ID is missing")
    if "sentiment" in row:
        task, label = "sentiment_classification", str(row["sentiment"])
    elif row.get("record_type") == "romanization_pair":
        task, label = "romanization", ""
    else:
        task, label = "text", ""
    roman = row.get("roman")
    split = row.get("split")
    metadata = {key: value for key, value in row.items() if key not in {"text"}}
    return {
        "id": stable_source_id(source_key + "\0" + original_id),
        "text": row["text"],
        "language": "ur",
        "script": "Latin" if source_key == "roman-urdu-sentiment" else "Arabic",
        "task": task,
        "label": label,
        "roman": roman if isinstance(roman, str) else "",
        "split": split if isinstance(split, str) else "",
        "source": source_key,
        "source_version": version,
        "license": license_name,
        "license_url": LICENSE_URLS[license_name],
        "review_status": review_status,
        "attribution": record_attribution(source_key, row, profile),
        "word_count": str(len(row["text"].split())),
        "metadata_json": json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
    }


def write_shard(output, index, rows):
    relative = f"data/klam-{index:05d}.jsonl.gz"
    path = output / relative
    with (path.open("wb") as raw,
          gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped,
          io.TextIOWrapper(zipped, encoding="utf-8", newline="\n") as stream):
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    payload = path.read_bytes()
    return {
        "path": relative,
        "records": len(rows),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def build(output, release_root):
    output, release_root = Path(output), Path(release_root)
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    (output / "data").mkdir()
    sources = []
    shards = []
    batch = []
    total_records = total_words = human_reviewed = 0
    seen_ids = set()
    for source_key, root in source_roots(release_root):
        profile = SOURCES[source_key]
        manifest_path = root / "manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"{source_key}: missing {manifest_path}")
        manifest_bytes = manifest_path.read_bytes()
        source_manifest = json.loads(manifest_bytes)
        version = hashlib.sha256(manifest_bytes).hexdigest()[:16]
        manifest_count = source_manifest.get("record_count", source_manifest.get("retained_records"))
        source_record_count = source_manifest.get("record_count", source_manifest.get("retained_records"))
        files = sorted((root / "data").glob("*.jsonl")) + sorted((root / "data").glob("*.jsonl.gz"))
        if not files:
            raise ValueError(f"{source_key}: no published JSONL records found in {root / 'data'}")
        source_rows = 0
        for path in files:
            opener = gzip.open if path.suffix == ".gz" else open
            with opener(path, "rt", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    row = json.loads(line)
                    record = normalized_record(source_key, version, row, profile)
                    if record["id"] in seen_ids:
                        raise ValueError(f"duplicate Klam ID in {source_key}: {record['id']}")
                    seen_ids.add(record["id"])
                    source_rows += 1
                    total_records += 1
                    total_words += int(record["word_count"])
                    human_reviewed += record["review_status"] == "human_reviewed"
                    batch.append(record)
                    if len(batch) >= SHARD_RECORDS:
                        shards.append(write_shard(output, len(shards) + 1, batch))
                        batch = []
        if source_record_count is not None and source_rows != source_record_count:
            raise ValueError(
                f"{source_key}: manifest says {source_record_count} rows, read {source_rows}"
            )
        sources.append({
            "id": source_key,
            "name": profile["display"],
            "license": profile["license"],
            "license_url": LICENSE_URLS[profile["license"]],
            "release_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "release_manifest": source_manifest,
            "records": source_rows,
        })
    if batch:
        shards.append(write_shard(output, len(shards) + 1, batch))
    (output / "sources.json").write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksums = []
    for shard in shards:
        checksums.append(f'{shard["sha256"]}  {shard["path"]}')
    sources_sha = digest(output / "sources.json")
    checksums.append(f"{sources_sha}  sources.json")
    (output / "checksums.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    manifest = {
        "dataset": "Klam (کلام)",
        "schema_version": "1.0",
        "format": "JSONL.GZ",
        "record_count": total_records,
        "whitespace_delimited_tokens": total_words,
        "human_verified_records": human_reviewed,
        "review_status": "unreviewed" if human_reviewed == 0 else "mixed",
        "license": "mixed; see per-record license and sources.json",
        "sources": sources,
        "shards": shards,
        "checksums_sha256": "checksums.sha256",
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "LICENSE").write_text(
        "# Klam data licenses\n\n"
        "Klam combines records under different source licenses. There is no single "
        "license for all text. Each record contains its applicable `license`, "
        "`license_url`, and `attribution`; sources.json provides source-level "
        "details. Follow the terms for the records you use.\n",
        encoding="utf-8")
    (output / "SOURCES.md").write_text(
        "# Klam sources\n\n"
        "Every record identifies its source, source release, license, and review status. "
        "The exact source release manifests are summarized in sources.json. "
        "All text remains unreviewed unless the record explicitly says otherwise.\n",
        encoding="utf-8")
    (output / "DATASET_CARD.md").write_text(
        "# Klam (کلام)\n\n"
        f"Klam contains {total_records:,} records in one simple schema. It combines "
        "eligible Urdu and Roman Urdu text, including text and sentiment records. "
        "Records preserve source, source version, license, attribution, and review status.\n\n"
        "**Native-speaker verified records: 0.** All current records are unreviewed. "
        "Automated checks do not confirm linguistic correctness, safety, or privacy.\n\n"
        "Licenses differ by source; there is no single license for the entire collection. "
        "See the per-record license fields and sources.json.\n",
        encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--release-root", default="artifacts/phase2-release")
    args = parser.parse_args()
    print(json.dumps(build(args.output, args.release_root), ensure_ascii=False))


if __name__ == "__main__":
    main()

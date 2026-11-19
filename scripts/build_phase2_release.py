"""Rebuild pinned Phase 2 corpora in CI before publication to Hugging Face."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = "8b813c3f62d37b2fa174d68c31e8b35ae2fe85e8"
EXPANSION_REVISION = "654c02de6fa4cff1e3ade4e5c9242bedc7ad7629"
SOURCES = [
    ("https://dumps.wikimedia.org/urwiki/20261101/urwiki-20261101-pages-articles.xml.bz2",
     "5cf02a04981c9efe8698ad880b09ca74e6404513a3c7cdb4eea9291ab8e52d0d",
     "urwiki-20261101-pages-articles.xml.bz2"),
    ("https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar",
     "83530bec211893d9df429298f42e63c350c25ad56f9f5172f85edb0575ee5b03",
     "dakshina_dataset_v1.0.tar"),
    (f"https://huggingface.co/datasets/ai4bharat/sangraha/resolve/{REVISION}/verified/urd/data-0.parquet?download=true",
     "0220cd62b7dde5d12fa52c6c40f47f7e06df3e7ccb659576488fd8a83b110d48",
     "sangraha-urd-data-0.parquet"),
    (f"https://huggingface.co/datasets/ai4bharat/sangraha/resolve/{REVISION}/verified/urd/data-1.parquet?download=true",
     "41d73f33b6efc3124cfce6b36f825510ea125fdbbe7761d17911319f1cb08125",
     "sangraha-urd-data-1.parquet"),
    ("https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz",
     "8f3472cfe8738a7b6099e8e999c3cbfae0dcd15696aac7d7738a8039db603e83",
     "lid.176.ftz"),
]
for _shard_number in range(2, 27):
    SOURCES.append((
        f"https://huggingface.co/datasets/ai4bharat/sangraha/resolve/{EXPANSION_REVISION}/verified/urd/data-{_shard_number}.parquet?download=true",
        None, f"sangraha-urd-data-{_shard_number}.parquet"))


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(url, destination, expected=None):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and expected is not None and sha256(destination) == expected:
        return destination
    request = urllib.request.Request(url, headers={"User-Agent": "open-urdu-datasets/phase2"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out, length=1024 * 1024)
    if expected is not None and sha256(destination) != expected:
        destination.unlink(missing_ok=True)
        raise ValueError(f"source SHA-256 mismatch: {destination.name}")
    return destination


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, check=True)


def index_existing_jsonl(source_roots, destination):
    destination.mkdir(parents=True, exist_ok=True)
    index = 0
    for source_root in source_roots:
        for path in sorted(source_root.rglob("*.jsonl*")):
            index += 1
            target = destination / f"{index:06d}-{path.name}"
            try:
                os.link(path, target)
            except OSError:
                shutil.copy2(path, target)


def index_release(root, destination):
    for path in sorted(root.rglob("*.jsonl*")):
        target = destination / f"{root.name}-{path.name}"
        try:
            os.link(path, target)
        except OSError:
            shutil.copy2(path, target)


def add_release_docs(root, source_dir):
    for filename in ("DATASET_CARD.md", "SOURCES.md", "LICENSE"):
        shutil.copy2(source_dir / filename, root / filename)


def add_dakshina_docs(root, source_dir):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    shutil.copy2(source_dir / "LICENSE", root / "LICENSE")
    retained = manifest["retained_records"]
    buckets = manifest["retained_by_type_split"]
    (root / "DATASET_CARD.md").write_text(
        "# Dakshina Urdu source release\n\n"
        f"This pinned full-source build contains {retained:,} retained records "
        f"across {len(buckets)} record-type/split buckets. It includes native Urdu "
        "sentences and Urdu-to-Roman-Urdu transliteration pairs. Records remain "
        "unreviewed by Klam native speakers.\n\n"
        "Counts are produced by the importer and are not unique counts across all "
        "Klam sources. Roman pair sides are preserved as linked fields in Klam.\n",
        encoding="utf-8",
    )
    members = "\n".join(
        f"- {item['member']} — {item['bytes']:,} bytes, SHA-256 {item['sha256']}"
        for item in manifest["members"]
    )
    (root / "SOURCES.md").write_text(
        "# Dakshina source and rights\n\n"
        "- Source: https://github.com/google-research-datasets/dakshina\n"
        "- Version: Dakshina v1.0\n"
        "- Archive: https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar\n"
        "- Archive SHA-256: 83530bec211893d9df429298f42e63c350c25ad56f9f5172f85edb0575ee5b03\n"
        "- License: CC BY-SA 4.0; see the copied source license and row metadata.\n"
        "- Klam native-speaker verified records: 0.\n\n"
        "## Processed source members\n\n" + members + "\n",
        encoding="utf-8",
    )


def main():
    artifact_root = Path(os.environ.get("PHASE2_RELEASE_ROOT", "artifacts/phase2-release"))
    if not artifact_root.is_absolute():
        artifact_root = ROOT / artifact_root
    if artifact_root.exists():
        raise FileExistsError(artifact_root)
    artifact_root.mkdir(parents=True)
    intake = artifact_root / "source-files"
    source_specs = {name: (url, digest) for url, digest, name in SOURCES}
    index = artifact_root / "dedup-index"
    index_existing_jsonl([ROOT / "datasets"], index)

    dakshina = artifact_root / "dakshina-urdu-bulk"
    dakshina_url, dakshina_sha = source_specs["dakshina_dataset_v1.0.tar"]
    dakshina_archive = download(
        dakshina_url, intake / "dakshina_dataset_v1.0.tar", dakshina_sha)
    run("scripts/import_dakshina_bulk.py", dakshina_archive, dakshina,
        artifact_root / "dakshina-work.sqlite")
    add_dakshina_docs(dakshina, ROOT / "datasets/corpora/dakshina-urdu-bulk")
    run("scripts/validate_bulk.py", dakshina)
    index_release(dakshina, index)
    dakshina_archive.unlink()

    wiki = artifact_root / "urwiki-articles"
    wiki_url, wiki_sha = source_specs["urwiki-20261101-pages-articles.xml.bz2"]
    wiki_dump = download(wiki_url, intake / "urwiki-20261101-pages-articles.xml.bz2", wiki_sha)
    run("scripts/import_urwiki_articles.py", wiki_dump,
        wiki, "--existing-root", index)
    add_release_docs(wiki, ROOT / "datasets/corpora/urwiki-articles")
    run("scripts/validate_urwiki_articles.py", wiki)
    index_release(wiki, index)
    wiki_dump.unlink()

    sangraha0 = artifact_root / "sangraha-verified-urdu"
    fasttext_url, fasttext_sha = source_specs["lid.176.ftz"]
    fasttext = download(fasttext_url, intake / "lid.176.ftz", fasttext_sha)
    data0_url, data0_sha = source_specs["sangraha-urd-data-0.parquet"]
    data0 = download(data0_url, intake / "sangraha-urd-data-0.parquet", data0_sha)
    run("scripts/import_sangraha_urdu.py", data0, fasttext, sangraha0, "--existing-root", index)
    add_release_docs(sangraha0, ROOT / "datasets/corpora/sangraha-verified-urdu")
    run("scripts/validate_sangraha_urdu.py", sangraha0)
    index_release(sangraha0, index)
    data0.unlink()

    sangraha1 = artifact_root / "sangraha-verified-urdu-data-1"
    data1_url, data1_sha = source_specs["sangraha-urd-data-1.parquet"]
    data1 = download(data1_url, intake / "sangraha-urd-data-1.parquet", data1_sha)
    run("scripts/import_sangraha_urdu.py", data1, fasttext, sangraha1, "--existing-root", index,
        "--source-path", "verified/urd/data-1.parquet")
    add_release_docs(sangraha1, ROOT / "datasets/corpora/sangraha-verified-urdu-data-1")
    run("scripts/validate_sangraha_urdu.py", sangraha1)
    index_release(sangraha1, index)
    data1.unlink()

    sangraha_expansions = []
    for shard_number in range(2, 27):
        source_path = f"verified/urd/data-{shard_number}.parquet"
        corpus_name = f"sangraha-verified-urdu-data-{shard_number}"
        corpus_root = artifact_root / corpus_name
        source_name = f"sangraha-urd-data-{shard_number}.parquet"
        source_url, source_sha = source_specs[source_name]
        source_file = download(source_url, intake / source_name, source_sha)
        run("scripts/import_sangraha_urdu.py",
            source_file, fasttext, corpus_root, "--existing-root", index,
            "--source-path", source_path, "--source-revision", EXPANSION_REVISION)
        add_release_docs(corpus_root, ROOT / "datasets/corpora/sangraha-verified-urdu-data-1")
        manifest = json.loads((corpus_root / "manifest.json").read_text(encoding="utf-8"))
        card = (
            "# AI4Bharat Sangraha verified Urdu shard " + str(shard_number) + "\n\n"
            + "This release contains **" + format(manifest["record_count"], ",")
            + " records and " + format(manifest["whitespace_delimited_tokens"], ",")
            + " whitespace-delimited tokens** from `" + source_path + "` at pinned revision `"
            + EXPANSION_REVISION + "`. These are whitespace counts, not model-token counts.\n\n"
            + "The upstream dataset card declares CC BY 4.0. Rows preserve source document ID, type, revision and file; original page URLs and creator names are unavailable in the source rows. Exact duplicate text was removed after NFC normalization and whitespace collapse against previously retained records. Semantic duplicates may remain. Automated Urdu language identification is not human verification. All records remain `review_status: unreviewed`; native Urdu review is pending.\n"
        )
        (corpus_root / "DATASET_CARD.md").write_text(card, encoding="utf-8")
        sources = ("# Source and license\n\n"
                   + "- Source dataset: https://huggingface.co/datasets/ai4bharat/sangraha\n"
                   + f"- Immutable source revision: {EXPANSION_REVISION}\n"
                   + f"- Source file: {source_path}\n"
                   + f"- Source file SHA-256: {manifest['source']['file_sha256']}\n"
                   + "- License declared on the upstream dataset card: CC BY 4.0\n"
                   + "- Original page URLs and creator names are absent from upstream rows.\n")
        (corpus_root / "SOURCES.md").write_text(sources, encoding="utf-8")
        run("scripts/validate_sangraha_urdu.py", corpus_root)
        index_release(corpus_root, index)
        sangraha_expansions.append(corpus_root)
        source_file.unlink()

    all_corpora = [wiki, sangraha0, sangraha1, *sangraha_expansions]
    run("scripts/audit_new_corpus_duplicates.py", "--existing-root", ROOT / "datasets",
        "--corpora", *all_corpora)
    dakshina_manifest = json.loads(
        (dakshina / "manifest.json").read_text(encoding="utf-8"))
    summary = {
        "corpora": [{
            "id": "dakshina-urdu-bulk",
            "records": dakshina_manifest["retained_records"],
            "whitespace_delimited_tokens": sum(
                dakshina_manifest["whitespace_delimited_tokens_by_type"].values()),
            "retained_by_type_split": dakshina_manifest["retained_by_type_split"],
        }] + [
            {"id": name, "records": json.loads(
                (artifact_root / name / "manifest.json").read_text())["record_count"],
                "whitespace_delimited_tokens": json.loads(
                    (artifact_root / name / "manifest.json").read_text())["whitespace_delimited_tokens"]}
            for name in ("urwiki-articles", "sangraha-verified-urdu",
                         "sangraha-verified-urdu-data-1",
                         *(f"sangraha-verified-urdu-data-{i}" for i in range(2, 27)))
        ]
    }
    (artifact_root / "release-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    fasttext.unlink(missing_ok=True)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()


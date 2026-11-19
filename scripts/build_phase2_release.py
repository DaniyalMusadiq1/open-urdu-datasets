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


def main():
    artifact_root = Path(os.environ.get("PHASE2_RELEASE_ROOT", "artifacts/phase2-release"))
    if not artifact_root.is_absolute():
        artifact_root = ROOT / artifact_root
    if artifact_root.exists():
        raise FileExistsError(artifact_root)
    artifact_root.mkdir(parents=True)
    intake = artifact_root / "source-files"
    downloaded = {name: download(url, intake / name, digest) for url, digest, name in SOURCES}
    index = artifact_root / "dedup-index"
    index_existing_jsonl([ROOT / "datasets"], index)

    wiki = artifact_root / "urwiki-articles"
    run("scripts/import_urwiki_articles.py", downloaded["urwiki-20261101-pages-articles.xml.bz2"],
        wiki, "--existing-root", index)
    add_release_docs(wiki, ROOT / "datasets/corpora/urwiki-articles")
    run("scripts/validate_urwiki_articles.py", wiki)
    index_release(wiki, index)

    sangraha0 = artifact_root / "sangraha-verified-urdu"
    run("scripts/import_sangraha_urdu.py", downloaded["sangraha-urd-data-0.parquet"],
        downloaded["lid.176.ftz"], sangraha0, "--existing-root", index)
    add_release_docs(sangraha0, ROOT / "datasets/corpora/sangraha-verified-urdu")
    run("scripts/validate_sangraha_urdu.py", sangraha0)
    index_release(sangraha0, index)

    sangraha1 = artifact_root / "sangraha-verified-urdu-data-1"
    run("scripts/import_sangraha_urdu.py", downloaded["sangraha-urd-data-1.parquet"],
        downloaded["lid.176.ftz"], sangraha1, "--existing-root", index,
        "--source-path", "verified/urd/data-1.parquet")
    add_release_docs(sangraha1, ROOT / "datasets/corpora/sangraha-verified-urdu-data-1")
    run("scripts/validate_sangraha_urdu.py", sangraha1)
    index_release(sangraha1, index)

    sangraha_expansions = []
    for shard_number in range(2, 27):
        source_path = f"verified/urd/data-{shard_number}.parquet"
        corpus_name = f"sangraha-verified-urdu-data-{shard_number}"
        corpus_root = artifact_root / corpus_name
        run("scripts/import_sangraha_urdu.py",
            downloaded[f"sangraha-urd-data-{shard_number}.parquet"],
            downloaded["lid.176.ftz"], corpus_root, "--existing-root", index,
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

    all_corpora = [wiki, sangraha0, sangraha1, *sangraha_expansions]
    run("scripts/audit_new_corpus_duplicates.py", "--existing-root", ROOT / "datasets",
        "--corpora", *all_corpora)
    summary = {
        "corpora": [
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
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

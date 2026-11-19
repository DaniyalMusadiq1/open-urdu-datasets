"""Sync validated GitHub metadata to HF; never claim unhosted shards are published."""
import argparse
import hashlib
import json
import os
from pathlib import Path

FILES = (
    "README.md",
    "docs/PHASE2.md",
    "datasets/PHASE2_DATASET_CARD.md",
    "catalog/datasets.json",
    "catalog/datasets.csv",
    "catalog/processed-corpora.json",
    "datasets/corpora/dakshina-urdu-bulk/manifest.json",
    "datasets/HUGGINGFACE_README.md",
    "docs/DATA_ARCHITECTURE.md",
    "docs/LICENSE_POLICY.md",
)
PREFIX = "github-sync"
BULK_ROOT = Path("datasets/corpora/dakshina-urdu-bulk")
BULK_REMOTE = "corpora/dakshina-urdu-bulk"
UCI_ROOT = Path("datasets/classification/uci-roman-urdu-sentiment")
UCI_REMOTE = "classification/uci-roman-urdu-sentiment"
WIKISOURCE_ROOT = Path("datasets/corpora/urwikisource-pd-old")
WIKISOURCE_REMOTE = "corpora/urwikisource-pd-old"
RELEASE_ROOT = Path(os.environ.get("PHASE2_RELEASE_ROOT", "datasets/corpora"))
URWIKI_ROOT = RELEASE_ROOT / "urwiki-articles"
URWIKI_REMOTE = "corpora/urwiki-articles"
SANGRAHA_ROOT = RELEASE_ROOT / "sangraha-verified-urdu"
SANGRAHA_REMOTE = "corpora/sangraha-verified-urdu"
SANGRAHA1_ROOT = RELEASE_ROOT / "sangraha-verified-urdu-data-1"
SANGRAHA1_REMOTE = "corpora/sangraha-verified-urdu-data-1"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true",
                        help="mirror updated catalog/docs after a corpus release")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO_ID", "Daniyal643/open-urdu-datasets")
    sha = os.environ.get("GITHUB_SHA")
    if not token or not sha or len(sha) != 40:
        raise SystemExit("HF_TOKEN and a full GITHUB_SHA are required")
    from huggingface_hub import CommitOperationAdd, HfApi

    operations = []
    entries = []
    for filename in FILES:
        path = Path(filename)
        data = path.read_bytes()
        entries.append({"path": filename, "sha256": hashlib.sha256(data).hexdigest(),
                        "bytes": len(data)})
        operations.append(CommitOperationAdd(
            path_in_repo=f"{PREFIX}/{filename}", path_or_fileobj=data))
        if filename == "datasets/HUGGINGFACE_README.md":
            # Publish the repository's actual dataset card at the Hub root.
            operations.append(CommitOperationAdd(
                path_in_repo="README.md", path_or_fileobj=data))
    manifest = {"source_repository": "DaniyalMusadiq1/open-urdu-datasets",
                "github_commit": sha, "files": entries,
                "scope": "metadata_and_validated_corpora"}
    bulk_manifest = json.loads((BULK_ROOT / "manifest.json").read_text(encoding="utf-8"))
    bulk_files = ["DATASET_CARD.md", "SOURCES.md", "LICENSE", "manifest.json",
                  "checksums.sha256"] + [item["path"] for item in bulk_manifest["shards"]]
    for filename in bulk_files:
        local = BULK_ROOT / filename
        payload = local.read_bytes()
        for item in bulk_manifest["shards"]:
            if (item["path"] == filename
                    and hashlib.sha256(payload).hexdigest() != item["sha256"]):
                raise RuntimeError("Local corpus hash mismatch: " + filename)
        operations.append(CommitOperationAdd(
            path_in_repo=f"{BULK_REMOTE}/{filename}", path_or_fileobj=payload))
    uci_files = ["DATASET_CARD.md", "SOURCES.md", "LICENSE", "manifest.json",
                 "checksums.sha256"]
    uci_manifest = json.loads((UCI_ROOT / "manifest.json").read_text(encoding="utf-8"))
    uci_files.extend(item["path"] for item in uci_manifest["shards"])
    for filename in uci_files:
        local = UCI_ROOT / filename
        if not local.is_file():
            raise RuntimeError("Missing UCI release file: " + filename)
        payload = local.read_bytes()
        operations.append(CommitOperationAdd(
            path_in_repo=f"{UCI_REMOTE}/{filename}", path_or_fileobj=payload))
    wikisource_manifest = json.loads(
        (WIKISOURCE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    wikisource_files = ["DATASET_CARD.md", "SOURCES.md", "LICENSE", "manifest.json",
                        "checksums.sha256"] + [item["path"] for item in wikisource_manifest["shards"]]
    for filename in wikisource_files:
        local = WIKISOURCE_ROOT / filename
        if not local.is_file():
            raise RuntimeError("Missing Wikisource release file: " + filename)
        payload = local.read_bytes()
        for item in wikisource_manifest["shards"]:
            if (item["path"] == filename
                    and hashlib.sha256(payload).hexdigest() != item["sha256"]):
                raise RuntimeError("Local Wikisource shard hash mismatch: " + filename)
        operations.append(CommitOperationAdd(
            path_in_repo=f"{WIKISOURCE_REMOTE}/{filename}", path_or_fileobj=payload))
    new_releases = []
    metadata_release_docs = []
    if args.metadata_only:
        metadata_roots = [Path("datasets/corpora/urwiki-articles"),
                          Path("datasets/corpora/sangraha-verified-urdu")]
        metadata_roots.extend(sorted(Path("datasets/corpora").glob("sangraha-verified-urdu-data-*")))
        for root in metadata_roots:
            for filename in ("DATASET_CARD.md", "SOURCES.md", "LICENSE"):
                local = root / filename
                if local.is_file():
                    payload = local.read_bytes()
                    operations.append(CommitOperationAdd(
                        path_in_repo=f"corpora/{root.name}/{filename}", path_or_fileobj=payload))
                    metadata_release_docs.append((root, filename))
    release_specs = [] if args.metadata_only else [
        (URWIKI_ROOT, URWIKI_REMOTE),
        (SANGRAHA_ROOT, SANGRAHA_REMOTE),
        (SANGRAHA1_ROOT, SANGRAHA1_REMOTE),
        *((path, f"corpora/{path.name}") for path in sorted(
            RELEASE_ROOT.glob("sangraha-verified-urdu-data-[2-7]"))),
    ]
    for root, remote in release_specs:
        release_manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        release_manifest["status"] = "published"
        release_manifest["published_from_github_commit"] = sha
        (root / "manifest.json").write_text(
            json.dumps(release_manifest, indent=2) + "\n", encoding="utf-8")
        release_files = ["DATASET_CARD.md", "SOURCES.md", "LICENSE", "manifest.json",
                         "checksums.sha256"] + [item["path"] for item in release_manifest["shards"]]
        for filename in release_files:
            local = root / filename
            if not local.is_file():
                raise RuntimeError("Missing corpus release file: " + str(local))
            payload = local.read_bytes()
            shard = next((item for item in release_manifest["shards"]
                          if item["path"] == filename), None)
            if shard and hashlib.sha256(payload).hexdigest() != shard["sha256"]:
                raise RuntimeError("Local corpus hash mismatch: " + filename)
            operations.append(CommitOperationAdd(
                path_in_repo=f"{remote}/{filename}", path_or_fileobj=payload))
        new_releases.append({"root": root, "remote": remote,
                             "files": release_files, "manifest": release_manifest})
    manifest["corpora"] = [
        {"path": str(item["root"]), "records": item["manifest"]["record_count"],
         "whitespace_delimited_tokens": item["manifest"]["whitespace_delimited_tokens"],
         "files": item["files"]} for item in new_releases]
    operations.append(CommitOperationAdd(
        path_in_repo=f"{PREFIX}/sync-manifest.json",
        path_or_fileobj=(json.dumps(manifest, indent=2) + "\n").encode("utf-8")))
    api = HfApi(token=token)
    api.repo_info(repo_id=repo_id, repo_type="dataset")
    result = api.create_commit(repo_id=repo_id, repo_type="dataset",
                               operations=operations,
                               commit_message=f"Sync GitHub metadata {sha[:12]}")
    # Verify the remote manifest content, not just the API success response.
    from huggingface_hub import hf_hub_download
    remote_path = hf_hub_download(repo_id=repo_id, repo_type="dataset",
                                  filename=f"{PREFIX}/sync-manifest.json",
                                  revision=result.oid, token=token)
    remote = json.loads(Path(remote_path).read_text(encoding="utf-8"))
    if remote != manifest:
        raise RuntimeError("remote sync manifest does not match the uploaded content")
    for entry in entries:
        remote_file = hf_hub_download(
            repo_id=repo_id, repo_type="dataset",
            filename=f"{PREFIX}/{entry['path']}",
            revision=result.oid, token=token)
        with Path(remote_file).open("rb") as stream:
            remote_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        if remote_hash != entry["sha256"]:
            raise RuntimeError("Remote metadata hash mismatch: " + entry["path"])
    hf_readme_path = hf_hub_download(
        repo_id=repo_id, repo_type="dataset", filename="README.md",
        revision=result.oid, token=token)
    with Path("datasets/HUGGINGFACE_README.md").open("rb") as stream:
        local_hf_readme_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    with Path(hf_readme_path).open("rb") as stream:
        remote_hf_readme_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    if local_hf_readme_hash != remote_hf_readme_hash:
        raise RuntimeError("Hugging Face root dataset card hash mismatch")
    for item in bulk_manifest["shards"]:
        remote_file = hf_hub_download(
            repo_id=repo_id, repo_type="dataset",
            filename=f'{BULK_REMOTE}/{item["path"]}',
            revision=result.oid, token=token)
        with Path(remote_file).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != item["sha256"]:
            raise RuntimeError("Remote corpus hash mismatch: " + item["path"])
    for filename in uci_files:
        remote_file = hf_hub_download(
            repo_id=repo_id, repo_type="dataset", filename=f"{UCI_REMOTE}/{filename}",
            revision=result.oid, token=token)
        with (UCI_ROOT / filename).open("rb") as stream:
            local_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        with Path(remote_file).open("rb") as stream:
            remote_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        if local_hash != remote_hash:
            raise RuntimeError("Remote UCI file hash mismatch: " + filename)
    for filename in wikisource_files:
        remote_file = hf_hub_download(
            repo_id=repo_id, repo_type="dataset",
            filename=f"{WIKISOURCE_REMOTE}/{filename}", revision=result.oid, token=token)
        with (WIKISOURCE_ROOT / filename).open("rb") as stream:
            local_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        with Path(remote_file).open("rb") as stream:
            remote_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        if local_hash != remote_hash:
            raise RuntimeError("Remote Wikisource file hash mismatch: " + filename)
    for release in new_releases:
        for filename in release["files"]:
            local = release["root"] / filename
            remote_file = hf_hub_download(
                repo_id=repo_id, repo_type="dataset",
                filename=f'{release["remote"]}/{filename}', revision=result.oid, token=token)
            with local.open("rb") as stream:
                local_hash = hashlib.file_digest(stream, "sha256").hexdigest()
            with Path(remote_file).open("rb") as stream:
                remote_hash = hashlib.file_digest(stream, "sha256").hexdigest()
            if local_hash != remote_hash:
                raise RuntimeError("Remote new corpus file hash mismatch: " + filename)
    for root, filename in metadata_release_docs:
        remote_file = hf_hub_download(
            repo_id=repo_id, repo_type="dataset",
            filename=f"corpora/{root.name}/{filename}",
            revision=result.oid, token=token)
        with (root / filename).open("rb") as stream:
            local_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        with Path(remote_file).open("rb") as stream:
            remote_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        if local_hash != remote_hash:
            raise RuntimeError("Remote metadata file hash mismatch: " + str(root / filename))
    summary = {"hf_repo": repo_id, "hf_revision": result.oid,
               "github_sha": sha, "synced_metadata_files": len(entries),
               "mirrored_existing_records": bulk_manifest["retained_records"],
               "published_new_corpus_records": uci_manifest["record_count"],
               "published_new_corpus_tokens": uci_manifest["whitespace_delimited_tokens"],
               "published_wikisource_records": wikisource_manifest["record_count"],
               "published_wikisource_tokens": wikisource_manifest["whitespace_delimited_tokens"],
               "verified_new_corpus_files": sum(len(item["files"]) for item in new_releases),
               "metadata_only": args.metadata_only,
               "metadata_release_docs": len(metadata_release_docs)}
    if new_releases:
        summary.update({
            "published_urwiki_records": new_releases[0]["manifest"]["record_count"],
            "published_urwiki_tokens": new_releases[0]["manifest"]["whitespace_delimited_tokens"],
            "published_sangraha_records": new_releases[1]["manifest"]["record_count"],
            "published_sangraha_tokens": new_releases[1]["manifest"]["whitespace_delimited_tokens"],
            "published_sangraha_shard_1_records": new_releases[2]["manifest"]["record_count"],
            "published_sangraha_shard_1_tokens": new_releases[2]["manifest"]["whitespace_delimited_tokens"],
        })
        for release in new_releases[3:]:
            number = release["manifest"]["source"]["file"].rsplit("-", 1)[-1].split(".", 1)[0]
            summary[f"published_sangraha_shard_{number}_records"] = release["manifest"]["record_count"]
            summary[f"published_sangraha_shard_{number}_tokens"] = release["manifest"]["whitespace_delimited_tokens"]
    print(json.dumps(summary))


if __name__ == "__main__":
    main()

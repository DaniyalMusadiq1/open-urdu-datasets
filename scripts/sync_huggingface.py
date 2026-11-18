"""Sync validated GitHub metadata to HF; never claim unhosted shards are published."""
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
)
PREFIX = "github-sync"
BULK_ROOT = Path("datasets/corpora/dakshina-urdu-bulk")
BULK_REMOTE = "corpora/dakshina-urdu-bulk"
UCI_ROOT = Path("datasets/classification/uci-roman-urdu-sentiment")
UCI_REMOTE = "classification/uci-roman-urdu-sentiment"


def main():
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
    manifest = {"source_repository": "DaniyalMusadiq1/open-urdu-datasets",
                "github_commit": sha, "files": entries,
                "scope": "metadata_mirror_only",
                "warning": "No new corpus shards published by this sync"}
    operations.append(CommitOperationAdd(
        path_in_repo=f"{PREFIX}/sync-manifest.json",
        path_or_fileobj=(json.dumps(manifest, indent=2) + "\n").encode("utf-8")))
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
    print(json.dumps({"hf_repo": repo_id, "hf_revision": result.oid,
                      "github_sha": sha, "synced_metadata_files": len(entries),
                      "mirrored_existing_records": bulk_manifest["retained_records"],
                      "published_new_corpus_records": uci_manifest["record_count"],
                      "published_new_corpus_tokens": uci_manifest["whitespace_delimited_tokens"]}))


if __name__ == "__main__":
    main()

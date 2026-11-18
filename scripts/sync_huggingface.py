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
    "datasets/corpora/dakshina-urdu-bulk/manifest.json",
)
PREFIX = "github-sync"


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
    print(json.dumps({"hf_repo": repo_id, "hf_revision": result.oid,
                      "github_sha": sha, "synced_metadata_files": len(entries),
                      "published_new_corpus_records": 0}))


if __name__ == "__main__":
    main()

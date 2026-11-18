"""Explicit opt-in Hugging Face upload; never called from CI."""
import argparse
import json
import os
from pathlib import Path

from phase2_validate import validate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--repo-id", required=True, help="Existing HF dataset repository")
    parser.add_argument("--confirm-upload", action="store_true")
    args = parser.parse_args()
    if not args.confirm_upload:
        parser.error("publication requires --confirm-upload")
    if not os.environ.get("HF_TOKEN"):
        parser.error("HF_TOKEN environment variable required")
    folder = Path(args.folder)
    summary = validate(folder)
    from huggingface_hub import HfApi
    api = HfApi(token=os.environ["HF_TOKEN"])
    api.upload_folder(repo_id=args.repo_id, repo_type="dataset",
                      folder_path=str(folder), path_in_repo="phase2")
    print(json.dumps({"uploaded_to": args.repo_id, "local_validation": summary,
                      "note": "Check remote file hashes before counting as published"}))


if __name__ == "__main__":
    main()

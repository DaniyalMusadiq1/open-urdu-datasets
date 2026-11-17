"""Validate the published web sample and uploaded-book intake metadata offline."""
import gzip
import hashlib
import json
from pathlib import Path

from urdu_data.core import verify_checksums

ROOT = Path(__file__).resolve().parents[1]


def main():
    entries = json.loads((ROOT / "catalog/web-corpora.json").read_text())
    for entry in entries:
        folder = ROOT / entry["local_path"]
        if not folder.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("unsafe dataset path")
        verify_checksums(folder / "checksums.sha256")
        manifest = json.loads((folder / "manifest.json").read_text())
        data = folder / manifest["data_path"]
        if not data.resolve().is_relative_to(folder.resolve()):
            raise ValueError("unsafe data path")
        if hashlib.sha256(data.read_bytes()).hexdigest() != manifest["data_sha256"]:
            raise ValueError("web data checksum differs")
        with gzip.open(data, "rt", encoding="utf-8") as stream:
            rows = [json.loads(line) for line in stream]
        if len(rows) != entry["documents"] or len(rows) != manifest["documents"]:
            raise ValueError("web document count differs")
        if len({row["id"] for row in rows}) != len(rows):
            raise ValueError("duplicate web documents")
        for row, evidence in zip(rows, manifest["crawl"]["pages"], strict=True):
            if row["id"] != hashlib.sha256(row["text"].encode()).hexdigest():
                raise ValueError("text identity differs")
            if row["license"] != "CC-BY-SA-4.0" or row["review_status"] != "unreviewed":
                raise ValueError("unexpected rights/review claim")
            if (row["source"]["revision_id"] != evidence["revision_id"]
                    or row["source"]["response_sha256"] != evidence["response_sha256"]
                    or not evidence["robots_allowed"]):
                raise ValueError("source evidence differs")
            if not row["attribution"] or not row["changes"] or not row["date_accessed"]:
                raise ValueError("missing attribution/changes/date")
        tokens = sum(len(row["text"].split()) for row in rows)
        if tokens != manifest["whitespace_tokens"] or tokens != entry["whitespace_tokens"]:
            raise ValueError("web token count differs")
        if manifest["human_reviewed_records"] != 0:
            raise ValueError("unsupported human review count")
        print(json.dumps({"web_documents": len(rows), "whitespace_tokens": tokens, "errors": 0}))
    intake = json.loads((ROOT / "catalog/upload-intake.json").read_text())
    if intake["raw_files_published"] or any(r["hosted"] for r in intake["items"]):
        raise ValueError("unapproved uploaded-book hosting")
    print(json.dumps({"uploaded_books_inspected": len(intake["items"]), "raw_books_hosted": 0}))


if __name__ == "__main__":
    main()

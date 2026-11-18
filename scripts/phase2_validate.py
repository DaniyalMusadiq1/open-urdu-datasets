"""Verify locally generated Phase 2 corpus counts and shard checksums."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from urdu_data.phase2 import accept, digest

def validate(folder):
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "local_unpublished":
        raise ValueError("unexpected manifest status")
    seen = set()
    total = tokens = 0
    for shard in manifest["shards"]:
        path = (folder / shard["path"]).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError("unsafe shard path")
        if hashlib.sha256(path.read_bytes()).hexdigest() != shard["sha256"]:
            raise ValueError("checksum mismatch")
        count = subtokens = 0
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if accept({**row, "redistribution_cleared": True}) is not None:
                    raise ValueError("invalid record")
                if row["id"] != digest(row["text"]) or row["id"] in seen:
                    raise ValueError("invalid or duplicate identity")
                if row["review_status"] != "unreviewed":
                    raise ValueError("unsubstantiated human review")
                if row["token_count_whitespace"] != len(row["text"].split()):
                    raise ValueError("token mismatch")
                seen.add(row["id"])
                count += 1
                subtokens += row["token_count_whitespace"]
        if count != shard["records"] or subtokens != shard["tokens"]:
            raise ValueError("shard counts differ")
        total += count
        tokens += subtokens
    if total != manifest["record_count"] or tokens != manifest["whitespace_delimited_tokens"]:
        raise ValueError("manifest counts differ")
    return {"records": total, "whitespace_delimited_tokens": tokens, "errors": 0}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    print(json.dumps(validate(args.folder)))

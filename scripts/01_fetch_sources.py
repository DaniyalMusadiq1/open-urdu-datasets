#!/usr/bin/env python3
"""Fetch approved, pinned Klam source files and record their checksums."""
import argparse
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "configs" / "sources.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "raw"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_registry():
    # sources.yaml is JSON syntax, which is also valid YAML 1.2. This avoids
    # requiring another parser just to fetch pinned sources.
    with REGISTRY.open(encoding="utf-8") as stream:
        registry = json.load(stream)
    if registry.get("schema_version") != "1.0" or not isinstance(registry.get("sources"), list):
        raise ValueError("unsupported or malformed source registry")
    return registry


def download_one(source, item, output_root):
    if source.get("status") != "approved" or source.get("download_enabled") is not True:
        raise ValueError("refusing to fetch source that is not approved for redistribution: " + source["source_id"])
    source_id = source["source_id"]
    relative = Path(source_id) / item["filename"]
    destination = output_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    expected = item.get("sha256")
    if destination.is_file():
        actual = sha256(destination)
        if expected is None or actual == expected:
            return {"path": relative.as_posix(), "url": item["url"], "sha256": actual, "bytes": destination.stat().st_size, "reused": True}
        destination.unlink()
    temporary = destination.with_name(destination.name + ".part")
    request = urllib.request.Request(item["url"], headers={"User-Agent": "klam-urdu-roman/0.1 source-fetch"})
    digest = hashlib.sha256()
    size = 0
    try:
        with urllib.request.urlopen(request, timeout=180) as response, temporary.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        actual = digest.hexdigest()
        if expected and actual != expected:
            raise ValueError("SHA-256 mismatch for " + source_id + "/" + item["filename"] + ": expected " + expected + ", got " + actual)
        os.replace(temporary, destination)
        return {"path": relative.as_posix(), "url": item["url"], "sha256": actual, "bytes": size, "reused": False}
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", help="approved source ID; repeat to select more than one")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    registry = load_registry()
    enabled = [s for s in registry["sources"] if s.get("status") == "approved" and s.get("download_enabled") is True]
    selected_ids = set(args.source) if args.source else {s["source_id"] for s in enabled}
    known_ids = {s["source_id"] for s in registry["sources"]}
    unknown = selected_ids - known_ids
    if unknown:
        raise SystemExit("unknown source ID(s): " + ", ".join(sorted(unknown)))
    selected = [s for s in enabled if s["source_id"] in selected_ids]
    if len(selected) != len(selected_ids):
        raise SystemExit("one or more selected sources are not approved and enabled for download")
    output_root = args.output.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    records = []
    for source in selected:
        for item in source.get("files", []):
            print("Fetching " + source["source_id"] + "/" + item["filename"], flush=True)
            records.append({"source_id": source["source_id"], **download_one(source, item, output_root)})
    manifest = {
        "dataset": "Klam-Urdu-Roman",
        "manifest_version": "1.0",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "registry": str(REGISTRY.relative_to(ROOT)),
        "files": records,
    }
    (output_root / "fetch-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_root), "files_fetched": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print("Fetch failed: " + str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
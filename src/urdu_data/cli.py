"""Explicit CLI. Outputs are created exclusively to protect existing files."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .core import (
    decode_csv_cells,
    duplicate_groups,
    normalize,
    read_records,
    stats,
    validate,
    verify_checksums,
    write_records,
)


def check_link(url):
    if urlparse(url).scheme not in {"http", "https"}:
        return {"url": url, "status": "invalid_scheme"}
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "open-urdu-datasets/0.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            return {"url": url, "status": "ok", "http_status": response.status,
                    "final_url": response.url}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": "unverified", "http_status": exc.code}
    except (OSError, ValueError) as exc:
        return {"url": url, "status": "unverified", "error": type(exc).__name__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "duplicates", "stats", "convert", "normalize"):
        p = sub.add_parser(name)
        p.add_argument("input", type=Path)
        if name == "validate":
            p.add_argument("schema", type=Path)
            p.add_argument("--typed-csv", action="store_true")
        if name in {"convert", "normalize"}:
            p.add_argument("output", type=Path)
        if name == "convert":
            p.add_argument("--typed-csv", action="store_true")
        if name == "duplicates":
            p.add_argument("--fields", nargs="+")
        if name == "normalize":
            p.add_argument("--field", required=True)
            p.add_argument("--nfc", action="store_true")
            p.add_argument("--map-yeh-kaf", action="store_true")
            p.add_argument("--digits", choices=["ascii", "urdu"])
            p.add_argument("--whitespace", action="store_true")
    sub.add_parser("checksums").add_argument("manifest", type=Path)
    sub.add_parser("links").add_argument("catalog", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "checksums":
            print(json.dumps({"checked": verify_checksums(args.manifest)}))
            return
        if args.command == "links":
            urls = sorted({r[k] for r in read_records(args.catalog)
                           for k in ("original_source_url", "download_url", "license_url") if r[k]})
            results = [check_link(url) for url in urls]
            print(json.dumps(results, indent=2))
            if any(r["status"] != "ok" for r in results):
                sys.exit(1)
            return
        rows = read_records(args.input)
        if getattr(args, "typed_csv", False):
            rows = decode_csv_cells(rows)
        if args.command == "validate":
            errors = validate(rows, json.loads(args.schema.read_text(encoding="utf-8")))
            print(json.dumps({"records": len(rows), "errors": errors}, ensure_ascii=False))
            if errors:
                sys.exit(1)
        elif args.command == "duplicates":
            print(json.dumps(duplicate_groups(rows, args.fields)))
        elif args.command == "stats":
            print(json.dumps(stats(rows)))
        elif args.command == "convert":
            write_records(args.output, rows)
        elif args.command == "normalize":
            result = []
            for row in rows:
                if "normalization" in row:
                    raise ValueError("refusing to replace existing normalization audit")
                result.append({**row, "normalization": normalize(row[args.field], nfc=args.nfc,
                              map_yeh_kaf=args.map_yeh_kaf, digits=args.digits,
                              whitespace=args.whitespace)})
            write_records(args.output, result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"{type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    main()

"""Small, explicit data operations with UTF-8 and no overwrite defaults."""

import csv
import hashlib
import json
import unicodedata
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def read_records(path):
    path = Path(path)
    with path.open(encoding="utf-8", newline="") as stream:
        if path.suffix == ".jsonl":
            rows = []
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    raise ValueError(f"blank JSONL line {line_number}")
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise TypeError(f"JSONL line {line_number} must be an object")
                rows.append(row)
            return rows
        if path.suffix == ".json":
            rows = json.load(stream)
            if not isinstance(rows, list):
                raise ValueError("JSON dataset must be an array")
            return rows
        if path.suffix == ".csv":
            reader = csv.DictReader(stream)
            fields = reader.fieldnames
            if not fields or len(fields) != len(set(fields)):
                raise ValueError("CSV header must be nonempty and unique")
            rows = list(reader)
            if any(None in r or any(v is None for v in r.values()) for r in rows):
                raise ValueError("CSV row width differs from header")
            return rows
    raise ValueError("supported inputs: .json, .jsonl, .csv")


def write_records(path, rows):
    """Create output exclusively. JSON cells in CSV retain nested types on conversion."""
    path = Path(path)
    if path.suffix not in {".json", ".jsonl", ".csv"}:
        raise ValueError("supported outputs: .json, .jsonl, .csv")
    with path.open("x", encoding="utf-8", newline="") as stream:
        if path.suffix == ".json":
            json.dump(rows, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        elif path.suffix == ".jsonl":
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        elif rows:
            fields = list(rows[0])
            if any(set(row) != set(fields) for row in rows):
                raise ValueError("CSV requires consistent fields")
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows({k: json.dumps(v, ensure_ascii=False) for k, v in r.items()} for r in rows)


def decode_csv_cells(rows):
    """Explicit typed-CSV decoder; never applied to arbitrary CSV automatically."""
    return [{k: json.loads(v) for k, v in row.items()} for row in rows]


def validate(rows, schema):
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for index, row in enumerate(rows, 1):
        for error in validator.iter_errors(row):
            errors.append(f"row {index} {list(error.path)}: {error.message}")
    return errors


def duplicate_groups(rows, fields=None):
    groups = {}
    for index, row in enumerate(rows, 1):
        key = row if fields is None else {field: row[field] for field in fields}
        serial = json.dumps(key, ensure_ascii=False, sort_keys=True)
        groups.setdefault(serial, []).append(index)
    return [indexes for indexes in groups.values() if len(indexes) > 1]


def normalize(text, *, nfc=False, map_yeh_kaf=False, digits=None, whitespace=False):
    """Return original + candidate + applied operations, never replacing input text.

    Preserve Heh Doachashmee, Yeh Barree, joiners, diacritics and punctuation.
    Mapping Arabic Yeh/Kaf is optional because it may damage quoted Arabic.
    """
    candidate = text
    operations = []

    def apply(name, value):
        nonlocal candidate
        if value != candidate:
            operations.append({"operation": name, "before": candidate, "after": value})
            candidate = value

    if nfc:
        apply("NFC", unicodedata.normalize("NFC", candidate))
    if map_yeh_kaf:
        apply("Arabic Yeh/Kaf to Urdu", candidate.translate({0x064A: 0x06CC, 0x0643: 0x06A9}))
    if digits not in {None, "ascii", "urdu"}:
        raise ValueError("digits must be ascii, urdu, or None")
    if digits:
        target = "0123456789" if digits == "ascii" else "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"
        source = "0123456789\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"
        apply("digit mapping: " + digits, candidate.translate(str.maketrans(source, target * 3)))
    if whitespace:
        apply("Unicode whitespace collapse", " ".join(candidate.split()))
    return {"original": text, "normalized": candidate, "changes": operations}


def stats(rows):
    return {"records": len(rows), "exact_duplicate_groups": duplicate_groups(rows),
            "review_status": dict(Counter(row.get("review_status", "not_applicable") for row in rows))}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_checksums(manifest):
    manifest = Path(manifest)
    root = manifest.parent.resolve()
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        target = (root / relative).resolve()
        if not target.is_relative_to(root) or len(digest) != 64:
            raise ValueError("unsafe or invalid checksum entry")
        if not target.is_file() or sha256(target) != digest:
            raise ValueError(f"checksum mismatch: {relative}")
        checked += 1
    if checked == 0:
        raise ValueError("empty checksum manifest")
    return checked

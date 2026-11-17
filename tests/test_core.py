"""Synthetic software fixtures only; no human-reviewed Urdu language examples."""
import json

import pytest

from urdu_data.core import (
    decode_csv_cells,
    duplicate_groups,
    normalize,
    read_records,
    sha256,
    validate,
    verify_checksums,
    write_records,
)


def test_normalization_default_preserves_joiners_diacritics_and_letters():
    text = "\u064a\u0643\u06be\u06c1\u06d2\u200c\u200d\u064e\u06f1\u0662\t  !"
    result = normalize(text)
    assert result == {"original": text, "normalized": text, "changes": []}


def test_explicit_normalization_audit_and_idempotence():
    text = " \u064a\u0643\u200c\u200d\u064e\u0661\u06f2  "
    result = normalize(text, map_yeh_kaf=True, digits="ascii", whitespace=True)
    assert result["original"] == text
    assert result["normalized"] == "\u06cc\u06a9\u200c\u200d\u064e12"
    assert len(result["changes"]) == 3
    assert normalize(result["normalized"], map_yeh_kaf=True, digits="ascii",
                     whitespace=True)["changes"] == []


def test_csv_roundtrip_nested_types_and_nulls(tmp_path):
    rows = [{"text": "comma,\nquote\"", "value": None, "provenance": {"line": 1}, "hosted": False}]
    output = tmp_path / "new.csv"
    write_records(output, rows)
    assert decode_csv_cells(read_records(output)) == rows
    with pytest.raises(FileExistsError):
        write_records(output, [{"changed": "no"}])
    assert decode_csv_cells(read_records(output)) == rows


@pytest.mark.parametrize("text", ['a,a\nx,y\n', 'a,b\nx\n', 'a,b\nx,y,z\n'])
def test_csv_rejects_duplicate_headers_and_ragged_rows(tmp_path, text):
    path = tmp_path / "bad.csv"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        read_records(path)


def test_invalid_utf8_and_jsonl_are_rejected(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_bytes(b'\xff')
    with pytest.raises(UnicodeDecodeError):
        read_records(path)
    path.write_text('[1,2]\n', encoding="utf-8")
    with pytest.raises(TypeError):
        read_records(path)


def test_required_fields_and_uri_format():
    schema = {"type": "object", "required": ["source"],
              "properties": {"source": {"type": "string", "format": "uri"}}}
    assert len(validate([{}, {"source": "not a uri"}], schema)) == 2
    assert validate([{"source": "https://example.org"}], schema) == []


def test_duplicates_by_content_ignore_provenance_when_requested():
    rows = [{"text": "same", "source": 1}, {"text": "same", "source": 2}]
    assert duplicate_groups(rows) == []
    assert duplicate_groups(rows, ["text"]) == [[1, 2]]


def test_checksum_tampering_and_path_escape(tmp_path):
    data = tmp_path / "data.jsonl"
    data.write_text(json.dumps({"fixture": True}) + "\n", encoding="utf-8")
    digest = sha256(data)
    manifest = tmp_path / "checksums.sha256"
    manifest.write_text(f"{digest}  data.jsonl\n", encoding="utf-8")
    assert verify_checksums(manifest) == 1
    data.write_text("tampered\n", encoding="utf-8")
    with pytest.raises(ValueError, match="mismatch"):
        verify_checksums(manifest)
    manifest.write_text(f"{digest}  ../outside\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unsafe"):
        verify_checksums(manifest)

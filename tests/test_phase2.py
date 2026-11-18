import json
from urdu_data.phase2 import accept, build
from scripts.phase2_validate import validate


def row(text="یہ ایک اردو عبارت ہے جس میں کافی الفاظ موجود ہیں اور متن مکمل ہے"):
    return {"text": text, "category": "books", "script": "urdu_arabic",
            "license": "CC-BY-4.0", "source_url": "https://example.org/book",
            "source_version": "v1", "rights_evidence_url": "https://example.org/license",
            "document_id": "chapter1", "revision": "v1", "redistribution_cleared": True}


def test_fail_closed():
    value = row()
    assert accept(value) is None
    assert accept({**value, "license": "CC-BY-NC-4.0"}) == "license_not_allowlisted"
    assert accept({**value, "redistribution_cleared": False}) == "rights_not_cleared"
    english = {**value, "text": "Only English text for this record is provided"}
    assert accept(english) == "script_mismatch"


def test_canonical_duplicates(tmp_path):
    source = tmp_path / "input.jsonl"
    a = row("یہ ایک اردو عبارت ہے جس میں کافی الفاظ موجود ہیں اور متن مکمل ہے")
    b = row("یہ  ایک اردو عبارت ہے جس میں کافی الفاظ موجود ہیں اور متن مکمل ہے")
    source.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in [a, b]) + "\n",
                      encoding="utf-8")
    result = build(source, tmp_path / "out")
    assert result["record_count"] == 1
    assert result["rejected"]["exact_duplicate"] == 1
    assert validate(tmp_path / "out")["records"] == 1


def test_build_validate(tmp_path):
    source = tmp_path / "input.jsonl"
    source.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in
                      [row(), row(), {**row(), "license": "unspecified"}]) + "\n",
                      encoding="utf-8")
    target = tmp_path / "out"
    result = build(source, target, max_records_per_shard=1)
    assert result["record_count"] == 1
    assert result["rejected"]["exact_duplicate"] == 1
    assert result["rejected"]["license_not_allowlisted"] == 1
    assert validate(target)["records"] == 1

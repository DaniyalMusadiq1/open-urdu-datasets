"""Synthetic software fixtures; no language examples are added to Klam."""
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.build_klam_release import (
    adapt_source_row,
    dedup_key,
    normalize_row,
    write_shard,
)
from scripts.validate_klam_release import validate


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/klam-record.schema.json").read_text(encoding="utf-8"))


def source():
    return {
        "source_version": "Dakshina-v1.0",
        "rights_basis": "cc_by_sa",
        "license": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "rights_evidence_url": "https://example.org/license",
        "attribution": "Synthetic test fixture",
    }


def test_dakshina_romanization_pair_keeps_both_scripts_and_valid_provenance():
    row = {
        "id": "fixture-pair-1",
        "record_type": "romanization_pair",
        "split": "dev",
        "text": "آزمائشی متن",
        "roman": "synthetic Roman side",
        "source": {
            "member": "lexicons/ur.translit.sampled.train.tsv",
            "line": 17,
            "revision_url": "https://ur.wikipedia.org/w/index.php?oldid=123",
        },
    }
    result = adapt_source_row("dakshina-urdu-bulk", row, source())
    assert result["task"] == "transliteration_pair"
    assert result["split"] == "validation"
    assert result["script"] == "Arabic"
    assert result["paired_text"] == "synthetic Roman side"
    assert result["paired_script"] == "Latin"
    Draft202012Validator(SCHEMA).validate(result)


def test_pair_identity_includes_both_sides():
    base = {"text": "Urdu text", "paired_text": "roman one",
            "task": "transliteration_pair", "label": ""}
    alternate = {**base, "paired_text": "roman two"}
    assert dedup_key(base) != dedup_key(alternate)
    assert dedup_key(base) == dedup_key({**base, "source_id": "other"})


def test_transliteration_pair_schema_requires_pair_fields():
    row = {
        "id": "a" * 64,
        "title": "",
        "text": "text",
        "language": "ur",
        "script": "Arabic",
        "task": "transliteration_pair",
        "label": "",
        "split": "train",
        "source_id": "fixture",
        "source_version": "1",
        "source_record_id": "r1",
        "source_locator": "",
        "rights_basis": "cc_by",
        "license": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "rights_evidence_url": "https://example.org/license",
        "attribution": "Synthetic test fixture",
        "review_status": "unreviewed",
        "reviewer_id": "",
        "review_date": "",
        "review_scope": "",
    }
    errors = list(Draft202012Validator(SCHEMA).iter_errors(row))
    assert any("paired_text" in error.message for error in errors)
    assert any("paired_script" in error.message for error in errors)


def test_release_validator_checks_pair_rows_and_manifest(tmp_path):
    release = tmp_path / "release"
    (release / "data").mkdir(parents=True)
    metadata = {
        "source_id": "fixture-source",
        **source(),
    }
    row = normalize_row(
        {"text": "آزمائشی متن", "review_status": "unreviewed"},
        "fixture-source",
        metadata,
        source_record_id="fixture-row-1",
        task="transliteration_pair",
        paired_text="aazmaishi matn",
        paired_script="Latin",
    )
    shard = write_shard(release, 1, [row], "train")
    source_bytes = json.dumps(
        {"policy_version": "1.0", "sources": [metadata]},
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")
    (release / "sources.json").write_bytes(source_bytes)
    manifest = {
        "record_count": 1,
        "whitespace_delimited_tokens": len(row["text"].split()),
        "paired_whitespace_delimited_tokens": len(row["paired_text"].split()),
        "human_reviewed_records": 0,
        "source_record_counts": {"fixture-source": 1},
        "task_record_counts": {"transliteration_pair": 1},
        "split_record_counts": {"train": 1},
        "license_record_counts": {"CC-BY-SA-4.0": 1},
        "sources": [metadata],
        "shards": [shard],
    }
    (release / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    (release / "checksums.sha256").write_text(
        f"{shard['sha256']}  {shard['path']}\n{source_hash}  sources.json\n",
        encoding="utf-8",
    )
    result = validate(release)
    assert result["records"] == 1
    assert result["paired_whitespace_delimited_tokens"] == 2
    assert result["integrity"] == "ok"

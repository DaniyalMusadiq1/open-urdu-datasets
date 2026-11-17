"""Synthetic code fixtures only; no invented Urdu language records."""
from urdu_data.bulk import flags, identity


def test_contact_triage_is_explicit_and_conservative():
    assert flags("contact fixture@example.org") == ["email_like"]
    assert flags("fixture +012345678901") == ["international_phone_like"]
    assert flags("a date: 2026-11-17") == []


def test_exact_identity_preserves_codepoint_differences_and_record_types():
    assert identity("native_sentence", "\u064a") != identity("native_sentence", "\u06cc")
    assert identity("native_sentence", "text") != identity("romanization_pair", "text", "roman")
    assert identity("romanization_pair", "text", "roman") != identity("romanization_pair", "text", "other")

"""English fixture tokens only, not translated or native-reviewed language data."""
import pytest

from urdu_data.pairs import aligned_passages


def record(number, text):
    return {"link": f"https://example.org/{number}", "question_number": 1,
            "correct_answer_num": "1", "flores_passage": text}


def test_pairs_use_ids_rather_than_line_order():
    english = [record(1, "first"), record(2, "second")]
    translated = [record(2, "fixture-two"), record(1, "fixture-one")]
    result = aligned_passages(english, translated)
    assert result[0]["urdu"] == "fixture-one"
    assert result[0]["urdu_line"] == 2


def test_pairs_reject_missing_or_duplicate_identifiers():
    rows = [record(1, "first"), record(2, "second")]
    with pytest.raises(ValueError, match="do not align"):
        aligned_passages(rows, rows[:1])
    with pytest.raises(ValueError, match="duplicate"):
        aligned_passages(rows + rows[:1], rows)


def test_pairs_check_all_answers_even_beyond_sample_limit():
    rows = [record(1, "first"), record(2, "second")]
    translated = [record(1, "fixture-one"), {**record(2, "fixture-two"), "correct_answer_num": "2"}]
    with pytest.raises(ValueError, match="answer IDs"):
        aligned_passages(rows, translated, limit=1)

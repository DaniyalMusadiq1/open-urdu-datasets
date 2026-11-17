"""Align licensed evaluation sources by publisher identifiers, never row position."""


def aligned_passages(english_rows, urdu_rows, limit=5):
    if limit < 1:
        raise ValueError("limit must be positive")

    def index(rows):
        found = {}
        for line, row in enumerate(rows, 1):
            key = (row["link"], row["question_number"])
            if key in found:
                raise ValueError("duplicate source identifier")
            found[key] = (line, row)
        return found

    english = index(english_rows)
    urdu = index(urdu_rows)
    if set(english) != set(urdu):
        raise ValueError("source identifiers do not align")
    output = []
    seen = set()
    for key, (english_line, en) in english.items():
        urdu_line, ur = urdu[key]
        if en["correct_answer_num"] != ur["correct_answer_num"]:
            raise ValueError("answer IDs differ across translations")
        if not en["flores_passage"] or not ur["flores_passage"]:
            raise ValueError("empty source passage")
        if en["flores_passage"] in seen:
            continue
        seen.add(en["flores_passage"])
        if len(output) < limit:
            output.append({"english": en["flores_passage"], "urdu": ur["flores_passage"],
                           "english_line": english_line, "urdu_line": urdu_line,
                           "upstream_page": key[0], "question_number": key[1]})
    return output

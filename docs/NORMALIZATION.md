# Conservative Unicode processing

`urdu-data normalize input.jsonl output.jsonl --field urdu` performs no changes by default. It preserves the source field and adds an audit object containing the original, candidate and each applied operation. Output must be a new file.

- `--nfc`: canonical composition only. Never NFKC.
- `--map-yeh-kaf`: optional Arabic Yeh U+064A → Urdu Yeh U+06CC and Arabic Kaf U+0643 → Urdu Kaf U+06A9. May corrupt Arabic quotations or multilingual text; requires review.
- `--digits ascii|urdu`: explicit mapping among ASCII, Arabic-Indic and Eastern Arabic-Indic digit forms. Original digits remain in the audit.
- `--whitespace`: explicitly collapse Unicode whitespace; may remove meaningful line boundaries.
- Heh Doachashmee U+06BE, Heh Goal U+06C1, Yeh Barree U+06D2, diacritics, ZWNJ U+200C, ZWJ U+200D and punctuation are preserved. No diacritic stripping, joiner removal, spelling correction, punctuation folding, or automatic transliteration is implemented.

The tests use escaped Unicode codepoints as synthetic software fixtures, not human-reviewed language examples. Normalization is not language verification.

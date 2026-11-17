---
language:
- ur
license: cc-by-sa-4.0
task_categories:
- translation
pretty_name: Dakshina Urdu romanization vocabulary sample
---

# Dakshina Urdu romanization vocabulary sample

25 records derived from an explicitly licensed source, not AI-generated language data. Technical provenance and structure are checked; all records remain `review_status: unreviewed` pending local native-speaker review. Upstream human attestations do not mean this project has reviewed their correctness.

## Fields

`urdu`, `roman`, `english`, `pos`, `example`, `source`, `license`, `review_status`, `attestations`. English meanings, POS and examples are null because the lexicon does not supply them. Do not fill them with guesses. `source.line` is the 1-based upstream TSV row, not the position in this sample.

## Scope and limitations

A deterministic first-word sample for testing tools, not a representative dictionary, teaching vocabulary, test benchmark or balanced linguistic resource. Roman Urdu spellings vary. Diacritics and source forms are retained. Upstream Wikipedia-derived vocabulary may include names, rare forms or language contamination. The default selection rule overweights alphabetically early words.

No private data is intentionally included. Automatic contact-pattern triage is limited and does not prove absence of sensitive content. No human review of toxicity or linguistic correctness has been completed. Do not infer identity from names.

## Rights and provenance

CC BY-SA 4.0 applies to the derived data. See LICENSE and SOURCES.md for attribution, changes and complete member checksum. The MIT project license does not apply to these records.

## Loading

```python
import json
from pathlib import Path
path = Path('datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl')
rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
assert len(rows) == 25
```

Validate with `urdu-data validate datasets/vocabulary/dakshina-urdu-sample/data/vocabulary.jsonl schemas/vocabulary.schema.json` and `urdu-data checksums datasets/vocabulary/dakshina-urdu-sample/checksums.sha256`.

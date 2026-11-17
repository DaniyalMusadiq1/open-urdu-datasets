---
language:
- ur
- en
license: cc-by-sa-4.0
task_categories:
- translation
pretty_name: Belebele Urdu-English evaluation passage sample
---

# Belebele Urdu-English evaluation passage sample

Five real paired passages copied from the publisher's CC-BY-SA evaluation data, joined by source identifiers. This sample is for loading/provenance demonstrations and evaluation inspection only. Do not use it for training or model-selection validation; this would contaminate a public evaluation benchmark.

Fields: `urdu`, `english`, nested `source`, `license`, `review_status`, `usage`. Every record is `review_status: unreviewed` and `usage: evaluation_only`. Text is preserved exactly; no Urdu or English was generated here. Urdu/English correctness and appropriateness need native review.

## Content warnings and limitations

Includes historical military conflict and public historical names, as well as technical/instructional content. No claim of PII/toxicity absence is made. The five alphabetically early source passages are not representative of Urdu domains or dialects. Wikimedia-source material is copyright-sensitive but the publisher explicitly licenses this evaluation component; per-record original-page links and dataset attribution are preserved. The training mixture has different terms and is excluded.

No questions or answers are hosted in this derived passage sample. The source data contains questions and answers; its original copyright, license and evaluation restrictions apply. See SOURCES.md and LICENSE.

## Loading

```python
import json
from pathlib import Path
path = Path('datasets/translation/belebele-urdu-english-eval-sample/data/pairs.jsonl')
rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
assert len(rows) == 5
assert all(row['usage'] == 'evaluation_only' for row in rows)
```

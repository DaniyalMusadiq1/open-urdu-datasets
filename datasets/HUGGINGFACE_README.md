---
language:
- ur
pretty_name: Klam (کلام)
configs:
- config_name: klam
  default: true
  data_files:
  - split: train
    path: "klam-original/data/*.jsonl.gz"
---

# Klam (کلام)

Klam is being built as one simple Urdu dataset from original material, contributor submissions with explicit permission, and rights-verified public-domain works.

**The new Klam release is not available yet.** The source registry is empty, and no records will be published until their rights evidence and data checks pass. The earlier third-party corpus releases are not part of this new Klam collection.

When records are available, load the single Klam dataset with:

```bash
python -m pip install "datasets>=3,<5"
```

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

for row in data.take(3):
    print(row["text"])
```

The release uses one record format. Rows carry source version, rights basis, license, attribution, and review status. Source manifests stay with the Klam release for people who need to audit them.

See the [Klam contribution guide](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/KLAM_CONTRIBUTION.md) for how original and permissioned text can be added.

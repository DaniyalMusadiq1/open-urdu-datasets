# Klam data architecture

Klam is one simple dataset release built from original material, contributor text with explicit permission, and rights-verified public-domain works. Earlier third-party corpus packages remain separate reference material and are not Klam inputs.

## Where things live

| Location | Purpose |
| --- | --- |
| `datasets/klam/sources.json` | Approved source and rights registry |
| `datasets/klam/records/` | Klam-originated records awaiting release |
| `schemas/klam-record.schema.json` | One normalized Klam record schema |
| `scripts/build_klam_release.py` | Builds a rights-checked Klam release |
| Hugging Face `klam-original/` | Normalized JSONL.GZ release and manifests |
| Existing corpus directories and catalog | Historical/reference datasets; never inputs to Klam |

GitHub is the source of truth for the source registry, code, and release policy. Hugging Face provides the single loadable Klam collection once approved records exist.

## Record and rights flow

1. A source is registered with its version, rights basis, evidence link, license, and attribution.
2. A maintainer approves the source rights before records can enter Klam.
3. Records are normalized to one schema. Exact duplicates and unapproved sources stop the build.
4. Each output row carries its source, rights basis, license, attribution, and review status. Full source details remain in `sources.json`.
5. The release gets one Klam revision and checksum manifest. Users can load Klam without choosing an upstream dataset.

Original and contributor-submitted text must have explicit permission for CC BY 4.0. Public-domain records remain marked as public domain and require evidence for the exact work and edition. Klam does not relicense text it does not own.

## Loading

The Klam source registry is currently empty, so an original-source Klam release is not available to load yet. Once records pass rights review and validation, the default dataset can be read with:

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

See the [Klam contribution guide](KLAM_CONTRIBUTION.md), [license policy](LICENSE_POLICY.md), and [record schema](../schemas/klam-record.schema.json).

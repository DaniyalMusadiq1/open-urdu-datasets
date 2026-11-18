# Published Urdu corpus overview

This release combines separately loadable Urdu corpora from Urdu Wikipedia and AI4Bharat Sangraha with previously published Dakshina, UCI Roman Urdu and Urdu Wikisource datasets.

- Total: **2,217,970 records / 1,006,902,795 whitespace-delimited tokens**
- Native-speaker verified records: **0**; review remains pending
- Formats: source-specific UTF-8 JSONL.GZ shards
- Licenses: source-specific; see each `LICENSE` and `SOURCES.md`
- Dataset configuration names and loading instructions: see the repository-root Hugging Face card

The aggregate count is not a promise of semantic uniqueness. Exact duplicate text was checked after NFC normalization and whitespace collapse; near duplicates and quoted passages may remain. The upstream Sangraha “verified” label and automated language filters do not count as human review. Consult the per-source cards, manifests and checksums before using or redistributing files.

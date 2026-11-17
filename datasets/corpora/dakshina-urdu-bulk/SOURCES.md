# Source, licensing and attribution

Dakshina v1.0 by Brian Roark, Lawrence Wolf-Sonkin, Christo Kirov, Sabrina J. Mielke, Cibu Johny, Işın Demirşahin and Keith Hall. Original source text is from Urdu Wikipedia contributors. Each native-text record retains the exact original article URL, revision ID and revision URL from Dakshina's attribution mapping. Lexicon rows retain source member/line and upstream attestations; article-level source mappings are not supplied for individual lexicon words.

- Publisher: https://github.com/google-research-datasets/dakshina
- Explicit dataset license: https://github.com/google-research-datasets/dakshina#license
- Dataset license: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
- Full legalcode in LICENSE copied from SPDX's license registry: https://github.com/spdx/license-list-data/blob/main/text/CC-BY-SA-4.0.txt
- Official archive: https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar
- Complete archive downloaded and SHA-256 checked locally: `83530bec211893d9df429298f42e63c350c25ad56f9f5172f85edb0575ee5b03`, 2,008,340,480 bytes. This is a locally computed checksum, not a publisher signature.
- Accessed: 2026-11-17. Native Wikipedia extraction: March 2019, as described by the publisher.
- Paper: https://aclanthology.org/2020.lrec-1.294/

```bibtex
@inproceedings{roark-etal-2020-processing,
  title = {Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset},
  author = {Roark, Brian and Wolf-Sonkin, Lawrence and Kirov, Christo and Mielke, Sabrina J. and Johny, Cibu and Demirsahin, Isin and Hall, Keith},
  booktitle = {Proceedings of the 12th Language Resources and Evaluation Conference},
  year = {2020},
  pages = {2413--2423},
  url = {https://aclanthology.org/2020.lrec-1.294/}
}
```

## Exact selection and changes

Read only named Urdu native-text train/valid TSV.GZ files, the publisher's original-page attribution mapping, and train/dev/test lexicon TSV files. Keep native rows only when the publisher's `include_bool` equals 1. Other languages, shuffled duplicate renderings, auxiliary/full unfiltered corpora and romanized-sentence alternatives are not added as extra copies.

Copy text exactly without local Unicode normalization, spelling repair, translation or AI generation. Convert to JSONL.GZ; add typed provenance, CC-BY-SA license, record type, source split and `review_status: unreviewed`. Identity is SHA-256 of record type + original text (+ romanization for word pairs), not normalized text.

Remove exact duplicates globally within each record type, retaining first provenance and duplicate occurrence count. Process validation before training so shared text is retained in validation. No near-duplicate removal is claimed. Exclude contact/credential-like pattern matches; the excluded-row audit retains only source coordinate, text checksum and rule names, not the flagged text. This is limited triage, not a privacy or toxicity guarantee.

The reproducible importer is `scripts/import_dakshina_bulk.py`. Member checksums, source counts, output counts, word counts and every shard checksum are in manifest.json. Share adapted data under CC BY-SA 4.0 with author/source attribution and modification notices. No project MIT relicensing applies.

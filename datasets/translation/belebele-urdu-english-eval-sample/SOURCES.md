# Source, license and attribution

Belebele by Meta/Facebook Research and the dataset contributors; passages derive from FLORES and the Wikimedia-source contributors linked in each record.

- Dataset and citation: https://github.com/facebookresearch/belebele
- Publisher card: https://huggingface.co/datasets/facebook/belebele
- Immutable dataset version: `7899cdfa4e1e0d733fd77c848e2c273cb1d32be2`
- Explicit dataset license: https://github.com/facebookresearch/belebele#license
- Upstream full license: https://github.com/facebookresearch/belebele/blob/main/LICENSE_CC-BY-SA4.0
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- Full legalcode text in LICENSE copied from SPDX: https://github.com/spdx/license-list-data/blob/main/text/CC-BY-SA-4.0.txt
- Accessed: 2026-11-17.

The publisher explicitly identifies this as evaluation data, separate from its differently licensed training mixture. No training-mixture files are used. Preserve the publisher citation and attribution to the original Wikimedia pages/contributors when sharing adaptations. Original article links are retained per record; source-version details beyond the publisher files were not independently reconstructed.

The complete three publisher JSONL files were downloaded and structurally validated: 900 records in each of English, Urdu Arabic script and Romanized Urdu. The pair sample uses only English and Urdu Arabic-script passages. Record-level URL, line and SHA-256 refer to those complete publisher files.

Selection and changes: join all English/Urdu questions by original-page link and question number (900 matching IDs), require matching correct-answer IDs, and take the first five distinct English passages in English-file order. Collection-date `ds` fields differ by language and are not join keys. Text is copied exactly, without normalization or translation. JSONL wrappers/provenance/license/review/usage fields were added. This is a passage sample, not five independent evaluation questions and not a representative translation benchmark.

No local native-speaker correctness review has occurred. Upstream human annotation does not imply project-level human verification. Share adapted sample data under CC BY-SA 4.0 with attribution and modification notices.

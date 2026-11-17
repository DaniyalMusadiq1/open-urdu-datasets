# Sources and attribution

Derived from Dakshina v1.0 by Brian Roark, Lawrence Wolf-Sonkin, Christo Kirov, Sabrina J. Mielke, Cibu Johny, Işın Demirşahin and Keith Hall; source Wikipedia contributors as described by Dakshina.

- Original dataset: https://github.com/google-research-datasets/dakshina
- Explicit license statement: https://github.com/google-research-datasets/dakshina#license
- License: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
- Full license text copied from SPDX's license registry: https://github.com/spdx/license-list-data/blob/main/text/CC-BY-SA-4.0.txt
- Publication: https://aclanthology.org/2020.lrec-1.294/
- Official archive: https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar
- Archive ETag: `"a560868b1d6702602c4ea4e83794fa26"` (identifier, not a cryptographic content guarantee).
- Complete extracted member: `dakshina_dataset_v1.0/ur/lexicons/ur.translit.sampled.train.tsv`
- Member bytes: 2185405; SHA-256: `41f4f4109e60813f578a70a75b19189acb907e800a862401b7205f6f4a51e7f2`.
- Member rows counted locally: 106260; distinct native-script words: 25000.
- Member retrieved with HTTP byte range 1831772672–1833958076, after validation of the TAR header; the complete 2 GB archive was not downloaded or hashed.
- Accessed: 2026-11-17.

Selection: take the first 25 distinct Urdu source words in file order; for each, choose the romanization with greatest upstream attestation count, retaining the earliest source row for ties. The spelling is copied without normalization. Each record retains its member line and checksum.

Changes: TSV converted to JSONL; added provenance, explicit null English/POS/example fields and `review_status: unreviewed`; no text was generated or translated. Share adaptations of this sample under CC BY-SA 4.0 and keep attribution. No native-speaker review has been performed here.

The citation in the upstream README identifies the authors, paper title, LREC 2020 and pages 2413–2423; cite that publication for the underlying dataset.

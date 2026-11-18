# Automatic Hugging Face metadata synchronization

On every push to `main`, GitHub Actions validates the existing catalog, bulk
and web corpora, then mirrors selected README, catalog, dataset card and manifest
files to `Daniyal643/open-urdu-datasets` under `github-sync/`.

**One-time maintainer setup:** Create a fine-grained Hugging Face token with
write access to this dataset. In GitHub repository Settings > Secrets and
variables > Actions, add it as a repository secret named `HF_TOKEN`.
Never commit or paste the token. Without it the workflow fails closed.
The dataset must already exist. The workflow uses a concurrency group to
avoid overlapping sync runs. The HF dataset repository's root README and
existing dataset files are not overwritten.

The action verifies the remote synchronization manifest against the GitHub
commit SHA and records file hashes. A successful metadata sync is **not**
a corpus upload and must **not** increase published record or token counts.
The script intentionally does not mirror bulk corpus shards, historical
unpublished files, source archives or license-uncleared text. Publish new
shards only after explicit source-specific redistribution clearance, quality
review, validation, and remote SHA-256 verification. No native-speaker
verification is implied.

This is automatic synchronization of approved GitHub metadata, **not**
automatic ingestion of arbitrary new web/books/news/speech data. The 200M-token
milestone remains pending until independently validated hosted shards exist.

# Automatic Hugging Face metadata synchronization

On every push to `main`, GitHub Actions validates the repository, bulk, web,
UCI and Wikisource corpora, then mirrors selected README, catalog, dataset card
and manifest files to `Daniyal643/open-urdu-datasets` under `github-sync/`.

**One-time maintainer setup:** Create a fine-grained Hugging Face token with
write access to this dataset. In GitHub repository Settings > Secrets and
variables > Actions, add it as a repository secret named `HF_TOKEN`.
Never commit or paste the token. Without it the workflow fails closed.
The dataset must already exist. The workflow uses a concurrency group to
avoid overlapping sync runs. The HF dataset repository's root README and
existing dataset files are not overwritten.

The action verifies the remote synchronization manifest against the GitHub
commit SHA and records file hashes. It also uploads the rights-filtered Urdu
Wikisource `PD-old` release, the existing Dakshina bulk corpus, and the UCI
Roman Urdu release. It verifies remote SHA-256 hashes for the published corpus
files before reporting counts and the immutable revision. No native-speaker
verification is implied.

This is automatic synchronization of reviewed repository files, **not**
automatic ingestion of arbitrary web/books/news/speech data. The 200M-token
phase milestone and 1.3B overall target remain pending; public accessibility alone is not permission
to republish.

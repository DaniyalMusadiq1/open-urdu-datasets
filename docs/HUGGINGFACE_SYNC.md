# GitHub and Hugging Face layout

The project uses GitHub for source code, the discovery catalog, dataset cards, source/license evidence, import tools and validation. Hugging Face hosts the downloadable corpus files and the root dataset card with one configuration per source schema.

## Hugging Face folders

- `corpora/<dataset-id>/`: corpus cards, source notes, license, manifest, checksums and JSONL.GZ shards.
- `classification/<dataset-id>/`: task datasets and their source labels.
- `github-sync/`: a revisioned snapshot of selected GitHub metadata and a sync manifest.

The large Urdu Wikipedia and Sangraha releases are rebuilt from pinned inputs in GitHub Actions. Other released packages are copied from their validated GitHub directories. The root Hugging Face `README.md` is generated from `datasets/HUGGINGFACE_README.md`; its YAML defines independent loadable configurations. No mixed-license, mixed-schema “all in one” training split is created.

## Publishing and verification

Regular pushes to `main` skip corpus builds. Use **Actions > Publish pinned corpus releases to Hugging Face > Run workflow** on `main` to choose a release operation.

- `metadata` mirrors the validated catalog, dataset card and GitHub-hosted packages without rebuilding the large corpus. A push to `main` with `[hf-sync-metadata]` also selects this operation.
- `publish-cached` reuses the validated normalized Klam release for the current inputs and verifies its checksums before upload. It stops before publishing if the matching cache is unavailable.
- `prepare-only` builds or restores the release, validates a fresh build, and saves the resulting files for review without publishing to Hugging Face.
- `build-if-needed` explicitly allows a rebuild on a cache miss. It saves the validated normalized release before upload so a publishing retry can reuse it. Changed inputs or cache eviction can require a new build.

Preparation and publishing run as separate jobs. If publishing fails, retry the failed job to reuse the same release artifact while it is retained for 14 days. The uploader verifies shard checksums before committing.

**One-time maintainer setup:** Create a Hugging Face token with write access to this dataset. In GitHub repository Settings > Secrets and variables > Actions, set the repository secret `HF_TOKEN`. Never commit or paste the token. The dataset repository must already exist. The workflow uses a concurrency group to prevent overlapping sync runs.

## Using the data

Install `datasets` and load a named configuration from [the Hugging Face dataset](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets). Configuration names, source-specific licenses, counts and review caveats are documented in the root card. Pin a Hugging Face commit revision for reproducible experiments.

Each release manifest records the source revision/hash, transformation details, counts and output shard hashes. Remote hash checks confirm file identity after upload; they do not establish linguistic correctness, legal advice, privacy, completeness or human review. See [data architecture](DATA_ARCHITECTURE.md) and [license policy](LICENSE_POLICY.md).

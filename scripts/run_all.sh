#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python scripts/01_fetch_sources.py "$@"

# Later numbered stages are intentionally gated until their implementations,
# source rights, and validation reports are approved.
for stage in \
  scripts/02_extract_text.py \
  scripts/03_normalize.py \
  scripts/04_quality_filter.py \
  scripts/05_dedup_minhash.py \
  scripts/06_tag_script.py \
  scripts/07_package_release.py \
  scripts/08_generate_datacard.py
do
  if [[ ! -f "$stage" ]]; then
    printf 'Stopped after Stage A: %s is not implemented yet.\n' "$stage"
    exit 2
  fi
  python "$stage"
done
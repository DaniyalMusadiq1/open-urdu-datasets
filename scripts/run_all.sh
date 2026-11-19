#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PHASE2_ROOT="${PHASE2_RELEASE_ROOT:-$ROOT/artifacts/phase2-release}"
KLAM_ROOT="$PHASE2_ROOT/klam-original"

if [[ -e "$PHASE2_ROOT" ]]; then
  printf 'Build output already exists: %s\n' "$PHASE2_ROOT" >&2
  printf 'Choose a new PHASE2_RELEASE_ROOT; this runner never overwrites output.\n' >&2
  exit 2
fi
export PHASE2_RELEASE_ROOT="$PHASE2_ROOT"

# The source-specific pinned importers perform fetching, extraction,
# normalization, language routing, and input validation.
python scripts/build_phase2_release.py

# Combine rights-cleared inputs into the single Klam record schema and retain
# row-level source/license metadata.
python scripts/build_klam_release.py \
  --output "$KLAM_ROOT" \
  --phase2-root "$PHASE2_ROOT" \
  --cleanup-phase2-inputs

python scripts/validate_klam_release.py "$KLAM_ROOT"

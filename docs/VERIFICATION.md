# Klam verification levels

Verification describes checks completed on records. An upstream label such as “verified” does not itself mean Klam’s text was reviewed by a native speaker.

| Level | Meaning | Evidence required |
|---|---|---|
| unverified | Default for records without completed checks | Keep source provenance and state what has not been reviewed |
| mechanical | Automated format, rights-metadata, script/language, privacy-triage, and dedup checks passed | Tool versions, thresholds, source revision, and report |
| human_reviewed | A reviewer sampled and checked the stated records | Reviewer ID, date, record scope, method, and outcome |
| native_speaker_verified | A qualified Urdu/Roman Urdu speaker reviewed the stated script and scope | Reviewer ID, date, script, sample method, scope, and outcome; cross-script claims require review of both scripts |

Mechanical checks are not proof of fluency, factual accuracy, full privacy safety, or native-speaker quality. Do not upgrade a whole source from a small sample without recording the sampling scope.

## Current counts

| Level | Records | Status |
|---|---:|---|
| unverified | Pending the expanded Klam build manifest | All new rows default to unverified/unreviewed |
| mechanical | Not measured for the full release | Do not infer from upstream filtering |
| human_reviewed | 0 reported in the current processed-corpora catalog | No reviewer evidence recorded |
| native_speaker_verified | 0 | Native reviewer work is pending |

## Reviewer log

| Reviewer ID | Date | Script | Source / record scope | Method and sample size | Outcome |
|---|---|---|---|---:|---|
|  |  |  |  |  |  |

Never add a reviewer name, date, count, or result unless the reviewer supplied it. Use anonymous reviewer IDs if preferred.
---
language:
- ur
license: cc-by-4.0
task_categories:
- text-classification
pretty_name: UCI Roman Urdu sentiment records (filtered release)
---

# UCI Roman Urdu sentiment records

This release combines eligible records from the UCI Roman Urdu Data Set (UCI
458) and RUSAD (UCI 854). The upstream UCI pages identify the datasets as CC BY
4.0. Original source labels are preserved in `source_label`; `sentiment` is a
lowercase copy of that label, not a relabeling or independent annotation.

All records are `review_status: unreviewed`. No claim of native-speaker
verification or label correctness is made. The sources describe collected
comments and reviews, but do not provide original per-post URLs or authors for
each row. Stable UCI dataset identifiers and 1-based source row numbers are
preserved as the available record provenance.

The manifest records source archive/member hashes, row-level rejection counts,
retained label distributions, exact duplicate counts, whitespace-delimited
tokens, and compressed shard checksums. Records shorter than 20 characters,
malformed rows, labels outside the publisher's documented classes, exact
duplicates, and rows matching email, phone-like, URL, or @handle patterns were
excluded. These pattern checks are limited triage and are not a guarantee that
the text contains no personal data.

## Attribution

- Zareen Sharf, *Roman Urdu Data Set*, UCI Machine Learning Repository,
  DOI: 10.24432/C58325.
- Khawar Mehmood, Daryl Essam, and Muhammad Kamran Malik, *Roman Urdu
  Sentiment Analysis Dataset (RUSAD)*, UCI Machine Learning Repository,
  DOI: 10.24432/C59046.

See `SOURCES.md` and `LICENSE` for source URLs and license notices. The source
label sets differ (three classes in UCI 458; positive/negative in RUSAD); do
not infer that their annotation schemes are directly equivalent.

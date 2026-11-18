# Source and processing record

Both source pages declare CC BY 4.0. The release records the dataset-level
source and source row because the original comment/review URLs are not included
by UCI.

| Dataset | Source and download | Version/citation | Source archive SHA-256 |
|---|---|---|---|
| UCI 458 | https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set | DOI 10.24432/C58325 | `78e7cd1d7b0dc8e960a52c9151fc3114c70a3809111d3421581bbad931a6f5a8` |
| UCI 854 (RUSAD) | https://archive.ics.uci.edu/dataset/854/roman+urdu+sentiment+analysis+dataset+(rusad) | DOI 10.24432/C59046 | `4fe3618d9353abe27fb94414f2741b8ed634a4467cec056be4a10732ec9a0be5` |

License statements: https://archive.ics.uci.edu/dataset/458/roman+urdu+data+set#license
and https://archive.ics.uci.edu/dataset/854/roman+urdu+sentiment+analysis+dataset+(rusad)#license.
Both pages say that sharing and adaptation are allowed with attribution under
CC BY 4.0. Attribution is included in the dataset card and per-record `source_doi`.

Rebuild from the original archives:

```sh
python scripts/import_uci_roman_urdu.py \
  --uci458 path/to/uci458.zip --uci854 path/to/uci854.zip \
  --out datasets/classification/uci-roman-urdu-sentiment
python scripts/validate_uci_roman_urdu.py
```

The importer fails closed on archive/member checksum drift. It preserves
source text and valid source labels, removes malformed/out-of-domain/short
records, exact text duplicates, and rows matching documented contact patterns.
Deduplication is exact after NFC and whitespace canonicalization; near-duplicates
are not claimed to be detected. The importer also scans existing published text
fields for exact duplicates. These social comments/reviews may contain harmful
or identifying text not caught by simple patterns.

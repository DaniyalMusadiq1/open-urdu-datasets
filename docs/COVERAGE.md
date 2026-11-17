# Coverage and research gaps

The draft contains 28 discovery entries, including one embeddings resource. It does not meet the target of 25 fully verified datasets. No upstream full dataset has been marked verified. A derived sample is tracked separately so it cannot inflate independent-dataset counts.

## Sources inspected

Original Makhzan and awesome-urdu pages; publisher dataset cards on Hugging Face; UCI API and dataset pages; Dakshina's official archive member; OPUS-100 publisher card; Tatoeba downloads and usage guidance; FLORES and XNLI pages; Wikipedia dump index; CC-100, OSCAR and mC4 cards; Mozilla Common Voice's current official listing; LDC catalog; IIIT OCR; and a Zenodo UPTI listing through web fetch. ACL Anthology supplies the Dakshina publication link. Some cards moved from CohereForAI to CohereLabs; canonical IDs are retained in the catalog.

Kaggle's Roman Urdu page returned no readable text through web fetch; no independent entry or license claim was created from it. ELRA's catalog page was inaccessible through web fetch. Broad academic paper searches returned discovery leads, not validated data distributions. arXiv abstracts and awesome lists are leads, not evidence of redistribution rights.

## Included task coverage

Discovery entries cover edited corpora, Roman Urdu sentiment, transliteration vocabulary, sentences, Urdu–English parallel text, QA/reading comprehension, instruction/conversation mixtures, NER, POS/tokenization/morphology/dependency parsing, classification, NLI, news/summarization, ASR, printed OCR, document layout and pretrained vectors (catalog only). Native Arabic-script Urdu is not necessarily rendered in Nastaliq: corpus Unicode characters do not prescribe a font.

## Unfilled areas

Stopwords/dictionaries with English meanings, emotion, sarcasm, hate speech, fake news, standalone lemmatization, paraphrase, spelling correction, deliberately annotated code-mixing, education, legal/government, TTS, speaker-identification benchmarks and handwriting OCR still need dataset-level source/license verification. No record-level education or legal advice data is hosted. Books, poetry and religious translations require particularly careful rights evidence.

Related languages are optional and are not counted as Urdu: Dakshina includes Sindhi and Gurmukhi Punjabi; neither is automatically Shahmukhi Punjabi. Pashto and Saraiki discovery remains future work. Do not infer a resource's script from its region or language name.

## Rejected assumptions

- IndicQA's inspected language list did not include Urdu; excluded.
- IndicXParaphrase's inspected files did not show an Urdu component; excluded pending evidence.
- A missing/401 HF endpoint was not treated as proof a dataset exists or a reason to request permissions.
- CC0 packaging in OSCAR does not establish a blanket right to republish source web text.
- UD Urdu UDTB and XNLI are NC; XL-Sum is NC/research-only; all remain link-only.
- Makhzan raw text is not redistributed.
- Aya Dataset and Aya Collection overlap; sizes must not be added as unique data.
- A Zenodo UPTI page describes text ground truth rather than the complete image collection; not added merely to inflate coverage.

## Next contributions

Resolve source-specific downloads and license texts; independently count and checksum explicitly scoped distributions; review PII/toxicity and attribution; then promote status with evidence. Prioritize a native Urdu reviewer for romanizations, spellings and the Urdu README. English glosses/POS/examples need reviewed contributions with explicit licensing; they remain null in the vocabulary sample. Urdu–English pairs remain a separate unmet hosting task; no translated pairs are invented to fill it.

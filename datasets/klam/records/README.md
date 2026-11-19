# Klam record intake

Klam accepts records authored for Klam, contributor submissions with explicit permission, and public-domain material whose status is evidenced for the exact work and edition.

Do not put text here until its source has an approved entry in [sources.json](../sources.json). The current registry is empty, so **no records are approved for publication yet**.

Add one UTF-8 JSON object per line in a `.jsonl` file. Each input row must contain:

```json
{"text":"<source text>","source_id":"<approved source ID>","source_record_id":"<stable source record ID>","source_locator":"<page, paragraph, or other locator>","script":"Arabic","task":"text","label":"","split":"","review_status":"unreviewed"}
```

Replace every placeholder with real evidence. Never include sample or AI-generated text as dataset content. Keep the original text unchanged. The build process creates stable IDs and fills the approved source version, rights, and attribution fields from the registry.

For public-domain material, the source entry must identify the exact work and edition and link to rights evidence. A public download page alone is not proof of public-domain status. Keep scans/OCR drafts and unclear-rights books out of this folder until cleared.

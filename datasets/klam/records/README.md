# Klam record intake

Klam accepts original records, contributor submissions with explicit permission, CC0-dedicated source texts, and public-domain material whose status is evidenced for the exact work and edition.

Do not put text here until its source has an approved entry in [sources.json](../sources.json). The current starter corpus has **307 Ghalib poetry records** from a CC0-dedicated transcription. All are marked `unreviewed`; none is marked human reviewed.

Add one UTF-8 JSON object per line in a `.jsonl` or `.jsonl.gz` file. Each input row must contain:

```json
{"title":"<record title>","text":"<source text>","source_id":"<approved source ID>","source_record_id":"<stable source record ID>","source_locator":"<page, paragraph, or other locator>","script":"Arabic","task":"text","label":"","split":"","review_status":"unreviewed"}
```

Replace every placeholder with real evidence. Never include sample or AI-generated text as dataset content. Keep the source text unchanged except for documented markup removal. Klam output carries the title, source version, rights, and review fields. The build process creates stable IDs and fills the approved source version, rights, and attribution fields from the registry.

For public-domain material, the source entry must identify the exact work and edition and link to rights evidence. For CC0 material, pin the exact source commit and link to the explicit dedication. A public download page alone is not proof of rights. Keep scans/OCR drafts and unclear-rights books out until cleared.

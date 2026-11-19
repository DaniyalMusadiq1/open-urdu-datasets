# Dataset licensing and ethics policy

Code and original documentation are MIT. Each dataset retains its own license; MIT does not license third-party data.

## Klam core collection

The Klam core is built only from original content, contributor submissions with explicit permission, CC0-dedicated source texts, or public-domain works whose status is verified for the exact work and edition. Previously published third-party corpus packages remain separate reference material and are not inputs to the Klam core. Do not import another dataset into Klam.

Original and contributor-submitted text must have explicit redistribution permission under CC BY 4.0. CC0-dedicated source texts retain the exact CC0 evidence and version. Public-domain records keep their public-domain status and require exact rights evidence and attribution. Record the basis, evidence, source version, and attribution in `datasets/klam/sources.json`; a maintainer must approve each source before its records can enter a release. If rights are unclear, exclude the text until they are resolved.

## Hosting decision

1. Identify the original publisher and version. Public download availability is not redistribution permission.
2. Read the dataset-specific license and original-source conditions. Record evidence URL, date and applicable component.
3. Permit public domain, CC0, CC-BY, CC-BY-SA or ODbL only when the relevant data is explicitly covered and redistribution is allowed. Other proposed equivalent licenses need a documented maintainer decision before hosting; they are not automatically accepted by tools.
4. NC, ND, research-only, unspecified or ToS-restricted data is catalog-only. Keep mixed-license compilations link-only until rights are resolved per component. Dataset packaging licenses do not necessarily cover underlying crawled content. OSCAR and web corpora require particular care.
5. News, poetry, books, religious translations and similar copyright-sensitive text stay link-only without explicit coverage. Do not download Makhzan raw content for redistribution.
6. Preserve attribution and share-alike obligations within each dataset directory. Provide the license text, source URLs, version, author attribution, changes made and checksum manifest. No relicensing.
7. Check text, metadata, usernames, emails, phone numbers and audio for privacy concerns. Machine pattern scans are triage, not proof of PII absence. Speaker IDs and voice recordings can be identifying. Do not host private data.

`hosted: false` does not mean redistribution is forbidden: the entry may simply be large, unverified, awaiting review, or excluded by project scope. Record the actual decision.

## Takedown and correction

Open a `Rights or privacy concern` issue with the affected dataset ID and a non-sensitive description. Do not include the harmful record itself. Use GitHub's reporting channels for private information. The maintainer should assess promptly, suspend affected distributions when appropriate, investigate provenance and rights, and record the outcome without exposing personal information. Requests to delete or overwrite files require maintainer approval. There is no guaranteed response SLA or configured private project inbox yet.

Removal from the current tree does not erase Git history, forks, caches or previous downloads. A confirmed sensitive leak may require coordinated history cleanup and platform support, separately approved. Avoid placing questionable content in Git in the first place.

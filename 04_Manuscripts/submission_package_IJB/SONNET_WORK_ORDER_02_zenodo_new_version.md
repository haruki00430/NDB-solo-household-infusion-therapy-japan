# SONNET WORK ORDER 02: Prepare and publish a new Zenodo version

## Preconditions

Do not begin until:

- Work Order 01 has passed independent numerical and provenance review;
- the revised manuscript, response letter, code, data, tables, and figures are final;
- the author has identified the correct existing Zenodo record and authenticated account;
- the author has explicitly approved creating a new version draft.

Publishing the draft is a separate irreversible gate and requires a second explicit author approval.

## Objective

Create a new version of the existing Zenodo record for the major revision. Do not overwrite the prior version. Preserve the prior version and its version-specific DOI.

## Procedure

1. Open the correct existing Zenodo record and confirm ownership, title, creators, concept DOI, version DOI, and current files.
2. Export or capture the current metadata and file inventory for audit.
3. Click/create `New version` and import the prior files into the draft.
4. Replace or add only the finalized revision artifacts.
5. Remove obsolete files from the new draft only when their replacements are present and verified.
6. Upload at minimum:
   - README with exact reproduction command;
   - source manifest with URLs and SHA-256 hashes;
   - raw public-source data where redistribution is permitted, otherwise download scripts and clear instructions;
   - derived 47-prefecture analytic dataset;
   - complete scripts;
   - locked environment/package specification;
   - machine-readable model results;
   - source data for every figure/table;
   - revised supplementary materials.
7. Scan all files for secrets, local usernames, absolute local paths, access tokens, private data, and temporary files.
8. Update metadata: title, description, version, publication date, keywords, related identifiers, licenses, creators, and contributor roles.
9. Reserve or obtain the new version-specific DOI while the record is still a draft, if the interface supports it.
10. Update the README, citation file, manuscript Data Availability statement, and response letter with the new version DOI. Distinguish it from the concept DOI.
11. Run a final file-by-file checksum and metadata audit.
12. Stop and present the complete draft inventory, new DOI, and proposed metadata to the author. Do not publish yet.
13. Publish only after the author explicitly states that the reviewed draft should be published.
14. After publication, verify DOI resolution, file downloads, checksums, version links, license, and citation metadata.

## Prohibited actions

- Do not delete the old record.
- Do not edit the files of the published old version as a substitute for versioning.
- Do not expose access tokens in logs, code, screenshots, or shell history.
- Do not publish a draft with placeholder URLs such as `XXX`.
- Do not publish if the manuscript DOI and the Zenodo version DOI disagree.
- Do not force-push or rewrite Git history.

## Final report

Return:

- old version DOI;
- concept DOI;
- new version DOI;
- published/unpublished status;
- final metadata;
- complete file list with size and SHA-256;
- DOI-resolution and download verification results;
- exact Data Availability wording used in the revised manuscript.


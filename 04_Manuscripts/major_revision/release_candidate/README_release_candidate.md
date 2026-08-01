# Release-candidate materials for Zenodo new version (NOT published)

This folder contains materials prepared for a future Zenodo new-version publication,
per `SONNET_WORK_ORDER_02_zenodo_new_version.md`. **Nothing in this folder has been
published or pushed anywhere.** Publication requires a separate, explicit author
approval gate after the manuscript itself is finalized (see
`SONNET_WORK_ORDER_02` preconditions).

## Contents

- `zenodo_v2_file_inventory.csv` — definitive list of every file proposed for
  inclusion in the new Zenodo version, with category, size, and SHA-256 hash
  (87 files: ETL scripts, analysis scripts, derived/interim data, results,
  reports, and final manuscript-package files; raw official source archives
  referenced by folder, with per-file hashes in `reports/major_revision/source_manifest.csv`).
- `requirements_lock_20260801.txt` — frozen Python environment (`pip freeze`)
  at the time this release candidate was assembled.
- `CITATION.cff.draft` — draft citation metadata for the new version, including
  an explicit `[[ZENODO_VERSION_DOI_PENDING]]` placeholder that must be replaced
  with the real reserved DOI only after the author approves publication.

## What is NOT included here

Large raw data files (`02_Data/raw/major_revision/`) are not duplicated into this
folder; they remain in place in the working repository and are referenced by path
and hash in `zenodo_v2_file_inventory.csv` and `source_manifest.csv`. The actual
Zenodo upload step (Work Order 02) will pull directly from the working repository.

## Next steps (require author approval)

1. Author reviews `zenodo_v2_file_inventory.csv` and confirms scope.
2. Author confirms the manuscript package in `04_Manuscripts/major_revision/final/`
   is final.
3. Only then does Work Order 02 proceed: open the existing Zenodo record, create
   a new version draft, upload the approved file set, reserve the new version DOI,
   and present the complete draft for a final explicit publish approval.

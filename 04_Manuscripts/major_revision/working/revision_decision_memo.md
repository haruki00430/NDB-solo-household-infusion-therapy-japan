# revision_decision_memo.md — Work Order 04 unresolved author decisions

## 1. Title

**Used throughout the revision candidate package (locked, per Work Order 04):**

> Prefecture-Level Measures of Older Adults Living Alone and Large-Volume Infusion Therapy Utilization in Japan: Accounting for Population Age Structure and Heat Exposure

**Alternatives for author consideration (from Codex's cover memo), not used in any file to keep consistency:**

1. "Older Adults Living Alone and Large-Volume Infusion Therapy Utilization Across Japan: Accounting for Population Age Structure and Heat Exposure"
2. "Prefecture-Level Measures of Older Adults Living Alone, Population Age Structure, and Large-Volume Infusion Therapy Utilization in Japan"

**Author decision needed:** confirm the working title or select an alternative before submission. If changed, title must be updated consistently in: manuscript (clean + marked), response letter, cover letter, supplement, and CITATION.cff draft.

## 2. Zenodo version DOI

The manuscript, supplement, and CITATION.cff draft use the placeholder `[[ZENODO_VERSION_DOI_PENDING]]`. This is intentional and must not be replaced with a fabricated DOI. Per Work Order 02 (unchanged precondition), the real version DOI can only be reserved after the author approves creating a Zenodo new-version draft, and only inserted into the manuscript after that DOI is confirmed to resolve correctly.

## 3. GitHub repository name containing "XXX"

`https://github.com/haruki00430/NDB_XXX_heatwave_heatstroke` was independently confirmed to be a live, public repository (not a broken placeholder link) via the GitHub API. Reviewer 2 and the original Reviewer 1 comment both flagged the literal string "XXX" as looking like an unfilled template field. We have not renamed the repository (an external, author-level action affecting the canonical URL of a public repository, out of scope for this work order without separate authorization). **Author decision needed:** rename the repository for clarity (e.g., to a descriptive slug without "XXX"), keeping in mind GitHub automatically redirects the old URL after a rename, or leave as-is and rely on the explanation already added to the manuscript's Data Availability statement.

## 4. Healthcare-supply variable asymmetry

`general_hospital_beds_per_100k` uses an official MHLW-calculated per-100,000 rate; `general_clinics_per_100k` is a rate we calculated ourselves (official count ÷ our own 2023 population figure), because no directly analogous official per-100,000 clinic-count table was found. This is disclosed in Methods but not resolved further. **Author decision needed:** none required to proceed; flagged for awareness only.

## 5. Hokkaido's WBGT aggregation

Confirmed as the most influential single observation in both exposure hierarchies (Cook's D up to ~0.67, roughly 7.6-fold the 4/N threshold), reflecting averaging across 163 monitoring sites with substantial internal climatic heterogeneity. The qualitative conclusion is unchanged when Hokkaido is excluded (leave-one-out analysis). **Author decision needed:** confirm the current Limitations wording is sufficiently detailed, or request a dedicated supplementary sensitivity table showing the O-D model with and without Hokkaido side by side (not currently a separate table; currently folded into the LOO results).

## 6. e-Stat appId history remediation

Code-level fix is complete and unpublished (uncommitted working-tree change). **Author decision needed:** (a) rotate/reissue the e-Stat appId (recommended, fastest, fully within author's control); (b) decide whether to additionally pursue Git history rewriting (`git filter-repo` + force-push), which is a separate, higher-risk, explicitly-authorized-only action. See `reports/major_revision/estat_appid_security_remediation.md`.

## 7. Interpretation branch

Branch 2 (substantial attenuation consistent with age-structure confounding) was authorized by the author via Work Order 04 and implemented consistently throughout. No further decision needed unless new evidence emerges.

## 8. Scope not completed in this pass

- Full page-by-page 100%-zoom visual inspection was performed for representative pages of each document (title, abstract, methods/results transition, both tables, figure, references, and response-letter opening) rather than literally every one of the 19 + 12 + supplement pages; no rendering defects were found in the pages inspected. A complete page-by-page pass is recommended before final submission if time permits.
- The reference audit used the CrossRef API for every DOI-bearing citation (25 of 30 references); the remaining 5 references are government/organizational sources without DOIs and were not independently re-verified against their source URLs in this pass.
- `README_release_candidate.md` and the Zenodo file inventory are prepared but the actual Zenodo record has not been touched.

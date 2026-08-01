# SONNET WORK ORDER 04: Branch 2 manuscript revision and point-by-point response package

## Authorization and fixed scientific direction

The author has selected **Branch 2: substantial attenuation consistent with confounding by population age structure**.

This strategic decision is fixed for this work order. Do not try to recover the submitted positive conclusion by selecting alternative models, outcomes, thresholds, exclusions, or wording.

The central finding is:

> The unadjusted association was substantially attenuated after adjustment for prefectural population age structure and was no longer statistically significant. Estimates were further attenuated in models that included healthcare supply and heat exposure.

The central methodological interpretation is:

> The submitted ecological association was sensitive to population age structure and exposure denominator choice.

Do not write:

- `no association exists`;
- `ageing completely explained the association`;
- `population ageing caused the original association`;
- `living alone has no effect`;
- any individual-level causal interpretation.

Use instead:

- `no evidence of an independent prefecture-level association`;
- `the association was not robust to adjustment`;
- `the estimate was substantially attenuated`;
- `the adjusted confidence interval remained compatible with both a modest positive association and little or no association` when discussing O-B.

## Scope

Create a complete revision candidate package:

1. revised clean manuscript;
2. separately marked-up manuscript;
3. point-by-point response to the editor and both reviewers;
4. revised supplementary material;
5. final publication tables and figures;
6. numerical, citation, and claim-traceability audits;
7. local release-candidate files for later GitHub/Zenodo work.

Do not push to GitHub, create or edit a Zenodo version, contact the journal, or upload to the submission system. External publication remains a later author-approved gate.

## Canonical working environment

Continue in the canonical project containing:

- `02_Data/`
- `03_Analysis/`
- `04_Manuscripts/submission_package_IJB/`
- `reports/major_revision/`

The project was previously identified as `NDB_Research_Hub/projects/NDB_XXX_heatwave_heatstroke/`. Resolve and record its actual absolute path at runtime.

Preserve the originally submitted DOCX byte-for-byte. Work on copies under a new directory such as:

- `04_Manuscripts/major_revision/working/`
- `04_Manuscripts/major_revision/final/`

Record the starting Git commit and final diff/status. Do not commit or push unless separately instructed.

## Evidence hierarchy

Use the following as controlling analysis evidence:

1. `reports/major_revision/original_exposure_additional_analysis.md`;
2. `reports/major_revision/g004_public_data_availability_audit.md`;
3. `03_Analysis/results/major_revision/original_exposure_*.csv`;
4. `03_Analysis/results/major_revision/original_vs_new_exposure_comparison.csv`;
5. Work Order 01 results for the alternative exposure, WBGT metrics, comparison outcome, and diagnostics;
6. the original manuscript and its 35 embedded Reviewer 1 comments;
7. the editor and Reviewer 2 decision letter.

If any narrative document conflicts with a machine-readable result, stop and resolve the discrepancy from code and source data before drafting.

## Required pre-drafting corrections

Complete these items before writing the revised manuscript.

### 1. Fill the missing standardized coefficient for O-C

The Report 02 table contains `—` for the standardized original-exposure coefficient in O-C. Recompute it by standardizing the variables and refitting the exact O-C model with HC3 inference.

Add the value and HC3 95% CI to all relevant result tables. Do not infer or hand-calculate it from rounded published values.

### 2. Verify cumulative model formulas

Confirm from code and design matrices that the models are exactly:

- O-A: original exposure.
- O-B: original exposure + ageing rate.
- O-C: original exposure + ageing rate + general hospital beds per 100,000.
- O-D: original exposure + ageing rate + general hospital beds per 100,000 + days with daily maximum WBGT >=28.

Save the exact formulas and design-matrix column names in the audit report.

### 3. Correct the reproduction language

The submitted 2020-denominator point estimate, beta=723.37, was exactly reproduced. The submitted inferential analysis was not exactly reproduced because the revision uses HC3 robust standard errors.

Use:

> The original point estimate was exactly reproduced using the submitted 2020 population denominator. Inferential statistics differed because the revised analysis used HC3 heteroskedasticity-robust standard errors.

Do not use:

> The original analysis was exactly reproduced.

### 4. Resolve internal issue tracking

Consolidate `reports/major_revision/issues_for_author.md` so that old and current statements do not conflict.

At minimum:

- mark the prior `G004 unconfirmed` item as `RESOLVED: NOT_PUBLICLY_AVAILABLE` and link the definitive audit;
- mark the Branch-selection item as `RESOLVED: Branch 2 selected by author`;
- retain genuinely unresolved items only;
- preserve the historical text in a dated archive or changelog rather than silently deleting it.

### 5. Security review of the exposed e-Stat appId

Treat the appId found in public Git history as compromised.

- Identify affected tracked files and commits without printing the full key in reports or terminal summaries.
- Mask the identifier, showing no more than the first and last four characters.
- Ensure the current working tree reads the replacement key from an environment variable or ignored `.env` file.
- Add or update `.env.example` with a placeholder only.
- Confirm `.env` and secrets are ignored.
- Create `reports/major_revision/estat_appid_security_remediation.md` describing what the author must revoke/reissue through e-Stat.
- Do not rewrite Git history, force-push, revoke credentials, or create a replacement credential without separate explicit author authorization and authenticated access.

The final report must state clearly that removing the key from the latest files does not remove it from Git history.

## Locked analysis presentation

### Primary exposure

Retain the prespecified submitted exposure as the primary exposure:

> Percentage of all households consisting of one person aged 65 years or older.

Describe it as a prefecture-level burden measure relative to all households. Do not call it a direct measure of individual social isolation.

### Alternative exposure

Present the reconstructed exposure as an `alternative-denominator analysis` or `exposure-definition sensitivity analysis`:

> Percentage of the population aged 65 years or older living alone.

State that the two variables estimate different concepts. Do not label either one as the uniquely correct exposure.

### Outcome

Use:

> large-volume infusion therapy utilization

or, where maximum technical precision is needed:

> prefecture-level claims rate for G004 large-volume intravenous infusion procedures (>=500 mL) per 100,000 population

Do not use `dehydration-related healthcare utilization` as the principal outcome name. G004 is not diagnosis-specific.

### Outcome denominator

- Primary: 2023 population estimate, temporally aligned with FY2023 NDB claims.
- Sensitivity: submitted 2020 population denominator.

Explain this before presenting model results.

### Main results that must remain consistent

Use unrounded machine-readable results for calculations, then round consistently for presentation.

- O-A: beta=656.22; HC3 95% CI 326.9 to 985.6; standardized beta=0.521; p<0.001.
- O-B: beta=306.14; HC3 95% CI -71.3 to 683.5; standardized beta=0.243; p=0.112.
- O-C: beta=94.09; HC3 95% CI -302.4 to 490.6; p=0.642; standardized beta and CI must be filled from code.
- O-D: beta=-9.41; HC3 95% CI -493.9 to 475.1; standardized beta=-0.007; p=0.970.
- Descriptive O-A to O-B attenuation: 53.3%.
- Original-exposure partial R-squared: 0.272, 0.056, 0.004, and 0.00004 across O-A to O-D.
- Alternative exposure: unadjusted r approximately 0.0003 and no evidence of association in unadjusted or adjusted models.

Do not round confidence-interval bounds in one document differently from another.

### WBGT findings

- Retain WBGT >=28 days as the prespecified primary heat adjustment variable.
- Treat WBGT >=31 days, >=33 days, and cumulative excess above 28 as sensitivity analyses.
- WBGT >=33 days: nominal p=0.018 and BH-FDR-adjusted p=0.055.

Use no more than a restrained sentence in the main Results/Discussion:

> Days with WBGT >=33 C showed a nominal association with infusion utilization, but the association did not remain statistically significant after correction for multiple comparisons.

Do not promote WBGT >=33 to the primary heat metric after seeing the result. Do not write `significant association` without the multiplicity qualification.

### G004 public-data limitation

Use the definitive audit finding:

> We independently reviewed the complete file inventory and the four publicly available G-injection tables in the Tenth NDB Open Data release. Prefecture-by-age cross-tabulated counts for G004 were not publicly available. We therefore could not construct an age-specific or age-standardized prefectural outcome.

Ensure the Methods or Limitations explain the separate marginal-table structure and do not imply that the authors simply failed to find the data.

## Provisional revised title

Use this as the working title:

> Prefecture-Level Measures of Older Adults Living Alone and Large-Volume Infusion Therapy Utilization in Japan: Accounting for Population Age Structure and Heat Exposure

Also include two shorter alternatives in the author decision memo, but use only the working title throughout the revision candidate so filenames, headers, and response text remain consistent.

Remove completely:

> Are Heat-Health Systems Socially Blind?

## Revised research question

Frame the study around:

> Do prefecture-level measures of older adults living alone identify large-volume infusion therapy utilization beyond population age structure, healthcare supply, and summer heat exposure?

The answer should be expressed as:

> The measures did not show a robust independent association after these factors were considered.

## Manuscript rewriting requirements

This is a substantive scientific rewrite, not a light copyedit. Preserve valid methods, data-source descriptions, author information, journal formatting, and references where possible, but rewrite every claim affected by the reanalysis.

### Title and Abstract

The Abstract must report both the unadjusted and adjusted interpretation.

Use this conclusion as a drafting basis, checking every value against the final tables:

> In unadjusted analyses, the proportion of all households consisting of an older adult living alone was associated with large-volume infusion therapy utilization. The estimate was attenuated by 53% and was no longer statistically significant after adjustment for prefectural population age structure. It approached zero after additional adjustment for healthcare supply and summer heat exposure. An alternative measure using the older population as the denominator was not associated with infusion utilization. These findings indicate that prefecture-level living-alone indicators should not be interpreted as independent heat-vulnerability markers without careful consideration of population age structure and denominator choice.

Avoid presenting `statistically significant/non-significant` as the only basis for interpretation. Include effect estimates and confidence intervals within the journal's abstract word limit.

### Introduction

Rewrite the rationale so it does not presuppose that living alone is associated with G004 utilization.

- Distinguish `living alone` from `social isolation`.
- Explain why prefecture-level living-arrangement measures may reflect both social-care burden and population age composition.
- Explain why denominator choice matters.
- State the revised neutral research question.
- Retain relevant heat-health literature, but do not claim that warning systems are socially blind.

### Materials and methods

Explicitly document:

- prefecture-level ecological design, N=47;
- FY2023 NDB period and 2023 population denominator;
- exact G004 definition and non-specificity;
- original and alternative exposure formulas;
- ageing-rate definition and year;
- healthcare-supply definitions and years;
- official daily-maximum WBGT construction and aggregation;
- exact cumulative O-A through O-D formulas;
- HC3 robust inference;
- standardized coefficient calculation;
- SSE-based partial R-squared definition;
- VIF and AICc definitions;
- nonlinearity tests;
- metropolitan, influence, LOO, WLS, log-outcome, clinic, legacy-denominator, and heat-metric sensitivity analyses;
- BH-FDR scope;
- G004 age-by-prefecture unavailability.

Do not use multicollinearity as a reason to avoid adjustment.

### Results

Present results in this order:

1. data and exposure definitions;
2. unadjusted O-A;
3. direct age-adjusted O-B and 53.3% descriptive attenuation;
4. O-C and O-D;
5. alternative-denominator exposure analysis;
6. sensitivity, influence, urban, and nonlinearity analyses;
7. exploratory WBGT findings;
8. comparison-outcome analysis, if retained.

Do not describe O-B as proving no positive association. Its CI remains wide. State that statistical evidence was lost and the estimate was substantially attenuated.

### Discussion

Organize the Discussion around:

1. principal result: sensitivity to age structure and denominator;
2. distinction between population burden and within-older-population prevalence;
3. why ecological social indicators can proxy demographic composition;
4. comparison with prior living-alone/heat-vulnerability literature without claiming direct contradiction at the individual level;
5. restrained interpretation of WBGT findings;
6. implications for validation of social-vulnerability indicators before surveillance use;
7. strengths and limitations.

Required limitations include:

- ecological design and ecological fallacy;
- living alone is not equivalent to social isolation;
- G004 is not specific to dehydration or heat illness;
- no public prefecture-by-age G004 cross-tabulation;
- one fiscal year and the unusual 2023 summer;
- N=47 and wide adjusted confidence intervals;
- residual confounding and treatment-practice variation;
- prefecture-level climate averaging and within-prefecture heterogeneity;
- Hokkaido's 163-site aggregation and influence, with unchanged LOO conclusion;
- temporal differences among source years, explaining why the main variables were updated/aligned;
- air-conditioning ownership does not establish actual use.

Do not claim that the reanalysis is a `robust null` without also acknowledging limited precision.

### Conclusion

Remove recommendations to immediately integrate the living-alone indicator into warning systems.

Use a conclusion of this form:

> The initially observed prefecture-level association was substantially attenuated after accounting for population age structure and approached zero after additional adjustment for healthcare supply and heat exposure. The alternative living-alone measure was also not associated with infusion utilization. Prefecture-level living-arrangement indicators therefore require careful demographic validation before being interpreted as independent heat-vulnerability markers.

### Data availability and AI statement

- Correct the invalid GitHub URL containing `XXX` in the manuscript-facing link.
- Do not invent a Zenodo DOI or cite an unpublished draft. Use an internal, unmistakable placeholder such as `[[ZENODO_VERSION_DOI_PENDING]]` only in working files.
- Update the AI-use statement to reflect the actual use of Claude/Sonnet and Codex for scripting, document drafting, and quality control, while retaining author responsibility.
- Remove local paths, usernames, credentials, and internal work-order names from all submission files.

## Tables and figures

### Main Table 1

Revised descriptive statistics and variable definitions, including years and denominators.

### Main Table 2

O-A through O-D hierarchical models. Include:

- exact cumulative adjustment label;
- unstandardized beta and HC3 95% CI;
- standardized beta and HC3 95% CI;
- p-value;
- partial R-squared;
- adjusted R-squared;
- VIF or maximum VIF;
- AICc.

No missing O-C standardized coefficient is permitted.

### Main Figure 1

Coefficient plot for O-A through O-D with HC3 95% CIs and a zero reference line.

### Supplementary material

Include, as appropriate:

- legacy 2020-denominator hierarchy;
- alternative exposure models;
- clinic substitution and other sensitivity models;
- leave-one-prefecture-out results;
- influence diagnostics;
- quadratic and spline analyses;
- metropolitan exclusion;
- alternative WBGT metrics with FDR-adjusted p-values;
- comparison-outcome analysis renamed from negative control;
- source data for all figures.

Remove or demote the old median-split figure and analysis. It must not be a primary result.

Use restrained decimal precision appropriate for N=47. Do not report three decimal places for descriptive quantities unless necessary.

## Point-by-point response

Create a complete response covering:

- editor comments;
- Reviewer 1's general comment and all 35 embedded comments;
- Reviewer 2's six numbered comments and associated requests.

For every item use:

1. verbatim or accurately transcribed reviewer comment;
2. `Response:`;
3. exact analysis or textual action taken;
4. key result where relevant;
5. final manuscript page and line location.

The central Reviewer 2 response should include:

> We agree that population age structure was a central potential source of confounding. Our reanalysis materially changed the interpretation of the study. We therefore did not attempt to preserve the original conclusion. We retained the originally submitted exposure and added the prefectural ageing rate to the same model. The exposure coefficient changed from 656.22 (95% CI 326.9 to 985.6) to 306.14 (95% CI -71.3 to 683.5), a descriptive attenuation of 53.3%. It was further attenuated after adjustment for healthcare supply and WBGT. We also examined an alternative exposure using the older population as the denominator, which showed no evidence of association with infusion utilization. We rewrote the title, Abstract, Results, Discussion, and Conclusions to reflect these revised findings.

Use the G004 audit response:

> We independently reviewed the complete file inventory and the four publicly available G-injection tables in the Tenth NDB Open Data release. Prefecture-by-age cross-tabulated counts for G004 were not publicly available. We therefore could not construct an age-specific or age-standardized prefectural outcome.

Do not argue with Reviewer 2. Do not describe requested analyses as unnecessary.

For Reviewer 1, ensure the response addresses at minimum:

- prefecture-level design and N=47;
- abbreviation expansion;
- meaning of informal monitoring;
- single-year rationale and 2023 heat anomaly;
- replacement of `heatwave days` with `days with maximum temperature >=35 C` where applicable;
- linearity and lag limitations;
- air-conditioning ownership versus use;
- thirst and hydration in older adults;
- other indications for G004 infusion;
- correct DOI for Miyatake et al.: `10.1007/s12199-011-0221-2`;
- decimal precision;
- cautious interpretation of low R-squared and wide CIs.

## Reference and citation audit

- Verify every DOI against the publisher/Crossref/PubMed or another authoritative bibliographic source.
- Correct the Miyatake DOI.
- Verify official URLs for NDB, Census, population estimates, medical facilities, WBGT, JMA 2023 climate, and FDMA data.
- Ensure every new methodological or clinical statement has an appropriate citation.
- Remove unsupported or redundant citations.
- Create `reports/major_revision/reference_audit.csv` with original citation, verified citation, DOI/URL status, and action.

Do not leave a DOI merely because it resolves; verify that it belongs to the cited article.

## Clean and marked-up manuscript rules

### Clean manuscript

- No Word tracked changes.
- No comments.
- No highlights indicating revision.
- Continuous line numbers if required by the journal format.
- No internal placeholders except the explicitly flagged pending Zenodo DOI in the internal pre-release candidate.

### Marked-up manuscript

- Separate file.
- Prefer visible highlighting or another clearly explained markup method rather than tracked changes that can render unpredictably.
- Ensure deletions/replacements are understandable without exposing internal drafting notes.

### Response letter

- Produce DOCX and PDF.
- Page/line references must be generated from the final rendered clean manuscript, not guessed.

## Required deliverables

Under the canonical project, create at minimum:

- `04_Manuscripts/major_revision/final/manuscript_main_IJB_major_revision_clean.docx`
- `04_Manuscripts/major_revision/final/manuscript_main_IJB_major_revision_marked.docx`
- `04_Manuscripts/major_revision/final/response_to_reviewers.docx`
- `04_Manuscripts/major_revision/final/response_to_reviewers.pdf`
- `04_Manuscripts/major_revision/final/online_resource_1_revised.docx` or the correct journal-compatible supplement format.
- `04_Manuscripts/major_revision/final/cover_letter_revision.docx`
- `04_Manuscripts/major_revision/working/revision_decision_memo.md`
- `reports/major_revision/reviewer_comment_matrix.csv`
- `reports/major_revision/manuscript_number_audit.csv`
- `reports/major_revision/claim_traceability.csv`
- `reports/major_revision/reference_audit.csv`
- `reports/major_revision/estat_appid_security_remediation.md`
- `reports/major_revision/SONNET_REPORT_03_branch2_revision_package.md`
- a DOCX copy of SONNET REPORT 03.

Also prepare, without publishing:

- a release-candidate folder containing scripts, derived data, manifests, machine-readable results, figure source data, README, environment lockfile, and citation metadata for subsequent GitHub/Zenodo work;
- a definitive list of files to include in the Zenodo new version.

## Numerical and document QA

### Numerical audit

1. Generate all manuscript and response numbers programmatically from machine-readable results where feasible.
2. Extract numbers back from the final DOCX files and compare them with the authoritative CSV rows.
3. Fail if the manuscript, Abstract, tables, figures, supplement, and response letter disagree.
4. Confirm all O-model formulas are cumulative.
5. Confirm O-C standardized beta and CI are present everywhere required.
6. Confirm the 53.3% attenuation is labeled descriptive.
7. Confirm the 2023 and legacy 2020 denominator analyses are not mixed.

### Claim audit

Fail if any submission file contains:

- `socially blind`;
- `social isolation was the only ecological factor`;
- `social factors outperformed climatic indicators`;
- `six-fold stronger`;
- `dehydration-related healthcare utilization` as the primary G004 outcome label;
- `ageing completely explained`;
- `no association exists`;
- a claim that WBGT >=33 remained significant after FDR;
- the old invalid Miyatake DOI;
- a GitHub URL containing `XXX`;
- an invented or unverified Zenodo DOI;
- an exposed appId or secret;
- internal paths or work-order names.

### DOCX/PDF render QA

Render every final DOCX to PDF and page PNGs. Inspect every page at 100% zoom.

Check:

- title and author block;
- tables within margins;
- figures and captions;
- line numbers and page numbers;
- references and URLs;
- no clipped text, missing glyphs, overlaps, orphaned headings, or broken page breaks;
- marked-up changes remain legible;
- response-letter page/line citations match the clean manuscript.

If rendering is unavailable, stop before declaring the package final and report the missing dependency.

## Acceptance criteria

- Branch 2 is consistently implemented throughout all documents.
- The original exposure remains the primary exposure and O-A through O-D are cumulative.
- The alternative exposure is clearly labeled as a different estimand/sensitivity analysis.
- The principal outcome is described as large-volume infusion utilization, not heat-specific dehydration care.
- The Abstract reports unadjusted and adjusted findings with appropriate uncertainty.
- O-C standardized beta and HC3 CI are filled.
- The original point estimate, rather than the entire original analysis, is described as exactly reproduced.
- G004 age-by-prefecture unavailability is documented from the definitive audit.
- Reviewer 1's 35 comments and Reviewer 2's six comments are all mapped and answered.
- The clean manuscript has no tracked changes or comments.
- The response letter is available as a visually verified PDF.
- All numbers, references, claims, and page/line locations pass automated and visual QA.
- Internal issue tracking is consolidated.
- The exposed e-Stat appId is not present in new/current files, and the author has a clear revocation/history-remediation action list.
- No GitHub push, Zenodo change, journal contact, or submission upload occurs.

## Final report to Codex/author

Return only after all acceptance criteria that do not require external authorization are met. Report:

1. final title and word counts;
2. O-C standardized coefficient and CI;
3. paths to the clean manuscript, marked-up manuscript, response letter, supplement, tables, and figures;
4. reviewer-comment coverage count;
5. numerical and claim-audit results;
6. reference/DOI audit results;
7. render-QA result and final page/line numbering;
8. e-Stat credential-remediation status without revealing the credential;
9. unresolved author decisions, including title alternatives and Zenodo DOI insertion;
10. exact release-candidate file inventory for Work Order 02.


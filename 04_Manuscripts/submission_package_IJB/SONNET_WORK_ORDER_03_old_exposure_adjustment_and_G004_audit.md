# SONNET WORK ORDER 03: Direct adjustment of the submitted exposure and definitive G004 data-availability audit

## Purpose

Complete the one analysis that remains necessary to answer Reviewer 2 directly:

> include prefectural ageing rate alongside elderly solo household rate and show how the estimate changes

The submitted exposure must be retained while prefectural ageing is added to the same model. Replacing the submitted exposure with a newly defined exposure does not answer this request by itself.

This work order has two mandatory components:

1. definitively verify whether prefecture-by-age counts for G004 are publicly available in the Tenth NDB Open Data;
2. fit hierarchical adjustment models using the original submitted exposure.

Do not revise the manuscript, upload to GitHub, create or edit a Zenodo version, or publish any external artifact in this work order.

## Working environment

Continue in the canonical Git project that contains:

- `02_Data/raw/major_revision/`
- `02_Data/interim/major_revision/prefecture_analysis.csv`
- `03_Analysis/analysis/major_revision/`
- `03_Analysis/results/major_revision/`
- `reports/major_revision/`

The report identifies this project as `NDB_Research_Hub/projects/NDB_XXX_heatwave_heatstroke/`. Resolve and record its actual absolute path at runtime. Do not create a parallel analysis tree under the Codex conversation folder.

Preserve all Work Order 01 files. Add new scripts and outputs; do not overwrite prior result files unless the replacement is explicitly versioned and the change is documented.

## Part 1: Definitive audit of G004 age-by-prefecture availability

### Official source

Use the official Ministry of Health, Labour and Welfare Tenth NDB Open Data page and its linked explanatory and data files. Do not rely on the prior Codex or Sonnet conclusion, a search-result snippet, or the NDB visualization site alone.

Audit all relevant public structures:

1. the complete Tenth NDB public file list;
2. G injections - prefecture-level calculation counts;
3. G injections - sex/age-level calculation counts;
4. G injections - month-level calculation counts;
5. all medical-procedure prefecture-by-sex/age cross tables;
6. explanatory documents describing which procedures receive cross-tabulation;
7. patient-count files, if any, that could contain G004.

Search the downloaded files themselves for:

- `G004`;
- the exact Japanese procedure label corresponding to intravenous infusion of at least 500 mL;
- variants caused by full-width characters, spaces, or encoding.

### Required determination

Classify the result as exactly one of the following:

- `AVAILABLE_USABLE`: G004 counts are cross-tabulated jointly by prefecture and age and can support a defensible older-age outcome.
- `AVAILABLE_LIMITED`: a joint table exists, but suppression, missing age bands, incompatible units, or another limitation prevents or weakens use.
- `NOT_PUBLICLY_AVAILABLE`: prefecture and age marginal tables exist separately, but no joint G004 prefecture-by-age table is public.

Do not infer joint counts by combining separate prefecture and age marginal tables. Do not treat suppressed cells as zero.

### Audit outputs

Create:

- `reports/major_revision/g004_public_data_availability_audit.md`
- `reports/major_revision/g004_public_file_inventory.csv`
- `reports/major_revision/g004_search_log.txt`
- raw copies or archived responses under `02_Data/raw/major_revision/ndb10_g004_audit/`

For every audited item, record:

- official title and exact Japanese table/file label;
- source URL;
- retrieval timestamp;
- local path;
- file size and SHA-256;
- whether G004 is present;
- available dimensions;
- suppression notation and its documented meaning.

The audit report must contain a short, source-supported sentence suitable for the response letter. Use one of these forms, adjusted only if the evidence requires it:

> We re-examined the complete public file structure of the Tenth NDB Open Data. Age-stratified G004 counts and prefecture-level G004 counts were available only as separate marginal tables; jointly age-stratified prefecture-level counts for G004 were not publicly available. We therefore could not calculate a prefecture-specific age-standardized or older-population-specific G004 rate.

or

> Jointly age-stratified prefecture-level G004 counts were publicly available. We therefore calculated [precisely describe the rate] and treated it as the preferred age-focused outcome.

### Conditional age-specific branch

If and only if the status is `AVAILABLE_USABLE` or analytically defensible `AVAILABLE_LIMITED`:

1. construct prefecture-specific G004 rates for adults aged 65 years or older using the corresponding 2023 population denominator;
2. if the published age bands and suppression pattern permit, calculate a directly age-standardized rate using prespecified five-year age bands and a clearly identified standard population;
3. otherwise calculate a crude 65+ rate and explain why direct standardization was not possible;
4. preserve suppressed values as unknown and assess whether aggregation is mathematically valid under the NDB suppression rules;
5. rerun the original-exposure hierarchy below using this age-focused outcome as a secondary/preferred analysis, clearly distinguished from the total-population outcome.

Do not silently replace the primary dataset or outcome.

## Part 2: Original-exposure hierarchical models

### Estimand

The exposure is the submitted variable:

`original_elderly_solo_household_pct`

Definition:

> Number of one-person households whose resident is aged 65 years or older divided by all households in the prefecture, multiplied by 100.

Interpret it as a prefecture-level population/service-burden indicator. Do not call it an individual effect of social isolation.

The new exposure, `older_living_alone_pct`, must remain in the project as a complementary analysis of a different estimand. Do not delete it and do not combine both exposures in the same regression model.

### Primary outcome

Use the G004 rate per 100,000 total population calculated with the 2023 population estimate, as in Work Order 01. Apply this same outcome definition to every primary hierarchical model.

Also run a legacy-denominator sensitivity set using the exact submitted 2020 population denominator. This separates the effect of updating the denominator year from the effect of adding confounders.

### Required model sequence

Use unambiguous model labels beginning with `O` for original exposure:

- `O-A`: original exposure only.
- `O-B`: original exposure + prefectural ageing rate.
- `O-C`: original exposure + prefectural ageing rate + general hospital beds per 100,000.
- `O-D`: original exposure + prefectural ageing rate + general hospital beds per 100,000 + days with daily maximum WBGT >=28.

Each model is cumulative. For example, `O-D` must contain all four predictors listed above.

Do not drop ageing rate because of collinearity. Report the estimate and its uncertainty.

### Required statistics

For every model, provide:

- exact formula and N;
- unstandardized original-exposure coefficient;
- HC3 robust standard error, 95% CI, and p-value;
- fully standardized original-exposure coefficient with HC3 95% CI;
- conventional OLS standard error for audit only;
- R-squared and adjusted R-squared;
- partial R-squared for the original exposure;
- VIF for every predictor;
- AIC, AICc, and BIC;
- residual degrees of freedom.

Define partial R-squared using the reduction in ordinary OLS residual sum of squares between the full model and the otherwise identical model without the exposure:

`partial_R2 = (SSE_reduced - SSE_full) / SSE_reduced`

Use HC3 for coefficient inference, but do not describe the SSE-based partial R-squared or likelihood-based AICc as HC3 statistics.

State the exact AICc formula and parameter count convention in the methods log.

### Direct attenuation summary

The principal reviewer-facing output is the change from `O-A` to `O-B`.

Calculate and report:

- absolute coefficient change: `beta_O-B - beta_O-A`;
- coefficient ratio: `beta_O-B / beta_O-A`;
- descriptive percentage attenuation: `100 * (beta_O-A - beta_O-B) / beta_O-A`;
- the same comparison for standardized coefficients;
- change in partial R-squared;
- change in adjusted R-squared and AICc.

Label percentage attenuation as descriptive. Do not call it mediation or the percentage causally explained by ageing.

Produce a coefficient plot showing the original-exposure estimate and HC3 95% CI for O-A through O-D on the same scale.

## Part 3: Sensitivity and diagnostics for the original exposure

Run the following using the full original-exposure hierarchy, not the new exposure:

1. Replace general hospital beds with general clinics per 100,000 in O-C and O-D.
2. Add log population density to O-D.
3. Exclude Tokyo, Osaka, and Kanagawa together from O-D.
4. Run leave-one-prefecture-out O-D for all 47 prefectures.
5. Report Cook's distance, leverage, and DFBETAs for O-D.
6. Log-transform the outcome.
7. Fit population-weighted least squares as exploratory analysis.
8. Replace WBGT >=28 days separately with WBGT >=31 days, WBGT >=33 days, and cumulative WBGT excess above 28.
9. Repeat O-A through O-D with the legacy 2020 outcome denominator.

If the original-exposure association remains after adjustment, do not describe it as robust unless its direction and magnitude are reasonably stable in the influence and leave-one-out analyses.

## Part 4: Nonlinearity and metropolitan influence for the original exposure

Reviewer 2's nonlinearity concern referred to the submitted/original exposure and its median-stratified result. Therefore repeat the nonlinearity assessment for the original exposure in the adjusted setting:

- linear O-D;
- O-D plus a centered quadratic original-exposure term;
- O-D with a natural cubic spline for original exposure, df=3.

Compare models using partial F tests and AICc. Save predicted curves with 95% confidence bands across the observed exposure range and show the prefecture points.

Keep the old median-split analysis only as a reproduction audit. Do not use it to establish dose-response or effect modification.

## Part 5: Side-by-side estimand comparison

Create a concise table that keeps the two exposure concepts separate:

- `O` models: original exposure, representing prefecture-level burden relative to all households;
- `N` models: new exposure, representing the prevalence of living alone within the older population.

Show O-A/O-D beside the corresponding unadjusted/fully adjusted new-exposure models. Include definitions, coefficients, standardized coefficients, CIs, partial R-squared, and interpretation.

Do not state that the original exposure is 'wrong'. Do not state that the new exposure is the only correct exposure. State that they answer different questions and have different relationships with population ageing.

## Part 6: Interpretation decision rules

Do not choose the narrative solely from the p-value. Use coefficient attenuation, confidence intervals, partial R-squared, model diagnostics, and sensitivity analyses.

Classify the result as one of three branches:

### Branch 1: residual population-burden association

Use this branch only if the original-exposure coefficient remains materially positive after age and supply adjustment, its uncertainty is not prohibitive, and influence analyses do not show that a few prefectures drive the result.

Interpretation:

> The association concerns the prefecture-level burden of older adults living alone relative to all households, not an independent individual-level effect of social isolation.

### Branch 2: substantial attenuation consistent with age-structure confounding

Use this branch if adding ageing rate materially reduces the coefficient and/or partial R-squared and the adjusted estimate is compatible with little or no association.

Interpretation:

> The submitted ecological association was sensitive to population age structure and exposure denominator choice.

Do not claim that ageing causally explained the association in full.

### Branch 3: inconclusive adjusted estimate

Use this branch if the adjusted point estimate remains positive but confidence intervals are wide, diagnostics are unstable, or conclusions change across reasonable sensitivity analyses.

Interpretation:

> The data do not distinguish a residual burden association from confounding with adequate precision.

## Required outputs

Add at minimum:

- `03_Analysis/analysis/major_revision/06_g004_availability_audit.py` or an equivalently reproducible audit script.
- `03_Analysis/analysis/major_revision/07_original_exposure_models.py`.
- `03_Analysis/results/major_revision/original_exposure_model_results.csv`.
- `03_Analysis/results/major_revision/original_exposure_model_fit.csv`.
- `03_Analysis/results/major_revision/original_exposure_vif.csv`.
- `03_Analysis/results/major_revision/original_exposure_attenuation.csv`.
- `03_Analysis/results/major_revision/original_exposure_sensitivity.csv`.
- `03_Analysis/results/major_revision/original_exposure_leave_one_out.csv`.
- `03_Analysis/results/major_revision/original_exposure_influence.csv`.
- `03_Analysis/results/major_revision/original_exposure_nonlinearity.csv`.
- `03_Analysis/results/major_revision/original_vs_new_exposure_comparison.csv`.
- `03_Analysis/results/major_revision/tables/table_original_exposure_hierarchy.csv`.
- `03_Analysis/results/major_revision/figures/figure_original_exposure_coefficients.png` plus source data.
- `03_Analysis/results/major_revision/figures/figure_original_exposure_nonlinearity.png` plus source data.
- `reports/major_revision/g004_public_data_availability_audit.md`.
- `reports/major_revision/original_exposure_additional_analysis.md`.
- `reports/major_revision/SONNET_REPORT_02_original_exposure_and_G004_audit.md`.
- a DOCX copy of SONNET REPORT 02 for review.

Update, without deleting prior entries:

- `reports/major_revision/source_manifest.csv`.
- `reports/major_revision/reproduction_log.md`.
- `reports/major_revision/issues_for_author.md`.

## Reproducibility checks

1. Record the repository commit/hash at the start and the full final `git status`/diff summary.
2. Run all new scripts from the command line in documented order.
3. Rebuild the analytic dataset and all O-model outputs from cached raw official files in a clean temporary directory.
4. Confirm exactly 47 unique prefecture codes in every complete-case primary analysis.
5. Independently recompute O-A through O-D in a separate verification script or code path and compare coefficients to a strict numerical tolerance.
6. Confirm that no Work Order 01 result was silently overwritten.
7. Confirm no GitHub, Zenodo, journal-submission, or other external state was changed.

## Reviewer-response draft required in the report

Prepare a factual draft paragraph, populated with the actual O-A through O-D results:

> We agree that population age structure was a central potential source of confounding. In direct response, we retained the originally submitted exposure - the percentage of all households consisting of one person aged 65 years or older - and added the prefectural percentage of residents aged 65 years or older to the same model. The original-exposure coefficient changed from [O-A estimate, CI] to [O-B estimate, CI], corresponding to a descriptive attenuation of [x%]. Further adjustment for healthcare supply and WBGT yielded [O-C and O-D summary]. We also reconstructed a complementary exposure using the population aged 65 years or older as the denominator; this alternative estimand was [summary]. These analyses materially changed/qualified the interpretation of the study, and we revised the manuscript accordingly.

Do not draft a rebuttal. Do not claim that the reviewer was incorrect.

## Acceptance criteria

- G004 prefecture-by-age availability is established from the complete official file structure with an auditable inventory.
- O-A through O-D all retain the submitted exposure and use cumulative adjustment.
- The O-A to O-B coefficient change directly answers Reviewer 2.
- Primary and legacy outcome denominators are clearly separated.
- Old and new exposure estimands are not conflated.
- Original-exposure nonlinearity, metropolitan influence, and leave-one-out behavior are evaluated.
- Every reported number maps to a machine-readable result row.
- The clean cached-raw rebuild and independent numerical verification pass.
- Null, attenuated, amplified, unstable, or reversed results are reported without suppression.
- No external repository, Zenodo record, or manuscript is changed.

## Final response to Codex/author

Return only after all acceptance criteria are met. Summarize:

1. definitive G004 age-by-prefecture availability classification and evidence;
2. O-A through O-D estimates;
3. O-A to O-B attenuation;
4. sensitivity, nonlinearity, and influence findings for the original exposure;
5. comparison with the new exposure;
6. selected interpretation branch and why;
7. unresolved author decisions;
8. exact output paths and rebuild command.


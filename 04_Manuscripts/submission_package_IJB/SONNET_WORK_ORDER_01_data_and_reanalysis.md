# SONNET WORK ORDER 01: Data acquisition and reanalysis

## Role

Act as a reproducible research analyst. Work conservatively. Do not alter the source manuscript, GitHub repository, or Zenodo record in this work order. Do not select models or heat metrics because they produce a smaller p-value.

## Inputs

- Source manuscript: `C:\Users\user\Desktop\Japan manuscript_main_IJB_anon.docx`
- Editorial/reviewer decision: `C:\Users\user\Desktop\Major_Revision_International_Journal_of_Biometeorology.pdf`
- Working root: `C:\Users\user\Documents\Codex\2026-08-01\are-heat-health-systems-socially-blind`
- Statistical specification: `outputs/major_revision_strategy_ja.md`

If the current analysis repository or raw dataset is not present under the working root, locate it only through an author-provided path or public GitHub/Zenodo identifier. Do not guess the repository URL. The manuscript URL containing `XXX` is known to be invalid.

## Non-negotiable rules

1. Preserve every downloaded source file byte-for-byte under `data/raw/`.
2. Record source URL, publisher, table name, retrieval timestamp, license/terms note, file size, and SHA-256 in `data/source_manifest.csv`.
3. Put all transformations in scripts. Never hand-edit analysis CSV/XLSX files.
4. Use stable prefecture codes as join keys. Do not join on uncontrolled name strings.
5. Keep suppressed NDB values distinct from true zeros. Document the rule used.
6. Use a single deterministic command to rebuild all derived data, tables, figures, and reports.
7. Freeze package versions and random seeds.
8. Do not publish, edit, or create a Zenodo version during this work order.
9. If a required official table cannot be unambiguously identified, stop that variable and log the issue. Do not substitute a secondary source silently.

## Required official data

### NDB outcome

- Tenth NDB Open Data, medical procedures, G injections, code G004, FY2023.
- Extract prefecture-level counts.
- Confirm whether the source includes public-expense claims and match the current manuscript's extraction definition.
- The public cross-table list does not appear to include G004 by prefecture and age. Verify this from the official file list and record the conclusion. Do not manufacture an elderly-specific outcome.

### Population denominators and ageing

- Statistics Bureau population estimates as of 1 October 2023:
  - total population by prefecture;
  - population aged 65 years or older by prefecture;
  - ageing percentage.
- Recalculate the G004 rate per 100,000 using 2023 total population.

### Living-alone exposure

- 2020 Population Census:
  - number of one-person households/persons aged 65 years or older by prefecture;
  - population aged 65 years or older by prefecture;
  - total households by prefecture for reproduction of the original exposure.
- Derive:
  - `older_living_alone_pct = older_one_person_count / population_65plus_2020 * 100`;
  - `original_elderly_solo_household_pct = older_one_person_households / total_households_2020 * 100`.
- Confirm that the numerator is numerically interpretable as persons living alone because a one-person household contains one person. State this explicitly.

### Healthcare supply

- 2023 Survey of Medical Institutions:
  - general beds in hospitals per 100,000 population as the primary supply variable;
  - general clinics per 100,000 population as the sensitivity variable.
- Preserve the exact Japanese table labels and English translations in the variable dictionary.

### Heat

- Ministry of the Environment official 2023 WBGT historical data, June-September.
- Use daily maximum WBGT, not a simplified formula based on daily mean temperature.
- If multiple observation sites exist per prefecture:
  1. calculate each site's number of threshold days and cumulative excess;
  2. average those site-level summaries within prefecture;
  3. report the number of sites per prefecture;
  4. run a sensitivity analysis using one prespecified representative site per prefecture if an official 47-site set exists.
- Derive:
  - days with daily maximum WBGT >=28;
  - days with daily maximum WBGT >=31;
  - days with daily maximum WBGT >=33;
  - cumulative excess above 28.
- Never label observed WBGT >=33 days as heat-alert days; the alert criterion concerns predicted WBGT.

### Urbanicity

- Population density by prefecture. Prefer a 2023 official population numerator and official land-area denominator. Log-transform for modeling.

## Analysis

### Data audit

- Produce a 47-row analytic dataset with one row per prefecture.
- Report missingness, suppression, duplicates, ranges, and units.
- Compare all reproducible current-manuscript variables/results against the original values and explain discrepancies.
- Produce a correlation matrix and scatterplot matrix for prespecified variables.

### Models

- M0: original exposure only.
- M1: revised living-alone exposure only.
- M2: M1 + ageing percentage.
- M3: M2 + general hospital beds per 100,000.
- M4: M3 + days with daily maximum WBGT >=28.

For every model, output:

- formula and N;
- unstandardized coefficient, HC3 95% CI, and p-value;
- fully standardized coefficient and HC3 95% CI;
- adjusted R-squared;
- exposure partial R-squared with its exact definition;
- VIF;
- residual and influence diagnostics.

Also retain conventional OLS standard errors in a machine-readable audit file, but use HC3 for primary inference.

### Sensitivity analyses

- Replace beds with clinics.
- Add log population density.
- Exclude Tokyo, Osaka, and Kanagawa together.
- Leave one prefecture out and save the exposure coefficient and CI for every iteration.
- Log-transform outcome.
- Population-weighted least squares as exploratory analysis.
- Replace the primary heat metric separately with WBGT >=31 days, WBGT >=33 days, and cumulative excess above 28.

### Nonlinearity

- Compare the linear exposure model with a quadratic exposure model using a partial F test and AICc.
- Fit a natural cubic spline with 3 degrees of freedom as an exploratory sensitivity analysis.
- Do not use median splitting as evidence of a dose-response relationship. Reproduce the old split only in an audit appendix if needed.

### Multiplicity

- Designate M4 as the primary adjusted model.
- Apply Benjamini-Hochberg FDR to exploratory heat-metric tests and any additional climate-variable tests.
- Report effect estimates and confidence intervals regardless of p-value.

### Comparison outcome

- If the outpatient-utilization analysis is retained, call it an exploratory comparison-outcome analysis.
- Apply the same adjustment set where feasible.
- Compare standardized coefficients, correlations, R-squared values, and 95% CIs.
- Do not compare raw coefficient magnitudes across outcomes and do not use the phrase 'six-fold stronger'.

## Required outputs

Create the following under the working root:

- `data/raw/` - untouched official source files.
- `data/derived/prefecture_analysis.csv` - final analytic dataset.
- `data/source_manifest.csv` - provenance and hashes.
- `docs/variable_dictionary.md` - definitions, years, units, transformations.
- `scripts/` - acquisition, cleaning, analysis, tables, and figures.
- `results/model_results.csv` - tidy coefficient-level output.
- `results/model_fit.csv` - N, R-squared, adjusted R-squared, AICc.
- `results/vif.csv`.
- `results/influence.csv`.
- `results/leave_one_out.csv`.
- `results/multiplicity.csv`.
- `results/tables/` - publication-ready tables.
- `results/figures/` - publication-ready figures plus source data.
- `reports/reanalysis_report.md` - methods, deviations, results, and interpretation.
- `reports/reproduction_log.md` - exact commands and package versions.
- `reports/issues_for_author.md` - unresolved decisions only.

## Acceptance tests

- Exactly 47 prefectures are present with unique official codes.
- Every reported manuscript number can be traced to one row in a machine-readable result file.
- A clean rebuild succeeds in a new temporary directory.
- No source file has been altered.
- No Zenodo or GitHub state has changed.
- Results that weaken or reverse the original claim are reported without suppression.

## Final response

Return a concise summary of:

1. whether G004 prefecture-by-age data were available;
2. the exposure estimate across M0-M4;
3. the main sensitivity and nonlinearity findings;
4. unresolved data or interpretation issues;
5. the exact paths of all required outputs.


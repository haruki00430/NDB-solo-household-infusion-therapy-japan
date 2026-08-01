# Prefecture-Level Measures of Older Adults Living Alone and Large-Volume Infusion Therapy Utilization in Japan: Accounting for Population Age Structure and Heat Exposure

Haruki Saito¹, Tetsuya Ohira¹,²

¹ Department of Epidemiology, Fukushima Medical University School of Medicine, Fukushima, Japan
² Radiation Medical Science Center for the Fukushima Health Management Survey, Fukushima Medical University, Fukushima, Japan

*Corresponding author. Email: m211039@fmu.ac.jp

---

## Abstract

### Background

Older adults living alone are often described as vulnerable to heat, but prefecture-level indicators of living alone can reflect both social circumstances and population age structure. We examined whether a prefecture-level measure of older adults living alone was associated with large-volume infusion therapy utilization, and whether this association was robust to adjustment for population age structure, healthcare supply, and summer heat exposure.

### Methods

We conducted an ecological study of 47 Japanese prefectures using fiscal year 2023 data. The primary exposure, prespecified at submission, was the percentage of all households consisting of one person aged ≥65 years (2020 National Census), interpreted as a prefecture-level living-alone burden measure relative to all households. The outcome was the prefecture-level claims rate for G004 large-volume intravenous infusion procedures (≥500 mL) per 100,000 population, primarily using the 2023 population estimate as the denominator, with the originally submitted 2020 population denominator examined as a sensitivity analysis. We fit four cumulative models (HC3 robust inference): the exposure alone (O-A), plus prefectural ageing rate (O-B), plus general hospital beds per 100,000 (O-C), and plus days with daily maximum WBGT ≥28°C (O-D). We also examined an alternative exposure — the percentage of the population aged ≥65 years living alone — as an exposure-definition sensitivity analysis with a different denominator.

### Results

In the unadjusted model, the primary exposure was associated with infusion utilization (β = 656.2; 95% CI, 326.9–985.6; standardized β = 0.521; p < 0.001). Adding prefectural ageing rate attenuated the estimate by 53.3% (β = 306.1; 95% CI, −71.3–683.5; standardized β = 0.243; p = 0.112), and the association was no longer statistically significant. Further adjustment for healthcare supply and heat exposure attenuated the estimate further (O-D: β = −9.4; 95% CI, −493.9–475.1; standardized β = −0.007; p = 0.970). The originally submitted 2020-denominator point estimate (β = 723.4) was exactly reproduced; inferential statistics differed because the revised analysis used HC3 robust standard errors. The alternative living-alone exposure (older population denominator) showed no evidence of association with infusion utilization, unadjusted or adjusted (p = 0.998 and p = 0.803, respectively).

### Conclusions

The unadjusted association between a prefecture-level living-alone measure and large-volume infusion therapy utilization was substantially attenuated after adjustment for prefectural population age structure and was no longer statistically significant. Estimates were further attenuated after adjustment for healthcare supply and heat exposure. Prefecture-level living-alone indicators should not be interpreted as independent heat-vulnerability markers without careful consideration of population age structure and denominator choice.

**Keywords:** heat-health surveillance; living alone; population ageing; ecological study; exposure definition; Japan

---

## Introduction

Older adults living alone are frequently described as a vulnerable group in heat-health research, on the premise that living alone may reduce informal monitoring, delay help-seeking, and limit access to cooling. Prefecture- or community-level measures of living alone are attractive as surveillance indicators because they are routinely available from census data, in contrast to individual-level social isolation, which requires dedicated survey instruments. However, "living alone" and "social isolation" are not equivalent constructs: living alone is an observable household arrangement, whereas social isolation refers to the broader absence of social contact and support, which can occur independently of household composition [Berkman ND et al., 2011 — retain as needed].

A further complication specific to prefecture-level ecological indicators of living alone is that they can simultaneously reflect two distinct phenomena: (1) the prevalence of living alone within the older population, and (2) the overall size of the older population relative to the total population — that is, population age structure. A prefecture-level percentage such as "the proportion of all households consisting of one older adult living alone" is mechanically higher in prefectures with more older residents overall, independent of any tendency for older adults specifically to live alone. Because population ageing is itself strongly associated with many health-service utilization outcomes, an ecological association between such a measure and a health outcome can arise largely, or entirely, from confounding by age structure rather than from any construct related to living alone or social isolation. Denominator choice is therefore not a technical detail but a substantive determinant of what an ecological "living-alone" measure actually estimates.

Separately, heat-health surveillance in Japan and elsewhere has relied primarily on meteorological indicators such as wet-bulb globe temperature (WBGT) forecasts and heat alerts. These systems describe environmental hazard but do not by themselves identify which populations are least able to receive warnings or respond to them. Whether routinely available social or demographic indicators can usefully complement meteorological surveillance is an open, policy-relevant question, but any such indicator must first be shown to carry information beyond population age structure and healthcare supply before it can be considered for that purpose.

We therefore examined, in a nationwide ecological analysis of Japanese prefectures, whether a prespecified prefecture-level measure of older adults living alone (percentage of all households consisting of one person aged ≥65 years) was associated with large-volume infusion therapy utilization, and specifically whether this association was robust to adjustment for prefectural population age structure, healthcare supply, and summer heat exposure. We also examined, as a complementary exposure-definition analysis, an alternative measure using the older population itself as the denominator (percentage of the population aged ≥65 years living alone), to separate the two concepts described above. Our research question was:

> Do prefecture-level measures of older adults living alone identify large-volume infusion therapy utilization beyond population age structure, healthcare supply, and summer heat exposure?

## Materials and methods

### 1. Study design

We conducted a nationwide ecological study using Japanese prefectures (N = 47) as the unit of analysis. Prefecture-level aggregate data were used because individual-level household and geospatial information are not available from NDB (National Database of Health Insurance Claims and Specific Health Checkups of Japan) Open Data. The study period was fiscal year 2023 (April 2023 through March 2024); heat exposure was measured during the summer season (June–September 2023).

### 2. Outcome: large-volume infusion therapy utilization

The outcome was derived from the 10th NDB Open Data. We extracted claims counts for procedure code G004 (intravenous infusion, ≥500 mL per day, for patients other than infants and excluding certain inpatient categories as defined by the procedure code), which is used for volume repletion in a range of clinical contexts and is not specific to heat illness or dehydration. We therefore describe the outcome throughout as **large-volume infusion therapy utilization** and do not use a diagnosis-specific label implying that it exclusively reflects dehydration or heat illness. Rates were calculated per 100,000 total population using the 2023 population estimate (Statistics Bureau of Japan, as of 1 October 2023), temporally aligned with the FY2023 NDB claims period. As a sensitivity analysis, we also calculated the outcome using the originally submitted 2020 National Census population denominator, to separate the effect of updating the denominator year from the effect of adding confounders (Online Resource 1, Table S3).

We independently reviewed the complete file inventory of the 10th NDB Open Data release, including all four publicly available G-injection tables (by sex/age, by prefecture, by treatment month, and by secondary medical area). Prefecture-by-age cross-tabulated counts for G004 were not publicly available; sex/age and prefecture counts exist only as separate marginal tables. We therefore could not construct an age-specific or age-standardized prefectural outcome and instead used the total-population rate, with prefectural ageing rate included as an adjustment variable to address the resulting potential confounding (see below).

### 3. Primary exposure: elderly solo household percentage

The prespecified primary exposure, unchanged from the original submission, was the percentage of all households in a prefecture consisting of one person aged ≥65 years, derived from the 2020 National Census. We interpret this measure as a **prefecture-level living-alone burden indicator relative to all households** — that is, an indicator of how much of a prefecture's total household stock is accounted for by older adults living alone — rather than as a direct, individual-level measure of social isolation.

### 4. Alternative exposure: living-alone prevalence within the older population

As a complementary exposure-definition sensitivity analysis, we constructed an alternative measure: the percentage of the prefecture's population aged ≥65 years who live alone, using the 2020 National Census 65+ population as the denominator (numerator: persons in single-person households aged ≥65 years, from the same census). This measure estimates a different concept — the **prevalence of living alone within the older population**, independent of how large that older population is relative to the total. The two exposures are correlated (r = 0.58) but are not interchangeable: the primary exposure correlated positively with prefectural ageing rate (r = 0.63), whereas the alternative exposure correlated weakly negatively with ageing rate (r = −0.24). We treat neither exposure as uniquely correct; they answer different questions.

### 5. Prefectural ageing rate

Prefectural ageing rate (percentage of the population aged ≥65 years) was calculated from the Statistics Bureau of Japan's population estimate as of 1 October 2023, temporally aligned with the outcome denominator. This variable was omitted from the original submission because it had not been merged into the analysis dataset; it is included here as a prespecified adjustment variable in direct response to reviewer comments.

### 6. Healthcare supply

General hospital beds per 100,000 population (2023 Survey of Medical Institutions, Ministry of Health, Labour and Welfare) were used as the primary healthcare-supply adjustment variable. General clinics per 100,000 population (same source and year) were examined as a sensitivity analysis, substituted for hospital beds.

### 7. Heat exposure

We used official wet-bulb globe temperature (WBGT) observations from the Ministry of the Environment's Heat Illness Prevention Information site (real-time/estimated WBGT API), rather than the simplified daily-mean-temperature-based approximation used in the original submission. For each prefecture, we retrieved hourly WBGT values from all available monitoring sites (mean 17.9 sites per prefecture; range 5–163) for June–September 2023, derived daily maximum WBGT per site, and averaged site-level summaries within each prefecture (number of sites recorded per prefecture; Online Resource 1, Table S1). The prespecified primary heat-adjustment variable was the number of days with daily maximum WBGT ≥28°C. Days with WBGT ≥31°C, days with WBGT ≥33°C, and cumulative WBGT excess above 28°C (Σ max[daily maximum WBGT − 28, 0]) were examined as sensitivity/exploratory heat metrics, with Benjamini-Hochberg false-discovery-rate (FDR) correction applied across this exploratory set. We did not label WBGT ≥33°C days as "alert days"; the official heat-illness alert criterion is based on forecast, not observed, WBGT.

### 8. Population density

Population density (2023, persons per km²) was obtained from the Statistics Bureau's social-life statistical indicators and log-transformed for use in sensitivity analyses.

### 9. Statistical analysis

All analyses used the prespecified primary exposure (percentage of all households with an older adult living alone) unless otherwise noted. We fit four cumulative, hierarchical linear regression models:

- **O-A**: outcome ~ primary exposure
- **O-B**: outcome ~ primary exposure + prefectural ageing rate
- **O-C**: outcome ~ primary exposure + prefectural ageing rate + general hospital beds per 100,000
- **O-D**: outcome ~ primary exposure + prefectural ageing rate + general hospital beds per 100,000 + days with WBGT ≥28°C

Each model retains every covariate from the preceding model. We did not use multicollinearity as a reason to avoid adjustment; variance inflation factors (VIFs) for all covariates in all models were below 3.1 (Table 2), well under conventional concern thresholds, and are reported for every model.

For every model we report: the unstandardized coefficient with heteroskedasticity-consistent (HC3) robust 95% confidence intervals and p-value; the fully standardized coefficient (all variables z-scored) with HC3 95% CI; conventional (classical) OLS standard errors for audit purposes only; R² and adjusted R²; the partial R² for the exposure, defined as (SSE of the model without the exposure − SSE of the full model) / SSE of the model without the exposure, based on ordinary least-squares residual sums of squares (this quantity does not depend on the choice of standard-error estimator); and the corrected Akaike information criterion (AICc), calculated as AIC + 2k(k+1)/(n−k−1), where k is the number of estimated parameters including the intercept and error variance.

We assessed nonlinearity by comparing the linear O-D model with (i) a model adding a centered quadratic term for the primary exposure and (ii) a model replacing the linear exposure term with a natural cubic spline (3 degrees of freedom), using partial F-tests and AICc. We repeated the original manuscript's median-split stratified analysis as an audit-only reproduction; it is not used as evidence of dose-response.

We conducted the following sensitivity analyses on the O-D model: substituting general clinics for hospital beds; adding log-transformed population density; excluding Tokyo, Osaka, and Kanagawa jointly; leave-one-prefecture-out re-estimation (47 iterations); log-transforming the outcome; population-weighted least squares; and separately substituting the primary heat-adjustment variable with WBGT ≥31°C days, WBGT ≥33°C days, and cumulative WBGT excess. We repeated the O-A–O-D hierarchy using the originally submitted 2020 population denominator for the outcome, keeping this legacy-denominator analysis clearly separate from the primary 2023-denominator analysis. We assessed regression diagnostics (residuals, leverage, Cook's distance, DFBETAs) for the O-D model.

As a complementary analysis, we examined general outpatient utilization (R5 Patient Survey) in relation to the primary exposure, reporting standardized coefficients, Pearson correlation, R², and 95% CIs; we refer to this as an **exploratory comparison-outcome analysis** rather than a negative control, and we do not compare raw (unstandardized) coefficient magnitudes across outcomes measured on different scales.

Analyses were performed using Python 3.14 with pandas, NumPy, SciPy, statsmodels, and scikit-learn. All code, machine-readable results, and provenance records (source URLs, retrieval timestamps, and SHA-256 checksums for all downloaded official data) are available in the accompanying data and code repository.

### 10. Ethics

This study used publicly available aggregate data; individual informed consent was not required, and institutional ethics review was not applicable in accordance with Japanese ethical guidelines for epidemiological research.

## Results

### 1. Data and exposure definitions

Descriptive statistics for all variables are shown in Table 1. The primary exposure (percentage of all households with an older adult living alone) had a mean of 12.6% (SD 1.9%, range 9.4–17.8%). The alternative exposure (percentage of the 65+ population living alone) had a mean of 17.7% (SD 3.1%, range 12.1–26.1%). The two exposures were correlated (r = 0.58). The primary exposure correlated with prefectural ageing rate at r = 0.63, whereas the alternative exposure correlated with ageing rate at r = −0.24, confirming that the two measures capture materially different information about population composition.

### 2. Unadjusted association (O-A)

The primary exposure was associated with large-volume infusion therapy utilization in the unadjusted model (β = 656.2; 95% CI, 326.9–985.6; standardized β = 0.521; R² = 0.272; adjusted R² = 0.256; p < 0.001; Table 2, Fig. 1).

### 3. Direct age-adjusted model (O-B) and descriptive attenuation

Adding prefectural ageing rate to the same model (O-B) changed the exposure coefficient from 656.2 to 306.1 (95% CI, −71.3–683.5; standardized β = 0.243; p = 0.112), a descriptive attenuation of 53.3% (absolute change −350.1; coefficient ratio 0.467). The exposure's partial R² decreased from 0.272 to 0.056. The 95% confidence interval for O-B is compatible with both a modest positive association and little or no association; we do not interpret this result as proof that no positive association exists, but statistical evidence for an independent association was lost at this step. Model fit improved (adjusted R² 0.256 → 0.365; AICc 853.2 → 847.1), reflecting that ageing rate itself explains additional variance in the outcome.

### 4. Further adjustment (O-C, O-D)

Adding general hospital beds per 100,000 (O-C) reduced the exposure coefficient further (β = 94.1; 95% CI, −302.4–490.6; standardized β = 0.075; p = 0.642; partial R² = 0.004). Adding days with WBGT ≥28°C (O-D) reduced the coefficient to near zero and reversed its sign (β = −9.4; 95% CI, −493.9–475.1; standardized β = −0.007; p = 0.970; partial R² < 0.001). Maximum VIF across O-A–O-D was 3.01 (Table 2), indicating that multicollinearity did not limit our ability to adjust for these covariates.

### 5. Legacy 2020-denominator sensitivity analysis

Repeating O-A–O-D using the originally submitted 2020 population denominator produced the same qualitative pattern. The original point estimate was exactly reproduced using the submitted 2020 population denominator (O-A: β = 723.4; 95% CI, 377.5–1,069.2; p < 0.001). Inferential statistics differed from the original submission because the revised analysis used HC3 heteroskedasticity-robust standard errors rather than conventional OLS standard errors. Adding ageing rate (O-B) attenuated the coefficient to 310.2 (95% CI, −87.0–707.4; p = 0.126), a descriptive attenuation of 57.1%; O-C and O-D showed further attenuation to near zero (β = 76.5, p = 0.719; β = −31.8, p = 0.902, respectively; Online Resource 1, Table S3).

### 6. Alternative-denominator exposure analysis

The alternative exposure (percentage of the 65+ population living alone) showed no evidence of association with infusion utilization at any stage of adjustment: unadjusted, r = 0.0003, standardized β = 0.0003 (95% CI, −0.327–0.328), p = 0.998; in the analogous fully adjusted model (ageing rate, hospital beds, WBGT ≥28°C days), standardized β = −0.034 (95% CI, −0.298–0.231), p = 0.803 (Table S4). This pattern was unchanged across all sensitivity analyses described for O-D, including leave-one-prefecture-out re-estimation (47/47 iterations with 95% CIs spanning zero) and tests for nonlinearity.

### 7. Sensitivity, influence, urban, and nonlinearity analyses (primary exposure, O-D)

Substituting general clinics for hospital beds (β = −35.6, p = 0.831), adding log population density (β = −63.2, p = 0.846), excluding Tokyo, Osaka, and Kanagawa jointly (β = −42.0, p = 0.891), log-transforming the outcome (p = 0.714), and population-weighted least squares (β = 91.8, p = 0.749) all yielded non-significant exposure estimates consistent with O-D (Online Resource 1, Table S5). Leave-one-prefecture-out re-estimation of O-D produced exposure coefficients ranging from −107.9 to 92.8 across all 47 iterations, with the 95% CI crossing zero in every iteration.

Cook's distance for O-D identified Hokkaido as the most influential prefecture (Cook's D = 0.667, exceeding the 4/N threshold of 0.085 by approximately 7.8-fold), followed by Kochi (0.190) and Hiroshima (0.144); this pattern was consistent with the alternative exposure's diagnostics. Hokkaido's WBGT summary is an average across 163 monitoring sites spanning substantial internal climatic heterogeneity (Online Resource 1). Excluding Hokkaido in the leave-one-out analysis did not change the qualitative conclusion.

A quadratic term for the primary exposure did not improve model fit relative to the linear O-D model (partial F-test p = 0.142; AICc 845.6 vs. 845.9), nor did a natural cubic spline (3 df; p = 0.141; AICc 845.9). The audit-only reproduction of the original median-split analysis showed non-significant associations in both the high (β = −192.9, p = 0.647) and low (β = 20.7, p = 0.966) exposure strata under full adjustment; this analysis is not used as evidence of dose-response and is presented only in Online Resource 1.

### 8. Exploratory WBGT findings

Substituting the primary heat-adjustment variable in O-D with WBGT ≥31°C days, WBGT ≥33°C days, or cumulative WBGT excess did not change the exposure conclusion (all p ≥ 0.64 for the exposure; Online Resource 1, Table S6). Days with WBGT ≥33°C showed a nominal association with infusion utilization, but the association did not remain statistically significant after correction for multiple comparisons (nominal p = 0.018; Benjamini-Hochberg FDR-adjusted p = 0.055).

### 9. Exploratory comparison-outcome analysis

The primary exposure's standardized association with general outpatient utilization (R5 Patient Survey; standardized β = 0.169; 95% CI, −0.135–0.473; R² = 0.029; p = 0.256) was numerically similar to, and not smaller than, its standardized association with the primary outcome under the same unadjusted specification (Online Resource 1, Table S7). This does not support the originally reported claim of a materially stronger, specific association with infusion therapy utilization.

## Discussion

### 1. Principal result

The prespecified prefecture-level living-alone measure was associated with large-volume infusion therapy utilization in unadjusted analysis, but this association was substantially attenuated (53.3%) and lost statistical significance after adjustment for prefectural ageing rate alone, and approached zero after additional adjustment for healthcare supply and summer heat exposure. This pattern was consistent whether the outcome used the 2023 or the originally submitted 2020 population denominator, and was not driven by any single prefecture. We interpret this as evidence that the submitted ecological association was sensitive to population age structure and exposure denominator choice, not as evidence that population ageing fully explains the original association or that no relationship of any kind exists.

### 2. Population burden versus within-population prevalence

Two conceptually distinct prefecture-level constructs were examined. The primary, prespecified exposure (percentage of all households with an older person living alone) reflects the overall burden of older adults living alone relative to a prefecture's total household stock — a quantity that is mechanically related to how many older residents a prefecture has. The alternative exposure (percentage of the 65+ population living alone) reflects the prevalence of living alone within the older population itself, independent of population size. The primary exposure correlated with ageing rate (r = 0.63); the alternative exposure did not (r = −0.24). Neither measure is inherently "correct"; they answer different demographic questions, and investigators using either indicator for surveillance purposes should be explicit about which one is intended.

### 3. Why ecological social indicators can proxy demographic composition

Ecological indicators constructed as a percentage of one age-restricted subgroup over a differently defined denominator (here, all households rather than older-adult households or older-adult population) are structurally prone to confounding by the size of that subgroup. This is a general caution for social-vulnerability indicators used in surveillance: an association observed at the ecological level may reflect the size of the vulnerable subgroup rather than a characteristic specific to its members.

### 4. Relation to prior heat-vulnerability literature

Prior studies have reported associations between social isolation and heat-related mortality at the individual and small-area level, including during the 1995 Chicago and 2003 European heat waves. Our findings do not contradict this individual-level literature; ecological associations and individual-level associations address different questions, and our null/attenuated ecological finding at the prefecture level should not be read as evidence against individual-level social-isolation effects on heat vulnerability, which we did not and cannot test with this design.

### 5. Restrained interpretation of WBGT findings

Days with WBGT ≥33°C showed a nominal association with infusion utilization that did not survive correction for multiple comparisons. We report this as an exploratory, hypothesis-generating observation rather than a primary positive finding, consistent with our prespecified designation of WBGT ≥28°C days as the primary heat-adjustment variable.

### 6. Implications for validation of social-vulnerability indicators before surveillance use

Our findings suggest that prefecture-level living-alone indicators should undergo explicit adjustment for population age structure, and ideally comparison of denominator choices, before being proposed as independent heat-vulnerability markers for surveillance. Indicators that have not been validated in this way risk directing resources toward prefectures that simply have more older residents, rather than toward prefectures where older adults are disproportionately likely to live alone.

### 7. Strengths and limitations

Strengths include nationwide coverage of all 47 prefectures, use of official NDB Open Data, direct re-analysis of the prespecified exposure and outcome, examination of a complementary exposure with a different denominator, official daily-maximum WBGT data in place of a simplified approximation, and a comprehensive set of sensitivity, influence, and nonlinearity analyses.

Limitations include: (1) the ecological design cannot support individual-level inference (ecological fallacy); (2) living alone is not equivalent to social isolation, and our exposures measure living arrangement rather than perceived or objective social contact; (3) G004 is not specific to dehydration or heat illness and may be used for volume repletion in many clinical contexts; (4) prefecture-by-age cross-tabulated G004 counts are not publicly available, precluding an age-specific or age-standardized outcome; (5) the analysis covers a single fiscal year during an unusually hot summer (2023), limiting generalizability to other years; (6) with N = 47, adjusted confidence intervals remain wide, and our analysis cannot precisely distinguish a small residual association from no association; (7) residual confounding by unmeasured factors (socioeconomic status, treatment practice variation, housing) cannot be excluded; (8) WBGT summaries are prefecture-level averages across monitoring sites and do not capture within-prefecture heterogeneity — Hokkaido's summary, in particular, averages 163 sites across substantial climatic variation and was the most influential observation in regression diagnostics, although the qualitative conclusion was unchanged when Hokkaido was excluded; (9) source years differ across variables by design (2020 Census for household composition, 2023 estimates for population and ageing rate, 2023 Survey of Medical Institutions for healthcare supply), and we aligned the outcome denominator to 2023 to match the NDB claims period while retaining the 2020-denominator analysis as a sensitivity check; and (10) air-conditioning ownership data (2014 survey; not used in the primary models here) reflect ownership, not actual use, and cannot establish whether cooling was applied.

## Conclusions

The initially observed prefecture-level association between a living-alone measure and large-volume infusion therapy utilization was substantially attenuated after accounting for population age structure and approached zero after additional adjustment for healthcare supply and heat exposure. An alternative living-alone measure using the older population as the denominator was also not associated with infusion utilization. Prefecture-level living-arrangement indicators therefore require careful demographic validation — including explicit adjustment for age structure and attention to denominator choice — before being interpreted as independent heat-vulnerability markers.

## Acknowledgments

The authors thank the Ministry of Health, Labour and Welfare of Japan for providing access to the NDB Open Data. All data used are publicly available aggregate statistics.

## Conflicts of Interest

The authors declare no conflicts of interest.

## Data Availability

The NDB Open Data used in this analysis are publicly available from the Ministry of Health, Labour and Welfare of Japan (https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html). The analysis code, derived data, and provenance records are openly available on GitHub (https://github.com/haruki00430/NDB-solo-household-infusion-therapy-japan) and archived on Zenodo; this revision corresponds to Zenodo version DOI https://doi.org/10.5281/zenodo.21739583 (concept DOI: https://doi.org/10.5281/zenodo.20740375).

## Author Contributions

Haruki Saito: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Visualization, Writing – original draft, Writing – review and editing.
Tetsuya Ohira: Conceptualization, Supervision, Writing – review and editing.

## Funding

None declared.

## Declaration of Generative AI and AI-Assisted Technologies in the Manuscript Preparation Process

During the preparation of the original submission and this revision, the authors used AI-assisted tools to support data acquisition scripting, statistical re-analysis, manuscript drafting, and quality-control review. Claude (Anthropic, models in the Claude 5/Sonnet family, accessed via Claude Code) was used for reproducible data-acquisition and analysis scripting, numerical and claim auditing, and drafting of revised manuscript text and the point-by-point response. A second, independent AI-assisted review was used to help specify the required re-analyses and to review the resulting findings before drafting proceeded. These tools were used only for text drafting, code generation, and quality-control review; no generative AI or AI-assisted tools were used to create, alter, or otherwise process the underlying data, or to fabricate results. The authors reviewed and verified all AI-assisted outputs against machine-readable, code-generated results and were responsible for the study design, selection of statistical methods, interpretation of findings, conclusions, and final reference list. The authors take full responsibility for the integrity and accuracy of the final content. AI was not listed as an author.

## References

Bach AJE, Cunningham SJK, Morris NR, Xu Z, Rutherford S, Binnewies S, et al (2024) Experimental research in environmentally induced hyperthermic older persons: a systematic quantitative literature review mapping the available evidence. Temperature (Austin) 11:4-26. https://doi.org/10.1080/23328940.2023.2242062

Berkman ND, Sheridan SL, Donahue KE, Halpern DJ, Crotty K (2011) Low health literacy and health outcomes: an updated systematic review. Ann Intern Med 155:97-107. https://doi.org/10.7326/0003-4819-155-2-201107190-00005

Blatteis CM (2012) Age-dependent changes in temperature regulation - a mini review. Gerontology 58:289-295. https://doi.org/10.1159/000333148

Blazejczyk K, Epstein Y, Jendritzky G, Staiger H, Tinz B (2012) Comparison of UTCI to selected thermal indices. Int J Biometeorol 56:515-535. https://doi.org/10.1007/s00484-011-0453-2

Bouchama A, Knochel JP (2002) Heat stroke. N Engl J Med 346:1978-1988. https://doi.org/10.1056/NEJMra011089

Canouï-Poitrine F, Cadot E, Spira A, Groupe Régional Canicule (2006) Excess deaths during the August 2003 heat wave in Paris, France. Rev Epidemiol Sante Publique 54:127-135. https://doi.org/10.1016/S0398-7620(06)76706-2

Conti S, Meli P, Minelli G, et al (2005) Epidemiologic study of mortality during the Summer 2003 heat wave in Italy. Environ Res 98:390-399. https://doi.org/10.1016/j.envres.2004.10.009

Farbotko C, Waitt G (2011) Residential air-conditioning and climate change: voices of the vulnerable. Health Promot J Austr 22:13-15. https://doi.org/10.1071/HE11413

Fire and Disaster Management Agency (2023) Daily number of patients with heatstroke transported by ambulance in Japan. Tokyo: FDMA. https://www.fdma.go.jp/disaster/heatstroke/post4.html

Günsche S, Borg MA, Anikeeva O, Varghese BM, Li Y, Bhandari D, et al (2026) Mortality, morbidity and healthcare costs of short-term high temperatures and heatwaves exposure in older populations: a global systematic review and meta-analysis. Environ Int 208:110129. https://doi.org/10.1016/j.envint.2026.110129

Harlan SL, Declet-Barreto JH, Stefanov WL, Petitti DB (2013) Neighborhood effects on heat deaths: social and environmental predictors of vulnerability in Maricopa County, Arizona. Environ Health Perspect 121:197-204. https://doi.org/10.1289/ehp.1104625

Hondula DM, Balling RC, Andrade R, Krayenhoff ES, Middel A, Urban A, Georgescu M, Sailor DJ (2017) Biometeorology for cities. Int J Biometeorol 61(Suppl 1):59-69. https://doi.org/10.1007/s00484-017-1412-3

Intergovernmental Panel on Climate Change (IPCC) (2021) Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press, Cambridge. https://www.ipcc.ch/report/ar6/wg1/

Kenney WL, Munce TA (2003) Invited review: aging and human temperature regulation. J Appl Physiol 95:2598-2603. https://doi.org/10.1152/japplphysiol.00202.2003

Liljegren JC, Carhart RA, Lawday P, Tschopp S, Sharp R (2008) Modeling the wet bulb globe temperature using standard meteorological measurements. J Occup Environ Hyg 5:645-655. https://doi.org/10.1080/15459620802310770

Ministry of Health, Labour and Welfare (MHLW) (2024) Vital Statistics: Annual status of deaths due to heatstroke in Japan. Tokyo: MHLW. https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/tokusyu/necchusho24/index.html

Ministry of Internal Affairs and Communications (MIC) (2015) National Survey of Family Income and Expenditure 2014. Tokyo: MIC.

Ministry of the Environment, Government of Japan (n.d.) Heat Illness Prevention Information: Heat Stress Index (WBGT) and Heat Stroke Alerts. https://www.wbgt.env.go.jp/en/

Miyatake N, Sakano N, Murakami S (2012) The relation between ambulance transports stratified by heat stroke and air temperature in all 47 prefectures of Japan in August, 2009: Ecological study. Environ Health Prev Med 17:77-80. https://doi.org/10.1007/s12199-011-0221-2

Naughton MP, Henderson A, Mirabelli MC, et al (2002) Heat-related mortality during a 1999 heat wave in Chicago. Am J Prev Med 22:221-227. https://doi.org/10.1016/S0749-3797(02)00421-X

Ng CF, Ueda K, Takeuchi A, et al (2014) Sociogeographic variation in the effects of heat and cold on daily mortality in Japan. J Epidemiol 24:15-24. https://doi.org/10.2188/jea.JE20130051

Oberai M, Xu Z, Bach A, Forbes C, Jackman E, O'Connor F, et al (2025) A digital heat early warning system for older adults. NPJ Digit Med 8:114. https://doi.org/10.1038/s41746-025-01505-5

Oka K, Honda Y, Hui Phung VL, Hijioka Y (2023) Potential effect of heat adaptation on association between number of heatstroke patients transported by ambulance and wet bulb globe temperature in Japan. Environ Res 216:114666. https://doi.org/10.1016/j.envres.2022.114666

Parsons K (2006) Heat stress standard ISO 7243 and its global application. Ind Health 44:368-379. https://doi.org/10.2486/indhealth.44.368

Patel T, Mullen SP, Santee WR (2013) Comparison of methods for estimating wet-bulb globe temperature index from standard meteorological measurements. Mil Med 178:926-933. https://doi.org/10.7205/MILMED-D-13-00117

Romitti Y, Sue Wing I, Spangler KR, Wellenius GA (2025) The effects of residential air conditioning and social vulnerability on heat-related hospitalizations in California. Environ Int 202:109659. https://doi.org/10.1016/j.envint.2025.109659

Semenza JC, Rubin CH, Falter KH, et al (1996) Heat-related deaths during the July 1995 heat wave in Chicago. N Engl J Med 335:84-90. https://doi.org/10.1056/NEJM199607113350203

Vandentorren S, Bretin P, Zeghnoun A, et al (2006) August 2003 heat wave in France: risk factors for death of elderly people living at home. Eur J Public Health 16:583-591. https://doi.org/10.1093/eurpub/ckl063

Weisskopf MG, Anderson HA, Foldy S, et al (2002) Heat wave morbidity and mortality, Milwaukee, Wis, 1999 vs 1995: an improved response? Am J Public Health 92:830-833. https://doi.org/10.2105/AJPH.92.5.830

Zhang C, Mohamad E, Azlan AA, Wu A, Ma Y, Qi Y (2025) Social media and eHealth literacy among older adults: systematic literature review. J Med Internet Res 27:e66058. https://doi.org/10.2196/66058

## Tables and Figures

**Table 1.** Descriptive Statistics of Prefecture-Level Variables (N = 47) — see `table1_descriptive_statistics.csv`.

**Table 2.** Original-exposure hierarchical models O-A through O-D (cumulative adjustment; N = 47 for each) — see `table2_original_exposure_hierarchy_final.csv`.

**Fig. 1** Coefficient plot for the primary exposure across models O-A through O-D, showing unstandardized HC3 95% confidence intervals and a zero reference line — `figure_original_exposure_coefficients.png`.

**Online Resource 1** (revised): legacy 2020-denominator hierarchy (Table S3); alternative-exposure models (Table S4); sensitivity analyses including clinic substitution, log density, metropolitan exclusion, log-outcome, and WLS (Table S5); leave-one-prefecture-out results; influence diagnostics; quadratic and spline nonlinearity analyses; alternative WBGT metrics with FDR-adjusted p-values (Table S6); audit-only reproduction of the original median-split analysis (clearly labeled as non-primary); exploratory comparison-outcome analysis (Table S7); source data for all figures.

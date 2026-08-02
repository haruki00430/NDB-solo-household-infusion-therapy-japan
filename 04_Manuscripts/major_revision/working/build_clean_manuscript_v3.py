# -*- coding: utf-8 -*-
"""
Surgical in-place revision of the actual submitted/annotated manuscript.

Base file: Japan manuscript_main_IJB_anon.docx (same paragraph/table structure
as the clean submitted manuscript_main_IJB.docx, confirmed by direct diff).

Only paragraphs that substantively changed are rewritten; everything else
(Acknowledgments, Conflicts of Interest, Funding, Author Contributions, and
~24 of 30 references) is left completely untouched so that a Word document
comparison against the true original shows a targeted, meaningful diff
instead of a wall-to-wall rewrite.

All comments are stripped at the end to produce the clean manuscript.
"""
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.shared import Inches

PROJECT_ROOT = Path(r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke")
BASE_DOCX = PROJECT_ROOT / "04_Manuscripts" / "submission_package_IJB" / "Japan manuscript_main_IJB_anon.docx"
OUT_DOCX = PROJECT_ROOT / "04_Manuscripts" / "major_revision" / "final" / "manuscript_main_IJB_major_revision_clean.docx"
FIGURE1_PNG = PROJECT_ROOT / "03_Analysis" / "results" / "major_revision" / "figures" / "figure_original_exposure_coefficients.png"

# ---------------------------------------------------------------------------
# 1. Paragraph-index -> new text (only substantively changed paragraphs)
# ---------------------------------------------------------------------------
REPLACEMENTS = {
    0: "Population Age Structure Explains the Ecological Association Between Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan",

    14: "Older adults living alone are often considered vulnerable to heat because of reduced informal monitoring, delayed help-seeking, and barriers to cooling. Prefecture-level indicators such as elderly solo household rate have been proposed as routinely available markers of this vulnerability, but such indicators may also reflect a prefecture's underlying population age structure. We examined the association between elderly solo household rate and large-volume infusion therapy utilization, and tested whether this association remained after accounting for population age structure, healthcare supply, and summer heat exposure.",

    16: "We conducted an ecological study of 47 Japanese prefectures using fiscal year 2023 data. Large-volume infusion therapy utilization (procedure code G004, \u2265500 mL) from the National Database (NDB) Open Data was used as the outcome, expressed per 100,000 population. Elderly solo household rate, defined as the percentage of all households consisting of one person aged \u226565 years, was derived from the 2020 National Census and used as the primary exposure. We fit cumulative regression models adding, in turn, prefectural ageing rate, general hospital beds per 100,000 population, and official daily-maximum wet-bulb globe temperature (WBGT) days (\u226528\u00b0C, June\u2013September 2023). Nonlinearity, metropolitan influence, and an alternative exposure using the older population as the denominator were also examined.",

    18: "Elderly solo household rate was associated with infusion therapy utilization in the unadjusted analysis (\u03b2 = 656.2; 95% CI, 326.9\u2013985.6; p < 0.001). Adding prefectural ageing rate attenuated the estimate by 53.3% (\u03b2 = 306.1; 95% CI, \u221271.3\u2013683.5; p = 0.112), and the association was no longer statistically significant. Further adjustment for healthcare supply and WBGT reduced the estimate toward zero (\u03b2 = \u22129.4; 95% CI, \u2212493.9\u2013475.1; p = 0.970).",

    20: "The prefectural elderly solo household rate was associated with large-volume infusion therapy utilization in the unadjusted analysis, but this association was substantially explained by prefectural population age structure and was further attenuated toward zero after additional adjustment for healthcare supply and summer heat exposure. These findings indicate that population age structure is a key driver of the apparent ecological association between elderly solo household rate and infusion therapy utilization, underscoring the importance of accounting for demographic composition when evaluating routinely available household-composition indicators for heat-health and social-vulnerability surveillance.",

    21: "Keywords: heat-health surveillance; elderly solo household rate; population ageing; healthcare utilization; ecological study; Japan",

    26: "Older adults living alone are often considered vulnerable to heat because of reduced informal household monitoring (for example, a family member or neighbor noticing signs of heat illness or prompting fluid intake and use of cooling), economic barriers to cooling use, delayed help-seeking, and reduced access to heat-health information, in addition to physiological vulnerability from reduced sweating capacity, diminished thirst perception, impaired thermoregulation, and chronic disease (Kenney and Munce 2003; Bouchama and Knochel 2002; Vandentorren et al. 2006; Canou\u00ef-Poitrine et al. 2006; MIC 2015; Farbotko and Waitt 2011; Semenza et al. 1996; Naughton et al. 2002; Oberai et al. 2025; Zhang et al. 2025). Prefecture-level elderly solo household rate, the percentage of all households consisting of one older adult living alone, has been proposed as a routinely available marker of this social vulnerability. However, because such a measure is calculated over all households, it may also reflect a prefecture's overall population age structure rather than a distinct social characteristic, and this potential confounding has not been formally examined in prior ecological work.",

    27: "Japanese studies have examined individual risk factors and ambulance transport data (Ng et al. 2014; Miyatake et al. 2012), but nationwide ecological evidence linking elderly solo household rate to large-volume infusion therapy utilization, and on whether such an association is independent of population age structure, healthcare supply, and heat exposure, is limited. We therefore examined whether elderly solo household rate was associated with large-volume infusion therapy utilization, and the extent to which this association remained after accounting for prefectural ageing rate, healthcare supply, and official heat-exposure measures.",

    31: "We conducted a nationwide ecological study using Japanese prefectures (N = 47) as the unit of analysis; the prefectures ranged in total 2023 population from approximately 0.5 million to 14.1 million, together representing Japan's total population of approximately 124.4 million. Prefecture-level aggregate data were used because individual household and geospatial information are not available from NDB Open Data. The study period was fiscal year 2023 (April 2023 through March 2024); heat exposure was measured using official Ministry of the Environment wet-bulb globe temperature (WBGT) monitoring-site observations during the summer season (June\u2013September 2023), an unusually hot summer at the time of data collection (Japan Meteorological Agency 2023).",

    32: "2. Outcome: Large-Volume Infusion Therapy Utilization",
    33: "Infusion therapy utilization rates were derived from the 10th NDB Open Data. We extracted claims for infusion procedures involving \u2265500 mL volume (procedure code G004), used for volume repletion in a range of clinical contexts including, but not limited to, heat-related dehydration; the code is not diagnosis-specific. We describe the outcome as large-volume infusion therapy utilization, a non-specific healthcare-utilization measure that may include a heat-related dehydration component. Rates were calculated per 100,000 population using the 2023 population estimate, temporally aligned with the FY2023 NDB claims period (a sensitivity analysis using the 2020 Census population denominator is reported in Online Resource 1). We independently reviewed the complete public file structure of the 10th NDB Open Data and confirmed that prefecture-by-age cross-tabulated counts for G004 are not publicly available; sex/age and prefecture counts exist only as separate marginal tables. We therefore could not construct an age-specific or age-standardized outcome and instead adjusted for prefectural ageing rate directly (Section 5). As a construct validity check, we examined the cross-prefectural correlation between infusion therapy utilization and the summer 2023 heatstroke ambulance transport rate from the Fire and Disaster Management Agency (FDMA) daily transport report (Fire and Disaster Management Agency 2023); this provides limited support for the presence of a heat-related component in the outcome rather than validating it as a direct heat-illness measure.",

    35: "Elderly solo household rate was defined as the percentage of all households consisting of one person aged \u226565 years, derived from the 2020 National Census. We interpret this measure as a prefecture-level indicator of the burden of older adults living alone relative to all households, rather than a direct individual-level measure of social isolation. As a complementary sensitivity analysis, we also constructed an alternative exposure using the prefecture's population aged \u226565 years as the denominator (percentage of the 65+ population living alone; Section 9; Online Resource 1).",

    37: "Heat exposure was assessed using official wet-bulb globe temperature (WBGT) observations from the Ministry of the Environment's Heat Illness Prevention Information monitoring network for June\u2013September 2023. For each monitoring site, we counted the number of days on which daily maximum WBGT met or exceeded each threshold, and then averaged these site-specific day-counts within each prefecture (mean 17.9 sites per prefecture; range 5\u2013163). The primary heat metric was the prefecture-mean number of days with daily maximum WBGT \u226528\u00b0C; days with WBGT \u226531\u00b0C, days with WBGT \u226533\u00b0C, and cumulative WBGT excess above 28\u00b0C were examined as sensitivity heat metrics (Section 6; Online Resource 1). For descriptive purposes (Table 1), we also report the number of days with daily maximum temperature \u226535\u00b0C, averaged across Japan Meteorological Agency stations within each prefecture; this variable was not used as an adjustment variable in the primary models.",

    38: "5. Prefectural Ageing Rate and Healthcare Supply",
    39: "Prefectural ageing rate, defined as the percentage of the population aged \u226565 years and calculated from the Statistics Bureau of Japan's population estimate as of 1 October 2023, was included as the primary demographic adjustment variable, temporally aligned with the outcome denominator. General hospital beds per 100,000 population (2023 Survey of Medical Institutions, Ministry of Health, Labour and Welfare) were included as the primary healthcare-supply adjustment variable, with general clinics per 100,000 population (same source and year) examined as a sensitivity analysis substituted for beds. Air conditioning prevalence (proportion of households owning at least one air conditioning unit, %), obtained from the 2014 National Survey of Family Income and Expenditure, is retained for descriptive purposes (Table 1) but was not included in the primary adjusted models, because these data describe ownership rather than use.",

    41: "All primary models used elderly solo household rate as the exposure. We fit four cumulative models: the exposure alone (Model O-A); Model O-A plus prefectural ageing rate (Model O-B); Model O-B plus general hospital beds per 100,000 (Model O-C); and Model O-C plus days with WBGT \u226528\u00b0C (Model O-D). We did not use multicollinearity as a reason to avoid adjustment; variance inflation factors for all covariates in all models were below 3.1 (Table 2). For every model we report the unstandardized coefficient with heteroskedasticity-consistent (HC3) robust 95% confidence intervals and p-value, the fully standardized coefficient, adjusted R\u00b2, the partial R\u00b2 for the exposure (based on the reduction in ordinary least-squares residual sum of squares, independent of the standard-error estimator), and the corrected Akaike information criterion (AICc).",

    42: "We conducted the following sensitivity analyses on the fully adjusted model: substituting general clinics for hospital beds; excluding Tokyo, Osaka, and Kanagawa jointly; leave-one-prefecture-out re-estimation (47 iterations); and separately substituting the primary heat metric with WBGT \u226531\u00b0C days, WBGT \u226533\u00b0C days, and cumulative WBGT excess, applying Benjamini-Hochberg false-discovery-rate correction across this exploratory heat-metric set. As a further sensitivity analysis, we repeated all models using the 2020 Census population denominator for the outcome (Online Resource 1). We assessed nonlinearity by comparing the linear model with a centered quadratic exposure term and a natural cubic spline (3 degrees of freedom), using partial F-tests and AICc; a median-split stratified analysis is reported in Online Resource 1 and did not support a simple dose-response interpretation. We also examined an alternative exposure using the older population as the denominator (Section 9).",

    43: "Regression coefficients (\u03b2), 95% confidence intervals (CIs), R\u00b2, adjusted R\u00b2, and p-values are reported, together with regression diagnostics (residuals, leverage, Cook's distance, DFBETAs) for the fully adjusted model. Statistical significance was defined as two-sided p < 0.05, interpreted alongside effect estimates and confidence intervals rather than significance alone. Analyses were performed using Python (version 3.14), statsmodels (version 0.14), scikit-learn, and matplotlib.",

    48: "Across the 47 Japanese prefectures, mean elderly solo household rate was 12.6 \u00b1 1.9% (range 9.4\u201317.8%; Table 1). Mean large-volume infusion therapy utilization was 8,022 \u00b1 2,389 per 100,000 population (range 4,231\u201313,234). Mean prefectural ageing rate was 31.6 \u00b1 3.3% (range 22.8\u201339.0%). Mean general hospital beds were 794 \u00b1 149 per 100,000 (range 509\u20131,147). Mean number of days with daily maximum WBGT \u226528\u00b0C (official Ministry of the Environment data) was 72.9 \u00b1 14.1 (range 27.3\u2013112.3); for descriptive comparison, mean number of days with maximum temperature \u226535\u00b0C was 17.9 \u00b1 12.1 (range 0.0\u201344.0). Mean air conditioning prevalence was 89.7 \u00b1 13.6% (range 26.6\u201398.2%).",

    49: "2. Association Between Elderly Solo Household Rate and Infusion Therapy Utilization: Unadjusted and Adjusted Models",
    50: "Elderly solo household rate was associated with infusion therapy utilization in the unadjusted model (Model O-A: \u03b2 = 656.2; 95% CI, 326.9\u2013985.6; standardized \u03b2 = 0.521; R\u00b2 = 0.272; adjusted R\u00b2 = 0.256; p < 0.001; Table 2, Fig. 1). Adding prefectural ageing rate (Model O-B) changed the coefficient to 306.1 (95% CI, \u221271.3\u2013683.5; standardized \u03b2 = 0.243; p = 0.112), a descriptive attenuation of 53.3%; the 95% confidence interval crossed zero and statistical significance was lost, although the interval remains compatible with both a modest positive association and little or no association. Adding general hospital beds per 100,000 (Model O-C) reduced the coefficient further (\u03b2 = 94.1; 95% CI, \u2212302.4\u2013490.6; p = 0.642); the estimate was similarly attenuated when clinics were substituted for beds (Online Resource 1). Adding WBGT \u226528\u00b0C days (Model O-D) reduced the coefficient to near zero and reversed its sign (\u03b2 = \u22129.4; 95% CI, \u2212493.9\u2013475.1; p = 0.970). Maximum VIF across all models was 3.01 (Table 2).",

    51: "3. Influence Diagnostics and Sensitivity Analyses",
    52: "Cook's distance for the fully adjusted model identified Hokkaido as the most influential prefecture (Cook's D = 0.667, exceeding the 4/N = 0.085 threshold by approximately 7.8-fold), followed by Kochi (0.190) and Hiroshima (0.144); Hokkaido's WBGT summary averages 163 monitoring sites spanning substantial internal climatic heterogeneity. Leave-one-prefecture-out re-estimation of the fully adjusted model (47 iterations) produced coefficients ranging from \u2212107.9 to 92.8, with the 95% CI crossing zero in every iteration, indicating that the attenuated result was not driven by any single prefecture, including Hokkaido. Excluding Tokyo, Osaka, and Kanagawa jointly did not materially change the result (\u03b2 = \u221242.0; 95% CI, \u2212645.6\u2013561.6; p = 0.891).",

    53: "4. Nonlinearity",
    54: "A quadratic term for elderly solo household rate did not improve model fit relative to the linear fully adjusted model (partial F test p = 0.142; AICc 845.6 versus 845.9), nor did a natural cubic spline (3 degrees of freedom; p = 0.141; AICc 845.9). A median-split stratified analysis, in which the association was present in the lower stratum but absent in the higher stratum, is reported in Online Resource 1; it did not support a simple dose-response interpretation and is not used as a primary result.",

    55: "5. Alternative Exposure (Denominator) Analysis",
    56: "As a complementary sensitivity analysis, we examined an alternative exposure defined as the percentage of the prefecture's population aged \u226565 years who live alone (denominator: 65+ population, rather than all households). This alternative measure showed no association with infusion utilization, either unadjusted (standardized \u03b2 = 0.0003; 95% CI, \u22120.327\u20130.328; p = 0.998) or in the analogous fully adjusted model (standardized \u03b2 = \u22120.034; 95% CI, \u22120.298\u20130.231; p = 0.803), and this pattern was unchanged across the sensitivity analyses described above (Online Resource 1).",

    57: "6. Comparison with FDMA Heatstroke Ambulance Transport",

    58: "As a construct validity check, infusion therapy utilization was examined in relation to the summer 2023 heatstroke ambulance transport rate from FDMA (Fire and Disaster Management Agency 2023). A positive association was observed (\u03b2 = 70.19; 95% CI, 36.85\u2013103.53; r = 0.534; p < 0.001; Online Resource 1), which provides limited support for the presence of a heat-related component in the infusion therapy outcome, rather than validating it as a direct measure of heat-related dehydration.",

    59: "7. Comparison-Outcome Analysis",
    60: "A comparison with general outpatient utilization (R5 Patient Survey), using standardized coefficients (Online Resource 1), showed that the standardized association with general outpatient utilization (β = 0.424; 95% CI, 0.088–0.760; p = 0.013) was only modestly smaller than the standardized association with infusion therapy utilization (β = 0.521; 95% CI, 0.260–0.783; p < 0.001) and did not support outcome specificity for infusion therapy.",

    63: "This nationwide ecological analysis examined whether elderly solo household rate, a routinely available prefecture-level indicator, was associated with large-volume infusion therapy utilization, and whether any such association was independent of population age structure, healthcare supply, and summer heat exposure. An association was present in the unadjusted analysis but was substantially attenuated (53.3%) and lost statistical significance after adjustment for prefectural ageing rate alone, and was further attenuated toward zero after additional adjustment for healthcare supply and heat exposure. An alternative exposure using the older population as the denominator showed no association with the outcome at any stage. These findings indicate that population age structure substantially explains the ecological association between elderly solo household rate and infusion therapy utilization.",

    64: "Physiological vulnerability to heat among older adults, including reduced thermoregulation and blunted thirst perception, remains biologically plausible and is well documented (Kenney and Munce 2003; Bouchama and Knochel 2002; Bach et al. 2024; Blatteis 2012). The present ecological results indicate that population age structure, rather than living alone itself, is the principal driver of the observed prefecture-level association with infusion therapy utilization.",

    65: "Regional infusion use may also reflect healthcare supply and local treatment practice in addition to underlying morbidity: the estimate was further attenuated after adjusting for general hospital beds, and this pattern was unchanged when clinics were substituted for beds. We did not test whether supply-induced demand specifically explains infusion use; we show only that accounting for healthcare supply further attenuates the association between elderly solo household rate and infusion therapy utilization.",

    66: "Our findings do not contradict international evidence that social isolation is associated with heat-related mortality at the individual and small-area level, including during the 1995 Chicago and 2003 European heat waves (Vandentorren et al. 2006; Canou\u00ef-Poitrine et al. 2006; Semenza et al. 1996; Conti et al. 2005). Ecological associations and individual-level associations address different questions, and our attenuated ecological finding at the prefecture level should not be read as evidence against individual-level effects of social isolation on heat vulnerability, which this design cannot test.",

    67: "That population age structure explains most of the ecological association for elderly solo household rate should not be interpreted as evidence that heat exposure is unimportant. Alternative WBGT metrics did not materially alter the interpretation; detailed exploratory results are reported in Online Resource 1. Prefecture-level climatic averages may also miss neighborhood and indoor exposures, and regional heat adaptation may attenuate simple ecological climate-health associations (Hondula et al. 2017; Harlan et al. 2013; Oka et al. 2023).",

    68: "These findings indicate that prefecture-level social-vulnerability indicators such as elderly solo household rate substantially reflect population age structure, and require careful demographic validation, together with consideration of healthcare supply and improved heat-exposure measures, before being proposed for heat-health surveillance.",

    69: "Strengths include nationwide coverage of all 47 prefectures, use of NDB Open Data, official daily-maximum WBGT observations, and a comprehensive set of sensitivity, influence, and nonlinearity analyses.",

    70: "Several limitations should be considered. First, this is an ecological design; associations at the prefecture level may not reflect individual-level relationships, and we cannot determine whether individuals living alone within a prefecture had higher infusion therapy utilization than those living with family. Second, elderly solo household rate is a household-composition measure and is not equivalent to social isolation. Third, infusion therapy utilization (G004) is not specific to dehydration or heat illness and may be used for volume repletion in other contexts, including perioperative fluid management, gastrointestinal illness, infections, and general supportive care; monthly aggregation of claims is not available in prefecture-level NDB Open Data, so a summer peak in utilization could not be verified directly.",

    71: "Fourth, prefecture-by-age cross-tabulated G004 counts are not publicly available in the 10th NDB Open Data, precluding an age-specific or age-standardized outcome; we addressed this by adjusting for prefectural ageing rate directly. Fifth, the analysis covers a single fiscal year (2023), which was unusually hot at the time (Japan Meteorological Agency 2023); given that summers in Japan are projected to become progressively hotter, this single-year window may in fact be broadly representative of near-future conditions, although replication across multiple years remains necessary to confirm generalizability. Sixth, with N = 47, adjusted confidence intervals remain wide, and this analysis cannot precisely distinguish a small residual association from no association. Seventh, unmeasured confounding cannot be excluded, including reduced thirst perception and lower fluid intake among older adults, chronic disease prevalence, medication use, infections, gastrointestinal illness, and other individual clinical factors associated with infusion therapy that are not captured at the prefecture level.",

    72: "Eighth, climatic measures are prefecture-level averages and do not capture indoor or neighborhood exposures; the WBGT summary for Hokkaido in particular averages 163 monitoring sites across substantial internal climatic heterogeneity and was the most influential single observation in regression diagnostics, although the qualitative conclusion was unchanged when Hokkaido was excluded (leave-one-prefecture-out analysis). Ninth, source years differ across variables (2020 Census for elderly solo household rate; 2023 estimates for population, ageing rate, and outcome denominator; 2023 Survey of Medical Institutions for healthcare supply; 2014 survey for air conditioning prevalence), and we aligned the outcome denominator to 2023 to match the NDB claims period while retaining a 2020 Census-based denominator analysis as a sensitivity check (Online Resource 1).",

    73: "Finally, air conditioning prevalence (2014 survey) reflects ownership, not actual use, and cannot establish whether cooling was applied; it is reported descriptively (Table 1) and was not included in the primary adjusted models. The present findings should be interpreted as evidence for cautious, demographically informed use of social-vulnerability indicators in heat-health surveillance, rather than as evidence against considering social factors altogether.",

    74: "Given the ecological, cross-sectional, and single-year design, these findings should be considered hypothesis-generating. These considerations indicate that firmer conclusions about an independent heat-vulnerability effect of household living arrangement would require age-specific outcome data, multi-year designs, and finer-grained exposure measurement, in addition to the demographic caution highlighted above.",

    77: "In this nationwide ecological study, elderly solo household rate was associated with large-volume infusion therapy utilization in unadjusted analysis; this association was substantially explained by prefectural ageing rate and was further attenuated toward zero after additional adjustment for healthcare supply and summer heat exposure.",

    78: "These findings indicate that population age structure, together with healthcare supply and heat exposure, substantially explains the ecological association between elderly solo household rate and infusion therapy utilization. Given the ecological, cross-sectional, and single-year design, these findings should be regarded as hypothesis-generating; they highlight the importance of explicit adjustment for age structure and attention to denominator choice before routinely available social-vulnerability indicators are proposed for heat-health surveillance.",

    79: "Future individual-level and longitudinal studies, and age-specific administrative data where available, are needed to clarify whether living alone carries an independent heat-vulnerability signal beyond population age structure, and to establish the role of healthcare supply and improved heat-exposure measures in explaining prefecture-level utilization patterns.",

    88: "The NDB Open Data used in this analysis are publicly available from the Ministry of Health, Labour and Welfare of Japan (https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html). The analysis code, derived data, and provenance records are openly available on GitHub (https://github.com/haruki00430/NDB-solo-household-infusion-therapy-japan) and archived on Zenodo (https://doi.org/10.5281/zenodo.20740374), which always resolves to the most recent version.",

    98: "During the preparation of the original submission, the authors used AI-assisted tools to support manuscript drafting and statistical analysis scripting. Cursor 3.0 (Anysphere) and Google Antigravity (Google) were used for AI-assisted writing and Python code development. Large language models used through these platforms included Claude Sonnet 4.6 and Claude Opus 4.8 (Anthropic), GPT-5.5 (OpenAI), and Gemini 3 Pro (Google). During preparation of the revision, the authors used AI-assisted tools (Claude Sonnet 5, Anthropic, accessed via Claude Code) to support text drafting and the development of data-processing and statistical-analysis code. The authors executed the code, verified all source data, numerical results, tables, and figures, and independently determined the statistical methods and interpretation. No generative image tools were used. The authors reviewed and edited all outputs and take full responsibility for the final manuscript. AI was not listed as an author.",

    133: "WBGT, wet-bulb globe temperature; SD, standard deviation. WBGT days are based on official Ministry of the Environment daily-maximum observations (June\u2013September 2023). Days with maximum temperature \u226535\u00b0C are shown for descriptive comparison and were not used as an adjustment variable. Air conditioning prevalence (2014 National Survey of Family Income and Expenditure) reflects ownership, not use, and was not used as an adjustment variable. Ageing rate and healthcare supply are the primary demographic and healthcare-supply adjustment variables in this analysis.",

    135: "Table 2. Hierarchical Regression Models: Elderly Solo Household Rate and Large-Volume Infusion Therapy Utilization (N = 47)",

    138: "N = 47 for all models. Model O-A: exposure alone. Model O-B: Model O-A + prefectural ageing rate. Model O-C: Model O-B + general hospital beds per 100,000. Model O-D: Model O-C + days with WBGT \u226528\u00b0C (each model cumulative). All confidence intervals are heteroskedasticity-consistent (HC3) robust; VIF, variance inflation factor; AICc, corrected Akaike information criterion. Using the 2020 Census population denominator (Online Resource 1, Table S3) yields a closely comparable Model O-A estimate; inferential statistics differ because this analysis uses HC3 robust standard errors.",

    141: "Fig. 1 Coefficient plot for elderly solo household rate across Models O-A through O-D, showing unstandardized coefficients with HC3 95% confidence intervals and a zero reference line.",

    149: "Online Resource 1 contains supplementary tables and figures, including the 2020 Census-denominator model hierarchy, the alternative-exposure (denominator) analysis, sensitivity and influence diagnostics, nonlinearity analyses (including the median-split analysis), exploratory WBGT metrics with FDR-adjusted p-values, and the comparison-outcome analysis with general outpatient utilization.",
}

# paragraphs to delete entirely: Panel A/B labels, Fig.2 heading+caption+image, Online Resource
# preview image (136, 137, 142, 145, 146, 150), plus reference-list entries no longer cited
# in-text now that the simplified WBGT formula and the original Discussion citing them have
# been removed/rewritten: Berkman (102), Liljegren (115), Patel (125), Romitti (126), Weisskopf (129)
DELETE_PARAGRAPHS = [102, 115, 125, 126, 129, 136, 137, 142, 145, 146, 150]

# Table 1 (index 0): new descriptive-statistics rows (row 0 header kept as-is)
TABLE0_NEW_ROWS = [
    ["Outcome variable", "", "", "", "", "", "", ""],
    ["Large-volume infusion therapy utilization (G004, \u2265500 mL)", "per 100,000", "47", "8,022.2", "2,389.3", "4,231.3", "7,608.7", "13,234.1"],
    ["Exposure variable", "", "", "", "", "", "", ""],
    ["Elderly solo household rate", "%", "47", "12.6", "1.9", "9.4", "12.3", "17.8"],
    ["Alternative exposure (sensitivity) variable", "", "", "", "", "", "", ""],
    ["% of population aged \u226565 living alone", "%", "47", "17.7", "3.1", "12.1", "17.1", "26.1"],
    ["Adjustment variables", "", "", "", "", "", "", ""],
    ["Prefectural ageing rate", "%", "47", "31.6", "3.3", "22.8", "31.7", "39.0"],
    ["General hospital beds", "per 100,000", "47", "794.2", "148.5", "508.7", "800.3", "1,146.5"],
    ["General clinics (sensitivity)", "per 100,000", "47", "84.5", "11.9", "61.8", "85.9", "113.0"],
    ["Climatic variables", "", "", "", "", "", "", ""],
    ["Days with WBGT \u226528\u00b0C (official, primary)", "days", "47", "72.9", "14.1", "27.3", "74.7", "112.3"],
    ["Days with WBGT \u226531\u00b0C (sensitivity)", "days", "47", "28.7", "10.6", "6.0", "26.5", "61.6"],
    ["Days with WBGT \u226533\u00b0C (sensitivity)", "days", "47", "2.9", "2.7", "0.0", "1.7", "10.8"],
    ["Days with maximum temperature \u226535\u00b0C (descriptive only)", "days", "47", "17.9", "12.1", "0.0", "17.0", "44.0"],
    ["Covariate (descriptive only)", "", "", "", "", "", "", ""],
    ["Air conditioning prevalence", "%", "47", "89.7", "13.6", "26.6", "94.8", "98.2"],
]

TABLE2_ROWS = [
    ["Model", "Added covariates", "\u03b2 (95% CI)", "Standardized \u03b2 (95% CI)", "p", "Exposure partial R\u00b2", "Adjusted R\u00b2", "AICc"],
    ["O-A", "Unadjusted", "656.2 (326.9, 985.6)", "0.521 (0.260, 0.783)", "<0.001", "0.272", "0.256", "853.2"],
    ["O-B", "+ ageing rate", "306.1 (-71.3, 683.5)", "0.243 (-0.057, 0.543)", "0.112", "0.056", "0.365", "847.1"],
    ["O-C", "+ ageing rate + hospital beds", "94.1 (-302.4, 490.6)", "0.075 (-0.240, 0.390)", "0.642", "0.004", "0.386", "846.9"],
    ["O-D", "+ ageing rate + hospital beds + WBGT\u226528d", "-9.4 (-493.9, 475.1)", "-0.007 (-0.392, 0.377)", "0.970", "<0.001", "0.422", "845.6"],
]


def set_fixed_column_widths(table, widths_in):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn as _qn
    table.autofit = False
    tblPr = table._tbl.tblPr
    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(_qn('w:type'), 'fixed')
    tblPr.append(tblLayout)
    for row in table.rows:
        for i, w in enumerate(widths_in):
            row.cells[i].width = Inches(w)
    for i, w in enumerate(widths_in):
        table.columns[i].width = Inches(w)
    # reduce font size slightly for dense tables
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = docx.shared.Pt(9)


def set_paragraph_text(paragraph, new_text):
    for run in list(paragraph.runs):
        run._element.getparent().remove(run._element)
    paragraph.add_run(new_text)


def main():
    document = docx.Document(BASE_DOCX)
    paras = document.paragraphs

    # --- text replacements ---
    for idx, new_text in REPLACEMENTS.items():
        set_paragraph_text(paras[idx], new_text)

    # --- reference DOI corrections (only the DOI substring changes; rest of citation untouched) ---
    doi_fixes = {
        105: ("10.1056/NEJMra011086", "10.1056/NEJMra011089"),
        107: ("10.1016/j.envres.2004.12.009", "10.1016/j.envres.2004.10.009"),
        108: ("10.1071/HE10013", "10.1071/HE11413"),
        111: ("10.1289/ehp.1103532", "10.1289/ehp.1104625"),
        119: ("10.1007/s12199-011-0267-9", "10.1007/s12199-011-0221-2"),
        120: ("10.1016/S0749-3797(02)00414-X", "10.1016/S0749-3797(02)00421-X"),
    }
    for idx, (old_doi, new_doi) in doi_fixes.items():
        p = paras[idx]
        full_text = p.text
        assert old_doi in full_text, f"Expected DOI not found in paragraph {idx}: {full_text[:80]}"
        new_full = full_text.replace(old_doi, new_doi)
        set_paragraph_text(p, new_full)

    # --- insert new JMA reference (alphabetically after IPCC [113], before Kenney [114]) ---
    from copy import deepcopy
    anchor_para = paras[113]
    new_para_element = deepcopy(anchor_para._element)
    anchor_para._element.addnext(new_para_element)
    new_para = docx.text.paragraph.Paragraph(new_para_element, anchor_para._parent)
    set_paragraph_text(
        new_para,
        "Japan Meteorological Agency (2023) Climate characteristics of summer 2023 (June–August): "
        "the warmest summer since observations began in 1898 (mean temperature anomaly +1.76°C, "
        "exceeding the previous record of +1.08°C set in 2010). Tokyo: JMA. "
        "https://www.jma.go.jp/jma/press/2309/01b/tenko230608.html",
    )

    # --- delete paragraphs (Panel labels, Fig.2 heading/caption/image, Online Resource preview image) ---
    # IMPORTANT: use the ORIGINAL `paras` list captured at the top of main(), not a fresh
    # document.paragraphs call. Paragraph.insert-via-addnext above (JMA reference) shifts
    # every subsequent index in a freshly recomputed document.paragraphs list, which previously
    # caused this block to delete the wrong paragraphs (Kenney/Parsons/Vandentorren instead of
    # Liljegren/Romitti/Weisskopf). `paras[i]` still points at the original i-th element by
    # object identity regardless of insertions elsewhere, so it remains correct here.
    to_delete_elements = [paras[i]._element for i in DELETE_PARAGRAPHS]
    for el in to_delete_elements:
        el.getparent().remove(el)

    # --- replace Figure 1 image (paragraph originally at index 144) ---
    # after deletions above (136,137 removed before it; 142,145,146,150 after it) index 144 shifts by -2
    # locate the image paragraph robustly by scanning for a paragraph containing a blip that is not yet processed
    target_img_para = None
    for p in document.paragraphs:
        if p._element.findall('.//' + qn('a:blip')):
            target_img_para = p
            break
    assert target_img_para is not None, "Could not locate Figure 1 image paragraph"
    for run in list(target_img_para.runs):
        run._element.getparent().remove(run._element)
    run = target_img_para.add_run()
    run.add_picture(str(FIGURE1_PNG), width=Inches(5.5))

    # --- rebuild Table 1 (descriptive stats): keep header row, replace remaining rows ---
    table0 = document.tables[0]
    # remove all rows except header
    for row in list(table0.rows[1:]):
        row._element.getparent().remove(row._element)
    for row_data in TABLE0_NEW_ROWS:
        cells = table0.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = val
    set_fixed_column_widths(table0, [1.95, 0.75, 0.32, 0.58, 0.55, 0.55, 0.62, 0.65])

    # --- replace Table (regression, index 1) with new 9-column hierarchical table; delete old sensitivity table (index 2) ---
    old_table1 = document.tables[1]
    old_table2 = document.tables[2]

    # insert new table right after old_table1's position, then remove old_table1 and old_table2
    anchor = old_table1._tbl
    new_table = document.add_table(rows=0, cols=len(TABLE2_ROWS[0]))
    anchor.addnext(new_table._tbl)
    for row_data in TABLE2_ROWS:
        cells = new_table.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = val
            if row_data is TABLE2_ROWS[0]:
                for para in cells[i].paragraphs:
                    for run in para.runs:
                        run.bold = True
    set_fixed_column_widths(new_table, [0.6, 1.05, 1.0, 0.95, 0.55, 0.7, 0.65, 0.5])
    # re-bold header row (font-size reset in set_fixed_column_widths clears bold via new Pt but not bold flag; ensure bold retained)
    for cell in new_table.rows[0].cells:
        for para in cell.paragraphs:
            for run in para.runs:
                run.bold = True

    anchor.getparent().remove(anchor)
    old_table2._tbl.getparent().remove(old_table2._tbl)

    # --- strip all comments (references, ranges, and extended/ids parts) to produce a clean manuscript ---
    body = document.element.body
    for tag in ("commentRangeStart", "commentRangeEnd", "commentReference"):
        for el in body.findall('.//' + qn(f'w:{tag}')):
            el.getparent().remove(el)

    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUT_DOCX)

    # remove the comments-related parts from the saved package entirely
    import zipfile
    tmp_path = OUT_DOCX.with_suffix('.tmp.docx')
    with zipfile.ZipFile(OUT_DOCX, 'r') as zin:
        names = zin.namelist()
        data = {n: zin.read(n) for n in names}
    drop = {n for n in names if 'comments' in n.lower()}
    # also scrub references to comments parts from [Content_Types].xml and document.xml.rels
    ct = data.get('[Content_Types].xml', b'').decode('utf-8')
    for n in drop:
        part_name = '/' + n
        ct = ct.replace(f'<Override PartName="{part_name}" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>', '')
    data['[Content_Types].xml'] = ct.encode('utf-8')
    rels_name = 'word/_rels/document.xml.rels'
    if rels_name in data:
        rels = data[rels_name].decode('utf-8')
        import re
        rels = re.sub(r'<Relationship[^>]*Target="comments[^"]*"[^>]*/>', '', rels)
        data[rels_name] = rels.encode('utf-8')

    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for n, content in data.items():
            if n in drop:
                continue
            zout.writestr(n, content)
    tmp_path.replace(OUT_DOCX)

    print(f"[OK] surgically revised clean manuscript written to {OUT_DOCX}")


if __name__ == "__main__":
    main()

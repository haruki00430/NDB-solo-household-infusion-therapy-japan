"""
Use Word COM to find the page and line number of anchor phrases in the final
clean manuscript. Page/line numbers are generated from the rendered document,
not guessed, per Work Order 04 requirements.
"""
import json
import win32com.client

DOCX_PATH = r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\04_Manuscripts\major_revision\final\manuscript_main_IJB_major_revision_clean.docx"

ANCHORS = {
    "abstract_background_start": "Older adults living alone are often described",
    "abstract_conclusion_53pct": "The estimate was attenuated by 53%",
    "intro_research_question": "Do prefecture-level measures of older adults living alone identify",
    "methods_study_design": "We conducted a nationwide ecological study using Japanese prefectures",
    "methods_outcome_g004": "The outcome was derived from the 10th NDB Open Data",
    "methods_g004_availability": "Prefecture-by-age cross-tabulated counts for G004 were not publicly available",
    "methods_primary_exposure": "The prespecified primary exposure, unchanged from the original submission",
    "methods_alternative_exposure": "As a complementary exposure-definition sensitivity analysis",
    "methods_ageing_rate": "Prefectural ageing rate (percentage of the population aged",
    "methods_healthcare_supply": "General hospital beds per 100,000 population",
    "methods_wbgt": "we used official wet-bulb globe temperature",
    "methods_statistical_analysis": "we fit four cumulative, hierarchical linear regression models",
    "methods_multicollinearity": "We did not use multicollinearity as a reason to avoid adjustment",
    "results_unadjusted_OA": "The primary exposure was associated with large-volume infusion therapy utilization in the unadjusted model",
    "results_OB_attenuation": "Adding prefectural ageing rate to the same model (O-B) changed the exposure coefficient",
    "results_OC_OD": "Adding general hospital beds per 100,000 (O-C) reduced the exposure coefficient further",
    "results_legacy_denominator": "Repeating O-A",
    "results_alternative_exposure": "The alternative exposure (percentage of the 65+ population living alone) showed no evidence",
    "results_sensitivity_hokkaido": "Cook's distance for O-D identified Hokkaido as the most influential prefecture",
    "results_nonlinearity": "A quadratic term for the primary exposure did not improve model fit",
    "results_wbgt33": "Days with WBGT \u2265 33\u00b0C showed a nominal association",
    "results_comparison_outcome": "The primary exposure's standardized association with general outpatient utilization",
    "discussion_principal_result": "The prespecified prefecture-level living-alone measure was associated",
    "discussion_burden_vs_prevalence": "Two conceptually distinct prefecture-level constructs were examined",
    "discussion_limitations": "Limitations include:",
    "conclusions": "The initially observed prefecture-level association between a living-alone measure",
    "data_availability_github": "github.com/haruki00430/NDB_XXX_heatwave_heatstroke",
    "ai_statement": "During the preparation of the original submission and this revision",
    "reference_miyatake": "Miyatake N, Sakano N, Murakami S (2012)",
    "table1_heading": "Table 1. Descriptive Statistics of Prefecture-Level Variables",
    "table2_heading": "Table 2. Original-Exposure Hierarchical Models",
    "figure1_caption": "Fig. 1 Coefficient plot for the primary exposure",
}


def main():
    word = win32com.client.gencache.EnsureDispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(DOCX_PATH)

    results = {}
    for key, phrase in ANCHORS.items():
        find_range = doc.Content
        found = find_range.Find.Execute(FindText=phrase, MatchCase=False, Forward=True)
        if found:
            page = find_range.Information(3)  # wdActiveEndPageNumber
            line = find_range.Information(10)  # wdFirstCharacterLineNumber
            results[key] = {"phrase": phrase, "page": page, "line": line}
        else:
            results[key] = {"phrase": phrase, "page": None, "line": None}

    doc.Close(False)
    word.Quit()

    out_path = r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\04_Manuscripts\major_revision\working\page_line_lookup.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    for key, val in results.items():
        print(f"{key}: page={val['page']} line={val['line']}")


if __name__ == "__main__":
    main()

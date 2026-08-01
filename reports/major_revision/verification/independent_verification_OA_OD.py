"""
Independent verification of O-A..O-D (original exposure) coefficients.

Deliberately does NOT import _common.py or reuse any of the pipeline's helper
functions -- uses a separate code path (statsmodels formula API) to recompute
the four HC3 coefficients and compare to the pipeline's own output CSV within
a strict numerical tolerance (1e-6 relative).
"""
import pandas as pd
import statsmodels.formula.api as smf

DATA_PATH = r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\02_Data\interim\major_revision\prefecture_analysis.csv"
RESULTS_PATH = r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\03_Analysis\results\major_revision\original_exposure_model_results.csv"

df = pd.read_csv(DATA_PATH, dtype={"pref_code": str})

formulas = {
    "O-A": "large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct",
    "O-B": "large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct",
    "O-C": "large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct + general_hospital_beds_per_100k",
    "O-D": "large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct + general_hospital_beds_per_100k + wbgt_days_ge28",
}

pipeline = pd.read_csv(RESULTS_PATH)
pipeline_hc3 = pipeline[
    (pipeline["se_type"] == "HC3")
    & (pipeline["coef_type"] == "unstandardized")
    & (pipeline["variable"] == "original_elderly_solo_household_pct")
    & (pipeline["denominator"] == "primary_2023_population")
].set_index("model")

TOL = 1e-6
all_pass = True
for model_name, formula in formulas.items():
    m = smf.ols(formula, data=df).fit(cov_type="HC3")
    coef = m.params["original_elderly_solo_household_pct"]
    se = m.bse["original_elderly_solo_household_pct"]
    p = m.pvalues["original_elderly_solo_household_pct"]
    ci = m.conf_int().loc["original_elderly_solo_household_pct"]

    ref = pipeline_hc3.loc[model_name]
    diffs = {
        "coef": abs(coef - ref["coef"]),
        "se": abs(se - ref["se"]),
        "p": abs(p - ref["p_value"]),
        "ci_low": abs(ci[0] - ref["ci_low"]),
        "ci_high": abs(ci[1] - ref["ci_high"]),
    }
    max_diff = max(diffs.values())
    status = "PASS" if max_diff < TOL else "FAIL"
    if status == "FAIL":
        all_pass = False
    print(f"{model_name}: independent_coef={coef:.6f} pipeline_coef={ref['coef']:.6f} max_diff={max_diff:.2e} [{status}]")

print()
print("ALL PASS" if all_pass else "SOME FAILED")
assert all_pass

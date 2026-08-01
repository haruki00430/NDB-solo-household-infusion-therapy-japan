"""
Major Revision 統計解析 10: 旧曝露(O) vs 新曝露(N) の並置比較（WORK_ORDER_03 Part 5）

両曝露を同一モデルに投入することはせず、別々の推定対象（estimand）として並べる。
「旧曝露が誤りで新曝露のみ正しい」とは述べず、両者が異なる問いに答えていることを示す。

出力:
  - results/original_vs_new_exposure_comparison.csv
"""
import pandas as pd

from _common import RESULTS_DIR

O_EXPOSURE = "original_elderly_solo_household_pct"
N_EXPOSURE = "older_living_alone_pct"


def get_row(coef_df, model, variable, se_type="HC3", coef_type="unstandardized"):
    sub = coef_df[
        (coef_df["model"] == model)
        & (coef_df["variable"] == variable)
        & (coef_df["se_type"] == se_type)
        & (coef_df["coef_type"] == coef_type)
    ]
    if "denominator" in sub.columns:
        sub = sub[sub["denominator"] == "primary_2023_population"]
    return sub.iloc[0]


def get_fit(fit_df, model):
    sub = fit_df[fit_df["model"] == model]
    if "denominator" in sub.columns:
        sub = sub[sub["denominator"] == "primary_2023_population"]
    return sub.iloc[0]


def main():
    o_coef = pd.read_csv(RESULTS_DIR / "original_exposure_model_results.csv")
    o_fit = pd.read_csv(RESULTS_DIR / "original_exposure_model_fit.csv")
    n_coef = pd.read_csv(RESULTS_DIR / "model_results.csv")
    n_fit = pd.read_csv(RESULTS_DIR / "model_fit.csv")

    rows = []
    pairs = [
        ("unadjusted", "O-A", "model1"),
        ("fully_adjusted", "O-D", "model4"),
    ]
    definitions = {
        "O": "Percentage of ALL households in the prefecture consisting of one person aged >=65 "
        "(prefecture-level population/service-burden indicator; denominator = all households)",
        "N": "Percentage of the prefecture's 65+ population living alone "
        "(prevalence of living-alone status within the older population; denominator = 65+ population)",
    }

    for stage, o_model, n_model in pairs:
        o_unstd = get_row(o_coef, o_model, O_EXPOSURE)
        o_std = get_row(o_coef, o_model, O_EXPOSURE, coef_type="standardized")
        o_fitrow = get_fit(o_fit, o_model)

        n_unstd = get_row(n_coef, n_model, N_EXPOSURE)
        n_std = get_row(n_coef, n_model, N_EXPOSURE, coef_type="standardized")
        n_fitrow = get_fit(n_fit, n_model)

        rows.append(
            {
                "stage": stage,
                "estimand": "O (original/submitted)",
                "model_label": o_model,
                "definition": definitions["O"],
                "unstd_coef": o_unstd["coef"],
                "unstd_ci_low": o_unstd["ci_low"],
                "unstd_ci_high": o_unstd["ci_high"],
                "unstd_p": o_unstd["p_value"],
                "std_coef": o_std["coef"],
                "std_ci_low": o_std["ci_low"],
                "std_ci_high": o_std["ci_high"],
                "exposure_partial_r2": o_fitrow["exposure_partial_r2"],
                "adj_r_squared": o_fitrow["adj_r_squared"],
            }
        )
        rows.append(
            {
                "stage": stage,
                "estimand": "N (new/complementary)",
                "model_label": n_model,
                "definition": definitions["N"],
                "unstd_coef": n_unstd["coef"],
                "unstd_ci_low": n_unstd["ci_low"],
                "unstd_ci_high": n_unstd["ci_high"],
                "unstd_p": n_unstd["p_value"],
                "std_coef": n_std["coef"],
                "std_ci_low": n_std["ci_low"],
                "std_ci_high": n_std["ci_high"],
                "exposure_partial_r2": n_fitrow["exposure_partial_r2"],
                "adj_r_squared": n_fitrow["adj_r_squared"],
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(RESULTS_DIR / "original_vs_new_exposure_comparison.csv", index=False, encoding="utf-8-sig")

    print("[OK] original_vs_new_exposure_comparison.csv written")
    print(out.to_string(index=False))
    print()
    print("Interpretation note (NOT overwritten elsewhere): O and N answer different questions")
    print("and have different relationships with population ageing (r=0.625 vs r=-0.242,")
    print("see reanalysis_report.md section 2.1). Neither is 'the correct exposure' in isolation.")


if __name__ == "__main__":
    main()

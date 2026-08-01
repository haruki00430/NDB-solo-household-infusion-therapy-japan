"""
Major Revision 統計解析 07: 旧曝露（original_elderly_solo_household_pct）の階層調整モデル

WORK_ORDER_03 Part 2 の実装。Reviewer 2 の最低限の要求
"include prefectural ageing rate alongside elderly solo household rate and show how
the estimate changes" に直接回答するため、投稿時の曝露（旧曝露）を保持したまま
高齢化率・医療供給・WBGTを順に追加する。新曝露（older_living_alone_pct）には置換しない。

Model sequence（すべて累積）:
  O-A: 旧曝露のみ
  O-B: 旧曝露 + 高齢化率
  O-C: 旧曝露 + 高齢化率 + 一般病床数(100k対)
  O-D: 旧曝露 + 高齢化率 + 一般病床数 + WBGT>=28日数

Primary outcome: 2023年人口分母（Work Order 01と同一定義）。
Legacy outcome: 投稿時と同一の2020年人口分母（別セットとして分離、混同しない）。

出力:
  - results/original_exposure_model_results.csv
  - results/original_exposure_model_fit.csv
  - results/original_exposure_vif.csv
  - results/original_exposure_attenuation.csv
  - results/tables/table_original_exposure_hierarchy.csv
"""
import pandas as pd

from _common import (
    CONFIG,
    OUTCOME,
    PROJECT_ROOT,
    RESULTS_DIR,
    compute_vif,
    fit_ols,
    load_dataset,
    model_fit_row,
    partial_r2,
    standardized_coefs,
    unstandardized_rows,
)

EXPOSURE = "original_elderly_solo_household_pct"

O_MODELS = {
    "O-A": [],
    "O-B": ["ageing_rate_pct"],
    "O-C": ["ageing_rate_pct", "general_hospital_beds_per_100k"],
    "O-D": ["ageing_rate_pct", "general_hospital_beds_per_100k", "wbgt_days_ge28"],
}


def fit_hierarchy(df: pd.DataFrame, outcome_col: str, denominator_label: str):
    y = df[outcome_col]
    coef_rows, fit_rows, vif_rows = [], [], []

    for model_name, adjust in O_MODELS.items():
        cols = [EXPOSURE] + adjust
        X = df[cols]
        formula = f"{outcome_col} ~ {' + '.join(cols)}"

        model_hc3 = fit_ols(y, X, robust="HC3")
        rows_hc3 = unstandardized_rows(model_hc3, model_name)
        rows_hc3["se_type"] = "HC3"
        rows_hc3["coef_type"] = "unstandardized"
        rows_hc3["denominator"] = denominator_label

        model_classical = fit_ols(y, X, robust=None)
        rows_classical = unstandardized_rows(model_classical, model_name)
        rows_classical["se_type"] = "classical_ols"
        rows_classical["coef_type"] = "unstandardized"
        rows_classical["denominator"] = denominator_label

        std_rows = standardized_coefs(y, X, robust="HC3").reset_index().rename(columns={"index": "variable"})
        std_rows["model"] = model_name
        std_rows["se_type"] = "HC3"
        std_rows["coef_type"] = "standardized"
        std_rows = std_rows.rename(
            columns={"std_coef": "coef", "std_ci_low": "ci_low", "std_ci_high": "ci_high", "std_p": "p_value"}
        )
        std_rows["se"] = float("nan")
        std_rows["denominator"] = denominator_label

        coef_rows.extend([rows_hc3, rows_classical, std_rows[rows_hc3.columns]])

        p_r2 = partial_r2(y, X, EXPOSURE)
        fit_row = model_fit_row(model_classical, model_name)
        fit_row["formula"] = formula
        fit_row["exposure"] = EXPOSURE
        fit_row["exposure_partial_r2"] = p_r2
        fit_row["df_resid"] = model_classical.df_resid
        fit_row["denominator"] = denominator_label
        fit_rows.append(fit_row)

        vif_df = compute_vif(X)
        vif_df["model"] = model_name
        vif_df["denominator"] = denominator_label
        vif_rows.append(vif_df)

    return pd.concat(coef_rows, ignore_index=True), pd.DataFrame(fit_rows), pd.concat(vif_rows, ignore_index=True)


def build_attenuation_table(coef_df: pd.DataFrame, fit_df: pd.DataFrame, denominator_label: str) -> pd.DataFrame:
    hc3_unstd = coef_df[
        (coef_df["denominator"] == denominator_label)
        & (coef_df["se_type"] == "HC3")
        & (coef_df["coef_type"] == "unstandardized")
        & (coef_df["variable"] == EXPOSURE)
    ].set_index("model")
    hc3_std = coef_df[
        (coef_df["denominator"] == denominator_label)
        & (coef_df["se_type"] == "HC3")
        & (coef_df["coef_type"] == "standardized")
        & (coef_df["variable"] == EXPOSURE)
    ].set_index("model")
    fit = fit_df[fit_df["denominator"] == denominator_label].set_index("model")

    beta_a = hc3_unstd.loc["O-A", "coef"]
    beta_b = hc3_unstd.loc["O-B", "coef"]
    std_a = hc3_std.loc["O-A", "coef"]
    std_b = hc3_std.loc["O-B", "coef"]

    row = {
        "denominator": denominator_label,
        "beta_O_A": beta_a,
        "beta_O_B": beta_b,
        "absolute_change_B_minus_A": beta_b - beta_a,
        "ratio_B_over_A": beta_b / beta_a if beta_a != 0 else float("nan"),
        "descriptive_pct_attenuation": 100 * (beta_a - beta_b) / beta_a if beta_a != 0 else float("nan"),
        "std_beta_O_A": std_a,
        "std_beta_O_B": std_b,
        "std_absolute_change_B_minus_A": std_b - std_a,
        "std_descriptive_pct_attenuation": 100 * (std_a - std_b) / std_a if std_a != 0 else float("nan"),
        "partial_r2_O_A": fit.loc["O-A", "exposure_partial_r2"],
        "partial_r2_O_B": fit.loc["O-B", "exposure_partial_r2"],
        "partial_r2_change": fit.loc["O-B", "exposure_partial_r2"] - fit.loc["O-A", "exposure_partial_r2"],
        "adj_r2_O_A": fit.loc["O-A", "adj_r_squared"],
        "adj_r2_O_B": fit.loc["O-B", "adj_r_squared"],
        "aicc_O_A": fit.loc["O-A", "aicc"],
        "aicc_O_B": fit.loc["O-B", "aicc"],
        "note": "descriptive attenuation only; NOT mediation or causal share explained by ageing",
    }
    return pd.DataFrame([row])


def main():
    df = load_dataset()
    legacy = pd.read_csv(
        PROJECT_ROOT / "02_Data" / "interim" / "major_revision" / "legacy_outcome_2020denominator.csv",
        dtype={"pref_code": str},
    )
    df_legacy = df.merge(legacy[["pref_code", "legacy_infusion_rate_per100k"]], on="pref_code", validate="one_to_one")

    coef_primary, fit_primary, vif_primary = fit_hierarchy(df, OUTCOME, "primary_2023_population")
    coef_legacy, fit_legacy, vif_legacy = fit_hierarchy(
        df_legacy, "legacy_infusion_rate_per100k", "legacy_2020_population"
    )

    coef_all = pd.concat([coef_primary, coef_legacy], ignore_index=True)
    fit_all = pd.concat([fit_primary, fit_legacy], ignore_index=True)
    vif_all = pd.concat([vif_primary, vif_legacy], ignore_index=True)

    attenuation_primary = build_attenuation_table(coef_all, fit_all, "primary_2023_population")
    attenuation_legacy = build_attenuation_table(coef_all, fit_all, "legacy_2020_population")
    attenuation = pd.concat([attenuation_primary, attenuation_legacy], ignore_index=True)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "tables").mkdir(parents=True, exist_ok=True)

    coef_all.to_csv(RESULTS_DIR / "original_exposure_model_results.csv", index=False, encoding="utf-8-sig")
    fit_all.to_csv(RESULTS_DIR / "original_exposure_model_fit.csv", index=False, encoding="utf-8-sig")
    vif_all.to_csv(RESULTS_DIR / "original_exposure_vif.csv", index=False, encoding="utf-8-sig")
    attenuation.to_csv(RESULTS_DIR / "original_exposure_attenuation.csv", index=False, encoding="utf-8-sig")

    # publication-ready hierarchy table (primary outcome only, HC3 unstandardized + standardized side by side)
    pub_rows = []
    for model_name in O_MODELS:
        unstd = coef_all[
            (coef_all["model"] == model_name)
            & (coef_all["denominator"] == "primary_2023_population")
            & (coef_all["se_type"] == "HC3")
            & (coef_all["coef_type"] == "unstandardized")
            & (coef_all["variable"] == EXPOSURE)
        ].iloc[0]
        std = coef_all[
            (coef_all["model"] == model_name)
            & (coef_all["denominator"] == "primary_2023_population")
            & (coef_all["se_type"] == "HC3")
            & (coef_all["coef_type"] == "standardized")
            & (coef_all["variable"] == EXPOSURE)
        ].iloc[0]
        fitrow = fit_all[(fit_all["model"] == model_name) & (fit_all["denominator"] == "primary_2023_population")].iloc[0]
        pub_rows.append(
            {
                "model": model_name,
                "n": fitrow["n"],
                "unstd_coef": unstd["coef"],
                "unstd_ci_low": unstd["ci_low"],
                "unstd_ci_high": unstd["ci_high"],
                "unstd_p": unstd["p_value"],
                "std_coef": std["coef"],
                "std_ci_low": std["ci_low"],
                "std_ci_high": std["ci_high"],
                "adj_r_squared": fitrow["adj_r_squared"],
                "exposure_partial_r2": fitrow["exposure_partial_r2"],
                "aicc": fitrow["aicc"],
            }
        )
    pd.DataFrame(pub_rows).to_csv(
        RESULTS_DIR / "tables" / "table_original_exposure_hierarchy.csv", index=False, encoding="utf-8-sig"
    )

    print("[OK] original_exposure_model_results.csv, _model_fit.csv, _vif.csv, _attenuation.csv written")
    print()
    print("=== Primary outcome (2023 population denominator) ===")
    print(fit_primary[["model", "n", "adj_r_squared", "exposure_partial_r2", "aicc"]].to_string(index=False))
    print()
    exposure_coefs_primary = coef_primary[
        (coef_primary["coef_type"] == "unstandardized")
        & (coef_primary["se_type"] == "HC3")
        & (coef_primary["variable"] == EXPOSURE)
    ]
    print(exposure_coefs_primary.to_string(index=False))
    print()
    print("=== O-A to O-B attenuation (primary outcome) ===")
    print(attenuation_primary.to_string(index=False))
    print()
    print("=== Legacy outcome (2020 population denominator, exact submitted) ===")
    print(fit_legacy[["model", "n", "adj_r_squared", "exposure_partial_r2", "aicc"]].to_string(index=False))
    exposure_coefs_legacy = coef_legacy[
        (coef_legacy["coef_type"] == "unstandardized")
        & (coef_legacy["se_type"] == "HC3")
        & (coef_legacy["variable"] == EXPOSURE)
    ]
    print(exposure_coefs_legacy.to_string(index=False))
    print()
    print("=== O-A to O-B attenuation (legacy outcome) ===")
    print(attenuation_legacy.to_string(index=False))


if __name__ == "__main__":
    main()

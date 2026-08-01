"""
Major Revision 統計解析 08: 旧曝露の感度分析・診断（WORK_ORDER_03 Part 3）

O-D（旧曝露のフル調整モデル）を基準に、以下を実施:
  1. 一般病床数 → 一般診療所数 への置換（O-C, O-D）
  2. 対数人口密度をO-Dへ追加
  3. 東京・大阪・神奈川の同時除外
  4. leave-one-prefecture-out（O-D、47回）
  5. Cook距離・レバレッジ・DFBETAs（O-D）
  6. outcomeの対数変換
  7. 人口重み付きWLS（探索的）
  8. WBGT>=28日数を>=31/>=33/累積超過量へ個別置換

出力:
  - results/original_exposure_sensitivity.csv
  - results/original_exposure_leave_one_out.csv
  - results/original_exposure_influence.csv
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

from _common import CONFIG, METRO_EXCLUDE, OUTCOME, RESULTS_DIR, fit_ols, load_dataset

EXPOSURE = "original_elderly_solo_household_pct"
O_D_ADJUST = ["ageing_rate_pct", "general_hospital_beds_per_100k", "wbgt_days_ge28"]


def coef_summary(model, label, n):
    ci = model.conf_int()
    return {
        "analysis": label,
        "n": n,
        "exposure_coef": model.params[EXPOSURE],
        "ci_low": ci[0][EXPOSURE],
        "ci_high": ci[1][EXPOSURE],
        "p_value": model.pvalues[EXPOSURE],
    }


def main():
    df = load_dataset()
    y = df[OUTCOME]
    rows = []

    # 0. O-D reference
    X0 = df[[EXPOSURE] + O_D_ADJUST]
    m0 = fit_ols(y, X0, robust="HC3")
    rows.append(coef_summary(m0, "O-D_reference", len(df)))

    # 1. beds -> clinics (in O-C and O-D adjustment sets)
    adjust_clinics_C = ["ageing_rate_pct", "general_clinics_per_100k"]
    adjust_clinics_D = ["ageing_rate_pct", "general_clinics_per_100k", "wbgt_days_ge28"]
    for label, adjust in [("O-C_beds_to_clinics", adjust_clinics_C), ("O-D_beds_to_clinics", adjust_clinics_D)]:
        X = df[[EXPOSURE] + adjust]
        m = fit_ols(y, X, robust="HC3")
        rows.append(coef_summary(m, label, len(df)))

    # 2. + log population density
    X2 = df[[EXPOSURE] + O_D_ADJUST + ["log_population_density"]]
    m2 = fit_ols(y, X2, robust="HC3")
    rows.append(coef_summary(m2, "O-D_add_log_population_density", len(df)))

    # 3. exclude Tokyo/Osaka/Kanagawa
    df_excl = df[~df["pref_code"].isin(METRO_EXCLUDE)]
    X3 = df_excl[[EXPOSURE] + O_D_ADJUST]
    y3 = df_excl[OUTCOME]
    m3 = fit_ols(y3, X3, robust="HC3")
    rows.append(coef_summary(m3, "O-D_exclude_tokyo_osaka_kanagawa", len(df_excl)))

    # 6. log-transform outcome
    y6 = np.log(df[OUTCOME])
    m6 = fit_ols(y6, X0, robust="HC3")
    rows.append(coef_summary(m6, "O-D_log_transform_outcome", len(df)))

    # 7. population-weighted WLS
    Xc = sm.add_constant(X0, has_constant="add")
    weights = df["total_population_2023"]
    m7 = sm.WLS(y, Xc, weights=weights).fit(cov_type="HC3")
    rows.append(coef_summary(m7, "O-D_population_weighted_wls", len(df)))

    # 8. heat-metric swap
    for metric in ["wbgt_days_ge31", "wbgt_days_ge33", "wbgt_cumulative_excess_28"]:
        adjust = ["ageing_rate_pct", "general_hospital_beds_per_100k", metric]
        X = df[[EXPOSURE] + adjust]
        m = fit_ols(y, X, robust="HC3")
        rows.append(coef_summary(m, f"O-D_heat_metric_{metric}", len(df)))

    sensitivity_df = pd.DataFrame(rows)

    # 4. leave-one-prefecture-out (O-D)
    loo_rows = []
    for pref in df["pref_code"]:
        df_loo = df[df["pref_code"] != pref]
        X_loo = df_loo[[EXPOSURE] + O_D_ADJUST]
        y_loo = df_loo[OUTCOME]
        m_loo = fit_ols(y_loo, X_loo, robust="HC3")
        ci = m_loo.conf_int()
        loo_rows.append(
            {
                "excluded_pref_code": pref,
                "n": len(df_loo),
                "exposure_coef": m_loo.params[EXPOSURE],
                "ci_low": ci[0][EXPOSURE],
                "ci_high": ci[1][EXPOSURE],
                "p_value": m_loo.pvalues[EXPOSURE],
            }
        )
    loo_df = pd.DataFrame(loo_rows)

    # 5. Cook's D, leverage, DFBETAs (O-D, classical OLS for influence stats)
    model_classical = fit_ols(y, X0, robust=None)
    influence = model_classical.get_influence()
    dfbetas = influence.dfbetas
    exposure_idx = list(model_classical.params.index).index(EXPOSURE)
    influence_df = pd.DataFrame(
        {
            "pref_code": df["pref_code"],
            "residual": model_classical.resid.values,
            "leverage": influence.hat_matrix_diag,
            "cooks_d": influence.cooks_distance[0],
            "dfbeta_exposure": dfbetas[:, exposure_idx],
        }
    ).sort_values("cooks_d", ascending=False)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sensitivity_df.to_csv(RESULTS_DIR / "original_exposure_sensitivity.csv", index=False, encoding="utf-8-sig")
    loo_df.to_csv(RESULTS_DIR / "original_exposure_leave_one_out.csv", index=False, encoding="utf-8-sig")
    influence_df.to_csv(RESULTS_DIR / "original_exposure_influence.csv", index=False, encoding="utf-8-sig")

    n = len(df)
    cooks_threshold = 4 / n
    print("[OK] original_exposure_sensitivity.csv, _leave_one_out.csv, _influence.csv written")
    print()
    print(sensitivity_df.to_string(index=False))
    print()
    print("LOO exposure coef range:", loo_df["exposure_coef"].min(), "-", loo_df["exposure_coef"].max())
    print("LOO: iterations where CI crosses zero:", (loo_df["ci_low"] * loo_df["ci_high"] < 0).sum(), "/", len(loo_df))
    print()
    print(f"Cook's D threshold (4/N) = {cooks_threshold:.4f}")
    print(influence_df[influence_df["cooks_d"] > cooks_threshold][["pref_code", "cooks_d", "leverage"]].to_string(index=False))


if __name__ == "__main__":
    main()

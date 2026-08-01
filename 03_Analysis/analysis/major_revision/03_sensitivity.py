"""
Major Revision 統計解析 03: 感度分析

major_revision_strategy_ja.md の感度分析仕様を実施し、Model 4（主要推論モデル）の
曝露係数（older_living_alone_pct）がどの程度頑健かを確認する。

実施内容:
  - 病床数 → 一般診療所数 への置換
  - 対数人口密度の追加調整
  - 東京・大阪・神奈川の同時除外
  - leave-one-prefecture-out（都道府県ごとの曝露係数・CIを全件保存）
  - outcomeの対数変換
  - 人口を重みとするWLS

出力:
  - results/sensitivity_analyses.csv （上記の各感度分析における曝露係数・CI・p・N）
  - results/leave_one_out.csv （都道府県ごとの曝露係数・CI）
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

from _common import CONFIG, METRO_EXCLUDE, OUTCOME, RESULTS_DIR, fit_ols, load_dataset


def coef_summary(model, exposure, label, n):
    ci = model.conf_int()
    return {
        "analysis": label,
        "n": n,
        "exposure_coef": model.params[exposure],
        "ci_low": ci[0][exposure],
        "ci_high": ci[1][exposure],
        "p_value": model.pvalues[exposure],
    }


def main():
    df = load_dataset()
    y = df[OUTCOME]

    primary_name = CONFIG["models"]["primary_inference_model"]
    spec = CONFIG["models"][primary_name]
    exposure = spec["exposure"]
    adjust = list(spec["adjust"])

    rows = []

    # 0. Model 4 そのもの（基準）
    X0 = df[[exposure] + adjust]
    m0 = fit_ols(y, X0, robust="HC3")
    rows.append(coef_summary(m0, exposure, "model4_reference", len(df)))

    # 1. 病床数 → 一般診療所数
    adjust_clinics = [
        "general_clinics_per_100k" if v == "general_hospital_beds_per_100k" else v for v in adjust
    ]
    X1 = df[[exposure] + adjust_clinics]
    m1 = fit_ols(y, X1, robust="HC3")
    rows.append(coef_summary(m1, exposure, "beds_to_clinics_substitution", len(df)))

    # 2. 対数人口密度の追加
    X2 = df[[exposure] + adjust + ["log_population_density"]]
    m2 = fit_ols(y, X2, robust="HC3")
    rows.append(coef_summary(m2, exposure, "add_log_population_density", len(df)))

    # 3. 東京・大阪・神奈川の同時除外
    df_excl = df[~df["pref_code"].isin(METRO_EXCLUDE)]
    X3 = df_excl[[exposure] + adjust]
    y3 = df_excl[OUTCOME]
    m3 = fit_ols(y3, X3, robust="HC3")
    rows.append(coef_summary(m3, exposure, "exclude_tokyo_osaka_kanagawa", len(df_excl)))

    # 4. outcomeの対数変換
    y4 = np.log(df[OUTCOME])
    m4 = fit_ols(y4, X0, robust="HC3")
    rows.append(coef_summary(m4, exposure, "log_transform_outcome", len(df)))

    # 5. 人口重み付きWLS（探索的）
    Xc = sm.add_constant(X0, has_constant="add")
    weights = df["total_population_2023"]
    m5 = sm.WLS(y, Xc, weights=weights).fit(cov_type="HC3")
    rows.append(coef_summary(m5, exposure, "population_weighted_wls", len(df)))

    sensitivity_df = pd.DataFrame(rows)

    # leave-one-prefecture-out
    loo_rows = []
    for pref in df["pref_code"]:
        df_loo = df[df["pref_code"] != pref]
        X_loo = df_loo[[exposure] + adjust]
        y_loo = df_loo[OUTCOME]
        m_loo = fit_ols(y_loo, X_loo, robust="HC3")
        ci = m_loo.conf_int()
        loo_rows.append(
            {
                "excluded_pref_code": pref,
                "n": len(df_loo),
                "exposure_coef": m_loo.params[exposure],
                "ci_low": ci[0][exposure],
                "ci_high": ci[1][exposure],
                "p_value": m_loo.pvalues[exposure],
            }
        )
    loo_df = pd.DataFrame(loo_rows)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sensitivity_df.to_csv(RESULTS_DIR / "sensitivity_analyses.csv", index=False, encoding="utf-8-sig")
    loo_df.to_csv(RESULTS_DIR / "leave_one_out.csv", index=False, encoding="utf-8-sig")

    print("[OK] sensitivity_analyses.csv, leave_one_out.csv written to", RESULTS_DIR)
    print()
    print(sensitivity_df.to_string(index=False))
    print()
    print("LOO exposure coef range:", loo_df["exposure_coef"].min(), "-", loo_df["exposure_coef"].max())
    print("LOO: iterations where CI crosses zero:", (loo_df["ci_low"] * loo_df["ci_high"] < 0).sum(), "/", len(loo_df))


if __name__ == "__main__":
    main()

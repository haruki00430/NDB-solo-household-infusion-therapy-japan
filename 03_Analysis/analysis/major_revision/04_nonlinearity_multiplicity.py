"""
Major Revision 統計解析 04: 非線形性の検証と多重性の調整

非線形性:
  - 線形モデル（Model 4）と、曝露の二次項を加えたモデルを partial F test と AICc で比較
  - 自然三次スプライン（df=3）を探索的感度分析として当てはめる
  - 中央値二分解析は補足資料専用（旧解析の再現、主結果には使わない）

多重性:
  - Model 4 を主要推論とし、WBGT>=31日数・>=33日数・累積超過量に置換した探索的モデルの
    p値に Benjamini-Hochberg FDR を適用する

出力:
  - results/nonlinearity.csv
  - results/multiplicity.csv
  - results/median_split_audit_only.csv （主結果ではないことを明記）
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrix
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests

from _common import CONFIG, OUTCOME, RESULTS_DIR, aicc, fit_ols, load_dataset


def main():
    df = load_dataset()
    y = df[OUTCOME]

    primary_name = CONFIG["models"]["primary_inference_model"]
    spec = CONFIG["models"][primary_name]
    exposure = spec["exposure"]
    adjust = list(spec["adjust"])

    # --- 非線形性: 線形 vs 二次項 ---
    X_lin = df[[exposure] + adjust]
    model_lin = fit_ols(y, X_lin, robust=None)

    df_quad = df.copy()
    df_quad[f"{exposure}_sq"] = df_quad[exposure] ** 2
    X_quad = df_quad[[exposure, f"{exposure}_sq"] + adjust]
    model_quad = fit_ols(y, X_quad, robust=None)

    anova_result = anova_lm(model_lin, model_quad)
    partial_f_p = anova_result["Pr(>F)"].iloc[1]

    nonlinearity_rows = [
        {
            "comparison": "linear_vs_quadratic",
            "aicc_linear": aicc(model_lin),
            "aicc_quadratic": aicc(model_quad),
            "partial_f_p_value": partial_f_p,
            "quadratic_term_coef": model_quad.params[f"{exposure}_sq"],
            "quadratic_term_p": model_quad.pvalues[f"{exposure}_sq"],
        }
    ]

    # --- 自然三次スプライン（df=3、探索的） ---
    spline_basis = dmatrix(f"cr({exposure}, df=3) - 1", data=df, return_type="dataframe")
    spline_basis.columns = [f"spline_{i}" for i in range(spline_basis.shape[1])]
    X_spline = pd.concat([spline_basis, df[adjust].reset_index(drop=True)], axis=1)
    X_spline.index = df.index
    model_spline = fit_ols(y, X_spline, robust=None)
    nonlinearity_rows.append(
        {
            "comparison": "linear_vs_natural_spline_df3",
            "aicc_linear": aicc(model_lin),
            "aicc_quadratic": aicc(model_spline),
            "partial_f_p_value": anova_lm(model_lin, model_spline)["Pr(>F)"].iloc[1],
            "quadratic_term_coef": np.nan,
            "quadratic_term_p": np.nan,
        }
    )

    nonlinearity_df = pd.DataFrame(nonlinearity_rows)

    # --- 中央値二分解析（補足資料専用、主結果に使わない） ---
    median_val = df[exposure].median()
    df_split = df.copy()
    df_split["exposure_group"] = np.where(df_split[exposure] >= median_val, "high", "low")
    median_rows = []
    for group, sub in df_split.groupby("exposure_group"):
        X_sub = sub[[exposure] + adjust]
        y_sub = sub[OUTCOME]
        if len(sub) <= len(adjust) + 2:
            continue
        m_sub = fit_ols(y_sub, X_sub, robust=None)
        ci = m_sub.conf_int()
        median_rows.append(
            {
                "group": group,
                "n": len(sub),
                "exposure_coef": m_sub.params[exposure],
                "ci_low": ci[0][exposure],
                "ci_high": ci[1][exposure],
                "p_value": m_sub.pvalues[exposure],
            }
        )
    median_split_df = pd.DataFrame(median_rows)

    # --- 多重性: 探索的暑熱指標の置換 ---
    heat_metrics = ["wbgt_days_ge31", "wbgt_days_ge33", "wbgt_cumulative_excess_28"]
    primary_heat = adjust[-1]  # wbgt_days_ge28 (Model4の最後の調整変数)
    base_adjust = adjust[:-1]

    multiplicity_rows = []
    for metric in heat_metrics:
        X_m = df[[exposure] + base_adjust + [metric]]
        m = fit_ols(y, X_m, robust="HC3")
        ci = m.conf_int()
        multiplicity_rows.append(
            {
                "heat_metric": metric,
                "exposure_coef": m.params[exposure],
                "ci_low": ci[0][exposure],
                "ci_high": ci[1][exposure],
                "p_value": m.pvalues[exposure],
                "heat_metric_coef": m.params[metric],
                "heat_metric_p": m.pvalues[metric],
            }
        )
    multiplicity_df = pd.DataFrame(multiplicity_rows)
    reject, p_adj, _, _ = multipletests(multiplicity_df["heat_metric_p"], method="fdr_bh")
    multiplicity_df["heat_metric_p_fdr_bh"] = p_adj
    multiplicity_df["significant_after_fdr"] = reject

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    nonlinearity_df.to_csv(RESULTS_DIR / "nonlinearity.csv", index=False, encoding="utf-8-sig")
    multiplicity_df.to_csv(RESULTS_DIR / "multiplicity.csv", index=False, encoding="utf-8-sig")
    median_split_df.to_csv(RESULTS_DIR / "median_split_audit_only.csv", index=False, encoding="utf-8-sig")

    print("[OK] nonlinearity.csv, multiplicity.csv, median_split_audit_only.csv written to", RESULTS_DIR)
    print()
    print(nonlinearity_df.to_string(index=False))
    print()
    print(multiplicity_df.to_string(index=False))
    print()
    print("[NOTE] median_split_audit_only.csv is NOT primary evidence (dose-response), audit/appendix use only:")
    print(median_split_df.to_string(index=False))


if __name__ == "__main__":
    main()

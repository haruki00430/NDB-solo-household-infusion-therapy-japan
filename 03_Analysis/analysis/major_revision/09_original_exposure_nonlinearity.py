"""
Major Revision 統計解析 09: 旧曝露の非線形性・都市影響（WORK_ORDER_03 Part 4）

Reviewer 2 の非線形性懸念は投稿時の曝露（旧曝露）とその中央値層別解析に向けられたもの
であるため、旧曝露についてO-Dを基準とした非線形性評価を行う。

  - 線形 O-D
  - O-D + 中心化した旧曝露の二次項
  - O-D + 旧曝露の自然三次スプライン（df=3）

partial F検定・AICcで比較し、観測範囲全体で予測曲線と95%信頼帯を都道府県の実測点とともに図示する。
中央値二分解析は再現監査としてのみ保持する（用量反応の根拠としては使わない）。

出力:
  - results/original_exposure_nonlinearity.csv
  - results/original_exposure_median_split_audit_only.csv
  - results/figures/figure_original_exposure_nonlinearity.png (+ 元データCSV)
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from patsy import dmatrix
from statsmodels.stats.anova import anova_lm

from _common import CONFIG, OUTCOME, RESULTS_DIR, aicc, fit_ols, load_dataset

EXPOSURE = "original_elderly_solo_household_pct"
O_D_ADJUST = ["ageing_rate_pct", "general_hospital_beds_per_100k", "wbgt_days_ge28"]


def main():
    df = load_dataset()
    y = df[OUTCOME]
    X_lin = df[[EXPOSURE] + O_D_ADJUST]
    model_lin = fit_ols(y, X_lin, robust=None)

    # 二次項（中心化）
    df_quad = df.copy()
    centered = df_quad[EXPOSURE] - df_quad[EXPOSURE].mean()
    df_quad[f"{EXPOSURE}_c"] = centered
    df_quad[f"{EXPOSURE}_c_sq"] = centered**2
    X_quad = df_quad[[f"{EXPOSURE}_c", f"{EXPOSURE}_c_sq"] + O_D_ADJUST]
    model_quad = fit_ols(y, X_quad, robust=None)
    anova_quad = anova_lm(model_lin, model_quad)

    # 自然三次スプライン df=3
    spline_basis = dmatrix(f"cr({EXPOSURE}, df=3) - 1", data=df, return_type="dataframe")
    spline_basis.columns = [f"spline_{i}" for i in range(spline_basis.shape[1])]
    X_spline = pd.concat([spline_basis, df[O_D_ADJUST].reset_index(drop=True)], axis=1)
    X_spline.index = df.index
    model_spline = fit_ols(y, X_spline, robust=None)
    anova_spline = anova_lm(model_lin, model_spline)

    nonlinearity_rows = [
        {
            "comparison": "linear_vs_quadratic",
            "aicc_linear": aicc(model_lin),
            "aicc_alt": aicc(model_quad),
            "partial_f_p_value": anova_quad["Pr(>F)"].iloc[1],
            "quadratic_term_coef": model_quad.params[f"{EXPOSURE}_c_sq"],
            "quadratic_term_p": model_quad.pvalues[f"{EXPOSURE}_c_sq"],
        },
        {
            "comparison": "linear_vs_natural_spline_df3",
            "aicc_linear": aicc(model_lin),
            "aicc_alt": aicc(model_spline),
            "partial_f_p_value": anova_spline["Pr(>F)"].iloc[1],
            "quadratic_term_coef": np.nan,
            "quadratic_term_p": np.nan,
        },
    ]
    nonlinearity_df = pd.DataFrame(nonlinearity_rows)

    # median split (audit only)
    median_val = df[EXPOSURE].median()
    df_split = df.copy()
    df_split["exposure_group"] = np.where(df_split[EXPOSURE] >= median_val, "high", "low")
    median_rows = []
    for group, sub in df_split.groupby("exposure_group"):
        X_sub = sub[[EXPOSURE] + O_D_ADJUST]
        y_sub = sub[OUTCOME]
        if len(sub) <= len(O_D_ADJUST) + 2:
            continue
        m_sub = fit_ols(y_sub, X_sub, robust=None)
        ci = m_sub.conf_int()
        median_rows.append(
            {
                "group": group,
                "n": len(sub),
                "exposure_coef": m_sub.params[EXPOSURE],
                "ci_low": ci[0][EXPOSURE],
                "ci_high": ci[1][EXPOSURE],
                "p_value": m_sub.pvalues[EXPOSURE],
            }
        )
    median_split_df = pd.DataFrame(median_rows)

    # --- predicted curve (linear model, adjust vars held at mean) with 95% CI band ---
    exposure_range = np.linspace(df[EXPOSURE].min(), df[EXPOSURE].max(), 100)
    mean_adjust = df[O_D_ADJUST].mean()
    pred_X = pd.DataFrame({EXPOSURE: exposure_range})
    for col in O_D_ADJUST:
        pred_X[col] = mean_adjust[col]
    pred_X = pred_X[[EXPOSURE] + O_D_ADJUST]
    pred = model_lin.get_prediction(__import__("statsmodels.api", fromlist=["add_constant"]).add_constant(pred_X, has_constant="add"))
    pred_summary = pred.summary_frame(alpha=0.05)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "figures").mkdir(parents=True, exist_ok=True)

    nonlinearity_df.to_csv(RESULTS_DIR / "original_exposure_nonlinearity.csv", index=False, encoding="utf-8-sig")
    median_split_df.to_csv(RESULTS_DIR / "original_exposure_median_split_audit_only.csv", index=False, encoding="utf-8-sig")

    curve_source = pd.DataFrame(
        {
            "exposure": exposure_range,
            "predicted_mean": pred_summary["mean"],
            "ci_low": pred_summary["mean_ci_lower"],
            "ci_high": pred_summary["mean_ci_upper"],
        }
    )
    curve_source.to_csv(RESULTS_DIR / "figures" / "figure_original_exposure_nonlinearity_source.csv", index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(exposure_range, pred_summary["mean"], color="C0", label="Linear fit (O-D, other covariates at mean)")
    ax.fill_between(exposure_range, pred_summary["mean_ci_lower"], pred_summary["mean_ci_upper"], color="C0", alpha=0.2)
    ax.scatter(df[EXPOSURE], df[OUTCOME], color="black", alpha=0.6, s=20, label="Prefectures (observed)")
    ax.set_xlabel("Original exposure: elderly solo household % (all households)")
    ax.set_ylabel("Large-volume infusion procedure rate (per 100,000)")
    ax.set_title("Original exposure: linear fit with 95% CI (O-D adjusted)")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figures" / "figure_original_exposure_nonlinearity.png", dpi=200)
    plt.close(fig)

    print("[OK] original_exposure_nonlinearity.csv, median_split_audit_only.csv, figure written")
    print()
    print(nonlinearity_df.to_string(index=False))
    print()
    print("[NOTE] median_split (audit only, not primary evidence):")
    print(median_split_df.to_string(index=False))


if __name__ == "__main__":
    main()

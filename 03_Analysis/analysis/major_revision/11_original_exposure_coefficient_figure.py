"""
Major Revision 統計解析 11: 旧曝露 O-A〜O-D 係数プロット（WORK_ORDER_03 Part 2 required figure）

出力:
  - results/figures/figure_original_exposure_coefficients.png
  - results/figures/figure_original_exposure_coefficients_source.csv
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from _common import RESULTS_DIR

EXPOSURE = "original_elderly_solo_household_pct"


def main():
    coef_df = pd.read_csv(RESULTS_DIR / "original_exposure_model_results.csv")
    sub = coef_df[
        (coef_df["variable"] == EXPOSURE)
        & (coef_df["se_type"] == "HC3")
        & (coef_df["coef_type"] == "unstandardized")
        & (coef_df["denominator"] == "primary_2023_population")
    ].copy()
    order = ["O-A", "O-B", "O-C", "O-D"]
    sub["model"] = pd.Categorical(sub["model"], categories=order, ordered=True)
    sub = sub.sort_values("model")

    source_path = RESULTS_DIR / "figures" / "figure_original_exposure_coefficients_source.csv"
    (RESULTS_DIR / "figures").mkdir(parents=True, exist_ok=True)
    sub.to_csv(source_path, index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(6, 4.5))
    y_pos = range(len(sub))
    ax.errorbar(
        sub["coef"],
        y_pos,
        xerr=[sub["coef"] - sub["ci_low"], sub["ci_high"] - sub["coef"]],
        fmt="o",
        color="C0",
        ecolor="C0",
        capsize=4,
    )
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(order)
    ax.invert_yaxis()
    ax.set_xlabel("Original-exposure coefficient (HC3 95% CI)\nInfusion rate per 100,000 per percentage-point")
    ax.set_title("Original exposure (elderly solo household %):\ncoefficient across O-A→O-D adjustment")
    for i, (_, row) in enumerate(sub.iterrows()):
        p_label = "p<0.001" if row["p_value"] < 0.001 else f"p={row['p_value']:.3f}"
        ax.annotate(p_label, (row["ci_high"], i), textcoords="offset points", xytext=(6, 0), fontsize=8, va="center")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figures" / "figure_original_exposure_coefficients.png", dpi=200)
    plt.close(fig)

    print("[OK] figure_original_exposure_coefficients.png + source CSV written")
    print(sub[["model", "coef", "ci_low", "ci_high", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()

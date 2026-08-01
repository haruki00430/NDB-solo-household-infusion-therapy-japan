"""
Major Revision 統計解析 12: Online Resource 1 Figure S1
（主曝露 O-A〜O-D 係数プロット、2023年分母 vs 2020年分母の並置比較）

本文Figure 1（2023年分母のみ）と同じ曝露・モデル系列を、投稿時分母（2020年）の
Legacy系列と並べて示す。データは既存の original_exposure_model_results.csv
（03_Analysis/analysis/major_revision/09,10番のスクリプトで生成済み）から読み込むのみで、
新規解析は行わない。

出力:
  - results/figures/figure_s1_denominator_comparison.png
  - results/figures/figure_s1_denominator_comparison_source.csv
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from _common import RESULTS_DIR

EXPOSURE = "original_elderly_solo_household_pct"
ORDER = ["O-A", "O-B", "O-C", "O-D"]


def main():
    coef_df = pd.read_csv(RESULTS_DIR / "original_exposure_model_results.csv")
    sub = coef_df[
        (coef_df["variable"] == EXPOSURE)
        & (coef_df["se_type"] == "HC3")
        & (coef_df["coef_type"] == "unstandardized")
    ].copy()
    sub["model"] = pd.Categorical(sub["model"], categories=ORDER, ordered=True)
    sub = sub.sort_values(["model", "denominator"])

    (RESULTS_DIR / "figures").mkdir(parents=True, exist_ok=True)
    source_path = RESULTS_DIR / "figures" / "figure_s1_denominator_comparison_source.csv"
    sub.to_csv(source_path, index=False, encoding="utf-8-sig")

    primary = sub[sub["denominator"] == "primary_2023_population"].set_index("model").loc[ORDER]
    legacy = sub[sub["denominator"] == "legacy_2020_population"].set_index("model").loc[ORDER]

    y_base = list(range(len(ORDER)))
    offset = 0.15

    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.errorbar(
        primary["coef"], [y + offset for y in y_base],
        xerr=[primary["coef"] - primary["ci_low"], primary["ci_high"] - primary["coef"]],
        fmt="o", color="C0", ecolor="C0", capsize=4,
        label="Primary (2023 population denominator, matches main Fig. 1)",
    )
    ax.errorbar(
        legacy["coef"], [y - offset for y in y_base],
        xerr=[legacy["coef"] - legacy["ci_low"], legacy["ci_high"] - legacy["coef"]],
        fmt="s", color="C1", ecolor="C1", capsize=4,
        label="Legacy (originally submitted 2020 population denominator)",
    )
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(y_base)
    ax.set_yticklabels(ORDER)
    ax.invert_yaxis()
    ax.set_xlabel("Original-exposure coefficient (HC3 95% CI)\nInfusion rate per 100,000 per percentage-point")
    ax.set_title("Original exposure: outcome-denominator sensitivity\nacross O-A→O-D adjustment")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figures" / "figure_s1_denominator_comparison.png", dpi=200)
    plt.close(fig)

    print("[OK] figure_s1_denominator_comparison.png + source CSV written")
    print(sub[["model", "denominator", "coef", "ci_low", "ci_high", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()

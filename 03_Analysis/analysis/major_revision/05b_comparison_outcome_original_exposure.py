"""
Major Revision 統計解析 05b: Comparison-outcome analysis（ORIGINAL exposure基準）

05_comparison_outcome.py は config.yaml の primary_inference_model（model4 = new/complementary
exposure の完全調整モデル）を参照していたため、本文 Table 2 / Results section 7 が使う
ORIGINAL exposure（original_elderly_solo_household_pct, Model O-A = unadjusted）とは異なる
曝露で比較outcome分析が計算されていた。このスクリプトは ORIGINAL exposure・unadjusted (O-A) を
明示的に指定して同じ比較を再計算し、本文・Online Resource 1 の記載と整合させる。

出力:
  - results/comparison_outcome_original_exposure.csv
"""
from pathlib import Path

import pandas as pd
from scipy import stats as scipy_stats

from _common import CONFIG, OUTCOME, RESULTS_DIR, load_dataset, standardized_coefs

import importlib
_cc = importlib.import_module("05_comparison_outcome")
parse_patient_survey = _cc.parse_patient_survey
SURVEY_PATH = _cc.SURVEY_PATH


def main():
    import yaml
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    with open(PROJECT_ROOT / "config" / "config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    name_to_code = {v: k for k, v in config["prefecture_codes"].items()}

    survey = parse_patient_survey(SURVEY_PATH)
    survey["pref_code"] = survey["都道府県"].map(name_to_code)
    assert survey["pref_code"].isna().sum() == 0

    df = load_dataset().merge(survey[["pref_code", "outpatient_rate_per100k"]], on="pref_code", validate="one_to_one")
    assert len(df) == 47

    exposure = config["variables"]["primary_exposure"]["original"]["name"]

    rows = []
    for outcome_col, label in [(OUTCOME, "primary_outcome_infusion"), ("outpatient_rate_per100k", "comparison_outcome_outpatient")]:
        y = df[outcome_col]
        x = df[exposure]
        r, p_r = scipy_stats.pearsonr(x, y)
        std = standardized_coefs(y, df[[exposure]], robust="HC3")
        rows.append(
            {
                "outcome": label,
                "pearson_r": r,
                "pearson_p": p_r,
                "r_squared": r**2,
                "standardized_beta": std.loc[exposure, "std_coef"],
                "std_ci_low": std.loc[exposure, "std_ci_low"],
                "std_ci_high": std.loc[exposure, "std_ci_high"],
                "std_p": std.loc[exposure, "std_p"],
            }
        )

    out = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "comparison_outcome_original_exposure.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    with open(RESULTS_DIR / "comparison_outcome_original_exposure_report.txt", "w", encoding="utf-8") as f:
        f.write(f"exposure used: {exposure}\n")
        f.write(out.to_string(index=False))
        f.write("\n")

    print("[OK] comparison_outcome_original_exposure.csv written to", out_path)
    print(f"exposure used: {exposure}")


if __name__ == "__main__":
    main()

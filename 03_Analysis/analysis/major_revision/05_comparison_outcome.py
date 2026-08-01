"""
Major Revision 統計解析 05: Comparison-outcome analysis（旧 negative control の再構築）

Reviewer 2 comment #5への対応:
  - 「6倍」という raw coefficient 比較は廃止する（アウトカムの尺度が異なるため）。
  - 一般外来利用は "negative control" ではなく "exploratory comparison-outcome analysis" と呼ぶ。
  - 標準化係数・Pearson r・R2・95%CIのみで比較する。

データソース: 02_Data/raw/patient_survey_r5_t36_pref_age.csv （R5患者調査、既存パース関数を流用）

出力:
  - results/comparison_outcome.csv
"""
import csv
import unicodedata
from pathlib import Path

import pandas as pd
import yaml
from scipy import stats as scipy_stats

from _common import CONFIG, OUTCOME, RESULTS_DIR, load_dataset, standardized_coefs

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SURVEY_PATH = PROJECT_ROOT / "02_Data" / "raw" / "patient_survey_r5_t36_pref_age.csv"

SURVEY_TO_FULL = {
    '北海道': '北海道', '青森': '青森県', '岩手': '岩手県', '宮城': '宮城県',
    '秋田': '秋田県', '山形': '山形県', '福島': '福島県', '茨城': '茨城県',
    '栃木': '栃木県', '群馬': '群馬県', '埼玉': '埼玉県', '千葉': '千葉県',
    '東京': '東京都', '神奈川': '神奈川県', '新潟': '新潟県', '富山': '富山県',
    '石川': '石川県', '福井': '福井県', '山梨': '山梨県', '長野': '長野県',
    '岐阜': '岐阜県', '静岡': '静岡県', '愛知': '愛知県', '三重': '三重県',
    '滋賀': '滋賀県', '京都': '京都府', '大阪': '大阪府', '兵庫': '兵庫県',
    '奈良': '奈良県', '和歌山': '和歌山県', '鳥取': '鳥取県', '島根': '島根県',
    '岡山': '岡山県', '広島': '広島県', '山口': '山口県', '徳島': '徳島県',
    '香川': '香川県', '愛媛': '愛媛県', '高知': '高知県', '福岡': '福岡県',
    '佐賀': '佐賀県', '長崎': '長崎県', '熊本': '熊本県', '大分': '大分県',
    '宮崎': '宮崎県', '鹿児島': '鹿児島県', '沖縄': '沖縄県',
}


def parse_patient_survey(filepath):
    results = []
    current_pref = None
    skip_prefectures = {'全国'}
    with open(filepath, encoding='cp932', errors='replace') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 6:
                continue
            row = [unicodedata.normalize('NFKC', cell).strip() for cell in row]
            if len(row) == 1 and row[0]:
                pref_short = row[0]
                current_pref = None if pref_short in skip_prefectures else pref_short
            elif len(row) == 9 and row[0] == '総数' and row[1] == '総数' and current_pref is not None:
                val_str = row[5]
                val = float(val_str) if val_str not in ('', '-') else float('nan')
                full_name = SURVEY_TO_FULL.get(current_pref)
                if full_name is None:
                    continue
                results.append({'都道府県': full_name, 'outpatient_rate_per100k': val})
                current_pref = None
    return pd.DataFrame(results)


def main():
    with open(PROJECT_ROOT / "config" / "config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    name_to_code = {v: k for k, v in config["prefecture_codes"].items()}

    survey = parse_patient_survey(SURVEY_PATH)
    survey["pref_code"] = survey["都道府県"].map(name_to_code)
    assert survey["pref_code"].isna().sum() == 0

    df = load_dataset().merge(survey[["pref_code", "outpatient_rate_per100k"]], on="pref_code", validate="one_to_one")
    assert len(df) == 47

    primary_name = CONFIG["models"]["primary_inference_model"]
    spec = CONFIG["models"][primary_name]
    exposure = spec["exposure"]

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
    out_path = RESULTS_DIR / "comparison_outcome.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[OK] comparison_outcome.csv written to {out_path}")
    print("[NOTE] labeled 'exploratory comparison-outcome analysis', not 'negative control'.")
    print("[NOTE] standardized comparisons only; raw-coefficient 'six-fold' claim is NOT reproduced here.")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

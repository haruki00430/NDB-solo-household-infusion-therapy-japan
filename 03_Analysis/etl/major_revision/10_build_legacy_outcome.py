"""
Major Revision ETL 10: 投稿原稿と同一の2020年人口分母によるレガシーoutcome

WORK_ORDER_03 Part 2: 「投稿時に使用した正確な2020年人口分母」を用いた
outcome（レガシー感度分析セット）を構築する。

投稿原稿の実際の計算式（03_Analysis/analysis/02_population_adjusted_analysis.py, line 101）:
  点滴注射_per100k = 点滴注射500mL以上_算定回数 / 総人口(prefecture_population_2020.csv) * 100000

本解析（Work Order 01）はこの分母を2023年人口推計に更新したが、更新の効果と
交絡調整の効果を分離するため、投稿時と全く同じ2020年分母によるoutcomeも別途保持する。

出力:
  - 02_Data/interim/major_revision/legacy_outcome_2020denominator.csv
    (pref_code, legacy_total_population_2020, legacy_infusion_rate_per100k)
"""
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
LEGACY_INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"

with open(PROJECT_ROOT / "config" / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)
NAME_TO_CODE = {v: k for k, v in config["prefecture_codes"].items()}


def main():
    pop2020 = pd.read_csv(LEGACY_INTERIM_DIR / "prefecture_population_2020.csv")
    pop2020["pref_code"] = pop2020["都道府県"].map(NAME_TO_CODE)
    assert pop2020["pref_code"].isna().sum() == 0
    pop2020 = pop2020.rename(columns={"総人口": "legacy_total_population_2020"})[
        ["pref_code", "legacy_total_population_2020"]
    ]

    infusion = pd.read_csv(LEGACY_INTERIM_DIR / "emergency_infusion_prefecture.csv")
    infusion["pref_code"] = infusion["都道府県"].map(NAME_TO_CODE)
    assert infusion["pref_code"].isna().sum() == 0
    infusion = infusion.rename(columns={"点滴注射500mL以上_算定回数": "g004_count_legacy_check"})[
        ["pref_code", "g004_count_legacy_check"]
    ]

    out = pop2020.merge(infusion, on="pref_code", validate="one_to_one")
    out["legacy_infusion_rate_per100k"] = (
        out["g004_count_legacy_check"] / out["legacy_total_population_2020"] * 100000
    )

    # クロスチェック: Work Order 01のg004_countと一致するはず（同じ抽出元）
    primary = pd.read_csv(INTERIM_DIR / "prefecture_analysis.csv", dtype={"pref_code": str})[
        ["pref_code", "g004_count"]
    ]
    out = out.merge(primary, on="pref_code", validate="one_to_one")
    mismatch = out[out["g004_count"] != out["g004_count_legacy_check"]]
    assert mismatch.empty, f"G004 count mismatch between WO01 and legacy extraction:\n{mismatch}"
    out = out.drop(columns=["g004_count_legacy_check"])

    assert len(out) == 47
    out = out.sort_values("pref_code").reset_index(drop=True)
    out_path = INTERIM_DIR / "legacy_outcome_2020denominator.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(out)} prefectures written to {out_path}")
    print("legacy_total_population_2020 sum:", out["legacy_total_population_2020"].sum())
    print(
        "NOTE: this legacy 2020 denominator sums to",
        out["legacy_total_population_2020"].sum(),
        "vs official 2020 census total population 126,146,099 -- the submitted pipeline's",
        "denominator source (0003445170, 一般世帯人員) undercounts the true census population",
        "by the institutional/group-living population not living in general households.",
        "This is documented as-is for legacy reproduction; it is not corrected here.",
    )


if __name__ == "__main__":
    main()

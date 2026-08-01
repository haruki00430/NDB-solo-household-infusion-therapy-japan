"""
Major Revision ETL 09: 47都道府県 解析用データセットの構築

すべての取得済み変数を都道府県コード（JIS 2桁）で結合し、
03_Analysis/analysis/major_revision/ の統計解析が読み込む単一データセットを作る。

入力:
  - 02_Data/interim/elderly_solo_household_rate.csv（既存、都道府県名キー）
  - 02_Data/interim/emergency_infusion_prefecture.csv（既存、都道府県名キー、G004算定回数）
  - 02_Data/interim/major_revision/pop2023_by_prefecture.csv
  - 02_Data/interim/major_revision/living_alone_exposure.csv
  - 02_Data/interim/major_revision/healthcare_supply_2023.csv
  - 02_Data/interim/major_revision/population_density_2023.csv
  - 02_Data/interim/major_revision/wbgt_summary_2023.csv

出力:
  - 02_Data/interim/major_revision/prefecture_analysis.csv（47行、解析用マスタ）
"""
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
LEGACY_INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim"

with open(PROJECT_ROOT / "config" / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)
NAME_TO_CODE = {v: k for k, v in config["prefecture_codes"].items()}


def load_named(path, rename_map):
    df = pd.read_csv(path)
    df["pref_code"] = df["都道府県"].map(NAME_TO_CODE)
    missing = df[df["pref_code"].isna()]["都道府県"].tolist()
    assert not missing, f"{path}: unmapped prefecture names {missing}"
    return df.rename(columns=rename_map)


def main():
    pop2023 = pd.read_csv(INTERIM_DIR / "pop2023_by_prefecture.csv", dtype={"pref_code": str})
    exposure = pd.read_csv(INTERIM_DIR / "living_alone_exposure.csv", dtype={"pref_code": str})
    supply = pd.read_csv(INTERIM_DIR / "healthcare_supply_2023.csv", dtype={"pref_code": str})
    density = pd.read_csv(INTERIM_DIR / "population_density_2023.csv", dtype={"pref_code": str})
    wbgt = pd.read_csv(INTERIM_DIR / "wbgt_summary_2023.csv", dtype={"pref_code": str})

    outcome = load_named(
        LEGACY_INTERIM_DIR / "emergency_infusion_prefecture.csv",
        {"点滴注射500mL以上_算定回数": "g004_count"},
    )[["pref_code", "g004_count"]]

    df = pop2023[["pref_code", "total_population_2023", "population_65plus_2023", "ageing_rate_pct"]].copy()
    df = df.merge(outcome, on="pref_code", validate="one_to_one")
    df["large_volume_infusion_procedure_rate"] = df["g004_count"] / df["total_population_2023"] * 100000

    df = df.merge(
        exposure[
            [
                "pref_code",
                "older_living_alone_pct",
                "original_elderly_solo_household_pct",
                "solo_65plus_persons_2020",
                "population_65plus_2020",
            ]
        ],
        on="pref_code",
        validate="one_to_one",
    )
    df = df.merge(
        supply[["pref_code", "general_hospital_beds_per_100k", "general_clinics_per_100k"]],
        on="pref_code",
        validate="one_to_one",
    )
    df = df.merge(
        density[["pref_code", "population_density_per_km2", "log_population_density"]],
        on="pref_code",
        validate="one_to_one",
    )
    df = df.merge(
        wbgt[
            [
                "pref_code",
                "n_stations",
                "wbgt_days_ge28",
                "wbgt_days_ge31",
                "wbgt_days_ge33",
                "wbgt_cumulative_excess_28",
            ]
        ],
        on="pref_code",
        validate="one_to_one",
    )

    # comparison outcome（既存の一般外来利用データがあれば結合、negative controlとは呼ばない）
    comparison_path = LEGACY_INTERIM_DIR.parent / "03_Analysis" / "results" / "outpatient_comparison.csv"

    assert len(df) == 47, f"Expected 47 prefectures, got {len(df)}"
    assert df.isna().sum().sum() == 0, f"Missing values found:\n{df.isna().sum()[df.isna().sum() > 0]}"

    df = df.sort_values("pref_code").reset_index(drop=True)
    out_path = INTERIM_DIR / "prefecture_analysis.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(df)} prefectures, {len(df.columns)} columns written to {out_path}")
    print("columns:", list(df.columns))


if __name__ == "__main__":
    main()

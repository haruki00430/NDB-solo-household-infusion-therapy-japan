"""
Major Revision ETL 04: 独居曝露指標（新・旧）の構築

新曝露: older_living_alone_pct = solo_65plus_persons_2020 / population_65plus_2020 * 100
  （65歳以上人口に占める、単独世帯で暮らす65歳以上人口の割合）
旧曝露: original_elderly_solo_household_pct = 既存 elderly_solo_household_rate.csv の「高齢者単独世帯率」
  （全世帯に占める65歳以上単独世帯率。Model 0=旧解析再現専用。分母が異なるため新指標と混同しない）

結合キーは都道府県コード（config.yaml prefecture_codes）を使用し、都道府県名の文字列結合は行わない。

入力:
  - 02_Data/interim/major_revision/census2020_solo65_by_prefecture.csv
  - 02_Data/interim/major_revision/census2020_age65_by_prefecture.csv
  - 02_Data/interim/elderly_solo_household_rate.csv（既存パイプライン出力、都道府県名キー）

出力:
  - 02_Data/interim/major_revision/living_alone_exposure.csv
"""
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
LEGACY_INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim"

with open(PROJECT_ROOT / "config" / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

CODE_TO_NAME = config["prefecture_codes"]
NAME_TO_CODE = {v: k for k, v in CODE_TO_NAME.items()}


def main():
    solo65 = pd.read_csv(INTERIM_DIR / "census2020_solo65_by_prefecture.csv", dtype={"pref_code": str})
    age65 = pd.read_csv(INTERIM_DIR / "census2020_age65_by_prefecture.csv", dtype={"pref_code": str})

    new_exposure = solo65.merge(age65, on="pref_code", how="inner", validate="one_to_one")
    assert len(new_exposure) == 47

    new_exposure["older_living_alone_pct"] = (
        new_exposure["solo_65plus_persons_2020"] / new_exposure["population_65plus_2020"] * 100
    )

    legacy = pd.read_csv(LEGACY_INTERIM_DIR / "elderly_solo_household_rate.csv")
    legacy["pref_code"] = legacy["都道府県"].map(NAME_TO_CODE)
    missing_names = legacy[legacy["pref_code"].isna()]["都道府県"].tolist()
    assert not missing_names, f"Unmapped prefecture names in legacy file: {missing_names}"

    legacy = legacy.rename(
        columns={
            "65歳以上単独世帯数": "legacy_solo65_households",
            "総世帯数": "legacy_total_households_2020",
            "高齢者単独世帯率": "original_elderly_solo_household_pct",
        }
    )[["pref_code", "legacy_solo65_households", "legacy_total_households_2020", "original_elderly_solo_household_pct"]]

    out = new_exposure.merge(legacy, on="pref_code", how="inner", validate="one_to_one")
    assert len(out) == 47

    # クロスチェック: 新規API由来のsolo65人数と、既存マイクロデータ抽出値が一致することを確認
    mismatch = out[out["solo_65plus_persons_2020"] != out["legacy_solo65_households"]]
    assert mismatch.empty, f"solo65 person count mismatch vs legacy extraction:\n{mismatch[['pref_code']]}"

    out = out.sort_values("pref_code").reset_index(drop=True)
    out_path = INTERIM_DIR / "living_alone_exposure.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(out)} prefectures written to {out_path}")
    print("[OK] new-exposure numerator cross-checked against legacy microdata extraction: exact match")
    print(
        "national older_living_alone_pct (population-weighted):",
        out["solo_65plus_persons_2020"].sum() / out["population_65plus_2020"].sum() * 100,
    )


if __name__ == "__main__":
    main()

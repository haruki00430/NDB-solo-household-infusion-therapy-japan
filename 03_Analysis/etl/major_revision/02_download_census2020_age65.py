"""
Major Revision ETL 02: 2020年国勢調査 都道府県別65歳以上人口

データソース: 総務省統計局「時系列データ 男女，年齢，配偶関係」
  統計表ID: 0003410381
  表章事項: 020 人口／cat01: 男女_総数(100)／cat02: 年齢(5歳階級)_総数(100),再掲65歳以上(400)
  time: 2020000000 (令和2年国勢調査)

取得内容:
  - 都道府県別 総人口（cat02=100, 2020年国勢調査、全数値）
  - 都道府県別 65歳以上人口（cat02=400, 再掲）

用途:
  - 新曝露 older_living_alone_pct の分母（65歳以上人口）
  - 既存 elderly_solo_household_rate.csv の65歳以上単独世帯数（分子）と結合して算出

出力:
  - 02_Data/raw/major_revision/estat_census2020_age65/raw_response.json
  - 02_Data/interim/major_revision/census2020_age65_by_prefecture.csv
"""
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
APP_ID = os.environ["ESTAT_APP_ID"]

STATS_DATA_ID = "0003410381"
URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "estat_census2020_age65"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

TIME_CODE = "2020000000"
CAT01_TOTAL = "100"  # 男女計
CAT02_TOTAL = "100"  # 年齢総数
CAT02_65PLUS = "400"  # （再掲）65歳以上
TAB_POPULATION = "020"  # 人口


def fetch():
    params = {
        "appId": APP_ID,
        "statsDataId": STATS_DATA_ID,
        "cdTab": TAB_POPULATION,
        "cdCat01": CAT01_TOTAL,
        "cdCat02": f"{CAT02_TOTAL},{CAT02_65PLUS}",
        "cdTime": TIME_CODE,
        "metaGetFlg": "N",
    }
    resp = requests.get(URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json(), resp.content


def main():
    data, raw_bytes = fetch()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    raw_path = RAW_DIR / "raw_response.json"
    raw_path.write_bytes(raw_bytes)
    sha256 = hashlib.sha256(raw_bytes).hexdigest()

    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if not isinstance(values, list):
        values = [values]

    rows = []
    for v in values:
        area_code5 = v["@area"]
        pref_code = area_code5[:2]
        cat02 = v["@cat02"]
        pop = int(v["$"])
        rows.append({"pref_code": pref_code, "cat02": cat02, "population": pop})

    df = pd.DataFrame(rows)
    total = (
        df[df["cat02"] == CAT02_TOTAL]
        .set_index("pref_code")["population"]
        .rename("total_population_2020_census")
    )
    pop65 = (
        df[df["cat02"] == CAT02_65PLUS]
        .set_index("pref_code")["population"]
        .rename("population_65plus_2020")
    )
    out = pd.concat([total, pop65], axis=1).reset_index()

    assert len(out) == 47, f"Expected 47 prefectures, got {len(out)}"
    assert out["pref_code"].nunique() == 47
    assert out.isna().sum().sum() == 0

    out = out.sort_values("pref_code").reset_index(drop=True)
    out_path = INTERIM_DIR / "census2020_age65_by_prefecture.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    manifest_row = {
        "variable": "total_population_2020_census, population_65plus_2020",
        "source_url": f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?statsDataId={STATS_DATA_ID}",
        "publisher": "総務省統計局 時系列データ「男女，年齢，配偶関係」（令和2年国勢調査）",
        "table_id": STATS_DATA_ID,
        "retrieved_at_utc": retrieved_at,
        "file_size_bytes": len(raw_bytes),
        "sha256": sha256,
        "license_note": "政府統計の総合窓口(e-Stat) 利用規約に基づく公開データ",
        "output_file": str(out_path.relative_to(PROJECT_ROOT)),
    }
    manifest_path = PROJECT_ROOT / "reports" / "major_revision" / "source_manifest.csv"
    manifest_df = pd.DataFrame([manifest_row])
    existing = pd.read_csv(manifest_path)
    manifest_df = pd.concat([existing, manifest_df], ignore_index=True)
    manifest_df.to_csv(manifest_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(out)} prefectures written to {out_path}")


if __name__ == "__main__":
    main()

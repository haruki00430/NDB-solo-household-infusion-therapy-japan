"""
Major Revision ETL 01: 2023年10月1日現在推計人口（都道府県・年齢5歳階級・男女計）

データソース: 総務省統計局「人口推計」各年10月1日現在人口 令和2年国勢調査基準
  統計表ID: 0004012968
  参考表022「都道府県，年齢（5歳階級），男女別人口－総人口」
  time=1801 (2023年10月1日現在)

取得内容:
  - 都道府県別 総人口（cat01=01000, cat02=000）
  - 都道府県別 65歳以上人口（cat01の65-69/70-74/75-79/80-84/85歳以上を合算, cat02=000）

出力:
  - 02_Data/raw/major_revision/estat_pop2023/raw_response.json（API生レスポンス、そのまま保存）
  - 02_Data/interim/major_revision/pop2023_by_prefecture.csv（都道府県コード, 総人口, 65歳以上人口, 高齢化率）

このスクリプトは02_Data/raw/を一切変更しない（新規サブフォルダへの追記のみ）。
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
APP_ID = os.environ["ESTAT_APP_ID"]

STATS_DATA_ID = "0004012968"
TIME_CODE = "1801"  # 2023年10月1日現在
URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "estat_pop2023"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# 65歳以上に合算する年齢5歳階級コード
AGE65_CODES = ["01014", "01015", "01016", "01017", "04018"]  # 65-69,70-74,75-79,80-84,85+
TOTAL_AGE_CODE = "01000"  # 総数


def fetch():
    params = {
        "appId": APP_ID,
        "statsDataId": STATS_DATA_ID,
        "cdCat02": "000",  # 男女計
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
        area_code5 = v["@area"]  # e.g. "01000"
        pref_code = area_code5[:2]
        if pref_code == "00":
            continue  # 全国は除外、都道府県のみ
        cat01 = v["@cat01"]
        pop = int(v["$"])
        rows.append({"pref_code": pref_code, "cat01": cat01, "population": pop})

    df = pd.DataFrame(rows)

    total = (
        df[df["cat01"] == TOTAL_AGE_CODE]
        .groupby("pref_code")["population"]
        .sum()
        .rename("total_population_2023")
    )
    pop65 = (
        df[df["cat01"].isin(AGE65_CODES)]
        .groupby("pref_code")["population"]
        .sum()
        .rename("population_65plus_2023")
    )

    out = pd.concat([total, pop65], axis=1).reset_index()
    out["ageing_rate_pct"] = out["population_65plus_2023"] / out["total_population_2023"] * 100

    assert len(out) == 47, f"Expected 47 prefectures, got {len(out)}"
    assert out["pref_code"].nunique() == 47

    out_path = INTERIM_DIR / "pop2023_by_prefecture.csv"
    out = out.sort_values("pref_code").reset_index(drop=True)
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    manifest_row = {
        "variable": "total_population_2023, population_65plus_2023, ageing_rate_pct",
        "source_url": f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?statsDataId={STATS_DATA_ID}",
        "publisher": "総務省統計局 人口推計（令和2年国勢調査基準）参考表022",
        "table_id": STATS_DATA_ID,
        "retrieved_at_utc": retrieved_at,
        "file_size_bytes": len(raw_bytes),
        "sha256": sha256,
        "license_note": "政府統計の総合窓口(e-Stat) 利用規約に基づく公開データ",
        "output_file": str(out_path.relative_to(PROJECT_ROOT)),
    }

    manifest_path = PROJECT_ROOT / "reports" / "major_revision" / "source_manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_df = pd.DataFrame([manifest_row])
    if manifest_path.exists():
        existing = pd.read_csv(manifest_path)
        manifest_df = pd.concat([existing, manifest_df], ignore_index=True)
    manifest_df.to_csv(manifest_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(out)} prefectures written to {out_path}")
    print(f"[OK] source manifest updated: {manifest_path}")


if __name__ == "__main__":
    main()

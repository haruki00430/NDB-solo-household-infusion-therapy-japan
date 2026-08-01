"""
Major Revision ETL 06: 2023年度 都道府県別人口密度（総面積1km2あたり）

データソース: 総務省統計局「都道府県データ 社会生活統計指標」
  統計表ID: 0000010201
  指標コード: #A01201（総面積1km2あたり人口密度）
  time: 2023100000（2023年度）

出力:
  - 02_Data/interim/major_revision/population_density_2023.csv
    (pref_code, population_density_per_km2, log_population_density)
"""
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import os

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
APP_ID = os.environ["ESTAT_APP_ID"]
URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

STATS_DATA_ID = "0000010201"
CAT01_DENSITY = "#A01201"
TIME_CODE = "2023100000"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "estat_pop2023"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)


def main():
    params = {
        "appId": APP_ID,
        "statsDataId": STATS_DATA_ID,
        "cdCat01": CAT01_DENSITY,
        "cdTime": TIME_CODE,
        "metaGetFlg": "N",
    }
    resp = requests.get(URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    raw_bytes = resp.content

    retrieved_at = datetime.now(timezone.utc).isoformat()
    raw_path = RAW_DIR / "population_density_raw_response.json"
    raw_path.write_bytes(raw_bytes)
    sha256 = hashlib.sha256(raw_bytes).hexdigest()

    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if not isinstance(values, list):
        values = [values]

    rows = []
    for v in values:
        area_code5 = v["@area"]
        if area_code5 == "00000" or len(area_code5) != 5 or area_code5[2:] != "000":
            continue
        rows.append({"pref_code": area_code5[:2], "population_density_per_km2": float(v["$"])})

    out = pd.DataFrame(rows).sort_values("pref_code").reset_index(drop=True)
    assert len(out) == 47, f"Expected 47 prefectures, got {len(out)}"
    assert out.isna().sum().sum() == 0

    out["log_population_density"] = np.log(out["population_density_per_km2"])

    out_path = INTERIM_DIR / "population_density_2023.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    manifest_row = {
        "variable": "population_density_per_km2, log_population_density",
        "source_url": f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?statsDataId={STATS_DATA_ID}",
        "publisher": "総務省統計局 都道府県データ 社会生活統計指標（#A01201 総面積1km2あたり人口密度）",
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
    print("density range:", out["population_density_per_km2"].min(), "-", out["population_density_per_km2"].max())


if __name__ == "__main__":
    main()

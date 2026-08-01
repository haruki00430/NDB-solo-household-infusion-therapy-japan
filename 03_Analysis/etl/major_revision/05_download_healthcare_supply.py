"""
Major Revision ETL 05: 2023年医療施設調査 都道府県別 医療供給指標

データソース: 厚生労働省「令和5年医療施設（静態・動態）調査 都道府県編」
  - 第15表 (0004024814): 病院の人口10万対病床数（病床の種類・都道府県別）
      cat01=8 → 一般病床（人口10万対、既に per-100k で提供される公式値）
  - 第25表 (0004024824): 一般診療所数（病床の有無等・都道府県別）
      cat01=1 → 施設数（総数）＝一般診療所数（実数）。人口10万対は自前の2023年人口推計で算出。

都道府県コードの対応（このMHLW統計表特有の規則）:
  area コード = 100 + 都道府県コード(1-47) * 10 （例: 00110=北海道=01, 00470=沖縄=47）
  指定都市・特別区・中核市の再掲行はこの規則に一致しないため自動的に除外される。

出力:
  - 02_Data/interim/major_revision/healthcare_supply_2023.csv
    (pref_code, general_hospital_beds_per_100k, general_clinics_count, general_clinics_per_100k)
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
URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "mhlw_iryo_shisetsu_2023"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

TIME_CODE = "2023000000"
STATS_ID_BEDS_PER_100K = "0004024814"  # T15
STATS_ID_CLINIC_COUNT = "0004024824"  # T25


def area_code_to_pref(area_code: str) -> str | None:
    n = int(area_code)
    if n <= 100 or n > 570:
        return None
    if (n - 100) % 10 != 0:
        return None  # 指定都市・特別区・中核市の再掲行を除外
    pref_num = (n - 100) // 10
    return f"{pref_num:02d}"


def fetch(stats_data_id: str, cd_cat01: str):
    params = {
        "appId": APP_ID,
        "statsDataId": stats_data_id,
        "cdCat01": cd_cat01,
        "cdTime": TIME_CODE,
        "metaGetFlg": "N",
    }
    resp = requests.get(URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json(), resp.content


def save_raw_and_manifest(raw_bytes, name, variable, stats_data_id, title, out_path):
    retrieved_at = datetime.now(timezone.utc).isoformat()
    raw_path = RAW_DIR / f"{name}_raw_response.json"
    raw_path.write_bytes(raw_bytes)
    sha256 = hashlib.sha256(raw_bytes).hexdigest()

    manifest_row = {
        "variable": variable,
        "source_url": f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?statsDataId={stats_data_id}",
        "publisher": f"厚生労働省 令和5年医療施設調査 都道府県編（{title}）",
        "table_id": stats_data_id,
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


def main():
    # --- 一般病床数（人口10万対、公式値） ---
    data_beds, raw_beds = fetch(STATS_ID_BEDS_PER_100K, cd_cat01="8")
    values = data_beds["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if not isinstance(values, list):
        values = [values]
    rows = []
    for v in values:
        pref_code = area_code_to_pref(v["@cat02"])
        if pref_code is None:
            continue
        rows.append({"pref_code": pref_code, "general_hospital_beds_per_100k": float(v["$"])})
    beds_df = pd.DataFrame(rows).sort_values("pref_code").reset_index(drop=True)
    assert len(beds_df) == 47, f"beds: expected 47 prefectures, got {len(beds_df)}"

    # --- 一般診療所数（実数） ---
    data_clinics, raw_clinics = fetch(STATS_ID_CLINIC_COUNT, cd_cat01="1")
    values = data_clinics["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if not isinstance(values, list):
        values = [values]
    rows = []
    for v in values:
        pref_code = area_code_to_pref(v["@cat02"])
        if pref_code is None:
            continue
        rows.append({"pref_code": pref_code, "general_clinics_count": int(v["$"])})
    clinics_df = pd.DataFrame(rows).sort_values("pref_code").reset_index(drop=True)
    assert len(clinics_df) == 47, f"clinics: expected 47 prefectures, got {len(clinics_df)}"

    pop2023 = pd.read_csv(
        INTERIM_DIR / "pop2023_by_prefecture.csv", dtype={"pref_code": str}
    )[["pref_code", "total_population_2023"]]

    out = beds_df.merge(clinics_df, on="pref_code", validate="one_to_one").merge(
        pop2023, on="pref_code", validate="one_to_one"
    )
    out["general_clinics_per_100k"] = out["general_clinics_count"] / out["total_population_2023"] * 100000

    assert len(out) == 47
    assert out.isna().sum().sum() == 0

    out_path = INTERIM_DIR / "healthcare_supply_2023.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")

    save_raw_and_manifest(
        raw_beds, "hospital_beds", "general_hospital_beds_per_100k",
        STATS_ID_BEDS_PER_100K, "第15表 人口10万対病床数", out_path,
    )
    save_raw_and_manifest(
        raw_clinics, "clinic_count", "general_clinics_count, general_clinics_per_100k",
        STATS_ID_CLINIC_COUNT, "第25表 一般診療所数", out_path,
    )

    print(f"[OK] {len(out)} prefectures written to {out_path}")
    print("national general_hospital_beds_per_100k mean:", out["general_hospital_beds_per_100k"].mean())
    print("national general_clinics_per_100k mean:", out["general_clinics_per_100k"].mean())


if __name__ == "__main__":
    main()

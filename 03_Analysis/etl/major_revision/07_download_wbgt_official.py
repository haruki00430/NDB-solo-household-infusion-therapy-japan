"""
Major Revision ETL 07: 環境省 熱中症予防情報サイト 公式WBGT実況値（2023年6-9月）

データソース: 環境省「熱中症予防情報サイト」実況値データ取得API
  URI: https://www.wbgt.env.go.jp/api/v1/getSurveyData
  仕様書: https://www.wbgt.env.go.jp/man15NH/wbgt_data_api_service_manual.pdf (第1.1版)
  location_type=2（都道府県別）, data_type=[0,1]（推定値+実測値＝サイト掲載の公式実況値と同じ定義）

このAPIの「都道府県コード」はJIS都道府県コードと異なり、北海道のみ14地域
（宗谷～檜山）に細分化されている。WBGT_PREF_TO_JIS でJISの47都道府県コードに
再集約する（北海道は14コードの地点を全て合算）。

1回のAPI呼び出しの上限が25,000件のため、(WBGTコード×月)単位でチャンク取得する。
既にダウンロード済みの生JSONはスキップする（再実行時のresume対応）。

出力:
  - 02_Data/raw/major_revision/env_wbgt_2023/{wbgt_code}_{yyyymm}.json（生レスポンス、都度保存）
  - 02_Data/interim/major_revision/wbgt_hourly_by_station.csv（観測所別・時刻別 生値）
"""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

URL = "https://www.wbgt.env.go.jp/api/v1/getSurveyData"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "env_wbgt_2023"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# WBGTサイト独自の都道府県コード → JIS都道府県コード（config.yamlのprefecture_codesに対応）
# 北海道は14地域（宗谷～檜山）を全てJIS "01" に集約する。
WBGT_PREF_TO_JIS = {
    # 北海道（14地域）
    "11": "01", "12": "01", "13": "01", "14": "01", "15": "01", "16": "01",
    "17": "01", "18": "01", "19": "01", "20": "01", "21": "01", "22": "01",
    "23": "01", "24": "01",
    # 東北
    "31": "02", "32": "05", "33": "03", "34": "04", "35": "06", "36": "07",
    # 関東
    "40": "08", "41": "09", "42": "10", "43": "11", "44": "13", "45": "12", "46": "14",
    # 甲信・東海
    "48": "20", "49": "19", "50": "22", "51": "23", "52": "21", "53": "24",
    # 北陸
    "54": "15", "55": "16", "56": "17", "57": "18",
    # 近畿
    "60": "25", "61": "26", "62": "27", "63": "28", "64": "29", "65": "30",
    # 中国
    "66": "33", "67": "34", "68": "32", "69": "31", "81": "35",
    # 四国
    "71": "36", "72": "37", "73": "38", "74": "39",
    # 九州・沖縄
    "82": "40", "83": "44", "84": "42", "85": "41", "86": "43", "87": "45", "88": "46",
    "9194": "47",
}

MONTHS_2023 = [
    ("202306", "20230601000000", "20230630230000"),
    ("202307", "20230701000000", "20230731230000"),
    ("202308", "20230801000000", "20230831230000"),
    ("202309", "20230901000000", "20230930230000"),
]


def fetch_chunk(wbgt_pref_cd: str, date_from: str, date_to: str):
    params = {
        "data_type": [0, 1],
        "location_type": 2,
        "pref_cds": [wbgt_pref_cd],
        "date_from": date_from,
        "date_to": date_to,
    }
    max_retries = 6
    backoff = 5
    for attempt in range(max_retries):
        resp = requests.get(URL, params=params, timeout=60)
        if resp.status_code == 429:
            print(f"  [429] rate limited, sleeping {backoff}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(backoff)
            backoff = min(backoff * 2, 120)
            continue
        resp.raise_for_status()
        return resp.json(), resp.content
    raise RuntimeError(f"Exceeded max retries for {wbgt_pref_cd} {date_from}-{date_to}")


def main():
    manifest_rows = []
    all_records = []
    total_calls = len(WBGT_PREF_TO_JIS) * len(MONTHS_2023)
    call_i = 0

    for wbgt_cd in WBGT_PREF_TO_JIS:
        for yyyymm, date_from, date_to in MONTHS_2023:
            call_i += 1
            raw_path = RAW_DIR / f"{wbgt_cd}_{yyyymm}.json"
            if raw_path.exists():
                raw_bytes = raw_path.read_bytes()
                data = json.loads(raw_bytes)
            else:
                data, raw_bytes = fetch_chunk(wbgt_cd, date_from, date_to)
                raw_path.write_bytes(raw_bytes)
                time.sleep(1.5)

            if data.get("status") != "success":
                print(f"[WARN] {wbgt_cd} {yyyymm}: status={data.get('status')} errMsg={data.get('errMsg')}")
                continue

            values = data.get("data", [])
            for v in values:
                all_records.append(
                    {
                        "wbgt_no": v["wbgt_no"],
                        "wbgt_date": v["wbgt_date"],
                        "wbgt_class": v["wbgt_class"],
                        "wbgt_pref_cd": str(v["pref_cd"]),
                        "wbgt_WI": v["wbgt_WI"],
                        "wbgt_WO": v["wbgt_WO"],
                    }
                )
            if call_i % 20 == 0 or call_i == total_calls:
                print(f"[{call_i}/{total_calls}] {wbgt_cd} {yyyymm}: {len(values)} records (cumulative {len(all_records)})")

            manifest_rows.append(
                {
                    "wbgt_pref_cd": wbgt_cd,
                    "month": yyyymm,
                    "sha256": hashlib.sha256(raw_bytes).hexdigest(),
                    "n_records": len(values),
                }
            )

    df = pd.DataFrame(all_records)
    df["jis_pref_code"] = df["wbgt_pref_cd"].map(WBGT_PREF_TO_JIS)
    unmapped = df[df["jis_pref_code"].isna()]["wbgt_pref_cd"].unique()
    assert len(unmapped) == 0, f"Unmapped WBGT pref codes: {unmapped}"

    df["wbgt_WO"] = pd.to_numeric(df["wbgt_WO"], errors="coerce")
    df["wbgt_date"] = pd.to_datetime(df["wbgt_date"])

    out_path = INTERIM_DIR / "wbgt_hourly_by_station.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest_summary = {
        "variable": "wbgt_hourly_by_station (raw hourly WBGT per AMeDAS site, Jun-Sep 2023)",
        "source_url": URL,
        "publisher": "環境省 熱中症予防情報サイト 実況値データ取得API (getSurveyData)",
        "table_id": "wbgt_survey_api_v1",
        "retrieved_at_utc": retrieved_at,
        "file_size_bytes": sum(r["n_records"] for r in manifest_rows),
        "sha256": "see individual chunk files under 02_Data/raw/major_revision/env_wbgt_2023/",
        "license_note": "環境省 熱中症予防情報サイト 利用規約に基づく公開データ",
        "output_file": str(out_path.relative_to(PROJECT_ROOT)),
    }
    manifest_path = PROJECT_ROOT / "reports" / "major_revision" / "source_manifest.csv"
    manifest_df = pd.DataFrame([manifest_summary])
    existing = pd.read_csv(manifest_path)
    manifest_df = pd.concat([existing, manifest_df], ignore_index=True)
    manifest_df.to_csv(manifest_path, index=False, encoding="utf-8-sig")

    n_stations = df["wbgt_no"].nunique()
    n_prefs = df["jis_pref_code"].nunique()
    print(f"[OK] {len(df)} hourly records, {n_stations} stations, {n_prefs} JIS prefectures -> {out_path}")


if __name__ == "__main__":
    main()

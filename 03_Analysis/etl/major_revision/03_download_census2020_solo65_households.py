"""
Major Revision ETL 03: 2020年国勢調査 都道府県別 65歳以上単独世帯人員（一般世帯人員ベース）

データソース: 総務省統計局「令和2年国勢調査 人口等基本集計」
  統計表ID: 0003445170（表番号22-4 住居の所有関係・建て方，世帯の家族類型別一般世帯人員）
  cat01=0（住居所有関係：総数）, cat02=R3（再掲：65歳以上の単独世帯）

national total cross-check (2026-08-01実施):
  cat01=0, cat02=R3, area=00000 → 6,716,806人
  既存 02_Data/interim/elderly_solo_household_rate.csv の合計（外部マイクロデータ由来）と完全一致。
  → 本APIは既存抽出値と同一の公式値であることを確認済み。都道府県別値をAPIから直接取得し、
    リポジトリ外パス（SharedWorkspace）への依存を無くして再現性を高める。

出力:
  - 02_Data/raw/major_revision/estat_census2020_age65/solo65_raw_response.json
  - 02_Data/interim/major_revision/census2020_solo65_by_prefecture.csv
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

STATS_DATA_ID = "0003445170"
URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "estat_census2020_age65"
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

NATIONAL_CROSSCHECK_VALUE = 6_716_806


def fetch():
    params = {
        "appId": APP_ID,
        "statsDataId": STATS_DATA_ID,
        "cdCat01": "0",
        "cdCat02": "R3",
        "metaGetFlg": "N",
    }
    resp = requests.get(URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json(), resp.content


def main():
    data, raw_bytes = fetch()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    raw_path = RAW_DIR / "solo65_raw_response.json"
    raw_path.write_bytes(raw_bytes)
    sha256 = hashlib.sha256(raw_bytes).hexdigest()

    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    if not isinstance(values, list):
        values = [values]

    rows = []
    national = None
    for v in values:
        area_code5 = v["@area"]
        is_national = area_code5 == "00000"
        is_prefecture = len(area_code5) == 5 and area_code5[2:] == "000" and area_code5 != "00000"
        if not (is_national or is_prefecture):
            continue  # 市区町村レベル（秘匿値"-"を含みうる）は都道府県合算に使わないので除外
        raw_value = v["$"]
        pop = int(raw_value)  # 都道府県・全国レベルは秘匿されない前提。秘匿値が来た場合は例外で停止する。
        if is_national:
            national = pop
        else:
            rows.append({"pref_code": area_code5[:2], "solo_65plus_persons_2020": pop})

    df = pd.DataFrame(rows).sort_values("pref_code").reset_index(drop=True)

    assert len(df) == 47, f"Expected 47 prefectures, got {len(df)}"
    assert national == NATIONAL_CROSSCHECK_VALUE, (
        f"National total {national} does not match prior cross-check "
        f"{NATIONAL_CROSSCHECK_VALUE}; do not silently proceed."
    )
    pref_sum = df["solo_65plus_persons_2020"].sum()
    assert pref_sum == national, f"Prefecture sum {pref_sum} != national total {national}"

    out_path = INTERIM_DIR / "census2020_solo65_by_prefecture.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    manifest_row = {
        "variable": "solo_65plus_persons_2020",
        "source_url": f"https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?statsDataId={STATS_DATA_ID}",
        "publisher": "総務省統計局 令和2年国勢調査 人口等基本集計（表22-4, 再掲R3）",
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

    print(f"[OK] {len(df)} prefectures written to {out_path}")
    print(f"[OK] national cross-check passed: {national:,}")


if __name__ == "__main__":
    main()

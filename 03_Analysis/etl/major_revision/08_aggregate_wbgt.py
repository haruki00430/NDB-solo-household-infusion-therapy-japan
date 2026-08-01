"""
Major Revision ETL 08: 公式WBGT実況値の都道府県集計

入力: 02_Data/interim/major_revision/wbgt_hourly_by_station.csv（観測所別・時刻別）

手順（SONNET_WORK_ORDER_01の仕様通り）:
  1. 観測所別に日最高WBGTを算出（時別値の日内最大値）
  2. 観測所別に閾値日数（>=28, >=31, >=33）と累積超過量 sum(max(daily_max-28,0)) を算出
  3. 都道府県内の観測所別集計値を平均する（地点数もあわせて記録）

出力:
  - 02_Data/interim/major_revision/wbgt_summary_2023.csv
    (pref_code, n_stations, wbgt_days_ge28, wbgt_days_ge31, wbgt_days_ge33, wbgt_cumulative_excess_28)
"""
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INTERIM_DIR = PROJECT_ROOT / "02_Data" / "interim" / "major_revision"


def main():
    df = pd.read_csv(INTERIM_DIR / "wbgt_hourly_by_station.csv", dtype={"jis_pref_code": str})
    df["wbgt_date"] = pd.to_datetime(df["wbgt_date"])
    df["date"] = df["wbgt_date"].dt.date

    before = len(df)
    df = df.dropna(subset=["wbgt_WO"])
    print(f"欠測値除外: {before} -> {len(df)} 行")

    # 観測所×日 の日最高WBGT
    daily_max = (
        df.groupby(["jis_pref_code", "wbgt_no", "date"])["wbgt_WO"]
        .max()
        .reset_index(name="daily_max_wbgt")
    )

    # 観測所別 閾値日数・累積超過量
    station_summary = (
        daily_max.groupby(["jis_pref_code", "wbgt_no"])
        .agg(
            wbgt_days_ge28=("daily_max_wbgt", lambda s: (s >= 28).sum()),
            wbgt_days_ge31=("daily_max_wbgt", lambda s: (s >= 31).sum()),
            wbgt_days_ge33=("daily_max_wbgt", lambda s: (s >= 33).sum()),
            wbgt_cumulative_excess_28=("daily_max_wbgt", lambda s: np.maximum(s - 28, 0).sum()),
            n_days_observed=("daily_max_wbgt", "count"),
        )
        .reset_index()
    )

    # 都道府県内で観測所別集計値を平均（地点数も記録）
    pref_summary = (
        station_summary.groupby("jis_pref_code")
        .agg(
            n_stations=("wbgt_no", "nunique"),
            wbgt_days_ge28=("wbgt_days_ge28", "mean"),
            wbgt_days_ge31=("wbgt_days_ge31", "mean"),
            wbgt_days_ge33=("wbgt_days_ge33", "mean"),
            wbgt_cumulative_excess_28=("wbgt_cumulative_excess_28", "mean"),
        )
        .reset_index()
        .rename(columns={"jis_pref_code": "pref_code"})
        .sort_values("pref_code")
        .reset_index(drop=True)
    )

    assert len(pref_summary) == 47, f"Expected 47 prefectures, got {len(pref_summary)}"
    assert pref_summary.isna().sum().sum() == 0

    out_path = INTERIM_DIR / "wbgt_summary_2023.csv"
    pref_summary.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[OK] {len(pref_summary)} prefectures written to {out_path}")
    print("n_stations range:", pref_summary["n_stations"].min(), "-", pref_summary["n_stations"].max())
    print("wbgt_days_ge28 range:", pref_summary["wbgt_days_ge28"].min(), "-", pref_summary["wbgt_days_ge28"].max())


if __name__ == "__main__":
    main()

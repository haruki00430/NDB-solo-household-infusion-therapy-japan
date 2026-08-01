# variable_dictionary.md — Major Revision 再解析データセット

対象ファイル: `02_Data/interim/major_revision/prefecture_analysis.csv`（47行=47都道府県、結合キー: `pref_code` JIS 2桁）

| 変数名 | 定義 | 出典・年次 | 単位 |
|---|---|---|---|
| `pref_code` | JIS都道府県コード（01-47） | — | — |
| `total_population_2023` | 総人口 | 総務省統計局 人口推計 2023年10月1日現在（e-Stat 0004012968） | 人 |
| `population_65plus_2023` | 65歳以上人口 | 同上 | 人 |
| `ageing_rate_pct` | 高齢化率 = population_65plus_2023 / total_population_2023 × 100 | 同上より算出 | % |
| `g004_count` | G004（点滴注射500mL以上）算定回数 | NDB第10回オープンデータ, FY2023（既存パイプライン抽出値を再利用） | 回 |
| `large_volume_infusion_procedure_rate` | outcome = g004_count / total_population_2023 × 100,000 | 上記より算出（旧解析は2020年人口を分母としていたが、本解析は2023年人口に統一） | 人口10万対 |
| `older_living_alone_pct` | **新曝露**: solo_65plus_persons_2020 / population_65plus_2020 × 100 | 総務省統計局 令和2年国勢調査（e-Stat 0003445170, 0003410381） | % |
| `original_elderly_solo_household_pct` | **旧曝露**（Model 0=旧解析再現専用）: 65歳以上単独世帯数 / 総世帯数(2020) × 100 | 既存パイプライン抽出値（マイクロデータ由来、公式集計値と国全体で完全一致することを確認済み） | % |
| `solo_65plus_persons_2020` | 65歳以上単独世帯人員（新曝露の分子） | 令和2年国勢調査 人口等基本集計 表22-4（再掲R3） | 人 |
| `population_65plus_2020` | 65歳以上人口（新曝露の分母、2020年） | 令和2年国勢調査 時系列データ | 人 |
| `general_hospital_beds_per_100k` | 一般病床数（人口10万対、公式値） | 厚生労働省 令和5年医療施設調査 都道府県編 第15表 | 人口10万対 |
| `general_clinics_per_100k` | 一般診療所数（人口10万対、自前算出） | 同 第25表 ÷ total_population_2023 | 人口10万対 |
| `population_density_per_km2` | 人口密度（総面積1km²あたり、2023年度） | 総務省統計局 社会生活統計指標（#A01201） | 人/km² |
| `log_population_density` | 上記の自然対数 | 算出 | — |
| `n_stations` | 都道府県内で集計に用いたWBGT観測地点数 | 環境省 熱中症予防情報サイト API | 地点 |
| `wbgt_days_ge28` / `_ge31` / `_ge33` | 日最高WBGTが28/31/33以上の日数（都道府県内地点平均） | 環境省 公式WBGT実況値（2023年6-9月, getSurveyData API） | 日 |
| `wbgt_cumulative_excess_28` | Σ max(日最高WBGT−28, 0)（地点平均） | 同上 | ℃・日 |

## 命名・単位の注意点

- `original_elderly_solo_household_pct` と `older_living_alone_pct` は**分母が異なる**（前者は全世帯数、後者は65歳以上人口）。両者を同一視しない。
- outcome分母を2020年人口から2023年人口へ変更したため、旧解析（Model 0以外）とのraw coefficientの単純比較はできない。標準化係数で比較する。
- WBGT≥33日数を「アラート日数」と呼ばない（熱中症警戒アラートの基準は予測値であり、本変数は実況値であるため）。

## 出典管理

全出典URL・取得日時・SHA-256は `reports/major_revision/source_manifest.csv` に記録。

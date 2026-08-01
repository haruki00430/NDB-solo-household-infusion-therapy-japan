# reproduction_log.md — Major Revision 再解析 実行ログ

実行日: 2026-08-01
実行環境: Python 3.14.2 / Windows

## パッケージバージョン（実行時点）

```
pandas 2.3.3
numpy 2.3.5
scipy 1.16.3
statsmodels 0.14.6
scikit-learn 1.8.0
requests 2.33.1
pyyaml 6.0.3
patsy 1.0.2
python-dotenv (.env 経由で ESTAT_APP_ID を読み込み)
```

乱数を用いる解析はこのフェーズには含まれない（Bootstrap等は未実施のためシード固定は不要）。

## 実行順序（単一コマンドでの再構築）

```bash
cd projects/NDB_XXX_heatwave_heatstroke

# --- データ取得（Phase 1） ---
python 03_Analysis/etl/major_revision/01_download_pop2023_by_age.py
python 03_Analysis/etl/major_revision/02_download_census2020_age65.py
python 03_Analysis/etl/major_revision/03_download_census2020_solo65_households.py
python 03_Analysis/etl/major_revision/04_build_living_alone_exposure.py
python 03_Analysis/etl/major_revision/05_download_healthcare_supply.py
python 03_Analysis/etl/major_revision/06_download_population_density.py
python 03_Analysis/etl/major_revision/07_download_wbgt_official.py   # resume対応、5回実行ごとに429で自動リトライ
python 03_Analysis/etl/major_revision/08_aggregate_wbgt.py
python 03_Analysis/etl/major_revision/09_build_analytic_dataset.py

# --- 統計解析（Phase 3） ---
cd 03_Analysis/analysis/major_revision
python 01_fit_models.py
python 02_diagnostics.py
python 03_sensitivity.py
python 04_nonlinearity_multiplicity.py
python 05_comparison_outcome.py
```

## 既知の注意点

- `07_download_wbgt_official.py` は初回実行時に環境省APIから429（レート制限）を受けた。
  スクリプトは (WBGTコード×月) 単位でダウンロード済みJSONをキャッシュし、再実行時は
  既存ファイルをスキップして再開する（`02_Data/raw/major_revision/env_wbgt_2023/*.json`）。
  429時は指数バックオフ（5秒→最大120秒）で自動リトライする。
- 総ダウンロード: 240リクエスト（60 WBGTコード × 4か月）、2,462,448時間別レコード、
  841観測所、47 JIS都道府県に正常集約。
- e-Stat appIdは `.env`（Git管理外）に格納。既存パイプラインのスクリプト内には
  平文のappIdが残っているため、著者にe-Stat側でのキー再発行を推奨する（`issues_for_author.md` 参照）。

## Work Order 03 追加実行分（2026-08-01）

開始時コミットハッシュ: `88f91d84585981db2710eaca9aa0ebe2763b03d8`（`git rev-parse HEAD`）

```bash
cd projects/NDB_XXX_heatwave_heatstroke

# --- G004 公開データ有無の確定監査 ---
cd 03_Analysis/analysis/major_revision
python 06_g004_availability_audit.py

# --- レガシー2020年人口分母outcomeの構築 ---
cd ../../etl/major_revision
python 10_build_legacy_outcome.py

# --- 旧曝露 O-A〜O-D 階層モデル・感度分析・非線形性・比較・図表 ---
cd ../../analysis/major_revision
python 07_original_exposure_models.py
python 08_original_exposure_sensitivity.py
python 09_original_exposure_nonlinearity.py
python 10_exposure_comparison.py
python 11_original_exposure_coefficient_figure.py
```

新規パッケージ依存: `openpyxl`（G004監査でのxlsx読み込み、requirements.txtに既存）。
乱数は使用していない（LOO・感度分析は決定的な再計算のみ）。

## 再現性チェック

- `02_Data/raw/` の既存ファイルは一切変更していない（新規サブフォルダ `major_revision/` への追記のみ）。
- 47都道府県の一意性・国全体合計値の公式統計との一致を各取得スクリプト内でassertし、
  すべてPASSしたことを確認済み（例: 2020年国勢調査総人口 126,146,099人、65歳以上単独世帯人員
  6,716,806人はいずれも公表値と完全一致）。

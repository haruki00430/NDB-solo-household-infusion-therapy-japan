# predrafting_corrections_audit.md — Work Order 04 §「Required pre-drafting corrections」実施記録

実施日: 2026-08-01

## 1. O-C標準化係数の欠落確認・補完

SONNET_REPORT_02の手書き要約表で「—」と表示されていた箇所は、**基盤となる機械可読ファイル
（`original_exposure_model_results.csv`, `tables/table_original_exposure_hierarchy.csv`）には
既に正しく計算済みであった**ことを確認した（レポート作成時の転記漏れであり、解析パイプライン自体の欠落ではない）。

```
O-C standardized coefficient (HC3): 0.074738
HC3 95% CI: [-0.240225, 0.389701]
p-value: 0.641872
```

出典: `03_Analysis/results/major_revision/original_exposure_model_results.csv`
（model=O-C, variable=original_elderly_solo_household_pct, se_type=HC3, coef_type=standardized,
denominator=primary_2023_population）

以降、すべての最終成果物（Table 2、本文、回答書）でこの値を使用する。

## 2. O-A〜O-D 累積デザイン行列の検証

`03_Analysis/analysis/major_revision/07_original_exposure_models.py` の `O_MODELS` 辞書、および
`original_exposure_model_fit.csv` の `formula` 列から直接確認:

| Model | 完全なモデル式 | N | 残差自由度 |
|---|---|---|---|
| O-A | `large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct` | 47 | 45 |
| O-B | `large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct` | 47 | 44 |
| O-C | `large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct + general_hospital_beds_per_100k` | 47 | 43 |
| O-D | `large_volume_infusion_procedure_rate ~ original_elderly_solo_household_pct + ageing_rate_pct + general_hospital_beds_per_100k + wbgt_days_ge28` | 47 | 42 |

各モデルは前モデルの共変量を全て含む累積調整であることを確認済み（O-Bの共変量⊂O-Cの共変量⊂O-Dの共変量）。

## 3. 再現表現の訂正

- ✅ 使用可能: "The original point estimate was exactly reproduced using the submitted 2020
  population denominator. Inferential statistics differed because the revised analysis used
  HC3 heteroskedasticity-robust standard errors."
- ❌ 使用禁止: "The original analysis was exactly reproduced."

根拠: レガシー2020年人口分母でのO-A点推定値 β=723.365229 は原稿の報告値 723.37 と完全一致するが、
原稿はHC3ロバストSEを使用しておらず（通常OLS SEのみ）、p値等の推測統計量は本再解析
（HC3）と厳密には一致しない。

以降、本文・回答書ではこの訂正済み表現のみを使用する。

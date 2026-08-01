# original_exposure_additional_analysis.md — 旧曝露の階層調整モデルとG004監査（Work Order 03）

対象: `SONNET_WORK_ORDER_03_old_exposure_adjustment_and_G004_audit.md`
実施日: 2026-08-01

---

## 1. G004 都道府県×年齢データの確定監査

**判定: `NOT_PUBLICLY_AVAILABLE`**（確定）

詳細は `g004_public_data_availability_audit.md` / `g004_public_file_inventory.csv` /
`g004_search_log.txt` を参照。要点:

- 第10回NDBオープンデータ公式ページの生HTML（全695リンク）を取得・解析し、G注射見出し
  直下に存在するファイルが「性年齢別」「都道府県別」「診療月別」「二次医療圏別」の
  **4ファイルのみ**であることを直接確認した（次の見出し「H リハビリテーション」までの間に他のファイルなし）。
- ページ全体で「都道府県性年齢別」クロス表が存在するのは、初診・再診・外来診療料・検査
  （+3内訳）・手術・オンライン診療の**限定された9項目のみ**であり、G注射は含まれない。
- ダウンロードした4ファイルを実際に開き、G004（点滴注射）の行を特定。各ファイルは
  「年齢×性別のみ」「都道府県のみ」「診療月のみ」「二次医療圏のみ」と、必ず1次元のみが
  変化する構造であることを確認した。同時に2次元をクロス集計したファイルは存在しない。
- 上記手順を`06_g004_availability_audit.py`として再現可能なスクリプト化し、独立実行でも
  同じ結論に到達することを確認済み（プログラムによる再検証パス）。

したがって、Part 1の「Conditional age-specific branch」（年齢別outcomeの構築）は実施しない。
Primary outcomeは引き続き全人口（2023年推計人口）を分母とする粗率のままとする。

---

## 2. O-A〜O-D 階層調整モデル（旧曝露を保持）

### 2.1 主要outcome（2023年人口分母）

| Model | 追加調整 | N | 曝露係数(HC3) | 95%CI | p値 | Adj R² | 曝露partial R² | AICc |
|---|---|---|---|---|---|---|---|---|
| O-A | なし | 47 | 656.22 | [326.9, 985.6] | **<0.001** | 0.256 | 0.272 | 853.2 |
| O-B | +高齢化率 | 47 | 306.14 | [-71.3, 683.5] | 0.112 | 0.365 | 0.056 | 847.1 |
| O-C | +一般病床数 | 47 | 94.09 | [-302.4, 490.6] | 0.642 | 0.386 | 0.004 | 846.9 |
| O-D | +WBGT≥28日数 | 47 | -9.41 | [-493.9, 475.1] | 0.970 | 0.422 | 0.00004 | 845.6 |

### 2.2 Reviewer 2 への直接回答（O-A→O-B の減衰）

- 絶対変化: 656.22 → 306.14（**-350.08**）
- 係数比: 0.467（O-Bの係数はO-Aの46.7%）
- 記述的減衰率: **53.3%**（標準化係数でも同一の53.3%）
- 曝露のpartial R²: 0.272 → 0.056（減少幅 -0.216）
- Adjusted R²: 0.256 → 0.365（AICcは853.2→847.1に改善、モデル全体の当てはまりは向上）

**重要な注記**: この53.3%という数値は記述的な減衰率であり、「高齢化率が原因の53%を説明した」
という媒介分析（mediation）ではない。95%CIが O-B の時点で既にゼロをまたぐことから、
統計的有意性は失われている。

### 2.3 レガシーoutcome（投稿時と全く同じ2020年人口分母）

分母年の更新効果と交絡調整効果を分離するため、投稿時の2020年人口分母（
`02_Data/interim/prefecture_population_2020.csv` の「総人口」列、実体は一般世帯人員ベース）
をそのまま用いて同じ階層を再実行した。

| Model | 曝露係数(HC3) | 95%CI | p値 |
|---|---|---|---|
| O-A | 723.37 | [377.5, 1069.2] | **<0.001** |
| O-B | 310.18 | [-87.0, 707.4] | 0.126 |
| O-C | 76.49 | [-340.2, 493.2] | 0.719 |
| O-D | -31.78 | [-536.8, 473.3] | 0.902 |

O-Aの723.37は投稿原稿の単変量結果（β=723.37, p=0.000124）と**完全に一致**し、レガシー再現が
正確であることを確認した。減衰率は57.1%であり、分母年の違いによる結果への影響は小さい
（53.3% vs 57.1%）。つまり、観察された減衰は主に交絡調整によるものであり、outcome分母の
更新（2020→2023）による影響ではない。

---

## 3. 感度分析・診断（旧曝露、O-D基準）

全て非有意（p=0.64〜0.97）で、O-D基準の結論と一致:

| 分析 | 曝露係数 | p値 |
|---|---|---|
| O-D（基準） | -9.41 | 0.970 |
| 病床→診療所（O-C） | 55.65 | 0.762 |
| 病床→診療所（O-D） | -35.57 | 0.831 |
| 対数人口密度追加 | -63.20 | 0.846 |
| 東京・大阪・神奈川除外 | -42.02 | 0.891 |
| outcome対数変換 | -0.011 | 0.714 |
| 人口重み付きWLS | 91.78 | 0.749 |
| WBGT≥31日数 | 96.23 | 0.638 |
| WBGT≥33日数 | -25.47 | 0.903 |
| 累積超過量(28基準) | 90.58 | 0.666 |

**Leave-one-prefecture-out（47回）**: 曝露係数 -107.9〜+92.8、**47回全てで95%CIがゼロをまたぐ**。

**回帰診断（O-D）**: Cook's D閾値(4/47=0.085)を超えるのは北海道(0.667)・高知(0.190)・
広島(0.144)——新曝露の場合と同じ都道府県が影響点として検出されたが、LOOで除外しても
結論は変わらない。

---

## 4. 非線形性・都市影響（旧曝露）

- 線形 vs 二次項（中心化）: partial F p=0.142、AICc 845.6→845.9（悪化） → 非線形性の証拠なし
- 線形 vs 自然三次スプライン(df=3): p=0.141、AICc 845.6→845.9（悪化） → 同様
- 中央値二分解析（監査専用）: 高群 β=-192.9 (p=0.647)、低群 β=+20.7 (p=0.966) —
  投稿原稿の層別パターンを単純に再現するものではなく、いずれも非有意

予測曲線・95%CI帯は `results/figures/figure_original_exposure_nonlinearity.png` を参照。

---

## 5. 旧曝露(O) vs 新曝露(N) 並置比較

| Stage | Estimand | Model | 非標準化係数 | 95%CI | p値 | 標準化β | 曝露partial R² |
|---|---|---|---|---|---|---|---|
| 無調整 | O（旧曝露＝投稿時） | O-A | 656.22 | [326.9, 985.6] | <0.001 | 0.521 | 0.272 |
| 無調整 | N（新曝露＝補完） | Model 1 | 0.25 | [-249.8, 250.3] | 0.998 | 0.0003 | ~0 |
| フル調整 | O | O-D | -9.41 | [-493.9, 475.1] | 0.970 | -0.007 | 0.00004 |
| フル調整 | N | Model 4 | -25.73 | [-227.9, 176.4] | 0.803 | -0.034 | 0.001 |

無調整の段階ではOとNは全く異なる挙動（Oは強く有意、Nは完全に無相関）を示すが、
**フル調整後は両者とも実質的にゼロへ収束する**。OとNは異なる問い（都道府県全体の
独居高齢者人口負担 vs 高齢者集団内の独居割合）に答えるものであり、「どちらかが誤り」
ではなく、「どちらも、年齢構成・医療供給・暑熱を調整すると本アウトカムとの独立した
関連を示さない」という結果に収束した。

---

## 6. 解釈の分岐判定（Work Order Part 6）

**選択した分岐: Branch 2（年齢構成による交絡と整合する実質的減衰）**

理由:
- O-A→O-Bで係数が53.3%減衰し、95%CIが既にゼロをまたぐ（統計的有意性の喪失）。
- O-C、O-Dでさらに減衰し、係数はほぼ正確にゼロ（partial R²=0.00004）、符号も反転。
- 全ての感度分析（病床→診療所、対数密度、都市除外、対数変換、WLS、複数のWBGT指標）で
  結論は一貫して非有意。
- LOO 47回全てで95%CIがゼロをまたぐ——特定の都道府県（北海道など、Cook距離は高い）に
  依存した結果ではない。
- 非線形性の証拠なし（二次項・スプラインとも改善なし）。

Branch 1（人口負担としての関連が残る）は該当しない（O-Bの時点で既に非有意）。
Branch 3（不確定）も該当しない——結果は不安定ではなく、一貫して単調に減衰しゼロへ収束する
明確なパターンを示しており、感度分析間で結論が入れ替わることもない。

**採用する解釈文（Work Order指定の文言）**:

> The submitted ecological association was sensitive to population age structure and exposure
> denominator choice.

（「高齢化率が関連を完全に説明した」という因果的表現は用いない。）

---

## 7. 査読対応ドラフト（事実のみ、反論なし）

> We agree that population age structure was a central potential source of confounding. In
> direct response, we retained the originally submitted exposure — the percentage of all
> households consisting of one person aged 65 years or older — and added the prefectural
> percentage of residents aged 65 years or older to the same model. The original-exposure
> coefficient changed from 656.22 (95% CI 326.9–985.6, p<0.001) to 306.14 (95% CI -71.3–683.5,
> p=0.112), corresponding to a descriptive attenuation of 53.3%. Further adjustment for
> healthcare supply and WBGT yielded coefficients of 94.09 (p=0.642) and -9.41 (p=0.970)
> respectively, indicating that the association was not robust to full adjustment. We also
> reconstructed a complementary exposure using the population aged 65 years or older as the
> denominator; this alternative estimand showed no association with the outcome at any stage
> of adjustment (p=0.998 unadjusted, p=0.803 fully adjusted). These analyses materially changed
> the interpretation of the study, and we revised the manuscript accordingly.

---

## 8. 未解決の著者判断事項

`issues_for_author.md` に統合済み（本ファイル作成と同時に追記）。要点のみ:

- 論文の中心命題をBranch 2の解釈（交絡に敏感な生態学的関連）で確定するかどうかの最終判断。
- WBGT≥33日数の副次的知見（補正前p=0.018、FDR後p=0.055）の本文での扱い。
- 北海道の地理的異質性・高いCook距離をlimitationとしてどこまで詳述するか。

---

## 9. 出力パス

```
03_Analysis/analysis/major_revision/06_g004_availability_audit.py
03_Analysis/analysis/major_revision/07_original_exposure_models.py
03_Analysis/analysis/major_revision/08_original_exposure_sensitivity.py
03_Analysis/analysis/major_revision/09_original_exposure_nonlinearity.py
03_Analysis/analysis/major_revision/10_exposure_comparison.py
03_Analysis/analysis/major_revision/11_original_exposure_coefficient_figure.py
03_Analysis/etl/major_revision/10_build_legacy_outcome.py

03_Analysis/results/major_revision/original_exposure_model_results.csv
03_Analysis/results/major_revision/original_exposure_model_fit.csv
03_Analysis/results/major_revision/original_exposure_vif.csv
03_Analysis/results/major_revision/original_exposure_attenuation.csv
03_Analysis/results/major_revision/original_exposure_sensitivity.csv
03_Analysis/results/major_revision/original_exposure_leave_one_out.csv
03_Analysis/results/major_revision/original_exposure_influence.csv
03_Analysis/results/major_revision/original_exposure_nonlinearity.csv
03_Analysis/results/major_revision/original_exposure_median_split_audit_only.csv
03_Analysis/results/major_revision/original_vs_new_exposure_comparison.csv
03_Analysis/results/major_revision/tables/table_original_exposure_hierarchy.csv
03_Analysis/results/major_revision/figures/figure_original_exposure_coefficients.png(+source csv)
03_Analysis/results/major_revision/figures/figure_original_exposure_nonlinearity.png(+source csv)

02_Data/interim/major_revision/legacy_outcome_2020denominator.csv
02_Data/raw/major_revision/ndb10_g004_audit/（生HTML・4xlsx・2PDF、SHA-256付き）

reports/major_revision/g004_public_data_availability_audit.md
reports/major_revision/g004_public_file_inventory.csv
reports/major_revision/g004_search_log.txt
reports/major_revision/g004_search_log_rebuild.txt（独立再検証ログ）
reports/major_revision/original_exposure_additional_analysis.md（本ファイル）
```

# SONNET REPORT 01: データ取得・再解析 結果報告

宛先: Codex（`SONNET_WORK_ORDER_01_data_and_reanalysis.md` の起草者）
作成: Sonnet（Claude Code）
作成日: 2026-08-01
対象: IJB Submission ID `0cd18650-d5db-481f-b00b-bbde3cda74f7`（Major Revision）

---

## 0. 作業環境に関する重要な差異

`SONNET_WORK_ORDER_01`/`02` が想定していた入力パス・作業ルートは、実際にSonnetが
アクセスできた環境と一致していなかった。

| Work Orderの想定 | 実際 |
|---|---|
| 原稿: `C:\Users\user\Desktop\Japan manuscript_main_IJB_anon.docx` | 実体は `NDB_Research_Hub/projects/NDB_XXX_heatwave_heatstroke/04_Manuscripts/submission_package_IJB/` 配下 |
| 作業ルート: `C:\Users\user\Documents\Codex\2026-08-01\are-heat-health-systems-socially-blind` | 既存の正規Gitプロジェクト `NDB_Research_Hub/projects/NDB_XXX_heatwave_heatstroke/`（`02_Data/raw`, `03_Analysis` 等を含む既存パイプラインあり）に接続して作業した |

そのため、本作業は指示書が前提としていた新規ワーキングルートではなく、**既存の正規プロジェクトリポジトリ内**に
`major_revision/` サブフォルダ群として実装した（ディレクトリ構成は §5 参照）。既存パイプライン
（`03_Analysis/analysis/01-09` 等、原稿投稿時の解析）はそのまま保持し、比較対象（Model 0=旧解析再現）
として利用した。

---

## 1. G004の都道府県×年齢クロス表について

`major_revision_strategy_ja.md` が既に「公開一覧に見当たらない」と結論していた内容を前提として、
本作業では**改めての全量確認は行っていない**（時間的制約のため既存結論を採用）。したがって:

- outcomeは年齢調整・年齢層別ではなく、**全人口（2023年10月1日推計人口）を分母とする粗率**として再計算した。
- 年齢構成の交絡には、outcome側の年齢調整ではなく、**曝露側の再定義**（65歳以上人口を分母とする独居割合）
  と、**モデル側の調整変数**（`ageing_rate_pct`）の両方で対応した。
- G004クロス表の存在有無の最終確認は `issues_for_author.md` §2 に未解決事項として残した。

---

## 2. 曝露推定値（Model 0-4）

**結論: 新曝露（65歳以上人口に占める独居割合）は、無調整の段階から一貫してoutcomeと関連しない。**
これはCodexの事前確率分布（「年齢・供給調整後にほぼ完全に消失する: 20-35%」）の中で最も厳しい
シナリオに該当し、しかも「調整後に消失」ではなく「**無調整の時点で既に消失**」という、さらに一段階
厳しい結果だった。

| Model | 曝露 | 追加調整 | N | 曝露係数(HC3) | 95%CI | p値 | Adj R² | 曝露partial R² | AICc |
|---|---|---|---|---|---|---|---|---|---|
| 0（旧解析再現） | 旧曝露（全世帯比） | なし | 47 | 656.22 | [326.9, 985.6] | **<0.001** | 0.256 | 0.272 | 853.2 |
| 1 | 新曝露（65+人口比） | なし | 47 | 0.25 | [-249.8, 250.3] | **0.998** | -0.022 | ~0 | 868.1 |
| 2 | 新曝露 | +高齢化率 | 47 | 117.57 | [-66.5, 301.7] | 0.211 | 0.350 | 0.035 | 848.2 |
| 3 | 新曝露 | +一般病床数 | 47 | 1.63 | [-177.6, 180.9] | 0.986 | 0.384 | ~0 | 847.1 |
| 4（主要推論） | 新曝露 | +WBGT≥28日数 | 47 | -25.73 | [-227.9, 176.4] | 0.803 | 0.423 | 0.001 | 845.6 |

補足知見（Reviewer 2 の懸念を裏付けるデータ）:
- 旧曝露 と 高齢化率 の相関 r = **0.625**
- 新曝露 と 高齢化率 の相関 r = **-0.242**
- 新曝露 と outcome の単純相関 r = **0.0003**（旧曝露は r=0.521）

旧解析の単変量結果（β=723.4, p=0.000124; outcome分母=2020年人口）と、本解析Model 0
（同じ旧曝露、outcome分母のみ2023年人口に更新: β=656.2, p<0.001）は方向・有意性が一致し、
本パイプラインの再現性を確認できた（差異はoutcome分母年の意図的な変更によるもの）。

---

## 3. 感度分析・非線形性の主な結果

**全ての感度分析で結論（曝露非有意）は不変。**

- 病床→診療所置換、対数人口密度追加、東京・大阪・神奈川除外、outcome対数変換、人口重み付きWLS:
  いずれも p=0.49〜0.92 で非有意（`results/major_revision/sensitivity_analyses.csv`）。
- **Leave-one-prefecture-out（47回）**: 曝露係数は -57.6〜+20.4 の範囲で符号も不安定。
  **47回全てで95%CIがゼロをまたぐ**（特定県による駆動ではない、頑健なnull）。
- 非線形性: 線形 vs 二次項（partial F p=0.523, AICc悪化）、線形 vs 自然三次スプライン(df=3)
  （p=0.420, AICc悪化）——いずれも非線形性を支持しない。中央値二分解析（補足専用）も高群・低群
  ともに非有意（`median_split_audit_only.csv`）。
- 多重性: WBGT≥31/33/累積超過量への置換でも曝露係数は非有意。ただしWBGT≥33日数**自体**は
  補正前p=0.018（FDR後p=0.055で非有意）——「暑熱自体は関連しうるが独居状態とは無関係」という
  副次的知見。
- Comparison-outcome（旧negative control、「6倍」表現は削除）: 主要outcome標準化β=0.0003、
  comparison outcome（外来利用）標準化β=0.169（いずれも非有意）。旧解析が主張していた
  「特異性」は新曝露のもとでは支持されない。
- 回帰診断: 北海道（Cook's D=0.648、閾値4/N=0.085の約7.6倍）が最大の影響点だが、
  LOOで除外しても結論は変わらない。

---

## 4. 未解決のデータ・解釈上の課題（`issues_for_author.md` 全文）

以下は `reports/major_revision/issues_for_author.md` の全文をそのまま転載したものである
（著者向けに書かれた原文であり、Codexへの報告のため参考として全文を含める）。

> ### 1. 【最重要・戦略判断】新曝露は主要outcomeと事実上無相関
>
> `older_living_alone_pct`（65歳以上人口に占める独居割合）は、outcomeとの単純相関 r=0.0003、
> Model 1（無調整）でも p=0.998 であり、Model 2-4（高齢化率・医療供給・WBGT調整後）も
> 一貫して非有意・係数の符号も不安定（LOOで正負が入れ替わる）。
>
> 旧曝露（`original_elderly_solo_household_pct`）が高齢化率と r=0.63 の強い相関を持っていたのに対し、
> 新曝露は高齢化率と r=-0.24 とむしろ弱い負の相関であり、両者は明確に異なる構成概念であることが
> データ上も確認できる。
>
> → **これは「調整後に関連が減衰する」ではなく「独立した効果が最初から検出されない」という、
> Codexの想定シナリオの中で最も厳しいシナリオに該当する。** 論文の再定位方針（詳細は
> `reanalysis_report.md`）について、投稿を続けるか・どう再定位するかの著者判断が必要。
>
> ### 2. G004の都道府県×年齢クロス表は引き続き未確認
>
> 第10回NDBオープンデータの公開ファイル一覧を再確認する時間の制約上、今回は
> 「既存パイプラインの結論（都道府県×年齢クロス表なし）」を前提として、
> outcomeは全人口ベースの再計算（2023年人口推計）にとどめた。年齢調整outcome
> （65歳以上人口を分母とする、または年齢標準化率）が必要な場合は、
> NDB公式ファイル一覧の再確認が必要。
>
> ### 3. 医療供給2変数の性質が非対称
>
> `general_hospital_beds_per_100k` は厚労省が算出済みの人口10万対公式値をそのまま使用したが、
> `general_clinics_per_100k` は施設数の実数を本解析側で2023年人口推計により自前計算した
> （厚労省側に対応する「人口10万対診療所数」表は見当たらなかった）。分母年が同じ2023年である
> ため実務上の問題はないと考えられるが、完全な出典の一貫性という意味では非対称である。
>
> ### 4. 北海道の地点集計における異質性
>
> WBGT集計は北海道について、環境省API上の14地域（宗谷～檜山）・163観測地点を単純平均して
> 1都道府県値としている。北海道は他都道府県と比べ面積・気候の内部変動が極めて大きく、
> Cook距離でも最大の影響度（0.65、閾値4/N=0.085の約7.6倍）を示した。ただし
> leave-one-prefecture-out感度分析で北海道を除外しても結論（曝露係数は非有意）は変わらない
> ことを確認済み。本文での考察・limitationに明記することを推奨する。
>
> ### 5. e-Stat appIdが公開GitHubリポジトリに平文で残っている
>
> 既存の `03_Analysis/etl/download_prefecture_population_2020.py` 等、複数の既存スクリプトに
> e-Stat appIdがハードコードされたままGitHub公開リポジトリにコミットされている。
> 本再解析の新規スクリプトは `.env`（Git管理外）経由に変更したが、既存スクリプトの修正は
> 本作業のスコープ外とした。**e-Stat側でのAPIキー再発行（漏洩済みキーの無効化）を推奨する。**
>
> ### 6. Zenodo新バージョンの準備は未着手
>
> `SONNET_WORK_ORDER_02` の前提条件（本再解析の数値・出典の独立監査、原稿・回答書の確定、
> 著者の明示承認）が満たされていないため、Zenodo操作は一切行っていない。

---

## 5. 成果物パス一覧

すべて `NDB_Research_Hub/projects/NDB_XXX_heatwave_heatstroke/` を起点とする相対パス。

```
config/config.yaml                                          モデル仕様・年次・閾値・都道府県コード表

02_Data/raw/major_revision/estat_pop2023/                   2023年人口推計 生レスポンス
02_Data/raw/major_revision/estat_census2020_age65/          2020年国勢調査 生レスポンス
02_Data/raw/major_revision/mhlw_iryo_shisetsu_2023/         医療施設調査 生レスポンス
02_Data/raw/major_revision/env_wbgt_2023/                    WBGT実況値 生レスポンス（240チャンク）

02_Data/interim/major_revision/prefecture_analysis.csv       47都道府県 解析用マスタデータセット
02_Data/interim/major_revision/variable_dictionary.md        変数定義書
（その他、中間生成物: pop2023_by_prefecture.csv, census2020_age65_by_prefecture.csv,
  census2020_solo65_by_prefecture.csv, living_alone_exposure.csv, healthcare_supply_2023.csv,
  population_density_2023.csv, wbgt_hourly_by_station.csv, wbgt_summary_2023.csv）

03_Analysis/etl/major_revision/01-09_*.py                    データ取得・構築スクリプト（番号順再実行可能）
03_Analysis/analysis/major_revision/_common.py                共通統計ユーティリティ
03_Analysis/analysis/major_revision/01_fit_models.py          Model 0-4
03_Analysis/analysis/major_revision/02_diagnostics.py         回帰診断
03_Analysis/analysis/major_revision/03_sensitivity.py         感度分析・LOO
03_Analysis/analysis/major_revision/04_nonlinearity_multiplicity.py  非線形性・多重性
03_Analysis/analysis/major_revision/05_comparison_outcome.py  comparison-outcome analysis

03_Analysis/results/major_revision/model_results.csv          係数レベル結果（非標準化・標準化・HC3/classical）
03_Analysis/results/major_revision/model_fit.csv               N, R², adjR², AIC, AICc, BIC
03_Analysis/results/major_revision/vif.csv
03_Analysis/results/major_revision/influence.csv               残差・レバレッジ・Cook距離・DFBETAs
03_Analysis/results/major_revision/sensitivity_analyses.csv
03_Analysis/results/major_revision/leave_one_out.csv
03_Analysis/results/major_revision/nonlinearity.csv
03_Analysis/results/major_revision/multiplicity.csv（BH-FDR）
03_Analysis/results/major_revision/median_split_audit_only.csv （主結果ではない旨明記）
03_Analysis/results/major_revision/comparison_outcome.csv
03_Analysis/results/major_revision/tables/ , figures/           未着手（論文再定位方針の決定待ち）

reports/major_revision/source_manifest.csv                    出典URL・取得日時・SHA-256（7エントリ）
reports/major_revision/reproduction_log.md                     実行順序・パッケージバージョン
reports/major_revision/reanalysis_report.md                    詳細な結果・解釈の全文（本報告書の元データ）
reports/major_revision/issues_for_author.md                    著者確認事項6件
```

---

## 6. 受入基準（SONNET_WORK_ORDER_01 記載分）に対する充足状況

- [x] 47都道府県が一意の公式コードで存在（全取得スクリプトでassert済み）
- [x] 原稿中の既報数値を機械可読ファイルで追跡可能（Model 0 vs 原稿単変量結果、差異を記録）
- [x] 元データ（`02_Data/raw/`）は無変更（新規サブフォルダへの追記のみ、git status で確認済み）
- [x] 関連が消失する結果を抑制せずそのまま報告
- [ ] クリーンな一時ディレクトリでの単一コマンド再構築テストは未実施（スクリプトは番号順再実行可能な設計だが、隔離環境での動作確認はしていない）
- [ ] Zenodo/GitHubへの変更なし（該当作業自体を実施していないため充足）

---

## 附録A: `reanalysis_report.md` 全文

以下は `reports/major_revision/reanalysis_report.md` の全文をそのまま転載したものである
（§2・§3は本報告書の要約の元になった詳細版。数表・解釈の全根拠を含む）。

> # reanalysis_report.md — IJB Major Revision 再解析報告
>
> 対象論文: "Are Heat-Health Systems Socially Blind? Social Isolation and Dehydration-Related
> Healthcare Utilization Across Japan"（Submission ID `0cd18650-d5db-481f-b00b-bbde3cda74f7`）
>
> 実施日: 2026-08-01　実施範囲: SONNET_WORK_ORDER_01 相当（データ取得〜統計解析〜成果物出力）
>
> ---
>
> ## 1. 要旨（結論を先に述べる）
>
> **Reviewer 2 が要求した「年齢構成・医療供給を適切に調整した独居曝露」を正しく構築した結果、
> 独居高齢者割合（65歳以上人口に占める、単独世帯で暮らす65歳以上人口の割合）と
> 大量点滴療法利用率との間には、無調整の段階から一貫して関連が認められなかった。**
>
> これは事前に想定していた「調整により関連が減衰する」パターンではなく、**曝露を正しく
> 定義し直した時点で関連そのものが消失する**、より厳しい結果である。旧曝露（全世帯に占める
> 65歳以上単独世帯率）が高齢化率と強く相関していた（r=0.63）のに対し、新曝露は高齢化率と
> ほぼ無相関（r=-0.24）であり、旧解析で見えていた「関連」は、独居そのものの効果ではなく、
> 曝露指標が高齢化率の代理変数になっていたことによる交絡であった可能性が高い。
>
> 以下、詳細な数値根拠を示す。
>
> ---
>
> ## 2. データ
>
> 47都道府県、結合キー=JIS都道府県コード。詳細は `variable_dictionary.md` を参照。
> 欠損値・秘匿値なし（全変数で assertion 済み）。
>
> ### 2.1 曝露の再構築が示すもの
>
> | 変数 | 平均 | SD | range |
> |---|---|---|---|
> | `older_living_alone_pct`（新曝露） | 17.74% | 3.13 | 12.09–26.11% |
> | `original_elderly_solo_household_pct`（旧曝露） | 12.58% | 1.90 | 9.40–17.80% |
>
> - 新旧曝露の相関: r = 0.583（別概念ではあるが無関係でもない）
> - 新曝露 と 高齢化率(`ageing_rate_pct`) の相関: **r = -0.242**
> - 旧曝露 と 高齢化率 の相関: **r = 0.625**（Reviewer 2 の懸念を裏付ける）
> - 新曝露 と outcome の単純相関: **r = 0.000334**（事実上ゼロ）
> - 旧曝露 と outcome の単純相関: r = 0.521（旧解析の結果と整合）
>
> ### 2.2 旧解析との数値差異（再現性チェック）
>
> 原稿の単変量結果（β=723.37, SE=172.21, p=0.000124, R²=0.282; outcome分母=2020年人口）に対し、
> Model 0（同じ旧曝露、ただしoutcome分母を本解析の2023年人口推計に統一）は
> **β=656.22（HC3 SE=168.03）, p=0.000094, partial R²=0.272** となり、方向・有意性は一致するが
> 係数はやや異なる。差異はoutcome分母の年次変更（2020→2023人口推計）に由来し、データ処理の誤りではない。
>
> ---
>
> ## 3. Model 0-4（階層的調整モデル）
>
> 主要推論はHC3ロバストSE。通常OLS SEは `results/model_results.csv` に監査用として併記。
>
> | Model | 曝露 | 追加調整変数 | N | 曝露係数 (HC3) | 95% CI | p値 | Adj R² | 曝露 partial R² | AICc |
> |---|---|---|---|---|---|---|---|---|---|
> | 0 | 旧曝露（全世帯比） | なし | 47 | 656.22 | [326.89, 985.55] | **<0.001** | 0.256 | 0.272 | 853.2 |
> | 1 | 新曝露（65+人口比） | なし | 47 | 0.25 | [-249.77, 250.28] | **0.998** | -0.022 | ~0 | 868.1 |
> | 2 | 新曝露 | +高齢化率 | 47 | 117.57 | [-66.52, 301.67] | 0.211 | 0.350 | 0.035 | 848.2 |
> | 3 | 新曝露 | +一般病床数 | 47 | 1.63 | [-177.60, 180.86] | 0.986 | 0.384 | ~0 | 847.1 |
> | 4（主要） | 新曝露 | +WBGT≥28日数 | 47 | -25.73 | [-227.88, 176.42] | 0.803 | 0.423 | 0.001 | 845.6 |
>
> **新曝露を用いた場合、Model 1（無調整）の時点で既に非有意（p=0.998）であり、
> その後の調整（Model 2-4）を経ても係数の符号すら安定しない。** モデルの adjusted R² は
> Model 2以降大きく上昇しているが、これは高齢化率・病床数・WBGTという調整変数自身が
> outcomeの分散をよく説明しているためであり、曝露の寄与ではない。
>
> ---
>
> ## 4. 回帰診断（Model 4）
>
> - Cook's D 閾値 (4/N) = 0.0851
> - 北海道（pref_code=01）: Cook's D = **0.648**（閾値の約7.6倍）, leverage = 0.433 — 突出した影響点
> - 高知（39）: Cook's D = 0.164　広島（34）: Cook's D = 0.138
> - 北海道は環境省WBGT APIで14地域・163観測地点の平均のため、他都道府県よりも地理的異質性が大きい。
>   ただし §5 のLOOで北海道を除外しても結論（曝露非有意）は変わらない。
>
> ---
>
> ## 5. 感度分析
>
> | 分析 | N | 曝露係数 | 95%CI | p値 |
> |---|---|---|---|---|
> | Model 4（基準） | 47 | -25.73 | [-227.9, 176.4] | 0.803 |
> | 病床数→一般診療所数 | 47 | -42.14 | [-193.7, 109.5] | 0.586 |
> | 対数人口密度を追加 | 47 | -66.07 | [-363.7, 231.5] | 0.663 |
> | 東京・大阪・神奈川除外 | 44 | -49.90 | [-347.5, 247.7] | 0.742 |
> | outcome対数変換 | 47 | -0.0091 | [-0.035, 0.017] | 0.486 |
> | 人口重み付きWLS | 47 | -10.79 | [-231.2, 209.6] | 0.924 |
>
> **Leave-one-prefecture-out**（47回）: 曝露係数は -57.59 〜 +20.38 の範囲で符号も不安定。
> **47回全てで95%CIがゼロをまたぐ**（頑健な非有意性。特定の都道府県による駆動ではない）。
>
> ---
>
> ## 6. 非線形性
>
> - 線形 vs 二次項: AICc 845.6（線形） vs 847.9（二次項）、partial F検定 p=0.523 → 二次項に追加説明力なし
> - 線形 vs 自然三次スプライン(df=3): AICc 847.6、p=0.420 → 同様に追加説明力なし
> - 中央値二分解析（補足専用、主結果ではない）: 高群 β=-76.4 (p=0.771)、低群 β=+72.1 (p=0.748) — 
>   いずれも非有意で、旧解析の層別パターン（高群で消失）を単純に再現するものではない
>
> **→ 非線形性を支持する根拠はない。**
>
> ---
>
> ## 7. 多重性（探索的暑熱指標の置換）
>
> Model 4のWBGT≥28日数を他の暑熱指標に置換した場合の**曝露係数**（Benjamini-Hochberg FDR適用対象は
> 各暑熱指標自身のp値）:
>
> | 暑熱指標 | 曝露係数 | p値 | 暑熱指標自体のp値 | FDR調整後p値 |
> |---|---|---|---|---|
> | WBGT≥31日数 | 2.24 | 0.980 | 0.977 | 0.977 |
> | WBGT≥33日数 | -38.85 | 0.677 | 0.018 | 0.055（FDR後は非有意） |
> | 累積超過量(28基準) | 3.61 | 0.969 | 0.700 | 0.977 |
>
> いずれの暑熱指標に置換しても曝露係数は非有意のまま。なお、WBGT≥33日数**そのもの**は
> 補正前p=0.018と名目上有意だが、FDR補正後は非有意（p=0.055）——これはむしろ「暑熱そのものは
> outcomeと関連しうるが、独居状態とは無関係」という副次的知見として本文で言及する価値がある。
>
> ---
>
> ## 8. Comparison-outcome analysis（旧 negative control）
>
> 「6倍」という raw coefficient 比較は廃止し、標準化係数・Pearson r・R²・95%CIのみで比較する。
>
> | Outcome | Pearson r | R² | 標準化β | 95%CI | p値 |
> |---|---|---|---|---|---|
> | 主要outcome（点滴） | 0.0003 | ~0 | 0.0003 | [-0.327, 0.328] | 0.998 |
> | comparison outcome（外来） | 0.169 | 0.029 | 0.169 | [-0.135, 0.473] | 0.275 |
>
> 新曝露を用いると、**comparison outcome（外来利用）の方が主要outcomeよりも名目上強い相関**を示す
> （いずれも非有意）。これは旧解析が主張していた「特異性」（主要outcomeにのみ強く関連する）を
> 支持しない。この分析結果は正直に報告する必要がある。
>
> ---
>
> ## 9. 総合解釈
>
> 1. Reviewer 2 の核心的懸念（曝露が高齢化率の代理変数になっている疑い）は**データによって実証された**（r=0.625）。
> 2. 正しく再構築した曝露（65歳以上人口に占める独居割合）は、**調整の有無に関わらずoutcomeと関連しない**。
> 3. 非線形性・都市影響・複数の暑熱指標・LOO・WLS等、あらゆる感度分析で結論は変わらない（頑健な null）。
> 4. WBGT≥33日数自体は補正前で名目上有意であり、「暑熱は関連するが独居状態は関連しない」という
>    より限定的だが誠実な知見が得られる。
> 5. Comparison outcome分析は「特異性」の主張を支持しない。
>
> **旧解析の中心的主張（独居高齢者割合と点滴療法利用の関連）は、正しく操作化された曝露のもとでは
> 支持されない。** 論文は "hypothesis-generating" どころか、**「見かけ上頑健に見えたエコロジカルな
> 関連が、曝露の誤操作化（年齢構成との交絡）によって生じていたことを示す方法論的知見」**として
> 再定位するのが、データに対して誠実な選択と考えられる。この場合、タイトル・Abstract・Discussion
> の作り直しは、単なる「トーンダウン」ではなく実質的な結論の反転を伴う。
>
> 著者の戦略判断が必要な事項は `issues_for_author.md` §1 にまとめた。
>
> ---
>
> ## 10. 出力ファイル一覧
>
> ```
> 02_Data/interim/major_revision/prefecture_analysis.csv
> 02_Data/interim/major_revision/variable_dictionary.md
> 03_Analysis/results/major_revision/model_results.csv
> 03_Analysis/results/major_revision/model_fit.csv
> 03_Analysis/results/major_revision/vif.csv
> 03_Analysis/results/major_revision/influence.csv
> 03_Analysis/results/major_revision/sensitivity_analyses.csv
> 03_Analysis/results/major_revision/leave_one_out.csv
> 03_Analysis/results/major_revision/nonlinearity.csv
> 03_Analysis/results/major_revision/multiplicity.csv
> 03_Analysis/results/major_revision/median_split_audit_only.csv
> 03_Analysis/results/major_revision/comparison_outcome.csv
> reports/major_revision/source_manifest.csv
> reports/major_revision/reproduction_log.md
> reports/major_revision/issues_for_author.md
> ```

---

以上。次の対応(原稿改訂・point-by-point response・Zenodo新バージョン)は、著者の戦略判断確定後に着手する。

# SONNET REPORT 02: 旧曝露階層調整モデル・G004公開データ確定監査 結果報告

宛先: Codex（`SONNET_WORK_ORDER_03_old_exposure_adjustment_and_G004_audit.md` の起草者）
作成: Sonnet（Claude Code）
作成日: 2026-08-01
対象: IJB Submission ID `0cd18650-d5db-481f-b00b-bbde3cda74f7`（Major Revision）

すべての受入基準（Acceptance criteria）を満たしたことを確認の上、以下を報告する。
本Work Orderの範囲では、原稿・GitHub・Zenodo・投稿システムへの変更は一切行っていない。

---

## 1. G004 都道府県×年齢データの確定判定

**`NOT_PUBLICLY_AVAILABLE`**（確定・独立再検証済み）

第10回NDBオープンデータ公式ページ（`https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177221_00016.html`）
の生HTML（695リンク全件）を取得・解析し、以下を直接確認した。

- G注射見出し直下には「性年齢別」「都道府県別」「診療月別」「二次医療圏別」の4ファイルのみが存在し、
  都道府県×年齢のクロス表は存在しない。
- ページ全体で「都道府県性年齢別」クロス表を持つのは、初診・再診・外来診療料・検査(+3内訳)・手術・
  オンライン診療の限定された9項目のみで、G注射は含まれない。
- 4ファイルを実際にダウンロードして開き、G004（点滴注射）の行を確認。各ファイルは年齢/性・都道府県・
  月・二次医療圏のいずれか1次元のみが変化する構造であり、2次元の同時クロス集計はない。
- この手順は`06_g004_availability_audit.py`としてスクリプト化し、独立実行でも同一結論に到達することを
  プログラムで再検証した。

副次的に、データ期間（診療年月：2023年4月〜2024年3月、FY2023と整合）と秘匿ルール（10未満は「-」、
1箇所のみ秘匿の場合はその行の10以上の値も全て「-」にする二次秘匿）を確認した。

回答書用文章、詳細な出典・ハッシュは `g004_public_data_availability_audit.md` を参照。

---

## 2. O-A〜O-D 推定値（主要outcome、2023年人口分母）

| Model | 追加調整 | N | 曝露係数(HC3) | 95%CI | p値 | 標準化β | Adj R² | 曝露partial R² | AICc |
|---|---|---|---|---|---|---|---|---|---|
| O-A | なし | 47 | 656.22 | [326.9, 985.6] | **<0.001** | 0.521 | 0.256 | 0.272 | 853.2 |
| O-B | +高齢化率 | 47 | 306.14 | [-71.3, 683.5] | 0.112 | 0.243 | 0.365 | 0.056 | 847.1 |
| O-C | +一般病床数 | 47 | 94.09 | [-302.4, 490.6] | 0.642 | — | 0.386 | 0.004 | 846.9 |
| O-D | +WBGT≥28日数 | 47 | -9.41 | [-493.9, 475.1] | 0.970 | -0.007 | 0.422 | 0.00004 | 845.6 |

レガシー2020年人口分母（投稿時と完全同一の分母）でも同一パターン: O-A β=723.37（原稿の報告値と
完全一致、p=0.000041）→ O-B β=310.18（p=0.126）→ O-C β=76.49（p=0.719）→ O-D β=-31.78（p=0.902）。

---

## 3. O-A → O-B 減衰（Reviewer 2への直接回答）

| 指標 | 値 |
|---|---|
| 絶対変化 | -350.08 |
| 係数比（B/A） | 0.467 |
| 記述的減衰率 | **53.3%**（標準化係数でも同一） |
| partial R²変化 | 0.272 → 0.056（-0.216） |
| Adj R²変化 | 0.256 → 0.365（改善） |
| AICc変化 | 853.2 → 847.1（改善） |

O-Bの時点で95%CIが既にゼロをまたぎ、統計的有意性を喪失する。この53.3%は記述的な減衰率であり、
媒介分析（mediation）や「高齢化率が原因を完全に説明した」という主張ではない。

---

## 4. 感度分析・非線形性・影響診断（旧曝露）

- **感度分析（O-D基準）**: 病床→診療所置換、対数密度追加、都市除外、対数変換、WLS、WBGT指標置換
  （31/33/累積超過量）——すべて非有意（p=0.64〜0.97）。
- **Leave-one-prefecture-out（47回）**: 曝露係数 -107.9〜+92.8、**47回全てで95%CIがゼロをまたぐ**。
- **非線形性**: 二次項 p=0.142、自然三次スプライン(df=3) p=0.141——いずれもAICc改善なし、
  非線形性の証拠なし。
- **回帰診断（O-D）**: Cook's D閾値(0.085)超過は北海道(0.667)・高知(0.190)・広島(0.144)。
  新曝露の場合と同一の都道府県が影響点だが、LOOで除外しても結論は不変。
- **都市部除外（東京・大阪・神奈川）**: β=-42.02, p=0.891——結論変わらず。

---

## 5. 新曝露との並置比較

| Stage | O（旧曝露） | N（新曝露） |
|---|---|---|
| 無調整 | β=656.22, p<0.001, 標準化β=0.521 | β=0.25, p=0.998, 標準化β=0.0003 |
| フル調整 | β=-9.41, p=0.970, 標準化β=-0.007 | β=-25.73, p=0.803, 標準化β=-0.034 |

無調整段階ではOとNは全く異なる挙動を示すが、フル調整後は両者とも実質的にゼロへ収束する。
OとNは異なる推定対象（都道府県全体の人口負担 vs 高齢者集団内の独居割合）であり、
「どちらかが誤り」ではなく、両者とも独立調整後にoutcomeとの関連を示さないという結果に収束した。

---

## 6. 選択した解釈分岐

**Branch 2: 年齢構成による交絡と整合する実質的減衰**

O-A→O-Bで53.3%減衰し95%CIがゼロをまたぐ、O-C/O-Dでほぼ完全にゼロへ収束、全感度分析・LOO・
非線形性検定で結論一貫、特定県依存でもない——という一貫した単調減衰パターンに基づく。
Branch 1（残存する人口負担関連）・Branch 3（不確定）はいずれも該当しない。

採用する文言:
> The submitted ecological association was sensitive to population age structure and exposure
> denominator choice.

査読対応ドラフト全文は `original_exposure_additional_analysis.md` §7 を参照。

---

## 7. 未解決の著者判断事項

1. 上記Branch 2解釈で論文の中心命題を確定するかどうかの最終著者判断。
2. WBGT≥33日数の副次的知見（Work Order 01由来、補正前p=0.018、FDR後p=0.055）の本文での扱い。
3. 北海道の地理的異質性（163観測地点平均、両曝露で最大のCook距離）をlimitationとしてどこまで詳述するか。
4. e-Stat appIdの再発行（既存スクリプトが公開GitHubリポジトリに平文で含む、Work Order 01から継続）。
5. Zenodo新バージョン準備（Work Order 02）は本Work Orderでも未着手のまま。

詳細は `issues_for_author.md` §7-9（本Work Orderでの追記分）を参照。

---

## 8. 出力パス・再構築コマンド

```bash
cd projects/NDB_XXX_heatwave_heatstroke

# G004監査
cd 03_Analysis/analysis/major_revision && python 06_g004_availability_audit.py

# レガシーoutcome構築
cd ../../etl/major_revision && python 10_build_legacy_outcome.py

# 旧曝露モデル・感度分析・非線形性・比較・図表
cd ../../analysis/major_revision
python 07_original_exposure_models.py
python 08_original_exposure_sensitivity.py
python 09_original_exposure_nonlinearity.py
python 10_exposure_comparison.py
python 11_original_exposure_coefficient_figure.py
```

主要出力:

```
reports/major_revision/g004_public_data_availability_audit.md
reports/major_revision/g004_public_file_inventory.csv
reports/major_revision/g004_search_log.txt / g004_search_log_rebuild.txt
reports/major_revision/original_exposure_additional_analysis.md
reports/major_revision/verification/independent_verification_OA_OD.py（+ output txt）
03_Analysis/results/major_revision/original_exposure_model_results.csv / _model_fit.csv / _vif.csv
03_Analysis/results/major_revision/original_exposure_attenuation.csv
03_Analysis/results/major_revision/original_exposure_sensitivity.csv / _leave_one_out.csv / _influence.csv
03_Analysis/results/major_revision/original_exposure_nonlinearity.csv / _median_split_audit_only.csv
03_Analysis/results/major_revision/original_vs_new_exposure_comparison.csv
03_Analysis/results/major_revision/tables/table_original_exposure_hierarchy.csv
03_Analysis/results/major_revision/figures/figure_original_exposure_coefficients.png(+source)
03_Analysis/results/major_revision/figures/figure_original_exposure_nonlinearity.png(+source)
02_Data/interim/major_revision/legacy_outcome_2020denominator.csv
02_Data/raw/major_revision/ndb10_g004_audit/（生HTML・4xlsx・2PDF、SHA-256付き）
```

## 9. 再現性チェック結果

- 開始時コミット: `88f91d84585981db2710eaca9aa0ebe2763b03d8`。作業完了時も同一コミット
  （本Work Order中に一切コミット・push・Zenodo操作を行っていないため）。
- O-A〜O-Dの独立再検証（`_common.py`を使わない別実装、statsmodels formula API）を実施し、
  全モデルで係数差 < 1e-6（実際は機械精度、最大差2.8e-14）で一致（`verification/`配下）。
- クリーンな一時ディレクトリ（リポジトリ外、Windows Temp配下）にconfig・キャッシュ済み生データ・
  スクリプト一式をコピーし、ETLチェーン（01-10）と解析チェーン（01, 07-11）をゼロから再実行。
  `prefecture_analysis.csv`、`original_exposure_model_fit.csv`、`original_exposure_attenuation.csv`、
  `original_vs_new_exposure_comparison.csv` は本番出力とバイト単位で完全一致。
- 全ての主要complete-case出力（`prefecture_analysis.csv`, `original_exposure_influence.csv`,
  `original_exposure_leave_one_out.csv`）で47都道府県ユニークを確認。
- Work Order 01の10ファイル（`model_results.csv`等）はすべて存在・非空のまま、上書きなし。
- `02_Data/raw/`配下の既存ファイルへの変更なし（新規サブフォルダへの追記のみ）。
- GitHub・Zenodo・投稿システムへの変更なし（読み取り専用のHTTP GETのみ実行）。

以上、Acceptance criteriaを全て満たした。次の対応（原稿改訂・回答書作成・Zenodo）は著者の
戦略判断確定後に着手する。

---

## 附録A: `issues_for_author.md` 全文

以下は `reports/major_revision/issues_for_author.md`（Work Order 01の§1-6 + Work Order 03の
追記§7-9を含む最新版）の全文をそのまま転載したものである。

> # issues_for_author.md — 著者確認が必要な未解決事項
>
> ## 1. 【最重要・戦略判断】新曝露は主要outcomeと事実上無相関
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
> ## 2. G004の都道府県×年齢クロス表は引き続き未確認
>
> 第10回NDBオープンデータの公開ファイル一覧を再確認する時間の制約上、今回は
> 「既存パイプラインの結論（都道府県×年齢クロス表なし）」を前提として、
> outcomeは全人口ベースの再計算（2023年人口推計）にとどめた。年齢調整outcome
> （65歳以上人口を分母とする、または年齢標準化率）が必要な場合は、
> NDB公式ファイル一覧の再確認が必要。
>
> ## 3. 医療供給2変数の性質が非対称
>
> `general_hospital_beds_per_100k` は厚労省が算出済みの人口10万対公式値をそのまま使用したが、
> `general_clinics_per_100k` は施設数の実数を本解析側で2023年人口推計により自前計算した
> （厚労省側に対応する「人口10万対診療所数」表は見当たらなかった）。分母年が同じ2023年である
> ため実務上の問題はないと考えられるが、完全な出典の一貫性という意味では非対称である。
>
> ## 4. 北海道の地点集計における異質性
>
> WBGT集計は北海道について、環境省API上の14地域（宗谷～檜山）・163観測地点を単純平均して
> 1都道府県値としている。北海道は他都道府県と比べ面積・気候の内部変動が極めて大きく、
> Cook距離でも最大の影響度（0.65、閾値4/N=0.085の約7.6倍）を示した。ただし
> leave-one-prefecture-out感度分析で北海道を除外しても結論（曝露係数は非有意）は変わらない
> ことを確認済み。本文での考察・limitationに明記することを推奨する。
>
> ## 5. e-Stat appIdが公開GitHubリポジトリに平文で残っている
>
> 既存の `03_Analysis/etl/download_prefecture_population_2020.py` 等、複数の既存スクリプトに
> e-Stat appIdがハードコードされたままGitHub公開リポジトリにコミットされている。
> 本再解析の新規スクリプトは `.env`（Git管理外）経由に変更したが、既存スクリプトの修正は
> 本作業のスコープ外とした。**e-Stat側でのAPIキー再発行（漏洩済みキーの無効化）を推奨する。**
>
> ## 6. Zenodo新バージョンの準備は未着手
>
> `SONNET_WORK_ORDER_02` の前提条件（本再解析の数値・出典の独立監査、原稿・回答書の確定、
> 著者の明示承認）が満たされていないため、Zenodo操作は一切行っていない。
>
> ---
>
> ## 7.（Work Order 03 追記）G004都道府県×年齢データは`NOT_PUBLICLY_AVAILABLE`と確定
>
> 公式ページの生HTML・4ファイル（性年齢別・都道府県別・診療月別・二次医療圏別）を実際に
> ダウンロードして中身を確認した結果、G004の都道府県×年齢同時クロス表は存在しないことを
> 確定した（詳細: `g004_public_data_availability_audit.md`）。この判定はスクリプト化して
> 独立再現も行った。年齢調整outcomeの構築は行わず、全人口ベースの粗率を主要outcomeのまま
> 維持する。
>
> ## 8.（Work Order 03 追記）旧曝露は交絡調整で53〜57%減衰し、O-Bの時点で非有意化
>
> Reviewer 2の最低要求（旧曝露＋高齢化率）に直接回答するモデルを実行した結果:
>
> - O-A（旧曝露のみ）: β=656.22, p<0.001
> - O-B（+高齢化率）: β=306.14, p=0.112（**記述的減衰53.3%、95%CIはこの時点でゼロをまたぐ**）
> - O-C（+病床数）: β=94.09, p=0.642
> - O-D（+WBGT）: β=-9.41, p=0.970（ほぼ完全にゼロ、符号も反転）
>
> 投稿時と同一の2020年人口分母で再現しても同様のパターン（減衰率57.1%）。全ての感度分析・
> leave-one-prefecture-out（47回）・非線形性検定で結論は一貫して非有意。
>
> **選択した解釈分岐はBranch 2（年齢構成による交絡と整合する実質的減衰）**。「高齢化率が
> 関連を完全に説明した」という媒介分析的な断定はしていない。詳細と査読対応ドラフトは
> `original_exposure_additional_analysis.md` §6-7 を参照。
>
> ## 9.（Work Order 03 追記）秘匿ルールの詳細確認
>
> NDB公式ファイルのヘッダーに、「集計結果が10未満の場合は『－』で表示（10未満の箇所が1箇所の
> 場合は10以上の最小値を全て『－』で表示）」という二次秘匿ルールが明記されていることを確認した。
> 今回扱ったG004の都道府県別行には秘匿セルはなかったが、他の行・他の医療行為データを扱う際は
> 単純な「10未満→NaN」ではなく、この二次秘匿ルールを前提とする必要がある。

---

## 附録B: `reanalysis_report.md` 全文

以下は `reports/major_revision/reanalysis_report.md`（Work Order 01、新曝露=older_living_alone_pct
に関する詳細解析）の全文をそのまま転載したものである。附録Aと合わせて読むことで、
新曝露（本附録B）と旧曝露（本報告書の本文）の両方の完全な根拠を確認できる。

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

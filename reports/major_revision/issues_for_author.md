# issues_for_author.md — 著者確認事項（統合版、2026-08-01）

Work Order 01〜03で蓄積した項目を統合した現行版。統合前の全文は
`issues_for_author_archive_20260801.md` に保存済み（削除ではなく整理）。

---

## RESOLVED（解決済み）

### R1. 論文の解釈分岐 — Branch 2 で確定

**ステータス: RESOLVED — 著者がBranch 2（年齢構成による交絡と整合する実質的減衰）を選択
（`SONNET_WORK_ORDER_04`にて2026-08-01authorized）。**

新曝露（`older_living_alone_pct`）は無調整の段階からoutcomeと事実上無相関（r=0.0003, p=0.998）。
旧曝露（投稿時の主解析曝露、`original_elderly_solo_household_pct`）はO-A→O-Bで53.3%減衰し
95%CIがゼロをまたぐ。以降の原稿改訂・回答書はこの決定を前提として作成する
（`original_exposure_additional_analysis.md`, `SONNET_REPORT_02...md` 参照）。

### R2. G004都道府県×年齢クロス表の公開有無

**ステータス: RESOLVED — `NOT_PUBLICLY_AVAILABLE` と確定（独立再現済み）。**

公式ページの生HTML（695リンク全件）とG注射の4ファイル（性年齢別・都道府県別・診療月別・
二次医療圏別）を実際にダウンロードして中身を確認し、都道府県×年齢の同時クロス表が
存在しないことを確定した。判定はスクリプト化（`06_g004_availability_audit.py`）して
独立再現も行った。詳細: `g004_public_data_availability_audit.md`。

### R3. O-C標準化係数の「欠落」

**ステータス: RESOLVED — 表示上の転記漏れであり、解析自体には欠落なし。**

`original_exposure_model_results.csv` には元々 O-C の標準化係数（0.0747, HC3 95%CI
[-0.240, 0.390], p=0.642）が正しく計算済みであった。SONNET_REPORT_02の手書き要約表で
「—」と表示されていたのはレポート転記時の見落とし。詳細: `predrafting_corrections_audit.md`。

### R4. 再現性の表現（"exactly reproduced"）

**ステータス: RESOLVED — 表現を訂正。**

「original analysis was exactly reproduced」ではなく「original point estimate was exactly
reproduced（β=723.37, 2020年人口分母）; inferential statistics differed due to HC3 use」と
記述する。詳細: `predrafting_corrections_audit.md`。

### R5. e-Stat appIdの平文ハードコード（現行コードへの対応）

**ステータス: RESOLVED（コード側）— 現在のワーキングツリーには存在しない。**

`03_Analysis/etl/` 配下の12スクリプトを `.env`（Git管理外）経由の読み込みに修正済み
（`grep`で全件確認、py_compileとスモークテストで動作確認済み）。

**未解決の残作業は下記 O1 を参照**（Git履歴からの除去・キー再発行は著者アクションが必要）。

### R6. NDB秘匿ルールの確認

**ステータス: NOTED（対応不要、情報として記録）。**

10未満は「-」表示、1箇所のみ秘匿の場合は同一行の10以上の値も全て「-」にする二次秘匿ルールを
確認済み。今回扱ったG004都道府県別行には秘匿セルはなかった。今後他の医療行為データを扱う際の
参考情報として記録。

---

## OPEN（未解決・著者確認が必要）

### O1. e-Stat appIdのGit履歴除去・キー再発行

コードは修正済みだが、**旧appIdは過去のGitコミット履歴に残ったまま**であり、
ワーキングツリーの修正だけでは公開済み履歴からの漏洩は解消されない。

- 履歴の書き換え（`git filter-repo`等）は破壊的操作のため、著者の明示承認なしに実行していない。
- **著者への推奨アクション**: (1) e-Stat側で旧appIdを失効させ新規キーを発行する、
  (2) 必要であれば履歴書き換えを別途依頼する。
- 詳細な影響範囲・具体的な手順は `estat_appid_security_remediation.md` を参照
  （鍵そのものは伏字表示）。

### O2. 医療供給2変数の出典非対称性

`general_hospital_beds_per_100k` は厚労省算出済みの公式値、`general_clinics_per_100k` は
実数を自前で人口10万対換算した値であり、出典の性質が非対称（対応する公式の「人口10万対
診療所数」表が見当たらないため）。分母年は同じ2023年であり実務上の影響は小さいと考えられるが、
Methodsに明記する。**著者確認**: この非対称性の記述で問題ないか。

### O3. 北海道の地理的異質性

WBGT集計は北海道について14地域・163観測地点の単純平均。Cook距離は両曝露で最大
（旧曝露0.667・新曝露0.648、閾値の約7.6〜7.8倍）。leave-one-prefecture-outで除外しても
結論は不変であることを確認済みだが、Limitationsでの記述の詳しさについて**著者確認**が必要
（現在の草稿では標準的なlimitation文として言及する想定）。

### O4. Zenodo新バージョンの準備

`SONNET_WORK_ORDER_02` の前提条件（原稿・回答書の確定、著者の明示承認）が満たされるまで
Zenodo操作は行わない。Work Order 04の範囲でも、release-candidateフォルダの準備までに留め、
実際の公開は行わない。

### O5. タイトル最終候補の選択

`SONNET_WORK_ORDER_04` の作業用タイトル（"Prefecture-Level Measures of Older Adults Living
Alone and Large-Volume Infusion Therapy Utilization in Japan: Accounting for Population Age
Structure and Heat Exposure"）に加え、Codexが提示した短縮版2案が `revision_decision_memo.md`
に記載されている。**著者確認**: 最終タイトルの決定。

# estat_appid_security_remediation.md

作成日: 2026-08-01
作成: Sonnet（Claude Code）、Work Order 04 §「Security review of the exposed e-Stat appId」対応

このファイルには漏洩したappId自体は記載しない（先頭4文字・末尾4文字のみのマスク表示とする）。

---

## 1. 事実確認（マスク表示）

- 漏洩したappId: `8ee5****...****140d`（先頭4文字・末尾4文字のみ表示）
- **リポジトリの公開状態**: `gh repo view` で確認済み — `github.com/haruki00430/NDB_XXX_heatwave_heatstroke` は **Public**（`isPrivate: false`）。
- **導入コミット**: `3687898`（"chore: initial import from NDB_Research_Hub monorepo"）の1コミットのみ。
- **影響ファイル（12件、いずれもこのコミット以降に他の変更は入っていない）**:
  - `03_Analysis/etl/download_prefecture_population_2020.py`
  - `03_Analysis/etl/download_aircon_prevalence.py`
  - `03_Analysis/etl/download_elderly_household_v2.py`
  - `03_Analysis/etl/download_elderly_household_from_estat.py`
  - `03_Analysis/etl/search_census_population_table.py`
  - `03_Analysis/etl/search_durable_goods_2019.py`
  - `03_Analysis/etl/search_housing_aircon.py`
  - `03_Analysis/etl/search_aircon_table.py`
  - `03_Analysis/etl/search_aircon_table_v2.py`
  - `03_Analysis/etl/debug_estat_api.py`
  - `03_Analysis/etl/get_estat_table_metadata.py`
  - `03_Analysis/etl/search_estat_elderly_table.py`
- **現在のHEAD（コミット済み履歴）にも、まだappIdが残っている**——2026-08-01に実施した
  修正（`.env`経由化）は**現時点でワーキングツリー上の未コミット変更**であり、コミットして
  初めて最新コミットから除去される（それでも過去コミット`3687898`には残り続ける。§2参照）。

## 2. 実施済みの対応（ワーキングツリー・今後のコミット分）

- 上記12ファイルすべてで、平文の `APP_ID = "..."` を撤去し、`python-dotenv` 経由で
  `.env`（Git管理外、`.gitignore`で除外済み）から読み込む方式に統一した。
- `.env.example`（プレースホルダのみ、実キーなし）を新規作成し、`.gitignore` に
  `!.env.example` の除外ルールを追加して、`.env.example` 自体はコミット可能な状態にした
  （`.env` 本体は引き続きGit管理外）。
- 全12ファイルの構文チェック（`py_compile`）と、代表1ファイルでの実際のAPI呼び出しに
  よるスモークテストを実施し、修正後も正常動作することを確認済み。
- 上記修正はコミットしていない（本Work Orderの指示により、著者の別途承認なしにコミット・
  pushは行わないため）。

## 3. 実施していない対応（著者の明示承認が必要）

以下は本Work Orderの指示により**意図的に実施していない**。

- Gitコミット履歴の書き換え（`git filter-repo`, `BFG Repo-Cleaner`等）によるappId除去。
- 上記ワーキングツリー修正のコミット・GitHubへのpush。
- e-Stat側での旧appIdの失効・新規appIdの発行（Sonnetはe-Statアカウントの認証情報を
  保有しておらず、実行不可能でもある）。

## 4. 著者が実施すべきアクション（推奨、優先順位順）

1. **最優先・直ちに実施可能**: e-Stat（政府統計の総合窓口）の利用者ページにログインし、
   現在のappId（`8ee5****...****140d`）を失効させ、新しいappIdを発行する。
   これにより、Git履歴に残る旧キーは無効な文字列になり、実質的なリスクがなくなる
   （**履歴の書き換えより迅速かつ確実な対処**）。
2. 新しいappIdを、リポジトリ直下の `.env` ファイル（`ESTAT_APP_ID=新しい値`）にのみ記載する。
   `.env` は既に `.gitignore` で除外済みのため、通常のコミット操作で誤ってpushされることはない。
3. 本Work Orderで用意した12ファイルの `.env` 化修正を確認の上、問題なければ通常のコミット
   （`git add` → `git commit`）でリポジトリに反映する。**この時点でappIdはコード上には
   一切残らない（新HEADのみ。過去コミットには引き続き残る）。**
4. 過去のGit履歴（コミット`3687898`）から旧appIdを完全に除去したい場合は、
   `git filter-repo` 等による履歴書き換えと、GitHubへの force-push が必要になる。
   これは**破壊的操作**であり、他の共同作業者のクローンとの不整合、既存のフォーク・
   PRへの影響が生じうるため、実施する場合は事前に必ずSonnet（またはCodex）へ
   明示的に指示すること。**旧キーが失効済みであれば、この手順は必須ではない**
   （リスクの実体は「有効なキーが公開されている」ことであり、失効済みキーが履歴に
   残ること自体は実害が小さい）。

## 5. 結論

**コードの修正だけでは、最新ファイルからappIdが消えるのみで、Git履歴（コミット`3687898`）
からは消えない。** 実質的なリスクを解消する最も確実な方法は、履歴の書き換えではなく
**e-Stat側での旧appIdの失効**である。履歴書き換えは著者が望む場合にのみ、別途の承認を
得たうえで実施する。

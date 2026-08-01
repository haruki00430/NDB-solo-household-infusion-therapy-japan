# g004_public_data_availability_audit.md

## 判定

**`NOT_PUBLICLY_AVAILABLE`**

第10回NDBオープンデータにおいて、G004（点滴注射、500mL以上）の都道府県別集計と
性年齢別集計はそれぞれ独立した周辺表（marginal table）としてのみ公開されており、
**都道府県×年齢の同時クロス集計表は公開されていない。**

この判定は、以下の通り前回の結論（Codex/Sonnetの既存判断）を無条件に踏襲したのではなく、
公式ページの完全なファイル構造を実機で再取得・再確認した結果として得たものである。

## 根拠

### 1. 公式ページの完全な列挙

出典: 第10回NDBオープンデータ公式ページ
`https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177221_00016.html`
（生HTML保存: `02_Data/raw/major_revision/ndb10_g004_audit/ndb10_official_page_20260801.html`,
SHA-256: `1cf603a602b64a1fafb38c6d971b36b6c6545b8eaf277521375f1cd75cb25781`）

このページの「医科診療行為（算定回数）」セクション（695リンク中）を全て解析した結果、
G注射の見出し（`<h4>G注射</h4>`）の直後には以下4ファイルのみが存在し、次の見出し
（`H リハビリテーション`）まで他のファイルは存在しない。

| ファイル | 内容 | URL | サイズ | SHA-256 |
|---|---|---|---|---|
| 001493140.xlsx | 性年齢別算定回数 | `/content/12400000/001493140.xlsx` | 44,760B | `1eb64eab...20512` |
| 001493141.xlsx | 都道府県別算定回数 | `/content/12400000/001493141.xlsx` | 51,101B | `281f45f4...b9188` |
| 001493142.xlsx | 診療月別算定回数 | `/content/12400000/001493142.xlsx` | 30,620B | `a56efc66...60287` |
| 001493143.xlsx | 二次医療圏別算定回数 | `/content/12400000/001493143.xlsx` | 194,791B | `06417adb...9c02a` |

### 2. 都道府県×性年齢クロス表が存在するカテゴリの完全列挙

公式ページ全体から「都道府県性年齢別」という文字列を含むリンクを正規表現で網羅的に
抽出した結果、該当するのは以下のカテゴリの算定回数版・患者数版のみ（計18ファイル）。

> 初診、再診、外来診療料、検査（および血液学的検査判断料・血液採取（静脈）・
> 生化学的検査（１）判断料の内訳3項目）、手術、オンライン診療

**G注射（G004を含む）はこのリストに含まれない。** クロス表が存在するカテゴリは限定的で、
すべてのカテゴリに存在するわけではないことが確認できた。

### 3. ファイル内容の直接確認

ダウンロードした4ファイルをopenpyxlで開き、G004（点滴注射）の行を特定した。

- **性年齢別ファイル（001493140.xlsx）**: 列は「男・女」×「5歳階級」のみ。都道府県列は存在しない。
- **都道府県別ファイル（001493141.xlsx）**: 列は47都道府県コード（01～47）＋全国計のみ。年齢列は存在しない。
- **診療月別ファイル（001493142.xlsx）**: 列は診療月（2023年4月～2024年3月）のみ。
- **二次医療圏別ファイル（001493143.xlsx）**: 列は二次医療圏（都道府県より細かい単位）のみ。年齢列は存在しない。

**4ファイルのいずれも、2つ以上の次元を同時にクロス集計したものではない。**

### 4. データ期間・秘匿ルールの確認（副次的成果）

- ファイルヘッダーより、データ期間は「診療年月：2023年04月～2024年03月」であることを確認
  （原稿のFY2023表記と整合）。
- 秘匿ルール: 「集計結果が10未満の場合は『－』で表示（10未満の箇所が1箇所の場合は10以上の
  最小値を全て『－』で表示）」——単純な「10未満→NaN」より厳格な二次秘匿ルールが明記されている。
  G004行自体（都道府県別ファイル）には秘匿セルは見当たらなかったが、他の行・他のクロス表を
  扱う際はこのルールを前提とする必要がある。

## 回答書に使用可能な文章

> We re-examined the complete public file structure of the Tenth NDB Open Data. Age-stratified
> G004 counts and prefecture-level G004 counts were available only as separate marginal tables;
> jointly age-stratified prefecture-level counts for G004 were not publicly available. We therefore
> could not calculate a prefecture-specific age-standardized or older-population-specific G004 rate.

## 結論の位置づけ

条件分岐（work order Part 1）に従い、`NOT_PUBLICLY_AVAILABLE` であるため、Part 1の
「Conditional age-specific branch」（年齢別outcomeの構築）は**実施しない**。
Primary outcomeは引き続き全人口（2023年推計人口）を分母とした粗率とする。

## 出典ファイル一覧

詳細は `reports/major_revision/g004_public_file_inventory.csv` および
`reports/major_revision/g004_search_log.txt` を参照。

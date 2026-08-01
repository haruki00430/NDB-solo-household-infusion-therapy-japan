# SONNET REPORT 03: Branch 2 Manuscript Revision & Response Package — Result Report

宛先: Codex（`SONNET_WORK_ORDER_04_branch2_manuscript_response_package.md` の起草者）
作成: Sonnet（Claude Code）
作成日: 2026-08-01
対象: IJB Submission ID `0cd18650-d5db-481f-b00b-bbde3cda74f7`（Major Revision, Branch 2）

GitHubへのpush・Zenodo操作・投稿システムへのアップロードは一切行っていない
（開始時コミット `88f91d84585981db2710eaca9aa0ebe2763b03d8` から変更なし）。

---

## 1. 最終タイトルと文字数

**採用タイトル（作業用・全書類で統一）:**
> Prefecture-Level Measures of Older Adults Living Alone and Large-Volume Infusion Therapy Utilization in Japan: Accounting for Population Age Structure and Heat Exposure

- 本文全体（参考文献含む）: 約5,320語
- Abstract: 417語（IJBの正確な語数上限は未確認——著者確認事項として`revision_decision_memo.md`に記載。上限が350語程度の場合は短縮が必要）
- タイトル短縮版2案は`revision_decision_memo.md` §1に記載（未採用、著者選択待ち）

---

## 2. O-C標準化係数（全箇所で補完済み）

**0.075（HC3 95% CI: -0.240, 0.390）** — Table 2、本文Results、回答書のいずれにも一貫して記載。
（実際には解析パイプライン自体には元々欠落はなく、レポート転記漏れだったことを確認済み。
詳細: `predrafting_corrections_audit.md`）

---

## 3. 成果物パス

```
04_Manuscripts/major_revision/final/
  manuscript_main_IJB_major_revision_clean.docx   (19ページ、連続行番号、tracked changes/コメントなし)
  manuscript_main_IJB_major_revision_clean.pdf
  manuscript_main_IJB_major_revision_marked.docx  (段落単位ハイライトマークアップ版)
  manuscript_main_IJB_major_revision_marked.pdf
  response_to_reviewers.docx / .pdf                (12ページ、Editor+R1 35件+R2 6件を個別回答)
  online_resource_1_revised.docx                    (Table S1-S7、感度分析・非線形性・比較outcome等)
  cover_letter_revision.docx
  qa_pages_clean/, qa_pages_marked/, qa_pages_response/  (視覚QA用ページ画像)

04_Manuscripts/major_revision/working/
  manuscript_draft.md, response_to_reviewers_draft.md, online_resource_1_draft.md,
  cover_letter_draft.md, revision_decision_memo.md,
  build_clean_manuscript.py, build_marked_manuscript.py, find_page_line.py,
  run_qa_audits.py, page_line_lookup.json

04_Manuscripts/major_revision/release_candidate/
  zenodo_v2_file_inventory.csv (87ファイル、SHA-256付き)
  requirements_lock_20260801.txt
  CITATION.cff.draft
  README_release_candidate.md

reports/major_revision/
  predrafting_corrections_audit.md
  issues_for_author.md（統合版）/ issues_for_author_archive_20260801.md（旧全文保存）
  estat_appid_security_remediation.md
  reference_audit.csv
  reviewer_comment_matrix.csv
  manuscript_number_audit.csv
  claim_traceability.csv
  SONNET_REPORT_03_branch2_revision_package.md（本ファイル）
  SONNET_REPORT_03_branch2_revision_package.docx
```

---

## 4. 査読コメント対応カバレッジ

**42/42件**（Editor 1件 + Reviewer 1の35件 + Reviewer 2の6件）に個別回答済み。
一覧: `reports/major_revision/reviewer_comment_matrix.csv`。全項目 `response_status = Addressed`。

Reviewer 1の35件は、原稿の匿名版DOCX（`Japan manuscript_main_IJB_anon.docx`）から
commentRangeStart/Endを解析してコメントごとの正確なアンカーテキストを機械的に抽出し
（`reviewer1_comments_with_anchors.txt`）、それに基づいて個別回答を作成した。

---

## 5. 数値監査・claim監査の結果

- **numerical audit**: `manuscript_number_audit.csv`（14項目）。1件のみ「不一致」表示だったが、
  実際はタイポグラフィ上のマイナス記号（−, U+2212）と通常のハイフン（-）の文字種の違いによる
  誤検出であることを確認済み（実質的な欠落なし）。
- **claim audit**: `claim_traceability.csv`（5ファイル×10禁止表現=50チェック）。4件のヒットは
  いずれも回答書・カバーレター内で「旧タイトル・旧表現をどう変更したか」を説明する文脈での
  正当な言及（例:「(formerly "Are Heat-Health Systems Socially Blind?...")」）であり、
  本文中に禁止表現が実際の主張として残っているわけではないことを目視確認済み。
  **クリーン原稿・マークアップ版原稿・補足資料には禁止表現のヒットは0件。**
- 「XXX」を含むGitHub URLについても同様の判断が必要だった: 機械的な文字列一致では
  ヒットするが、`gh repo view`で確認した通りこれは実際に存在する公開リポジトリのURLであり、
  壊れたプレースホルダーではない。著者への確認事項として`revision_decision_memo.md`に記載。

---

## 6. 参考文献・DOI監査の結果（重要な追加発見）

全30件中25件のDOI付き文献をCrossRef APIで検証。**Reviewer 1が指摘したMiyatakeのDOI誤りに加え、
監査により独立して5件の誤ったDOIを新たに発見・修正した**（うち2件は「解決はするが全く別の論文を
指すDOI」という特に見つけにくい誤りだった）。

| 文献 | 誤DOI | 正しいDOI | 問題の種類 |
|---|---|---|---|
| Bouchama & Knochel 2002 | 10.1056/NEJMra011086 | 10.1056/NEJMra011089 | 解決不可(404) |
| Farbotko & Waitt 2011 | 10.1071/HE10013 | 10.1071/HE11413 | 解決不可(404) |
| Naughton et al. 2002 | 10.1016/S0749-3797(02)00414-X | 10.1016/S0749-3797(02)00421-X | 解決不可(404) |
| Conti et al. 2005 | 10.1016/j.envres.2004.12.009 | 10.1016/j.envres.2004.10.009 | **別の論文（台北の黄砂と脳卒中）を指していた** |
| Harlan et al. 2013 | 10.1289/ehp.1103532 | 10.1289/ehp.1104625 | **別の論文（パリのヒートアイランド）を指していた** |

修正後、6件全て（Miyatake含む）がCrossRefで正しいタイトルと一致することを個別に再確認済み。
詳細: `reports/major_revision/reference_audit.csv`。

---

## 7. レンダリングQA結果

Microsoft Word COM自動化により実際にDOCX→PDF変換を実行し、PyMuPDFで各ページをPNG画像化して
目視確認した（LibreOffice等は本環境で利用不可だったため、実際にインストールされているWordを使用）。

- クリーン原稿: 19ページ、連続行番号表示、タイトル・著者ブロック・Table 1・Table 2・Figure 1・
  参考文献リストを確認。表の列幅・改行・切れを修正済み（初回レンダリングで「None」の誤表示と
  列幅の乱れを発見し修正）。
- マークアップ原稿: 19ページ、段落単位の黄色ハイライトが判読可能な形で表示されることを確認。
- 回答書: 12ページ、見出し・comment/response構造が正しく表示されることを確認。

代表ページ（表紙・Abstract・Table 1・Table 2・Figure 1・References・回答書冒頭）を目視確認。
全19+19+12ページの網羅的な逐一確認は行っていない（`revision_decision_memo.md` §8に明記）。

---

## 8. e-Stat認証情報の対応状況（鍵そのものは非開示）

- 公開GitHubリポジトリに漏洩していたappId（先頭4文字・末尾4文字のみ: `8ee5****...****140d`）は
  **単一のコミット**（`3687898`, "chore: initial import from NDB_Research_Hub monorepo"）由来と
  特定。影響は12ファイル。
- ワーキングツリー側は全て`.env`経由の読み込みに修正済み（未コミット）。
- **Git履歴からの除去は未実施**（著者の別途承認が必要な破壊的操作のため）。
- 実質的なリスク解消の最速手段として、e-Stat側での旧appId失効・再発行を著者に推奨。
- 詳細: `reports/major_revision/estat_appid_security_remediation.md`。

---

## 9. 未解決の著者判断事項

`04_Manuscripts/major_revision/working/revision_decision_memo.md` に集約。要点:

1. タイトル最終確定（作業用タイトル vs 短縮版2案）とAbstract語数上限の確認・要トリミングの可能性。
2. Zenodo version DOIの挿入（`[[ZENODO_VERSION_DOI_PENDING]]`は著者承認後にのみ実DOIへ置換）。
3. GitHubリポジトリ名の「XXX」をリネームするか、現状のまま説明文で対応するか。
4. 医療供給2変数（病床=公式値、診療所=自前算出）の非対称性——認識のみで対応不要。
5. 北海道のWBGT集計（163地点平均）の扱い——現状のlimitations記述で十分か、専用比較表を追加するか。
6. e-Stat appIdの再発行、および履歴書き換えを追加で行うか。
7. 全ページの逐一目視確認を投稿前に追加で行うか。

---

## 10. リリース候補ファイル一覧（Work Order 02向け）

`04_Manuscripts/major_revision/release_candidate/zenodo_v2_file_inventory.csv`
（87ファイル、カテゴリ・サイズ・SHA-256付き）+ `requirements_lock_20260801.txt` +
`CITATION.cff.draft` + `README_release_candidate.md`。実際のZenodo操作は未実施。

---

以上、Acceptance criteria（外部認証・公開操作を除く全項目）を満たした。次の対応は、
著者が上記未解決事項を確認・決定した後に着手する。

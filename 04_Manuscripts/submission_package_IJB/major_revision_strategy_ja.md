# Major Revision 対応方針

## 結論

本件は、本格的な再解析を伴う Major Revision として対応する価値が高い。Reviewer 2 の中心条件は、(1) 年齢構成、(2) 医療供給、(3) 非線形性・都市影響、(4) より妥当な暑熱指標を扱った後に、観察された関連がどの程度残るかを示すことである。

ただし、論文の回収可能性を「関連が有意に残ること」だけに依存させない。改訂後の問いは次のように置く。

> To what extent is the prefecture-level association between living alone among older adults and large-volume infusion use explained by population ageing, healthcare supply, and heat exposure?

関連が減衰または消失しても、その結果を主要知見として正確に報告する。

## 現稿から判明した重要事項

- 原稿は都道府県を単位とする N=47 の生態学的横断研究である。
- Reviewer 1 の添付原稿には35件のコメントがある。
- 現曝露は「全世帯に占める65歳以上単独世帯の割合」であり、高齢化率と独居傾向を分離できない。
- G004は熱中症・脱水に特異的ではない。タイトルでは `dehydration-related` を外す。
- `living alone` は `social isolation` と同義ではない。主解析・タイトル・結果では前者を使い、後者は仮説上の機序として限定的に扱う。
- 「多重共線性のため単変量回帰を採用」は維持しない。交絡因子は事前指定し、VIFが高くても推定値と不確実性を提示する。
- 公開されている第10回NDBのG注射には、都道府県別、性年齢別、診療月別の各集計はあるが、G004の都道府県×性年齢クロス表は公開一覧に見当たらない。したがって、G004の都道府県別年齢標準化率または65歳以上率を主計画に前提化しない。
- 原稿中のGitHub URLには `XXX` が残っている。
- Miyatake et al. のDOIは現稿の `10.1007/s12199-011-0267-9` ではなく `10.1007/s12199-011-0221-2`。

## 改訂後の主要変数

### Outcome

- 第10回NDB Open DataのG004算定回数。
- 2023年10月1日人口推計を分母とした人口10万人当たり率を再計算する。
- 名称は `large-volume infusion procedure rate` とする。
- 脱水または暑熱との関係は、非特異的な可能性を含む補助的解釈に限定する。

### Primary exposure

- 2020年国勢調査の「65歳以上単独世帯数」を、2020年の65歳以上人口で除した割合。
- 表現は `percentage of adults aged >=65 years living alone` を優先する。
- 旧指標（全世帯に占める65歳以上単独世帯率）は原解析再現用として保持する。

### Prespecified confounders

- 都道府県の65歳以上人口割合：2023年人口推計。
- 一般病床数（病院）／人口10万人：2023年医療施設調査。精神病床を含む総病床数より一般病床を優先する。
- 主暑熱指標：環境省の2023年公式WBGTから作成した、日最高WBGTが28以上の日数。複数地点を用いる場合は、地点別日数を算出後、都道府県内で平均する。

### Secondary/sensitivity covariates

- 一般診療所数／人口10万人。
- 日最高WBGT 31以上の日数。
- 日最高WBGT 33以上の日数（「アラート日」とは呼ばない）。
- 累積超過量 `sum(max(daily maximum WBGT - 28, 0))`。
- 対数人口密度。
- 空調保有率は使用率ではないため主解析から外し、残す場合も探索的補足解析とする。

## 解析仕様

### 主モデル

- Model 0: 旧曝露のみ（現稿結果の再現）。
- Model 1: 新曝露のみ。
- Model 2: Model 1 + 65歳以上人口割合。
- Model 3: Model 2 + 一般病床数／10万人。
- Model 4: Model 3 + 日最高WBGT 28以上の日数。

各モデルで、未標準化係数、標準化係数、95% CI、p値、adjusted R2、曝露のpartial R2、VIFを報告する。推論はHC3ロバスト標準誤差を主とし、通常のOLS標準誤差を再現性確認用に保持する。

### 診断・感度分析

- 残差、レバレッジ、Cook's distance、DFBETAs。
- leave-one-prefecture-outで曝露係数の分布を示す。統計的有意性の回数を頑健性の根拠にしない。
- 東京・大阪・神奈川の同時除外。
- 対数人口密度の追加調整。
- 一般病床を一般診療所数へ置換。
- outcomeの対数変換。
- 人口を重みとするWLSを探索的に実施し、非加重OLSとの差を示す。

### 非線形性

- 線形モデルを基準とする。
- 二次項モデルを事前指定の非線形性検定とし、線形モデルとpartial F testおよびAICcで比較する。
- 自然三次スプライン（自由度3）は探索的感度分析とする。
- 中央値二分解析は主結果から外す。残す場合は旧解析の再現として補足資料に置く。

### 多重比較

- Model 4を主要推論とする。
- WBGT 31、33、累積超過量およびその他の気候指標は探索的と明示し、Benjamini-Hochberg FDRを併記する。
- p値の閾値だけで結論を分岐させず、効果量と95% CIを中心に記述する。

### Comparison outcome

- 一般外来利用は `negative control` と呼ばない。
- 残す場合は `exploratory comparison-outcome analysis` とし、標準化係数、相関、R2、95% CIのみを比較する。
- raw coefficientの「約6倍」は削除する。

## タイトルと論文の再定位

推奨タイトル：

> Prefecture-Level Prevalence of Older Adults Living Alone and Large-Volume Infusion Therapy Use in Japan: A Hypothesis-Generating Ecological Study

主張の基本形：

> The findings warrant further evaluation of whether routinely available indicators of living arrangements could complement meteorological surveillance.

警報システムを直接評価したとの表現、`socially blind`、`social isolation was the only factor`、気候指標を社会指標が上回ったとの表現は削除する。

## データ年次の整理

- Outcome: FY2023 NDB。
- Outcome denominator and ageing rate: 2023年10月1日人口推計。
- Living-alone exposure: 2020年国勢調査（最新の悉皆国勢調査として説明）。
- Healthcare supply: 2023年医療施設調査。
- Heat: 2023年6月から9月の環境省WBGT。
- 2014年空調保有率は主解析から外す。

2023年夏は、当時、1898年の統計開始以降で最も高温だった。2026年時点では2025年が最高で、2023年は2024年と並ぶ次点であるため、本文では `the hottest Japanese summer on record at that time` とする。

## Sonnetとの分担

1. Codexが解析仕様、変数辞書、受入基準を固定する。
2. Sonnetが一次資料からデータを取得し、出典URL、取得日時、ファイルハッシュ、変換ログを残す。
3. Sonnetが再現可能なスクリプトで解析し、機械可読な結果と図表を出力する。
4. Codexが数値、モデル式、データ由来、文章との整合を独立監査する。
5. 結果を見て、原稿、補足資料、point-by-point responseを改訂する。
6. SonnetがZenodoの新バージョンドラフトを作成する。
7. Codexがドラフト内容とDOI記載を確認する。
8. 著者の明示承認後にのみSonnetがZenodoを公開する。

Sonnetに渡す指示は、データ取得と解析、Zenodo更新を別作業にする。解析結果が確定する前にZenodoを変更しない。

## 延長申請

推奨送信文：

> Subject: Request for extension - Submission ID 0cd18650-d5db-481f-b00b-bbde3cda74f7
>
> Dear Dr Fitchett,
>
> Thank you for the opportunity to revise our manuscript. To address the reviewers' substantive requests concerning population age structure, healthcare supply, nonlinearity, and improved WBGT measures, we would be grateful for an extension of the revision deadline to 4 September 2026. This additional time would allow us to complete the requested analyses and provide a careful point-by-point response.
>
> Submission ID: 0cd18650-d5db-481f-b00b-bbde3cda74f7
>
> Kind regards,  
> Haruki Saito

## 完了条件

- 47都道府県が一意に結合され、欠損と抑制値の処理が文書化されている。
- 元データは変更せず保存され、すべての派生値がコードから再生成できる。
- 主結果の表・図・本文・回答書で数値が一致する。
- Reviewer 1の35件とReviewer 2の6項目に一対一で応答する。
- clean manuscriptにtracked changesを残さず、必要なら別にmarked-up版を作る。
- GitHubリンク、全DOI、Zenodoのversion DOIを最終確認する。
- AI利用声明を実際の作業内容に合わせて更新する。


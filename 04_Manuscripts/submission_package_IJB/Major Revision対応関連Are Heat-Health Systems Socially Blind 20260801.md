
以下コメント推移

## 結論

これは、**十分にアクセプトへつながり得るMajor Revision**です。少なくとも、拒絶に近い形式的な改訂要求ではありません。

Reviewer 1はテーマを「interesting」と評価し、追加説明と主張の抑制で改善可能としています。Reviewer 2も「important and timely」「useful contribution」と評価したうえで、**年齢構成と医療供給を調整した後にも関連が残ること**を主要条件としています。編集者も、正確な結果報告、過大主張の修正、限界の十分な説明を求め、改訂後の迅速な判断を示唆しています。

したがって、今回は文章修正だけではなく、**解析設計を一段階引き上げる本格的な改訂**が必要です。

## 最重要の判断

Reviewer 2の以下の2点には、反論せず全面的に対応すべきです。

1. **高齢化率による交絡**
2. **病床・診療所など医療供給による交絡**

現稿の「多重共線性があったため単変量回帰を用いた」という説明は、今回の改訂では維持できません。Reviewer 2が明確に「collinearity does not remove the need to address this confounding」と指摘しているためです。

現在の曝露である「全世帯に占める65歳以上単独世帯率」は、社会的孤立だけでなく、都道府県の高齢化そのものを含んでいます。これは今回の最も本質的な弱点です。

## 推奨する解析改訂

### 1. 曝露指標を再構築する

現行指標に加えて、次を作るのが最善です。

> **65歳以上人口に占める、単独世帯で暮らす65歳以上人口の割合**

これにより、「高齢者が多い県」と「高齢者の中で独居が多い県」を分離できます。

2020年国勢調査には、都道府県別の65歳以上人口と65歳以上単独世帯・単独世帯人員を取得できる表があります。したがって、Reviewer 2への対応は実行可能です。

推奨モデルは、段階的に示します。

- Model 1：独居高齢者割合のみ
- Model 2：＋65歳以上人口割合
- Model 3：＋医療供給指標
- Model 4：＋主要な暑熱指標

標準化β、95% CI、部分R²、VIFも報告します。

NDBに都道府県×年齢別のG004件数が存在する場合は、65歳以上人口を分母とした率または年齢標準化率を最優先します。利用できない場合は、そのデータ構造を明示したうえで、高齢化率を調整したモデルを提示します。

### 2. 医療供給を追加する

主解析には、まず以下を1つ入れるのが妥当です。

> **一般病院病床数／人口10万人**

感度分析として、

> **一般診療所数／人口10万人**

を追加します。

2023年医療施設調査には、都道府県別の病床数、診療所数、医師数などが提供されています。したがって、「入手不能」とする必要はありません。

N＝47なので、供給変数を多数同時投入するのではなく、**病床数を主指標、診療所数を感度分析**とするのが安全です。

### 3. WBGTを全面的に改善する

現在の「日平均気温から簡易式で推定した平均WBGT」は、Reviewer 2の指摘どおり弱い指標です。現稿自身もピーク屋外暑熱を過小評価し得ると認めています。

改訂では、環境省が公開している公式の日最高WBGTデータを使い、例えば以下を算出します。

- 日最高WBGT 28以上の日数
- 日最高WBGT 31以上の日数
- 日最高WBGT 33以上の日数
- 累積WBGT超過量：Σ max（日最高WBGT－28, 0）

環境省は過去の日最高WBGTを提供しており、WBGT 28以上で熱中症発生が顕著に増えること、熱中症警戒アラートの基準が33以上であることを示しています。

なお、2023年夏は「通常の夏」ではなく、当時1898年以降で最も高温の夏でした。この事実をMethodsまたはDiscussionに明記し、単年度結果の一般化可能性を制限として扱います。

### 4. 非線形性と都市影響を検証する

現在の中央値二分による層別解析は、主結果としては外した方がよいです。高群で関連が消失しており、単純な用量反応を支持しないからです。

代わりに、

- 線形モデル
- 二次項モデル
- 制限付き三次スプライン、または自然スプライン
- 線形モデルとの適合度比較
- leave-one-prefecture-out解析
- 東京・大阪・神奈川除外
- 人口密度調整

を実施します。

中央値層別解析は、残すとしても「探索的補足解析」に格下げします。

### 5. Negative controlを修正する

「βが約6倍」という記述は削除が必須です。アウトカムの尺度が異なるため、raw coefficient同士を比較できないというReviewer 2の指摘は正当です。

比較するなら、

- 標準化β
- Pearsonのr
- R²
- 95% CI

に限定します。

また、一般外来利用も年齢・アクセス・供給の影響を受けるため、**negative controlではなく“comparison outcome analysis”**と呼び替えるのが安全です。

## 論文の再定位

現在のタイトル、

> Are Heat-Health Systems Socially Blind?

は魅力的ですが、今回は外すべきです。警報システム自体を評価していないため、Reviewer 2と編集者の双方が求める「記述的で過大でない論文」に合わせます。

第一候補は以下です。

> **Prefecture-Level Elderly Solo Household Prevalence and Large-Volume Infusion Therapy Utilization in Japan: A Hypothesis-Generating Ecological Study**

「dehydration-related」も、タイトルと主解析では避け、本文中で、

> large-volume infusion therapy utilization, which may include a heat-related dehydration component

程度に抑えます。G004は熱中症や脱水に限定されず、現稿でも夏季ピークを確認できないことが記載されています。

政策結論も、

> social vulnerability indicators should be integrated

から、

> the findings support further evaluation of whether social vulnerability indicators could complement meteorological surveillance

程度に変更します。

## Reviewer 1への対応

Reviewer 1の多数のインラインコメントは、主として次の内容です。

- 都道府県レベル研究であることの明確化
- 略語の初出時展開
- 「informal monitoring」の具体化
- 1年のみを扱う理由
- 2023年夏の異常性
- 35℃をheatwaveと呼ぶ根拠
- 線形性とラグ
- エアコンの所有と使用の区別
- 高齢者の口渇低下・飲水不足
- 点滴が行われる他の疾患・状況
- DOI確認
- 小数桁削減
- 低いR²の慎重な解釈

これらはほぼすべて受け入れて修正できます。特に35℃以上は「heatwave days」ではなく、気象庁用語に近い **extremely hot days** または単に **days with maximum temperature ≥35°C** とするべきです。

## 採択可能性の見通し

私の現時点での条件付き予測は以下です。

- 年齢・供給調整後も関連が明確に残る：**65～80%**
- 効果が半分程度に減衰するが方向性が残る：**50～65%**
- 95% CIがゼロをまたぐが方向性と非線形パターンが残る：**35～50%**
- 年齢・供給調整後にほぼ完全に消失する：**20～35%**

関連が弱くなっても、結果を隠したり旧主張を守ったりせず、**「独居指標の未調整関連は、年齢構成と医療供給によりどの程度説明されるか」**という、より科学的に堅い論文へ転換すれば回収可能性は残ります。

## 締切について

推奨締切は2026年8月14日ですが、この内容には新規データ取得、再解析、本文全面改訂、35件のインライン対応、回答書作成が必要です。

したがって、**直ちに9月4日頃までの延長を申請することを推奨します**。理由は簡潔で十分です。

> Dear Dr Fitchett,  
> Thank you for the opportunity to revise our manuscript. To address the reviewers’ substantive requests regarding population age structure, healthcare supply, nonlinearity, and improved WBGT measures, we would be grateful for an extension of the revision deadline to 4 September 2026. This additional time would allow us to complete the requested analyses and provide a careful point-by-point response.  
> Kind regards,  
> Haruki Saito

今回の改訂では、**旧主張を守ることではなく、交絡を正面から処理して、結果がどこまで残るかを誠実に示すこと**がアクセプトへの最短経路です。



はい、この進め方が適切です。原稿と査読資料を照合したところ、十分に対応可能なMajor Revisionですが、解析の問い自体を再定義する必要があります。査読PDF と、35件のReviewer 1コメントを含む原稿 を確認しました。

重要な補正点は次のとおりです。

- 第10回NDBでは、G004の「都道府県×年齢」クロス集計は公開一覧に見当たりません。したがって、年齢別G004率を前提にせず、2023年高齢化率による調整を確実に実施する設計としました。[第10回NDB公式ページ](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177221_00016.html)
- 曝露は「社会的孤立」ではなく、厳密には「高齢者のうち独居する者の割合」です。`living alone` と `social isolation` を同義に扱わないことが重要です。[2020年国勢調査の該当表](https://www.e-stat.go.jp/stat-search/files?cycle=0&layout=dataset&month=0&stat_infid=000001086178&tclass1=000001011805&toukei=00200521&tstat=000001011777&year=20200)
- G004は脱水・熱中症に特異的でないため、タイトルから `dehydration-related` も外すべきです。
- Outcome分母と高齢化率は、2020年国勢調査ではなく2023年人口推計に更新するのが望ましいです。[統計局2023年人口推計](https://www.stat.go.jp/data/jinsui/2023np/index.html)
- 医療供給は2023年一般病床数を主指標、一般診療所数を感度分析とします。[2023年医療施設調査](https://www.mhlw.go.jp/toukei/saikin/hw/iryosd/23/)
- WBGTは公式の日最高値を用います。≥28日数を主指標、≥31、≥33、累積超過量を探索的指標としました。[環境省WBGTサイト](https://www.wbgt.env.go.jp/wbgt_data.php/alert.php)
- 2023年夏は「当時、1898年以降で最も高温」と記述します。現在は2025年が最高なので、単に「観測史上最高」と現在形で書かない方が正確です。[気象庁](https://www.jma.go.jp/jma/press/2309/01b/tenko230608.html)
- Zenodoは既存版を上書きせず、新バージョンを作成します。公開は解析監査後かつ著者の最終承認後です。[Zenodoの版管理](https://help.zenodo.org/docs/deposit/manage-versions/)

作成したファイルはこちらです。

- [Major Revision全体方針・解析仕様・延長申請文](/C:/Users/user/Documents/Codex/2026-08-01/are-heat-health-systems-socially-blind/outputs/major_revision_strategy_ja.md)
- [Sonnet指示書01：データ取得・再解析](/C:/Users/user/Documents/Codex/2026-08-01/are-heat-health-systems-socially-blind/outputs/SONNET_WORK_ORDER_01_data_and_reanalysis.md)
- [Sonnet指示書02：Zenodo新バージョン作成](/C:/Users/user/Documents/Codex/2026-08-01/are-heat-health-systems-socially-blind/outputs/SONNET_WORK_ORDER_02_zenodo_new_version.md)

推奨タイトルは以下です。

> Prefecture-Level Prevalence of Older Adults Living Alone and Large-Volume Infusion Therapy Use in Japan: A Hypothesis-Generating Ecological Study

なお、この環境にはSonnetを直接呼び出すCLIまたはプラグインが現在接続されていないため、指示書の自動投入・実行とZenodo操作はまだ行っていません。Sonnet環境への接続後は、まず指示書01を実行し、こちらで数値と出典を監査してから、原稿・回答書・Zenodoへ進む順序が安全です。最初の実務は、Submission IDを含めた9月4日までの延長申請です。

4:02

ちなみに延長申請は必要ないと考えますが、どう思いますか？

4:08

現時点で直ちに延長申請する必要はない、という判断でもよいと思います。締切表現も “We recommend submitting … by 14 Aug” で、絶対期限というより推奨期限です。

ただし、8月14日まで約13日しかなく、成否は再解析が早期に完了するかで決まります。次の内部期限を置くのが現実的です。

- 8月3日：必要データの取得可否を確定
- 8月5日：年齢・医療供給調整モデルまで完了
- 8月7日：WBGT、非線形性、都市影響を含む全解析を固定
- 8月10日：本文・表図・回答書の初稿完成
- 8月12日：数値照合、共著者確認、Zenodo更新
- 8月14日：投稿

8月5日時点でModel 3まで完成していなければ、その時点で延長を申請すれば十分です。特に以下のどれかが発生した場合は延長へ切り替えます。

- 公式WBGTデータの地点対応・欠測処理に時間がかかる
- 既存解析コードまたは元データを再現できない
- 年齢・供給調整後の結果が大きく変わり、論文構成の再設計が必要
- 共著者確認に数日以上必要
- Zenodoの新バージョン準備が締切直前になる

したがって私の推奨は、「今は申請しない。ただし8月5日を延長判断のハードゲートにする」です。解析が順調なら14日提出は可能ですが、旧解析を守るために急いで不十分な調整を提出することだけは避けるべきです。


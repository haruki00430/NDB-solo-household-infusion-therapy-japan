# Prefecture-Level Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan
**An Ecological Study**

**都道府県単位の高齢者単独世帯率と大量輸液療法利用の関連：日本の生態学的研究**
（人口高齢化構造・医療供給・夏季熱曝露で調整すると関連は減弱・消失）

---

## Overview / 概要

### English

This repository contains analysis code for a nationwide ecological study examining whether **prefecture-level older-adult solo household rate** — a community-level marker of social isolation — is associated with **large-volume infusion therapy utilization** (NDB procedure code G004, ≥500 mL) across Japan's 47 prefectures, and whether this association persists after accounting for population age structure, healthcare supply, and summer heat exposure.

**Key finding**: Older-adult solo household rate was associated with infusion therapy utilization in the unadjusted analysis (β = 656.2; 95% CI, 326.9–985.6; *p* < 0.001). Adding prefectural ageing rate attenuated the estimate by 53.3% (β = 306.1; 95% CI, −71.3–683.5; *p* = 0.112), and the association was no longer statistically significant. Further adjustment for healthcare supply and official WBGT reduced the estimate toward zero (β = −9.4; 95% CI, −493.9–475.1; *p* = 0.970). These findings do not support an independent ecological association between living-alone indicators and infusion therapy utilization once population age structure is taken into account.

**Study design**: Ecological study | N = 47 prefectures | Fiscal Year 2023

**Manuscript**: Saito H, Ohira T. Prefecture-Level Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan: An Ecological Study. *International Journal of Biometeorology* (Major Revision under review, 2026).

### 日本語

本リポジトリは、都道府県単位（N = 47）の全国生態学研究の解析コードを公開するものです。**高齢者単独世帯率**（社会的孤立の地域指標）が**大量輸液療法利用**（NDB 手技コード G004、500 mL 以上）と関連するか、また人口高齢化構造・医療供給・夏季熱曝露で調整した後も関連が残るかを検証しました。

**主要結果**: 高齢者単独世帯率は非調整解析で輸液療法実施率と関連しました（β = 656.2、95% CI: 326.9–985.6、*p* < 0.001）。都道府県高齢化率を追加すると推定値は53.3%減弱し（β = 306.1、95% CI: −71.3–683.5、*p* = 0.112）、統計的有意性は失われました。さらに医療供給・公式WBGTで調整するとゼロに近づきました（β = −9.4、95% CI: −493.9–475.1、*p* = 0.970）。人口構造を考慮すると、独居指標と輸液療法利用の間に独立した生態学的関連は支持されませんでした。

**研究デザイン**: 生態学的研究 | N = 47 都道府県 | 2023 年度（令和 5 年度）

---

## Data Sources / データソース

| Source | Variables | 説明 |
|---|---|---|
| NDB Open Data No.10 (MHLW, FY2023) | Large-volume infusion therapy rate (G004, ≥500 mL) | 輸液療法算定回数 |
| e-Stat: Population estimates, Oct 1, 2023 (Statistics Bureau) | Total population, population 65+, ageing rate | 総人口・65歳以上人口・高齢化率 |
| 2020 National Census (Statistics Bureau) | Older-adult solo household rate (primary exposure); legacy elderly solo household rate (sensitivity) | 高齢者単独世帯率（新曝露）・旧曝露（感度分析用） |
| MHLW Survey of Medical Institutions 2023 (医療施設調査) | General hospital beds, general clinics per 100,000 population | 病床数・診療所数 |
| Statistics Bureau: Social Indicators by Prefecture | Population density | 人口密度 |
| Ministry of the Environment (official WBGT observations, Jun–Sep 2023) | Daily maximum WBGT day-counts (≥28/31/33°C) | 公式WBGT実況値 |
| Japan Meteorological Agency (JMA) | 2023 summer temperature anomaly (context) | 2023年夏季気温平年差 |

> **Note / 注意**: NDB raw data are not included in this repository and are not redistributable. Aggregate open data are available from the Ministry of Health, Labour and Welfare: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html
>
> NDB 生データは本リポジトリに含まれておらず、再配布できません。集計オープンデータは厚生労働省ウェブサイトから入手可能です。

---

## Repository Structure / リポジトリ構造

```
NDB-solo-household-infusion-therapy-japan/
├── 02_Data/interim/
│   └── major_revision/                     # Analytic dataset + variable dictionary (derived, aggregate)
├── 03_Analysis/
│   ├── etl/                                # Original-submission ETL (JMA weather, 2020 Census)
│   │   └── major_revision/                 # 2023 population, Census age65, healthcare supply,
│   │                                       #   population density, official WBGT
│   ├── analysis/                           # Original-submission analysis (01–09)
│   │   └── major_revision/                 # Models O-A–O-D, diagnostics, sensitivity,
│   │                                       #   nonlinearity/multiplicity, exposure comparison
│   └── results/
│       └── major_revision/                 # Model results, diagnostics, figures, tables (CSV/PNG)
├── 04_Manuscripts/
│   ├── major_revision/
│   │   ├── final/                          # Revised manuscript (clean + tracked-changes), cover
│   │   │                                   #   letter, Online Resource 1, response-to-reviewers
│   │   └── working/                        # Manuscript-build scripts and Markdown drafts
│   └── submission_package_IJB/             # IJB submission package (title page, STROBE checklist,
│                                           #   figures, cover letter)
├── reports/major_revision/                 # Formal reports, traceability/audit CSVs, source manifest
└── config/config.yaml                      # Model specification and thresholds
```

---

## Reproduction / 再現手順

### Prerequisites / 必要環境

- Python ≥ 3.10
- An e-Stat API application ID (free registration at https://www.e-stat.go.jp/api/) set as `ESTAT_APP_ID` in a local `.env` file (see `.env.example`)

### Installation / インストール

```bash
git clone https://github.com/haruki00430/NDB-solo-household-infusion-therapy-japan.git
cd NDB-solo-household-infusion-therapy-japan
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # then fill in ESTAT_APP_ID
```

### Major Revision Data Acquisition & Analysis / Major Revision データ取得・解析

```bash
# ETL (run in order)
python 03_Analysis/etl/major_revision/01_download_pop2023_by_age.py
python 03_Analysis/etl/major_revision/02_download_census2020_age65.py
python 03_Analysis/etl/major_revision/03_download_census2020_solo65_households.py
python 03_Analysis/etl/major_revision/04_build_living_alone_exposure.py
python 03_Analysis/etl/major_revision/05_download_healthcare_supply.py
python 03_Analysis/etl/major_revision/06_download_population_density.py
python 03_Analysis/etl/major_revision/07_download_wbgt_official.py
python 03_Analysis/etl/major_revision/08_aggregate_wbgt.py
python 03_Analysis/etl/major_revision/09_build_analytic_dataset.py
python 03_Analysis/etl/major_revision/10_build_legacy_outcome.py

# Analysis (run in order)
python 03_Analysis/analysis/major_revision/01_fit_models.py
python 03_Analysis/analysis/major_revision/02_diagnostics.py
python 03_Analysis/analysis/major_revision/03_sensitivity.py
python 03_Analysis/analysis/major_revision/04_nonlinearity_multiplicity.py
python 03_Analysis/analysis/major_revision/05_comparison_outcome.py
python 03_Analysis/analysis/major_revision/05b_comparison_outcome_original_exposure.py
python 03_Analysis/analysis/major_revision/06_g004_availability_audit.py
python 03_Analysis/analysis/major_revision/07_original_exposure_models.py
python 03_Analysis/analysis/major_revision/08_original_exposure_sensitivity.py
python 03_Analysis/analysis/major_revision/09_original_exposure_nonlinearity.py
python 03_Analysis/analysis/major_revision/10_exposure_comparison.py
python 03_Analysis/analysis/major_revision/11_original_exposure_coefficient_figure.py
python 03_Analysis/analysis/major_revision/12_figure_s1_denominator_comparison.py
```

### Original-Submission Pipeline / 初回投稿時パイプライン（Model 0 の再現用）

```bash
python 03_Analysis/etl/01_jma_weather_data_download.py
python 03_Analysis/etl/02_process_jma_data.py
python 03_Analysis/etl/03_aggregate_weather_data.py
python 03_Analysis/etl/04_extract_elderly_solo_rate.py
python 03_Analysis/analysis/01_integrate_and_analyze.py
python 03_Analysis/analysis/02_population_adjusted_analysis.py
python 03_Analysis/analysis/03_ridge_regression_analysis.py
python 03_Analysis/analysis/04_stepwise_univariate_analysis.py
python 03_Analysis/analysis/05_sensitivity_analysis.py
python 03_Analysis/analysis/06_figures_english.py
python 03_Analysis/analysis/07_additional_climate_variables.py
python 03_Analysis/analysis/08_fdma_heatstroke_validation.py
python 03_Analysis/analysis/09_negative_control_outpatient.py
```

---

## Citation / 引用

If you use this code, please cite the associated manuscript and code repository:  
本コードを使用する場合は、論文とコードリポジトリの両方を引用してください：

**Manuscript**:
> Saito H, Ohira T. Prefecture-Level Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan: An Ecological Study. *International Journal of Biometeorology* (Major Revision under review, 2026).

**Code repository**:
> Saito H. Analysis code for "Prefecture-Level Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan" [Software]. Zenodo. 2026. https://doi.org/10.5281/zenodo.20740375

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20740375.svg)](https://doi.org/10.5281/zenodo.20740375)

---

## Ethics / 倫理事項

This study used publicly available aggregate data. Individual informed consent was not required, and institutional ethics review was not applicable in accordance with Japanese ethical guidelines for epidemiological research.

本研究は公表集計データを使用しており、個人の同意取得および倫理審査委員会の審査は不要です（「疫学研究に関する倫理指針」に準拠）。

---

## License / ライセンス

Analysis code is released under the [MIT License](LICENSE).  
NDB Open Data is provided by the Ministry of Health, Labour and Welfare of Japan and is not redistributable as part of this repository.

解析コードは MIT ライセンスで公開しています。NDB オープンデータは厚生労働省が提供するものであり、本リポジトリから再配布することはできません。

# Manuscript Change Traceability Audit

Every paragraph in `manuscript_main_IJB_major_revision_clean.docx` that differs from the
originally submitted manuscript (`04_Manuscripts/submission_package_IJB/Japan manuscript_main_IJB_anon.docx`)
is listed below with its specific justification. Paragraph indices are the
`python-docx` paragraph indices shared by both files (the revision script,
`build_clean_manuscript_v3.py`, is a surgical patch against the original: any
paragraph index not listed in its `REPLACEMENTS` dict or `DELETE_PARAGRAPHS`
list is untouched from the original).

Justification codes:
- **R1-n**: Reviewer 1 comment n (verbatim quotes in `response_to_reviewers_draft.md`)
- **R2-n**: Reviewer 2 comment n
- **Editor**: Editor's general comment ("ensure results accurately reported, any
  overstated conclusions are rewritten and the limitations of the work fully explained")
- **Ohira-1/2/3**: Co-author Tetsuya Ohira's three comments (title; narrative framing
  toward "explains" rather than "refutes"; 2023 heat as forward-looking rather than
  purely limiting)
- **Consequence**: a direct, unavoidable consequence of implementing one of the above
  (e.g., Reviewer 2's explicit request to add ageing rate, healthcare supply, official
  WBGT, and nonlinearity testing necessarily requires new Methods/Results content
  describing those variables and models -- this is not scope creep, it is the
  requested analysis itself)

## Title and Abstract

| Para | Change | Justification |
|---|---|---|
| 0 | Title reframed from "Are Heat-Health Systems Socially Blind?..." to "Population Age Structure Explains the Ecological Association..." | R2-6 (descriptive title matching ecological design), Editor (title no longer implies warning-system evaluation), Ohira-1 |
| 14 | Background: no longer calls the exposure "social isolation"; foreshadows age-structure confounding | R1-2 (is this really an ecological "social isolation" factor?), Consequence of R2's core request |
| 16 | Methods: describes G004 definition, 2020 Census exposure, cumulative models with ageing rate/healthcare supply/WBGT | Consequence of R2's core request (the actual analysis performed must be described) |
| 18 | Results: reports O-A/O-B/O-D estimates with 95% CI | Editor (report with CI, not significance alone), Consequence |
| 20 | Conclusions: reframed to "population age structure...explains" | Ohira-2 |
| 21 | Keywords updated (removed "social isolation", "dehydration") | Consequence of R1-2 / R2-6 terminology fixes |

## Introduction

| Para | Change | Justification |
|---|---|---|
| 24 | Minor punctuation (missing period added) and "aging"->"ageing" spelling | **No specific comment identified.** Flagged for revert; see note below. |
| 25 | Minor sentence-merging/wording tightening, no content change | **No specific comment identified.** Flagged for revert; see note below. |
| 26 | Clarifies "informal monitoring" with a concrete example; adds sentence on age-structure confounding not previously examined | R1-4 (explain what informal monitoring means), Consequence of R2's core request (sets up the age-structure question) |
| 27 | Research question reworded to state the age-structure/healthcare-supply/heat-exposure test | Consequence of R2's core request |

**Note on paragraphs 24-25**: on review, these two paragraphs contain no
content change traceable to a specific reviewer or co-author comment -- only
a missing-period fix and a spelling-consistency edit ("ageing" is used
throughout all of the new Reviewer-2-mandated content; the original's
"aging" appeared only here). These are reverted to the original wording in
this round, since the user's instruction is to keep only comment-justified
changes. This is the only case in the manuscript where this applied.

## Methods

| Para | Change | Justification |
|---|---|---|
| 31 | Adds prefecture population range, official WBGT source, JMA hot-summer citation | R1-1 (population range), Consequence of R2 (official WBGT) |
| 32 | Heading: "Infusion Therapy Utilization" -> "Large-Volume Infusion Therapy Utilization" | R2-6 (non-specific outcome naming) |
| 33 | Outcome section: G004 non-specificity, public-data audit finding, downgrades FDMA "validation" claim | R1 (other indications for G004 infusion), R2-6 (outcome naming; FDMA "Validation" overclaim) |
| 35 | Exposure: distinguishes living-alone burden measure from individual-level social isolation; adds alternative-denominator sensitivity analysis | R1-2, R2 central request (alternative exposure) |
| 37 | Climatic Covariates: replaces simplified WBGT approximation with official Ministry of the Environment observations; precise per-site aggregation method | R2 central request; R1-9 (is this the JMA/official definition?) |
| 38-39 | New section "Prefectural Ageing Rate and Healthcare Supply" | R2-1, R2-2 (central request) |
| 41-43 | Statistical Analysis: replaces univariate-only approach (justified in original by collinearity) with cumulative hierarchical models O-A-O-D, VIF reporting, HC3 robust inference | R2 central request (explicitly rejects multicollinearity as a reason to avoid adjustment) |

## Results

| Para | Change | Justification |
|---|---|---|
| 48 | Descriptive statistics updated for new/added variables (ageing rate, hospital beds, official WBGT) | Consequence of R2 central request |
| 49-50 | Section renamed/rewritten around O-A-O-D hierarchical models | Consequence of R2 central request |
| 51-52 | New section: Influence Diagnostics and Sensitivity Analyses (Cook's distance, LOO, metro exclusion) | R2-3 (urban influence) |
| 53-54 | New section: Nonlinearity (quadratic, spline) | R2-3 (nonlinearity) |
| 55-56 | New section: Alternative Exposure (denominator) Analysis | R2 central request (alternative exposure) |
| 57-58 | FDMA section renamed from "Construct Validity...Validation" to "Comparison with..."; downgrades causal/validating language | Prior Codex pre-submission review pass (overclaiming "Validation") |
| 59-60 | Comparison-outcome analysis: standardized coefficients only, sixfold claim removed | R2-5 (remove sixfold claim, use standardized comparisons) |

## Discussion and Conclusions

| Para | Change | Justification |
|---|---|---|
| 63-65 | Principal result reframed to "population age structure...explains" the association; healthcare-supply attenuation discussed | Ohira-2, Consequence of R2 central request |
| 66 | Distinguishes ecological finding from individual-level social-isolation literature | R1-2 |
| 67-68 | WBGT restrained-finding framing; social-vulnerability-indicator caution reframed to "substantially reflect population age structure" | R2 (avoid overclaiming WBGT significance after FDR), Ohira-2 |
| 69 | Strengths: removed "direct re-examination of the originally specified exposure...replacement of the original approximation" (revision-process language) | Prior Codex review pass (remove revision-meta-language from main text) |
| 70-74 | Limitations expanded to 9 numbered points (ecological design, living-alone vs. social isolation, G004 non-specificity, G004 age-table unavailability, single hot year + forward-looking generalizability, N=47 CI width, unmeasured confounding, climate averaging/Hokkaido, source-year differences, AC ownership-vs-use, hypothesis-generating) | Editor ("limitations fully explained"), individually: R1 items on G004/AC/thirst-hydration/other-indications, R2-6 (hypothesis-generating), Ohira-3 (2023 heat forward-looking). **Confirmed with user to keep as-is** per Editor's general mandate, even where a specific point (e.g., source-year differences) has no single named reviewer comment. |
| 77-79 | Conclusions reframed to "explains" per Ohira; hypothesis-generating retained | Ohira-2, R2-6 |

## References, AI declaration, Data Availability, Tables/Figures

| Para | Change | Justification |
|---|---|---|
| 105,107,108,111,120 | DOI corrections (trailing digits) | Independent CrossRef/PubMed verification audit (SONNET_WORK_ORDER_04's "verify every DOI" requirement); these are factual bibliographic corrections, not narrative changes -- reverting would reintroduce incorrect DOIs |
| 119 | Miyatake DOI correction | R1-12 (explicitly named) |
| 102,115,125,126,129 (deleted) | Berkman, Liljegren, Patel, Romitti, Weisskopf references removed | Orphaned once their citing paragraphs were rewritten as a consequence of R2's request (simplified-WBGT-formula citations, the "layered policy system" recommendation, and a health-literacy digression no longer present) |
| 88 | Data Availability: GitHub URL renamed; Zenodo concept DOI | R2-6 ("XXX" placeholder) |
| 98 | AI declaration rewritten for the revision portion | Factual accuracy requirement (the original's own AI declaration establishes the practice of disclosing tools used in each round of preparation; this is not optional embellishment) |
| 133,138 | Table footnotes updated for new variables/models | Consequence |
| 135 | Table 2 title updated for hierarchical models | Consequence |
| 141 | Figure 1 legend updated for coefficient plot (replacing stratified scatter) | Consequence of R2 (nonlinearity/median-split demoted from primary result) |
| 149 | Online Resource 1 pointer updated | Consequence |
| 136,137,142,145,146,150 (deleted) | Old Table 2 Panel A/B labels, old Figure 2 heading/caption/image, Online Resource preview image | Consequence: table/figure structure changed under R2's request; old Figure 2 (simple non-stratified scatter) became redundant once Figure 1 became the coefficient plot |

## Outcome of this audit

Two paragraphs (24, 25) had no identifiable justification and are reverted
to the original wording in this round. All other changes trace to a specific
reviewer comment, the Editor's comment, a co-author comment, or a direct,
unavoidable consequence of implementing one of those. The scale of the
Methods/Results restructuring (new sections on ageing rate, healthcare
supply, official WBGT, nonlinearity, and alternative exposure) reflects the
scope of Reviewer 2's central request, not scope creep beyond it.

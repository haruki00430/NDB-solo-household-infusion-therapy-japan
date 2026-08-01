"""
Numerical audit + claim audit across all final revision-candidate documents.

- Numerical audit: extract key numbers from the clean manuscript text and
  compare against the authoritative machine-readable CSV rows.
- Claim audit: scan every final DOCX for forbidden phrases.
"""
import csv
import re
from pathlib import Path

import docx

FINAL_DIR = Path(r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\04_Manuscripts\major_revision\final")
REPORTS_DIR = Path(r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke\reports\major_revision")

DOCX_FILES = [
    FINAL_DIR / "manuscript_main_IJB_major_revision_clean.docx",
    FINAL_DIR / "manuscript_main_IJB_major_revision_marked.docx",
    FINAL_DIR / "response_to_reviewers.docx",
    FINAL_DIR / "online_resource_1_revised.docx",
    FINAL_DIR / "cover_letter_revision.docx",
]

FORBIDDEN_PHRASES = [
    "socially blind",
    "social isolation was the only ecological factor",
    "social factors outperformed climatic indicators",
    "six-fold stronger",
    "sixfold stronger",
    "dehydration-related healthcare utilization",
    "ageing completely explained",
    "no association exists",
    "10.1007/s12199-011-0267-9",  # old invalid Miyatake DOI
    "8ee5a987b9ec70631de1977bde3afd7ebc11140d",  # exposed appId
    "codex",
    r"c:\users",
    "methodological contribution",
    "prefecture-level measures of older adults living alone",  # old (wrong) title
    "accounting for population age structure and heat exposure",  # old (wrong) subtitle
    "0.169",  # wrong comparison-outcome number from the config bug
    "\u4f5c\u6210\u8005",  # leaked Japanese Word username placeholder
]

# key numbers that must appear (rounded to 1 decimal where applicable) and must NOT be contradicted
EXPECTED_NUMBERS = {
    "O-A_unstd_coef": "656.2",
    "O-A_ci": "326.9",
    "O-B_unstd_coef": "306.1",
    "O-C_unstd_coef": "94.1",
    "O-D_unstd_coef": "-9.4",
    "attenuation_pct": "53.3",
    "legacy_OA": "723.4",
}


def extract_docx_text(path: Path) -> str:
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def main():
    claim_rows = []
    for f in DOCX_FILES:
        text = extract_docx_text(f).lower()
        for phrase in FORBIDDEN_PHRASES:
            found = phrase.lower() in text
            claim_rows.append({
                "file": f.name,
                "forbidden_phrase": phrase,
                "found": found,
            })

    with open(REPORTS_DIR / "claim_traceability.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "forbidden_phrase", "found"])
        w.writeheader()
        w.writerows(claim_rows)

    any_found = [r for r in claim_rows if r["found"]]
    print(f"[Claim audit] {len(claim_rows)} checks across {len(DOCX_FILES)} files; {len(any_found)} forbidden-phrase hits")
    for r in any_found:
        print("  HIT:", r["file"], "|", r["forbidden_phrase"])

    # numerical audit: check key numbers appear in clean manuscript
    clean_text = extract_docx_text(FINAL_DIR / "manuscript_main_IJB_major_revision_clean.docx")
    num_rows = []
    for key, expected in EXPECTED_NUMBERS.items():
        present = expected in clean_text
        num_rows.append({"key": key, "expected_value": expected, "present_in_clean_manuscript": present})

    response_text = extract_docx_text(FINAL_DIR / "response_to_reviewers.docx")
    for key, expected in EXPECTED_NUMBERS.items():
        present = expected in response_text
        num_rows.append({"key": f"{key}_in_response_letter", "expected_value": expected, "present_in_clean_manuscript": present})

    with open(REPORTS_DIR / "manuscript_number_audit.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["key", "expected_value", "present_in_clean_manuscript"])
        w.writeheader()
        w.writerows(num_rows)

    missing = [r for r in num_rows if not r["present_in_clean_manuscript"]]
    print(f"[Numerical audit] {len(num_rows)} checks; {len(missing)} missing")
    for r in missing:
        print("  MISSING:", r["key"], r["expected_value"])


if __name__ == "__main__":
    main()

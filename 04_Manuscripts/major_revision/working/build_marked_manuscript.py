"""
Build the marked-up manuscript from the clean manuscript: adds a legend note
and highlights substantively revised text in yellow. Given the scale of the
Branch-2 rewrite, nearly all body content (Title through Conclusions, AI
statement) is revised; the reference list is highlighted only where it
changed (the corrected Miyatake DOI). This avoids Word's native tracked-
changes feature, which can render unpredictably, per Work Order 04.
"""
from pathlib import Path

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Pt

PROJECT_ROOT = Path(r"C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB_XXX_heatwave_heatstroke")
CLEAN_DOCX = PROJECT_ROOT / "04_Manuscripts" / "major_revision" / "final" / "manuscript_main_IJB_major_revision_clean.docx"
OUT_DOCX = PROJECT_ROOT / "04_Manuscripts" / "major_revision" / "final" / "manuscript_main_IJB_major_revision_marked.docx"

UNCHANGED_STYLES = set()  # nothing is fully unchanged except most reference entries


def is_reference_paragraph(text: str) -> bool:
    # crude heuristic: reference entries contain a year in parentheses and end with a DOI/URL or period
    return (
        ') (' not in text
        and any(f"({y})" in text for y in range(1990, 2027))
        and ('doi.org' in text or 'http' in text or text.strip().endswith('.'))
        and len(text) > 60
    )


def main():
    document = docx.Document(CLEAN_DOCX)

    # Insert legend at the very top
    legend_after = document.paragraphs[0]  # title paragraph
    legend_para = legend_after.insert_paragraph_before()
    run = legend_para.add_run(
        "MARKED-UP VERSION — REVIEWER NOTE: Highlighted (yellow) text indicates content "
        "that was substantively revised in response to Major Revision comments (Branch 2: "
        "attenuation of the original association after adjustment for population age "
        "structure). Because nearly the entire manuscript body was rewritten, highlighting "
        "is applied at the paragraph level rather than the word level. The reference list "
        "is highlighted only where a citation was corrected (Miyatake et al., DOI). See the "
        "accompanying point-by-point response letter for the full itemized mapping of "
        "changes to reviewer comments."
    )
    run.font.size = Pt(10)
    run.italic = True

    in_references = False
    for p in document.paragraphs:
        style_name = p.style.name if p.style else ''
        text = p.text.strip()
        if style_name == 'Heading 1' and text == 'References':
            in_references = True
            continue
        if style_name == 'Title':
            for run in p.runs:
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            continue
        if style_name in ('Heading 1', 'Heading 2'):
            continue  # standard section labels unchanged; leave unhighlighted for readability
        if not text:
            continue
        if in_references:
            if 'Miyatake' in text:
                for run in p.runs:
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            continue
        # all other body content: revised
        for run in p.runs:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW

    document.save(OUT_DOCX)
    print(f"[OK] marked-up manuscript written to {OUT_DOCX}")


if __name__ == "__main__":
    main()

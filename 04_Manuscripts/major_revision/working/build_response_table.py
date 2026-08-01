"""
response_to_reviewers_draft.md を Editor / Reviewer 1 / Reviewer 2 の順番のまま、
表形式（No. | Reviewer | Comment | Response）に変換した別ファイルを生成する。
"""
import re
from pathlib import Path

SRC = Path("response_to_reviewers_draft.md")
OUT = Path("response_to_reviewers_table_draft.md")

text = SRC.read_text(encoding="utf-8")

# split top-level ## sections, keep order
parts = re.split(r"\n## ", text)
header = parts[0]
sections = parts[1:]

rows = []  # (no, reviewer, comment, response)

for sec in sections:
    lines = sec.split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:])

    if title.startswith("Response to the Editor"):
        m_comment = re.search(r'\*\*Comment:\*\*\s*"(.+?)"\s*\n', body, re.S)
        m_response = re.search(r"\*\*Response:\*\*\s*(.+?)(?:\n---|\Z)", body, re.S)
        comment = m_comment.group(1).strip() if m_comment else ""
        response = m_response.group(1).strip() if m_response else ""
        rows.append(("Editor", "Editor", comment, response))
        continue

    if title.startswith("Response to Reviewer 1") or title.startswith("Response to Reviewer 2"):
        reviewer_label = "Reviewer 1" if title.startswith("Response to Reviewer 1") else "Reviewer 2"
        # split this section's body into per-item blocks on the "### " heading marker
        blocks = re.split(r"\n### ", body)[1:]  # first chunk before first "### " is the intro; drop it
        for block in blocks:
            block_lines = block.split("\n")
            heading_line = block_lines[0]
            no_match = re.match(r"(R1-\d+|R2 Comment \d+)", heading_line)
            if not no_match:
                continue
            no = no_match.group(1)
            rest = "\n".join(block_lines[1:])
            # comment: the quoted text on the "> \"...\"" line (single line, non-DOTALL)
            comment_match = re.search(r'^>\s*"(.*)"\s*(?:\[sic\])?\s*$', rest, re.M)
            comment = comment_match.group(1).strip() if comment_match else ""
            # response: everything after "**Response:**" to the end of this block
            response_match = re.search(r"\*\*Response:\*\*\s*(.+)", rest, re.S)
            response = response_match.group(1).strip() if response_match else ""
            response = re.sub(r"\n*---\s*$", "", response).strip()
            rows.append((no, reviewer_label, comment, response))
        continue

def esc(cell: str) -> str:
    # collapse newlines and escape pipe characters for markdown table cells
    return cell.replace("\n", " ").replace("|", "\\|").strip()

lines_out = []
lines_out.append("# Response to Editor and Reviewers (Table Format)")
lines_out.append("")
lines_out.append('Manuscript: "Prefecture-Level Older-Adult Solo Household Rate and Large-Volume Infusion Therapy Utilization in Japan: An Ecological Study" (formerly "Are Heat-Health Systems Socially Blind? Social Isolation and Dehydration-Related Healthcare Utilization Across Japan")')
lines_out.append("")
lines_out.append("Submission ID: 0cd18650-d5db-481f-b00b-bbde3cda74f7")
lines_out.append("")
lines_out.append(f"This table presents the same point-by-point response as the narrative version, in the order Editor → Reviewer 1 → Reviewer 2, as a single table for ease of cross-checking ({len(rows)} items).")
lines_out.append("")
lines_out.append("| No. | Reviewer | Comment | Our Response |")
lines_out.append("|---|---|---|---|")
for no, reviewer, comment, response in rows:
    lines_out.append(f"| {esc(no)} | {esc(reviewer)} | {esc(comment)} | {esc(response)} |")

OUT.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
print(f"[OK] {OUT} written, {len(rows)} rows")

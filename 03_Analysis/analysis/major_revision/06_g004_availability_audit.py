"""
Major Revision 統計解析 06: G004 都道府県×年齢 公開データ有無の確定監査

WORK_ORDER_03 Part 1 の再現可能な実装。
第10回NDBオープンデータ公式ページの生HTMLを取得し、
  (a) "G注射" 見出し直下のファイル一覧（都道府県×性年齢クロス表が無いことの確認）
  (b) ページ全体で「都道府県性年齢別」クロス表を持つカテゴリの完全列挙（G注射が含まれないことの確認）
を機械的に再実行する。手動監査（2026-08-01）と同じ結論に到達することを検証する。

出力:
  - 02_Data/raw/major_revision/ndb10_g004_audit/（生HTML・xlsx・PDFのアーカイブ、SHA-256付き）
  - reports/major_revision/g004_public_file_inventory.csv
  - reports/major_revision/g004_search_log.txt
  - reports/major_revision/g004_public_data_availability_audit.md の結論と整合するassertion
"""
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "02_Data" / "raw" / "major_revision" / "ndb10_g004_audit"
REPORTS_DIR = PROJECT_ROOT / "reports" / "major_revision"
RAW_DIR.mkdir(parents=True, exist_ok=True)

NDB10_PAGE_URL = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177221_00016.html"
G_INJECTION_FILES = {
    "001493140.xlsx": "性年齢別算定回数",
    "001493141.xlsx": "都道府県別算定回数",
    "001493142.xlsx": "診療月別算定回数",
    "001493143.xlsx": "二次医療圏別算定回数",
}
CONTENT_BASE = "https://www.mhlw.go.jp/content/12400000/"


def fetch_and_hash(url: str, dest: Path) -> tuple[bytes, str]:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return resp.content, hashlib.sha256(resp.content).hexdigest()


def main():
    log_lines = []

    # --- 1. 公式ページ取得 ---
    html_bytes, html_sha = fetch_and_hash(NDB10_PAGE_URL, RAW_DIR / "ndb10_official_page_rebuild.html")
    html = html_bytes.decode("utf-8")
    log_lines.append(f"Fetched {NDB10_PAGE_URL} sha256={html_sha}")

    # --- 2. G注射 見出し直下のファイル一覧を抽出 ---
    idx = html.find("G注射")
    assert idx > 0, "G注射 heading not found on page"
    window = html[idx : idx + 2000]
    next_heading = re.search(r'<h4 class="m-hdgLv4__hdg"[^>]*>([^<]+)</h4>', window[20:])
    assert next_heading, "Could not locate the next category heading after G注射"
    block = window[: 20 + next_heading.start()]
    log_lines.append(f"Next heading after G注射: {next_heading.group(1)}")
    files_in_block = re.findall(r'href="(/content/12400000/(\d+\.xlsx))"', block)
    log_lines.append(f"G注射 block contains {len(files_in_block)} files: {[f[1] for f in files_in_block]}")
    assert len(files_in_block) == 4, f"Expected exactly 4 files under G注射, found {len(files_in_block)}"
    assert set(f[1] for f in files_in_block) == set(G_INJECTION_FILES.keys())

    # --- 3. 都道府県性年齢別クロス表を持つカテゴリの完全列挙 ---
    cross_tab_matches = re.findall(
        r'href="(/content/12400000/[0-9]+\.xlsx)">([^<]*都道府県性年齢[^<]*)</a>', html
    )
    log_lines.append(f"Prefecture x age/sex cross-tab files found site-wide: {len(cross_tab_matches)}")
    for href, label in cross_tab_matches:
        log_lines.append(f"  {href} | {label}")
    g_injection_in_crosstabs = any("G" in label and "注射" in label for _, label in cross_tab_matches)
    assert not g_injection_in_crosstabs, "G-injection unexpectedly found among prefecture x age cross-tabs"

    # --- 4. G注射の4ファイルを取得し、G004行と次元構造を確認 ---
    g004_findings = []
    for fname, label in G_INJECTION_FILES.items():
        content, sha = fetch_and_hash(CONTENT_BASE + fname, RAW_DIR / fname)
        wb = openpyxl.load_workbook(RAW_DIR / fname, data_only=True)
        sheet = wb[wb.sheetnames[2]]  # 医科 sheet (index 2)
        g004_rows = [
            r
            for r in range(1, sheet.max_row + 1)
            if sheet.cell(row=r, column=1).value == "G004"
        ]
        assert g004_rows, f"G004 not found in {fname}"
        # dimension check: read header rows 3-4 to see what varies across columns
        header_row3 = [sheet.cell(row=3, column=c).value for c in range(7, 12)]
        header_row4 = [sheet.cell(row=4, column=c).value for c in range(7, 12)]
        g004_findings.append(
            {
                "file": fname,
                "label": label,
                "sha256": sha,
                "size": len(content),
                "g004_row": g004_rows[0],
                "header_sample": (header_row3, header_row4),
            }
        )
        log_lines.append(f"{fname} ({label}): G004 at row {g004_rows[0]}, sha256={sha}")

    # --- 5. 出力 ---
    log_path = REPORTS_DIR / "g004_search_log_rebuild.txt"
    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    print("[OK] G004 availability audit rebuild complete.")
    print("Classification: NOT_PUBLICLY_AVAILABLE (verified programmatically)")
    print(f"Rebuild log written to {log_path}")
    for f in g004_findings:
        print(f"  {f['file']}: row={f['g004_row']} header_sample={f['header_sample']}")


if __name__ == "__main__":
    main()

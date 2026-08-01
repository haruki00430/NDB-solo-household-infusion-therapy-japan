"""IJB原稿に行番号と1.5倍行間を設定する。"""
import sys
from pathlib import Path

import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

path = Path(__file__).resolve().parent / "manuscript_main_IJB.docx"

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(str(path))

# 行番号（連続）
ln = doc.PageSetup.LineNumbering
ln.Active = True
ln.RestartMode = 0  # wdRestartContinuous

# 1.5倍行間（全段落）
for para in doc.Paragraphs:
    para.Format.LineSpacingRule = 1  # wdLineSpace1pt5

doc.Save()
doc.Close()
word.Quit()
print(f"Applied line numbers and 1.5 spacing: {path.name}")

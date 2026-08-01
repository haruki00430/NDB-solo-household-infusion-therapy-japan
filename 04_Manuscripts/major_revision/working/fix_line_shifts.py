"""
Results §3 の1文削除（-2行シフト、旧239行目以降）に伴う response_to_reviewers_draft.md の
行番号引用を一括修正する。旧239行目より前の引用は変更しない。
"""
from pathlib import Path

PATH = Path("response_to_reviewers_draft.md")
text = PATH.read_text(encoding="utf-8")

# (old_substring, new_substring, expected_count)
replacements = [
    ("lines 325–362", "lines 323–360", 1),
    ("lines 296–303", "lines 294–301", 1),
    ("lines 337–339", "lines 335–337", 2),
    ("line 357–359", "line 355–357", 1),
    ("lines 357–359", "lines 355–357", 2),
    ("lines 240–242", "lines 238–240", 2),
    ("lines 363–366", "lines 361–364", 1),
    ("lines 313–319", "lines 311–317", 1),
    ("lines 283–288", "lines 281–286", 1),
    ("lines 368–386", "lines 366–384", 2),
    ("lines 330–334", "lines 328–332", 2),
    ("lines 341–345", "lines 339–343", 1),
    ("line 493", "line 491", 1),
    ("lines 243–246", "lines 241–244", 1),
    ("lines 227–238", "lines 227–236", 1),  # non-uniform: paragraph itself shortened
    ("lines 304–312", "lines 302–310", 1),
    ("lines 263–268", "lines 261–266", 1),
    ("lines 351–356", "lines 349–354", 1),
    ("lines 396–404", "lines 394–402", 1),
]

for old, new, expected in replacements:
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"MISMATCH: {old!r} found {count} times, expected {expected}")
    text = text.replace(old, new)

PATH.write_text(text, encoding="utf-8")
print("[OK] all replacements applied and verified")

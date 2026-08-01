"""
manuscript_main_IJB.docx の参考文献を Vancouver 番号式から IJB 著者-年式へ変換する。

Usage:
    python convert_references_author_year.py
"""
from __future__ import annotations

import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from docx import Document

sys.stdout.reconfigure(encoding="utf-8")

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript_main_IJB.docx"
BACKUP_SUFFIX = "_pre_author_year_backup"

# Vancouver 番号順（References 節の 1–30）
VANCOUVER_REFS: list[str] = [
    "Fire and Disaster Management Agency. Daily number of patients with heatstroke transported by ambulance in Japan. Tokyo: Fire and Disaster Management Agency (FDMA), Ministry of Internal Affairs and Communications; 2023. Available from: https://www.fdma.go.jp/disaster/heatstroke/post4.html",
    "Ministry of Health, Labour and Welfare. Vital Statistics: Annual status of deaths due to heatstroke in Japan. Tokyo: MHLW; 2024. Available from: https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/tokusyu/necchusho24/index.html",
    "Intergovernmental Panel on Climate Change (IPCC). Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report. Cambridge: Cambridge University Press; 2021. Available from: https://www.ipcc.ch/report/ar6/wg1/",
    "Günsche S, Borg MA, Anikeeva O, Varghese BM, Li Y, Bhandari D, et al. Mortality, morbidity and healthcare costs of short-term high temperatures and heatwaves exposure in older populations: a global systematic review and meta-analysis. Environ Int. 2026;208:110129. doi:10.1016/j.envint.2026.110129",
    "Parsons K. Heat stress standard ISO 7243 and its global application. Ind Health. 2006;44(3):368-379. doi:10.2486/indhealth.44.368",
    "Blazejczyk K, Epstein Y, Jendritzky G, Staiger H, Tinz B. Comparison of UTCI to selected thermal indices. Int J Biometeorol. 2012;56(3):515-535.",
    "Ministry of the Environment, Government of Japan. Heat Illness Prevention Information: Heat Stress Index (WBGT) and Heat Stroke Alerts. Available from: https://www.wbgt.env.go.jp/en/",
    "Hondula DM, Balling RC, Andrade R, Krayenhoff ES, Middel A, Urban A, Georgescu M, Sailor DJ. Biometeorology for cities. Int J Biometeorol. 2017;61(Suppl 1):59-69.",
    "Harlan SL, Declet-Barreto JH, Stefanov WL, Petitti DB. Neighborhood effects on heat deaths: social and environmental predictors of vulnerability in Maricopa County, Arizona. Environ Health Perspect. 2013;121(2):197-204.",
    "Kenney WL, Munce TA. Invited review: aging and human temperature regulation. J Appl Physiol (1985). 2003;95(6):2598-2603.",
    "Bouchama A, Knochel JP. Heat stroke. N Engl J Med. 2002;346(25):1978-1988.",
    "Vandentorren S, Bretin P, Zeghnoun A, et al. August 2003 heat wave in France: risk factors for death of elderly people living at home. Eur J Public Health. 2006;16(6):583-591.",
    "Canouï-Poitrine F, Cadot E, Spira A, Groupe Régional Canicule. Excess deaths during the August 2003 heat wave in Paris, France. Rev Epidemiol Sante Publique. 2006;54(2):127-135. doi:10.1016/S0398-7620(06)76706-2",
    "Ministry of Internal Affairs and Communications. National Survey of Family Income and Expenditure 2014. Tokyo: MIC; 2015.",
    "Farbotko C, Waitt G. Residential air-conditioning and climate change: voices of the vulnerable. Health Promot J Austr. 2011;22(4):13-15.",
    "Semenza JC, Rubin CH, Falter KH, et al. Heat-related deaths during the July 1995 heat wave in Chicago. N Engl J Med. 1996;335(2):84-90.",
    "Naughton MP, Henderson A, Mirabelli MC, et al. Heat-related mortality during a 1999 heat wave in Chicago. Am J Prev Med. 2002;22(4):221-227.",
    "Oberai M, Xu Z, Bach A, Forbes C, Jackman E, O'Connor F, et al. A digital heat early warning system for older adults. NPJ Digit Med. 2025;8(1):114. doi:10.1038/s41746-025-01505-5",
    "Zhang C, Mohamad E, Azlan AA, Wu A, Ma Y, Qi Y. Social media and eHealth literacy among older adults: systematic literature review. J Med Internet Res. 2025;27:e66058. doi:10.2196/66058",
    "Ng CF, Ueda K, Takeuchi A, et al. Sociogeographic variation in the effects of heat and cold on daily mortality in Japan. J Epidemiol. 2014;24(1):15-24. doi:10.2188/jea.JE20130051",
    "Miyatake N, Sakano N, Murakami S. The relation between ambulance transports stratified by heat stroke and air temperature in all 47 prefectures of Japan in August, 2009: Ecological study. Environ Health Prev Med. 2012;17(1):77-80.",
    "Patel T, Mullen SP, Santee WR. Comparison of methods for estimating wet-bulb globe temperature index from standard meteorological measurements. Mil Med. 2013;178(8):926-933. doi:10.7205/MILMED-D-13-00117",
    "Liljegren JC, Carhart RA, Lawday P, Tschopp S, Sharp R. Modeling the wet bulb globe temperature using standard meteorological measurements. J Occup Environ Hyg. 2008;5(10):645-655.",
    "Bach AJE, Cunningham SJK, Morris NR, Xu Z, Rutherford S, Binnewies S, et al. Experimental research in environmentally induced hyperthermic older persons: a systematic quantitative literature review mapping the available evidence. Temperature (Austin). 2024;11(1):4-26. doi:10.1080/23328940.2023.2242062",
    "Blatteis CM. Age-dependent changes in temperature regulation - a mini review. Gerontology. 2012;58(4):289-295.",
    "Romitti Y, Sue Wing I, Spangler KR, Wellenius GA. The effects of residential air conditioning and social vulnerability on heat-related hospitalizations in California. Environ Int. 2025;202:109659. doi:10.1016/j.envint.2025.109659",
    "Weisskopf MG, Anderson HA, Foldy S, et al. Heat wave morbidity and mortality, Milwaukee, Wis, 1999 vs 1995: an improved response? Am J Public Health. 2002;92(5):830-833.",
    "Conti S, Meli P, Minelli G, et al. Epidemiologic study of mortality during the Summer 2003 heat wave in Italy. Environ Res. 2005;98(3):390-399.",
    "Berkman ND, Sheridan SL, Donahue KE, Halpern DJ, Crotty K. Low health literacy and health outcomes: an updated systematic review. Ann Intern Med. 2011;155(2):97-107.",
    "Oka K, Honda Y, Hui Phung VL, Hijioka Y. Potential effect of heat adaptation on association between number of heatstroke patients transported by ambulance and wet bulb globe temperature in Japan. Environ Res. 2023;216(Pt 3):114666. doi:10.1016/j.envres.2022.114666",
]

# 本文引用ラベル（括弧内、IJB 例: Author et al. 2020）
INTEXT_LABELS: list[str] = [
    "Fire and Disaster Management Agency 2023",
    "MHLW 2024",
    "IPCC 2021",
    "Günsche et al. 2026",
    "Parsons 2006",
    "Blazejczyk et al. 2012",
    "Ministry of the Environment Japan n.d.",
    "Hondula et al. 2017",
    "Harlan et al. 2013",
    "Kenney and Munce 2003",
    "Bouchama and Knochel 2002",
    "Vandentorren et al. 2006",
    "Canouï-Poitrine et al. 2006",
    "MIC 2015",
    "Farbotko and Waitt 2011",
    "Semenza et al. 1996",
    "Naughton et al. 2002",
    "Oberai et al. 2025",
    "Zhang et al. 2025",
    "Ng et al. 2014",
    "Miyatake et al. 2012",
    "Patel et al. 2013",
    "Liljegren et al. 2008",
    "Bach et al. 2024",
    "Blatteis 2012",
    "Romitti et al. 2025",
    "Weisskopf et al. 2002",
    "Conti et al. 2005",
    "Berkman et al. 2011",
    "Oka et al. 2023",
]

# Springer author-year 参考文献リスト（アルファベット順）
SPRINGER_REFS: list[str] = [
    "Bach AJE, Cunningham SJK, Morris NR, Xu Z, Rutherford S, Binnewies S, et al (2024) Experimental research in environmentally induced hyperthermic older persons: a systematic quantitative literature review mapping the available evidence. Temperature (Austin) 11:4-26. https://doi.org/10.1080/23328940.2023.2242062",
    "Berkman ND, Sheridan SL, Donahue KE, Halpern DJ, Crotty K (2011) Low health literacy and health outcomes: an updated systematic review. Ann Intern Med 155:97-107. https://doi.org/10.7326/0003-4819-155-2-201107190-00005",
    "Blatteis CM (2012) Age-dependent changes in temperature regulation - a mini review. Gerontology 58:289-295. https://doi.org/10.1159/000333148",
    "Blazejczyk K, Epstein Y, Jendritzky G, Staiger H, Tinz B (2012) Comparison of UTCI to selected thermal indices. Int J Biometeorol 56:515-535. https://doi.org/10.1007/s00484-011-0453-2",
    "Bouchama A, Knochel JP (2002) Heat stroke. N Engl J Med 346:1978-1988. https://doi.org/10.1056/NEJMra011086",
    "Canouï-Poitrine F, Cadot E, Spira A, Groupe Régional Canicule (2006) Excess deaths during the August 2003 heat wave in Paris, France. Rev Epidemiol Sante Publique 54:127-135. https://doi.org/10.1016/S0398-7620(06)76706-2",
    "Conti S, Meli P, Minelli G, et al (2005) Epidemiologic study of mortality during the Summer 2003 heat wave in Italy. Environ Res 98:390-399. https://doi.org/10.1016/j.envres.2004.12.009",
    "Farbotko C, Waitt G (2011) Residential air-conditioning and climate change: voices of the vulnerable. Health Promot J Austr 22:13-15. https://doi.org/10.1071/HE10013",
    "Fire and Disaster Management Agency (2023) Daily number of patients with heatstroke transported by ambulance in Japan. Tokyo: FDMA. https://www.fdma.go.jp/disaster/heatstroke/post4.html",
    "Günsche S, Borg MA, Anikeeva O, Varghese BM, Li Y, Bhandari D, et al (2026) Mortality, morbidity and healthcare costs of short-term high temperatures and heatwaves exposure in older populations: a global systematic review and meta-analysis. Environ Int 208:110129. https://doi.org/10.1016/j.envint.2026.110129",
    "Harlan SL, Declet-Barreto JH, Stefanov WL, Petitti DB (2013) Neighborhood effects on heat deaths: social and environmental predictors of vulnerability in Maricopa County, Arizona. Environ Health Perspect 121:197-204. https://doi.org/10.1289/ehp.1103532",
    "Hondula DM, Balling RC, Andrade R, Krayenhoff ES, Middel A, Urban A, Georgescu M, Sailor DJ (2017) Biometeorology for cities. Int J Biometeorol 61(Suppl 1):59-69. https://doi.org/10.1007/s00484-017-1412-3",
    "Intergovernmental Panel on Climate Change (IPCC) (2021) Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press, Cambridge. https://www.ipcc.ch/report/ar6/wg1/",
    "Kenney WL, Munce TA (2003) Invited review: aging and human temperature regulation. J Appl Physiol 95:2598-2603. https://doi.org/10.1152/japplphysiol.00202.2003",
    "Liljegren JC, Carhart RA, Lawday P, Tschopp S, Sharp R (2008) Modeling the wet bulb globe temperature using standard meteorological measurements. J Occup Environ Hyg 5:645-655. https://doi.org/10.1080/15459620802310770",
    "Ministry of Health, Labour and Welfare (MHLW) (2024) Vital Statistics: Annual status of deaths due to heatstroke in Japan. Tokyo: MHLW. https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/tokusyu/necchusho24/index.html",
    "Ministry of Internal Affairs and Communications (MIC) (2015) National Survey of Family Income and Expenditure 2014. Tokyo: MIC.",
    "Ministry of the Environment, Government of Japan (n.d.) Heat Illness Prevention Information: Heat Stress Index (WBGT) and Heat Stroke Alerts. https://www.wbgt.env.go.jp/en/",
    "Miyatake N, Sakano N, Murakami S (2012) The relation between ambulance transports stratified by heat stroke and air temperature in all 47 prefectures of Japan in August, 2009: Ecological study. Environ Health Prev Med 17:77-80. https://doi.org/10.1007/s12199-011-0267-9",
    "Naughton MP, Henderson A, Mirabelli MC, et al (2002) Heat-related mortality during a 1999 heat wave in Chicago. Am J Prev Med 22:221-227. https://doi.org/10.1016/S0749-3797(02)00414-X",
    "Ng CF, Ueda K, Takeuchi A, et al (2014) Sociogeographic variation in the effects of heat and cold on daily mortality in Japan. J Epidemiol 24:15-24. https://doi.org/10.2188/jea.JE20130051",
    "Oberai M, Xu Z, Bach A, Forbes C, Jackman E, O'Connor F, et al (2025) A digital heat early warning system for older adults. NPJ Digit Med 8:114. https://doi.org/10.1038/s41746-025-01505-5",
    "Oka K, Honda Y, Hui Phung VL, Hijioka Y (2023) Potential effect of heat adaptation on association between number of heatstroke patients transported by ambulance and wet bulb globe temperature in Japan. Environ Res 216:114666. https://doi.org/10.1016/j.envres.2022.114666",
    "Parsons K (2006) Heat stress standard ISO 7243 and its global application. Ind Health 44:368-379. https://doi.org/10.2486/indhealth.44.368",
    "Patel T, Mullen SP, Santee WR (2013) Comparison of methods for estimating wet-bulb globe temperature index from standard meteorological measurements. Mil Med 178:926-933. https://doi.org/10.7205/MILMED-D-13-00117",
    "Romitti Y, Sue Wing I, Spangler KR, Wellenius GA (2025) The effects of residential air conditioning and social vulnerability on heat-related hospitalizations in California. Environ Int 202:109659. https://doi.org/10.1016/j.envint.2025.109659",
    "Semenza JC, Rubin CH, Falter KH, et al (1996) Heat-related deaths during the July 1995 heat wave in Chicago. N Engl J Med 335:84-90. https://doi.org/10.1056/NEJM199607113350203",
    "Vandentorren S, Bretin P, Zeghnoun A, et al (2006) August 2003 heat wave in France: risk factors for death of elderly people living at home. Eur J Public Health 16:583-591. https://doi.org/10.1093/eurpub/ckl063",
    "Weisskopf MG, Anderson HA, Foldy S, et al (2002) Heat wave morbidity and mortality, Milwaukee, Wis, 1999 vs 1995: an improved response? Am J Public Health 92:830-833. https://doi.org/10.2105/AJPH.92.5.830",
    "Zhang C, Mohamad E, Azlan AA, Wu A, Ma Y, Qi Y (2025) Social media and eHealth literacy among older adults: systematic literature review. J Med Internet Res 27:e66058. https://doi.org/10.2196/66058",
]

# JECH Vancouver 形式: ".1), 2)" / ",5), 6)" / ".7)" / "12)–19)"
# 小数 (3.13)、CI (1,070.21)、千位区切り (1,580) と衝突しないよう、
# 数字直後の "." / "," は引用開始とみなさない。
CITE_ONE = r"(?:[1-9]|[1-2]\d|30)\)"
CITE_CLUSTER_RE = re.compile(
    r"(?<!\d)(?:\.|,)\s*("
    + CITE_ONE
    + r"\s*[\u2013-]\s*"
    + CITE_ONE
    + r"|"
    + CITE_ONE
    + r"(?:\s*,\s*"
    + CITE_ONE
    + r")*)"
)
CITE_NUM_EXTRACT = re.compile(r"30|[1-2]\d|[1-9]")
CITE_SINGLE_RE = re.compile(r"(?<=[a-zA-Z])" + CITE_ONE + r"(?!\d)")


def _labels_from_cluster(cluster: str) -> str:
    range_match = re.match(
        r"((?:[1-9]|[1-2]\d|30))\)\s*[\u2013-]\s*((?:[1-9]|[1-2]\d|30))\)",
        cluster.strip(),
    )
    if range_match:
        start, end = int(range_match.group(1)), int(range_match.group(2))
        nums = list(range(start, end + 1))
    else:
        nums = [int(n) for n in CITE_NUM_EXTRACT.findall(cluster) if 1 <= int(n) <= 30]
    if not nums:
        return cluster
    labels = [INTEXT_LABELS[n - 1] for n in nums]
    return "(" + "; ".join(labels) + ")"


def convert_citations(text: str) -> str:
    """番号式引用クラスタを著者-年式に置換する。"""

    def _replace_cluster(match: re.Match[str]) -> str:
        return " " + _labels_from_cluster(match.group(1))

    text = CITE_CLUSTER_RE.sub(_replace_cluster, text)

    def _replace_single(match: re.Match[str]) -> str:
        num = int(match.group(0)[:-1])
        return "(" + INTEXT_LABELS[num - 1] + ")"

    return CITE_SINGLE_RE.sub(_replace_single, text)


def replace_in_paragraph(paragraph) -> None:
    """段落内の全 run を結合して置換し、単一 run に戻す。"""
    if not paragraph.text:
        return
    new_text = convert_citations(paragraph.text)
    if new_text == paragraph.text:
        return
    for run in paragraph.runs:
        run.text = ""
    if paragraph.runs:
        paragraph.runs[0].text = new_text
    else:
        paragraph.add_run(new_text)


def replace_in_cell(cell) -> None:
    for paragraph in cell.paragraphs:
        replace_in_paragraph(paragraph)


def rebuild_references_section(doc: Document) -> None:
    """References 見出し以降を再構築（図表セクションは保持）。"""
    ref_idx = None
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == "References":
            ref_idx = i
            break
    if ref_idx is None:
        raise ValueError("References 見出しが見つかりません")

    tail_markers = ("Tables and Figures", "Table 1.", "Figure Legends")
    tail_idx = len(doc.paragraphs)
    for i in range(ref_idx + 1, len(doc.paragraphs)):
        t = doc.paragraphs[i].text.strip()
        if any(t.startswith(m) for m in tail_markers):
            tail_idx = i
            break

    # 旧 Vancouver リストを削除（後ろから）
    for i in range(tail_idx - 1, ref_idx, -1):
        p = doc.paragraphs[i]._element
        p.getparent().remove(p)

    # References 見出しと Tables and Figures の間へ挿入（A→Z 順）
    insert_anchor = doc.paragraphs[ref_idx + 1]
    for ref_line in SPRINGER_REFS:
        insert_anchor.insert_paragraph_before(ref_line)


def remove_author_block(doc: Document) -> None:
    """メイン原稿先頭の著者名・日付行を削除（タイトルページに集約）。"""
    remove_texts = {
        "Haruki Saito",
        "Tetsuya Ohira",
        "2026-06-19",
    }
    for para in list(doc.paragraphs[:8]):
        if para.text.strip() in remove_texts:
            para._element.getparent().remove(para._element)


def trim_keywords(doc: Document) -> None:
    """Keywords を IJB 規定の 4–6 個に調整。"""
    for para in doc.paragraphs:
        if para.text.startswith("Keywords:"):
            para.text = (
                "Keywords: heat-health surveillance; social isolation; "
                "elderly solo household; dehydration; ecological study; Japan"
            )
            return


def rename_methods_heading(doc: Document) -> None:
    """IJB 推奨の Materials and methods 見出しへ変更（Introduction 以降）。"""
    seen_intro = False
    for para in doc.paragraphs:
        t = para.text.strip()
        if t == "Introduction":
            seen_intro = True
        if seen_intro and t == "Methods":
            para.text = "Materials and methods"
            return


def verify_numeric_integrity(doc: Document) -> list[str]:
    """変換後に数値破損が残っていないか検証する。"""
    issues: list[str] = []
    patterns = [
        ("version 3 (", "Python version corrupted"),
        ("statsmodels (version 0 (", "statsmodels version corrupted"),
        ("1,070 (Miyatake", "Table 2 CI corrupted"),
        ("886 (Liljegren", "Table 2 CI corrupted"),
        ("106 (Kenney", "Table 2 CI corrupted"),
    ]
    texts: list[str] = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.append(cell.text)
    blob = "\n".join(texts)
    for needle, msg in patterns:
        if needle in blob:
            issues.append(msg)
    if "723.37 (376.52, 1,070.21)" not in blob:
        issues.append("Table 2 primary CI missing or altered")
    if "Python (version 3.14)" not in blob:
        issues.append("Python version 3.14 missing")
    if "statsmodels (version 0.14)" not in blob:
        issues.append("statsmodels version 0.14 missing")
    return issues


def process_document(path: Path) -> None:
    backup = path.with_name(path.stem + BACKUP_SUFFIX + path.suffix)
    if not backup.exists():
        backup.write_bytes(path.read_bytes())
        print(f"Backup: {backup.name}")

    doc = Document(path)
    remove_author_block(doc)
    trim_keywords(doc)
    rename_methods_heading(doc)

    in_refs = False
    for para in doc.paragraphs:
        if para.text.strip() == "References":
            in_refs = True
            continue
        if in_refs:
            if para.text.strip().startswith("Tables and Figures"):
                break
            continue
        replace_in_paragraph(para)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_in_cell(cell)

    rebuild_references_section(doc)

    issues = verify_numeric_integrity(doc)
    if issues:
        raise RuntimeError(
            "Numeric integrity check failed after conversion: " + "; ".join(issues)
        )

    doc.save(path)
    print(f"Updated: {path.name}")
    print("Numeric integrity check: OK")


if __name__ == "__main__":
    process_document(MANUSCRIPT)

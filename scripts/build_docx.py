"""Build deliverable/Zou_CTGT_Work_Sample_RulesTrack.docx from the files in work/.

Layout: a plain two-page memo. Letter portrait, 0.65 in margins, Calibri throughout
(Carlito renders it metric-identically in LibreOffice). Cases are numbered paragraphs
rather than a table; the only table is the small results table (8.5 pt, light gray header).
"""
import datetime
import json
import os
import re
import sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

FONT = "Calibri"
TP = 9          # case-table point size
SP = 8.5        # results strip, legend and table notes
BODY = 9.5     # body prose
INK = RGBColor(0x1F, 0x2A, 0x37)        # charcoal for headings
MUTED = RGBColor(0x55, 0x5F, 0x6B)
RULE = "A6ADB4"
HEAD_FILL = "EDEFF2"

cases = json.load(open("work/final_cases.json"))
strip = json.load(open("work/results_strip.json"))
meta = json.load(open("work/deliverable_meta.json"))

NBSP = "\u00a0"
FOR_PDF = "--for-pdf" in sys.argv
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "deliverable/Zou_CTGT_Work_Sample_RulesTrack.docx"


def typeset(text):
    """Typography only; the words are exactly the tested text.

    Quoted notice language becomes curly double quotes, apostrophes become curly,
    and citations get non-breaking spaces so '12 CFR' never ends a line.
    """
    text = re.sub(r"(?<![\w])'([^']+?)'(?![\w])", "\u201c\\1\u201d", text)
    text = re.sub(r"\u201d([,.])", "\\1\u201d", text)          # American style: comma and period inside
    text = text.replace("'", "\u2019")
    text = re.sub(r"12 CFR (1002)", "12" + NBSP + "CFR" + NBSP + r"\1", text)
    text = re.sub(r"\b([Cc]omments?) (\d)", r"\1" + NBSP + r"\2", text)
    if FOR_PDF:
        # Line-break guards for the LibreOffice PDF render only. The delivered .docx omits them,
        # so Word's Find still matches citations such as 1002.9(b)(2) and 9(b)(2)-7.
        text = re.sub(r"\)-(\d)", ")\u2011\\1", text)
        text = text.replace(")(", ")\u2060(")
    return text

doc = Document()
cp = doc.core_properties
cp.author = "Jason Zou"
cp.last_modified_by = "Jason Zou"
cp.title = "Work Sample, Rules Track: Regulation B, 12 CFR 1002.9(b)(2)"
cp.subject = "CTGT internship work sample"
cp.created = cp.modified = datetime.datetime(2026, 10, 31, 12, 0, 0)
cp.comments = ""
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(0.65))
sec.header_distance = Inches(0.35)
sec.footer_distance = Inches(0.35)

normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = Pt(10)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.line_spacing = 1.0


def run(p, text, size=None, bold=False, italic=False, color=None):
    # U+2011 marks a hyphen that must not break a line; Word's form is <w:noBreakHyphen/>.
    first, *rest = text.split("\u2011")
    r = p.add_run(first)
    for piece in rest:
        r._r.append(OxmlElement("w:noBreakHyphen"))
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = piece
        r._r.append(t)
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if size:
        r.font.size = Pt(size)
    r.bold, r.italic = bold, italic
    if color is not None:
        r.font.color.rgb = color
    return r


def hyperlink(p, url, text, size):
    """Insert a real hyperlink run (python-docx has no high-level API for this)."""
    rid = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), rid)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    for tag, val in (("w:rFonts", None), ("w:color", "1F4E79"), ("w:sz", str(int(size * 2))), ("w:u", "single")):
        el = OxmlElement(tag)
        if tag == "w:rFonts":
            el.set(qn("w:ascii"), FONT)
            el.set(qn("w:hAnsi"), FONT)
        else:
            el.set(qn("w:val"), val)
        rpr.append(el)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)
    h.append(r)
    p._p.append(h)


def bottom_rule(p, color=RULE, sz=6):
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "1"), ("w:color", color)):
        b.set(qn(k), v)
    bdr.append(b)
    ppr.append(bdr)


def heading(text, before=7, after=2.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = True
    run(p, text, size=11, bold=True, color=INK)
    return p


def cell_borders(cell, top=None, bottom=None):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge, spec in (("top", top), ("bottom", bottom), ("left", None), ("right", None)):
        el = OxmlElement(f"w:{edge}")
        if spec:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(spec[0]))
            el.set(qn("w:color"), spec[1])
        else:
            el.set(qn("w:val"), "nil")
        b.append(el)
    tcpr.append(b)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), fill)
    tcpr.append(s)


def cell_margins(table, top=32, bottom=32, left=70, right=70):
    tblpr = table._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{k}")
        el.set(qn("w:w"), str(v))
        el.set(qn("w:type"), "dxa")
        m.append(el)
    tblpr.append(m)


def no_split(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    trpr.append(el)


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    trpr.append(el)


def set_widths(table, widths):
    """Fixed layout with explicit grid columns; LibreOffice and Word both honor tblGrid."""
    table.autofit = False
    tblpr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblpr.append(layout)
    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        tblpr.append(tblw)
    tblw.set(qn("w:w"), str(int(sum(widths) * 1440)))
    tblw.set(qn("w:type"), "dxa")
    for gc, w in zip(table._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for row in table.rows:
        for c, w in zip(row.cells, widths):
            c.width = Inches(w)


def para_in(cell, first=True):
    return cell.paragraphs[0] if first else cell.add_paragraph()


# ---------------------------------------------------------------- header
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
run(p, "Jason Zou", size=13, bold=True, color=INK)
run(p, " | Work Sample, Rules Track | Regulation B, 12" + NBSP + "CFR" + NBSP + "1002.9(b)(2) | ", size=10, color=MUTED)
hyperlink(p, "mailto:jzou1@uchicago.edu", "jzou1@uchicago.edu", 10)
bottom_rule(p, color="1F2A37", sz=6)

# Footer: page number only, centered.
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run()
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag:
        f = OxmlElement("w:fldChar")
        f.set(qn("w:fldCharType"), tag)
        r._r.append(f)
    else:
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = txt
        r._r.append(it)
r.font.size = Pt(8.5)
r.font.color.rgb = MUTED


def body_para(text, before=0, after=0, indent=None, size=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    if text:
        run(p, typeset(text), size=size or BODY)
    return p


# ---------------------------------------------------------------- method
heading("Method", before=4)
body_para(meta["method_note"])

# ---------------------------------------------------------------- cases
# Each case reads top to bottom: a title line with the answer on the right, the facts,
# then the reasoning in a marked-off block with the citations in small gray type.
heading("Ten cases, clearest first")
LABEL = {"complies": ("Complies", RGBColor(0x2F, 0x6B, 0x3A)),
         "violates": ("Violates", RGBColor(0x9B, 0x2C, 0x2C)),
         "depends": ("Depends", RGBColor(0x8A, 0x5A, 0x00))}
TEXT_W = sec.page_width - sec.left_margin - sec.right_margin


def left_bar(p, color="C9CED6", sz=12, space=6):
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:left")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", str(space)), ("w:color", color)):
        b.set(qn(k), v)
    bdr.append(b)
    ppr.append(bdr)


for i, cs in enumerate(cases, 1):
    word, colour = LABEL[cs["gold_label"]]
    t = doc.add_paragraph()
    t.paragraph_format.space_before = Pt(0 if i == 1 else 6)
    t.paragraph_format.space_after = Pt(1)
    t.paragraph_format.keep_with_next = True
    t.paragraph_format.tab_stops.add_tab_stop(TEXT_W, alignment=2)   # right-aligned tab for the label
    run(t, f"{i}. {cs['title']}", size=10.5, bold=True, color=INK)
    run(t, "\t" + word, size=10, bold=True, color=colour)

    f = body_para(cs["facts"])
    f.paragraph_format.keep_with_next = True

    for k, sentence in enumerate(cs["why"]):
        a = doc.add_paragraph()
        a.paragraph_format.left_indent = Inches(0.16)
        a.paragraph_format.space_before = Pt(3 if k == 0 else 0)
        if k < len(cs["why"]) - 1:
            a.paragraph_format.keep_with_next = True
        left_bar(a)
        run(a, typeset(sentence), size=BODY)
        if k == len(cs["why"]) - 1:
            run(a, "  " + typeset(cs["cites"]), size=SP, color=MUTED)

# ---------------------------------------------------------------- results table
heading("How the models did")
cols = len(cases) + 2
t2 = doc.add_table(rows=1, cols=cols)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
cell_margins(t2, top=20, bottom=20, left=50, right=50)
w2 = [2.25] + [0.42] * len(cases) + [0.75]
heads = ["Case"] + [str(i) for i in range(1, len(cases) + 1)] + ["Missed"]
for c, txt in zip(t2.rows[0].cells, heads):
    shade(c, HEAD_FILL)
    cell_borders(c, top=(4, RULE), bottom=(4, RULE))
    p = c.paragraphs[0]
    if txt != "Case":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, txt, size=SP, bold=True, color=INK)
first_count = True
for r_ in strip["rows"]:
    row = t2.add_row()
    cells = row.cells
    top = None
    if r_.get("count_row") and first_count:
        top, first_count = (4, RULE), False
    run(cells[0].paragraphs[0], r_["label"], size=SP)
    for j, v in enumerate(r_["cells"], 1):
        p = cells[j].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        missed = v not in ("", "0")
        run(p, v or NBSP, size=SP, bold=missed, color=INK if missed else MUTED)   # NBSP keeps row heights even
    p = cells[-1].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, r_["total"], size=SP)
    for c in cells:
        cell_borders(c, top=top, bottom=(2, "D5D9DE"))
set_widths(t2, w2)
p = body_para(None, before=3)
run(p, typeset(strip["legend"]), size=SP, color=MUTED)
body_para(meta["harness"], before=4)

# ---------------------------------------------------------------- what I noticed
heading("What I noticed")
for k, para in enumerate(meta["noticed"]):
    body_para(para, before=0 if k == 0 else 3)

# ---------------------------------------------------------------- limits and files
heading("Limits")
body_para(meta["limits"])

doc.save(OUT)
print("saved")

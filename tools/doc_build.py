# -*- coding: utf-8 -*-
"""Genera la propuesta editorial de la landing (DOCX) para Coach Gloria Celis.

Diseño: portada a sangre, sistema de tokens del brief, tablas con encabezado carbón,
callouts con borde acento, especímenes tipográficos con las fuentes reales y
verificación visual iterativa vía LibreOffice Kit.
"""
import os
import copy

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK, WD_TAB_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
WORK = os.path.join(ROOT, "tools", "doc_work")
IMG = os.path.join(WORK, "img")
os.makedirs(DOCS, exist_ok=True)

OUT_DOCX = os.path.join(DOCS, "Propuesta_Landing_Coach_Basketball.docx")

# ------------------------------------------------------------------ paleta
INK = "0A0B0D"
CARBON = "111317"
STEEL = "1A1D22"
CREAM = "F4F1E9"
GOLD = "E9B44C"
GOLD_D = "8A6416"      # oro legible sobre blanco
FLAME = "FF4D1F"
LINE_C = "E4DFD3"
WARM = "F8F6F1"
TEXT = "1A1D22"
SOFT = "4E545C"        # secundario sobre claro
MUTED = "8E959E"       # secundario solo sobre oscuro
WHITE = "FFFFFF"

# ------------------------------------------------------------------ fuentes
BD = "Barlow Condensed"            # 700 bold
BDE = "Barlow Condensed ExtraBold" # 800
BDS = "Barlow Condensed SemiBold"  # 600
BDM = "Barlow Condensed Medium"    # 500
IN = "Inter"                       # 400 / bold
INS = "Inter SemiBold"             # 600
INM = "Inter Medium"               # 500

PAGE_W, PAGE_H = 8.5, 11.0
MARGIN = 0.95
CONTENT_W = PAGE_W - 2 * MARGIN     # 6.6 in

# ------------------------------------------------------------------ utilidades XML
RPR_AFTER_CAPS = ("w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow", "w:emboss",
                  "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish", "w:webHidden", "w:color",
                  "w:spacing", "w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight",
                  "w:u", "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl",
                  "w:cs", "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath")
RPR_AFTER_SPACING = ("w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight", "w:u",
                     "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs",
                     "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath")
RPR_AFTER_SHD = ("w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang",
                 "w:eastAsianLayout", "w:specVanish", "w:oMath")
PPR_AFTER_PBDR = ("w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
                  "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi",
                  "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing",
                  "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection",
                  "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
                  "w:rPr", "w:sectPr", "w:pPrChange")
PPR_AFTER_SHD = ("w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct",
                 "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd",
                 "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
                 "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
                 "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr",
                 "w:sectPr", "w:pPrChange")
TCPR_AFTER_SHD = ("w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def insert_before(parent, child, successors):
    tags = {qn(t) for t in successors}
    for c in parent:
        if c.tag in tags:
            c.addprevious(child)
            return
    parent.append(child)


# ------------------------------------------------------------------ runs y párrafos
def add_run(p, text, font=IN, size=10, bold=False, color=TEXT, caps=False, spacing=0.0,
            italic=False, shade=None):
    r = p.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor.from_string(color)
    rPr = r._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), font)
    if caps:
        insert_before(rPr, el("w:caps", val="1"), RPR_AFTER_CAPS)
    if spacing:
        insert_before(rPr, el("w:spacing", val=str(int(round(spacing * 20)))), RPR_AFTER_SPACING)
    if shade:
        insert_before(rPr, el("w:shd", val="clear", color="auto", fill=shade), RPR_AFTER_SHD)
    return r


def p_shade(p, fill):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:shd")):
        pPr.remove(old)
    insert_before(pPr, el("w:shd", val="clear", color="auto", fill=fill), PPR_AFTER_SHD)


def p_borders(p, **sides):
    """sides: bottom=('single', 4, LINE_C), top=..., left=..., right=..."""
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:pBdr")):
        pPr.remove(old)
    bdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        if side in sides:
            val, sz, color = sides[side]
            bdr.append(el("w:" + side, val=val, sz=sz, space="2", color=color))
    insert_before(pPr, bdr, PPR_AFTER_PBDR)


def para(container, text="", font=IN, size=10, bold=False, color=TEXT, caps=False, spacing=0.0,
         italic=False, before=0, after=0, line=None, align=None, keep=False, keep_lines=False,
         left=0.0, right=0.0, first_line=0.0, shade=None, page_break_before=False):
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing = Pt(line)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    if align is not None:
        p.alignment = align
    if keep:
        pf.keep_with_next = True
    if keep_lines:
        pf.keep_together = True
    if left:
        pf.left_indent = Inches(left)
    if right:
        pf.right_indent = Inches(right)
    if first_line:
        pf.first_line_indent = Inches(first_line)
    if page_break_before:
        pf.page_break_before = True
    if shade:
        p_shade(p, shade)
    if text:
        add_run(p, text, font=font, size=size, bold=bold, color=color, caps=caps,
                spacing=spacing, italic=italic)
    return p


def rich(p, chunks):
    """chunks: list of (text, dict(kw))"""
    for text, kw in chunks:
        add_run(p, text, **kw)
    return p


def spacer(container, pts):
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(pts)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    return p


def bar(container, color, width_in, thickness_pt, left=0.0, before=0, after=0, avail=CONTENT_W,
        pbb=False):
    """Franja de color real (párrafo sombreado)."""
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = Pt(thickness_pt)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.left_indent = Inches(left)
    pf.right_indent = Inches(avail - left - width_in)
    if pbb:
        pf.page_break_before = True
    pf.keep_with_next = True
    p_shade(p, color)
    return p


def page_break(doc):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    r = p.add_run()
    r.font.size = Pt(1)
    r.add_break(WD_BREAK.PAGE)
    return p


def field(p, instr, font=BD, size=8.5, color=SOFT, bold=False, spacing=0.0):
    fld = el("w:fldSimple", instr=instr)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rf = el("w:rFonts", ascii=font, hAnsi=font, cs=font, eastAsia=font)
    rPr.append(rf)
    if bold:
        rPr.append(el("w:b", val="1"))
    rPr.append(el("w:color", val=color))
    if spacing:
        rPr.append(el("w:spacing", val=str(int(round(spacing * 20)))))
    rPr.append(el("w:sz", val=str(int(size * 2))))
    rPr.append(el("w:szCs", val=str(int(size * 2))))
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    p._p.append(fld)


# ------------------------------------------------------------------ tablas
def _border_el(tag, val="single", sz=4, color=LINE_C):
    return el("w:" + tag, val=val, sz=sz, space="0", color=color)


def table_borders(tbl, color=LINE_C, sz=4, inside=True, val="single"):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right"):
        b.append(_border_el(side, val=val, sz=sz, color=color))
    for side in ("insideH", "insideV"):
        b.append(_border_el(side, val=val if inside else "nil", sz=sz, color=color))
    # posición: después de tblW/jc, antes de shd/tblLayout
    insert_before(tblPr, b, ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook"))


def table_layout(tbl, widths, border_color=LINE_C, borders=True, border_sz=4, inside=True,
                 pad=(60, 60, 110, 110)):
    tblPr = tbl._tbl.tblPr
    for child in list(tblPr):
        tblPr.remove(child)
    tw = el("w:tblW", w=int(round(sum(widths) * 1440)), type="dxa")
    tblPr.append(tw)
    jc = el("w:jc", val="left")
    tblPr.append(jc)
    if borders:
        b = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right"):
            b.append(_border_el(side, val="single", sz=border_sz, color=border_color))
        for side in ("insideH", "insideV"):
            b.append(_border_el(side, val="single" if inside else "nil", sz=border_sz,
                                color=border_color))
        tblPr.append(b)
    else:
        b = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            b.append(_border_el(side, val="nil", sz=0, color="auto"))
        tblPr.append(b)
    mar = OxmlElement("w:tblCellMar")
    for side, v in zip(("top", "bottom", "left", "right"), pad):
        mar.append(el("w:" + side, w=v, type="dxa"))
    tblPr.append(mar)
    tblPr.append(el("w:tblLayout", type="fixed"))
    tblPr.append(el("w:tblLook", val="0000", firstRow="0", lastRow="0", firstColumn="0",
                    lastColumn="0", noHBand="1", noVBand="1"))
    grid = tbl._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        tbl._tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths:
        grid.append(el("w:gridCol", w=int(round(w * 1440))))
    tbl._tbl.insert(list(tbl._tbl).index(tblPr) + 1, grid)
    for row in tbl.rows:
        for i, c in enumerate(row.cells):
            c.width = Inches(widths[i])


def row_height(row, h_in, exact=False):
    trPr = row._tr.get_or_add_trPr()
    for old in trPr.findall(qn("w:trHeight")):
        trPr.remove(old)
    insert_before(trPr, el("w:trHeight", val=int(round(h_in * 1440)),
                           hRule="exact" if exact else "atLeast"),
                  ("w:tblHeader", "w:tblCellSpacing", "w:jc", "w:hidden"))


def row_repeat(row):
    trPr = row._tr.get_or_add_trPr()
    if not trPr.findall(qn("w:tblHeader")):
        trPr.append(el("w:tblHeader", val="1"))


def row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if not trPr.findall(qn("w:cantSplit")):
        insert_before(trPr, el("w:cantSplit"), ("w:trHeight", "w:tblHeader"))


def cell_fmt(c, fill=None, valign=None, borders=None, pad=None):
    tcPr = c._tc.get_or_add_tcPr()
    if borders:
        for old in tcPr.findall(qn("w:tcBorders")):
            tcPr.remove(old)
        b = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            if side in borders:
                val, sz, color = borders[side]
                b.append(el("w:" + side, val=val, sz=sz, space="0", color=color))
            else:
                b.append(el("w:" + side, val="nil", sz=0, space="0", color="auto"))
        insert_before(tcPr, b, ("w:shd",) + TCPR_AFTER_SHD)
    if pad:
        for old in tcPr.findall(qn("w:tcMar")):
            tcPr.remove(old)
        mar = OxmlElement("w:tcMar")
        for side, v in zip(("top", "left", "bottom", "right"), pad):
            mar.append(el("w:" + side, w=v, type="dxa"))
        insert_before(tcPr, mar, TCPR_AFTER_SHD)
    if fill:
        for old in tcPr.findall(qn("w:shd")):
            tcPr.remove(old)
        insert_before(tcPr, el("w:shd", val="clear", color="auto", fill=fill), TCPR_AFTER_SHD)
    if valign is not None:
        c.vertical_alignment = valign


def cell_text(c, text, font=IN, size=8.5, bold=False, color=TEXT, caps=False, spacing=0.0,
              line=11.0, align=None, before=0, after=0, italic=False, first=True):
    p = c.paragraphs[0] if first else c.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = Pt(line)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    if align is not None:
        p.alignment = align
    for i, ln in enumerate(str(text).split("\n")):
        if i > 0:
            p = c.add_paragraph()
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(after)
            pf.line_spacing = Pt(line)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            if align is not None:
                p.alignment = align
        add_run(p, ln, font=font, size=size, bold=bold, color=color, caps=caps,
                spacing=spacing, italic=italic)
    return p


def new_table(doc, widths, **kw):
    t = doc.add_table(rows=1, cols=len(widths))
    table_layout(t, widths, **kw)
    return t


def data_table(doc, widths, headers, rows, header_fill=CARBON, header_color=CREAM,
               body_size=8.3, body_line=10.6, header_size=7.4, header_line=9.0,
               zebra=True, first_col_dark=False, row_pad=(64, 64, 104, 104),
               split_rows=False):
    t = new_table(doc, widths, pad=row_pad)
    hdr = t.rows[0]
    row_cant_split(hdr)
    row_repeat(hdr)
    for i, h in enumerate(headers):
        c = hdr.cells[i]
        cell_fmt(c, fill=header_fill, valign=WD_ALIGN_VERTICAL.CENTER)
        cell_text(c, h, font=BDS, size=header_size, color=header_color, caps=True,
                  spacing=0.7, line=header_line)
    for ri, r in enumerate(rows):
        row = t.add_row()
        if not split_rows:
            row_cant_split(row)
        for ci, val in enumerate(r):
            c = row.cells[ci]
            fill = WARM if (zebra and ri % 2 == 1) else None
            cell_fmt(c, fill=fill, valign=WD_ALIGN_VERTICAL.TOP)
            cell_text(c, val, font=IN, size=body_size, color=TEXT, line=body_line)
    return t


def keep_table_together(t):
    """Evita que una tabla corta se parta entre páginas."""
    rows = t.rows
    for ri, row in enumerate(rows):
        row_cant_split(row)
        if ri < len(rows) - 1:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.keep_with_next = True


# ------------------------------------------------------------------ componentes
def framed_image(doc, path, width_in, caption=None, frame=GOLD, pad=0.05, before=0, after=0):
    t = new_table(doc, [width_in], borders=True, border_color=frame, border_sz=4,
                  pad=(int(pad * 1440), int(pad * 1440), int(pad * 1440), int(pad * 1440)))
    c = t.rows[0].cells[0]
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run()
    run.add_picture(path, width=Inches(width_in - 2 * pad - 0.02))
    if caption:
        para(doc, caption, size=7.2, color=SOFT, line=9.2, before=5, after=10)
    return t


def callout(doc, body, kicker=None, accent=FLAME, dark=False, width=CONTENT_W,
            body_font=IN, body_size=10.2, body_line=14.6, body_color=None, title=None):
    t = new_table(doc, [width], borders=False, pad=(210, 210, 260, 260))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=CARBON if dark else "FAF7F0",
             borders={"left": ("single", 24, accent)})
    first = True
    if kicker:
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = Pt(9)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, kicker.upper(), font=INS, size=7.2,
                color=accent if dark else accent, caps=True, spacing=1.8)
        first = False
    if title:
        p = c.paragraphs[0] if first else c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(21)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, title, font=BDS, size=17, color=CREAM if dark else TEXT, caps=False)
        first = False
    p = c.paragraphs[0] if first else c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(body_line)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    for i, ln in enumerate(body.split("\n")):
        if i:
            p = c.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(body_line)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, ln, font=body_font, size=body_size,
                color=body_color or (CREAM if dark else TEXT))
    return t


def quote_panel(doc, quote, author, compact=False):
    if compact:
        pad = (150, 160, 230, 230)
        qsize, qline, qafter = 16.0, 17.5, 6
        asize, aline = 6.8, 8.6
    else:
        pad = (260, 270, 320, 320)
        qsize, qline, qafter = 19.5, 23, 12
        asize, aline = 7.6, 11
    t = new_table(doc, [CONTENT_W], borders=False, pad=pad)
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=INK)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(qafter)
    p.paragraph_format.line_spacing = Pt(qline)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, quote, font=BDS, size=qsize, color=CREAM)
    p2 = c.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = Pt(aline)
    p2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p2, author.upper(), font=INS, size=asize, color=GOLD, caps=True, spacing=1.6)
    row_cant_split(t.rows[0])
    return t


def sec_head(doc, num, label, title_lines, deck=None, first=False, new_page=True):
    if first:
        spacer(doc, 4)
        bar(doc, FLAME, 0.42, 3.2, before=0, after=10)
    elif new_page:
        bar(doc, FLAME, 0.42, 3.2, before=0, after=10, pbb=True)
    else:
        spacer(doc, 26)
        bar(doc, FLAME, 0.42, 3.2, before=0, after=10)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(9)
    p.paragraph_format.line_spacing = Pt(11)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.keep_with_next = True
    add_run(p, num, font=BDE, size=11, color=FLAME, spacing=0.6)
    add_run(p, "  /  ", font=INS, size=7, color=MUTED)
    add_run(p, label.upper(), font=INS, size=7.6, color=GOLD_D, caps=True, spacing=2.2)
    for tl in title_lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(27.5)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p.paragraph_format.keep_with_next = True
        add_run(p, tl, font=BD, size=30, color=INK, bold=True, spacing=-0.25)
    if deck:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(15.2)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p.paragraph_format.right_indent = Inches(0.9)
        add_run(p, deck, font=IN, size=10.4, color=SOFT)
    spacer(doc, 18)


def h3(doc, text, before=16, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = Pt(15)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.keep_with_next = True
    add_run(p, text.upper(), font=BDS, size=10.6, color=INK, caps=True, spacing=1.1)
    return p


def lead(doc, text, size=11.0, color=TEXT, line=16.4, before=0, after=9, right=0.4):
    return para(doc, text, size=size, color=color, line=line, before=before, after=after,
                right=right)


def body(doc, text, size=9.6, line=14.4, before=0, after=7, color=TEXT, right=0.2):
    return para(doc, text, size=size, color=color, line=line, before=before, after=after,
                right=right)


def stats_row(doc, items, dark=True):
    n = len(items)
    gap = 0.13
    w = (CONTENT_W - gap * (n - 1)) / n
    widths = []
    for i in range(n):
        widths.append(w)
        if i < n - 1:
            widths.append(gap)
    t = new_table(doc, widths, borders=False, pad=(160, 160, 150, 150))
    row = t.rows[0]
    for i, (num, label) in enumerate(items):
        c = row.cells[i * 2]
        cell_fmt(c, fill=CARBON if dark else WARM)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = Pt(34)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, num, font=BDE, size=31, color=FLAME)
        p2 = c.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = Pt(10)
        p2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p2, label.upper(), font=INS, size=6.9, color=MUTED if dark else SOFT,
                caps=True, spacing=1.1)
    row_cant_split(row)
    return t


# ================================================================== PORTADA
def build_cover(doc, sec):
    sec.page_width = Inches(PAGE_W)
    sec.page_height = Inches(PAGE_H)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin",
              "header_distance", "footer_distance"):
        setattr(sec, m, Inches(0))

    t = new_table(doc, [PAGE_W], borders=False, pad=(0, 0, 0, 0))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=INK)
    row_height(t.rows[0], PAGE_H - 0.44, exact=True)

    # bloque superior
    spacer(c, 30)
    logo = os.path.join(IMG, "doc_logo.png")
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(30)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.add_run().add_picture(logo, height=Inches(0.42))

    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(16)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "GLORIA CELIS", font=BD, size=12.5, color=CREAM, bold=True, spacing=1.4)

    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(10)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "BASKETBALL COACH · ALTO RENDIMIENTO", font=INS, size=6.4, color=MUTED,
            caps=True, spacing=2.6)

    # aire
    spacer(c, 118)

    # eyebrow
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(11)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "PROPUESTA DE DISEÑO · LANDING PAGE · V1.0", font=INS, size=7.4,
            color=GOLD, caps=True, spacing=2.4)

    spacer(c, 16)
    # concepto
    concept = [("EL JUEGO SE GANA", CREAM), ("ANTES DEL", None), ("SALTO INICIAL.", CREAM)]
    for i, (line, col) in enumerate(concept):
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Inches(0.95)
        p.paragraph_format.line_spacing = Pt(52)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        if i == 1:
            add_run(p, "ANTES", font=BDE, size=57, color=FLAME, spacing=-0.9)
            add_run(p, " DEL", font=BDE, size=57, color=CREAM, spacing=-0.9)
        else:
            add_run(p, line, font=BDE, size=57, color=col, spacing=-0.9)

    spacer(c, 14)
    bar(c, FLAME, 2.35, 6.0, left=0.95, before=0, after=0, avail=PAGE_W)
    spacer(c, 18)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.right_indent = Inches(1.3)
    p.paragraph_format.line_spacing = Pt(14)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Concepto creativo, sistema de diseño y dirección de arte para una marca "
               "de alto rendimiento.", font=IN, size=9.6, color=MUTED)

    # segunda línea de aire: tono de marca
    spacer(c, 150)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(10)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "AUTORIDAD  ·  DISCIPLINA  ·  ESTRATEGIA  ·  RESULTADOS", font=INS, size=6.6,
            color=GOLD, caps=True, spacing=3.0)

    # empuje al pie
    spacer(c, 40)
    # pie de portada
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.right_indent = Inches(0.95)
    p_borders(p, bottom=("single", 4, "2E323A"))

    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(15)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "PROPUESTA DE LANDING PAGE", font=BD, size=9.6, color=CREAM, bold=True,
            spacing=1.6)
    add_run(p, "      COACH GLORIA CELIS  ·  BOGOTÁ, COLOMBIA", font=IN, size=8.2,
            color=MUTED)

    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Inches(0.95)
    p.paragraph_format.line_spacing = Pt(13)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "OCTUBRE 2026", font=INS, size=9.2, color=GOLD, caps=True, spacing=2.6)
    add_run(p, "      DOCUMENTO CONFIDENCIAL", font=INS, size=6.6, color=MUTED, caps=True,
            spacing=2.2)

    # franja inferior a sangre (párrafo que cierra la sección de portada)
    band = doc.add_paragraph()
    pf = band.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(0.44 * 72)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.left_indent = Inches(0)
    pf.right_indent = Inches(0)
    p_shade(band, INK)
    add_run(band, " ", font=IN, size=1, color=INK)
    return band


# ================================================================== PÁGINAS
def build_carta(doc):
    sec_head(doc, "00", "Documento", ["UNA LANDING QUE SE JUEGA", "COMO UN PARTIDO."],
             "Propuesta de diseño, dirección de arte y arquitectura de conversión para la "
             "landing page de la Coach Gloria Celis. Bogotá · Octubre 2026.", first=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = Pt(15.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Gloria: ", font=INS, size=10.2, color=INK)
    add_run(p, "tu trabajo ya tiene lo que casi nadie puede fabricar con marketing — nueve "
               "títulos, más de 340 jugadoras formadas y una metodología que se puede medir. "
               "Lo que falta es un lugar digital que esté a la altura de esa evidencia: una "
               "landing que no explique quién eres, sino que demuestre cómo piensas el juego.",
            font=IN, size=10.2, color=TEXT)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    p.paragraph_format.line_spacing = Pt(15.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Este documento recoge el concepto creativo, el sistema de diseño, la dirección "
               "de arte, el copy final y la estrategia de conversión de esa landing. Está "
               "escrito para decidir: cada sección termina en una recomendación concreta, no "
               "en una idea suelta.", font=IN, size=10.2, color=TEXT)

    h3(doc, "Resumen ejecutivo", before=6, after=8)
    items = [
        ("EL RETO", "El alto rendimiento se percibe en la cancha, no en una web genérica de "
                    "«entrenamientos». La marca necesita un activo digital con autoridad "
                    "visual y una única acción clara: agendar el diagnóstico."),
        ("LA RESPUESTA", "Un sistema editorial construido sobre la idea «el juego se gana "
                         "antes del salto inicial»: oscuridad de vestuario, luz de cancha, "
                         "tipografía condensada y datos verificables como argumento."),
        ("EL RESULTADO", "Un sitio de una sola página, rápido y accesible, con un CTA "
                         "primario repetido con disciplina y una medición que permita "
                         "optimizar semana a semana."),
    ]
    t = new_table(doc, [0.42, 6.18], borders=False, pad=(0, 130, 0, 0))
    for i, (k, v) in enumerate(items):
        row = t.rows[0] if i == 0 else t.add_row()
        row_cant_split(row)
        c = row.cells[0]
        cell_fmt(c, fill=None)
        numpy = c.paragraphs[0]
        numpy.paragraph_format.space_before = Pt(2)
        numpy.paragraph_format.space_after = Pt(0)
        numpy.paragraph_format.line_spacing = Pt(15)
        numpy.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(numpy, f"0{i + 1}", font=BDE, size=11, color=FLAME)
        c2 = row.cells[1]
        cell_fmt(c2, fill=None)
        p = c2.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(10)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, k, font=INS, size=7.1, color=INK, caps=True, spacing=1.6)
        p2 = c2.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(9)
        p2.paragraph_format.line_spacing = Pt(13.2)
        p2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p2, v, font=IN, size=8.8, color=SOFT)

    spacer(doc, 8)
    h3(doc, "Ficha del proyecto", before=10, after=8)
    data_table(
        doc, [1.45, 5.15],
        ["Campo", "Detalle"],
        [
            ["Cliente", "Coach Gloria Celis — alto rendimiento femenino"],
            ["Proyecto", "Landing page de captación (one-page)"],
            ["Alcance", "Concepto, sistema de diseño, dirección de arte, copy, CRO y "
                        "especificación técnica"],
            ["Formato", "Documento Word / PDF · 8,5 × 11 in · 9 secciones"],
            ["Idioma", "Español (Colombia)"],
            ["Fecha", "Octubre 2026"],
            ["Versión", "1.0 — propuesta sujeta a ajuste con el cliente"],
        ],
        body_size=8.2, body_line=10.2,
    )


def build_index(doc, pages):
    sec_head(doc, "00", "Índice", ["NUEVE MOVIMIENTOS.", "UN SOLO PARTIDO."],
             "El documento sigue el orden en que se toma una decisión: primero el concepto, "
             "después el sistema, luego el copy y, al final, el plan para ejecutarlo.")

    rows = [
        ("01", "Concepto creativo y posicionamiento", pages["01"]),
        ("02", "Arquitectura de la landing, sección por sección", pages["02"]),
        ("03", "Sistema de diseño: color, tipografía, rejilla y componentes", pages["03"]),
        ("04", "Dirección de arte: fotografía, piezas 3D y gráficos tácticos", pages["04"]),
        ("05", "Copywriting persuasivo y variantes A/B", pages["05"]),
        ("06", "CRO: reglas de conversión, formulario y medición", pages["06"]),
        ("07", "Especificación técnica, accesibilidad y performance", pages["07"]),
        ("08", "Cronograma de implementación y entregables", pages["08"]),
        ("09", "Próximos pasos y firma", pages["09"]),
    ]
    t = new_table(doc, [0.62, 5.32, 0.66], borders=False, pad=(0, 0, 0, 0))
    for i, (num, title, page) in enumerate(rows):
        row = t.rows[0] if i == 0 else t.add_row()
        row_cant_split(row)
        row_height(row, 0.42)
        c = row.cells[0]
        cell_fmt(c, fill=None, borders={"bottom": ("single", 4, LINE_C)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, num, font=BDE, size=10.5, color=FLAME)
        c = row.cells[1]
        cell_fmt(c, fill=None, borders={"bottom": ("single", 4, LINE_C)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, title, font=BD, size=13.5, color=INK, bold=True, spacing=0.1)
        c = row.cells[2]
        cell_fmt(c, fill=None, borders={"bottom": ("single", 4, LINE_C)},
                 valign=WD_ALIGN_VERTICAL.CENTER)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, page, font=BD, size=10.5, color=SOFT, bold=True)

    spacer(doc, 20)
    callout(doc, "Los textos en mayúsculas y entre comillas de la sección 02 son copy final: "
                 "van al prototipo tal como están escritos. Las tablas de especificación son "
                 "instrucciones de producción, no sugerencias. Todo lo que no está en este "
                 "documento se decide en la fase 1, con el cliente en la mesa.",
            kicker="Cómo leer este documento", accent=FLAME, dark=False)

    spacer(doc, 10)
    callout(doc, "El palmarés, las cifras, los testimonios y los datos de contacto de Gloria "
                 "Celis son un caso de demostración construido para este proyecto. El sistema "
                 "está diseñado para que el cliente real sustituya una sola variable —nombre, "
                 "biografía y respaldo— sin tocar la estructura, el concepto ni la dirección "
                 "de arte. Las fotografías incluidas son material de archivo de demostración.",
            kicker="Nota sobre el contenido", accent=GOLD, dark=True)


def build_concepto(doc):
    sec_head(doc, "01", "Concepto creativo", ["EL JUEGO SE GANA", "ANTES DEL SALTO INICIAL."],
             "La landing no vende entrenamientos. Vende criterio: la capacidad de leer el "
             "juego antes de que ocurra. Todo el sistema —paleta, tipografía, fotografía y "
             "copy— se deriva de esta idea.")

    t = new_table(doc, [CONTENT_W], borders=False, pad=(280, 290, 380, 380))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=INK)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = Pt(11)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "BIG IDEA", font=INS, size=7.2, color=GOLD, caps=True, spacing=2.4)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = Pt(35)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "EL JUEGO SE GANA\nANTES DEL SALTO INICIAL.", font=BDE, size=36, color=CREAM,
            spacing=-0.7)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(12.6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.right_indent = Inches(1.6)
    add_run(p, "La frase ordena el negocio y el diseño: el resultado se construye en el "
               "trabajo invisible —videoanálisis, rutina, plan individual— mucho antes del "
               "primer salto.", font=IN, size=9.0, color=MUTED)

    h3(doc, "Por qué este concepto", before=18, after=6)
    body(doc, "El básquetbol se decide en fracciones de segundo, pero se gana en las horas que "
              "nadie filma: la sesión de video, la conversación previa al partido, el plan "
              "individual que se revisa cada cuatro semanas. Ese es el territorio real de una "
              "entrenadora de alto rendimiento, y es exactamente lo que la landing debe poner "
              "en pantalla.")
    body(doc, "Por eso la dirección de arte no ilustra el deporte: lo trata como un documento. "
              "Fotografía real con contraste alto, tipografía condensada que grita sin adornos "
              "y datos fechados —títulos, clubes, años— en lugar de adjetivos. La página no "
              "dice «soy la mejor»: muestra el historial que lo respalda.")

    h3(doc, "Posicionamiento", before=16, after=6)
    lead(doc, "Para familias, clubes y federaciones que invierten en formación deportiva "
              "seria, Gloria Celis es la entrenadora que convierte talento en criterio y "
              "criterio en resultados medibles. No compite con motivadores ni con contenido "
              "viral: compite con la falta de método.", size=10.4, line=15.6, after=14)

    quote_panel(doc, "«La cancha no premia al que más corre, sino al que mejor decide.»",
                "Coach Gloria Celis · filosofía de marca", compact=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = Pt(9)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.keep_with_next = True
    add_run(p, "POSICIONAMIENTO · QUÉ COMPRA EL CLIENTE Y QUÉ NO", font=INS, size=7.2,
            color=GOLD_D, caps=True, spacing=2.0)

    t = new_table(doc, [3.25, 3.25], pad=(80, 80, 130, 130), border_color=LINE_C)
    hdr = t.rows[0]
    for i, (txt, fill, col) in enumerate((("LO QUE COMPRA EL CLIENTE", CARBON, CREAM),
                                          ("LO QUE NO ESTAMOS VENDIENDO", WARM, INK))):
        c = hdr.cells[i]
        cell_fmt(c, fill=fill)
        cell_text(c, txt, font=BDS, size=7.2, color=col, caps=True, spacing=0.9, line=9)
    pairs = [
        ("Criterio y lectura de juego", "Motivación vacía y frases de vestuario"),
        ("Resultados medibles: PER, becas, convocatorias", "Promesas sin dato"),
        ("Un método con nombre propio: Sistema 360", "«Entrenamientos personalizados» genéricos"),
        ("Autoridad verificable y fechada", "Trofeos sin contexto"),
    ]
    for a, b in pairs:
        row = t.add_row()
        row_cant_split(row)
        cell_fmt(row.cells[0], fill=None)
        cell_text(row.cells[0], a, font=INS, size=8.4, color=INK, line=10.6)
        cell_fmt(row.cells[1], fill=WARM)
        cell_text(row.cells[1], b, font=IN, size=8.4, color=SOFT, line=10.8, italic=True)
    keep_table_together(t)


def build_concepto2(doc):
    """Segunda página del concepto: promesa, tono y decisiones."""
    spacer(doc, 2)
    h3(doc, "Promesa central", before=10, after=8)
    callout(doc, "Formar jugadoras que leen el juego, lideran bajo presión y compiten con "
                 "criterio.", kicker="La promesa que sostiene todo el copy", accent=FLAME,
            dark=True, body_font=BDS, body_size=20, body_line=24)

    h3(doc, "Tono y lenguaje", before=22, after=7)
    body(doc, "La voz de la marca es la de una entrenadora que explica, no la de una marca que "
              "vende. Frases cortas, verbos en primera persona, cero adornos. El entusiasmo se "
              "demuestra con precisión, no con signos de exclamación.")

    chips = ["AUTORIDAD", "DISCIPLINA", "ESTRATEGIA", "RESULTADOS", "LIDERAZGO", "EXCELENCIA"]
    t = new_table(doc, [1.06] * 6, borders=False, pad=(30, 30, 40, 40))
    for i, ch in enumerate(chips):
        c = t.rows[0].cells[i]
        cell_fmt(c, fill=None, borders={"top": ("single", 6, GOLD), "left": ("single", 6, GOLD),
                                        "bottom": ("single", 6, GOLD),
                                        "right": ("single", 6, GOLD)})
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = Pt(9)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, ch, font=INS, size=6.3, color=GOLD_D, caps=True, spacing=1.1)

    spacer(doc, 14)
    t = new_table(doc, [CONTENT_W], borders=False, pad=(240, 240, 280, 280))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill="FAF7F0", borders={"left": ("single", 24, FLAME)})
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = Pt(9)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "ANTI-TONO · LO QUE NUNCA VAMOS A ESCRIBIR", font=INS, size=7.2, color=FLAME,
            caps=True, spacing=1.8)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(14.6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "«Transforma tu vida». Emojis. Degradados pastel. Stock genérico de gente "
               "sonriendo en un gimnasio. La palabra «pasión» como argumento. «Nivel dios», "
               "«élite», «mentalidad ganadora» sin una sola cifra que lo respalde.",
            font=IN, size=9.6, color=TEXT)

    h3(doc, "Tres decisiones que ordenan todo", before=20, after=8)
    decisions = [
        ("01", "OSCURIDAD DE VESTUARIO, LUZ DE CANCHA",
         "El fondo es carbón; la luz entra dura y lateral. La página se siente como estar "
         "dentro del pabellón antes del partido: silencio, concentración, expectativa."),
        ("02", "EL DATO COMO DRAMA",
         "Los números no decoran: argumentan. 9 títulos, 340 jugadoras, 94 % de continuidad. "
         "Cada cifra aparece con su contexto —año, club, categoría— para que no pueda leerse "
         "como marketing."),
        ("03", "LA FOTO COMO ARCHIVO, NO COMO STOCK",
         "Tratamiento documental, grano fino, sin poses. La galería se revela en color al "
         "pasar el cursor: el archivo se abre cuando el visitante se interesa."),
    ]
    for num, title, text in decisions:
        t = new_table(doc, [0.5, 6.1], borders=False, pad=(100, 0, 120, 0))
        c = t.rows[0].cells[0]
        cell_fmt(c, fill=None)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(16)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, num, font=BDE, size=13, color=FLAME)
        c = t.rows[0].cells[1]
        cell_fmt(c, fill=None)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(11)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, title, font=BDS, size=8.6, color=INK, caps=True, spacing=0.8)
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = Pt(12.6)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, text, font=IN, size=8.8, color=SOFT)


def build_arquitectura(doc, page_later=False):
    sec_head(doc, "02", "Arquitectura", ["NUEVE BLOQUES.", "UN SOLO DESTINO."],
             "Cada sección tiene un trabajo: construir autoridad, disolver una duda o llevar "
             "al diagnóstico. El copy es el definitivo del brief y no se reescribe en "
             "producción.")

    rows = [
        ("00\nBARRA + HERO",
         "Promesa, prueba y CTA visibles sin scroll. Es el único lugar donde la marca se "
         "presenta y el único donde compite con la atención del visitante.",
         "Nav: Logros · Filosofía · Método · Programas · Contacto\n"
         "CTA nav: «AGENDAR DIAGNÓSTICO»\n"
         "Franja: «DISPONIBILIDAD LIMITADA — 4 ASESORÍAS 1:1 AL MES»\n"
         "Eyebrow: «BASKETBALL COACH · ALTO RENDIMIENTO · BOGOTÁ»\n"
         "H1: «EL JUEGO SE GANA / ANTES DEL / SALTO INICIAL.»\n"
         "Sub: «Formo jugadoras que leen el juego, lideran bajo presión y compiten con "
         "criterio. 12 años en cancha, 9 títulos y una metodología que convierte talento en "
         "resultados medibles.»\n"
         "CTA 2: «VER LA METODOLOGÍA ↓»\n"
         "Micro: «30 min · Sin costo · Cupos limitados»\n"
         "Tarjeta: «9 TÍTULOS / +340 JUGADORAS FORMADAS»\n"
         "Stats: 12 TEMPORADAS · 9 CAMPEONATOS · +340 JUGADORAS · 28 PROCESOS DE CLUB",
         "AGENDAR\nDIAGNÓSTICO\nGRATUITO"),
        ("01\nPRUEBA SOCIAL",
         "Convertir la promesa en evidencia. Es la sección que responde «¿y a quién le ha "
         "funcionado?» antes de que el visitante se lo pregunte.",
         "Eyebrow: «PALMARÉS»\nH2: «AUTORIDAD QUE SE MIDE EN LA CANCHA.»\n"
         "Intro: «Los títulos no se declaran: se registran. Este es el historial que respalda "
         "cada sesión.»\n"
         "Contadores: 9 Campeonatos · 12 Temporadas · 340+ Jugadoras formadas · 94 % "
         "Continuidad de procesos\n"
         "Timeline: 2025 Campeona Interclubes Femenino Sub-17 · Club Capas Basket / 2024 "
         "Subcampeona Nacional Femenino Mayores · Selección departamental / 2023 Campeona Liga "
         "Departamental · Invicta 14-0 / 2022 Clasificación Juegos Nacionales · Cuartos de "
         "final / 2021 Campeona Copa Ciudad Femenino Sub-15\n"
         "Chips oro: FIBA WABC Nivel 2 · Entrenadora Nivel III · Analista de video deportivo · "
         "Preparación física aplicada al baloncesto · Primeros auxilios deportivos\n"
         "Métricas: +18 jugadoras con beca deportiva universitaria · 7 convocadas a selección "
         "departamental · 31 % mejora promedio en índice de eficiencia (PER) tras 12 semanas",
         "—"),
        ("02\nFILOSOFÍA",
         "Diferenciar el método del resto del mercado. Aquí se explica por qué entrenar con "
         "ella no es «tomar clases».",
         "Eyebrow: «FILOSOFÍA»\nH2: «NO ENTRENO CUERPOS. / ENTRENO CRITERIO.»\n"
         "Intro: «Una jugadora sin lectura del juego depende de la suerte. Una jugadora con "
         "criterio decide el partido. Mi trabajo es construir esa diferencia, sesión tras "
         "sesión.»\n"
         "01 LECTURA DEL JUEGO — «Enseño a ver el espacio antes de ocuparlo. Cada decisión "
         "nace de una lectura, no de una corazonada.»\n"
         "02 DISCIPLINA INVISIBLE — «Hábitos, descanso, hidratación y rutina mental. La "
         "excelencia es un estándar diario, no un día inspirado.»\n"
         "03 LIDERAZGO COMPARTIDO — «Formo jugadoras que hablan, corrigen y sostienen al "
         "equipo cuando el marcador aprieta.»\n"
         "04 TALENTO CON PLAN — «Un plan individual por jugadora: técnica, físico, mentalidad "
         "y proyecto de vida. Nadie se desarrolla por accidente.»",
         "—"),
        ("03\nMETODOLOGÍA",
         "Dar nombre y estructura a lo que se compra. Convierte el servicio en sistema y "
         "justifica el precio.",
         "Eyebrow: «METODOLOGÍA»\nH2: «EL SISTEMA 360.»\n"
         "Intro: «Cuatro fases, un ciclo medible. Nada se deja a la intuición: cada semana "
         "tiene un objetivo, cada mes una evaluación.»\n"
         "01 DIAGNÓSTICO 360° — «Videoanálisis, métricas físicas y entrevista de contexto. "
         "Radiografía completa antes de tocar la cancha.»\n"
         "02 PLAN INDIVIDUAL — «Roadmap de 12 semanas con objetivos técnicos, tácticos y "
         "mentales por jugadora.»\n"
         "03 CANCHA — «Sesiones con carga táctica real: decisiones bajo presión, no repetición "
         "sin contexto.»\n"
         "04 EVALUACIÓN — «Datos cada 4 semanas. Si el plan no mueve el indicador, el plan se "
         "ajusta.»\n"
         "Microcopy: «Promedio de mejora documentada: 31 % en índice de eficiencia a las 12 "
         "semanas.»",
         "—"),
        ("04\nPROGRAMAS",
         "Segmentar la oferta y llevar a cada perfil a la conversación correcta. La asesoría "
         "1:1 es la opción destacada.",
         "Eyebrow: «PROGRAMAS»\nH2: «ELIGE TU CANCHA.»\n"
         "01 CLÍNICA GRUPAL — Para clubes y academias — 8 a 14 jugadoras · 90 min · 2 "
         "sesiones/semana — Incluye: Plan de sesiones · Videoanálisis grupal · Informe de "
         "progreso.\n"
         "02 ASESORÍA 1:1 — Para jugadoras que quieren dar el salto — Plan individual · 3 "
         "sesiones/semana · Seguimiento telefónico — Incluye: Diagnóstico 360° · Plan 12 "
         "semanas · Videoanálisis quincenal.\n"
         "03 DIRECCIÓN TÉCNICA — Para instituciones y federaciones — Temporada completa · "
         "Cuerpo técnico — Incluye: Modelo de juego · Formación de entrenadores · Informes de "
         "rendimiento.",
         "SOLICITAR\nDISPONIBILIDAD\n\nAGENDAR\nDIAGNÓSTICO\n(destacado)\n\nHABLAR CON LA "
         "COACH"),
        ("05\nGALERÍA",
         "Demostrar sin adjetivos. La evidencia visual reemplaza cualquier testimonio "
         "genérico.",
         "Eyebrow: «EVIDENCIA»\nH2: «DENTRO Y FUERA DE LA CANCHA.»\n"
         "Pie: «Fotos reales de procesos, clínicas y celebraciones. Sin stock, sin poses: "
         "trabajo.»\n"
         "4 piezas: retrato, equipo campeón, trofeo, clínica. Hover: escala 1.03 + etiqueta "
         "contextual; la imagen pasa de blanco y negro a color.",
         "—"),
        ("06\nTESTIMONIOS",
         "Cerrar la duda emocional: «¿quién responde por ella?». Tres voces, tres tipos de "
         "cliente.",
         "H2: «QUIENES YA JUGARON ESTE JUEGO.»\n"
         "Tres citas: jugadora, padre o madre, presidente de club. Se producen en la fase 1 "
         "con material real del cliente; no se inventan en diseño.",
         "—"),
        ("07\nCONTACTO",
         "Única conversión de la página. Todo el scroll anterior existe para que este "
         "formulario se sienta como el siguiente paso lógico.",
         "Eyebrow: «AGENDA»\nH2: «HABLEMOS DE TU PRÓXIMA TEMPORADA.»\n"
         "Sub: «Cuéntame dónde estás y a dónde quieres llegar. Te respondo en menos de 24 "
         "horas con un diagnóstico inicial sin costo.»\n"
         "Formulario: Nombre · Email · Teléfono · Perfil (Jugadora / Club o academia / "
         "Institución / Padre o madre) · Objetivo (textarea)\n"
         "Botón: «AGENDAR MI DIAGNÓSTICO →»\n"
         "Micro: «Sin costo ni compromiso · Respuesta en menos de 24 h · Datos tratados de "
         "forma confidencial.»\n"
         "Tarjeta: «AGENDA DIRECTA» — llamada directa, correo, base en Bogotá. «PRÓXIMA "
         "DISPONIBILIDAD: ABRIL — 3 CUPOS»\n"
         "FAQ: modalidad online · edades · nivel mínimo · política de cancelación",
         "AGENDAR MI\nDIAGNÓSTICO →"),
        ("08\nFOOTER",
         "Cerrar la marca y dejar accesos legales y de navegación para quien no convirtió.",
         "Logo + claim: «Criterio, disciplina y resultados.»\n"
         "Columnas: navegación · contacto · redes (Instagram, YouTube, LinkedIn)\n"
         "Legal: «© 2026 Gloria Celis · Política de privacidad · Términos»",
         "—"),
    ]
    t_arch = data_table(doc, [0.95, 1.38, 3.42, 0.85],
                        ["Sección", "Objetivo de conversión", "Copy final (brief)", "CTA"],
                        rows, body_size=7.4, body_line=9.4, header_size=6.9, header_line=8.4,
                        row_pad=(58, 58, 92, 92))
    # los CTA se maquetan como botones: Barlow Condensed en mayúsculas
    for ri in range(1, len(t_arch.rows)):
        c = t_arch.rows[ri].cells[3]
        texts = [p.text for p in c.paragraphs]
        for p in list(c.paragraphs):
            p._p.getparent().remove(p._p)
        for txt in texts:
            p = c.add_paragraph()
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            if not txt.strip():
                pf.line_spacing = Pt(5)
                pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                continue
            pf.line_spacing = Pt(9.6)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            add_run(p, txt, font=BD, size=7.6, color=INK, bold=True, caps=True, spacing=0.4)

    spacer(doc, 12)
    h3(doc, "Mapa de CTAs: una sola acción, cinco apariciones", before=14, after=6)
    body(doc, "El CTA primario es siempre el mismo texto y el mismo destino. Cambiar la "
              "etiqueta según la sección es la forma más rápida de romper una landing que "
              "convierte: el visitante tiene que reconocer el botón antes de leerlo.")

    data_table(doc, [1.5, 2.15, 2.95],
               ["Punto de contacto", "Etiqueta exacta", "Condición de aparición"],
               [
                   ["Nav (sticky)", "AGENDAR DIAGNÓSTICO", "Siempre visible; fondo carbón al "
                                                            "hacer scroll"],
                   ["Hero", "AGENDAR DIAGNÓSTICO GRATUITO", "Sobre el pliegue, junto al CTA "
                                                           "secundario"],
                   ["Programa 1:1", "AGENDAR DIAGNÓSTICO", "Tarjeta destacada con borde "
                                                           "naranja"],
                   ["Barra móvil", "AGENDAR DIAGNÓSTICO GRATUITO", "Fija al pie en < 768 px"],
                   ["Formulario", "AGENDAR MI DIAGNÓSTICO →", "Botón del formulario: dice el "
                                                              "resultado, no la acción"],
               ], body_size=8.0, body_line=10.0)

    spacer(doc, 14)
    h3(doc, "Anclas y navegación", before=14, after=6)
    data_table(doc, [1.35, 1.75, 3.5],
               ["Ancla", "Destino", "Nota de maquetación"],
               [
                   ["#logros", "Prueba social y palmarés", "Scroll suave con offset de 64 px "
                                                            "por el header sticky"],
                   ["#filosofia", "Filosofía y pilares", "La marquesina ✦ separa sin cortar el "
                                                          "ritmo de lectura"],
                   ["#metodo", "Sistema 360", "La pizarra isométrica sangra el borde derecho"],
                   ["#programas", "Tres programas", "La tarjeta 1:1 es la única con borde "
                                                     "naranja"],
                   ["#contacto", "Formulario y agenda", "Ancla del CTA primario en toda la "
                                                         "página"],
               ], body_size=7.8, body_line=9.8)

    spacer(doc, 12)
    callout(doc, "Una sección no es un bloque de contenido: es una objeción que se resuelve. "
                 "Si al eliminar una sección la decisión del visitante no cambia, la sección "
                 "no era necesaria. El orden del brief ya está probado; la producción no lo "
                 "reordena.",
            kicker="Regla de arquitectura", accent=FLAME, dark=True,
            body_font=IN, body_size=9.6, body_line=14)


def build_sistema(doc, page_later=False):
    sec_head(doc, "03", "Sistema de diseño", ["CARBÓN, CREMA", "Y DOS ACENTOS."],
             "Un sistema de tokens cerrado: si un color, un tamaño o un radio no está en esta "
             "sección, no existe en la página. La consistencia es lo que hace que una landing "
             "parezca una marca.", new_page=False)

    # qué contiene la sección (llena el final de página y orienta al lector)
    strip = [("01", "COLOR"), ("02", "TIPOGRAFÍA"), ("03", "REJILLA"), ("04", "COMPONENTES")]
    gap = 0.12
    cw = (CONTENT_W - gap * 3) / 4
    t = new_table(doc, [cw, gap, cw, gap, cw, gap, cw], borders=False, pad=(0, 0, 0, 0))
    for i, (num, label) in enumerate(strip):
        c = t.rows[0].cells[i * 2]
        cell_fmt(c, fill=WARM, borders={"top": ("single", 12, GOLD)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, num, font=BDE, size=9.6, color=FLAME)
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(9)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, label, font=INS, size=6.6, color=INK, caps=True, spacing=1.2)
    row_cant_split(t.rows[0])

    h3(doc, "Paleta: roles y proporción", before=22, after=7)
    intro = body(doc, "Nueve tokens, una regla 60/30/10. Los neutros dominan el 80 % de la "
                      "superficie; el naranja queda reservado a la acción y el oro al logro. "
                      "Nunca comparten componente.")
    intro.paragraph_format.keep_with_next = True

    palette = [
        ("--ink", "Carbón 900", "0A0B0D", "Fondo principal, vestuario", "45 %"),
        ("--carbon", "Carbón 800", "111317", "Secciones alternas", "20 %"),
        ("--steel", "Carbón 700", "1A1D22", "Tarjetas y superficies", "15 %"),
        ("--line", "Acero línea", "3A3D43", "Bordes y divisores (blanco al 10 %)", "—"),
        ("--cream", "Crema", "F4F1E9", "Texto principal sobre carbón", "10 %"),
        ("--muted", "Acero", "8E959E", "Texto secundario en oscuro", "—"),
        ("--flame", "Naranja Balón", "FF4D1F", "CTA, energía, datos clave", "6 %"),
        ("--gold", "Oro Trofeo", "E9B44C", "Logros, certificaciones, premium", "3 %"),
        ("--wood", "Madera cancha", "2A1B12", "Textura sutil de cancha", "1 %"),
    ]
    t = new_table(doc, [0.5, 0.95, 0.72, 3.33, 1.1], pad=(70, 70, 100, 100))
    hdr = t.rows[0]
    for i, h in enumerate(("", "Token", "Hex", "Rol", "Proporción")):
        c = hdr.cells[i]
        cell_fmt(c, fill=CARBON)
        cell_text(c, h, font=BDS, size=6.9, color=CREAM, caps=True, spacing=0.8, line=8.4)
    for token, name, hexv, role, prop in palette:
        row = t.add_row()
        row_cant_split(row)
        row_height(row, 0.36, exact=True)
        c = row.cells[0]
        cell_fmt(c, fill=hexv)
        cell_fmt(row.cells[1], fill=None)
        cell_text(row.cells[1], token, font=INS, size=7.4, color=INK, line=9.4)
        cell_fmt(row.cells[2], fill=None)
        cell_text(row.cells[2], "#" + hexv, font=IN, size=7.2, color=SOFT, line=9.4)
        cell_fmt(row.cells[3], fill=None)
        cell_text(row.cells[3], f"{name} · {role}", font=IN, size=7.6, color=TEXT, line=9.6)
        c = row.cells[4]
        cell_fmt(c, fill=None)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(9.4)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, prop, font=BD, size=9.2, color=INK, bold=True)
    keep_table_together(t)

    spacer(doc, 10)
    # barra de proporción real
    widths = [0.45 * 6.6, 0.20 * 6.6, 0.15 * 6.6, 0.10 * 6.6, 0.06 * 6.6, 0.03 * 6.6,
              0.01 * 6.6]
    fills = [INK, CARBON, STEEL, CREAM, FLAME, GOLD, "2A1B12"]
    t = new_table(doc, widths, borders=True, border_color=WHITE, border_sz=2,
                  pad=(0, 0, 0, 0))
    for i, (w, f) in enumerate(zip(widths, fills)):
        c = t.rows[0].cells[i]
        cell_fmt(c, fill=f)
        cell_text(c, "", size=1, line=1)
    row_height(t.rows[0], 0.30, exact=True)
    p = para(doc, "", size=6.6, color=SOFT, line=9, before=4, after=4)
    add_run(p, "PROPORCIÓN 60/30/10  ·  ", font=INS, size=6.2, color=SOFT, caps=True,
            spacing=1.2)
    add_run(p, "neutros 80 % (ink + carbon + steel + cream)  /  naranja 6 %  /  oro 3 %",
            font=IN, size=6.6, color=SOFT)

    callout(doc, "Naranja sobre crema: prohibido (contraste 2,9:1, no pasa AA). El naranja "
                 "solo aparece sobre carbón, y el oro solo sobre carbón o blanco en su versión "
                 "oscura #8A6416. Nunca naranja y oro en el mismo componente: compiten y "
                 "ninguno gana.",
            kicker="Reglas que no se negocian", accent=GOLD, dark=False)

    h3(doc, "Contraste: los pares aprobados", before=18, after=6)
    data_table(doc, [2.35, 1.15, 3.1],
               ["Combinación", "Ratio", "Uso permitido"],
               [
                   ["Crema #F4F1E9 sobre carbón 900", "17,4:1", "Texto principal, párrafos y "
                                                                "titulares"],
                   ["Crema sobre carbón 800", "16,5:1", "Secciones alternas y tarjetas"],
                   ["Oro #E9B44C sobre carbón 900", "10,4:1", "Kickers, chips y cifras de "
                                                              "logro"],
                   ["Naranja #FF4D1F sobre carbón 900", "5,9:1", "CTA, cifras y acentos: pasa "
                                                                 "AA también en texto pequeño"],
                   ["Oro oscuro #8A6416 sobre crema", "5,0:1", "Kickers y enlaces sobre "
                                                               "superficies claras"],
                   ["Naranja sobre crema", "2,9:1", "Prohibido para texto: solo filetes y "
                                                    "formas, nunca tipografía"],
               ], body_size=7.8, body_line=9.8)


def build_sistema_tipo(doc):
    h3(doc, "Tipografía: especímenes reales", before=18, after=8)
    intro = body(doc, "Barlow Condensed para la voz alta —titulares, cifras, botones— e Inter "
                      "para la voz que explica. Ambas están autoalojadas en woff2 y se aplican "
                      "tal como se ven aquí: este documento usa los archivos del proyecto, no "
                      "una aproximación.")
    intro.paragraph_format.keep_with_next = True

    # espécimen display
    t = new_table(doc, [CONTENT_W], borders=False, pad=(300, 300, 340, 340))
    row_cant_split(t.rows[0])
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=INK)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(9)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "DISPLAY · BARLOW CONDENSED 800 · MAYÚSCULAS", font=INS, size=6.4, color=GOLD,
            caps=True, spacing=2.0)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = Pt(38)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "EL JUEGO\nSE GANA ANTES", font=BDE, size=44, color=CREAM, spacing=-0.8)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(10.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "ABCDEFGHIJKLMNOPQRSTUVWXYZ  ·  0123456789  ·  ÁÉÍÓÚÑ", font=BDE, size=8.4,
            color=MUTED, spacing=1.2)

    # anotaciones técnicas del display
    t = new_table(doc, [1.65, 1.65, 1.65, 1.65], borders=False, pad=(120, 0, 150, 0))
    specs = [("PESO", "700 / 800"), ("TRACKING", "−0.015 em"),
             ("LINE-HEIGHT", "0.92"), ("ESCALA", "clamp(2.75–6.5 rem)")]
    for i, (k, v) in enumerate(specs):
        c = t.rows[0].cells[i]
        cell_fmt(c, fill=None, borders={"top": ("single", 6, GOLD)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(8)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, k, font=INS, size=6.0, color=SOFT, caps=True, spacing=1.4)
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(13)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, v, font=BD, size=11.5, color=INK, bold=True)
    row_cant_split(t.rows[0])

    spacer(doc, 16)
    # espécimen de cuerpo + eyebrow + números
    t = new_table(doc, [CONTENT_W], borders=True, border_color=LINE_C, border_sz=4,
                  pad=(300, 300, 340, 340))
    row_cant_split(t.rows[0])
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=None)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = Pt(10)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "EYEBROW · INTER SEMIBOLD 600 · 11–12 PX · TRACKING .20 EM", font=INS,
            size=6.6, color=GOLD_D, caps=True, spacing=2.2)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = Pt(13)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Cuerpo · Inter 400 · 16–19 px · line-height 1.65 · máximo 62 caracteres por "
               "línea. Una jugadora sin lectura del juego depende de la suerte; una jugadora "
               "con criterio decide el partido.", font=IN, size=10.4, color=TEXT)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(10)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "NÚMEROS · BARLOW CONDENSED 800 · 72–96 PX · TABULAR-NUMS", font=INS, size=6.6,
            color=GOLD_D, caps=True, spacing=2.2)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(30)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "9    12    340+    94 %    31 %", font=BDE, size=27, color=INK, spacing=0.4)

    spacer(doc, 16)
    h3(doc, "Escala tipográfica", before=8, after=6)
    data_table(doc, [1.2, 1.35, 1.4, 1.05, 1.6],
               ["Token", "Familia / peso", "Tamaño", "Interlineado", "Uso"],
               [
                   ["Display XL", "Barlow Cond 800", "clamp 44–104 px", "0.92", "H1 del hero"],
                   ["Display L", "Barlow Cond 800", "56–72 px", "0.94", "H2 de sección"],
                   ["Título M", "Barlow Cond 700", "32–40 px", "1.00", "H3, tarjetas de programa"],
                   ["Número", "Barlow Cond 800", "72–96 px", "0.90", "Contadores y cifras"],
                   ["Cuerpo L", "Inter 400", "18–19 px", "1.65", "Intro de sección"],
                   ["Cuerpo M", "Inter 400", "16–17 px", "1.65", "Párrafos y listas"],
                   ["Eyebrow", "Inter 600", "11–12 px", "1.20", "Kickers, tracking .20 em"],
                   ["Botón", "Barlow Cond 700", "15–16 px", "1.00", "CTA, tracking .10 em"],
                   ["Micro", "Inter 500", "12–13 px", "1.40", "Prueba, notas legales"],
               ], body_size=7.8, body_line=9.6)


def build_sistema_grid(doc):
    h3(doc, "Rejilla, espaciado y componentes", before=18, after=8)
    body(doc, "Una rejilla de 12 columnas con 1 240 px de ancho máximo y 24 px de gutter. Las "
              "secciones respiran con 112 px de padding vertical: aire suficiente para que la "
              "página se lea como una revista, no como un panel de administración.")

    # diagrama de 12 columnas
    gut = 0.055
    col = (CONTENT_W - gut * 11) / 12
    widths, fills = [], []
    for i in range(12):
        widths.append(col)
        fills.append(FLAME if i in (0, 6) else "EDE7DA")
        if i < 11:
            widths.append(gut)
            fills.append(WHITE)
    t = new_table(doc, widths, borders=False, pad=(0, 0, 0, 0))
    for i, f in enumerate(fills):
        c = t.rows[0].cells[i]
        cell_fmt(c, fill=None if f == WHITE else f)
        cell_text(c, "", size=1, line=1)
    row_height(t.rows[0], 0.36, exact=True)
    p = para(doc, "", size=6.6, color=SOFT, line=9, before=4, after=6)
    add_run(p, "12 COLUMNAS  ·  24 PX GUTTER  ·  MAX-WIDTH 1 240 PX  ·  PADDING 112 PX",
            font=INS, size=6.0, color=SOFT, caps=True, spacing=1.2)

    data_table(doc, [1.3, 1.5, 3.8],
               ["Token de espacio", "Valor", "Uso"],
               [
                   ["--s1", "4 px", "Separación mínima entre icono y texto"],
                   ["--s2", "8 px", "Interior de chips y etiquetas"],
                   ["--s3", "16 px", "Ritmo de párrafo"],
                   ["--s4", "24 px", "Gutter de rejilla"],
                   ["--s5", "32 px", "Padding de tarjeta"],
                   ["--s6", "48 px", "Separación entre bloques"],
                   ["--s7", "64 px", "Encabezado de sección"],
                   ["--s8", "112 px", "Padding vertical de sección"],
               ], body_size=7.8, body_line=9.8)

    spacer(doc, 10)
    data_table(doc, [1.35, 2.4, 2.85],
               ["Componente", "Especificación", "Comportamiento"],
               [
                   ["Botón primario", "Fondo #FF4D1F · texto #0A0B0D · Barlow Cond 700 "
                                      "16 px, MAYÚS, tracking .10 em · radio 2 px · padding "
                                      "18 × 32 px",
                    "Hover: translateY(−2 px) + sombra 0 30 80 −20 rgba(0,0,0,.65)"],
                   ["Botón secundario", "Transparente · borde 1 px rgba(255,255,255,.18) · "
                                        "texto crema", "Hover: borde crema al 40 %"],
                   ["Chip / badge", "Radio 999 px · borde 1 px oro 45 % · Inter 600 11 px, "
                                    "MAYÚS, tracking .14 em", "Solo sobre carbón"],
                   ["Tarjeta", "Fondo #1A1D22 · borde 1 px rgba(255,255,255,.10) · radio "
                               "2 px · padding 32 px", "Hover: translateY(−4 px)"],
                   ["Campo de formulario", "Fondo transparente · borde inferior 1 px · label "
                                           "flotante en Inter 500 12 px",
                    "Foco: anillo naranja 2 px + offset 2 px"],
                   ["Acordeón FAQ", "Borde superior 1 px · icono +/− a la derecha",
                    "aria-expanded, una sola respuesta abierta"],
                   ["Marquesina", "Barlow Cond 700, palabras separadas por ✦",
                    "32 s linear infinite · pausa en hover"],
               ], body_size=7.6, body_line=9.4)


def build_direccion(doc):
    sec_head(doc, "04", "Dirección de arte", ["QUE PAREZCA", "UNA CANCHA."],
             "Tres materiales y nada más: fotografía real tratada como documento, tres piezas "
             "3D secundarias y gráficos tácticos 2D. Si un elemento decorativo no aporta "
             "evidencia, se elimina.", new_page=False)

    # fotografía: texto + retrato
    t = new_table(doc, [3.45, 3.15], borders=False, pad=(0, 0, 0, 140))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=None)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = Pt(15)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "FOTOGRAFÍA · EL ARCHIVO, NO EL STOCK", font=BDS, size=10.2, color=INK,
            caps=True, spacing=1.0)
    txt = ("Contraste alto, negros profundos, saturación contenida (−10) y grano fino de "
           "película al 4 %. Luz dura de cancha, sombras marcadas, encuadres que cortan el "
           "cuerpo como un reportaje deportivo. Nada de sonrisas a cámara.")
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = Pt(13.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, txt, font=IN, size=9.2, color=TEXT)
    specs = [("Recortes", "4:5 verticales · 3:4 galería"), ("Hero", "máscara diagonal + marco oro 1 px"),
             ("Galería", "B/N por defecto, color al hover"), ("Grano", "film 4 % · sin HDR")]
    for k, v in specs:
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(11.6)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, k.upper() + "  ", font=INS, size=6.6, color=GOLD_D, caps=True, spacing=1.2)
        add_run(p, v, font=IN, size=8.6, color=SOFT)
    c = t.rows[0].cells[1]
    cell_fmt(c, fill=None, pad=(0, 0, 0, 0))
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.add_run().add_picture(os.path.join(IMG, "doc-hero-retrato.jpg"), width=Inches(2.72))
    p = c.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(9.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Hero · retrato 4:5 con máscara diagonal", font=IN, size=6.6, color=SOFT,
            italic=True)

    spacer(doc, 12)
    h3(doc, "El archivo se revela", before=12, after=6)
    body(doc, "La galería se entrega en blanco y negro y revela su color al pasar el cursor. "
              "Es un gesto narrativo, no un efecto: la página muestra primero el documento y "
              "solo entrega la memoria cuando el visitante demuestra interés.")
    t = new_table(doc, [3.25, 3.25], borders=False, pad=(0, 0, 0, 60))
    for i, (path, cap) in enumerate((
            (os.path.join(IMG, "doc-equipo-bw.jpg"), "01 · Por defecto: archivo en B/N"),
            (os.path.join(IMG, "doc-equipo-color.jpg"), "02 · Hover: el archivo se revela"))):
        c = t.rows[0].cells[i]
        cell_fmt(c, fill=None, pad=(0, 90, 0, 90))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p.add_run().add_picture(path, width=Inches(3.12))
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(9.4)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, cap, font=IN, size=6.6, color=SOFT, italic=True)


def build_direccion3d(doc):
    h3(doc, "Elementos 3D: tres piezas, nunca protagonistas", before=18, after=6)
    body(doc, "Las piezas 3D existen para dar profundidad a la foto, no para reemplazarla. "
              "Son secundarias, oscuras y rugosas: materiales gastados, no plásticos de "
              "catálogo. La regla es simple: si una pieza compite con el retrato, se elimina.")
    t3d = data_table(doc, [1.15, 1.25, 1.65, 1.45, 1.1],
                     ["Elemento", "Dónde", "Material y geometría", "Luces", "Cámara / export"],
               [
                   ["Balón flotante", "Hero, detrás del retrato, 180–220 px",
                    "Cuero naranja #FF4D1F con desgaste sutil; esfera con costuras modeladas",
                    "Key lateral dura + rim light frío", "50 mm · PNG alfa · WebP < 300 KB"],
                   ["Pizarra táctica isométrica", "Metodología, sangrando el borde derecho",
                    "Tablero 1400 × 900, isometría 30°; imanes circulares naranja/gris, "
                    "flechas de corte en oro", "Luz cenital suave + fill", "Orto · fondo "
                                                                          "transparente"],
                   ["Trofeo estilizado", "Logros, junto al contador de 9 campeonatos, 260 px",
                    "Low-poly, oro mate #E9B44C, sin brillo especular alto",
                    "Key + rim + fill suave", "35 mm · sombra de contacto quemada"],
               ], body_size=7.4, body_line=9.2)
    keep_table_together(t3d)

    spacer(doc, 10)
    t = new_table(doc, [CONTENT_W], borders=False, pad=(260, 260, 300, 300))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=CARBON, borders={"left": ("single", 24, GOLD)})
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = Pt(9.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "ESPECIFICACIÓN DE RENDER", font=INS, size=7.2, color=GOLD, caps=True,
            spacing=2.0)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(14.2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Blender, Cinema 4D o Spline  ·  motor Cycles / Redshift  ·  tres luces "
               "(key + rim + fill suave)  ·  materiales rugosos, roughness ≥ 0,6  ·  render "
               "4K  ·  export PNG con alfa + WebP < 300 KB  ·  sombra de contacto quemada en "
               "la imagen  ·  rotación del balón 30 s en CSS (rotateY), nunca en video.",
            font=IN, size=8.8, color=CREAM)


def build_direccion2d(doc):
    h3(doc, "Gráficos tácticos 2D", before=20, after=6)
    body(doc, "Las líneas de cancha funcionan como textura de fondo al 6 % de opacidad; los "
              "diagramas de jugada —flechas discontinuas, X de defensa, imanes— se usan como "
              "separadores y como fondo de la sección de metodología. Todo en SVG para que "
              "escale sin perder nitidez.")
    framed_image(doc, os.path.join(IMG, "doc-tactico-2d.png"), CONTENT_W,
                 "Diagrama de jugada · flechas discontinuas en oro, defensa en acero, imanes "
                 "naranja · export SVG + PNG de respaldo", frame=LINE_C, pad=0.06)
    spacer(doc, 4)
    t2d = data_table(doc, [2.0, 4.6],
                     ["Pieza", "Especificación"],
               [
                   ["Textura de cancha", "SVG · trazo #F4F1E9 al 6 % de opacidad · repetida "
                                          "con background-position"],
                   ["Diagramas de jugada", "SVG inline · flechas discontinuas oro, X de "
                                           "defensa acero · 1 por sección como máximo"],
                   ["Marquesina", "Palabras clave separadas por ✦ · 32 s linear infinite · "
                                  "respeta prefers-reduced-motion"],
                   ["Etiquetas de hover", "Chip oro al 45 % con Inter 600 11 px sobre la "
                                          "fotografía"],
               ], body_size=7.8, body_line=9.8)
    keep_table_together(t2d)


def build_copy(doc):
    sec_head(doc, "05", "Copywriting", ["DECIR POCO.", "DECIR EXACTO."],
             "La voz no pide atención: la gana con precisión. Titulares cortos, datos antes "
             "que adjetivos, segunda persona y ni un emoji en toda la página.", new_page=False)

    h3(doc, "Titulares finales", before=4, after=6)
    body(doc, "Estos son los titulares que van a producción. Cada uno tiene una función "
              "distinta en el recorrido y se mantiene idéntico en todas las versiones del "
              "prototipo.")
    heads = [
        ("H1 · HERO", "EL JUEGO SE GANA ANTES DEL SALTO INICIAL."),
        ("H2 · PALMARÉS", "AUTORIDAD QUE SE MIDE EN LA CANCHA."),
        ("H2 · FILOSOFÍA", "NO ENTRENO CUERPOS. ENTRENO CRITERIO."),
        ("H2 · MÉTODO", "EL SISTEMA 360."),
        ("H2 · PROGRAMAS", "ELIGE TU CANCHA."),
        ("H2 · GALERÍA", "DENTRO Y FUERA DE LA CANCHA."),
        ("H2 · TESTIMONIOS", "QUIENES YA JUGARON ESTE JUEGO."),
        ("H2 · CONTACTO", "HABLEMOS DE TU PRÓXIMA TEMPORADA."),
    ]
    t = new_table(doc, [1.35, 5.25], borders=False, pad=(60, 60, 80, 80))
    for i, (k, v) in enumerate(heads):
        row = t.rows[0] if i == 0 else t.add_row()
        row_cant_split(row)
        row_height(row, 0.36)
        c = row.cells[0]
        cell_fmt(c, fill=None, borders={"bottom": ("single", 4, LINE_C)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(9)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, k, font=INS, size=6.4, color=SOFT, caps=True, spacing=1.4)
        c = row.cells[1]
        cell_fmt(c, fill=None, borders={"bottom": ("single", 4, LINE_C)})
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(15)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, v, font=BD, size=13.6, color=INK, bold=True, spacing=0.2)

    h3(doc, "A/B testing: tres titulares, tres apuestas", before=18, after=6)
    body(doc, "Tres variantes para el H1 con hipótesis distintas. La A es la recomendada; B y C "
              "se reservan para tráfico frío y campañas. Se prueban de a una, con una sola "
              "variable: cambiar titular y CTA a la vez invalida la lectura.")
    data_table(doc, [0.55, 2.55, 3.5],
               ["Var.", "Titular", "Razón estratégica"],
               [
                   ["A", "EL JUEGO SE GANA ANTES DEL SALTO INICIAL.",
                    "Recomendada. Crea curiosidad y enmarca el criterio como ventaja; el "
                    "visitante no sabe qué vende todavía y quiere saberlo."],
                   ["B", "NO ENTRENO CUERPOS. ENTRENO CRITERIO.",
                    "Diferenciación directa. Apela a padres y clubes que ya se decepcionaron "
                    "de la formación físico-técnica sin lectura de juego."],
                   ["C", "9 TÍTULOS. 340 JUGADORAS. UNA METODOLOGÍA.",
                    "Prueba primero. Funciona en tráfico frío de pauta: la autoridad numérica "
                    "detiene el scroll antes de cualquier promesa."],
               ], body_size=7.8, body_line=9.8)

    h3(doc, "A/B testing: tres CTAs", before=16, after=6)
    data_table(doc, [0.55, 2.15, 3.9],
               ["Var.", "CTA", "Razón estratégica"],
               [
                   ["A", "AGENDAR DIAGNÓSTICO GRATUITO",
                    "Recomendada. La palabra «gratuito» elimina el riesgo de la primera "
                    "interacción y «diagnóstico» promete valor, no una llamada de venta."],
                   ["B", "QUIERO EL DIAGNÓSTICO 360°",
                    "Primera persona y nombre propio del método: mayor intención para "
                    "visitantes que ya leyeron la metodología."],
                   ["C", "VER DISPONIBILIDAD",
                    "Escasez y bajo compromiso. Para audiencias tibias y para la barra móvil, "
                    "donde el usuario decide si sigue o abandona."],
               ], body_size=7.8, body_line=9.8)


def build_copy2(doc):
    h3(doc, "Microcopy: los textos que sostienen la conversión", before=16, after=6)
    body(doc, "El microcopy no es relleno: es donde se responde la objeción real. Se escribe "
              "con el mismo cuidado que el H1 y se revisa junto con el flujo de formulario.")
    data_table(doc, [1.5, 5.1],
               ["Ubicación", "Texto exacto"],
               [
                   ["Bajo el CTA del hero", "30 min · Sin costo · Cupos limitados"],
                   ["Bajo el botón del formulario",
                    "Sin costo ni compromiso · Respuesta en menos de 24 h · Datos tratados de "
                    "forma confidencial."],
                   ["Franja de disponibilidad", "DISPONIBILIDAD LIMITADA — 4 ASESORÍAS 1:1 AL "
                                                "MES"],
                   ["Tarjeta de agenda", "PRÓXIMA DISPONIBILIDAD: ABRIL — 3 CUPOS"],
                   ["FAQ · modalidad", "Sesiones presenciales en Bogotá y acompañamiento online "
                                       "para jugadoras de otras ciudades."],
                   ["FAQ · edades", "Desde los 12 años, con autorización de acudiente hasta los "
                                    "18."],
                   ["FAQ · nivel mínimo", "No se exige nivel competitivo: se exige compromiso "
                                          "de tres sesiones semanales."],
                   ["FAQ · cancelación", "Reprogramación sin costo hasta 24 h antes; las "
                                         "sesiones no se acumulan."],
               ], body_size=7.8, body_line=9.8)

    spacer(doc, 14)
    callout(doc, "La diferencia entre una landing que convierte y un folleto digital está en "
                 "lo que no dice. Cada sección elimina una objeción: ¿tiene resultados? ¿tiene "
                 "método? ¿es para alguien como yo? ¿qué pasa si escribo?",
            kicker="El principio de escritura", accent=FLAME, dark=True,
            body_font=INS, body_size=12.6, body_line=18)


def build_cro(doc):
    sec_head(doc, "06", "CRO", ["UNA SOLA ACCIÓN.", "CINCO OPORTUNIDADES."],
             "La conversión no se diseña al final: se decide en la arquitectura. Ocho reglas "
             "operativas, un formulario de cuatro campos y siete eventos que permiten saber "
             "dónde se pierde el partido.", new_page=False)

    h3(doc, "Ocho reglas de conversión", before=4, after=6)
    data_table(doc, [0.4, 2.2, 2.55, 1.45],
               ["#", "Regla", "Implementación", "Verificación"],
               [
                   ["1", "Un solo CTA primario", "Mismo texto y destino en cinco puntos: nav, "
                                                 "hero, programa 1:1, barra móvil y formulario",
                    "Auditoría: una sola etiqueta primaria por viewport"],
                   ["2", "Promesa + prueba + CTA sin scroll", "Hero a 100 vh con tarjeta de 9 "
                                                              "títulos y micro-prueba",
                    "Test en 390 × 844 y 1280 × 720"],
                   ["3", "Formulario de 4 campos + mensaje", "Nombre, Email, Teléfono, Perfil y "
                                                             "Objetivo", "Conteo de inputs del "
                                                                         "flujo"],
                   ["4", "El botón dice el resultado", "«AGENDAR MI DIAGNÓSTICO →», nunca "
                                                       "«Enviar»", "Revisión de copy"],
                   ["5", "Prueba numérica y fechada", "Cinco hitos con año y club en el "
                                                      "palmarés", "Revisión editorial"],
                   ["6", "Reducir ansiedad", "«Sin costo», «sin compromiso», «24 h», «cupos "
                                              "limitados» junto al CTA", "Micro bajo el botón"],
                   ["7", "Llamada directa flotante", "Canal de menor fricción en LATAM; "
                                                         "aparece tras 30 % de scroll",
                    "No tapa el CTA ni el formulario"],
                   ["8", "Anclas exactas y sticky header", "Scroll suave con offset de 64 px; "
                                                           "header con CTA en mobile",
                    "Prueba en iOS y Android"],
               ], body_size=7.5, body_line=9.4)

    h3(doc, "Arquitectura del formulario", before=16, after=6)
    data_table(doc, [1.15, 1.05, 0.9, 1.65, 1.85],
               ["Campo", "Tipo", "Obligatorio", "Validación", "Microcopy"],
               [
                   ["Nombre", "Texto", "Sí", "Mínimo 2 caracteres", "¿Cómo te llamas?"],
                   ["Email", "Email", "Sí", "Formato + dominio válido", "Te escribo aquí"],
                   ["Teléfono / WhatsApp", "Teléfono", "Sí", "+57 · 10 dígitos", "Solo para coordinar"],
                   ["Perfil", "Select", "Sí", "4 opciones cerradas", "Jugadora / Club o "
                                                                      "academia / Institución / "
                                                                      "Padre o madre"],
                   ["Objetivo", "Textarea", "No", "Máximo 280 caracteres", "¿Dónde estás y a "
                                                                          "dónde quieres "
                                                                          "llegar?"],
               ], body_size=7.6, body_line=9.4)

    h3(doc, "Eventos de medición", before=16, after=6)
    data_table(doc, [1.7, 2.15, 1.7, 1.05],
               ["Evento", "Disparador", "Parámetros", "Destino"],
               [
                   ["cta_click_hero", "Clic en CTA del hero", "seccion, variante_ab", "GA4"],
                   ["cta_click_programa", "Clic en CTA de programa", "programa, precio_rango",
                    "GA4"],
                   ["form_start", "Primer foco en el formulario", "campo_origen", "GA4"],
                   ["form_submit", "Envío exitoso", "perfil, objetivo_len", "GA4 + CRM"],
                   ["phone_click", "Clic en «Llamar»", "origen, seccion", "GA4"],
                   ["scroll_75", "75 % de la página recorrida", "seccion_actual", "GA4"],
                   ["faq_open", "Apertura de una pregunta", "pregunta", "GA4"],
               ], body_size=7.5, body_line=9.2)

    spacer(doc, 14)
    stats_row(doc, [("≥ 4 %", "Conversión de formulario"),
                    ("≥ 9 %", "Clic a llamada"),
                    ("< 24 h", "Respuesta al lead"),
                    ("< 1,8 s", "LCP en 4G")])


def build_tecnica(doc):
    sec_head(doc, "07", "Especificación", ["RÁPIDO, ACCESIBLE,", "SIN DEPENDENCIAS."],
             "El prototipo se construye en HTML, CSS y JavaScript sin librerías. Cada decisión "
             "técnica está tomada para que la página cargue antes de que el visitante decida "
             "abandonarla.", new_page=False)

    h3(doc, "Stack y construcción", before=4, after=6)
    data_table(doc, [1.45, 2.45, 2.7],
               ["Capa", "Decisión", "Razón"],
               [
                   ["Markup", "HTML5 semántico, una sola página con anclas",
                    "Base accesible, indexable y sin hidratación"],
                   ["Estilos", "CSS3 con custom properties para los tokens",
                    "Tema consistente sin build step"],
                   ["Comportamiento", "JavaScript vanilla, ≤ 12 KB minificado",
                    "Sin dependencias, sin bloqueo de render"],
                   ["Tipografía", "woff2 autoalojadas (OFL), preload de display",
                    "Sin FOIT, sin llamadas a terceros"],
                   ["Formulario", "Endpoint propio + honeypot + rate limit",
                    "Sin SDKs pesados ni cookies de terceros"],
                   ["Analítica", "GA4 con eventos personalizados",
                    "Medición del funnel completo"],
                   ["Despliegue", "Hosting estático + CDN con HTTPS",
                    "TTFB < 200 ms en Colombia"],
               ], body_size=7.6, body_line=9.4)

    h3(doc, "Accesibilidad (WCAG 2.1 AA)", before=16, after=6)
    data_table(doc, [1.45, 3.25, 1.9],
               ["Criterio", "Implementación", "Verificación"],
               [
                   ["Contraste", "Crema sobre carbón 17,4:1; naranja sobre carbón 5,9:1; "
                                 "nunca naranja sobre crema (2,9:1)", "axe + contraste manual"],
                   ["Foco visible", ":focus-visible de 2 px naranja con offset 2 px",
                    "Recorrido completo con Tab"],
                   ["Landmarks", "header, nav, main, section, footer", "Lector de pantalla"],
                   ["Alternativas", "alt descriptivo en cada foto; decorativas con alt vacío",
                    "Revisión editorial"],
                   ["ARIA", "aria-expanded en FAQ, aria-controls en menú", "axe + VoiceOver"],
                   ["Movimiento", "prefers-reduced-motion desactiva reveals y marquesina",
                    "Test del sistema operativo"],
                   ["Formularios", "Labels visibles, errores en aria-live", "Prueba con "
                                                                          "teclado"],
               ], body_size=7.4, body_line=9.2)

    h3(doc, "Presupuesto de performance", before=16, after=6)
    data_table(doc, [1.6, 1.5, 3.5],
               ["Métrica", "Objetivo", "Técnica"],
               [
                   ["LCP", "< 1,8 s en 4G", "Hero preload + fetchpriority=high + WebP"],
                   ["CLS", "< 0,05", "width/height declarados, fuentes con size-adjust"],
                   ["JS", "≤ 12 KB", "Vanilla, sin frameworks ni polyfills"],
                   ["Imágenes", "≤ 900 KB total", "Lazy salvo hero, AVIF/WebP responsive"],
                   ["Fuentes", "≤ 180 KB", "Subset latin, font-display: swap"],
                   ["Lighthouse", "≥ 95 en Performance y Accessibility", "Auditoría en cada "
                                                                          "release"],
               ], body_size=7.6, body_line=9.4)

    spacer(doc, 12)
    t = new_table(doc, [CONTENT_W], borders=False, pad=(240, 260, 280, 280))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=CARBON, borders={"left": ("single", 24, FLAME)})
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = Pt(9.4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "SEO Y METADATOS", font=INS, size=7.2, color=GOLD, caps=True, spacing=2.0)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(13.6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "title ≤ 60 caracteres  ·  meta description ≤ 155  ·  Open Graph 1200 × 630  ·  "
               "JSON-LD Person + SportsActivityLocation  ·  hreflang es-CO  ·  sitemap y "
               "robots  ·  canonical con dominio final.", font=IN, size=8.6, color=CREAM)


def build_cronograma(doc):
    sec_head(doc, "08", "Cronograma", ["DIEZ SEMANAS.", "CUATRO FASES."],
             "Un plan de diez semanas con un copy lock al final de la semana 2. Todo lo que "
             "viene después depende de esa aprobación: sin texto definitivo no hay diseño "
             "definitivo.", new_page=False)

    data_table(doc, [1.3, 0.8, 1.85, 1.6, 1.05],
               ["Fase", "Semanas", "Trabajo", "Entregables", "Hito"],
               [
                   ["01 · Dirección y contenido", "S1–S2", "Kickoff, auditoría de marca, "
                                                            "arquitectura de contenido, guion "
                                                            "final, wireframes",
                    "Mapa de contenido, wireframe, copy lock", "Aprobación de copy"],
                   ["02 · Diseño y dirección de arte", "S3–S5", "Sistema de diseño, UI desktop "
                                                                 "y mobile, retoque fotográfico, "
                                                                 "renders 3D, gráficos tácticos",
                    "Figma + style guide, assets finales", "Aprobación visual"],
                   ["03 · Construcción", "S6–S8", "Maquetación, animaciones, formulario, "
                                                  "analítica, CMS de testimonios",
                    "Staging navegable, QA, accesibilidad", "Aprobación de staging"],
                   ["04 · Lanzamiento y medición", "S9–S10", "QA cross-browser, performance, "
                                                             "SEO, publicación, tablero",
                    "Sitio en vivo, informe, plan de optimización", "Go live"],
               ], body_size=7.5, body_line=9.4)

    h3(doc, "Entregables del proyecto", before=16, after=6)
    data_table(doc, [2.4, 1.9, 2.3],
               ["Entregable", "Formato", "Fase"],
               [
                   ["Prototipo navegable (desktop y mobile)", "index.html + assets/", "03"],
                   ["Documento de propuesta", "DOCX + PDF", "00"],
                   ["Sistema de diseño y style guide", "Figma + PDF", "02"],
                   ["Piezas 3D y gráficos tácticos", "PNG con alfa, WebP, SVG", "02"],
                   ["Capturas de presentación", "PNG en preview/", "03"],
                   ["Tablero de medición y plan de optimización", "GA4 + informe", "04"],
               ], body_size=7.6, body_line=9.4)

    spacer(doc, 12)
    callout(doc, "La ruta crítica son dos fechas: el copy lock de la semana 2 y la aprobación "
                 "visual de la semana 5. Si alguna se mueve, el lanzamiento se mueve con ella. "
                 "El resto del cronograma está diseñado para absorber una semana de ajustes sin "
                 "tocar la fecha de go live.",
            kicker="Ruta crítica", accent=GOLD, dark=True, body_font=IN, body_size=9.6,
            body_line=14)

    h3(doc, "Equipo asignado", before=16, after=6)
    data_table(doc, [1.9, 2.2, 2.5],
               ["Rol", "Responsabilidad", "Dedicación"],
               [
                   ["Dirección de arte", "Concepto, sistema y fotografía", "Fase 1–2, 40 %"],
                   ["Diseño UI", "Interfaces y prototipo navegable", "Fase 2–3, 60 %"],
                   ["Front-end", "Maquetación, performance y accesibilidad", "Fase 3–4, 80 %"],
                   ["Copy y estrategia", "Guion, microcopy y CRO", "Fase 1 y 4, 30 %"],
                   ["Coach (cliente)", "Validación de contenido y testimonios", "Reuniones "
                                                                            "semanales"],
               ], body_size=7.6, body_line=9.6)


def build_cierre(doc):
    sec_head(doc, "09", "Próximos pasos", ["EL PRÓXIMO", "SALTO INICIAL."],
             "Tres movimientos y el proyecto está en marcha. La propuesta está pensada para "
             "aprobarse rápido: el concepto y el copy ya están resueltos; lo que sigue es "
             "producción.", new_page=False)

    callout(doc, "Concepto y copy  ·  Sistema de diseño y tipografía  ·  Dirección de arte y "
                 "assets  ·  Cronograma y fechas  ·  Firma de contacto",
            kicker="Checklist de aprobación · v1.0", accent=FLAME, dark=True,
            body_font=INS, body_size=11.0, body_line=15)

    h3(doc, "Lo que necesitamos de ti", before=18, after=6)
    treq = data_table(doc, [1.55, 3.6, 1.45],
                      ["Elemento", "Qué aporta", "Cuándo"],
                      [
                          ["Fotografías y video", "8–12 piezas reales, sin editar", "Semana 1"],
                          ["Testimonios y palmarés", "Tres citas y certificados a la vista",
                           "Semana 1"],
                          ["Accesos y dominio", "Hosting, dominio, Instagram y teléfono",
                           "Semana 2"],
                      ], body_size=7.8, body_line=9.8)
    keep_table_together(treq)

    spacer(doc, 26)
    steps = [
        ("01", "REVISAR ESTA PROPUESTA", "48 horas", "Lectura del documento y devolución con "
                                                       "comentarios. Sin costo."),
        ("02", "KICKOFF Y COPY LOCK", "Semana 1", "Reunión de arranque, ajuste de nombre y "
                                                  "biografía, validación del guion."),
        ("03", "DISEÑO Y CONSTRUCCIÓN", "Semanas 2–8", "Sistema, prototipo, desarrollo y QA "
                                                       "con revisiones semanales."),
    ]
    t = new_table(doc, [0.6, 2.05, 3.95], border_color=LINE_C, pad=(180, 180, 200, 200))
    for i, (num, title, when, text) in enumerate(steps):
        row = t.rows[0] if i == 0 else t.add_row()
        row_cant_split(row)
        c = row.cells[0]
        cell_fmt(c, fill=None)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(20)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, num, font=BDE, size=16, color=FLAME)
        c = row.cells[1]
        cell_fmt(c, fill=None)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(11)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, title, font=BDS, size=9.2, color=INK, caps=True, spacing=0.7)
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(9.4)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        add_run(p, when.upper(), font=INS, size=6.6, color=GOLD_D, caps=True, spacing=1.2)
        c = row.cells[2]
        cell_fmt(c, fill=None)
        cell_text(c, text, font=IN, size=8.6, color=SOFT, line=11.2)
    keep_table_together(t)

    spacer(doc, 18)
    # bloque de firma
    t = new_table(doc, [CONTENT_W], borders=False, pad=(360, 360, 380, 380))
    c = t.rows[0].cells[0]
    cell_fmt(c, fill=INK)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(10)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "FIRMA DE CONTACTO", font=INS, size=7.2, color=GOLD, caps=True, spacing=2.4)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(16)
    p.paragraph_format.line_spacing = Pt(28)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "COACH GLORIA CELIS", font=BDE, size=25, color=CREAM, spacing=-0.2)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(20)
    p.paragraph_format.line_spacing = Pt(12)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "Head Coach · Alto rendimiento femenino · Bogotá, Colombia", font=IN, size=9.0,
            color=MUTED)

    # línea de firma y datos
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(1)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p_borders(p, top=("single", 4, "3A3D43"))
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(14)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "lorisisabel22@gmail.com", font=INS, size=8.8, color=CREAM)
    add_run(p, "      ·      +57 298 5298", font=IN, size=8.8, color=CREAM)
    # handle de Instagram pendiente de confirmar con la coach

    spacer(doc, 22)
    # cierre conceptual: la big idea otra vez, ahora como despedida
    bar(doc, FLAME, 0.42, 3.2, before=0, after=12)
    p = para(doc, "", size=7.2, line=10, before=0, after=8)
    add_run(p, "NOS VEMOS EN LA CANCHA", font=INS, size=7.2, color=GOLD_D, caps=True,
            spacing=2.2)
    p = para(doc, "EL JUEGO SE GANA ANTES DEL SALTO INICIAL.", font=BDE, size=27, color=INK,
             line=27, before=0, after=8, spacing=-0.4)
    p = para(doc, "Gracias por la confianza. El diagnóstico inicial toma 30 minutos y no "
                  "cuesta nada: el resto es trabajo.", size=9.4, color=SOFT, line=14,
             right=0.6)

    spacer(doc, 12)
    # mock del CTA final, como aparece en la landing
    tcta = new_table(doc, [3.05, 0.22, 3.33], borders=False, pad=(0, 0, 0, 0))
    c = tcta.rows[0].cells[0]
    cell_fmt(c, fill=FLAME, valign=WD_ALIGN_VERTICAL.CENTER)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(13)
    p.paragraph_format.line_spacing = Pt(13)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "AGENDAR DIAGNÓSTICO GRATUITO", font=BD, size=11.6, color=INK, bold=True,
            caps=True, spacing=1.0)
    c = tcta.rows[0].cells[2]
    cell_fmt(c, fill=WARM, valign=WD_ALIGN_VERTICAL.CENTER)
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(9)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "ASÍ SE VE EL BOTÓN EN LA LANDING", font=INS, size=6.2, color=GOLD_D, caps=True,
            spacing=1.8)
    p = c.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = Pt(9.6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(p, "30 min · Sin costo · Cupos limitados", font=IN, size=7.4, color=SOFT)

    spacer(doc, 14)
    p = para(doc, "", size=8.0, color=SOFT, line=12.5)
    add_run(p, "Documento preparado en Bogotá, octubre de 2026. ", font=IN, size=7.8,
            color=SOFT)
    add_run(p, "El palmarés, los testimonios y los datos de contacto son demostrativos: el "
               "sistema está listo para incorporar la información real de la coach sin cambios "
               "estructurales.", font=IN, size=7.8, color=SOFT)


# ================================================================== ENSAMBLE
def setup_body_section(sec):
    sec.page_width = Inches(PAGE_W)
    sec.page_height = Inches(PAGE_H)
    sec.left_margin = Inches(MARGIN)
    sec.right_margin = Inches(MARGIN)
    sec.top_margin = Inches(1.02)
    sec.bottom_margin = Inches(0.82)
    sec.header_distance = Inches(0.46)
    sec.footer_distance = Inches(0.38)

    hdr = sec.header
    hdr.is_linked_to_previous = False
    for p in list(hdr.paragraphs):
        p._p.getparent().remove(p._p)
    ht = hdr.add_table(rows=1, cols=2, width=Inches(CONTENT_W))
    table_layout(ht, [4.85, 1.75], borders=False, pad=(0, 0, 0, 0))
    hl = ht.rows[0].cells[0]
    cell_fmt(hl, borders={"bottom": ("single", 4, "E7E2D7")}, pad=(0, 0, 30, 0))
    hp = hl.paragraphs[0]
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(0)
    hp.paragraph_format.line_spacing = Pt(11)
    hp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(hp, "■ ", font=BD, size=6.4, color=FLAME)
    add_run(hp, "GLORIA CELIS", font=BDS, size=7.4, color=INK, caps=True, spacing=1.6)
    add_run(hp, "  /  PROPUESTA DE LANDING PAGE", font=INS, size=6.4, color=SOFT, caps=True,
            spacing=1.4)
    hr = ht.rows[0].cells[1]
    cell_fmt(hr, borders={"bottom": ("single", 4, "E7E2D7")}, pad=(0, 0, 30, 0))
    hp2 = hr.paragraphs[0]
    hp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp2.paragraph_format.space_before = Pt(0)
    hp2.paragraph_format.space_after = Pt(0)
    hp2.paragraph_format.line_spacing = Pt(11)
    hp2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(hp2, "OCTUBRE 2026", font=INS, size=6.4, color=MUTED, caps=True, spacing=1.4)
    tail = hdr.add_paragraph()
    tail.paragraph_format.space_before = Pt(0)
    tail.paragraph_format.space_after = Pt(0)
    tail.paragraph_format.line_spacing = Pt(1)
    tail.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(tail, " ", font=IN, size=1, color=WHITE)

    ftr = sec.footer
    ftr.is_linked_to_previous = False
    for p in list(ftr.paragraphs):
        p._p.getparent().remove(p._p)
    ft = ftr.add_table(rows=1, cols=2, width=Inches(CONTENT_W))
    table_layout(ft, [4.85, 1.75], borders=False, pad=(0, 0, 0, 0))
    fl = ft.rows[0].cells[0]
    cell_fmt(fl, borders={"top": ("single", 4, "E7E2D7")}, pad=(30, 0, 0, 0))
    fp = fl.paragraphs[0]
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    fp.paragraph_format.line_spacing = Pt(11)
    fp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(fp, "DOCUMENTO CONFIDENCIAL · V1.0", font=INS, size=6.2, color=MUTED, caps=True,
            spacing=1.4)
    fr = ft.rows[0].cells[1]
    cell_fmt(fr, borders={"top": ("single", 4, "E7E2D7")}, pad=(30, 0, 0, 0))
    fp2 = fr.paragraphs[0]
    fp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp2.paragraph_format.space_before = Pt(0)
    fp2.paragraph_format.space_after = Pt(0)
    fp2.paragraph_format.line_spacing = Pt(11)
    fp2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(fp2, "PÁGINA ", font=INS, size=6.6, color=SOFT, caps=True, spacing=1.4)
    field(fp2, " PAGE ", font=BD, size=8.4, color=INK, bold=True)
    add_run(fp2, "  /  ", font=BD, size=7.4, color=MUTED)
    field(fp2, " NUMPAGES ", font=BD, size=8.4, color=SOFT, bold=True)
    tail = ftr.add_paragraph()
    tail.paragraph_format.space_before = Pt(0)
    tail.paragraph_format.space_after = Pt(0)
    tail.paragraph_format.line_spacing = Pt(1)
    tail.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    add_run(tail, " ", font=IN, size=1, color=WHITE)


def make_logo(path):
    from PIL import Image, ImageDraw, ImageFont
    size = 640
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, size - 1, size - 1], fill=(255, 77, 31, 255))
    f = ImageFont.truetype(os.path.join(WORK, "fonts", "barlow-condensed-800.ttf"), 340)
    bb = d.textbbox((0, 0), "GC", font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), "GC", font=f,
           fill=(244, 241, 233, 255))
    im.save(path)
    print("logo:", path)


def build(pages):
    make_logo(os.path.join(IMG, "doc_logo.png"))
    doc = Document()
    # elimina párrafos iniciales vacíos del template
    body_el = doc.element.body
    for p in body_el.findall(qn("w:p")):
        body_el.remove(p)

    sec1 = doc.sections[0]
    band = build_cover(doc, sec1)
    # portada termina aquí: copia el sectPr de portada dentro del párrafo de la franja
    sect_copy = copy.deepcopy(sec1._sectPr)
    band._p.get_or_add_pPr().append(sect_copy)

    # segunda sección: cuerpo
    setup_body_section(sec1)

    build_carta(doc)
    build_index(doc, pages)
    build_concepto(doc)
    build_concepto2(doc)
    build_arquitectura(doc)
    build_sistema(doc)
    build_sistema_tipo(doc)
    build_sistema_grid(doc)
    build_direccion(doc)
    build_direccion3d(doc)
    build_direccion2d(doc)
    build_copy(doc)
    build_copy2(doc)
    build_cro(doc)
    build_tecnica(doc)
    build_cronograma(doc)
    build_cierre(doc)

    cp = doc.core_properties
    cp.title = "Propuesta de landing page — Coach Gloria Celis"
    cp.subject = "Concepto creativo, sistema de diseño, dirección de arte, copy y CRO"
    cp.author = "Estudio de diseño editorial y marca"
    cp.keywords = "landing page, básquetbol, alto rendimiento, propuesta de diseño"

    doc.save(OUT_DOCX)
    print("saved:", OUT_DOCX)
    return OUT_DOCX


if __name__ == "__main__":
    PAGES = {"01": "4", "02": "6", "03": "8", "04": "11", "05": "14", "06": "16",
             "07": "17", "08": "18", "09": "19"}
    build(PAGES)


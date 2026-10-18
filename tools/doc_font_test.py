# -*- coding: utf-8 -*-
"""Prueba rápida: confirma que LibreOffice ve las fuentes locales y la página oscura."""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_work", "fonttest.docx")
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, m, Inches(0))

def shade(el, hexcolor):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    el.append(shd)

t = doc.add_table(rows=1, cols=1)
t.autofit = False
cell = t.cell(0, 0)
cell.width = Inches(8.5)
shade(cell._tc.get_or_add_tcPr(), "0A0B0D")
row = t.rows[0]
trPr = row._tr.get_or_add_trPr()
h = OxmlElement("w:trHeight"); h.set(qn("w:val"), str(int(11 * 1440))); h.set(qn("w:hRule"), "exact")
trPr.append(h)

tests = [
    ("Barlow Condensed", 700, "EL JUEGO SE GANA ANTES DEL SALTO INICIAL.", 40),
    ("Barlow Condensed ExtraBold", None, "Barlow Condensed ExtraBold 800 · MAYÚSCULAS", 22),
    ("Barlow Condensed SemiBold", None, "Barlow Condensed SemiBold 600", 18),
    ("Barlow Condensed Medium", None, "Barlow Condensed Medium 500", 18),
    ("Inter", 400, "Inter 400 — Formo jugadoras que leen el juego, lideran bajo presión.", 11),
    ("Inter", 700, "Inter 700 — AGENDAR DIAGNÓSTICO GRATUITO", 11),
    ("Inter SemiBold", None, "Inter SemiBold 600 — BASKETBALL COACH · ALTO RENDIMIENTO", 9),
    ("Inter Medium", None, "Inter Medium 500 — cuerpo secundario 16 px", 10),
]
p0 = cell.paragraphs[0]
for i, (name, bold, text, size) in enumerate(tests):
    p = p0 if i == 0 else cell.add_paragraph()
    r = p.add_run(text)
    r.font.name = name
    r.font.size = Pt(size)
    if bold:
        r.font.bold = True
    r.font.color.rgb = RGBColor(0xF4, 0xF1, 0xE9)
    r._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    r._element.rPr.rFonts.set(qn("w:cs"), name)

doc.save(OUT)
print("saved", OUT)

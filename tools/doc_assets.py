# -*- coding: utf-8 -*-
"""Genera assets derivados para el documento de propuesta (prefijo doc_):
- tratamientos de fotografÃ­a (color documento / blanco y negro archivo)
- diagrama tÃ¡ctico 2D de ejemplo (estilo de los grÃ¡ficos de la landing)
- muestras de la retÃ­cula de 12 columnas
"""
import os, math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
WORK = os.path.join(ROOT, "tools", "doc_work")
OUT = os.path.join(WORK, "img")
os.makedirs(OUT, exist_ok=True)

FONT_DIR = os.path.join(WORK, "fonts")
INB = ImageFont.truetype(os.path.join(FONT_DIR, "barlow-condensed-700.ttf"), 40)
INB_XL = ImageFont.truetype(os.path.join(FONT_DIR, "barlow-condensed-800.ttf"), 92)
IN_M = ImageFont.truetype(os.path.join(FONT_DIR, "inter-500.ttf"), 24)

# ---------------------------------------------------------------- fotografÃ­a
def treat_color(im):
    im = im.convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(0.90)
    im = ImageEnhance.Brightness(im).enhance(0.97)
    return im

def treat_bw(im):
    im = im.convert("L").convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.28)
    # grano fino tipo pelÃ­cula
    noise = Image.effect_noise(im.size, 14).convert("L")
    im = Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.045)
    return im

def save(im, name, quality=92):
    out = os.path.join(OUT, name)
    im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"  {name}: {im.size} {os.path.getsize(out)//1024} KB")

def area(im, w, h, anchor="center"):
    """Recorte centrado al ratio pedido sin deformar."""
    tw, th = w / h, im.width / im.height
    if th > tw:  # recortar a los lados
        nw = int(im.height * tw)
        x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / tw)
        y = 0 if anchor == "top" else (im.height - nh) // 2
        im = im.crop((0, y, im.width, y + nh))
    return im

print("== FotografÃ­a ==")
hero = Image.open(os.path.join(IMG, "coach-hero.jpg"))
save(treat_color(area(hero, 4, 5, "top")), "doc-hero-retrato.jpg")
equipo = Image.open(os.path.join(IMG, "equipo-campeon.jpg"))
save(treat_color(area(equipo, 4, 3)), "doc-equipo-color.jpg")
save(treat_bw(area(equipo, 4, 3)), "doc-equipo-bw.jpg")
trofeo = Image.open(os.path.join(IMG, "coach-trofeo.jpg"))
save(treat_bw(area(trofeo, 3, 4)), "doc-trofeo-bw.jpg")
clinica = Image.open(os.path.join(IMG, "coach-clinica.jpg"))
save(treat_bw(area(clinica, 3, 4)), "doc-clinica-bw.jpg")
save(treat_color(area(clinica, 3, 4)), "doc-clinica-color.jpg")

# ---------------------------------------------------------------- tÃ¡ctico 2D
W, H = 1900, 1120
CREAM = (246, 242, 232)
INK = (10, 11, 13)
FLAME = (255, 77, 31)
GOLD = (233, 180, 76)
STEEL = (26, 29, 34)

canvas = Image.new("RGBA", (W, H), CREAM + (255,))
d = ImageDraw.Draw(canvas, "RGBA")

# textura de cancha: lÃ­neas al 8 %
court = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(court)
L, T, R, B = 150, 90, W - 90, H - 90
line = (INK[0], INK[1], INK[2], 34)
cd.rectangle([L, T, R, B], outline=line, width=5)
# media cancha: aro a la izquierda
key_w, key_h = 470, 380
cy = (T + B) // 2
cd.rectangle([L, cy - key_h // 2, L + key_w, cy + key_h // 2], outline=line, width=5)
cd.arc([L + key_w - 230, cy - 230, L + key_w + 230, cy + 230], -90, 90, fill=line, width=5)
cd.arc([L - 40, cy - 40, L + 40, cy + 40], 0, 360, fill=line, width=5)
# arco de tres (desde el aro)
cd.arc([L + 40, cy - 430, L + 40 + 860, cy + 430], -78, 78, fill=line, width=5)
# lÃ­nea de fondo del lado derecho + cÃ­rculo central recortado
cd.line([R, T, R, B], fill=line, width=5)
cd.arc([R - 260, cy - 260, R, cy + 260], 90, 270, fill=line, width=5)
canvas.alpha_composite(court)

def dash(pts, color, width=6, dash=22, gap=16):
    """PoliÃ­nia discontinua con punta de flecha."""
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        seg = math.hypot(x2 - x1, y2 - y1)
        if not seg:
            continue
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        t = 0.0
        while t < seg:
            t2 = min(t + dash, seg)
            d.line([(x1 + ux * t, y1 + uy * t), (x1 + ux * t2, y1 + uy * t2)], fill=color, width=width)
            t += dash + gap
    # punta
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (+1, -1):
        a = ang + s * math.radians(158)
        d.line([(x2, y2), (x2 + 26 * math.cos(a), y2 + 26 * math.sin(a))], fill=color, width=width)

def player(x, y, num, fill=FLAME, r=44):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill + (255,))
    d.ellipse([x - r, y - r, x + r, y + r], outline=CREAM + (255,), width=5)
    f = ImageFont.truetype(os.path.join(FONT_DIR, "barlow-condensed-800.ttf"), 48)
    tw = d.textlength(str(num), font=f)
    d.text((x - tw / 2, y - 30), str(num), font=f, fill=CREAM + (255,))

def defender(x, y, r=30):
    d.line([x - r, y - r, x + r, y + r], fill=(90, 96, 104, 235), width=8)
    d.line([x - r, y + r, x + r, y - r], fill=(90, 96, 104, 235), width=8)

# 1-4 flat: jugadoras y defensas
P = {1: (250, cy - 10), 2: (760, 250), 3: (760, cy + 10), 4: (1120, 240), 5: (1430, cy - 40)}
D = {1: (430, cy - 20), 2: (880, 285), 3: (860, cy + 30), 4: (1250, 300), 5: (1330, cy + 260)}
for k, (x, y) in D.items():
    defender(x, y)
for k, (x, y) in P.items():
    player(x, y, k)

# cortes (oro discontinuo) y bloqueo (lÃ­nea recta)
dash([(760, 250), (1060, 430), (1290, cy + 420)], GOLD + (245,))
dash([(1120, 240), (870, 430), (620, cy + 330)], GOLD + (245,))
dash([(1430, cy - 40), (1330, cy + 120)], GOLD + (245,))
d.line([(680, 300), (690, 470)], fill=STEEL + (255,), width=8)  # bloqueo
d.ellipse([680, 470, 700, 490], fill=STEEL + (255,))

# etiquetas de estilo
d.text((L + 6, 26), "1-4 FLAT  /  CORTE EN L  /  LECTURA DEL ESPACIO", font=IN_M, fill=(10, 11, 13, 150))
d.text((W - 330, H - 52), "MOVIMIENTO Â· ORO", font=ImageFont.truetype(os.path.join(FONT_DIR, "inter-600.ttf"), 22), fill=(233, 180, 76, 255))

out = os.path.join(OUT, "doc-tactico-2d.png")
canvas.convert("RGB").save(out, "PNG", optimize=True)
print(f"  doc-tactico-2d.png: {canvas.size} {os.path.getsize(out)//1024} KB")
print("OK")


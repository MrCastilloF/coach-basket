# -*- coding: utf-8 -*-
"""Extrae el TrueType embebido de los EOT servidos por Google Fonts (endpoint legado).
Los .ttf resultantes se instalan por usuario para que LibreOffice los use al exportar."""
import os, struct, shutil

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_work")
OUT = os.path.join(WORK, "fonts")
os.makedirs(OUT, exist_ok=True)

def sfnt_ok(b):
    if len(b) < 12:
        return False
    ver, num = struct.unpack(">IH", b[:6])
    return ver in (0x00010000, 0x4F54544F, 0x74727565) and 4 <= num <= 40

for name in sorted(os.listdir(WORK)):
    if not name.endswith(".ttf"):
        continue
    path = os.path.join(WORK, name)
    b = open(path, "rb").read()
    if sfnt_ok(b):
        dst = os.path.join(OUT, name)
        shutil.copyfile(path, dst)
        print(f"{name}: ya era sfnt ({len(b)} bytes)")
        continue
    eot_size, font_size = struct.unpack("<II", b[:8])
    target = dst = os.path.join(OUT, name)
    for off in (len(b) - font_size, 82, 228):
        if off < 0 or off >= len(b):
            continue
        cand = b[off:]
        if sfnt_ok(cand):
            open(target, "wb").write(cand)
            print(f"{name}: EOT({len(b)}) -> sfnt desde offset {off} ({len(cand)} bytes)")
            break
    else:
        print(f"{name}: NO se pudo extraer")

# Verificación: lee la tabla name para confirmar familia y estilo
def read_names(b):
    ver, num = struct.unpack(">IH", b[:6])
    tables = {}
    for i in range(num):
        tag, chk, off, ln = struct.unpack(">4sIII", b[12 + 16 * i: 28 + 16 * i])
        tables[tag.decode("latin1")] = (off, ln)
    off, ln = tables["name"]
    fmt, count, str_off = struct.unpack(">HHH", b[off:off + 6])
    names = {}
    for i in range(count):
        pid, eid, lid, nid, l, o = struct.unpack(">HHHHHH", b[off + 6 + 12 * i: off + 18 + 12 * i])
        raw = b[off + str_off + o: off + str_off + o + l]
        try:
            txt = raw.decode("utf-16-be") if pid in (0, 3) else raw.decode("latin1")
        except Exception:
            txt = repr(raw)
        if nid in (1, 2, 4, 6):
            names.setdefault(nid, txt)
    return names

print("\n== Verificación de familias ==")
for name in sorted(os.listdir(OUT)):
    b = open(os.path.join(OUT, name), "rb").read()
    n = read_names(b)
    print(f"{name}: family={n.get(1)!r} style={n.get(2)!r} full={n.get(4)!r} ps={n.get(6)!r}")

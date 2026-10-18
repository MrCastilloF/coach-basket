# -*- coding: utf-8 -*-
"""Rebrand del documento: Coach Mariana Vélez -> Coach Gloria Celis (solo identidad)."""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "doc_build.py")

pairs = [
    ("Mariana Vélez", "Gloria Celis"),
    ("MARIANA VÉLEZ", "GLORIA CELIS"),
    ("Mariana:", "Gloria:"),
    ("marianavelez", "gloriacelis"),
    ('"MV"', '"GC"'),
]

s = io.open(SRC, "r", encoding="utf-8").read()
before = s
for a, b in pairs:
    s = s.replace(a, b)
io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)

print("reemplazos aplicados:", sum(before.count(a) for a, _ in pairs))
for token in ("Mariana", "MARIANA", "marianavelez", '"MV"'):
    n = len(re.findall(re.escape(token), s))
    print(f"  quedan {token!r}: {n}")
print("GC en logo:", s.count('"GC"'), "| Gloria Celis:", s.count("Gloria Celis"),
      "| GLORIA CELIS:", s.count("GLORIA CELIS"))

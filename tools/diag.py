# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const out = {fonts: [...document.fonts].map(f => f.family + ' | ' + f.weight + ' | ' + f.status)};
  const c = document.createElement('canvas').getContext('2d');
  c.font = '800 100px "Barlow Condensed"'; out.wCond = c.measureText('HHHHHHHHHH').width;
  c.font = '800 100px "Bahnschrift"';      out.wBahn = c.measureText('HHHHHHHHHH').width;
  c.font = '800 100px sans-serif';         out.wSans = c.measureText('HHHHHHHHHH').width;
  const h = document.querySelector('.hero__title'); const cs = getComputedStyle(h);
  out.h1 = {font: cs.fontFamily, size: cs.fontSize, lh: cs.lineHeight,
            w: h.getBoundingClientRect().width, hh: h.getBoundingClientRect().height};
  const el = document.querySelector('.brand__name'); const cs2 = getComputedStyle(el);
  out.brand = {font: cs2.fontFamily, size: cs2.fontSize, w: el.getBoundingClientRect().width, display: cs2.display};
  out.bodyFont = getComputedStyle(document.body).fontFamily;
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://127.0.0.1:8899/index.html")
    pg.wait_for_load_state("load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(800)
    print(pg.evaluate(JS))
    b.close()

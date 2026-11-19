#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rose Frond Theme — flat vector logo candidates (SVG, headless Chromium).

Style: **flat** — solid fills only, no gradients, no highlights, no outlines.
Two or three shapes per mark, built around a frond (the reference art's palm
leaf) rather than another generic flower.

The palette is all pale, so every mark includes a deep-rose or deep-ink element
to stay legible on both the rose frame and the petal-white page.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


ROSE = hx(_C["frame"])                             # #F59BC1
PINK = hx(_C["toolbar"])                           # #FFCED6
PETAL = hx(_C["ntp_background"])                   # #FFF9F9
MINT = hx(_C["button_background"])                 # #B2F1B3
PALEMINT = hx(_C["button_background_secondary"])   # #D9FED6
INK = hx(_C["ntp_text"])                           # #4A2B3C
DEEP = hx(_C["ntp_link"])                          # #A8477A


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s<g transform="translate(128 128) scale(0.94) '
            'translate(-128 -128)">%s</g></svg>' % (CELL, CELL, defs, body))


def circle(cx, cy, r, fill):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, fill)


def frond(x0, y0, x1, y1, leaflets, size, fill, curve=26):
    """A single flat frond: curved stem with paired leaflets along the tangent."""
    cx, cy = (x0 + x1) / 2 + curve, (y0 + y1) / 2 - abs(curve) * 0.5

    def point(t):
        u = 1 - t
        return (u * u * x0 + 2 * u * t * cx + t * t * x1,
                u * u * y0 + 2 * u * t * cy + t * t * y1)

    out = ['<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
           'stroke-width="6" stroke-linecap="round"/>'
           % (x0, y0, cx, cy, x1, y1, fill)]
    for i in range(leaflets):
        t = 0.14 + 0.76 * i / max(1, leaflets - 1)
        px, py = point(t)
        qx, qy = point(min(1.0, t + 0.02))
        a = math.degrees(math.atan2(qy - py, qx - px))
        rx = size * (1 - 0.42 * t)
        ry = rx * 0.44
        for side in (-1, 1):
            ox = px - math.sin(math.radians(a)) * rx * side * 0.9
            oy = py + math.cos(math.radians(a)) * rx * side * 0.9
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
                       'transform="rotate(%.1f %.1f %.1f)"/>'
                       % (ox, oy, rx, ry, fill, a + side * 50, ox, oy))
    return "".join(out)


def leaf(cx, cy, length, width, angle, fill):
    half = length * 0.5
    d = ("M0 0 C %.1f %.1f %.1f %.1f 0 %.1f C %.1f %.1f %.1f %.1f 0 0 Z"
         % (width, -half * 0.55, width * 0.86, -half * 1.25, -length,
            -width * 0.86, -half * 1.25, -width, -half * 0.55))
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)"><path d="%s" fill="%s"/></g>'
            % (cx, cy, angle, d, fill))


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
%s
%s
""" % (circle(128, 128, 96, PETAL),
       frond(70, 206, 186, 62, 6, 26, DEEP, curve=34)))

SVG_02 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, ROSE),
       frond(72, 198, 184, 78, 5, 22, INK, curve=28),
       frond(184, 198, 86, 92, 4, 18, PETAL, curve=-28)))

SVG_03 = svg_open("""
%s
%s
%s
%s
""" % (circle(128, 128, 96, PETAL),
       leaf(128, 196, 116, 42, 0, DEEP),
       leaf(128, 196, 104, 38, -48, ROSE),
       leaf(128, 196, 104, 38, 48, ROSE)))

SVG_04 = svg_open("""
%s
%s
""" % (circle(128, 128, 96, ROSE),
       frond(78, 196, 180, 70, 6, 24, MINT, curve=30)))

SVG_05 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, PETAL),
       frond(70, 190, 182, 86, 5, 21, DEEP, curve=30),
       frond(186, 190, 96, 108, 4, 18, ROSE, curve=-30)))

SVG_06 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, INK),
       frond(80, 192, 178, 74, 5, 23, ROSE, curve=28),
       circle(166, 92, 14, MINT)))

CANDIDATES = [
    ("01", "frond-spray", "One deep-rose frond on petal white", SVG_01),
    ("02", "twin-frond", "Two crossing fronds on a rose disc", SVG_02),
    ("03", "leaf-fan", "Three leaves fanning from one base", SVG_03),
    ("04", "mint-frond", "Mint frond on a rose disc — most colour contrast", SVG_04),
    ("05", "frond-pair", "Two fronds on petal white — softest", SVG_05),
    ("06", "ink-frond", "Rose frond on deep ink — strongest at 32px", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), PETAL)
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=INK)
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, PETAL, INK, (170, 120, 145),
                  CAND_DIR / "contact-light.png", "Rose Frond — flat candidates (petal)")
    contact_sheet(rendered, ROSE, PETAL, (190, 120, 155),
                  CAND_DIR / "contact-dark.png", "Rose Frond — candidates on the rose frame")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()

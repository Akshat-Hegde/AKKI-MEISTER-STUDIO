"""Outline Saira (variable, Google Fonts) to SVG paths at any width/weight, upright or italic."""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

BASE = r"C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/@fontsource-variable/saira/files/"
_cache = {}


def font(wght=900, wdth=125, italic=True):
    key = (wght, wdth, italic)
    if key not in _cache:
        f = TTFont(BASE + ("saira-latin-wdth-italic.woff2" if italic else "saira-latin-wdth-normal.woff2"))
        _cache[key] = instantiateVariableFont(f, {"wght": wght, "wdth": wdth})
    return _cache[key]


def outline(text, size, wght=900, wdth=125, italic=True, track=0.0, kern=None):
    """(path_d, advance_width, cap_height) for text; baseline at y=0, y grows downward in SVG"""
    f = font(wght, wdth, italic)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    sc = size / upm
    pen = SVGPathPen(gs)
    x = 0.0
    for i, ch in enumerate(text):
        g = cmap.get(ord(ch))
        if g is None:
            continue
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, 0)))
        x += hmtx[g][0] * sc + track * size + ((kern or {}).get(i, 0) * size)
    cap = f["OS/2"].sCapHeight * sc
    return pen.getCommands(), x - track * size, cap


def bounds(text, size, **kw):
    f = font(kw.get("wght", 900), kw.get("wdth", 125), kw.get("italic", True))
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    sc = size / f["head"].unitsPerEm
    bp = BoundsPen(gs)
    x = 0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(bp, (sc, 0, 0, -sc, x, 0)))
        x += hmtx[g][0] * sc + kw.get("track", 0) * size
    return bp.bounds


def svg_text(text, height_px, color, wght=900, wdth=125, italic=True, track=0.0, style=""):
    """inline svg sized to cap height = height_px"""
    d, w, cap = outline(text, 100, wght, wdth, italic, track)
    b = bounds(text, 100, wght=wght, wdth=wdth, italic=italic, track=track)
    s = height_px / cap
    x0, y0, x1, y1 = b
    W = (x1 - x0) * s
    Hh = (y1 - y0) * s
    return (f'<svg width="{W:.1f}" height="{Hh:.1f}" viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" style="display:block;overflow:visible;{style}">'
            f'<path fill="{color}" d="{d}"/></svg>')


if __name__ == "__main__":
    rows = []
    for t, wg, wd, it in (("AKKI MEISTER", 900, 125, True), ("AKKI MEISTER", 800, 125, False), ("RACE DAY", 900, 62, True), ("AM AM AM", 900, 125, True), ("MOTORSPORT · PERFORMANCE", 400, 125, False)):
        rows.append(svg_text(t, 70, "#0b0b0e", wg, wd, it, 0.02 if wd < 100 else 0.0))
    html = "<html><body style='background:#eee;padding:30px;display:flex;flex-direction:column;gap:30px'>" + "".join(rows) + "</body></html>"
    open("../round4/saira-test.html", "w").write(html)
    print("ok")

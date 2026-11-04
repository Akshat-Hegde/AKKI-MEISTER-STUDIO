"""Colour iterations on the locked ///AM: fades, multicolour (livery-inspired) bars, coloured outlines."""
import tune
from tune import add, V, NIGHT, ICE, RED, ORANGE, BLUE, STEEL, YEL

TEAL, GOLD, PAPAYA, GULF_B, GULF_O, NAVY, MARTINI_L, SAFFRON, GREEN, MAG = "#00D2BE", "#D4AF37", "#FF8000", "#6CB4E4", "#F47A20", "#1B2A6B", "#5BB8E8", "#FF9933", "#138808", "#E6007E"
del V[:]
# bars listed: [next to A, middle, outermost]
FADES = [("red", RED), ("orange", ORANGE), ("cobalt", BLUE), ("teal", TEAL), ("gold", GOLD), ("steel", STEEL)]
MULTI = [
    ("tyres", "Tyre compounds", [RED, YEL, None]),
    ("heat", "Heat: red to orange to yellow", [RED, ORANGE, YEL]),
    ("india", "Saffron, white, green", [GREEN, None, SAFFRON]),
    ("gulf", "Gulf livery", [GULF_O, GULF_B, GULF_B]),
    ("martini", "Martini stripes", [RED, MARTINI_L, NAVY]),
    ("papaya", "Papaya + cobalt", [PAPAYA, BLUE, PAPAYA]),
    ("bull", "Navy, red, yellow", [RED, YEL, NAVY]),
    ("silver", "Silver arrows: teal, steel", [TEAL, STEEL, STEEL]),
    ("rgb", "Red, ice, cobalt", [RED, None, BLUE]),
    ("ice-red", "Red bar leads, rest neutral", [RED, None, None]),
]
for bg, tag, fg in ((NIGHT, "d", ICE), (ICE, "l", fg if False else NIGHT)):
    fg = ICE if tag == "d" else NIGHT
    for n, c in FADES:
        add(f"{tag}-fade-{n}", f"Fade {n}", fg, [(c, 1), (c, .55), (c, .25)], bg)
    add(f"{tag}-fade-heat", "Fade heat", fg, [(RED, 1), (ORANGE, .7), (YEL, .45)], bg)
    for n, title, cols in MULTI:
        add(f"{tag}-multi-{n}", title, fg, [c or fg for c in cols], bg)
    for n, c in (("red", RED), ("orange", ORANGE), ("cobalt", BLUE), ("teal", TEAL), ("gold", GOLD)):
        add(f"{tag}-ol-{n}", f"Outline {n}", fg, [c] * 3, bg, bar_stroke=True, sw=1.0, cutw=0.06)
    add(f"{tag}-ol-heat", "Outline heat", fg, [RED, ORANGE, YEL], bg, bar_stroke=True, sw=1.0, cutw=0.06)
    add(f"{tag}-ol-martini", "Outline martini", fg, [RED, MARTINI_L, NAVY if tag == "l" else ICE], bg, bar_stroke=True, sw=1.0, cutw=0.06)
    add(f"{tag}-ol-tyres", "Outline tyres", fg, [RED, YEL, fg], bg, bar_stroke=True, sw=1.0, cutw=0.06)
print(len(V))

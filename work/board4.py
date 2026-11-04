"""AKKI MEISTER round 4: professional brand board + social templates, in the Verstappen/Red Bull sim racing register.
Writes ../round4/system.html; snap4.js screenshots every top-level [data-snap]."""
import re, math
import saira

R4 = "../round4/"
A = "file:///C:/Users/admin/Akki-Portfolio-main/brag-output-2026-10-12-233528/work/assets/"
F = "file:///C:/Users/admin/Akki-Portfolio-main/akki-meister-logos/work/node_modules/@fontsource-variable/"
MID, NAVY, RED, ICE, STEEL, LINE = "#06070B", "#0C1530", "#E10A23", "#F4F5F7", "#8C93A3", "rgba(244,245,247,.12)"


def inner(name):
    s = open(R4 + name + ".svg").read()
    s = s[s.index("</title>") + 8: s.rindex("</svg>")]
    return re.sub(r'<rect width="256" height="256"[^>]*/>', "", s)


MK = {k: inner(k) for k in ("m1-fusion-rev", "m1-fusion-black", "m2-fusion-bar-rev", "m2-fusion-bar-color", "m3-crest-rev", "m3-crest-black", "m1-fusion-color", "m3-crest-color")}


def mark(k, w, fg=None, style=""):
    s = MK[k]
    if fg:
        s = s.replace(f'fill="{ICE}"', f'fill="{fg}"').replace('fill="#06070B"', f'fill="{fg}"')
    return f'<svg viewBox="0 0 256 256" width="{w}" height="{w}" style="display:block;{style}">{s}</svg>'


def wm(h, col=ICE, text="AKKI MEISTER", wght=900, wdth=125, italic=True, track=0.0):
    return saira.svg_text(text, h, col, wght, wdth, italic, track)


def lockup(h, col=ICE, sub=STEEL, k="m1-fusion-rev"):
    m = mark(k, h * 1.9, fg=col if col != ICE else None, style=f"margin:{-h * .45:.0f}px {-h * .25:.0f}px")
    return (f'<div style="display:flex;align-items:center;gap:{h * .55:.0f}px">{m}'
            f'<div style="display:flex;flex-direction:column;gap:{h * .32:.0f}px">{wm(h * .62, col)}{wm(h * .17, sub, "MOTORSPORT · PERFORMANCE", 500, 125, False, 0.32)}</div></div>')


def contour(w, h, col="rgba(244,245,247,.07)", n=6, x=0.62, sw=1.5):
    g = "".join(f'<path d="M{-s * .35:.0f} {-s:.0f} L{s * .5:.0f} 0 L{-s * .35:.0f} {s:.0f}" fill="none" stroke="{col}" stroke-width="{sw}"/>' for s in [180 + i * 120 for i in range(n)])
    return f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0"><g transform="translate({w * x:.0f} {h * .5:.0f})">{g}</g></svg>'


def slit(w, h=6, col=RED):
    k = math.tan(math.radians(12))
    return f'<svg width="{w}" height="{h}" style="display:block"><polygon points="{h * k:.1f},0 {w},0 {w - h * k:.1f},{h} 0,{h}" fill="{col}"/></svg>'


def graded(src, w, h, pos="50% 50%", extra=""):
    """cool monochrome grade: grayscale → navy multiply → black lift"""
    return (f'<div style="position:absolute;width:{w}px;height:{h}px;overflow:hidden;{extra}">'
            f'<img src="{A}{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};filter:grayscale(1) contrast(1.3) brightness(1.02)"/>'
            f'<div style="position:absolute;inset:0;background:{NAVY};mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 30%,rgba(120,150,255,.16),transparent 60%)"></div></div>')


def kicker(t, col=STEEL, size=13):
    return f'<div class="kick" style="color:{col};font-size:{size}px">{t}</div>'


def mono(t, col=STEEL, size=13):
    return f'<div class="mono" style="color:{col};font-size:{size}px">{t}</div>'


def partner_bar(w, col=STEEL):
    slots = "".join(f'<div class="kick" style="color:{col};opacity:.55;font-size:13px;letter-spacing:.3em">PARTNER</div>' for _ in range(4))
    return f'<div style="width:{w}px;border-top:1px solid {LINE};padding-top:26px;display:flex;justify-content:space-between;align-items:center">{slots}</div>'


def head(n, t):
    return (f'<div style="position:absolute;left:64px;top:52px;right:64px;display:flex;justify-content:space-between;align-items:center;z-index:9">'
            f'<div style="display:flex;gap:18px;align-items:center">{kicker(n, RED, 12)}{kicker(t, ICE, 12)}</div>{kicker("AKKI MEISTER · IDENTITY SYSTEM", STEEL, 12)}</div>')


# ------------------------------------------------------------------ templates (full size)
def t_raceday():
    return f'''<div class="tpl" data-snap="post-race-day" style="width:1080px;height:1350px;background:{MID}">
      {graded("williams.jpg", 1080, 1350, "45% 40%")}
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,{MID}f2 0%,{MID}66 22%,transparent 40%,{MID}aa 62%,{MID} 86%)"></div>
      {contour(1080, 1350, "rgba(225,10,35,.35)", 5, .78, 2)}
      <div style="position:absolute;left:80px;top:80px;right:80px;display:flex;justify-content:space-between;align-items:center">{mark("m1-fusion-rev", 92, style="margin:-20px")}{mono("RND 05 / 12", ICE, 18)}</div>
      <div style="position:absolute;left:76px;top:690px">
        <div class="cond" style="font-size:210px;line-height:.82;color:{ICE}">RACE<br/>DAY</div>
        <div style="margin:34px 0 22px">{slit(300, 8)}</div>
        <div class="exp" style="font-size:34px;color:{ICE}">GT3 SPRINT · SPA-FRANCORCHAMPS</div>
        <div style="display:flex;gap:40px;margin-top:18px">{mono("LIGHTS OUT 20:30 IST", STEEL, 19)}{mono("LIVE ON TWITCH", RED, 19)}</div></div>
      <div style="position:absolute;left:80px;bottom:70px">{partner_bar(920)}</div>
    </div>'''


def t_result():
    return f'''<div class="tpl" data-snap="post-result" style="width:1080px;height:1350px;background:{MID}">
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 75% 35%,{NAVY} 0%,{MID} 65%)"></div>
      {graded("podium-p1-jeddah.jpg", 600, 1350, "48% 30%", "right:0;top:0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 45%)")}
      <div style="position:absolute;left:80px;top:80px">{mark("m1-fusion-rev", 92, style="margin:-20px")}</div>
      <div style="position:absolute;left:72px;top:250px" class="cond"><span style="font-size:470px;line-height:.8;color:{RED}">P1</span></div>
      <div style="position:absolute;left:80px;top:720px">{kicker("RESULT · ROUND 03", STEEL, 18)}
        <div class="exp" style="font-size:66px;color:{ICE};margin-top:18px;line-height:1">JEDDAH</div>
        <div class="exp" style="font-size:24px;color:{STEEL};margin-top:10px;font-weight:600">RACEATWILL F1 · 2025</div></div>
      <div style="position:absolute;left:80px;top:1010px;width:920px;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid {LINE}">
        {"".join(f'<div style="padding-top:24px">{kicker(k, STEEL, 13)}<div class="mono" style="font-size:40px;color:{c};margin-top:12px">{v}</div></div>' for k, v, c in (("FASTEST LAP", "1:26.004", ICE), ("GAP TO P2", "+2.418", ICE), ("START", "P1", RED)))}</div>
      <div style="position:absolute;left:80px;bottom:62px">{mono("TEMPLATE · NUMBERS ARE PLACEHOLDERS", "#2c3140", 12)}</div>
    </div>'''


def t_driver():
    return f'''<div class="tpl" data-snap="post-driver" style="width:1080px;height:1350px;background:{MID}">
      {graded("suit-full.jpg", 1080, 1350, "50% 22%")}
      <div style="position:absolute;inset:0;background:linear-gradient(90deg,{MID} 0%,{MID}cc 30%,transparent 62%),linear-gradient(0deg,{MID} 0%,transparent 40%)"></div>
      <div class="cond" style="position:absolute;right:-30px;top:110px;font-size:640px;line-height:.8;color:transparent;-webkit-text-stroke:2px rgba(244,245,247,.18)">45</div>
      <div style="position:absolute;left:80px;top:80px">{mark("m3-crest-rev", 120, style="margin:-24px")}</div>
      <div style="position:absolute;left:80px;top:760px">{kicker("DRIVER · SIM / KART / FS", RED, 18)}
        <div class="exp" style="font-size:84px;color:{ICE};line-height:.95;margin-top:24px">AKSHAT<br/>HEGDE</div>
        <div style="margin:30px 0">{slit(240, 7)}</div>
        <div style="display:grid;grid-template-columns:auto auto auto;gap:60px">
          {"".join(f'<div>{kicker(k, STEEL, 13)}<div class="mono" style="font-size:30px;color:{ICE};margin-top:10px">{v}</div></div>' for k, v in (("NUMBER", "#45"), ("BASE", "BENGALURU"), ("SINCE", "2020")))}</div></div>
      <div style="position:absolute;left:80px;bottom:70px">{partner_bar(920)}</div>
    </div>'''


def t_story():
    return f'''<div class="tpl" data-snap="story-race-day" style="width:1080px;height:1920px;background:{MID}">
      {graded("kart-start.jpg", 1080, 1920, "55% 50%")}
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,{MID} 0%,{MID}99 25%,transparent 45%,{MID}cc 70%,{MID} 90%)"></div>
      {contour(1080, 1920, "rgba(244,245,247,.08)", 7, .7)}
      <div style="position:absolute;left:0;right:0;top:150px;display:flex;justify-content:center">{mark("m1-fusion-rev", 130)}</div>
      <div style="position:absolute;left:0;right:0;top:1150px;text-align:center">{kicker("LIGHTS OUT IN", STEEL, 24)}
        <div class="mono" style="font-size:150px;color:{ICE};margin-top:26px;letter-spacing:-.02em">02:14:09</div>
        <div style="display:flex;justify-content:center;margin:46px 0">{slit(360, 8)}</div>
        <div class="exp" style="font-size:40px;color:{ICE}">KARTING · ROUND 05</div>
        <div style="margin-top:16px">{mono("MEKO KARTODROME · 18:00 IST", STEEL, 22)}</div></div>
      <div style="position:absolute;left:0;right:0;bottom:150px;display:flex;justify-content:center">{kicker("TAP TO SET A REMINDER", ICE, 18)}</div>
    </div>'''


def t_quote():
    return f'''<div class="tpl" data-snap="post-statement" style="width:1080px;height:1350px;background:{MID}">
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 20% 100%,{NAVY} 0%,{MID} 60%)"></div>
      <div style="position:absolute;left:-160px;top:180px;opacity:.06">{mark("m1-fusion-rev", 1100)}</div>
      <div style="position:absolute;left:80px;top:80px;right:80px;display:flex;justify-content:space-between">{kicker("AKKI MEISTER", ICE, 16)}{mono("NO. 012", STEEL, 16)}</div>
      <div style="position:absolute;left:80px;top:430px;width:900px">
        <div class="cond" style="font-size:150px;line-height:.86;color:{ICE}">ONE OBSESSION.<br/><span style="color:{RED}">MANY LANES.</span></div>
        <div style="margin:46px 0 30px">{slit(260, 7)}</div>
        <div class="body" style="font-size:30px;color:{STEEL};width:760px">Sim racing, karting, Formula Student, data and coaching. Five ways in, one direction: forward.</div></div>
      <div style="position:absolute;left:80px;bottom:80px">{mono("@AKKKKKI_45", ICE, 18)}</div>
    </div>'''


# ------------------------------------------------------------------ board panels
def panel(pid, html, bg=MID):
    return f'<section data-snap="{pid}" style="width:1600px;height:1000px;background:{bg}">{html}</section>'


def scaled(html, w, h, s, left, top):
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w * s:.0f}px;height:{h * s:.0f}px;overflow:hidden"><div style="transform:scale({s});transform-origin:0 0;width:{w}px;height:{h}px">{html}</div></div>'


def build():
    P = []
    P.append(panel("01-cover", f'''
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 72% 45%,{NAVY} 0%,{MID} 62%)"></div>
      {contour(1600, 1000, "rgba(244,245,247,.06)", 7, .72)}
      <div style="position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center">{lockup(118)}</div>
      <div style="position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center">{slit(120, 5)}</div>
      <div style="position:absolute;left:64px;bottom:52px">{mono("IDENTITY SYSTEM · V1.0 · 2026", STEEL, 12)}</div>
      <div style="position:absolute;right:64px;bottom:52px">{mono("BENGALURU · IN", STEEL, 12)}</div>'''))
    tiles = [("PRIMARY · FUSION", MID, mark("m1-fusion-rev", 250)), ("SECONDARY · SPEED", MID, mark("m2-fusion-bar-rev", 270)), ("BADGE · VISOR CREST", MID, mark("m3-crest-rev", 250)),
             ("ON ICE", ICE, mark("m1-fusion-color", 250)), ("ON SIGNAL RED", RED, mark("m1-fusion-rev", 250)), ("CREST · ON ICE", ICE, mark("m3-crest-color", 240))]
    g = ""
    for i, (cap, bg, art) in enumerate(tiles):
        x, y = 64 + (i % 3) * 496, 112 + (i // 3) * 300
        cc = MID if bg == ICE else ICE
        g += f'<div class="tile" style="left:{x}px;top:{y}px;width:480px;height:284px;background:{bg};border:1px solid {LINE}">{art}<div style="position:absolute;left:22px;bottom:18px">{kicker(cap, cc, 11)}</div></div>'
    g += f'<div class="tile" style="left:64px;top:712px;width:1472px;height:240px;background:{MID};border:1px solid {LINE}">{lockup(88)}<div style="position:absolute;left:22px;bottom:18px">{kicker("HORIZONTAL LOCKUP", ICE, 11)}</div></div>'
    P.append(panel("02-logo-suite", g + head("02", "LOGO SUITE"), "#0A0C12"))
    # construction
    P.append(panel("03-construction", f'''
      <div style="position:absolute;left:120px;top:150px;width:700px;height:700px;border:1px solid {LINE}">
        <svg width="700" height="700" style="position:absolute">{"".join(f'<line x1="{x}" x2="{x}" y1="0" y2="700" stroke="{LINE}"/>' for x in range(70, 700, 70))}{"".join(f'<line y1="{y}" y2="{y}" x1="0" x2="700" stroke="{LINE}"/>' for y in range(70, 700, 70))}</svg>
        <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{mark("m1-fusion-rev", 660)}</div></div>
      <div style="position:absolute;left:900px;top:170px;width:600px">
        {kicker("01 · LETTERFORMS", RED, 13)}<div class="body" style="margin:12px 0 40px">A and M are outlined from Saira Expanded Black Italic: a 12° italic built for speed and legibility, licensed for logo use under the SIL Open Font License.</div>
        {kicker("02 · FUSION", RED, 13)}<div class="body" style="margin:12px 0 40px">The M slides into the A until the A's right leg and the M's first stroke share ink. Two letters, one silhouette.</div>
        {kicker("03 · THE SLIT", RED, 13)}<div class="body" style="margin:12px 0 40px">One knife cut at crossbar height runs through both letters. It is the A's crossbar, the overtaking line and the gap to the car ahead.</div>
        {kicker("04 · CLEAR SPACE", RED, 13)}<div class="body" style="margin-top:12px">Keep clear space equal to the height of the A's counter on all sides. Minimum size: 24 px on screen, 10 mm in print.</div></div>
      {head("03", "CONSTRUCTION")}'''))
    # type + colour
    sw = (("MIDNIGHT", MID, "60%"), ("DEEP NAVY", NAVY, "20%"), ("SIGNAL RED", RED, "8%"), ("ICE", ICE, "10%"), ("STEEL", STEEL, "2%"))
    swatch = "".join(f'<div style="position:absolute;left:{64 + i * 196}px;top:600px;width:180px;height:330px;background:{hx};border:1px solid {LINE}"><div style="position:absolute;left:18px;bottom:62px">{kicker(n, MID if n in ("ICE", "STEEL") else ICE, 12)}</div><div style="position:absolute;left:18px;bottom:40px">{mono(hx, MID if n in ("ICE", "STEEL") else ICE, 12)}</div><div style="position:absolute;left:18px;bottom:18px">{mono("USE " + p, MID if n in ("ICE", "STEEL") else STEEL, 11)}</div></div>' for i, (n, hx, p) in enumerate(sw))
    P.append(panel("04-type-colour", f'''
      <div style="position:absolute;left:64px;top:120px">{kicker("DISPLAY · SAIRA (GOOGLE FONTS, OFL)", RED, 12)}</div>
      <div class="cond" style="position:absolute;left:60px;top:150px;font-size:170px;line-height:.85;color:{ICE}">RACE DAY</div>
      <div class="exp" style="position:absolute;left:64px;top:310px;font-size:62px;color:{ICE}">AKKI MEISTER</div>
      <div class="exp" style="position:absolute;left:66px;top:400px;font-size:22px;color:{STEEL};font-weight:500;font-style:normal;letter-spacing:.32em">MOTORSPORT · PERFORMANCE</div>
      <div style="position:absolute;left:64px;top:470px;display:flex;gap:60px">{kicker("CONDENSED BLACK ITALIC · HEADLINES", STEEL, 11)}{kicker("EXPANDED BLACK ITALIC · NAMES", STEEL, 11)}{kicker("EXPANDED REGULAR · TAGLINES", STEEL, 11)}</div>
      <div style="position:absolute;left:1080px;top:150px;width:460px">{kicker("TEXT · INTER TIGHT", RED, 12)}<div class="body" style="font-size:24px;color:{ICE};margin-top:14px">Five ways into motorsport, one direction: forward.</div>
        <div style="margin-top:44px">{kicker("DATA · JETBRAINS MONO", RED, 12)}</div><div class="mono" style="font-size:44px;color:{ICE};margin-top:14px">1:26.004</div><div class="mono" style="font-size:22px;color:{STEEL};margin-top:8px">S2 −0.214 · 287 KM/H</div></div>
      {swatch}
      <div style="position:absolute;left:1080px;top:600px;width:460px">{kicker("ONE RED THING", RED, 12)}<div class="body" style="margin-top:12px">Midnight and Deep Navy are the stage. Signal Red appears once per frame: the slit, the result or the live tag. Never two saturated colours together.</div></div>
      {head("04", "TYPE & COLOUR")}'''))
    # language: imagery + graphic devices
    P.append(panel("05-language", f'''
      {graded("fs-bw.jpg", 720, 820, "50% 55%", "left:64px;top:120px")}
      <div style="position:absolute;left:84px;top:870px">{kicker("IMAGERY · COOL MONO GRADE, ONE LIGHT SOURCE", ICE, 11)}</div>
      <div style="position:absolute;left:840px;top:120px;width:696px;height:390px;background:{MID};border:1px solid {LINE};overflow:hidden">{contour(696, 390, "rgba(244,245,247,.12)", 6, .7)}
        <div style="position:absolute;left:30px;top:30px">{kicker("CONTOUR LINES", RED, 12)}</div>
        <div style="position:absolute;left:30px;bottom:110px">{slit(420, 9)}</div><div style="position:absolute;left:30px;bottom:30px">{kicker("THE SLIT · ONE PER LAYOUT", ICE, 12)}</div></div>
      <div style="position:absolute;left:840px;top:530px;width:696px;height:410px;background:{MID};border:1px solid {LINE};padding:30px">
        {kicker("DATA AS TEXTURE", RED, 12)}
        <div style="display:grid;grid-template-columns:repeat(3,1fr);margin-top:30px;border-top:1px solid {LINE}">
        {"".join(f'<div style="padding-top:20px">{kicker(k, STEEL, 11)}<div class="mono" style="font-size:32px;color:{c};margin-top:10px">{v}</div></div>' for k, v, c in (("BEST LAP", "1:26.004", ICE), ("DELTA", "−0.214", RED), ("V-MAX", "287", ICE)))}</div>
        <div style="margin-top:50px">{partner_bar(636)}</div></div>
      {head("05", "GRAPHIC LANGUAGE")}'''))
    # social overview
    tp = [t_raceday(), t_result(), t_driver(), t_quote()]
    g = "".join(scaled(t, 1080, 1350, .245, 64 + i * 278, 112) for i, t in enumerate(tp))
    g += scaled(t_story(), 1080, 1920, .36, 1190, 112)
    g += f'<div style="position:absolute;left:64px;top:470px">{kicker("POSTS 4:5 · STORY 9:16", RED, 12)}</div>'
    av = "".join(f'<div style="width:150px;height:150px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;border:1px solid {LINE}">{mark(k, 118)}</div>' for k, bg in (("m3-crest-rev", f"radial-gradient(circle at 50% 30%,{NAVY},{MID})"), ("m1-fusion-rev", RED)))
    g += f'<div style="position:absolute;left:64px;top:600px">{kicker("AVATAR", STEEL, 11)}<div style="display:flex;gap:28px;margin-top:18px">{av}</div></div>'
    g += f'<div style="position:absolute;left:520px;top:600px;width:600px">{kicker("TEMPLATE RULES", STEEL, 11)}<div class="body" style="margin-top:12px">Mark top-left. One headline in Saira Condensed. One slit. Data in mono. Partner bar on key posts. Photos always graded cool and dark.</div></div>'
    P.append(panel("06-social", g + head("06", "SOCIAL"), "#0A0C12"))
    return P, [t_raceday(), t_result(), t_driver(), t_quote(), t_story()]


CSS = f"""
@font-face {{ font-family: Saira; src: url({F}saira/files/saira-latin-wdth-normal.woff2) format('woff2'); font-weight: 100 900; font-stretch: 50% 125%; }}
@font-face {{ font-family: Saira; src: url({F}saira/files/saira-latin-wdth-italic.woff2) format('woff2'); font-weight: 100 900; font-stretch: 50% 125%; font-style: italic; }}
@font-face {{ font-family: InterT; src: url({F}inter-tight/files/inter-tight-latin-wght-normal.woff2) format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: JBM; src: url({F}jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2) format('woff2'); font-weight: 100 800; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; }}
section, .tpl {{ position: relative; overflow: hidden; margin-bottom: 40px; }}
.kick {{ font-family: Saira; font-stretch: 125%; font-weight: 600; text-transform: uppercase; letter-spacing: .24em; white-space: nowrap; }}
.mono {{ font-family: JBM; font-weight: 500; letter-spacing: .04em; white-space: nowrap; }}
.cond {{ font-family: Saira; font-stretch: 62%; font-weight: 900; font-style: italic; text-transform: uppercase; }}
.exp {{ font-family: Saira; font-stretch: 125%; font-weight: 900; font-style: italic; text-transform: uppercase; letter-spacing: .01em; white-space: nowrap; }}
.body {{ font-family: InterT; font-weight: 400; font-size: 18px; line-height: 1.55; color: #A9AFBC; }}
.tile {{ position: absolute; display: flex; align-items: center; justify-content: center; }}
"""

if __name__ == "__main__":
    P, T = build()
    open(R4 + "system.html", "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(P)}{"".join(T)}</body></html>')
    print("ok")

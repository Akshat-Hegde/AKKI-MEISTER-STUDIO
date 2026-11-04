"""Reel soundtrack: intro build that drops into a 120 BPM premium house-leaning groove, plus a few tactile accents."""
import json, os, wave
import numpy as np

SR, END = 44100, 31.0
N = int(SR * END)
rng = np.random.default_rng(7)
BPM = 120; BEAT = 60 / BPM; S16 = BEAT / 4
T = lambda n: np.arange(n) / SR


def lp(x, fc):
    fc = np.broadcast_to(np.asarray(fc, float), x.shape); a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a[i]) * x[i] + a[i] * z; y[i] = z
    return y


def bp(x, fc, q=2.0):
    fc = np.broadcast_to(np.asarray(fc, float), x.shape); f = 2 * np.sin(np.pi * np.minimum(fc, SR / 6) / SR)
    lo = b = 0.0; y = np.empty_like(x)
    for i in range(len(x)):
        h = x[i] - lo - b / q; b += f[i] * h; lo += f[i] * b; y[i] = b
    return y


hp = lambda x, fc: x - lp(x, fc)
L, R, SEND, DLY = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)


def add(buf, at, g=1.0, pan=0.0, rev=0.0, dly=0.0):
    i = int(at * SR)
    if i < 0 or i >= N: return
    buf = buf[:N - i] * g; j = i + len(buf)
    L[i:j] += buf * np.sqrt(1 - pan); R[i:j] += buf * np.sqrt(1 + pan)
    if rev: SEND[i:j] += buf * rev
    if dly: DLY[i:j] += buf * dly


def note(nm):
    o = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    return 440 * 2 ** ((o[nm[0]] + (1 if "#" in nm else 0) + (int(nm[-1]) - 4) * 12) / 12)


# ---------------- instruments ----------------
def pluck(f, d=.5, bright=6.0):
    """additive pluck: higher harmonics decay faster -> plucky filter-envelope feel"""
    n = int(d * SR); t = T(n); x = 0
    for k in range(1, 10):
        x = x + np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (2.5 + bright * k * .9))
    return x * np.minimum(1, t / .002)


def pad(fs, d):
    """warm detuned saw-ish pad (additive, 3 voices per note, gentle brightness)"""
    n = int(d * SR); t = T(n); x = 0
    for f in fs:
        for dt in (-.006, 0, .007):
            for k in range(1, 7):
                x = x + np.sin(2 * np.pi * f * (1 + dt) * k * t + k * dt * 300) / k ** 1.4
    x /= len(fs) * 3
    return x * np.minimum(1, t / .25) * np.minimum(1, (d - t) / .3)


def kick():
    n = int(.42 * SR); t = T(n); f = 46 + 95 * np.exp(-t / .03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .2)
    click = bp(rng.standard_normal(n), 3500, 1.5) * np.exp(-t / .002) * .4
    return np.tanh(1.6 * body) + click


def clap():
    n = int(.35 * SR); t = T(n); e = np.zeros(n)
    for s in (0, .009, .019):
        m = t >= s; e[m] += np.exp(-(t[m] - s) / (.006 if s < .019 else .07))
    return bp(rng.standard_normal(n), 1500, 1.2) * e


def hat(open_=False):
    n = int((.16 if open_ else .035) * SR); t = T(n)
    return hp(rng.standard_normal(n), 7000) * np.exp(-t / (.06 if open_ else .009))


def bass(f, d):
    n = int(d * SR); t = T(n)
    x = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .08) + .15 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / .04)
    return np.tanh(1.4 * x) * np.minimum(1, t / .004) * np.exp(-t / (d * .55))


def riser(d):
    """filtered noise + rising tone into the drop"""
    n = int(d * SR); t = T(n); u = t / d
    nz = lp(rng.standard_normal(n), 400 + 7000 * u ** 2) * u ** 2.2
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * u)) / SR) * u ** 3 * .25
    return (nz * .7 + tone) * np.minimum(1, (d - t) / .01)


def impact():
    """the drop: deep sub boom + punchy transient + airy tail"""
    n = int(2.8 * SR); t = T(n); f = 32 + 90 * np.exp(-t / .045)
    sub = np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 1.0))
    tr = bp(rng.standard_normal(n), 2200, .9) * np.exp(-t / .012) * .8
    air = hp(rng.standard_normal(n), 5000) * np.exp(-t / .6) * .12
    return sub + tr + air


def thock():
    """tactile premium knock: short low-mid body + felt click, like a weighted switch"""
    n = int(.14 * SR); t = T(n)
    body = np.sin(2 * np.pi * (165 + 90 * np.exp(-t / .006)) * t) * np.exp(-t / .045)
    knock = bp(rng.standard_normal(n), 900, 1.4) * np.exp(-t / .007) * .5
    click = bp(rng.standard_normal(n), 3800, 2) * np.exp(-t / .0015) * .25
    return lp(body + knock + click, 5000)


def soft_tick():
    n = int(.05 * SR); t = T(n)
    return lp(np.sin(2 * np.pi * 1400 * t) * np.exp(-t / .008) + bp(rng.standard_normal(n), 3000, 2) * np.exp(-t / .002) * .3, 7000)


def key_tick():
    n = int(.03 * SR); t = T(n)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t / .005) * .5


def pop():
    n = int(.08 * SR); t = T(n); f = 380 + 300 * np.exp(-t / .01)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .025)


# ---------------- events ----------------
EV = json.load(open("../events.json"))
hits = sorted(e["t"] for e in EV if e["kind"] == "hit")
DROP, FINAL = hits[0], hits[-1]
INTRO_NOTES = ["A4", "C5", "E5", "A5"]
# a licensed track replaces the synthesized intro build + groove when TRACK is set
TRACK = os.environ.get("TRACK", "../music/drums.wav")
for e in EV:
    k, t, g = e["kind"], e["t"], e["gain"]
    if TRACK and k in ("note", "riser"): continue
    if k == "note": add(pluck(note(INTRO_NOTES[int(g)]), .9, 4), t, .2, (-.3, .3)[int(g) % 2], .5, .35)
    elif k == "riser": add(riser(DROP - t), t, .32, 0, .3)
    elif k == "hit": add(impact(), t, .3 if TRACK else .75, 0, .35)
    elif k == "thock": add(thock(), t, .4 * g, 0, .12)
    elif k == "tick": add(soft_tick(), t, .16 * g, 0, .15)
    elif k == "pop": add(pop(), t, .12 * g, 0, .15)
    elif k == "type": add(key_tick(), t, .45 * g, 0, .05)

def load_track(path):
    with wave.open(path) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2) / 32768.
    return x


if TRACK:
    # track's first big hit (2.93 s) lands on the logo drop; splice to its outro hit (45.03 s) on the final lockup
    TR = load_track(TRACK); A_HIT, B_HIT, XF = 2.93, 45.03, int(.012 * SR)
    a0 = int((A_HIT - DROP) * SR); cut = int(FINAL * SR) - int(.006 * SR)
    partA = TR[a0:a0 + cut + XF]
    b0 = int(B_HIT * SR) - int(.006 * SR); partB = TR[b0 - XF:b0 + (N - cut)]
    mus = np.zeros((N, 2))
    mus[:cut] = partA[:cut]
    fade = np.linspace(1, 0, XF)[:, None]
    mus[cut:cut + XF] = partA[cut:cut + XF] * fade + partB[:XF] * (1 - fade)
    rest = partB[XF:XF + N - cut - XF]; mus[cut + XF:cut + XF + len(rest)] = rest
    tail = int(1.8 * SR); mus[-tail:] *= (np.linspace(1, 0, tail) ** 1.5)[:, None]
    gain = .4
    L += mus[:, 0] * gain; R += mus[:, 1] * gain
else:
    # ---------------- music: drops on the logo, rides to the final lockup ----------------
    M = (L, R, SEND, DLY)
    SAVED = [a.copy() for a in M]
    for a in M: a[:] = 0
    PROG = [("A1", ["A3", "C4", "E4", "G4", "B4"]), ("F1", ["F3", "A3", "C4", "E4", "G4"]),
            ("C2", ["G3", "C4", "E4", "G4", "B4"]), ("G1", ["G3", "B3", "D4", "E4", "A4"])]
    ARP = [0, 2, 4, 1, 3, 4, 2, 0, 1, 3, 4, 2, 3, 1, 4, 2]
    BAR = 4 * BEAT
    nbars = int(np.ceil((FINAL - DROP) / BAR))
    S2_START = DROP + 2.0                      # hats/arp enter as the story starts
    FULL = DROP + 2 * BAR + 1.6                # claps + open hats from the first section
    KICKS = []
    for b in range(nbars):
        t0 = DROP + b * BAR
        root, ch = PROG[b % 4]
        fs = [note(x) for x in ch]
        add(pad(fs[:4], BAR + .2), t0, .085, 0, .5)
        for s in range(16):
            at = t0 + s * S16
            if at >= FINAL - .05: break
            swing = .012 if s % 2 else 0
            if s % 4 == 0: KICKS.append(at)
            if at >= FULL and s in (4, 12): add(clap(), at, .2, 0, .35)
            if at >= S2_START:
                add(hat(), at + swing, .05 if s % 2 else .028, (.25, -.25)[s % 2])
                if s % 4 == 2 and at >= FULL: add(hat(True), at, .045, .1)
                if s % 2 == 0 or at >= FULL:
                    add(pluck(fs[ARP[s]] * 2, .35, 7), at + swing, .055, (-.35, .35)[s % 2], .25, .4)
            if s in (2, 6, 10, 14) or (s == 15 and b % 2):
                add(bass(note(root) * (2 if s == 15 else 1), S16 * 2.2), at, .32)
    # sidechain pump on the music bed, then the kicks on top un-pumped
    tt = np.arange(N) / SR
    pump = np.where((tt >= DROP) & (tt < FINAL), 1 - .55 * np.exp(-((tt - DROP) % BEAT) / .09), 1)
    for a in M: a *= pump
    for at in KICKS: add(kick(), at, .5)
    # outro: sustained chord + echoing pluck after the final hit
    add(pad([note(x) for x in ["A3", "C4", "E4", "B4"]], END - FINAL), FINAL, .1, 0, .6)
    for i, nm in enumerate(["E5", "A5", "B5", "E6"]):
        add(pluck(note(nm), .8, 4), FINAL + .25 + i * BEAT / 2, .07, (-.3, .3)[i % 2], .5, .45)
    for a, s0 in zip(M, SAVED): a += s0

# ---------------- dotted-eighth ping-pong delay + reverb + master ----------------
dl = int(BEAT * .75 * SR); fb = .38; dL = np.zeros(N); dR = np.zeros(N)
src = lp(DLY, 4000)
for k in range(1, 6):
    sh = dl * k
    if sh >= N: break
    (dL if k % 2 else dR)[sh:] += src[:N - sh] * fb ** (k - 1) * .6
L += dL; R += dR
irn = int(2.0 * SR); ti = T(irn)
irl = lp(rng.standard_normal(irn) * np.exp(-ti / .5), 6000); irr = lp(rng.standard_normal(irn) * np.exp(-ti / .5), 6000)
irl /= np.sqrt((irl ** 2).sum()); irr /= np.sqrt((irr ** 2).sum())
m = 1 << int(np.ceil(np.log2(N + irn))); S = np.fft.rfft(SEND, m)
L += np.fft.irfft(S * np.fft.rfft(irl, m), m)[:N] * .45; R += np.fft.irfft(S * np.fft.rfft(irr, m), m)[:N] * .45
mix = np.stack([hp(L, 28), hp(R, 28)], 1)
mix /= np.max(np.abs(mix)) + 1e-9
DRV = 1.0 if TRACK else 1.6
mix = np.tanh(mix * DRV) / np.tanh(DRV)
fi, fo = int(.05 * SR), int(.6 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]; mix[-fo:] *= (np.linspace(1, 0, fo) ** 2)[:, None]
mix *= (.74 if TRACK else .89) / np.max(np.abs(mix))
with wave.open("../audio.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("audio ok", len(EV), "events", "drop", DROP, "final", FINAL)

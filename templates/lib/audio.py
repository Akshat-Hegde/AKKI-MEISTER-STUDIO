"""Soft accent track for template reels: a tactile knock on cuts and a quiet tick when type lands.
Subtle and premium per CLAUDE.md: no whooshes, no engine/beep/radio effects. Music (a real, licensed
track) is mixed in by templates/lib/reel.js, not synthesised here.
    python audio.py events.json <duration_s> out.wav"""
import json, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a) * x[i] + a * z; y[i] = z
    return y


def bp(x, fc, q=1.5):
    f = 2 * np.sin(np.pi * min(fc, SR / 6) / SR); lo = b = 0.0; y = np.empty_like(x)
    for i in range(len(x)):
        h = x[i] - lo - b / q; b += f * h; lo += f * b; y[i] = b
    return y


def knock():
    """weighted-switch knock: short low-mid body + felt click"""
    n = int(.16 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (150 + 80 * np.exp(-t / .006)) * t) * np.exp(-t / .05)
    felt = bp(rng.standard_normal(n), 850, 1.4) * np.exp(-t / .008) * .45
    click = bp(rng.standard_normal(n), 3600, 2) * np.exp(-t / .0015) * .18
    return lp(body + felt + click, 4500)


def tick():
    n = int(.05 * SR); t = np.arange(n) / SR
    return lp(np.sin(2 * np.pi * 1250 * t) * np.exp(-t / .007) + bp(rng.standard_normal(n), 2800, 2) * np.exp(-t / .002) * .25, 6000) * .5


def main():
    ev = json.load(open(sys.argv[1])); dur = float(sys.argv[2]); out = sys.argv[3]
    N = int(SR * dur) + SR; L = np.zeros(N); R = np.zeros(N)
    K, T = knock(), tick()
    for e in ev:
        s = K if e["kind"] == "knock" else T
        i = int(e["t"] * SR); g = e.get("gain", 1) * (.32 if e["kind"] == "knock" else .16)
        if i < 0 or i >= N: continue
        seg = s[:N - i] * g; pan = .08 if e["kind"] == "tick" else 0
        L[i:i + len(seg)] += seg * (1 - pan); R[i:i + len(seg)] += seg * (1 + pan)
    # tiny room: two short reflections, keeps it from sounding dry/clicky
    for d, g in ((.023, .22), (.041, .12)):
        k = int(d * SR); L[k:] += L[:-k] * g; R[k:] += R[:-k] * g * .9
    st = np.stack([L, R], 1)[:int(SR * dur)]
    st = np.clip(st, -1, 1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()

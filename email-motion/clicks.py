"""Premium touchscreen taps for email-open.mp4: the tap on the email, a lighter one as it opens."""
import wave
import numpy as np

SR, END = 44100, 3.0
N = int(SR * END)
rng = np.random.default_rng(5)
T = lambda n: np.arange(n) / SR


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a) * x[i] + a * z; y[i] = z
    return y


def bp(x, fc, q=1.5):
    f = 2 * np.sin(np.pi * fc / SR); lo = bb = 0.0; y = np.empty_like(x)
    for i in range(len(x)):
        h = x[i] - lo - bb / q; bb += f * h; lo += f * bb; y[i] = bb
    return y


def touch(bright=4200, thump=.55):
    """premium touchscreen tap: crisp glassy 'tk' + a tiny haptic thump underneath"""
    n = int(.05 * SR); t = T(n)
    tk = bp(rng.standard_normal(n), bright, 2.2) * np.exp(-t / .0016)
    glass = np.sin(2 * np.pi * 3100 * t) * np.exp(-t / .004) * .35
    haptic = np.sin(2 * np.pi * (170 + 80 * np.exp(-t / .004)) * t) * np.exp(-t / .011) * thump
    return tk + glass + haptic


mix = np.zeros(N)
for fn, at, g in ((lambda: touch(), .68, .6), (lambda: touch(5200, .3), 1.0, .28)):
    s = fn() * g; i = int(at * SR); mix[i:i + len(s)] += s[:N - i]
# a touch of room so they don't sound dry
ir = rng.standard_normal(int(.25 * SR)) * np.exp(-T(int(.25 * SR)) / .05) * .04
mix = mix + np.convolve(mix, ir)[:N]
mix *= .7 / np.max(np.abs(mix))
st = np.stack([mix, mix], 1)
with wave.open("clicks.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")

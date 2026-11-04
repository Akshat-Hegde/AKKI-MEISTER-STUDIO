"""Sound for email-open.mp4 from real SFX: click on the tap, page flip as the email opens, soft ting on the highlight."""
import wave
import numpy as np

SR, END = 44100, 3.0
N = int(SR * END)


def load(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.


def cut(x, a, b, fi=.002, fo=.03):
    s = x[int(a * SR):int(b * SR)].copy(); n = len(s)
    s[:int(fi * SR)] *= np.linspace(0, 1, int(fi * SR)); s[n - int(fo * SR):] *= np.linspace(1, 0, int(fo * SR))
    return s


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a) * x[i] + a * z; y[i] = z
    return y


click = cut(load("sfx/Mouse_click_.wav"), 1.795, 1.95)
flip = load("sfx/Page_Turn_So.wav")
pk = int(np.argmax(np.abs(flip))) / SR                     # loudest point of the flip
flip = lp(cut(flip, pk - .32, pk + .42, .03, .12), 7000)    # softened, so it reads as a swipe not a crash
ting = cut(load("sfx/TING_SOUND_E.wav"), .76, 2.0, .002, .25)

mix = np.zeros(N)
for s, at, g in ((click, .67, .75), (flip, 1.08 - .32, .32), (ting, 1.45, .28)):
    i = int(at * SR); s = s[:N - i] * g / (np.max(np.abs(s)) + 1e-9); mix[i:i + len(s)] += s
mix *= .7 / np.max(np.abs(mix))
st = np.stack([mix, mix], 1)
with wave.open("clicks.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok, flip peak at", round(pk, 2))

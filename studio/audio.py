# Procedural score: tempo-locked bed (96 bpm) with one motif that opens and closes the film,
# soft cues only on executed trades, the risk-off drop and the risk-on chime. Seeded, no samples.
import json, sys, numpy as np, wave
sr = 48000; cues = json.load(open(sys.argv[1])); out = sys.argv[2]
dur = cues['duration']; n = int(sr * dur); t = np.arange(n) / sr
mix = np.zeros(n)
def env(x, a=0.005, r=0.3):
    return np.minimum(x / a, 1) * np.exp(-x / r)
def add(sig, at, gain=1.0):
    i = int(at * sr); j = min(n, i + len(sig))
    if i < n: mix[i:j] += sig[:j - i] * gain
def tone(f, d, a=0.005, r=0.3, harm=(1, .3, .1)):
    x = np.arange(int(sr * d)) / sr
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * x) for k, h in enumerate(harm)) * env(x, a, r)
beat = 60 / 96
# bed: A1 drone + fifth, slow swell, a filtered pulse on every beat
drone = np.sin(2*np.pi*55*t) * .5 + np.sin(2*np.pi*82.41*t) * .22 + np.sin(2*np.pi*110*t) * .1
drone *= 0.55 + 0.25 * np.sin(2*np.pi*t / (beat * 8))
mix += drone * 0.5
for b in np.arange(0, dur, beat):
    add(tone(55, .5, .01, .18, (1, .5)), b, .22)
# motif (A min pent): E4 G4 A4 C5 at the open and again at the payoff
motif = [329.63, 392.0, 440.0, 523.25]
for start in (0.5, 28.0):
    for i, f in enumerate(motif):
        add(tone(f, 1.0, .01, .45), start + i * beat * .5, .16)
# cues: executed trades -> soft tick (win) / low thud (loss); capped level so they stay under the bed
for c in cues['cues']:
    if c['win']: add(tone(1320 if c['size'] == 1 else 1760, .25, .002, .06, (1, .2)), c['t'], .10)
    else: add(tone(160, .3, .002, .09, (1, .4)), c['t'], .16)
m = cues['markers']
x = np.arange(int(sr * 1.2)) / sr
add(np.sin(2*np.pi*(600 * np.exp(-x * 1.6)) * x) * env(x, .01, .5), m['riskOff'], .35)        # risk off: falling sweep
for i, f in enumerate([523.25, 659.25, 783.99]): add(tone(f, 1.2, .01, .5), m['riskOn'] + i * .09, .14)  # risk on: chime
mix *= np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5)
mix = mix / max(1e-9, np.abs(mix).max()) * 0.8
with wave.open(out, 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype('<i2').tobytes())

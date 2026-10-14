# Ship Line score (baseline sound spec): tempo-locked procedural bed with one motif that returns on the key idea,
# soft cues only on meaningful actions (role introduced, ship, gate off / on). 120 bpm = 60 beats in 30 s. ~ -16 LUFS, true peak <= -1.5 dBTP.
import json, sys, numpy as np, wave
sr = 48000; tl = json.load(open(sys.argv[1])); out = sys.argv[2]; D = tl['duration']; M = tl['markers']
n = int(sr * D); tt = np.arange(n) / sr; mix = np.zeros(n); beat = .5
def env(x, a=.004, r=.25): return np.minimum(x / a, 1) * np.exp(-x / r)
def X(d): return np.arange(int(sr * d)) / sr
def add(sig, at, g=1.):
    i = int(round(at * sr))
    if i < 0 or i >= n: return
    j = min(n, i + len(sig)); mix[i:j] += sig[:j - i] * g
def tone(f, d, a=.004, r=.25, h=(1, .22, .07)):
    x = X(d); return sum(k * np.sin(2*np.pi*f*(i+1)*x) for i, k in enumerate(h)) * env(x, a, r)
ramp = lambda a, b: np.clip((tt - a) / (b - a), 0, 1)
# bed: sub + soft pad (A minor) that opens as the crew comes online, a little less in the turn, full at the payoff
mix += np.sin(2*np.pi*55*tt) * (.10 + .06*ramp(3.6, 12)) 
for f, a in ((110, .05), (130.81, .04), (164.81, .04), (196, .03)):
    mix += np.sin(2*np.pi*f*tt + .5*np.sin(2*np.pi*.17*tt + f)) * a * (.5 + .5*ramp(3.6, 12))
# pulse: quiet kick on every beat from the model scene, hat on off-beats from the proof
for b in range(int(D / beat)):
    at = b * beat
    if at >= 3.6:
        x = X(.22); add(np.sin(2*np.pi*(48 + 70*np.exp(-x*30))*x) * np.exp(-x*11), at, .30 * (.6 + .4*(at >= 12)))
    if at >= 12 and b % 2 == 1:
        add(np.diff(np.random.RandomState(b).randn(int(sr*.03) + 1)) * env(X(.03), .001, .012), at, .09)
# motif: A4 C5 E5 G5, opens the film and returns when the gate is back on
mot = [440.0, 523.25, 659.25, 783.99]
for st in (.5, M['payoff']):
    for i, f in enumerate(mot): add(tone(f, 1.0, .006, .4), st + i*beat*.5, .13)
# cues: a role comes online (rising ping), ships (soft tick), gate off (falling sweep), gate on (chime)
for k, t in enumerate(M['stage']): add(tone(660 * 2**(k/6), .35, .004, .12), t, .12)
for t in tl['flashes']:
    if t > 12: add(tone(1320, .12, .002, .04, (1, .2)), t, .06)
x = X(1.2); add(np.sin(2*np.pi*(520 * np.exp(-x*1.7)) * x) * env(x, .01, .5), M['turn0'], .28)
add(np.sin(2*np.pi*70*X(.8)) * env(X(.8), .004, .3), M['turn0'], .30)
for i, f in enumerate((523.25, 659.25, 783.99)): add(tone(f, 1.2, .01, .5), M['turn1'] + i*.09, .12)
# fades, normalise (loudness is set afterwards with ffmpeg)
mix *= np.minimum(1, tt / .4) * np.minimum(1, (D - tt) / 1.2)
mix /= max(1e-9, np.abs(mix).max()); mix *= .85
with wave.open(out, 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype('<i2').tobytes())

# Night Desk score, ORIGINAL: dark industrial / electronic. Pulsing synth bass, breakbeat drums, tense low strings, brass stabs.
# 138.46 bpm = exactly 60 beats in 26 s, so the groove loops. Climax hit at the signal (climax marker), second hit at ORDER FILLED.
# Rendered with a 0.9 s pre-roll that the end cross-fades into, so the last sample leads into the first.
import json, sys, numpy as np, wave
sr = 48000; tl = json.load(open(sys.argv[1])); out = sys.argv[2]
D = tl['duration']; M = tl['markers']; TC = M['climax']; TF = M['fill']; PRE = 0.9
n = int(sr * (D + PRE)); tt = np.arange(n) / sr - PRE
rs = np.random.RandomState(11)
beat = 60 / 138.4615; s16 = beat / 4; bar = beat * 4
ramp = lambda a, b: np.clip((tt - a) / (b - a), 0, 1)
def env(x, a=.003, r=.2): return np.minimum(x / a, 1) * np.exp(-x / r)
def add(sig, at, g=1.0, buf=None):
    buf = mix if buf is None else buf
    i = int(round((at + PRE) * sr))
    if i >= n or i + len(sig) <= 0: return
    j0 = max(0, -i); i0 = max(0, i); j = min(n, i0 + len(sig) - j0)
    buf[i0:j] += sig[j0:j0 + (j - i0)] * g
def X(d): return np.arange(int(sr * d)) / sr
def noise(d): return rs.randn(int(sr * d))
def hp(x, a=.96): y = np.zeros_like(x); y[1:] = x[1:] - a * x[:-1]; return y
def saw(f, d, harm=12, decay=0.0, a=.004, r=.2, c=1.0):
    x = X(d); y = sum(np.sin(2*np.pi*f*h*x) / h**1.1 * (c**(h-1)) * np.exp(-x*decay*h) for h in range(1, harm + 1)); return y * env(x, a, r)
mix = np.zeros(n); wet = np.zeros(n)

# ---------- drums ----------
def kick(at, g=1.0):
    x = X(.34); add(np.sin(2*np.pi*(46 + 90*np.exp(-x*32))*x) * np.exp(-x*8) + 0.15*hp(noise(.34))*np.exp(-x*90), at, .62*g)
def snare(at, g=1.0):
    x = X(.2); add(hp(noise(.2), .86)*np.exp(-x*22)*0.9 + np.sin(2*np.pi*(185+60*np.exp(-x*40))*x)*np.exp(-x*20)*.55, at, .42*g)
def hat(at, g=1.0, op=False):
    d = .22 if op else .045; x = X(d); add(hp(noise(d), .985)*np.exp(-x*(14 if op else 95)), at, .12*g)
def clang(at, g=1.0):                        # metallic, inharmonic: industrial colour
    x = X(.7); y = sum(np.sin(2*np.pi*f*x + k)*np.exp(-x*(5+k)) for k, f in enumerate((412, 677, 1119, 1789, 2851))); add(y*.18, at, g); add(y*.18, at, g*.5, wet)
KICK  = [0, 3, 8, 10, 14]; SNARE = [4, 12]; GHOST = [7, 15, 9]
def drums(b0, b1, level, full):
    for k in range(int(round((b1 - b0) / bar)) + 1):
        t0 = b0 + k * bar
        for st in range(16):
            at = t0 + st * s16
            if at < -PRE or at >= b1: continue
            if st in KICK: kick(at, level)
            if st in SNARE: snare(at, level)
            elif full and st in GHOST: snare(at, .28*level)
            if full or st % 2 == 0: hat(at, (1.0 if st % 4 == 2 else .55)*level, op=(st == 14))
# ---------- bass: pulsing synth with opening filter ----------
BN = [41.2, 41.2, 41.2, 49.0, 41.2, 41.2, 43.65, 41.2]                  # E1 F1 G1 : phrygian, dark
def bass(b0, b1, g):
    i = 0; at = b0
    while at < b1:
        f = BN[i % 8]; c = .35 + .6*np.clip((at - 7)/(TC - 7), 0, 1); d = beat/2
        y = saw(f*2, d*0.95, 9, 1.2, .004, .16, c) + 1.1*np.sin(2*np.pi*f*X(d*.95))*env(X(d*.95), .004, .22)
        add(y, at, .33*g); i += 1; at += beat/2
# ---------- strings: tense low cluster ----------
def strings(g_fn):
    notes = [(82.41, .55), (123.47, .4), (164.81, .35), (196.0, .25)]
    sw = np.zeros(n)
    for f, a in notes:
        for det in (-0.45, 0.4):
            vib = 1 + 0.003*np.sin(2*np.pi*5.4*tt + f)
            for h, ha in ((1, 1), (2, .45), (3, .3), (4, .18)): sw += a*ha*0.5*np.sin(2*np.pi*(f+det)*h*vib*tt)
    clash = np.sin(2*np.pi*174.6*tt)*ramp(11, 19)*.5 + np.sin(2*np.pi*233.1*tt)*ramp(15, 20)*.4     # F / Bb against E: tension
    trem = 1 - .35*ramp(10, 19)*(0.5 + 0.5*np.sin(2*np.pi*7.5*tt))
    return (sw + clash) * trem * g_fn
# ---------- brass stabs ----------
def stab(at, notes=(82.41, 123.47, 164.81, 196.0, 247.0), g=1.0, r=.3):
    d = r*3.2; x = X(d); y = np.zeros(len(x))
    for f in notes:
        for h in range(1, 11): y += np.sin(2*np.pi*f*h*x*(1+0.0015*np.sin(2*np.pi*6*x)))/h * np.exp(-x*(1/r + 1.4*h)) 
    y *= np.minimum(x/.014, 1); add(y, at, .12*g); add(y, at, .12*g*.7, wet)
# ---------- arrangement ----------
mix += strings(0.045*(0.35 + 0.65*ramp(0, TC))*(1 - 0.0*ramp(TC, D)))
mix += np.sin(2*np.pi*41.2*tt)*(.14 + .1*ramp(0, TC))                                  # sub drone
for at in np.arange(-PRE, 5.5, bar*2): clang(at + 3*beat, .5)                          # sparse metal in the intro
drums(5.0, TC - 0.25, .0, False) if False else None
# intro hats -> breakbeat -> roll -> drop
for k in range(int((TC - 5)/s16)):
    at = 5.0 + k*s16
    if at >= 9.5: break
    if k % 2 == 0: hat(at, .6 + .3*((k//2) % 2))
drums(9.5 - ((9.5 - 0.0) % bar), 19.4, .85, False)
drums(9.5 - ((9.5 - 0.0) % bar), 19.4, .0, True)                                       # (ghosts only in the drop; this pass adds nothing)
at = 16.2
while at < TC - 0.27:                                                                   # snare roll, accelerating
    snare(at, .35 + .65*(at - 16.2)/(TC - 16.4)); at += max(s16/2, (s16*1.6)*(1 - .8*(at - 16.2)/(TC - 16.4)))
bass(7.0, TC - 0.3, ramp(7, 9)[int((7.0 + PRE) * sr)] if False else 1.0)
for at in (14.1, 15.2, 16.0): stab(at, g=.6)
# riser
L = TC - 0.27 - 16.2; x = X(L); u = x/L
add(np.sin(2*np.pi*(180*L*(np.exp(np.log(14)*u) - 1)/np.log(14)))*u**2*.30 + hp(noise(L))*u**3*.32, 16.2, 1.0)
# drop: full groove from the climax to the end (and across the loop point)
t_drop = TC
drums(t_drop - ((t_drop - 0.0) % bar) + (bar if (t_drop % bar) > 0 else 0), D + PRE, 1.0, True)
bass(TC, D + PRE, 1.2)
bar_starts = [t for t in np.arange(0, D + PRE, bar) if t >= TC]
for t in bar_starts: stab(t, g=.75); stab(t + 10*s16, (82.41, 123.47, 196.0), g=.55, r=.2)
# the hit at the signal, and a second at ORDER FILLED
x = X(2.6); add(np.sin(2*np.pi*(40 + 70*np.exp(-x*6))*x)*np.exp(-x*1.5), TC, 1.25)
add(hp(noise(2.2))*np.exp(-X(2.2)*2.4), TC, .38)
stab(TC, (82.41, 123.47, 164.81, 196.0, 247.0, 329.6), g=1.7, r=.9)
kick(TC, 1.3); snare(TC, 1.0)
for k, f in enumerate((659.3, 987.8, 1318.5)): add(saw(f, 1.6, 5, .6, .003, .5), TC + .03 + k*.05, .07)
stab(TF, (164.81, 246.94, 329.63), g=1.1, r=.45); x = X(.5); add(np.sin(2*np.pi*(62 + 50*np.exp(-x*9))*x)*np.exp(-x*6), TF, .8)
add(saw(1318.5, .4, 4, 2, .002, .12), TF + .02, .12); add(saw(1975.5, .5, 4, 2, .002, .18), TF + .13, .12)
# reverb on the wet bus (decaying-noise impulse), then mix in
ir = noise(1.1)*np.exp(-X(1.1)*3.6); ir /= np.abs(ir).sum()**0.5 * 6
spec = np.fft.rfft(wet, n + len(ir)) * np.fft.rfft(ir, n + len(ir)); mix += np.fft.irfft(spec)[:n] * 3.0
# duck right before the climax (tension), then slam
mix *= 1 - 0.95*np.exp(-((tt - (TC - 0.13))/0.10)**2)
# loop: last PRE seconds cross-fade into the pre-roll; short fade-in on the very first samples
M_ = int(PRE*sr); res = mix[M_:].copy(); N = len(res)
a = np.sin(np.linspace(0, np.pi/2, M_))**2; res[N - M_:] = res[N - M_:]*(1 - a) + mix[:M_]*a
res -= res.mean(); res /= max(1e-9, np.abs(res).max()); res *= .85
with wave.open(out, 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((res*32767).astype('<i2').tobytes())

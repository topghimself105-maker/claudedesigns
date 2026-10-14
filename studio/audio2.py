# Procedural score for ict-desk. Cues are placed on detected events (markers in the cues json).
import json, sys, numpy as np, wave
sr=48000; tl=json.load(open(sys.argv[1])); out=sys.argv[2]; dur=tl['duration']; m=tl['markers']; n=int(sr*dur); t=np.arange(n)/sr; mix=np.zeros(n)
def env(x,a=.005,r=.3): return np.minimum(x/a,1)*np.exp(-x/r)
def add(sig,at,g=1.): i=int(at*sr); j=min(n,i+len(sig)); mix[i:j]+=sig[:j-i]*g if i<n else 0
def tone(f,d,a=.005,r=.3,h=(1,.3,.1)):
    x=np.arange(int(sr*d))/sr; return sum(k_*np.sin(2*np.pi*f*(i+1)*x) for i,k_ in enumerate(h))*env(x,a,r)
beat=60/90
drone=(np.sin(2*np.pi*55*t)*.5+np.sin(2*np.pi*82.41*t)*.2+np.sin(2*np.pi*110*t)*.1)*(0.5+0.3*np.sin(2*np.pi*t/(beat*8)))
mix+=drone*.5
for b in np.arange(0,dur,beat): add(tone(55,.5,.01,.16,(1,.5)),b,.2)
for st in (0.5,28.3):
    for i,f in enumerate([329.63,392.0,440.0,523.25]): add(tone(f,1.0,.01,.45),st+i*beat*.5,.15)
x=np.arange(int(sr*1.0))/sr
add(tone(110,2.0,.4,1.0,(1,.5,.2)),m['kz'],.25)                                    # killzone opens: swell
add(tone(180,.35,.002,.1,(1,.5)),m['skip'],.18)                                    # skipped sweep: dull tick
add(np.sin(2*np.pi*(700*np.exp(-x*1.4))*x)*env(x,.01,.45),m['sweep'],.3)           # sweep: falling sweep
for k,f in enumerate([523.25,783.99]): add(tone(f,.5,.005,.18),m['mss']+k*.09,.16) # MSS: rising pair
add(tone(1320,.25,.002,.07,(1,.2)),m['fvg'],.12)                                   # FVG
add(tone(987.77,.4,.003,.14),m['stage'],.14)                                       # staged
add(tone(90,.5,.002,.18,(1,.6)),m['sign'],.4); add(tone(1760,.15,.001,.04,(1,.3)),m['sign'],.14)  # sign: stamp
add(tone(1320,.2,.002,.05,(1,.2)),m['fill'],.14)                                   # fill: click
for k,f in enumerate([523.25,659.25,783.99,1046.5]): add(tone(f,1.4,.01,.5),m['tp']+k*.08,.13)   # target: chime
mix*=np.minimum(1,t/1.)*np.minimum(1,(dur-t)/1.5); mix=mix/max(1e-9,np.abs(mix).max())*.8
with wave.open(out,'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix*32767).astype('<i2').tobytes())

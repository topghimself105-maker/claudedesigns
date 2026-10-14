# Procedural score for night-desk: ambient pad -> arp + hats + kick -> riser -> silence -> hit at the climax -> fill confirm.
# Seamless loop: rendered with a 0.9 s pre-roll and cross-faded into it, so the last sample leads into the first.
import json, sys, numpy as np, wave
sr=48000; tl=json.load(open(sys.argv[1])); out=sys.argv[2]; D=tl['duration']; m=tl['markers']; TC=m['climax']; TF=m['fill']; PRE=0.9
n=int(sr*(D+PRE)); tt=np.arange(n)/sr-PRE; mix=np.zeros(n)
ramp=lambda a,b:np.clip((tt-a)/(b-a),0,1)
def env(x,a=.003,r=.2): return np.minimum(x/a,1)*np.exp(-x/r)
def add(sig,at,g=1.):
    i=int(round((at+PRE)*sr)); 
    if i<0 or i>=n: return
    j=min(n,i+len(sig)); mix[i:j]+=sig[:j-i]*g
def tone(f,d,a=.003,r=.2,h=(1,.25,.08)):
    x=np.arange(int(sr*d))/sr; return sum(k*np.sin(2*np.pi*f*(i+1)*x) for i,k in enumerate(h))*env(x,a,r)
rs=np.random.RandomState(7)
def noise(d): return rs.randn(int(sr*d))
def hp(x,a=.97): y=np.zeros_like(x); y[1:]=x[1:]-a*x[:-1]; return y
beat=.5
# bed: sub + pad
mix+=np.sin(2*np.pi*55*tt)*(0.30+0.12*np.sin(2*np.pi*tt/D*2))*(0.55+0.45*ramp(0,TC))
for f in (110,130.81,164.81,196.0):
    mix+=np.sin(2*np.pi*f*tt+0.4*np.sin(2*np.pi*0.2*tt+f))*0.045*(0.6+0.4*ramp(2,TC))
# arp, 16ths, pentatonic, climbs in octave across the build
pent=[220,261.63,329.63,392,440,523.25,659.25,783.99]; step=0.125; s=0
for at in np.arange(-PRE,D,step):
    if at<2: s+=1; continue
    lvl=0.05+0.20*np.clip((at-3)/(TC-3),0,1) if at<TC-0.25 else (0.0 if at<TC+0.05 else 0.16)
    oct_=2 if at>12 else 1; note=pent[(s*3+(s//8))%8]*oct_/ (2 if at<8 else 1)
    add(tone(note,0.3,.002,.11,(1,.4,.15)),at,lvl); s+=1
# hats / clap / kick
for at in np.arange(-PRE,D,0.25 if True else .5):
    if at<6 or (TC-0.25<=at<TC+0.05): continue
    sub=(at>=14); add(hp(noise(.04))*env(np.arange(int(sr*.04))/sr,.001,.012),at,0.05+0.05*sub)
    if sub: add(hp(noise(.03))*env(np.arange(int(sr*.03))/sr,.001,.01),at+0.125,0.04)
for at in np.arange(-PRE,D,beat):
    if at<8 or (TC-0.4<=at<TC+0.05): continue
    x=np.arange(int(sr*.28))/sr; add(np.sin(2*np.pi*(45+70*np.exp(-x*28))*x)*np.exp(-x*9),at,0.55)
    if at>=14 and (int(round(at/beat))%2==1): add(hp(noise(.12))*env(np.arange(int(sr*.12))/sr,.001,.05),at,0.11)
# riser (16.2 -> 20.35), silence, hit
L=TC-0.25-16.2; x=np.arange(int(sr*L))/sr; u=x/L
chirp=np.sin(2*np.pi*(200*L*(np.exp(np.log(12)*u)-1)/np.log(12)))*u**2*0.34
add(chirp+hp(noise(L))*u**3*0.34,16.2,1.0)
x=np.arange(int(sr*2.5))/sr
add(np.sin(2*np.pi*(42+60*np.exp(-x*7))*x)*np.exp(-x*1.7),TC,1.15)                     # boom
add(hp(noise(2.0))*np.exp(-np.arange(int(sr*2.0))/sr*2.6),TC,0.32)                      # crash
for k,f in enumerate((880,1318.5,1760,2637)): add(tone(f,2.0,.002,.7,(1,.2)),TC+0.02+k*0.045,0.075)  # chime
# fill confirm
add(tone(1318.5,.35,.002,.12),TF,0.14); add(tone(1760,.5,.002,.2),TF+0.11,0.14); add(np.sin(2*np.pi*(70*np.exp(-np.arange(int(sr*.5))/sr*5))*np.arange(int(sr*.5))/sr)*np.exp(-np.arange(int(sr*.5))/sr*5),TF,0.4)
# duck just before the hit
mix*=1-0.92*np.exp(-((tt-(TC-0.12))/0.11)**2)
# loop: last PRE seconds cross-fade into the pre-roll (which equals the start state)
res=mix[int(PRE*sr):].copy(); N=len(res); M=int(PRE*sr)
a=np.sin(np.linspace(0,np.pi/2,M))**2
res[N-M:]=res[N-M:]*(1-a)+mix[:M]*a
res/=max(1e-9,np.abs(res).max()); res*=0.85
with wave.open(out,'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((res*32767).astype('<i2').tobytes())

// Procedural score for "One bot, four agents", built with the Web Audio API and rendered offline in headless Chrome.
// A tempo-locked bed (96 bpm = 72 beats in 45 s) with ONE motif that returns on the key idea (the split, then the payoff).
// Soft UI cues only on actions that carry meaning. No random(): noise comes from a seeded generator.
(function(){
  const SR=48000,DUR=45,BPM=96,BEAT=60/BPM;
  const rngf=seed=>{let a=seed>>>0;return()=>{a=(a+0x6d2b79f5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};};
  window.renderAudio=async function(){
    const ctx=new OfflineAudioContext(1,SR*DUR,SR);
    const T=window.TIMELINE.cues;
    const master=ctx.createGain();master.gain.setValueAtTime(0.0001,0);master.gain.linearRampToValueAtTime(1,1.5);master.gain.setValueAtTime(1,DUR-1.4);master.gain.linearRampToValueAtTime(0.0001,DUR);
    const comp=ctx.createDynamicsCompressor();comp.threshold.value=-24;comp.ratio.value=3;comp.attack.value=.01;comp.release.value=.25;
    master.connect(comp);comp.connect(ctx.destination);
    const nb=ctx.createBuffer(1,SR*2,SR),nd=nb.getChannelData(0),rn=rngf(77);for(let i=0;i<nd.length;i++)nd[i]=rn()*2-1;
    function tone(f,t0,d,o={}){const type=o.type||'sine',g=o.gain||.05,a=o.attack||.005,r=o.release||d*.8;
      const os=ctx.createOscillator(),gn=ctx.createGain();os.type=type;os.frequency.setValueAtTime(f,t0);if(o.glideTo)os.frequency.exponentialRampToValueAtTime(o.glideTo,t0+d);
      gn.gain.setValueAtTime(0.0001,t0);gn.gain.linearRampToValueAtTime(g,t0+a);gn.gain.exponentialRampToValueAtTime(0.0001,t0+Math.max(a+.01,r));
      let node=os;os.connect(gn);if(o.lp){const bq=ctx.createBiquadFilter();bq.type='lowpass';bq.frequency.value=o.lp;gn.connect(bq);bq.connect(master);}else gn.connect(master);
      os.start(t0);os.stop(t0+d+.05);}
    function hold(f,t0,d,o={}){const type=o.type||'triangle',g=o.gain||.03,a=o.attack||1.2,r=o.release||1.4;
      const os=ctx.createOscillator(),gn=ctx.createGain(),bq=ctx.createBiquadFilter();os.type=type;os.frequency.value=f;bq.type='lowpass';bq.frequency.value=o.lp||1000;
      gn.gain.setValueAtTime(0.0001,t0);gn.gain.linearRampToValueAtTime(g,t0+a);gn.gain.setValueAtTime(g,t0+d-r);gn.gain.linearRampToValueAtTime(0.0001,t0+d);
      os.connect(gn);gn.connect(bq);bq.connect(master);os.start(t0);os.stop(t0+d+.05);}
    function noise(t0,d,o={}){const src=ctx.createBufferSource(),gn=ctx.createGain(),bq=ctx.createBiquadFilter();src.buffer=nb;bq.type=o.type||'bandpass';bq.frequency.setValueAtTime(o.f||1500,t0);if(o.sweep)bq.frequency.exponentialRampToValueAtTime(o.sweep,t0+d);bq.Q.value=o.q||1.2;
      gn.gain.setValueAtTime(0.0001,t0);gn.gain.linearRampToValueAtTime(o.gain||.05,t0+(o.attack||.01));gn.gain.exponentialRampToValueAtTime(0.0001,t0+d);src.connect(bq);bq.connect(gn);gn.connect(master);src.start(t0,0,d+.05);}
    // ---- bed: slow chords on a 5 s grid (8 beats), bass root, a quiet pulse on every beat ----
    const CH=[[146.83,185,220,277.18],[123.47,146.83,185,220],[98,123.47,146.83,185],[110,138.59,164.81,196]],ROOT=[73.42,61.74,49,55];
    for(let k=0;k<9;k++){const t0=k*8*BEAT,c=CH[k%4];c.forEach((f,i)=>hold(f*(i%2?1:1),t0,8*BEAT+.4,{gain:.026,lp:900,attack:1.4,release:1.6,type:'triangle'}));
      hold(ROOT[k%4],t0,8*BEAT+.3,{type:'sine',gain:.07,attack:.8,release:1.2,lp:300});}
    for(let b=0;b<72;b++){const t=b*BEAT,lvl=t<16?.0:(t<34?.012:.016);if(lvl>0&&t>6)tone(b%2?392:293.66,t+BEAT/2,.18,{gain:lvl,type:'sine',release:.16});
      if(t>=16.4&&t<34.4)noise(t,.05,{type:'highpass',f:6500,gain:.006,q:.5});}
    // ---- the motif: D F# A E, returns at the split and again at the payoff ----
    const MOT=[293.66,369.99,440,659.25];
    const motif=t0=>MOT.forEach((f,i)=>{tone(f,t0+i*BEAT/2,.7,{type:'triangle',gain:.07,release:.65,lp:2600});tone(f*2,t0+i*BEAT/2,.3,{type:'sine',gain:.02,release:.28});});
    motif(T.split);motif(T.payoff);
    // ---- cues ----
    T.arrive.forEach(t=>tone(1800,t,.05,{gain:.03,release:.045}));                                                    // a signal arrives
    T.reveal.forEach((t,i)=>tone([587.33,739.99,880,987.77][i],t,.5,{type:'triangle',gain:.05,release:.45,lp:2800}));  // each agent is named
    noise(T.toFilter,.55,{f:700,sweep:2600,gain:.045,attack:.15,q:.8});                                               // five tickets move on
    T.rejects.forEach(t=>{tone(196,t,.16,{gain:.11,release:.14});noise(t,.05,{type:'lowpass',f:900,gain:.05,q:.5});});  // a no
    tone(880,T.passFilter,.4,{gain:.06,release:.35,type:'triangle'});tone(1318.51,T.passFilter+.09,.5,{gain:.05,release:.45,type:'triangle'});   // two pass the filter
    tone(1046.5,T.sized,.45,{gain:.06,release:.4,type:'triangle'});                                                  // sized
    [523.25,659.25,783.99].forEach((f,i)=>tone(f,T.order+i*.07,1.2,{gain:.07,release:1.1,type:'triangle',lp:2600}));    // the one order leaves
    tone(620,T.merge,1.6,{gain:.05,release:1.5,glideTo:180,type:'sine'});tone(310,T.merge,1.6,{gain:.025,release:1.5,glideTo:90,type:'triangle'});  // risk folds into execute
    tone(90,T.replayOrder,.35,{gain:.16,release:.32});noise(T.replayOrder,.25,{type:'lowpass',f:500,gain:.05,q:.4});    // an order nobody checked
    tone(587.33,T.replayOrder,.9,{gain:.025,release:.85,type:'triangle'});tone(622.25,T.replayOrder,.9,{gain:.02,release:.85,type:'triangle'});   // a small clash
    [293.66,369.99,440,587.33].forEach((f,i)=>hold(f,T.union,DUR-T.union,{gain:.03,attack:.9,release:1.3,lp:1800,type:'triangle'}));                    // resolve
    const buf=await ctx.startRendering();const ch=buf.getChannelData(0);
    // cap and convert to 16-bit PCM, base64 in chunks
    let peak=0;for(let i=0;i<ch.length;i++){const a=Math.abs(ch[i]);if(a>peak)peak=a;}
    const out=new Int16Array(ch.length);const g=peak>0?0.89/peak:1;for(let i=0;i<ch.length;i++)out[i]=Math.max(-32767,Math.min(32767,Math.round(ch[i]*g*32767)));
    const bytes=new Uint8Array(out.buffer);let s='';for(let i=0;i<bytes.length;i+=0x8000)s+=String.fromCharCode.apply(null,bytes.subarray(i,i+0x8000));
    return{sampleRate:SR,b64:btoa(s)};
  };
})();

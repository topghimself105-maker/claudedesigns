// ICT-style scanner on a scripted synthetic session. Candles are scripted; every annotation is DETECTED from them.
(function (root) {
  function rng(seed){let a=seed>>>0;return function(){a=(a+0x6d2b79f5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
  const N = 108, START_MIN = 20*60, TF = 5;               // 5m candles, 20:00 -> 05:00 New York time
  const PLAYBOOK = { name: 'ICT · LONDON SWEEP', version: 'v0', killzone: [2*60, 5*60], eqTol: 1.5, minBodyX: 1.8, riskPct: 0.5, oteLo: 0.62, oteHi: 0.79, pdh: 21520, stopBuffer: 3 };

  function candles() {
    const r = rng(11), C = [];
    let prev = 21405;
    for (let i = 0; i < N; i++) {
      let o = prev, c, h, l;
      if (i < 48) { const mid = 21405 + 22*Math.sin(i*2*Math.PI/26) + (r()-.5)*3; c = mid; }
      else if (i < 70) { c = 21404 - (i-48)*0.45 + 3*Math.sin(i*.9) + (r()-.5)*2; }
      else c = o;
      h = Math.max(o, c) + 1 + r()*3; l = Math.min(o, c) - 1 - r()*3;
      if (i < 70) { h = Math.min(h, i<48?21429:21409); l = Math.max(l, 21382); c = Math.min(Math.max(c, l), h); }
      C.push({ o, h, l, c }); prev = C[i].c;
    }
    const set = (i, o, h, l, c) => { C[i] = { o, h, l, c }; };
    // equal lows (SSL) and equal highs (BSL) of the Asia range
    C[19].l = 21380.0; C[45].l = 21380.6; C[6].h = 21430.0; C[32].h = 21430.8;
    [[46,21384,21393,21382,21392],[47,21392,21403,21390,21402],[48,21402,21413,21400,21412],[49,21412,21426,21410,21424]].forEach(a => set(...a));
    // fake BSL sweep at 00:10 (outside the killzone, no displacement after)
    set(50, 21424, 21436, 21422, 21424); [[51,21424,21425,21419,21420],[52,21420,21422,21414,21415],[53,21415,21417,21410,21411],[54,21411,21414,21407,21409]].forEach(a => set(...a));
    // run-in, lower swing high at 02:05 (idx 73), sweep of equal lows at 02:25 (idx 77)
    [[70,21393,21396,21389,21391],[71,21391,21394,21388,21390],[72,21390,21394,21387,21392],[73,21392,21397,21390,21395],
     [74,21395,21395.5,21388,21389],[75,21389,21392,21386,21387],[76,21387,21390,21384,21385],[77,21385,21388,21371,21386],
     [78,21386,21390,21378,21381],                                   // last down candle = order block
     [79,21381,21404,21380,21402],[80,21402,21436,21400,21433],[81,21433,21452,21421,21449],[82,21449,21466,21440,21460],  // displacement leg
     [83,21460,21462,21438,21440],[84,21440,21442,21423,21425],[85,21425,21427,21412,21415],[86,21415,21417,21403,21408]  // retrace into FVG + OTE
    ].forEach(a => set(...a));
    const run = [21422,21436,21431,21445,21452,21448,21462,21470,21466,21480,21488,21484,21496,21503,21499,21511,21516,21518,21516,21514,21517];
    let pc = 21408; run.forEach((cl, k) => { const i = 87 + k; if (i >= N) return; const rr = rng(100+i); set(i, pc, Math.max(pc, cl) + 2 + rr()*2, Math.min(pc, cl) - 2 - rr()*2, cl); pc = cl; });
    C[104].h = 21521; C[104].c = 21518;
    return C;
  }
  const hm = i => { i = Math.floor(i + 1e-9); const m = (START_MIN + i*TF) % 1440; return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0'); };
  const price = v => v.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 1 });

  function detect(C) {
    const P = PLAYBOOK, ev = [], out = { C, ev, P };
    const inKZ = i => { const m = (START_MIN + i*TF) % 1440; return m >= P.killzone[0] && m < P.killzone[1]; };
    // swings (fractal 2)
    const swH = [], swL = [];
    for (let i = 2; i < N-2; i++) {
      if (C[i].h > Math.max(C[i-1].h, C[i-2].h, C[i+1].h, C[i+2].h)) swH.push(i);
      if (C[i].l < Math.min(C[i-1].l, C[i-2].l, C[i+1].l, C[i+2].l)) swL.push(i);
    }
    const eq = (list, key) => { const g = []; for (let a = 0; a < list.length; a++) for (let b = a+1; b < list.length; b++) if (list[b] < 72 && Math.abs(C[list[a]][key] - C[list[b]][key]) <= P.eqTol) g.push([list[a], list[b]]); return g; };
    const eqL = eq(swL, 'l'), eqH = eq(swH, 'h');
    out.ssl = eqL.length ? { a: eqL[0][0], b: eqL[0][1], level: Math.min(C[eqL[0][0]].l, C[eqL[0][1]].l) + 0.3 } : null;
    out.bsl = eqH.length ? { a: eqH[0][0], b: eqH[0][1], level: Math.max(C[eqH[0][0]].h, C[eqH[0][1]].h) - 0.4 } : null;
    out.killzoneOpen = START_MIN + 0; out.kzIdx = [0..N].length && Array.from({length:N},(_,i)=>i).find(inKZ);
    const avgBody = i => { let s = 0, k = 0; for (let j = Math.max(0, i-20); j < i; j++) { s += Math.abs(C[j].c - C[j].o); k++; } return s / Math.max(1, k); };
    // sweeps
    const sweeps = [];
    for (let i = 20; i < N; i++) {
      if (out.ssl && i > out.ssl.b && C[i].l < out.ssl.level && C[i].c > out.ssl.level && !sweeps.some(s => s.side === 'SSL')) sweeps.push({ i, side: 'SSL', level: out.ssl.level, ext: C[i].l });
      if (out.bsl && i > out.bsl.b && C[i].h > out.bsl.level && C[i].c < out.bsl.level && !sweeps.some(s => s.side === 'BSL')) sweeps.push({ i, side: 'BSL', level: out.bsl.level, ext: C[i].h });
    }
    for (const s of sweeps) {
      const lastSwing = s.side === 'SSL' ? [...swH].reverse().find(j => j + 2 < s.i) : [...swL].reverse().find(j => j + 2 < s.i);
      let mss = null;
      for (let j = s.i + 1; j <= s.i + 6 && j < N; j++) {
        const body = Math.abs(C[j].c - C[j].o) >= P.minBodyX * avgBody(j);
        if (s.side === 'SSL' && C[j].c > C[lastSwing].h && body) { mss = j; break; }
        if (s.side === 'BSL' && C[j].c < C[lastSwing].l && body) { mss = j; break; }
      }
      s.swing = lastSwing; s.mss = mss; s.kz = inKZ(s.i); s.valid = !!mss && s.kz;
      ev.push({ i: s.i, kind: 'sweep', side: s.side, valid: s.valid, text: `${s.side} SWEEP ${price(s.ext)}`, why: s.valid ? 'back inside, MSS follows' : (!s.kz ? 'outside killzone' : '') + (!mss ? (s.kz ? '' : ' · ') + 'no MSS' : '') });
    }
    out.sweeps = sweeps;
    const S = sweeps.find(s => s.valid);
    if (S) {
      out.sweep = S; out.mss = S.mss;
      ev.push({ i: S.mss, kind: 'mss', valid: true, text: `MSS ${price(C[S.swing].h)} broken`, why: 'displacement close' });
      // FVGs created during the displacement, keep the largest
      const fv = [];
      for (let i = S.mss - 1; i <= S.mss + 3; i++) if (C[i+1].l > C[i-1].h) fv.push({ i, lo: C[i-1].h, hi: C[i+1].l, size: C[i+1].l - C[i-1].h });
      out.fvg = fv.sort((a, b) => b.size - a.size)[0];
      // order block = last down-close candle before the displacement
      let ob = S.mss - 1; while (C[ob].c >= C[ob].o) ob--; out.ob = { i: ob, lo: C[ob].l, hi: C[ob].h };
      // impulse leg and OTE
      const legHi = swH.find(j => j > S.mss); out.leg = { lo: S.ext, hi: C[legHi].h, i: legHi };
      const f = r => out.leg.hi - r * (out.leg.hi - out.leg.lo);
      out.ote = { lo: f(P.oteHi), hi: f(P.oteLo) };
      const ovLo = Math.max(out.ote.lo, out.fvg.lo), ovHi = Math.min(out.ote.hi, out.fvg.hi);
      out.entry = Math.round((ovLo + ovHi) / 2); out.stop = Math.round(S.ext - P.stopBuffer); out.tp = P.pdh;
      out.risk = out.entry - out.stop; out.rr = (out.tp - out.entry) / out.risk;
      out.stageIdx = legHi + 2;
      out.fillIdx = (() => { for (let j = legHi + 1; j < N; j++) if (C[j].l <= out.entry) return j; })();
      out.tpIdx = (() => { for (let j = out.fillIdx; j < N; j++) { if (C[j].l <= out.stop) return -1; if (C[j].h >= out.tp) return j; } })();
      ev.push({ i: out.fvg.i + 1, kind: 'fvg', valid: true, text: `FVG ${price(out.fvg.lo)}-${price(out.fvg.hi)}`, why: 'gap left by displacement' });
      ev.push({ i: out.stageIdx, kind: 'stage', valid: true, text: `LONG ${price(out.entry)} staged`, why: `SL ${price(out.stop)} · TP ${price(out.tp)}` });
      ev.push({ i: out.fillIdx, kind: 'fill', valid: true, text: `FILLED ${price(out.entry)}`, why: 'limit touched' });
      ev.push({ i: out.tpIdx, kind: 'tp', valid: true, text: `TARGET ${price(out.tp)} hit`, why: `+${out.rr.toFixed(1)}R` });
    }
    ev.sort((a, b) => a.i - b.i);
    out.inKZ = inKZ;
    return out;
  }
  // time <-> candle head mapping (seconds -> fractional candle count)
  const KEYS = [[0.3,0],[3.5,24],[6.5,50.6],[9.0,72],[11.0,77.8],[12.2,79.9],[13.5,82.9],[15.5,84.9],[17.0,86.9],[19.0,91],[24.0,104.9],[25.5,107.99]];
  function headAt(t) { if (t <= KEYS[0][0]) return 0; for (let k = 1; k < KEYS.length; k++) if (t <= KEYS[k][0]) { const [t0,h0] = KEYS[k-1], [t1,h1] = KEYS[k]; return h0 + (h1-h0) * (t-t0)/(t1-t0); } return KEYS[KEYS.length-1][1]; }
  function timeAt(h) { for (let k = 1; k < KEYS.length; k++) if (h <= KEYS[k][1]) { const [t0,h0] = KEYS[k-1], [t1,h1] = KEYS[k]; return t0 + (t1-t0) * (h-h0)/(h1-h0); } return KEYS[KEYS.length-1][0]; }
  const CAPTIONS = [
    [0.3, 4.0, ['ICT looks like art.', 'A bot reads it as rules.']],
    [4.1, 6.4, ['First: mark the liquidity.']],
    [6.5, 8.9, ['Sweep outside the killzone? Skip.']],
    [9.0, 10.9, ['London opens. The bot arms.']],
    [11.0, 12.1, ['Stops swept. Price snaps back.']],
    [12.2, 13.4, ['Structure shifts. Displacement.']],
    [13.5, 15.4, ['Gap and retrace line up.']],
    [15.5, 16.9, ['Bot stages the order.', 'You sign.']],
    [17.0, 23.9, ['Fixed risk. Target three R.']],
    [24.0, 28.0, ['One trade. Six checks passed.']],
    [28.1, 32.0, ['Never let the bot place the order.', 'You sign.']]
  ];
  const api = { rng, candles, detect, hm, price, headAt, timeAt, CAPTIONS, N, START_MIN, TF, PLAYBOOK, DURATION: 32 };
  if (typeof module !== 'undefined') module.exports = api; else root.SIM2 = api;
})(typeof window !== 'undefined' ? window : globalThis);

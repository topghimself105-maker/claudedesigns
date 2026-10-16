// F369 engine: a scripted 24 h NQ-like day (288 x 5m candles, 18:00 -> 18:00 New York time) and the detectors that read it.
// Every annotation on screen is DETECTED here, not placed by hand. Prices are simulated.
(function (root) {
  function rng(seed){let a=seed>>>0;return function(){a=(a+0x6d2b79f5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
  const N = 288, START_MIN = 18 * 60, TF = 5;
  const RULES = { eqTol: 1.5, minBodyX: 1.8, risk: 0.005, rr: 5, equity: 100000, stopBuf: 3, ptValue: 2,
    // New York time, 90-minute cycles: 3 per session, none for Asia (owner rule). [open minute, name]
    sessions: [[120, 'LDN'], [420, 'NY']], cycleMin: 90, cycles: 3 };
  const hm = i => { i = Math.floor(i + 1e-9); const m = (START_MIN + i * TF) % 1440; return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0'); };
  const price = v => v.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 1 });

  function candles() {
    const r = rng(23), C = []; let prev = 21400;
    const set = (i, o, h, l, c) => { C[i] = { o, h, l, c }; };
    for (let i = 0; i < N; i++) {
      let o = prev, c;
      if (i < 24) c = 21400 + 6 * Math.sin(i / 3) + (r() - .5) * 3;
      else if (i < 72) c = 21405 + 22 * Math.sin((i - 24) * 2 * Math.PI / 26) + (r() - .5) * 3;
      else if (i < 94) c = 21404 - (i - 72) * .45 + 3 * Math.sin(i * .9) + (r() - .5) * 2;
      else c = o;
      let h = Math.max(o, c) + 1 + r() * 3, l = Math.min(o, c) - 1 - r() * 3;
      if (i >= 24 && i < 72) { h = Math.min(h, 21429); l = Math.max(l, 21382); c = Math.min(Math.max(c, l), h); }
      if (i >= 72 && i < 94) { h = Math.min(h, 21409); l = Math.max(l, 21382); c = Math.min(Math.max(c, l), h); }
      C.push({ o, h, l, c }); prev = C[i].c;
    }
    // Asia: equal highs (BSL) and equal lows (SSL)
    C[43].l = 21380.0; C[69].l = 21380.6; C[30].h = 21430.0; C[56].h = 21430.8;
    // set A: the London setup. 94..100 run-in with a down run, 101 sweep, 102 order block, 103 CSD, 104 displacement + MSS, 105 FVG, 106 leg high, 107..110 retrace
    const A = [[94,21393,21396,21389,21391],[95,21391,21394,21388,21390],[96,21390,21394,21387,21392],[97,21392,21397,21390,21395],
      [98,21395,21395.5,21388,21389],[99,21389,21392,21386,21387],[100,21387,21390,21384,21385],
      [101,21385,21388,21371,21386],[102,21386,21390,21378,21381],[103,21381,21396,21380,21395.5],[104,21395.5,21436,21394,21433],
      [105,21433,21452,21416,21449],[106,21449,21466,21440,21460],[107,21460,21462,21438,21440],[108,21440,21442,21423,21425],
      [109,21425,21427,21412,21415],[110,21415,21417,21403,21408]];
    A.forEach(a => set(...a));
    // the run to the opposing BSL (5R target)
    const run = [21422,21440,21436,21458,21470,21466,21488,21500,21496,21520,21534,21528,21552,21566,21560,21580,21588,21584,21594,21592];
    let pc = 21408; run.forEach((cl, k) => { const i = 111 + k, rr = rng(500 + i); set(i, pc, Math.max(pc, cl) + 2 + rr()*2, Math.min(pc, cl) - 2 - rr()*2, cl); pc = cl; });
    C[130].h = 21597;
    // after the target: pullback, NY session range, drift into the afternoon
    for (let i = 131; i < 196; i++) { const rr = rng(900 + i), o = pc, tgt = i < 156 ? 21566 : 21556 + 14*Math.sin((i-156)*2*Math.PI/23), c = o + (tgt - o) * .22 + (rr() - .5) * 4; set(i, o, Math.max(o, c) + 1 + rr()*3, Math.min(o, c) - 1 - rr()*3, c); pc = c; }
    // set B: the SAME pattern, 123 candles later and 150 points higher, outside every 90 m window (12:40 NY)
    for (let i = 196; i < 217; i++) { const rr = rng(1300 + i), o = pc, tgt = 21545 + 14*Math.sin((i-196)*2*Math.PI/18), c = o + (tgt - o) * .3 + (rr() - .5) * 3; let h = Math.max(o, c) + 1 + rr()*3, l = Math.min(o, c) - 1 - rr()*3; l = Math.max(l, 21531.5); h = Math.min(h, 21579); set(i, o, h, l, Math.min(Math.max(c, l), h)); pc = C[i].c; }
    C[200].l = 21530.0; C[212].l = 21530.6; C[206].h = 21580.0;
    A.forEach(a => set(a[0] + 123, a[1] + 150, a[2] + 150, a[3] + 150, a[4] + 150));
    // the first pattern-B candle after the run-in connects to the range
    C[217].o = C[216].c;
    for (let i = 234; i < 262; i++) { const rr = rng(1700 + i), o = i === 234 ? C[233].c : pc, tgt = 21625 + 10*Math.sin((i-234)*.5), c = o + (tgt - o) * .25 + (rr() - .5) * 4; set(i, o, Math.max(o, c) + 1 + rr()*3, Math.min(o, c) - 1 - rr()*3, c); pc = c; }
    // set C: a RUN of equal highs (BSL 21,640): closes through the level and keeps going
    C[240].h = 21640.0; C[247].h = 21640.6;
    set(250, 21632, 21641, 21630, 21640); set(251, 21640, 21654, 21638, 21652); set(252, 21652, 21666, 21650, 21664); set(253, 21664, 21678, 21662, 21676); set(254, 21676, 21690, 21674, 21688);
    pc = 21688; for (let i = 255; i < N; i++) { const rr = rng(2100 + i), o = pc, c = o + (21660 - o) * .12 + (rr() - .5) * 6; set(i, o, Math.max(o, c) + 1 + rr()*3, Math.min(o, c) - 1 - rr()*3, c); pc = c; }
    for (let i = 1; i < N; i++) if (!(i >= 94 && i <= 110) && !(i >= 217 && i <= 233) && !(i >= 250 && i <= 254)) C[i].o = C[i - 1].c;
    for (let i = 0; i < N; i++) { const c = C[i]; c.h = Math.max(c.h, c.o, c.c); c.l = Math.min(c.l, c.o, c.c); }
    return C;
  }

  // ---- time validity: 90-minute cycles, 3 per session (London, New York), none for Asia -------------------------------
  function windowAt(i) { const m = (START_MIN + i * TF) % 1440;
    for (const [open, name] of RULES.sessions) { const since = m - open; if (since >= 0 && since < RULES.cycleMin * RULES.cycles) return { ok: true, ses: name, cyc: Math.floor(since / RULES.cycleMin) + 1, since }; }
    return { ok: false, ses: m >= 1200 || m < 0 ? 'ASIA' : '--', cyc: 0, since: 0 }; }

  function detect(C) {
    const out = { C, setups: [], runs: [] }, P = RULES;
    const swH = [], swL = [];
    for (let i = 2; i < N - 2; i++) {
      if (C[i].h > Math.max(C[i-1].h, C[i-2].h, C[i+1].h, C[i+2].h)) swH.push(i);
      if (C[i].l < Math.min(C[i-1].l, C[i-2].l, C[i+1].l, C[i+2].l)) swL.push(i);
    }
    const avgBody = i => { let s = 0, k = 0; for (let j = Math.max(0, i - 20); j < i; j++) { s += Math.abs(C[j].c - C[j].o); k++; } return s / Math.max(1, k); };
    const prom = (key, sign) => { const L = []; for (let i = 6; i < N - 6; i++) { let ok = true; for (let d = 1; d <= 6; d++) if (sign > 0 ? !(C[i][key] > C[i-d][key] && C[i][key] > C[i+d][key]) : !(C[i][key] < C[i-d][key] && C[i][key] < C[i+d][key])) { ok = false; break; } if (ok) L.push(i); } return L; };
    const pools = (list, key, sign) => { const g = []; for (let a = 0; a < list.length; a++) for (let b = a + 1; b < list.length; b++) if (Math.abs(C[list[a]][key] - C[list[b]][key]) <= P.eqTol && list[b] - list[a] > 8 && !C.slice(list[a], list[b] + 1).some(c => sign > 0 ? c.h > C[list[a]][key] + .9 : c.l < C[list[a]][key] - .9)) g.push({ a: list[a], b: list[b], level: sign > 0 ? Math.max(C[list[a]].h, C[list[b]].h) - .4 : Math.min(C[list[a]].l, C[list[b]].l) + .3 }); return g; };
    out.ssl = pools(prom('l', -1), 'l', -1); out.bsl = pools(prom('h', 1), 'h', 1);
    // SSL events: sweep (wick through, close back inside) vs run (close through and stays)
    const used = new Set();
    for (const pl of out.ssl) { for (let i = pl.b + 3; i < N; i++) { if (used.has(pl.level)) break;
      if (C[i].l < pl.level && C[i].c > pl.level) {
        used.add(pl.level);
        const s = { pool: pl, sweep: i, ext: C[i].l };
        // CSD: first close above the open of the down-run that led into the sweep
        let k = i - 1; while (k > 0 && C[k].c < C[k].o) k--; const runStart = k + 1; s.csdLevel = C[runStart].o;
        for (let j = i + 1; j < i + 8; j++) if (C[j].c > s.csdLevel) { s.csd = j; break; }
        const sh = [...swH].reverse().find(j => j + 2 < i); s.swingHigh = sh;
        for (let j = i + 1; j < i + 8; j++) if (C[j].c > C[sh].h && Math.abs(C[j].c - C[j].o) >= P.minBodyX * avgBody(j)) { s.mss = j; s.disp = j; break; }
        if (s.mss != null) {
          s.fvg = null; for (let j = s.mss - 1; j <= s.mss + 2; j++) if (C[j + 1].l > C[j - 1].h) { const f = { i: j, lo: C[j - 1].h, hi: C[j + 1].l }; if (!s.fvg || f.hi - f.lo > s.fvg.hi - s.fvg.lo) s.fvg = f; }
          let ob = s.mss - 1; while (C[ob].c >= C[ob].o) ob--; s.ob = { i: ob, lo: C[ob].l, hi: C[ob].h };
          const lh = swH.find(j => j > s.mss); s.leg = { lo: s.ext, hi: C[lh].h, i: lh }; s.eq = (s.leg.lo + s.leg.hi) / 2;
          if (s.fvg) { s.fvg.mid = (s.fvg.lo + s.fvg.hi) / 2; s.fvg.discount = s.fvg.hi <= s.eq; }
          s.entry = Math.round(s.fvg.mid); s.stop = Math.round(s.ext - P.stopBuf); s.risk = s.entry - s.stop; s.tp = s.entry + P.rr * s.risk; s.rr = (s.tp - s.entry) / s.risk;
          s.fill = (() => { for (let j = lh + 1; j < N; j++) if (C[j].l <= s.entry) return j; })();
          s.tpIdx = (() => { for (let j = s.fill; j < N; j++) { if (C[j].l <= s.stop) return -1; if (C[j].h >= s.tp) return j; } return -1; })();
          s.win = windowAt(s.sweep);
          s.chain = [s.win.ok, true, true, true, s.csd != null, s.disp != null, s.mss != null, !!(s.fvg && s.fvg.discount), true, s.tpIdx > 0];
          s.take = s.chain.every(Boolean);
        }
        if (s.mss != null && s.fvg) out.setups.push(s); break;
      }
      if (C[i].c < pl.level - 3 && C[i + 1] && C[i + 1].c < pl.level - 3) break; } }
    // BSL events: run (close above the level, keeps going)
    for (const pl of out.bsl) for (let i = pl.b + 3; i < N - 3; i++) { if (C[i].c > pl.level + 3 && C[i + 1].c > C[i].c && C[i + 2].c > C[i + 1].c) { out.runs.push({ pool: pl, run: i, side: 'BSL' }); break; } }
    out.windowAt = windowAt;
    // risk math, consistent everywhere
    const s = out.setups.find(x => x.take);
    if (s) { const risk$ = P.equity * P.risk, perPt = risk$ / s.risk, contracts = Math.floor(perPt / P.ptValue); out.math = { equity: P.equity, riskPct: P.risk, riskUsd: risk$, entry: s.entry, stop: s.stop, tp: s.tp, risk: s.risk, perPt, contractsRaw: perPt / P.ptValue, contracts, actualRisk: contracts * s.risk * P.ptValue, rr: s.rr }; }
    return out;
  }
  const api = { rng, candles, detect, windowAt, hm, price, N, START_MIN, TF, RULES };
  if (typeof module !== 'undefined') module.exports = api; else root.SIM3 = api;
})(typeof window !== 'undefined' ? window : globalThis);

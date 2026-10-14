// Deterministic simulation: every number on screen comes from here. Pure function of (seed, t).
(function (root) {
  function rng(seed) { // mulberry32
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const DURATION = 31;
  const FALL = 5.0;                 // seconds from spawn to the execute line
  const GATE_FRAC = [0.30, 0.52, 0.72]; // filter, risk, (third = size) -> mapped below
  // gate fractions of the fall: 1 FILTER, 2 RISK, 3 EXECUTE is the bottom
  const GATES = [0.34, 0.66];       // fractions of fall for FILTER and RISK
  const T_OFF = 21.0, T_ON = 27.5;  // risk gate bypassed in [T_OFF, T_ON)
  const NAMES = ['SIGNAL', 'FILTER', 'RISK GATE', 'EXECUTE'];
  const REASONS = [
    null,
    ['spread too wide', 'volume too low', 'stale price', 'outside session', 'news window'],
    ['daily loss cap', 'correlated position', 'size over limit', 'max open trades']
  ];

  function passP(gate, tc) { // pass probability for gate 0=filter,1=risk at crossing time tc
    if (gate === 0) return 0.35;
    return (tc >= T_OFF && tc < T_ON) ? 1.0 : 0.5;
  }

  function build(seed, N) {
    const r = rng(seed);
    const P = [];
    for (let i = 0; i < N; i++) {
      const ts = 2.2 + Math.pow(i / N, 0.92) * 28.0;
      const u = ((r() + r() + r()) / 3) * 2 - 1;
      const r0 = r(), r1 = r(), rw = r(), rd = r(), rs = r();
      const tc = [ts + FALL * GATES[0], ts + FALL * GATES[1]];
      const tex = ts + FALL;
      let fate = 'exec', k = -1;
      if (r0 >= passP(0, tc[0])) { fate = 'rej'; k = 0; }
      else if (r1 >= passP(1, tc[1])) { fate = 'rej'; k = 1; }
      const off = tex >= T_OFF && tex < T_ON;
      const win = rw < (off ? 0.38 : 0.6);
      const size = off ? 3 : 1;
      const pnl = win ? 1.0 * size : -0.8 * size;
      P.push({ i, ts, u, tc, tex, fate, k, win, size, pnl, dir: u >= 0 ? 1 : -1, rd, rs,
        reason: k > 0 ? REASONS[k][Math.floor(rs * REASONS[k].length)] : (k === 0 ? REASONS[1][Math.floor(rs * REASONS[1].length)] : null) });
    }
    const exec = P.filter(p => p.fate === 'exec').sort((a, b) => a.tex - b.tex);
    let eq = 0; exec.forEach(p => { eq += p.pnl; p.eq = eq; });
    return { P, exec, seed };
  }

  function stats(S, t) {
    const c = { signals: 0, filtRej: 0, filtPass: 0, riskRej: 0, riskPass: 0, exec: 0, eq: 0, peak: 0, dd: 0 };
    for (const p of S.P) {
      if (p.ts <= t) c.signals++;
      if (p.tc[0] <= t) { if (p.k === 0) c.filtRej++; else c.filtPass++; }
      if (p.k !== 0 && p.tc[1] <= t) { if (p.k === 1) c.riskRej++; else c.riskPass++; }
      if (p.fate === 'exec' && p.tex <= t) c.exec++;
    }
    let peak = 0, eq = 0;
    for (const p of S.exec) { if (p.tex > t) break; eq = p.eq; if (eq > peak) peak = eq; }
    c.eq = eq; c.peak = peak; c.dd = peak - eq;
    return c;
  }

  const CAPTIONS = [
    [0.3, 3.2, ['Your bot just saw hundreds of signals.']],
    [3.3, 6.8, ['Every one meets the same gates.']],
    [6.9, 11.0, ['Signal. Filter. Risk gate. Execute.']],
    [11.1, 18.8, ['Most die at the filter.', 'Half of the rest, at risk.']],
    [18.9, 20.9, ['Rejected is the bot doing its job.']],
    [21.0, 24.8, ['Now switch the risk gate off.']],
    [24.9, 27.4, ['More trades. Bigger size. Drawdown.']],
    [27.5, 31.0, ['Gate back on.', 'The edge is what it refuses.']]
  ];

  const api = { rng, build, stats, DURATION, FALL, GATES, T_OFF, T_ON, NAMES, REASONS, CAPTIONS, N: 420, SEED: 19 };
  if (typeof module !== 'undefined') module.exports = api; else root.SIM = api;
})(typeof window !== 'undefined' ? window : globalThis);

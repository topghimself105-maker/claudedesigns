# Decisions (creative calls made without asking)
- Topic: "what a trading bot refuses" (signal -> filter -> risk gate -> execute). Chosen because it is one idea, visual, and corrects a common belief that more trades means more edge.
- Audience: people curious about trading automation. Outcome: they can name the gates and know the risk gate is what protects the account.
- Direction A (funnel) wins; B, C, D are kept as notes in directions.html.
- Core metaphor object: the funnel. It stays on screen the whole film; only the camera, gate colours and counters change.
- One accent (lime) for pass/win, amber for rejected, red only for danger/loss.
- All numbers come from a seeded simulation (seed 19). The seed was chosen so the story reads clearly (steady gains, then a drawdown with the risk gate off). That makes the sim an illustration, not evidence. It is labelled "simulated" on every frame.
- Frame rate 30 fps (references run 30-60). Raise in studio/render.mjs if wanted.
- Voiceover: none. Burned-in captions + score + .srt, since X autoplay is muted.

## Film 2: ict-desk (ICT London sweep scanner)
- Idea: ICT looks like art, but a bot can read it as an ordered rule list; the human signs the order. One idea, one dense HUD.
- Price data is scripted (it has to contain the setup) but every annotation (equal highs/lows, sweeps, MSS, FVG, order block, OTE, entry, target) is DETECTED by sim.js from the candles, not hand-placed. A skipped fake sweep at 00:10 shows the scanner rejecting a look-alike.
- ICT conventions used: London killzone 02:00-05:00 New York, Asia range 20:00-00:00, previous-day high as target. These are widely taught conventions, not proof of edge.
- 4:5 master (best on the X feed) and 16:9 (YouTube); reduced-motion cut for 4:5.
- Frank369: rules unknown to the studio, so playbooks/frank369.json is a labelled placeholder. Nothing in the film claims to be their method.
- "Still unverified" panel is deliberately honest: news calendar, spread, HTF bias and the single-day sample are not checked.

## Film 3: ship-line (explainer-film baseline, vortex look)
- Brief: "remake this one with the baseline". Reference = the green vortex build-desk video. Owner chose: the VIDEO's look wins over the baseline's visual bans (no neon / particles); topic = automation crew shipping work; own brand, none of the reference's names, text or numbers.
- One idea: a crew of automated roles pushes thousands of tasks through gates; most are held, and that is why what ships stays clean. Hook belief: "automation = AI writes it and it ships".
- Turn: reviewer gate OFF -> more ships, more reverts. Payoff: gate back on, opening image read correctly, next step "add one gate to yours".
- 4:5 master only (the reference's native frame and the X feed); 16:9 / 9:16 / 1:1 recompositions are not built yet. 30 s, 60 fps, BT.709.
- Captions: reference has none; baseline requires them. Compromise: one large caption pill (34 px, readable at 390 px wide) plus captions.srt; HUD text stays small and decorative.
- Flashes: ship bursts de-duplicated to at most 2.5 per second. Reduced-motion cut: fixed camera, weaker flashes, no strobing.
- Score: clean generated bed (sub, pad, soft pulse, A-minor motif that returns on "gate back on"), UI cues only on role intros, ships, gate off/on. No strings/brass this time.
- Disclaimer line kept at the bottom (channel is trading-adjacent) even though the topic is not trading.

## Film 4: f369-engine (brand film, explainer-film baseline with owner overrides)
- Overrides from the owner: brand look and the ink craft level override the baseline visual bans (glow and radial streaks are brand). Music = ONLY the supplied track (Janji - Heroes Tonight, NCS), no generated music or sound effects.
- One idea: ICT liquidity, PD arrays and Frank369 timing are rules, not art: BSL/SSL rest orders, a sweep takes them, CSD + displacement + MSS confirm, the algo buys only from a discount PD array, and only inside the F369 time gate.
- 9:16 master (like the brand reference), 4:5 and 16:9 recompositions of the same film. 45 s = 24 bars at 128 bpm.
- Music cut: window starts at 38.955 s of the track so its silence-then-hit lands on 28.125 s (bar 15 = ORDER PLACED). Bass enters at bar 7, other energy shifts at bars 12, 16, 20. Fade-out starts 41.3 s under the end card. Mixed to -14 LUFS with a plain gain change (no limiter), 12 ms fade-in to avoid a click.
- Frank369 rules as given by the owner: "90m liq sweep, csd, mss, 0.5% risk, 5 rr". Interpretations (assumptions, change in sim.js if wrong): 90m window = 3 cycles per London (from 02:00) and New York (from 07:00) session, none for Asia; CSD = first close back through the open of the down-run that led into the sweep; target 5R = opposing BSL.
- 369 math (owner: "use also 369 math", rule not specified): implemented as the digit sum of the sweep time (HHMM). Digital root must be 3, 6 or 9. 02:25 = 0+2+2+5 = 9 passes; 12:40 = 1+2+4+0 = 7 fails. ASSUMPTION: this definition is mine; the owner never described it. It is isolated in sim.js (digits369) and shown in the ledger, cards, session routes panel and the answer plate. Numbers equal to 3, 6, 9 are highlighted in mint in the math.
- The brand reference video (refs/brand_f369.mp4) was never supplied; the look follows the owner's written description only.
- Prices are scripted/simulated; every annotation (sweep, run, CSD, displacement, MSS, FVG, dealing range, premium/discount, order, target, skip) is detected from the candles in sim.js.

## Film 5: nasdaq-flash (high-dopamine montage, owner's Hyperliquid-style reference)
- Reference = the supplied 12.6 s montage (cuts every 0.2-0.4 s, white flashes, glitch slices, order tickets, chart walls, big captions). Only the editing language is taken; none of its footage, people, articles or text.
- Owner: "real stocks and automations that we have used", Nasdaq stocks, "TradingView charts like in the video". Implemented as: 14 real Nasdaq tickers; the five automations we built in this studio shown with real frames captured from our own films (assets/); a pro-style dark chart drawn by us (no TradingView branding or data).
- No market-data access in this environment, so chart price action is ILLUSTRATIVE (seeded, indexed to 100, badge on screen) and no real quotes, P&L or results are shown. Order tickets show ticker + order type only.
- 30 s = 16 bars at 128 bpm, 16:9 (YouTube, as for the F369 film). Music = Heroes Tonight only; window starts at 59.58 s so the track's silence-then-hit lands at 7.5 s (beat 16) = the drop/flash.
- End card uses the owner's F369.AI brand mark.

- nasdaq-flash music change: owner replaced Heroes Tonight with Jeff Germita - IM SO LUCKY (HARDTEKK) (156 bpm, 89.3 s). Cut window starts at 55.426 s so the second drop (61.58 s, after a 12-bar breakdown) lands on beat 16 (6.15 s). Licence not stated by the owner: flagged, not assumed.

## Nasdaq Flash v2 (finetune)
- Every cut is >= 1 beat (0.385 s at 156 bpm), so flashes are never closer than that (owner asked ~0.30 s; whole beats keep cuts on the music grid).
- Build-up = the owner's four page lines, one per bar; drop = AUTOMATED.; Nasdaq fact cards; company edits (Google, Meta, Apple, Microsoft, Amazon, NVIDIA, Tesla, Netflix) with own graphics, illustrative charts, no logos.
- Facts to verify before publishing: Nasdaq founded 1971, Nasdaq-100 ~100 large non-financial companies, IPO years per company; "70%", "$300M / 0.006 s" are the owner's page texts.
- Layouts: 4x5 (X feed) and 16x9 (YouTube) from the same film file.

## Data to Order (film 6, X)
- Rebuilt to the supplied reference layout (HUD, 8 section tabs, crawler spider in a node nebula, six panels); grayscale like the reference, one mint accent only on the order ticket.
- 1080x1350 (4:5), 60 fps (owner wrote 165 Hz + 30 fps; X plays max 60 fps, owner chose 60), BT.709 limited range, silent.
- All trades, journal notes and stats are seeded and simulated (NQ); order sized from risk 0.5% / 25 pts / $20 per point = 1 contract; rules labelled example.

## Data to Order v2
- Clusters are now spheres (balls of information) joined by a route; the spider carries each sphere's key result in a CARRYING box and ends on ORDER FILLED (simulated fill 0.25 pt slippage).
- Music: owner-supplied Afro House mix, window 99.49 s -> 129.49 s, its drop at film 26.0 s = ORDER FILLED; -14.0 LUFS gain-only, peak -1.7 dBFS; 120 bpm, section cuts on the 0.5 s beat grid. Licence/credits unconfirmed.

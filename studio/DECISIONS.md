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

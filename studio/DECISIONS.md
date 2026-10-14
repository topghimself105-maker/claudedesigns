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

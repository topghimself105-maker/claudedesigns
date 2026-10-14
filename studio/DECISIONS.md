# Decisions (creative calls made without asking)
- Topic: "what a trading bot refuses" (signal -> filter -> risk gate -> execute). Chosen because it is one idea, visual, and corrects a common belief that more trades means more edge.
- Audience: people curious about trading automation. Outcome: they can name the gates and know the risk gate is what protects the account.
- Direction A (funnel) wins; B, C, D are kept as notes in directions.html.
- Core metaphor object: the funnel. It stays on screen the whole film; only the camera, gate colours and counters change.
- One accent (lime) for pass/win, amber for rejected, red only for danger/loss.
- All numbers come from a seeded simulation (seed 19). The seed was chosen so the story reads clearly (steady gains, then a drawdown with the risk gate off). That makes the sim an illustration, not evidence. It is labelled "simulated" on every frame.
- Frame rate 30 fps (references run 30-60). Raise in studio/render.mjs if wanted.
- Voiceover: none. Burned-in captions + score + .srt, since X autoplay is muted.

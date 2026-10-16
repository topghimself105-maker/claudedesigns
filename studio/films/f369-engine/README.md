# F369 engine (16:9 YouTube master)

Deliverable: `out/f369-engine_16x9_final.mp4` (1920x1080, 60 fps, 45 s, BT.709, 65.6 MB) with captions `out/f369-engine.srt` and description `out/f369-engine/DESCRIPTION.txt`.
Source: `studio/films/f369-engine/` (`index.html`, `sim.js`, `audio_map.js`). Re-render: `node studio/renderpar.mjs f369-engine 16x9 4 <audio.wav>`.

Music: Janji - Heroes Tonight (feat. Johnning) [NCS Release] — ncs.io/ht (the only audio in the film; no generated sound).

## Tested
- Frame determinism: the same frame rendered twice is byte-identical (t = 28.4 s).
- Video: 2,700 frames, 60 fps, 45.000 s, BT.709 limited range tagged; the four parallel segments join without a visible seam (PSNR at the joins matches the neighbouring frames).
- Audio: 45.0 s window of the track starting at 38.955 s, 12 ms fade-in, fade-out from 41.3 s; -14.0 LUFS integrated, sample peak -6.4 dBFS, no clipped samples; gain change only.
- Music sync, measured on the track: bass enters at bar 7; silence then hit at 28.1 s (= bar 15 = ORDER PLACED); other energy changes fall on bars 12, 16, 20.
- Logic: every annotation is detected from the simulated candles (sim.js). The 02:25 London setup passes all 10 checks (entry 21,406, stop 21,368, target 21,596, RR 5.00, 6 MNQ, risk $456). The same pattern at 12:40 fails only the F369 time check.
- Readability: a 390 px wide still of the 9:16 layout was read; the 16:9 layout was checked on stills only.

## Not tested
- Not listened to end to end by the maker; no muted/audio-only review; no design-review pass; no reduced-motion cut; 9:16 and 4:5 layouts exist in the code but were not rendered.
- `refs/brand_f369.mp4` was never supplied, so the brand match is from the written description only.

## Assumptions to confirm (see studio/DECISIONS.md)
- 369 math = digit sum of the sweep time must reduce to 3, 6 or 9 (02:25 -> 9 passes, 12:40 -> 7 fails). The owner did not define it.
- 90m window = 3 cycles per London (02:00) and New York (07:00) session, none for Asia; CSD = first close back through the open of the down-run before the sweep.

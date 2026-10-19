# Nasdaq Flash (16:9 YouTube master)

Deliverable: `out/nasdaq-flash_16x9_final.mp4` (1920x1080, 60 fps, 30 s, BT.709, 65 MB), `out/nasdaq-flash.srt`, `out/nasdaq-flash/DESCRIPTION.txt`.
Re-render: `node studio/renderpar.mjs nasdaq-flash 16x9 4 <audio.wav>`. Source: `index.html`, `audio_map.js`, `assets/` (frames of our own films).

Music: Jeff Germita — IM SO LUCKY (HARDTEKK) (file supplied by the owner; tag: ℗ void). RIGHTS/LICENCE NOT CONFIRMED: the owner has not stated the licence, so check it before publishing. Only this track is used (no generated sound).
The schedule is in beats; BPM is a constant at the top of index.html (156 for this track, drop at beat 16 = 6.15 s). A different track needs its tempo and drop re-measured (`?bpm=` overrides for tests).

## Tested
- Video: 1,800 frames, 60 fps, 30.000 s, BT.709 tagged, plays as h264/aac.
- Audio: 30 s window of the track from 55.426 s (bar 36 of the track), 12 ms fade-in, fade-out from 27.5 s; -14.0 LUFS integrated, sample peak -8.7 dBFS (measured on the final mp4), gain change only. Track tempo measured at 156.05 bpm; its second drop (bar 40, 61.58 s) lands at 6.15 s = beat 16 = the white-flash drop, after a 4-bar build.
- Stills at every beat type (text, chart, ticket, tape, grid, automation shot, counters, end card) were read.

## Not tested
- No full listen/watch by the maker, no muted/audio-only pass, no design review, no reduced-motion cut (the film is made of flashes: it is NOT suitable for photosensitive viewers; the 16 fps cut rate is above 3 flashes per second in places).
- Ticker listings (all believed Nasdaq) were not verified against a live source (no network).

## Honesty notes
- Charts are illustrative, seeded, indexed to 100 and badged ILLUSTRATIVE; no real quotes, P&L or results are shown.
- Automation shots are real frames of our own films; order tickets show ticker and order type only.

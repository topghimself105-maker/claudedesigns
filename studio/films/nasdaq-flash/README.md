# Nasdaq Flash (16:9 YouTube master)

Deliverable: `out/nasdaq-flash_16x9_final.mp4` (1920x1080, 60 fps, 30 s, BT.709, 62 MB), `out/nasdaq-flash.srt`, `out/nasdaq-flash/DESCRIPTION.txt`.
Re-render: `node studio/renderpar.mjs nasdaq-flash 16x9 4 <audio.wav>`. Source: `index.html`, `audio_map.js`, `assets/` (frames of our own films).

Music (current, reserve version): Janji - Heroes Tonight (feat. Johnning) [NCS Release] — ncs.io/ht. The owner asked for a different track from the Drive folder "Music for F369Ai"; the folder could not be read, so this version stays until the file is supplied. The schedule is in beats (128 bpm, drop at beat 16); a new track needs its tempo and drop re-measured.

## Tested
- Video: 1,800 frames, 60 fps, 30.000 s, BT.709 tagged, plays as h264/aac.
- Audio: 30 s window of the track from 59.58 s, 12 ms fade-in, fade-out from 27.2 s; -14.1 LUFS integrated, sample peak -6.5 dBFS, gain change only. The track's silence-then-hit lands at 7.5 s = beat 16 = the white-flash drop (measured).
- Stills at every beat type (text, chart, ticket, tape, grid, automation shot, counters, end card) were read.

## Not tested
- No full listen/watch by the maker, no muted/audio-only pass, no design review, no reduced-motion cut (the film is made of flashes: it is NOT suitable for photosensitive viewers; the 16 fps cut rate is above 3 flashes per second in places).
- Ticker listings (all believed Nasdaq) were not verified against a live source (no network).

## Honesty notes
- Charts are illustrative, seeded, indexed to 100 and badged ILLUSTRATIVE; no real quotes, P&L or results are shown.
- Automation shots are real frames of our own films; order tickets show ticker and order type only.

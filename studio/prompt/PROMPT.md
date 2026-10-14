# Explainer-film prompt (baseline, adapted for automation / trading content)

Fill the three `{{ }}` fields and hand this file to the studio.

<goal>
Turn {{TOPIC}} into a finished explainer film that leaves {{AUDIENCE}} with one new
understanding in {{SECONDS}} seconds. Deliverable: rendered video with sound and
captions, plus the source that re-renders it. A plan, moodboard or still is not the deliverable.
</goal>

<references>
Style recipe taken from refs/ (four reference films):
- Black ground, ONE glowing object that is the metaphor (funnel, vortex, bloom, equity line).
- Mono-type HUD panels around it carrying real-looking data: counters, ladders, mini charts.
- One accent colour, a second colour only for "rejected / danger". Glow = meaning, never decoration.
- Objects stay alive across scenes and transform; the camera reframes between ideas.
- Counters tick, labels pin to the action, captions are short and burned in.
</references>

<principles>
- Shape before polish. Settle the one idea and the viewer's mental model first.
- Who is this for, what are they believing now, does the idea need a name or can it stay invisible?
- Go wide, then decide: 3-4 directions in studio/directions.html, mark the winner and why.
- Anchor to the brand tokens in studio/brand/tokens.json. Restraint is taste.
</principles>

<story_arc>
Question 0-10% (open on the thing people get wrong, as an image) ->
Model 10-35% (smallest correct picture, one element per beat) ->
Proof 35-75% (run it on a real case, let cause and effect play out) ->
Turn 75-90% (change one variable, show what follows) ->
Payoff 90-100% (opening image again, now read correctly, plus one next step).
</story_arc>

<rules>
- Max 2 lines on screen, max 8 words a line. One name per thing, used every time.
- Every number is simulated or sourced; label simulated numbers as simulated. No performance claims.
- Trading content carries a short "not financial advice" line.
- Contrast >= 4.5:1, no flashes above 3 per second, reduced-motion cut keeps the same sequence of ideas.
- window.seek(t) paints the frame at time t; every frame is a pure function of t; seeded randomness only.
- Audio: tempo-locked procedural bed, soft UI cues only on meaningful actions, ~ -16 LUFS, true peak <= -1.5 dBTP.
</rules>

<verification>
Render one frame twice and diff; read a still at 390px wide; watch muted, listen audio-only;
run an accessibility pass; every fix ships with a before/after frame pair.
</verification>

<delivery>
out/master_1x1.mp4, out/master_9x16.mp4, out/master_16x9.mp4, captions.srt, contact.png, source, README listing only what was tested.
</delivery>

<autonomy>
Do not stop for approval on creative calls. Stop only for missing rights, unsafe content, or an ambiguity that changes the goal.
</autonomy>

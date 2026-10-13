# Lessons & roadmap

## Recommendations for builders

1. **Measure the impedance before anything else.** A 50 Ω resistor and two jack leads identify the
   driver version and give the real port tuning in minutes ([Impedance jig](03-impedance-jig.md)).
2. **Don't copy the 43 Hz tuning for the Aiyima.** Aim for ≈ 50 Hz; a 175 mm total port gave
   ≈ 48 Hz and a flat bass in this box. Cut long, measure, trim.
3. **Place damping by the mode, not by the panel.** Thick, loose fill at mid-height for the 350 Hz
   mode; wool on the back panel for the ~950 Hz depth mode. One thin layer alone does little.
4. **The budget damping layout works:** one layer of sheep's wool fleece on the back panel plus 50 g of pillow
   fill in a wool pocket across the middle third of the height.
5. **Build the back panel as drawn** — 292 × 482 mm, gasket and screws — and seal the OSB inside.
   A friction fit leaks and shifts the bass every time it's refitted.
6. **Stop before the impedance dip disappears.** When the dip between the bass peaks is down to
   ~1 Ω, more damping costs bass.
7. **Make the setup repeatable before you measure the speaker:** floor marks, taped knobs, a
   loopback reference, fingerprints at every session.

## Conclusions

- **Measurement makes it verifiable; the ears make it final.** The curves say the alignment is
  right; the listening test says it sounds more balanced. Tuning further would trade evenness
  against bass quantity — a matter of taste, not of right or wrong.
- **Balance, not quantity.** For more bass level the levers are placement (closer to a wall, as the
  original design intends), a gentle EQ shelf, or loudness compensation — all safe once the
  protective high-pass sits at 0.75 × Fb.
- **The first tube cut landed on target.** Partly luck — but the prediction came from the measured
  tuning, and three independent checks (port near field, bass sum, impedance) agree on ≈ 48 Hz.

## Roadmap

| Step | Status |
| --- | --- |
| 1 — Damping (speaker L) | done |
| 2 — Port tube (speaker L) | done |
| Speaker R: same damping and 175 mm port, check measurement | next |
| Finishing: tube glued, back panel gasket + screws, neat damping, one confirming session | next |
| 3 — Correction EQ for the treble peaks (~6 and ~10.5 kHz) | planned |
| Room: placement and room correction at the listening seat | planned |

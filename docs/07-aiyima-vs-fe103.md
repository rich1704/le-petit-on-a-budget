# Aiyima vs. FE103NV2

The plan used here is drawn for the **Fostex FE103NV2**. This build uses the **Aiyima 4"
full-range (8 Ω version)**. What carries over, and what doesn't:

| | Original (FE103NV2) | This build (Aiyima, 8 Ω) |
| --- | --- | --- |
| Power rating | 5 W | 25 W |
| Bass character | lean; the plan: "bass falls off below approx. 300 Hz" | more bass of its own; in-box estimate Fs ≈ 82 Hz (new suspension) |
| Intended tuning | 43 Hz (117 mm tube + 22 mm doubler), with wall or corner placement | **≈ 50 Hz**; measured ≈ 48 Hz with a 175 mm port |
| Impedance | — | 7.6–7.9 Ω plateau; the datasheet shipped with it describes the 4 Ω version |
| Damping | box modes come from the box — the same targets for both drivers | |

## The driver changes the tuning, not the damping

- **Box resonances** (350 Hz height mode, ~950 Hz depth mode, the port's pipe resonance) are set by
  the box's dimensions. They are there with either driver, and the damping that tames them carries
  over. The plan's own note — 50 mm foam is better against the low mode than thin felt — matches
  the measurements.
- **The tuning target differs.** The FE103NV2 relies on a deep tuning plus a nearby wall to sound
  full. The Aiyima has more bass of its own; tuned to 43 Hz it would droop early. Around 50 Hz the
  bass is flat.
- **The real box tunes higher than the plan's calculation.** The bare 44 mm port measured 74.4 Hz
  (predicted ≈ 61 Hz). Scaled from that measurement, the plan's 139 mm port would give about
  50–51 Hz here, and 43 Hz would need ≈ 216 mm — more than the box is deep.

## Practical consequences

1. **Measure the impedance first** — it shows the driver version and the real tuning in minutes.
2. **Aim for ≈ 50 Hz** and cut the tube long; trim with the jig and the near-field bass.
3. **Mind the depth:** the tube's inner end needs ≈ 5 cm free space to the back panel and damping.
4. **Watch the pipe resonance:** a longer port lowers its own pipe resonance (≈ 840 Hz for 139 mm),
   close to the 912 Hz depth mode — another reason for wool on the back panel.
5. **25 W instead of 5 W** makes the Aiyima usable with ordinary class-D amplifiers; still use a
   protective high-pass at ≈ 0.75 × Fb (36 Hz here).

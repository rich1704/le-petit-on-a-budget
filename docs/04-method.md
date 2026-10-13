# Method

> *Part of **How it was measured** — optional reading. To build the speaker you only need the [build guide](01-build.md).*

Two independent methods: **electrical impedance**, which is immune to the room and pins down the
port tuning, and **acoustic measurements** at three microphone positions, which show what the
speaker radiates. The raw impulse responses are stored, so any window or smoothing can be
re-applied later (see [data](data/README.md)).

## Excitation and processing

- **Synchronized exponential sine sweep** (Novak et al., JAES 2015), 20 Hz–20 kHz, 5 s, two sweeps
  averaged, 48 kHz. The synchronized form places the harmonic impulse responses at exact times, so
  harmonic distortion (H2–H5) is measured in the same run.
- **Loopback reference:** the deconvolution divides the mic recording by the loopback recording
  (regularized spectral division). Interface latency and response cancel; all measurements share
  one time zero.
- **Levels:** −30 dBFS far field, −50 dBFS near field (20 dB quieter keeps the mic out of overload
  at 5 mm); gains fixed for the whole series.

## Windows and validity

| Measurement | Window | Valid range |
| --- | --- | --- |
| Far field, gated | 3.4 ms (before the floor reflection at 3.8 ms) | room-free above ≈ 290 Hz (1/gate) |
| Far field, in-room | 300 ms | what the mic hears in the room |
| Near-field driver | 300 ms | absolute up to ≈ 1.3 kHz for the 81 mm cone (Keele, JAES 1974: f ≈ 10 950 / D<sub>cm</sub>) |
| Near-field port | 300 ms | absolute up to ≈ 1.6 kHz for the 70 mm port; above that a *relative* before/after measure at a fixed position |

## Bass sum

Driver and port near-field responses are added as **complex** values, the port scaled by its area
relative to the cone (pressure × D<sub>port</sub>/D<sub>cone</sub>). The shared time zero keeps
their phases aligned — that matters most around and below Fb, where cone and port partly cancel.
The sum is a half-space response and reads a few dB high in the bass, so it's judged by its
**shape** relative to the upper bass (levelled to 150–250 Hz).

**Full-range view:** the bass sum spliced to the gated far field at 400 Hz (level-matched over
± ½ octave) gives the complete room-free response.

## Impedance

See [Impedance jig](03-impedance-jig.md): voltage divider, cross-spectrum estimate of
G = V<sub>B</sub>/V<sub>A</sub> with 1/48-octave smoothing, Z = R·G/(1−G), channel calibration,
verification against a 10 Ω resistor. A sweep of 10 Hz–20 kHz at −10 dBFS from the headphone
output.

## Study design

- **One change per round**, each compared with the untreated baseline at the problem frequencies
  (band maxima, 1/12 octave).
- **Fingerprints** and re-placement tests at every session ([Measurement rig](02-measurement-rig.md)).
- **What wasn't controlled:** the seating of the friction-fit back panel during the damping study
  shifted the port's bass output between refits, so bass comparisons are only made between
  sessions with the same panel state. (Build the back with gasket and screws — see [Build](01-build.md).)
- **Listening tests** with equal-level test signals sent to one speaker at a time.

## References

- J. Hiraga, "Le Petit", *L'Audiophile* no. 29, 1983.
- A. Novak, P. Lotton, L. Simon, "Synchronized swept-sine: theory, application and implementation",
  *J. Audio Eng. Soc.* 63(10), 2015.
- D. B. Keele, "Low-frequency loudspeaker assessment by nearfield sound-pressure measurement",
  *J. Audio Eng. Soc.* 22(3), 1974.

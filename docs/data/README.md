# Measurement data

Every measurement of speaker L, in two forms:

- **[`csv/`](csv/)** — plain text, opens in any spreadsheet: frequency responses (1/12 octave),
  impedance (magnitude and phase) and the near-field bass sums. Start here.
- **`*.npz`** — the raw recordings (impulse responses, complex impedance) for anyone who wants to
  re-window or re-smooth; a `.png` overview of each sits next to it.

## CSV files

| File | Columns |
| --- | --- |
| `<session>-far.csv` | `frequency_hz`, `level_db_300ms` (in-room at the mic), `level_db_gated_3.4ms` (room-free direct sound, valid above ≈ 290 Hz; empty below) |
| `<session>-near-driver.csv`, `-near-port.csv` | `frequency_hz`, `level_db_300ms` |
| `<session>-bass-sum.csv` | `frequency_hz`, `driver_db`, `port_scaled_db`, `sum_db` — near-field driver + port, complex sum, port scaled by its area |
| `L-z-*.csv`, `T-z-10r-check.csv` | `frequency_hz`, `impedance_ohm`, `phase_deg` |

Levels are dB relative, with the same reference for all sessions (loopback-referenced, fixed gains),
so curves can be compared directly. The first line of every file describes the speaker's state for
that session.

## Raw format (`.npz`)

Each `.npz` is a NumPy archive with a JSON metadata string:

```python
import json, numpy as np

d = np.load("L-11-tube175-far.npz", allow_pickle=False)
meta = json.loads(str(d["meta"]))      # fs, sweep f1/f2, level_db, note, peak, start, ...
ir = d["ir"]                           # acoustic: impulse response (loopback-referenced), float32
# impedance files instead hold  f (Hz), Z (complex ohms), G (voltage ratio VB/VA)
```

- **Acoustic** (`ir`): the impulse response deconvolved against the loopback. `meta["peak"]` is the
  sample index of the direct sound; window around it (e.g. 1 ms before, 3.4 ms after for the gated
  far field, 300 ms for in-room/near field) and FFT. `meta["placement"]` is `far`, `near-driver` or
  `near-port`.
- **Impedance** (`f`, `Z`, `G`): sense resistor 50.1 Ω (`meta["r_sense"]`), channel calibration
  applied (`zcal.npz` holds the calibration itself).

## Files

| Files | What |
| --- | --- |
| `zcal.npz`, `T-z-10r-check` | jig calibration; jig verification with a 10.1 Ω resistor |
| `L-z-00` … `L-z-03-tube175-taped` | impedance: untreated, damped, 175 mm port, port + taped seams |
| `L-00-baseline-*` | untreated box: far field, near-field driver, near-field port, bass sum |
| `L-01`, `L-02` | leak test: port near field with the back panel seams untaped / taped |
| `L-03` … `L-09` | damping variants (see [Step 1](../05-step-1-damping.md)); `L-07` measured twice (`_2`) |
| `L-10-damped-sealed-*` | the chosen damping, panel closed (friction fit — the name predates that note) |
| `L-11-tube175-*` | damped + 175 mm port |
| `L-history-*.png`, `compare-*.png` | overlays of several sessions |

Session names: `L-<nn>-<change>`; `L` is the left speaker. The `note` field in each file describes
the state of the speaker for that session.

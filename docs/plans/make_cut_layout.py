"""Cutting plan: one pair of Le Petit boxes from a single 2000 x 1000 mm board of 22 mm OSB.

    python docs/plans/make_cut_layout.py      (from the repository root; needs matplotlib)

Writes cut-layout-2000x1000.{svg,png} next to this file. The layout is the one the speakers
were actually cut from: trim one long edge and one end, five cuts straight across the board
(530 · 530 · 300 · 296 · 300), then each piece is ripped or cut to length. The only change to the
original sheet: the backs are cut 482 long and ripped to 292 (2 mm play per side in the
296 x 486 opening) instead of 484 / 294. The script checks that nothing overlaps and that
everything stays on the board, kerf included.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BOARD_W, BOARD_H = 2000, 1000   # x runs along the 2000 mm length, y across the 1000 mm width
TRIM = 10                        # trim one long edge (bottom) and one end (left)
KERF = 4                         # generous: track saw 2.2, circular saw 2.4-3.2 mm

# the five pieces from the cross cuts, left to right: (name, length along the board, parts)
# parts are stacked from the trimmed long edge: (label, size across the board, note)
COLUMNS = [
    ("A", 530, [("Front", 340, ""), ("Front", 340, "")]),
    ("B", 530, [("Side", 210, ""), ("Side", 210, ""), ("Side", 210, ""), ("Side", 210, "")]),
    ("strip 1", 300, [("Back", 482, "rip to 292 after gluing"), ("Back", 482, "rip to 292 after gluing")]),
    ("strip 2", 296, [("Top / bottom", 210, ""), ("Top / bottom", 210, ""), ("Top / bottom", 210, ""),
                      ("Top / bottom", 210, "")]),
    ("strip 3", 300, [("Doubler", 300, ""), ("Doubler", 300, "")]),
]


def layout():
    parts, cuts, x = [], [], TRIM
    for name, length, items in COLUMNS:
        y = TRIM
        for lab, size, note in items:
            parts.append((name, lab, note, x, y, length, size))
            y += size + KERF
        x += length
        cuts.append(x)
        x += KERF
    return parts, cuts


def check(parts):
    for _, lab, _, x, y, w, h in parts:
        assert x >= TRIM and y >= TRIM, lab
        assert x + w <= BOARD_W and y + h <= BOARD_H, f"{lab} runs off the board"
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            ax, ay, aw, ah = a[3:]
            bx, by, bw, bh = b[3:]
            apart = (ax + aw + KERF <= bx or bx + bw + KERF <= ax or
                     ay + ah + KERF <= by or by + bh + KERF <= ay)
            assert apart, f"{a[1]} and {b[1]} overlap"


def draw(parts, cuts, out: Path):
    ink, muted, offcut = "#16181a", "#5b5f63", "#e9e9e6"
    fig, ax = plt.subplots(figsize=(16, 9.6))
    ax.add_patch(plt.Rectangle((0, 0), BOARD_W, BOARD_H, fc=offcut, ec=ink, lw=1.4))
    ax.add_patch(plt.Rectangle((0, 0), BOARD_W, TRIM, fc="#555", ec="none"))          # trimmed long edge
    ax.add_patch(plt.Rectangle((0, 0), TRIM, BOARD_H, fc="#555", ec="none"))          # trimmed end
    for _, lab, note, x, y, w, h in parts:
        ax.add_patch(plt.Rectangle((x, y), w, h, fc="#ffffff", ec=ink, lw=1.0))
        size = f"{w} × {h}" if lab != "Back" else f"{h} × {w}"
        txt = f"{lab}\n{size}" + (f"\n{note}" if note else "")
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=9.5, color=ink, linespacing=1.5)
    # offcut labels
    for name, length, items in COLUMNS:
        x0 = next(p[3] for p in parts if p[0] == name)
        top = max(p[4] + p[6] for p in parts if p[0] == name) + KERF
        if BOARD_H - top > 60:
            ax.text(x0 + length / 2, (top + BOARD_H) / 2, f"offcut {length} × {BOARD_H - top}", ha="center",
                    va="center", fontsize=8.5, color=muted, style="italic")
    # numbered cross cuts
    ax.plot([TRIM] * 2, [-28, BOARD_H + 28], color=ink, lw=1)
    for i, (cx, (name, length, _)) in enumerate(zip(cuts, COLUMNS)):
        ax.plot([cx + KERF / 2] * 2, [-28, BOARD_H + 28], color=ink, lw=2.2)
        ax.text(cx + KERF / 2, BOARD_H + 40, str(i + 3), ha="center", va="bottom", fontsize=10, weight="bold")
        x0 = cx - length
        ax.text(x0 + length / 2, BOARD_H + 40, name, ha="center", va="bottom", fontsize=10.5, weight="bold",
                color=ink)
        ax.text(x0 + length / 2, -45, f"{length}", ha="center", va="top", fontsize=9, color=muted)
    ax.text(BOARD_W / 2, -95, "1 — trim the long edge, 10 mm: reference for every rip      "
            "2 — trim one end square to it, 10 mm: reference for every cross cut", ha="center", va="top",
            fontsize=9, color=muted)
    ax.set_xlim(-30, BOARD_W + 30)
    ax.set_ylim(-150, BOARD_H + 160)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0, BOARD_H + 125, "Cutting plan — one board, 2000 × 1000 mm, 22 mm OSB: both Le Petit cabinets",
            fontsize=13, weight="bold", color=ink)
    used = sum(w * h for *_, w, h in parts)
    ax.text(0, BOARD_H + 95, f"Every part drawn to scale · kerf {KERF} mm · {TRIM} mm trim on two edges · "
            f"{cuts[-1] + KERF} of 2000 mm used along the board · parts {used / 1e6:.2f} m²",
            fontsize=9, color=muted)
    fig.tight_layout()
    for ext in ("svg", "png"):
        fig.savefig(out.with_suffix("." + ext), dpi=160)
    plt.close(fig)
    return used


if __name__ == "__main__":
    parts, cuts = layout()
    check(parts)
    used = draw(parts, cuts, Path(__file__).with_name("cut-layout-2000x1000"))
    backs = max(p[4] + p[6] for p in parts if p[0] == "strip 1")
    print(f"{len(parts)} parts on the board, no overlaps. Cross cuts at {cuts}. Parts {used / 1e6:.3f} m². "
          f"Strip 1 (backs) ends at {backs} mm: {BOARD_H - backs} mm spare to the untrimmed long edge.")

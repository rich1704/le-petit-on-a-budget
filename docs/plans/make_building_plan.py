"""Le Petit building plan, as built: three A3 sheets as SVG (1:5, detail 1:2).

Carcass glued with biscuits (size 20), no screws; back panel 292 x 482 on cleats with
M4 inserts; port Ø70 through front and doubler, HT DN75 tube 131 mm with screwed flaps.
Run: python make_building_plan.py  ->  building-plan-sheet-{1,2,3}.svg
"""
import math
from pathlib import Path

OUT = Path(__file__).parent
W, H = 420, 297                      # A3 landscape, mm
DATE = "13.10.2026"
BIS = (45, 133, 221, 309, 397, 485)  # front onto sides, along the 530 edges
BIS_FT = (70, 170, 270)              # front onto top/bottom, from the front's edge
BIS_SE = (45, 105, 165)              # sides onto top/bottom ends, from the front edge
BACK_X = (56, 146, 236)              # back screws, top/bottom rows (back 292 x 482)
BACK_Y = (31, 136, 241, 346, 451)    # back screws, side columns
E = 6.5                              # screw centre from the back's edge

CSS = """
text{font-family:Helvetica,Arial,sans-serif;fill:#000}
.o{stroke:#000;stroke-width:.35;fill:none}.t{stroke:#000;stroke-width:.18;fill:none}
.hd{stroke:#000;stroke-width:.18;fill:none;stroke-dasharray:1.2 .8}
.c{stroke:#000;stroke-width:.13;fill:none;stroke-dasharray:4 .8 .6 .8}
.d{stroke:#000;stroke-width:.13;fill:none}
.cut{stroke:#000;stroke-width:.35;fill:url(#h)}.cut2{stroke:#000;stroke-width:.35;fill:url(#h2)}
.bis{fill:#d9b06a;stroke:#5a3e12;stroke-width:.15}
.bish{fill:#f3e6c9;stroke:#5a3e12;stroke-width:.15;stroke-dasharray:.8 .5}
.pipe{fill:#9aa0a6;stroke:#000;stroke-width:.2}
.g{fill:#555}.w{fill:#fff}
"""
DEFS = """<defs>
<pattern id="h" width="1.2" height="1.2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="1.2" stroke="#000" stroke-width=".12"/></pattern>
<pattern id="h2" width="1" height="1" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
<line x1="0" y1="0" x2="0" y2="1" stroke="#000" stroke-width=".12"/></pattern>
</defs>"""


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Sheet:
    def __init__(s):
        s.e = []

    def raw(s, x):
        s.e.append(x)

    def line(s, x1, y1, x2, y2, c="t"):
        s.raw(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{c}"/>')

    def rect(s, x, y, w, h, c="o"):
        s.raw(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" class="{c}"/>')

    def circle(s, cx, cy, r, c="o"):
        s.raw(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{c}"/>')

    def poly(s, pts, c="o"):
        s.raw(f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" class="{c}"/>')

    def text(s, x, y, t, size=2.0, anchor="start", rot=0, weight=None, fill=None):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        a += f' transform="rotate({rot} {f(x)} {f(y)})"' if rot else ""
        a += f' font-weight="{weight}"' if weight else ""
        a += f' style="fill:{fill}"' if fill else ""
        t = t.replace("&", "&amp;").replace("<", "&lt;")
        s.raw(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}"{a}>{t}</text>')

    def lens(s, cx, cy, L, w, vertical=False, c="bis"):
        """Biscuit symbol: a lens L long, w wide (paper mm)."""
        R = (L * L / 4 + w * w / 4) / w
        d = f"M{f(-L/2)},0 A{f(R)},{f(R)} 0 0 1 {f(L/2)},0 A{f(R)},{f(R)} 0 0 1 {f(-L/2)},0Z"
        rot = " rotate(90)" if vertical else ""
        s.raw(f'<path d="{d}" transform="translate({f(cx)},{f(cy)}){rot}" class="{c}"/>')

    def tick(s, x, y):
        s.line(x - .8, y + .8, x + .8, y - .8, "o")

    def dimh(s, x1, x2, y, label, yref=None, size=1.8):
        s.line(x1 - 1.2, y, x2 + 1.2, y, "d")
        for x in (x1, x2):
            s.tick(x, y)
            if yref is not None:
                s.line(x, yref + (.8 if y > yref else -.8), x, y + (1 if y > yref else -1), "d")
        s.text((x1 + x2) / 2, y - .7, label, size, "middle")

    def dimv(s, y1, y2, x, label, xref=None, size=1.8):
        s.line(x, y1 - 1.2, x, y2 + 1.2, "d")
        for y in (y1, y2):
            s.tick(x, y)
            if xref is not None:
                s.line(xref + (.8 if x > xref else -.8), y, x + (1 if x > xref else -1), y, "d")
        s.text(x - .7, (y1 + y2) / 2, label, size, "middle", rot=-90)

    def leader(s, x1, y1, x2, y2, label, size=1.9, anchor=None):
        s.line(x1, y1, x2, y2, "d")
        s.circle(x1, y1, .25, "g")
        a = anchor or ("start" if x2 >= x1 else "end")
        s.text(x2 + (.8 if a == "start" else -.8), y2 + .6, label, size, a)

    def svg(s):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
                f'viewBox="0 0 {W} {H}">\n<style>{CSS}</style>\n{DEFS}\n'
                f'<rect width="{W}" height="{H}" fill="#fff"/>\n' + "\n".join(s.e) + "\n</svg>\n")


class View:
    """Panel coordinates (mm, u right, v down) -> paper at scale k."""

    def __init__(v, sh, ox, oy, k=0.2):
        v.s, v.ox, v.oy, v.k = sh, ox, oy, k

    def p(v, u, w):
        return v.ox + u * v.k, v.oy + w * v.k

    def rect(v, u, w, du, dw, c="o"):
        x, y = v.p(u, w)
        v.s.rect(x, y, du * v.k, dw * v.k, c)

    def circle(v, u, w, r, c="o"):
        x, y = v.p(u, w)
        v.s.circle(x, y, r * v.k, c)

    def line(v, u1, w1, u2, w2, c="t"):
        v.s.line(*v.p(u1, w1), *v.p(u2, w2), c)

    def lens(v, u, w, vertical=False, c="bis", L=56, wd=10):
        v.s.lens(*v.p(u, w), L * v.k, wd * v.k, vertical, c)

    def chain_h(v, us, w, off, w_ref=None, labels=None):
        y = v.oy + w * v.k + off
        yref = v.oy + (w if w_ref is None else w_ref) * v.k
        for i in range(len(us) - 1):
            lab = labels[i] if labels else f(us[i + 1] - us[i])
            v.s.dimh(v.ox + us[i] * v.k, v.ox + us[i + 1] * v.k, y, lab, yref)

    def chain_v(v, ws, u, off, u_ref=None, labels=None):
        x = v.ox + u * v.k + off
        xref = v.ox + (u if u_ref is None else u_ref) * v.k
        for i in range(len(ws) - 1):
            lab = labels[i] if labels else f(ws[i + 1] - ws[i])
            v.s.dimv(v.oy + ws[i] * v.k, v.oy + ws[i + 1] * v.k, x, lab, xref)

    def text(v, u, w, t, size=2.0, anchor="start", rot=0, fill=None):
        v.s.text(*v.p(u, w), t, size, anchor, rot, fill=fill)


def frame(s, title, scale, n):
    s.rect(10, 10, 400, 277, "o")
    x0, y0 = 283, 252
    s.rect(x0, y0, 127, 35, "o")
    s.text(x0 + 3, y0 + 8.5, "Le Petit", 5.5)
    s.text(x0 + 42, y0 + 8.5, "after Jean Hiraga", 2.4)
    s.text(x0 + 3, y0 + 13.5, "L'Audiophile no. 29 (1983) · hole positions after R. Berchtold (2022)", 1.8)
    s.text(x0 + 3, y0 + 17.5, "22 mm OSB · biscuits (size 20) + wood glue, no screws · removable back", 1.8)
    s.text(x0 + 3, y0 + 23, title, 2.5)
    s.line(x0, y0 + 25, x0 + 127, y0 + 25, "t")
    s.line(x0 + 72, y0 + 25, x0 + 72, y0 + 35, "t")
    s.line(x0 + 102, y0 + 25, x0 + 102, y0 + 35, "t")
    s.text(x0 + 3, y0 + 31, f"All dimensions in mm · Rev. as built · {DATE}", 1.7)
    s.text(x0 + 75, y0 + 31, scale, 1.7)
    s.text(x0 + 105, y0 + 31, f"Sheet {n} / 3", 1.7)


def heading(s, x, y, t, sub=None):
    s.text(x, y, t, 3.0)
    if sub:
        s.text(x, y + 4.5, sub, 1.8, fill="#333")


def legend(s, x, y):
    s.text(x, y, "LEGEND", 2.4)
    s.lens(x + 4, y + 5, 11.2, 2.4)
    s.text(x + 11, y + 5.7, "biscuit slot, size 20 (56 × 23 × 4), centred in the 22 mm edge", 1.8)
    s.lens(x + 4, y + 10, 11.2, 2.4, c="bish")
    s.text(x + 11, y + 10.7, "biscuit, hidden", 1.8)
    s.rect(x + 1, y + 13.5, 6, 3, "cut")
    s.text(x + 11, y + 15.7, "cut section (OSB; beech cleats hatched the other way)", 1.8)


# ---------------------------------------------------------------- sheet 1
def sheet1():
    s = Sheet()
    # FRONT VIEW
    heading(s, 38, 33, "FRONT VIEW")
    v = View(s, 38, 41.5)
    v.rect(0, 0, 340, 530)
    v.rect(22, 22, 296, 486, "hd")
    v.rect(20, 230, 300, 300)
    v.text(30, 500, "doubler", 1.6, fill="#555")
    v.circle(170, 115, 47)
    v.circle(170, 380, 35)
    v.line(170, -10, 170, 540, "c")
    for y, r in ((115, 60), (380, 50)):
        v.line(170 - r, y, 170 + r, y, "c")
    for y in BIS:
        v.lens(11, y, True, "bish")
        v.lens(329, y, True, "bish")
    for x in BIS_FT:
        v.lens(x, 11, c="bish")
        v.lens(x, 519, c="bish")
    v.chain_v([0, 115, 230, 380, 530], 340, 6)
    v.chain_v([0, 530], 340, 12)
    v.chain_h([0, 20, 320, 340], 530, 6)
    v.chain_h([0, 340], 530, 12)
    s.leader(*v.p(137, 82), *v.p(70, 30), "Ø94")
    s.leader(*v.p(195, 405), *v.p(225, 470), "Ø70, front + doubler")
    for y in (-14, 544):  # section A-A marks
        x, yy = v.p(170, y)
        s.text(x - 2, yy + .7, "A", 2.2, "end")
    for u in (-14, 354):
        x, y = v.p(u, 380)
        s.text(x, y + 4, "B", 2.2, "middle")
        s.line(x, y - 1.5, x, y + 1.5, "o")
    s.leader(*v.p(11, 133), *v.p(-40, 160), "biscuits", 1.7)

    # SECTION A-A (u = 0 at the doubler's outer face)
    heading(s, 166, 33, "SECTION A–A")
    v = View(s, 170, 41.5)
    for r in ((0, 230, 22, 115), (0, 415, 22, 115), (22, 0, 22, 68), (22, 162, 22, 183),
              (22, 415, 22, 115), (44, 0, 210, 22), (44, 508, 210, 22), (232, 24, 22, 482)):
        v.rect(*r, "cut")
    v.rect(211, 22, 20, 15, "cut2")
    v.rect(211, 493, 20, 15, "cut2")
    v.rect(211, 37, 20, 456, "t")
    v.rect(19, 63, 3, 104, "t")
    s.poly([v.p(22, 68), v.p(54, 98), v.p(54, 132), v.p(22, 162)], "t")
    v.rect(54, 101, 16, 28, "t")
    v.rect(44, 342.5, 131, 1.9, "pipe")
    v.rect(44, 415.6, 131, 1.9, "pipe")
    v.rect(44, 322.5, 1.9, 20, "pipe")
    v.rect(44, 417.5, 1.9, 20, "pipe")
    v.line(-8, 380, 190, 380, "c")
    v.rect(32.5, 9, 23, 4, "bis")
    v.rect(32.5, 517, 23, 4, "bis")
    v.chain_h([0, 22, 44, 232, 254], 530, 6)
    v.chain_h([22, 254], 530, 12)
    v.chain_h([0, 254], 530, 18)
    v.chain_v([0, 22, 508, 530], 254, 6)
    v.chain_v([0, 530], 254, 12)
    v.chain_h([0, 175], 470, 0, 437, ["175 port"])
    v.chain_h([44, 175], 310, 0, 322, ["131 tube"])
    s.leader(*v.p(70, 115), *v.p(90, 140), "driver (schematic)", 1.8)
    s.leader(*v.p(50, 11), *v.p(95, 45), "biscuit (cut)", 1.8)
    s.leader(*v.p(221, 30), *v.p(195, 75), "cleat 15 × 20", 1.8, "end")
    s.leader(*v.p(232, 230), *v.p(150, 230), "back 292 × 482", 1.8, "end")
    v.text(150 - 4, 230 + 18, "removable", 1.8, "end")
    s.leader(*v.p(33, 270), *v.p(-30, 270), "front 22", 1.8)
    s.leader(*v.p(11, 500), *v.p(-30, 500), "doubler 22", 1.8)
    s.leader(*v.p(120, 344), *v.p(150, 395), "HT DN75 tube", 1.8)
    v.text(150 + 4, 395 + 18, "flaps screwed", 1.8)

    # VIEW FROM BEHIND
    heading(s, 262, 33, "VIEW FROM BEHIND")
    v = View(s, 264, 41.5)
    v.rect(0, 0, 340, 530)
    v.rect(22, 22, 296, 486, "t")
    v.rect(24, 24, 292, 482)
    v.rect(37, 37, 266, 456, "hd")
    holes = [(x, y) for x in BACK_X for y in (E, 482 - E)] + \
            [(x, y) for x in (E, 292 - E) for y in BACK_Y]
    for x, y in holes:
        v.circle(24 + x, 24 + y, 2.25, "t")
        v.line(24 + x - 5, 24 + y, 24 + x + 5, 24 + y, "t")
        v.line(24 + x, 24 + y - 5, 24 + x, 24 + y + 5, "t")
    for x in (126, 166):
        v.circle(24 + x, 24 + 390, 6)
    v.line(170, -10, 170, 540, "c")
    v.text(45, 50, "back 292 × 482 — 2 mm play per side", 1.7, fill="#555")
    s.leader(*v.p(30.5, 24 + 241), *v.p(80, 200), "M4, 16× — layout on sheet 2", 1.8)
    s.leader(*v.p(195, 408), *v.p(240, 360), "terminals 2 × Ø12", 1.8)
    v.chain_h([0, 24, 316, 340], 530, 6)
    v.chain_h([0, 340], 530, 12)
    v.chain_v([0, 24, 506, 530], 340, 6)
    v.chain_v([0, 530], 340, 12)
    v.chain_v([414, 506], 0, -6, 150, ["92"])
    v.chain_h([150, 190], 400, -2, 408, ["40"])

    # SECTION B-B (v = 0 at the rear edge, front at the bottom)
    heading(s, 38, 168, "SECTION B–B")
    v = View(s, 38, 176)
    for r in ((0, 0, 22, 210), (318, 0, 22, 210), (0, 210, 135, 22), (205, 210, 135, 22),
              (20, 232, 115, 22), (205, 232, 115, 22), (24, 0, 292, 22)):
        v.rect(*r, "cut")
    v.rect(22, 23, 15, 20, "cut2")
    v.rect(303, 23, 15, 20, "cut2")
    v.rect(37, 23, 266, 20, "t")
    v.rect(132.5, 79, 1.9, 131, "pipe")
    v.rect(205.6, 79, 1.9, 131, "pipe")
    v.rect(112.5, 208.1, 20, 1.9, "pipe")
    v.rect(207.5, 208.1, 20, 1.9, "pipe")
    v.line(170, 70, 170, 262, "c")
    v.rect(9, 198.5, 4, 23, "bis")
    v.rect(327, 198.5, 4, 23, "bis")
    v.circle(18, 20, 22, "t")
    v.text(-14, 6, "C", 2.4)
    v.chain_h([0, 22, 318, 340], 254, 6, 210)
    v.chain_h([0, 340], 254, 12, 210)
    v.chain_v([0, 22, 210, 232, 254], 340, 6)
    v.chain_v([0, 254], 340, 12)
    s.leader(*v.p(11, 205), *v.p(60, 160), "biscuit (cut)", 1.8)
    s.leader(*v.p(170, 120), *v.p(230, 120), "tube, Ø ≈ 71 inside", 1.8)

    # DETAIL C, 1:2 (u = 0 at the side's outer face, v = 0 at the rear edge)
    heading(s, 150, 183, "DETAIL C")
    s.text(170, 183, "1:2 — flush removable back", 2.0)
    v = View(s, 152, 199, 0.5)
    v.rect(0, 0, 22, 85, "cut")
    v.rect(24, 0, 70, 22, "cut")
    v.rect(22, 23, 15, 20, "cut2")
    v.rect(22, 22, 15, 1, "g")
    v.rect(27.5, 23, 6, 10, "pipe")
    v.rect(28.5, 0, 4, 30, "w")
    v.rect(28.5, 0, 4, 30, "t")
    v.rect(26, -.8, 9, .8, "o")
    v.rect(26.5, -3.8, 8, 3, "o")
    v.chain_h([0, 22, 37], 85, 6)
    v.chain_v([0, 22], 94, 6)
    v.chain_v([0, 23, 43], 94, 14, 37)
    v.chain_h([24, 30.5], -3.8, -5, labels=["6.5"])
    lx = 222
    for (u, w), t, y in (((30.5, -2), "M4 × 30 pan head + washer", 196),
                         ((70, 11), "back 22, 2 mm play to the side", 203),
                         ((33, 22.5), "foam gasket 3 × 10, ≈ 1 mm compressed", 210),
                         ((32.5, 30), "M4 threaded insert", 217),
                         ((36, 40), "cleat 15 × 20, beech, glued", 224),
                         ((11, 60), "side 22", 231)):
        s.leader(*v.p(u, w), lx, y + 5, t, 1.8)

    # NOTES
    x, y = 285, 170
    s.text(x, y, "NOTES", 2.6)
    for i, t in enumerate((
        "Inner clear 486 × 296 × 188 = 27.0 l (original 26.5 l).",
        "Port Ø70 in front and doubler + 131 mm tube = 175 mm, Fb ≈ 48 Hz (Aiyima 4\").",
        "Original plan: Ø75 bore, 117 tube + 22 doubler = 139 mm, ≈ 43 Hz (FE103NV2).",
        "Carcass: biscuits size 20 + wood glue, no screws — 30 per cabinet (sheet 2).",
        "Back 292 × 482: 2 mm play per side; the gasket seals on the cleats.",
        "OSB is NOT airtight: two coats of thinned lacquer inside, glue fillet in",
        "every inside corner. Size the cut edges before gluing.",
        "Back screws 6.5 from the panel edge: pan heads, no countersink.",
        "Driver cutout Ø94 fits the Aiyima 4\" — check against your driver.",
    )):
        s.text(x, y + 5 + i * 3.6, t, 1.85)
    legend(s, x, 213)
    frame(s, "Views and sections", "Scale 1:5 (C 1:2) @ A3", 1)
    return s


# ---------------------------------------------------------------- sheet 2
def sheet2():
    s = Sheet()
    heading(s, 25, 28, "FRONT", "530 × 340 × 22 · 1 per box · seen from inside · 18 biscuit slots in the face")
    v = View(s, 33, 46)
    v.rect(0, 0, 340, 530)
    v.rect(20, 230, 300, 300, "hd")
    v.text(26, 244, "doubler (outside)", 1.6, fill="#555")
    v.circle(170, 115, 47)
    v.circle(170, 380, 35)
    v.line(170, -8, 170, 538, "c")
    v.line(110, 115, 230, 115, "c")
    v.line(120, 380, 220, 380, "c")
    for y in BIS:
        v.lens(11, y, True)
        v.lens(329, y, True)
    for x in BIS_FT:
        v.lens(x, 11)
        v.lens(x, 519)
    v.chain_v([0, 115, 380, 530], 340, 6)
    v.chain_v([0, 530], 340, 12)
    v.chain_h([0, 170, 340], 530, 6)
    v.chain_h([0, 340], 530, 12)
    v.chain_v([0, *BIS, 530], 0, -6)
    v.chain_h([0, *BIS_FT, 340], 0, -5)
    s.leader(*v.p(137, 82), *v.p(70, 175), "Ø94")
    s.leader(*v.p(147, 405), *v.p(80, 460), "Ø70")
    v.text(170, 290, "slots 11 from the edge", 1.6, "middle", fill="#555")

    heading(s, 130, 28, "BACK", "482 × 292 × 22 · 1 per box · seen from behind")
    v = View(s, 140, 48)
    v.rect(0, 0, 292, 482)
    holes = [(x, y) for x in BACK_X for y in (E, 482 - E)] + \
            [(x, y) for x in (E, 292 - E) for y in BACK_Y]
    for x, y in holes:
        v.circle(x, y, 2.25, "t")
        v.line(x - 5, y, x + 5, y, "t")
        v.line(x, y - 5, x, y + 5, "t")
    for x in (126, 166):
        v.circle(x, 390, 6)
    v.line(146, -8, 146, 490, "c")
    v.text(20, 40, "16 × Ø4.5 through", 1.8)
    v.text(20, 55, "2 × Ø12 terminals", 1.8)
    v.text(20, 70, "(no countersink)", 1.8, fill="#555")
    v.chain_h([0, *BACK_X, 292], 482, 6)
    v.chain_h([0, 292], 482, 12)
    v.chain_v([0, *BACK_Y, 482], 292, 6)
    v.chain_v([0, 482], 292, 12)
    v.chain_h([292 - E, 292], 0, -4, labels=["6.5"])
    v.chain_v([390, 482], 0, -6, 120)
    v.chain_h([126, 166], 360, 0, 384)

    heading(s, 232, 28, "SIDE", "530 × 210 × 22 · 2 per box · inner face")
    v = View(s, 244, 48)
    v.rect(0, 0, 210, 530)
    v.rect(167, 22, 20, 486, "hd")
    v.text(180, 265, "cleat", 1.6, "middle", -90, fill="#555")
    for y in BIS:
        v.lens(0, y, True)
    for x in BIS_SE:
        v.lens(x, 11)
        v.lens(x, 519)
    v.text(4, 560, "front edge", 1.6, fill="#555")
    v.chain_v([0, *BIS, 530], 0, -6)
    v.chain_h([0, *BIS_SE, 210], 0, -4)
    v.chain_v([0, 530], 210, 6)
    v.chain_h([187, 210], 530, 6)
    v.chain_h([0, 210], 530, 12)

    heading(s, 25, 180, "TOP / BOTTOM", "296 × 210 × 22 · 2 per box · inner face, front edge at the bottom")
    v = View(s, 33, 196)
    v.rect(0, 0, 296, 210)
    v.rect(15, 23, 266, 20, "hd")
    v.text(148, 37, "cleat", 1.6, "middle", fill="#555")
    for x in BIS_FT:
        v.lens(x - 22, 210)
    for y in BIS_SE:
        v.lens(0, 210 - y, True)
        v.lens(296, 210 - y, True)
    v.text(148, 200, "front edge", 1.6, "middle", fill="#555")
    v.chain_h([0, 48, 148, 248, 296], 210, 6)
    v.chain_h([0, 296], 210, 12)
    v.chain_v([0, 45, 105, 165, 210], 296, 6)
    v.chain_v([0, 210], 296, 12)
    v.chain_v([0, 23], 0, -5)

    heading(s, 130, 180, "DOUBLER", "300 × 300 × 22 · 1 per box · glued on the outside")
    v = View(s, 140, 196)
    v.rect(0, 0, 300, 300)
    v.circle(150, 150, 35)
    v.line(150, -8, 150, 308, "c")
    v.line(-8, 150, 308, 150, "c")
    s.leader(*v.p(175, 125), *v.p(190, 60), "Ø70 (as front)")
    v.chain_h([0, 150, 300], 300, 6)
    v.chain_v([0, 150, 300], 300, 6)

    heading(s, 222, 180, "CLEATS", "beech 15 × 20 · per box")
    s.rect(222, 192, 486 * .2, 3)
    s.text(222, 199, "2 × 486 (sides)", 1.8)
    s.rect(222, 204, 266 * .2, 3)
    s.text(222, 211, "2 × 266 (top, bottom)", 1.8)
    s.text(222, 220, "section 1:2", 1.6, fill="#555")
    s.rect(222, 222, 7.5, 10, "cut2")
    s.dimh(222, 229.5, 236, "15", 232)
    s.dimv(222, 232, 233, "20", 229.5)

    # tables
    x, y = 300, 28
    s.text(x, y, "CUT LIST", 3.0)
    cols = (0, 34, 85, 98)
    for i, row in enumerate((("Part", "Size (mm)", "Box", "Pair"),
                             ("Front", "530 × 340 × 22", "1", "2"),
                             ("Side", "530 × 210 × 22", "2", "4"),
                             ("Top / bottom", "296 × 210 × 22", "2", "4"),
                             ("Back", "482 × 292 × 22", "1", "2"),
                             ("Doubler", "300 × 300 × 22", "1", "2"),
                             ("Cleat, beech", "486 × 15 × 20", "2", "4"),
                             ("Cleat, beech", "266 × 15 × 20", "2", "4"),
                             ("Biscuits", "size 20", "30", "60"))):
        yy = y + 7 + i * 4.6
        for c, t in zip(cols, row):
            s.text(x + c, yy, t, 1.9)
        s.line(x, yy + 1.5, x + 106, yy + 1.5, "o" if i == 0 else "t")
    s.text(x, y + 52, "OSB for the pair: 1.52 m² net — one 2000 × 1000 board.", 1.8)
    s.text(x, y + 55.5, "Cleats: cut to fit the finished opening.", 1.8)

    y = 96
    s.text(x, y, "HOLES", 3.0)
    for i, row in enumerate((("Driver", "Ø94", "front, centred, 115 below top"),
                             ("Port", "Ø70", "front, centred, 150 above bottom"),
                             ("Port", "Ø70", "doubler, centre"),
                             ("Terminals", "2 × Ø12", "back, 40 apart, 92 up"),
                             ("Screws", "16 × Ø4.5", "back, see layout"))):
        for c, t in zip((0, 22, 44), row):
            s.text(x + c, y + 7 + i * 4.2, t, 1.9)
    s.text(x, y + 30, "Chamfer the inside edge of the driver cutout.", 1.8)
    s.text(x, y + 33.5, "Check Ø94 against your actual driver first.", 1.8)

    y = 140
    s.text(x, y, "CARCASS JOINTS — BISCUITS + GLUE", 3.0)
    for i, t in enumerate((
        "No screws: the glue carries the joint, the biscuits locate it.",
        "Size 20 (56 × 23 × 4), slots centred in the 22 mm thickness.",
        "Front onto sides: 6 per 530 edge at 45 / 133 / 221 / 309 / 397 / 485.",
        "Front onto top and bottom: 3 per edge at 70 / 170 / 270",
        "(from the front's edge = 48 / 148 / 248 on the top/bottom).",
        "Sides onto top/bottom ends: 3 per edge at 45 / 105 / 165 from the front.",
        "30 per cabinet, 60 per pair.",
        "OSB: reference the joiner from the face, not the fence. Check every slot",
        "for voids, shift it 20 mm if hollow. Keep sealer out of the slots.",
        "Clamp with a ratchet strap and cauls.",
    )):
        s.text(x, y + 6 + i * 3.7, t, 1.85)
    legend(s, x, 226)
    frame(s, "Panels and cut list", "Scale 1:5 @ A3", 2)
    return s


# ---------------------------------------------------------------- sheet 3
C, S = 0.5 * math.cos(math.radians(30)), 0.5 * math.sin(math.radians(30))


def P(X, Y, Z):
    """Cabinet oblique: X right, Y up, Z into the box; returns (x, y-down)."""
    return X + Z * C, -(Y + Z * S)


def sheet3():
    parts = []  # (key, draw-callback) - painter's algorithm, far first

    def box(x0, y0, z0, x1, y1, z1, d=(0, 0, 0), extra=None):
        dx, dy, dz = d
        x0, x1, y0, y1, z0, z1 = x0 + dx, x1 + dx, y0 + dy, y1 + dy, z0 + dz, z1 + dz
        faces = [[(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
                 [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
                 [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)]]
        key = (z0 + z1) / 2 - C * 2 * (x0 + x1) / 2 - S * 2 * (y0 + y1) / 2
        parts.append((key, faces, extra, (dx, dy, dz)))

    def slot(c, a, b, L=56, w=6):
        return [tuple(c[i] + sa * a[i] * L / 2 + sb * b[i] * w / 2 for i in range(3))
                for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    ex = 170
    top_slots = [slot((x, 519, 22), X, Y) for x in BIS_FT] + \
                [slot((318, 519, 22 + z), Z, Y) for z in BIS_SE]
    bot_slots = [slot((x, 11, 22), X, Y) for x in BIS_FT] + \
                [slot((318, 11, 22 + z), Z, Y) for z in BIS_SE]
    box(22, 0, 22, 318, 22, 232, (0, -ex + 20, 0), {"slots": bot_slots})
    box(22, 508, 22, 318, 530, 232, (0, ex - 20, 0), {"slots": top_slots})
    lside = [slot((11, y, 22), Y, X) for y in BIS] + \
            [slot((22, yy, 22 + z), Z, Y) for z in BIS_SE for yy in (11, 519)]
    box(0, 0, 22, 22, 530, 232, (-ex, 0, 0), {"slots": lside})
    box(318, 0, 22, 340, 530, 232, (ex, 0, 0), {"slots": [slot((329, y, 22), Y, X) for y in BIS]})
    box(22, 22, 189, 37, 508, 209, (-ex / 2, 0, 0))
    box(303, 22, 189, 318, 508, 209, (ex / 2, 0, 0))
    box(37, 22, 189, 303, 37, 209, (0, -ex / 2, 0))
    box(37, 493, 189, 303, 508, 209, (0, ex / 2, 0))
    box(24, 24, 210, 316, 506, 232, (0, 0, 190), {"holes": [(150, 414, 6), (190, 414, 6)]})
    box(0, 0, 0, 340, 530, 22, (0, 0, -300), {"holes": [(170, 415, 47), (170, 150, 35)]})
    box(20, 0, -22, 320, 300, 0, (-30, -60, -560), {"holes": [(170, 150, 35)]})
    parts.sort(key=lambda p: -p[0])

    s = Sheet()
    heading(s, 20, 28, "EXPLODED VIEW")
    pts = [P(*q) for _, faces, _, _ in parts if faces != "tube" for fc in faces for q in fc]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(185 / (max(xs) - min(xs)), 225 / (max(ys) - min(ys)))
    ox = 20 + (185 - k * (max(xs) - min(xs))) / 2 - k * min(xs)
    oy = 38 - k * min(ys)

    def T(q):
        x, y = P(*q)
        return ox + k * x, oy + k * y

    for _, faces, extra, d in parts:
        if faces == "tube":
            r, z0, z1 = 37.5, 22 + d[2], 153 + d[2]
            a, b = T((170, 150, z0)), T((170, 150, z1))
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
            ux, uy = math.cos(ang) * r * k, math.sin(ang) * r * k
            s.circle(*b, r * k, "o w")
            s.poly([(a[0] + ux, a[1] + uy), (b[0] + ux, b[1] + uy),
                    (b[0] - ux, b[1] - uy), (a[0] - ux, a[1] - uy)], "w")
            s.line(a[0] + ux, a[1] + uy, b[0] + ux, b[1] + uy, "o")
            s.line(a[0] - ux, a[1] - uy, b[0] - ux, b[1] - uy, "o")
            s.circle(*a, r * k, "o w")
            s.circle(*a, 35.5 * k, "t")
            continue
        for fc in faces:
            s.poly([T(q) for q in fc], "o w")
        for hx, hy, hr in (extra or {}).get("holes", []):
            z = faces[0][0][2]
            c = T((hx + d[0], hy + d[1], z))
            s.circle(*c, hr * k, "o")
            c2 = T((hx + d[0], hy + d[1], z + 22))
            s.raw(f'<clipPath id="c{id(c)}"><circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(hr * k)}"/></clipPath>')
            s.raw(f'<circle cx="{f(c2[0])}" cy="{f(c2[1])}" r="{f(hr * k)}" class="t" clip-path="url(#c{id(c)})"/>')
        for sl in (extra or {}).get("slots", []):
            s.poly([T(tuple(q[i] + d[i] for i in range(3))) for q in sl], "bis")
    s.text(20, 268, "Not to scale. Doubler, front and back pulled forward/back; sides, top and bottom "
           "pulled out; cleats pulled in. Biscuit slots shown on the visible faces.", 1.7, fill="#555")

    x, y = 215, 28
    s.text(x, y, "ASSEMBLY", 3.0)
    steps = (
        ("Cut and check.", "Cut all panels from one 2000 × 1000 board (cutting plan in the build guide).",
         "The front sets the box square — check its diagonals."),
        ("Holes.", "Ø94 and Ø70 in the front, Ø70 in the doubler, Ø12 and 16 × Ø4.5 in the back."),
        ("Seal.", "Two coats of thinned lacquer on all inside faces before assembly — OSB is porous."),
        ("Cleats.", "Glue to sides, top and bottom, cleat face 23 mm from the rear edge. Jig: back panel",
         "on the rear edges, 22 mm offcuts + 1 mm card underneath as spacers."),
        ("Biscuit slots.", "30 per cabinet, size 20 (sheet 2). Reference the joiner from the face, not the",
         "fence; check every slot for voids, shift it 20 mm if hollow. No sealer in the slots."),
        ("Carcass.", "Size the cut edges with thin PVA, let it tack, then glue sides, top and bottom with",
         "biscuits, strap-clamped. A back dry-fitted on wax paper holds it square."),
        ("Front.", "Glue the front on with its 18 biscuits — ratchet strap and cauls across the front."),
        ("Doubler.", "Flush with the bottom edge, 20 mm in from each side; a Ø70 offcut through both",
         "port holes locates it."),
        ("Seal and tube.", "Glue fillet or acrylic in every inside corner. Tube 151 mm with 20 mm flaps,",
         "butted against the inside of the front, four flaps screwed (3.5 × 12), joint sealed."),
        ("Finish.", "Sand 80 then 120 only — the resin-rich chips sand harder than the binder.",
         "Then 2–3 coats of clear water-based lacquer."),
        ("Inserts.", "Clamp the back on, drill through its holes into the cleats, set the M4 inserts."),
        ("Close.", "Gasket on the cleats, damping, wire driver and terminals, screw the back on."),
    )
    yy = y + 7
    for n, (title, *lines) in enumerate(steps, 1):
        s.text(x, yy, str(n), 1.9)
        s.text(x + 5, yy, title, 1.9)
        for ln in lines:
            s.text(x + 30, yy, ln, 1.9)
            yy += 3.6
        yy += 1.2

    yy += 6
    s.text(x, yy, "HARDWARE  (pair)", 3.0)
    yy += 7
    for q, t in (("2", "Aiyima 4\" full-range driver, 8 Ω (plan: Fostex FE103NV2)"),
                 ("2 × 151 mm", "HT pipe DN75 (75 o.d. / ≈ 71 i.d.)"),
                 ("60", "biscuits, size 20 — carcass, no screws"),
                 ("32", "M4 threaded inserts, for hardwood"),
                 ("32", "M4 × 30 pan head screws + washers"),
                 ("8", "screws 3.5 × 12 (tube flaps)"),
                 ("≈ 3.1 m", "beech strip 15 × 20 (cleats)"),
                 ("≈ 3.5 m", "foam gasket tape 3 × 10 mm"),
                 ("2 pairs", "speaker terminals for Ø12 hole"),
                 ("", "sheep's wool fleece ≈ 10 mm + 2 × 50 g polyester fill"),
                 ("", "PVA glue, clear lacquer, acrylic sealant, wire")):
        s.text(x, yy, q, 1.9)
        s.text(x + 30, yy, t, 1.9)
        yy += 3.6

    yy += 6
    s.text(x, yy, "BEFORE YOU PLAY", 3.0)
    yy += 7
    for t in ("The Aiyima 4\" is rated 25 W; the plan's FE103NV2 only 5 W.",
              "Port 175 mm ≈ 48 Hz: bass flat to ≈ 55 Hz free-standing, −3 dB at 47 Hz.",
              "With a DSP, set a protective high-pass at ≈ 0.75 × Fb (36 Hz).",
              "Start at a low level — below the port tuning the cone is unloaded."):
        s.text(x, yy, t, 1.9)
        yy += 3.6
    frame(s, "Assembly and hardware", "Scale n.t.s. @ A3", 3)
    return s


if __name__ == "__main__":
    for n, fn in ((1, sheet1), (2, sheet2), (3, sheet3)):
        p = OUT / f"building-plan-sheet-{n}.svg"
        p.write_text(fn().svg())
        print("wrote", p.name)

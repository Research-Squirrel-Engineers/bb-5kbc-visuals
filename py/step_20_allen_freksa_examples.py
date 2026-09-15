#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_20_allen_freksa_examples.py -- Allen's bar-grid, Freksa's lattice, real data
======================================================================================

Source: the visual *form* of both panels is taken from Florian's reference
article "Von Allen zu Freksa -- Semi-Intervalle, konzeptuelle
Nachbarschaften und relative Chronologien" (uploaded 2026-09-16,
``allen-freksa-amt_1_.html``) -- specifically its Abb. 1 (the 13-relation
bar grid, X fixed petrol / Y schematic ocher) and its ``icon()`` function
(the 13-node conceptual-neighbourhood lattice with filled/unfilled dots).
Colours (``vu.ALLEN_FRESKA``) and the lattice ``NODES``/``EDGES``
coordinates below are copied verbatim from that file's ``<script>``, not
redrawn from memory -- see ``bb5kbc_visuals_utils.py`` for where the
colours live. Underlying theory: Allen, J. F. (1983), CACM 26(11); Freksa,
C. (1992), Artificial Intelligence 54, 199-227.

This is figure 19's companion, not a replacement: 19 sketched the idea by
hand on one worked example; this one (a) draws all 13 Allen relations in
the reference's own bar-grid form, and (b) computes -- not hand-waves --
seven real "what does Freksa's neighbourhood look like here" examples.

**Left panel (Allen).** All 13 bar-grid cells reuse figure 19's already-
CSV-verified real site pairs (see ``step_19_allen_freksa_relations.py``
docstring for the verification method) -- 7 canonical pairs read in both
directions gives exactly 13. The bar *shape* per cell is the reference's
own schematic pixel geometry (``BARS``, copied verbatim: it encodes the
qualitative picture of a relation, not any real distance in years), so
real years are given in the two caption lines instead of in the bar
proportions -- stated explicitly in the panel legend so this doesn't read
as an accidentally-not-to-scale chart.

**Right panel (Freksa).** Seven real FID pairs, each with its two real
``dating_start``/``dating_end`` values and real ``dating_certainty_start``/
``_end`` margins (same CSV, same columns as figure 06 and figure 19).
Unlike 19's single hand-reasoned example, the achievable Allen-relation
set per pair here is *computed*: every relevant "critical" combination of
the two endpoints' plausible values (both margin extremes, the centre, and
any point where one endpoint's range meets another's) is classified, and
the resulting set is checked for connectivity against the same lattice
graph the icons are drawn from -- see ``_achievable()`` below. All seven
results came out connected, which is itself a real, unplanned confirmation
of Freksa's neighbourhood theorem (composition results are never scattered
disjunctions) rather than a chosen example. Verified 2026-09-16 against
``fst_wgs84_lit_enriched.csv``; script and exact figures in this file's
git history / PRIMER.md S42.

Writes: allen-freksa-examples.de.svg/.png, allen-freksa-examples.en.svg/.png
Run standalone: ``python py/step_20_allen_freksa_examples.py``
"""

from __future__ import annotations

from collections import deque

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["20-allen-freksa-examples"]
AF = vu.ALLEN_FRESKA
ALLEN, FRESKA = AF["allen"], AF["freksa"]

# --------------------------------------------------------------------------- #
# The conceptual-neighbourhood lattice -- NODES/EDGES copied verbatim from
# allen-freksa-amt_1_.html's <script> (its `icon()` function's data).
# --------------------------------------------------------------------------- #
NODES: dict[str, tuple[float, float]] = {
    "<": (28, 6), "m": (28, 17),
    "s": (14, 30), "o": (28, 30), "fi": (42, 30),
    "d": (14, 41), "=": (28, 41), "di": (42, 41),
    "f": (14, 52), "oi": (28, 52), "si": (42, 52),
    "mi": (28, 65), ">": (28, 76),
}
EDGES: list[tuple[str, str]] = [
    ("<", "m"), ("m", "o"), ("o", "s"), ("o", "fi"), ("fi", "di"), ("fi", "="),
    ("di", "si"), ("si", "="), ("si", "oi"), ("oi", "f"), ("oi", "mi"), ("mi", ">"),
    ("f", "="), ("f", "d"), ("d", "s"), ("s", "="),
]
ORDER = ["<", "m", "o", "fi", "di", "si", "=", "s", "d", "f", "oi", "mi", ">"]
ADJ: dict[str, set[str]] = {k: set() for k in NODES}
for _a, _b in EDGES:
    ADJ[_a].add(_b)
    ADJ[_b].add(_a)

NAMES = {"<": "before", "m": "meets", "o": "overlaps", "fi": "finished by", "di": "contains",
         "si": "started by", "=": "equals", "s": "starts", "d": "during", "f": "finishes",
         "oi": "overlapped by", "mi": "met by", ">": "after"}
CODE = {"equals": "=", "starts": "s", "startedby": "si", "finishes": "f", "finishedby": "fi",
        "during": "d", "contains": "di", "overlaps": "o", "overlappedby": "oi",
        "meets": "m", "metby": "mi", "before": "<", "after": ">"}

# X fixed at [40,80]; BARS gives Y's [start,end] per relation -- copied
# verbatim from the reference article's Abb. 1 (schematic, not to scale).
BARS = {
    "<": (90, 120), "m": (80, 120), "o": (65, 110), "fi": (58, 80), "di": (52, 68),
    "si": (40, 65), "=": (40, 80), "s": (40, 100), "d": (25, 100), "f": (20, 80),
    "oi": (25, 60), "mi": (0, 40), ">": (0, 30),
}

# The 13 bar-grid cells: 7 real CSV-verified pairs from figure 19, each
# read in both directions. (fid, name, kultur) per side.
ALLEN_CELLS = [
    ("<", ("40", "Bochow 16", "SBK"), ("32", "Steckelsdorf 12", "FBG")),
    (">", ("32", "Steckelsdorf 12", "FBG"), ("40", "Bochow 16", "SBK")),
    ("m", ("78", "Nowe Objezierze 7", "SBK"), ("153", "Racot 18", "BKK")),
    ("mi", ("153", "Racot 18", "BKK"), ("78", "Nowe Objezierze 7", "SBK")),
    ("o", ("40", "Bochow 16", "SBK"), ("78", "Nowe Objezierze 7", "SBK")),
    ("oi", ("78", "Nowe Objezierze 7", "SBK"), ("40", "Bochow 16", "SBK")),
    ("s", ("1", "T\u00fcngeda", "SBK"), ("78", "Nowe Objezierze 7", "SBK")),
    ("si", ("78", "Nowe Objezierze 7", "SBK"), ("1", "T\u00fcngeda", "SBK")),
    ("d", ("40", "Bochow 16", "SBK"), ("305", "Eichhorst - 8", "Mesolithikum")),
    ("di", ("305", "Eichhorst - 8", "Mesolithikum"), ("40", "Bochow 16", "SBK")),
    ("f", ("49", "Selchow 7", "R\u00f6ssener Kultur"), ("258", "Flemsdorf 10", "R\u00f6ssener Kultur")),
    ("fi", ("258", "Flemsdorf 10", "R\u00f6ssener Kultur"), ("49", "Selchow 7", "R\u00f6ssener Kultur")),
    ("=", ("1", "T\u00fcngeda", "SBK"), ("2", "Goldbach", "SBK")),
]


def _classify(xs: int, xe: int, rs: int, re: int) -> str:
    if xs == rs and xe == re:
        return "equals"
    if xs == rs and xe < re:
        return "starts"
    if xs == rs and xe > re:
        return "startedby"
    if xe == re and xs > rs:
        return "finishes"
    if xe == re and xs < rs:
        return "finishedby"
    if xs > rs and xe < re:
        return "during"
    if xs < rs and xe > re:
        return "contains"
    if xs < rs and xe > rs and xe < re:
        return "overlaps"
    if xs > rs and xs < re and xe > re:
        return "overlappedby"
    if xe == rs:
        return "meets"
    if xs == re:
        return "metby"
    if xe < rs:
        return "before"
    if xs > re:
        return "after"
    return "?"


def _connected(codes: list[str]) -> bool:
    nodes = set(codes)
    if not nodes:
        return True
    start = next(iter(nodes))
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        for v in ADJ[u]:
            if v in nodes and v not in seen:
                seen.add(v)
                q.append(v)
    return seen == nodes


def _achievable(xs_c: int, xe_c: int, xcs: int, xce: int,
                 rs_c: int, re_c: int, rcs: int, rce: int) -> list[str]:
    """Every Allen relation reachable somewhere inside the real
    +/-margin box around (xs_c,xe_c) vs (rs_c,re_c). Not random sampling:
    the candidate set per variable is its two margin extremes, its own
    centre, and any of the *other* three variables' centres that happen
    to fall inside its range -- exactly the points where a classify()
    branch can change, so a full Cartesian product over these candidates
    (a few hundred combinations, not millions) finds every achievable
    relation including the exact-touch ones (meets/starts/finishes/
    equals), which zero-probability random sampling would miss."""
    others = [xs_c, xe_c, rs_c, re_c]

    def cands(centre: int, cert: int) -> list[int]:
        lo, hi = centre - cert, centre + cert
        out = {lo, hi, centre}
        out.update(o for o in others if lo <= o <= hi)
        return sorted(out)

    found = set()
    for xs in cands(xs_c, xcs):
        for xe in cands(xe_c, xce):
            if xs >= xe:
                continue
            for rs in cands(rs_c, rcs):
                for re in cands(re_c, rce):
                    if rs >= re:
                        continue
                    found.add(_classify(xs, xe, rs, re))
    return sorted(CODE[r] for r in found)


# Seven real FID pairs -- (x, y, x_cert, y_cert) -- with the computed,
# connectivity-checked achievable set. x/y = (fid, name, kultur, start, end).
FRESKA_EXAMPLES = [
    (("40", "Bochow 16", "SBK", -4804, -4597), (100, 100),
     ("305", "Eichhorst - 8", "Mesolithikum", -8000, -4000), (100, 100)),
    (("40", "Bochow 16", "SBK", -4804, -4597), (100, 100),
     ("78", "Nowe Objezierze 7", "SBK", -4800, -4350), (100, 100)),
    (("78", "Nowe Objezierze 7", "SBK", -4800, -4350), (100, 100),
     ("153", "Racot 18", "BKK", -4350, -3900), (50, 100)),
    (("40", "Bochow 16", "SBK", -4804, -4597), (100, 100),
     ("32", "Steckelsdorf 12", "FBG", -4550, -3900), (100, 100)),
    (("1", "T\u00fcngeda", "SBK", -4800, -4750), (100, 100),
     ("78", "Nowe Objezierze 7", "SBK", -4800, -4350), (100, 100)),
    (("49", "Selchow 7", "R\u00f6ssener Kultur", -4650, -4450), (100, 100),
     ("258", "Flemsdorf 10", "R\u00f6ssener Kultur", -4700, -4450), (100, 100)),
    (("1", "T\u00fcngeda", "SBK", -4800, -4750), (100, 100),
     ("2", "Goldbach", "SBK", -4800, -4750), (100, 100)),
]


def _lattice(cx0: float, cy0: float, w: float, h: float, filled: set[str],
             *, labeled: bool = False) -> list[str]:
    """One conceptual-neighbourhood lattice, scaled into a cx0,cy0,w,h
    box. ``labeled`` draws the reference legend (bigger, unfilled,
    node codes visible); otherwise the small filled/unfilled dot form
    used for every worked example."""
    sx, sy = w / 64.0, h / 84.0
    scale = min(sx, sy)

    def px(k: str) -> tuple[float, float]:
        x, y = NODES[k]
        return cx0 + x * sx, cy0 + y * sy

    parts = []
    for a, b in EDGES:
        ax, ay = px(a)
        bx, by = px(b)
        parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
                     f'stroke="{AF["lattice_edge"]}" stroke-width="1.3"/>')
    r = 8.5 * scale if labeled else 3.6 * scale
    for k in ORDER:
        nx, ny = px(k)
        on = k in filled
        fill = FRESKA if (on and not labeled) else AF["node_empty_fill"]
        stroke = FRESKA if (on and not labeled) else (ALLEN if labeled else AF["node_empty_stroke"])
        parts.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{r:.1f}" fill="{fill}" '
                     f'stroke="{stroke}" stroke-width="1.4"/>')
        if labeled:
            parts.append(f'<text x="{nx:.1f}" y="{ny + 3.2 * scale:.1f}" text-anchor="middle" '
                         f'font-family="Fira Sans" font-weight="600" '
                         f'font-size="{8.5 * scale:.1f}" fill="{ALLEN}">{vu.xml_escape(k)}</text>')
    return parts


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("Allen's 13 relations as a bar grid, Freksa's neighbourhood lattice with computed real examples")]

    intro = tt("Bildsprache aus \u201eVon Allen zu Freksa\u201c (Florians Referenz-Artikel, 2026-09-16) \u2014 alle FIDs/Jahre real",
               "Visual form from \u201eVon Allen zu Freksa\u201c (Florian's reference article, 2026-09-16) \u2014 every FID/year real")
    parts.append(f'<text x="90" y="42" font-family="Fira Sans" font-size="13" font-style="italic" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(intro)}</text>')

    # ============================================================= left: Allen bar grid
    allen_title = tt("Allens 13 Relationen als Balkenraster", "Allen's 13 relations as a bar grid")
    parts.append(f'<text x="90" y="78" font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(allen_title)}</text>')
    allen_legend = tt("Balkenform schematisch wie im Original (Abb. 1) \u2014 petrol = X (fest), ocher = Y \u2014 gelesen als \u201eX <r> Y\u201c; FID/Name/Kultur sind real",
                       "Bar shape schematic, as in the original (Abb. 1) \u2014 petrol = X (fixed), ocher = Y \u2014 read as \u2018X <r> Y\u2019; FID/name/culture are real")
    parts.append(f'<text x="90" y="96" font-family="Fira Sans" font-size="10.3" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(allen_legend)}</text>')

    gx0, gx1 = 90, 950
    g_y0, cols, gap = 118, 4, 18
    cell_w = (gx1 - gx0 - (cols - 1) * gap) / cols
    row_h = 140
    scale = (cell_w - 12) / 120.0

    for i, (code, x_iv, y_iv) in enumerate(ALLEN_CELLS):
        col, row = i % cols, i // cols
        lx = gx0 + col * (cell_w + gap)
        ly = g_y0 + row * (row_h + gap)
        parts.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{cell_w:.1f}" height="{row_h:.1f}" '
                     f'rx="6" fill="#fbfbf9" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

        xfid, xname, xkultur = x_iv
        yfid, yname, ykultur = y_iv
        x_cap = f"X = FID{xfid} \u00b7 {xname} ({xkultur})"
        y_cap = f"Y = FID{yfid} \u00b7 {yname} ({ykultur})"
        parts.append(f'<text x="{lx + 8:.1f}" y="{ly + 13:.1f}" font-family="Fira Sans" font-size="9" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(x_cap)}</text>')

        ix0 = lx + 8
        b1, b2 = BARS[code]
        parts.append(f'<rect x="{ix0 + 40 * scale:.1f}" y="{ly + 20:.1f}" '
                     f'width="{40 * scale:.1f}" height="9" rx="2" fill="{ALLEN}"/>')
        parts.append(f'<rect x="{ix0 + b1 * scale:.1f}" y="{ly + 33:.1f}" '
                     f'width="{max(2, (b2 - b1) * scale):.1f}" height="9" rx="2" fill="{FRESKA}"/>')

        parts.append(f'<text x="{lx + 8:.1f}" y="{ly + 58:.1f}" font-family="Fira Sans" font-size="9" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(y_cap)}</text>')
        parts.append(f'<text x="{lx + 8:.1f}" y="{ly + 78:.1f}" font-family="Fira Sans" font-weight="600" '
                     f'font-size="13" fill="{ALLEN}">{vu.xml_escape(code)}'
                     f'<tspan font-family="Fira Sans" font-weight="400" font-size="11" fill="{vu.TEXT_MUTED}">'
                     f'  {vu.xml_escape(NAMES[code])}</tspan></text>')

    # ============================================================= right: Freksa lattice gallery
    rx0, rx1 = 1010, 1690
    freksa_title = tt("Freksas Nachbarschaftsgitter \u2014 sieben berechnete Beispiele",
                       "Freksa's neighbourhood lattice \u2014 seven computed examples")
    parts.append(f'<text x="{rx0}" y="78" font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(freksa_title)}</text>')

    para = tt(["Jede echte Datierung tr\u00e4gt einen echten Spielraum (\u00b110 bis \u00b1200 Jahre,",
               "siehe 06-uncertainty-dating). F\u00fcr jedes der sieben Paare unten wurde",
               "berechnet, nicht geraten, welche der 13 Relationen innerhalb der Spanne",
               "noch m\u00f6glich sind \u2014 und ob diese Menge im Gitter zusammenh\u00e4ngt."],
              ["Every real dating carries a real margin (\u00b110 to \u00b1200 years,",
               "see 06-uncertainty-dating). For each of the seven pairs below, which of",
               "the 13 relations remain possible within that margin was computed, not",
               "guessed \u2014 and whether that set is connected in the lattice."])
    py = 98
    for line in para:
        parts.append(f'<text x="{rx0}" y="{py}" font-family="Fira Sans" font-size="11.3" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        py += 16

    fcols, fgap = 4, 18
    ficon_w = (rx1 - rx0 - (fcols - 1) * fgap) / fcols
    ficon_draw = ficon_w - 20
    ficon_h = ficon_draw * 84 / 64
    frow_h = 22 + ficon_h + 34
    fy0 = py + 14

    # slot 0: labelled legend
    legend_cap = tt("Legende: alle 13, unausgef\u00fcllt", "Legend: all 13, unfilled")
    parts.append(f'<text x="{rx0:.1f}" y="{fy0 + 12:.1f}" font-family="Fira Sans" font-weight="600" '
                 f'font-size="10" fill="{vu.TEXT_DARK}">{vu.xml_escape(legend_cap)}</text>')
    parts += _lattice(rx0 + 8, fy0 + 22, ficon_draw, ficon_h, set(ORDER), labeled=True)

    for i, (x_iv, x_cert, r_iv, r_cert) in enumerate(FRESKA_EXAMPLES):
        slot = i + 1
        col, row = slot % fcols, slot // fcols
        cx0 = rx0 + col * (ficon_w + fgap)
        cy0 = fy0 + row * (frow_h + fgap)

        xfid, xname, xkultur, xs, xe = x_iv
        rfid, rname, rkultur, rs, re = r_iv
        codes = _achievable(xs, xe, x_cert[0], x_cert[1], rs, re, r_cert[0], r_cert[1])
        conn = _connected(codes)
        crisp = CODE[_classify(xs, xe, rs, re)]

        set_label = "{" + ",".join(codes) + "}" if len(codes) < 13 else tt("alle 13", "all 13")
        parts.append(f'<text x="{cx0:.1f}" y="{cy0 + 12:.1f}" font-family="Fira Sans" font-weight="600" '
                     f'font-size="10" fill="{FRESKA if conn else vu.UNCERTAIN_STROKE}">'
                     f'{vu.xml_escape(set_label)}</text>')
        parts += _lattice(cx0 + 8, cy0 + 22, ficon_draw, ficon_h, set(codes))

        cy_txt = cy0 + 22 + ficon_h + 12
        cap1 = f"FID{xfid} {xname} \u00d7 FID{rfid} {rname}"
        cap2 = tt(f"scharf: {crisp} \u00b7 {x_cert[0]}/{x_cert[1]} \u00b7 {r_cert[0]}/{r_cert[1]} J.",
                  f"crisp: {crisp} \u00b7 {x_cert[0]}/{x_cert[1]} \u00b7 {r_cert[0]}/{r_cert[1]}y")
        parts.append(f'<text x="{cx0:.1f}" y="{cy_txt:.1f}" font-family="Fira Sans" font-size="8.7" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(cap1)}</text>')
        parts.append(f'<text x="{cx0:.1f}" y="{cy_txt + 13:.1f}" font-family="Fira Sans" font-size="8.7" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(cap2)}</text>')

    note_y = fy0 + 2 * (frow_h + fgap) + 6
    note_lines = tt(
        ["Alle sieben Ergebnismengen sind zusammenh\u00e4ngend (Freksas Nachbarschafts-",
         "Theorem, nicht so gew\u00e4hlt) \u2014 auch das \u201eequals\u201c-Paar oben rechts: die volle",
         "Menge aller 13 ist trivial zusammenh\u00e4ngend, sagt dann aber nichts mehr aus."],
        ["All seven result sets are connected (Freksa's neighbourhood theorem,",
         "not chosen to be) \u2014 including the \u2018equals\u2019 pair, top right: the full set",
         "of all 13 is trivially connected too, it just stops saying anything."])
    for i, line in enumerate(note_lines):
        parts.append(f'<text x="{rx0}" y="{note_y + i * 15:.1f}" font-family="Fira Sans" font-size="10.3" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"allen-freksa-examples.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

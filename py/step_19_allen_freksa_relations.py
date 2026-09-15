#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_19_allen_freksa_relations.py -- Allen's 13 relations, then a Freksa sketch
=================================================================================

Source: builds directly on the two lines already in
``step_06_uncertainty_dating.py`` ("opens Allen relations: Phase A ends
before Phase B begins") -- this is that note, opened up. Left panel:
Allen (1983)'s 13 interval relations, shown as the standard seven
canonical rows (relation + its inverse in one picture, e.g. "meets /
met-by"). Right panel: a sketch of what Freksa's semi-interval /
conceptual-neighbourhood extension would add once ``datingCertaintyStart``/
``End`` margins are taken into account instead of ignored.

**Every example pair in the left panel is real**, taken from
``data/raw/bb-5kbc-sites/fst_wgs84_lit_enriched.csv`` (FID, fst_name,
kultur, dating_start, dating_end) and verified once by classifying every
pair of the CSV's 18 *distinct* (dating_start, dating_end) intervals by
hand-written Allen predicates, then checking the result against the
expected relation before picking it for a row (2026-09-15h). No
invented site names or years -- see item S31 in PRIMER.md for why that
distinction matters in this repo. FID 1 ("T\u00fcngeda") and FID 78
("Nowe Objezierze 7") each appear twice, because the real data happens
to pair them with two different relations (starts/started-by and,
for 78, also meets) -- not because a distinct example was unavailable.

The right panel's worked example reuses the real "meets" pair (FID 78
meets FID 153 at year \u22124350) together with their real
``dating_certainty_start``/``_end`` values (\u00b1100 / \u00b150 years) --
also directly from the CSV, not invented. What the panel does with
those numbers (the "could really be: before / meets / overlaps" framing)
is illustrative reasoning, stated by hand, not a point-algebra
computation -- the closing panel says this explicitly, the same way
the docstring above says which parts of a figure are checked and which
are not.

Relation names (before, meets, overlaps, starts, during, finishes,
equal, and their inverses) are Allen's own English terms in *both*
language versions -- there is no settled German equivalent in the GIS/
temporal-reasoning literature, and treating them as an untranslated
technical identifier matches how this repo already leaves
``crm:E52_Time-Span`` unchanged in the German figures (see step_00
docstring for the general convention; class/property names that
*are* bb5kbc: vocabulary still go through ``vu.cls()``/``vu.prop()``
as usual).

Writes: allen-freksa-relations.de.svg/.png, allen-freksa-relations.en.svg/.png
Run standalone: ``python py/step_19_allen_freksa_relations.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["19-allen-freksa-relations"]
DATING = vu.WORLD_COLORS["time"]          # R (reference interval) -- same teal as 06/08's time:Interval
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}  # X (the varying interval)
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE


def yr(n: int) -> str:
    """Format a year the way the rest of this repo does: a real minus
    sign for BCE, not a hyphen (every year in this dataset is BCE)."""
    return f"\u2212{abs(n)}" if n < 0 else str(n)


# Seven canonical Allen rows (relation, inverse, X, R), each a real,
# verified pair from fst_wgs84_lit_enriched.csv -- see docstring above.
# X = (fid, name, kultur, start, end); R likewise.
ROWS = [
    ("before", "after",
     ("40", "Bochow 16", "SBK", -4804, -4597),
     ("32", "Steckelsdorf 12", "FBG", -4550, -3900)),
    ("meets", "met-by",
     ("78", "Nowe Objezierze 7", "SBK", -4800, -4350),
     ("153", "Racot 18", "BKK", -4350, -3900)),
    ("overlaps", "overlapped-by",
     ("40", "Bochow 16", "SBK", -4804, -4597),
     ("78", "Nowe Objezierze 7", "SBK", -4800, -4350)),
    ("starts", "started-by",
     ("1", "T\u00fcngeda", "SBK", -4800, -4750),
     ("78", "Nowe Objezierze 7", "SBK", -4800, -4350)),
    ("during", "contains",
     ("40", "Bochow 16", "SBK", -4804, -4597),
     ("305", "Eichhorst - 8", "Mesolithikum", -8000, -4000)),
    ("finishes", "finished-by",
     ("49", "Selchow 7", "R\u00f6ssener Kultur", -4650, -4450),
     ("258", "Flemsdorf 10", "R\u00f6ssener Kultur", -4700, -4450)),
    ("equal", "equal",
     ("1", "T\u00fcngeda", "SBK", -4800, -4750),
     ("2", "Goldbach", "SBK", -4800, -4750)),
]


def _row(y_top: float, rel: str, inv: str, x_iv, r_iv, tx0: float, tx1: float) -> list[str]:
    parts = []
    xfid, xname, xkultur, xs, xe = x_iv
    rfid, rname, rkultur, rs, re = r_iv

    parts.append(f'<text x="90" y="{y_top + 34:.1f}" font-family="Fira Sans" font-weight="500" '
                 f'font-size="16" fill="{vu.TEXT_DARK}">{vu.xml_escape(rel)}</text>')
    if rel != inv:
        parts.append(f'<text x="90" y="{y_top + 54:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">/ {vu.xml_escape(inv)}</text>')

    lo_raw, hi_raw = min(xs, rs), max(xe, re)
    pad = max(15, (hi_raw - lo_raw) * 0.08)
    lo, span = lo_raw - pad, (hi_raw + pad) - (lo_raw - pad)

    def mx(year: float) -> float:
        return tx0 + (year - lo) / span * (tx1 - tx0)

    x_cap = f"FID{xfid} \u00b7 {xname} ({xkultur}) \u00b7 {yr(xs)} \u2013 {yr(xe)}"
    r_cap = f"FID{rfid} \u00b7 {rname} ({rkultur}) \u00b7 {yr(rs)} \u2013 {yr(re)}"
    parts.append(f'<text x="{tx0:.1f}" y="{y_top + 10:.1f}" font-family="Fira Sans" font-size="10.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(x_cap)}</text>')
    parts.append(f'<text x="{tx0:.1f}" y="{y_top + 88:.1f}" font-family="Fira Sans" font-size="10.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(r_cap)}</text>')

    # touching-boundary guide (only when a real shared coordinate exists)
    for boundary in {xe if xe == rs else None, xs if xs == rs else None, xe if xe == re else None}:
        if boundary is not None:
            bx = mx(boundary)
            parts.append(f'<line x1="{bx:.1f}" y1="{y_top + 14:.1f}" x2="{bx:.1f}" y2="{y_top + 68:.1f}" '
                         f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1" stroke-dasharray="3 4"/>')

    x0, x1 = mx(xs), mx(xe)
    parts.append(f'<rect x="{x0:.1f}" y="{y_top + 16:.1f}" width="{max(3, x1 - x0):.1f}" height="16" rx="4" '
                 f'fill="{NEUTRAL["fill"]}" stroke="{NEUTRAL["stroke"]}" stroke-width="1.4"/>')
    r0, r1 = mx(rs), mx(re)
    parts.append(f'<rect x="{r0:.1f}" y="{y_top + 42:.1f}" width="{max(3, r1 - r0):.1f}" height="16" rx="4" '
                 f'fill="{DATING["fill"]}" stroke="{DATING["stroke"]}" stroke-width="1.4"/>')
    return parts


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("Allen's 13 interval relations, then a Freksa/semi-interval sketch under real dating uncertainty")]

    intro = tt("Skizze \u2014 baut auf der \u201eAllen-Relationen\u201c-Notiz in 06-uncertainty-dating auf; "
               "alle Werte real, siehe FID-Angaben",
               "Sketch \u2014 builds on the \u201eopens Allen relations\u201c note in 06-uncertainty-dating; "
               "every value real, see FID references")
    parts.append(f'<text x="90" y="42" font-family="Fira Sans" font-size="13" font-style="italic" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(intro)}</text>')

    # ---------------------------------------------------------------- left: Allen gallery
    gallery_title = tt("Allens 13 Relationen, sieben kanonische Paare",
                        "Allen's 13 relations, seven canonical pairs")
    parts.append(f'<text x="90" y="78" font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(gallery_title)}</text>')
    legend = tt("Nach Allen (1983), englisch zitiert \u2014 grau = X (variiert) \u00b7 gr\u00fcnlich = R (Referenz)",
                "Allen (1983) names, cited in English \u2014 grey = X (varies) \u00b7 teal = R (reference)")
    parts.append(f'<text x="90" y="96" font-family="Fira Sans" font-size="11" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(legend)}</text>')

    tx0, tx1 = 250, 950
    y0, row_h = 132, 112
    for i, (rel, inv, x_iv, r_iv) in enumerate(ROWS):
        parts += _row(y0 + i * row_h, rel, inv, x_iv, r_iv, tx0, tx1)

    # ---------------------------------------------------------------- right: Freksa sketch
    rx0, rx1 = 1010, 1690
    freksa_title = tt("Was Freksa erg\u00e4nzt: Relationen unter Endpunkt-Unsicherheit",
                       "What Freksa adds: relations under endpoint uncertainty")
    parts.append(f'<text x="{rx0}" y="78" font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(freksa_title)}</text>')

    para_de = [
        "Jede Datierung tr\u00e4gt bereits einen Spielraum \u2014 datingCertaintyStart/End,",
        "\u00b110 bis \u00b1200 Jahre je nach Fundstelle (siehe 06-uncertainty-dating).",
        "Eine scharfe Allen-Relation schaut nur auf die zwei exakten Zahlen und",
        "ignoriert diesen Spielraum. Freksas Semi-Intervalle teilen jedes",
        "Intervall in Start- und Endpunkt und fragen, wo jeder Punkt innerhalb",
        "seines Spielraums plausibel liegen k\u00f6nnte \u2014 das schr\u00e4nkt die Antwort",
        "auf eine Nachbarschaft von Relationen ein, statt sie festzulegen.",
    ]
    para_en = [
        "Every dating already carries a margin \u2014 datingCertaintyStart/End,",
        "\u00b110 to \u00b1200 years depending on the site (see 06-uncertainty-dating).",
        "A crisp Allen relation looks only at the two exact numbers and",
        "ignores that margin. Freksa's semi-intervals split each interval",
        "into a start-point and an end-point and ask where each point could",
        "plausibly sit within its margin \u2014 narrowing the answer to a",
        "neighbourhood of relations, rather than pinning down one.",
    ]
    py = 108
    for line in tt(para_de, para_en):
        parts.append(f'<text x="{rx0}" y="{py}" font-family="Fira Sans" font-size="12.3" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        py += 19

    worked_title = tt("Durchgerechnetes Beispiel \u2014 das echte \u201emeets\u201c-Paar aus der Galerie",
                       "Worked example \u2014 the real \u2018meets\u2019 pair from the gallery")
    parts.append(f'<text x="{rx0}" y="{py + 20}" font-family="Fira Sans" font-weight="500" font-size="13" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(worked_title)}</text>')
    sub = tt(f"FID78 Nowe Objezierze 7 (SBK) meets FID153 Racot 18 (BKK) bei {yr(-4350)}",
             f"FID78 Nowe Objezierze 7 (SBK) meets FID153 Racot 18 (BKK) at {yr(-4350)}")
    parts.append(f'<text x="{rx0}" y="{py + 40}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(sub)}</text>')

    # -- mini uncertainty diagram: the real +/-100y and +/-50y margins around -4350 --
    d_lo, d_hi = -4490.0, -4210.0
    d_span = d_hi - d_lo
    dx0, dx1 = rx0 + 10, rx1 - 10
    d_top = py + 62

    def dmx(year: float) -> float:
        return dx0 + (year - d_lo) / d_span * (dx1 - dx0)

    band_x_lo, band_x_hi = dmx(-4450), dmx(-4250)   # Nowe Objezierze 7 end, +/-100y
    band_r_lo, band_r_hi = dmx(-4400), dmx(-4300)   # Racot 18 start, +/-50y
    parts.append(f'<rect x="{band_x_lo:.1f}" y="{d_top + 6:.1f}" width="{band_x_hi - band_x_lo:.1f}" height="22" '
                 f'rx="4" fill="{U_FILL}" stroke="{U_STROKE}" stroke-width="1.2" opacity="0.75"/>')
    band_x_label = tt("Nowe Objezierze 7, Ende \u00b1100 J.", "Nowe Objezierze 7, end \u00b1100y")
    parts.append(f'<text x="{dx0:.1f}" y="{d_top + 2:.1f}" font-family="Fira Sans" font-size="10" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(band_x_label)}</text>')

    parts.append(f'<rect x="{band_r_lo:.1f}" y="{d_top + 38:.1f}" width="{band_r_hi - band_r_lo:.1f}" height="22" '
                 f'rx="4" fill="{U_STROKE}" stroke="{U_STROKE}" stroke-width="1.2" opacity="0.55"/>')
    band_r_label = tt("Racot 18, Start \u00b150 J.", "Racot 18, start \u00b150y")
    parts.append(f'<text x="{dx0:.1f}" y="{d_top + 34:.1f}" font-family="Fira Sans" font-size="10" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(band_r_label)}</text>')

    boundary_x = dmx(-4350)
    boundary_label = tt(f"{yr(-4350)} \u00b7 scharfe Grenze", f"{yr(-4350)} \u00b7 crisp boundary")
    parts.append(f'<line x1="{boundary_x:.1f}" y1="{d_top:.1f}" x2="{boundary_x:.1f}" y2="{d_top + 78:.1f}" '
                 f'stroke="{vu.TEXT_DARK}" stroke-width="1.4"/>')
    parts.append(f'<text x="{boundary_x:.1f}" y="{d_top + 92:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="10" fill="{vu.TEXT_DARK}">{vu.xml_escape(boundary_label)}</text>')

    pointer_line = tt("\u2192 je nachdem, wo die wahre Grenze innerhalb des Spielraums liegt, k\u00f6nnte \u201emeets\u201c in Wahrheit sein:",
                       "\u2192 depending on where the true boundary falls within the margin, \u2018meets\u2019 could really be:")
    parts.append(f'<text x="{rx0}" y="{d_top + 116}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(pointer_line)}</text>')

    pill_y = d_top + 132
    for i, label in enumerate(["before", "meets", "overlaps"]):
        pw = 86
        px = rx0 + i * (pw + 12)
        parts.append(f'<rect x="{px:.1f}" y="{pill_y:.1f}" width="{pw}" height="26" rx="13" '
                     f'fill="{U_FILL}" stroke="{U_STROKE}" stroke-width="1.3"/>')
        parts.append(f'<text x="{px + pw / 2:.1f}" y="{pill_y + 13:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" font-size="12" '
                     f'fill="{U_STROKE}">{vu.xml_escape(label)}</text>')

    bridge = tt("Dieselben \u00b110/50/100/200-Jahres-Spannen aus 06-uncertainty-dating w\u00fcrden das antreiben \u2014 nichts Neues zu messen.",
                "The same \u00b110/50/100/200-year margins already in 06-uncertainty-dating would drive this \u2014 nothing new to measure.")
    parts.append(f'<text x="{rx0}" y="{pill_y + 50}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(bridge)}</text>')

    note_y = pill_y + 80
    parts.append(vu.svg_dashed_container(rx0, note_y, rx1 - rx0, 120,
                                          tt("Skizze, keine Berechnung", "Sketch, not a computation")))
    note_de = [
        "Die Relationsnamen im Beispiel oben sind von Hand aus den echten",
        "\u00b1100/\u00b150-Jahres-Spannen abgeleitet, nicht aus einer Punktalgebra-",
        "Implementierung. Eine vollst\u00e4ndige Freksa(1992)-Behandlung ist",
        "zuk\u00fcnftige Arbeit \u2014 noch nicht in queries.yaml oder einer .rq-Datei.",
    ]
    note_en = [
        "The relation names in the example above are stated by hand from",
        "the real \u00b1100/\u00b150-year margins, not derived from a point-algebra",
        "implementation. A full Freksa (1992) treatment is future work \u2014",
        "not yet in queries.yaml or any .rq file.",
    ]
    ny = note_y + 42
    for line in tt(note_de, note_en):
        parts.append(f'<text x="{rx0 + 16}" y="{ny}" font-family="Fira Sans" font-size="11.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        ny += 19

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"allen-freksa-relations.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

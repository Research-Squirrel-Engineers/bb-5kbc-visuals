#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_17_stats_infographic.py -- 540 sites, where they actually are
=======================================================================

Source: computed directly from ``data/fst_wgs84.csv`` (540 rows), not
from the paper's rounded prose. ``Counter`` over the ``bundesland``
column (folding the raw "MVP" value to "Mecklenburg-Vorpommern", the
alias step_02 already discusses) gives an exact, complete regional
breakdown: 362 DE sites across 5 Bundeslaender, 178 PL sites across 10
Wojewodschaften. Note the discrepancy with the paper's own prose, which
says "neun Wojewodschaften" and "350" for Germany: the ``land`` column
(country-level) is empty for 12 rows, all of them Brandenburg, resolved
to Germany only at LOD-generation time via a fallback rule -- the paper's
350 counts only the explicit "Deutschland" rows, this figure's 362 counts
by the always-populated ``bundesland`` column instead (350 + 12 = 362).
Both are correct, they just count at different pipeline stages; this
figure says so rather than picking one silently. The tenth Wojewodschaft
(Woj. Pomorskie, 3 sites) is real, verified data, not a rounding
correction.

Bilingual (revision) -- see step_00 docstring for the convention. Region
names are real place names and are never translated.

Writes: stats-infographic.de.svg/.png, stats-infographic.en.svg/.png
Run standalone: ``python py/step_17_stats_infographic.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["17-stats-infographic"]
GEO = vu.GEO
SITE = vu.SITE

DE_REGIONS = [
    ("Brandenburg", 324), ("Sachsen-Anhalt", 24), ("Th\u00fcringen", 7),
    ("Sachsen", 6), ("Mecklenburg-Vorpommern", 1),
]
PL_REGIONS = [
    ("Woj. Kujawsko-Pomorskie", 91), ("Woj. Dolno\u015bl\u0105skie", 31),
    ("Woj. Zachodniopomorskie", 21), ("Woj. Lubuskie", 17), ("Woj. Wielkopolskie", 8),
    ("Woj. Opolskie", 3), ("Woj. Pomorskie", 3), ("Woj. Warmi\u0144sko-Mazurskie", 2),
    ("Woj. Ma\u0142opolskie", 1), ("Woj. \u015al\u0105skie", 1),
]


def _bars(parts, x, y0, w, pitch, bar_h, data, max_val, color):
    label_w = 230
    bar_x = x + label_w
    bar_max_w = w - label_w - 70
    for i, (name, count) in enumerate(data):
        ry = y0 + i * pitch
        parts.append(f'<text x="{x:.1f}" y="{ry + bar_h/2:.1f}" dominant-baseline="central" '
                     f'font-family="Fira Sans" font-size="13" fill="{vu.TEXT_DARK}">{vu.xml_escape(name)}</text>')
        bw = max(4, count / max_val * bar_max_w)
        parts.append(f'<rect x="{bar_x:.1f}" y="{ry:.1f}" width="{bw:.1f}" height="{bar_h:.1f}" rx="5" '
                     f'fill="{color["fill"]}" stroke="{color["stroke"]}" stroke-width="1.4"/>')
        parts.append(f'<text x="{bar_x + bw + 10:.1f}" y="{ry + bar_h/2:.1f}" dominant-baseline="central" '
                     f'font-family="Fira Sans" font-weight="500" font-size="12.5" '
                     f'fill="{vu.TEXT_DARK}">{count}</text>')


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("540 archaeological sites: dataset scale and where they actually are")]

    parts.append(f'<text x="60" y="115" font-family="Fira Sans" font-weight="500" font-size="72" '
                 f'fill="{vu.BB5KBC_MAGENTA}">540</text>')
    sub1 = tt("arch\u00e4ologische Fundstellen, 5. Jahrtausend v. Chr.",
              "archaeological sites, 5th millennium BC")
    sub2 = tt("Brandenburg, Ostdeutschland, West- bis Mittelpolen",
              "Brandenburg, eastern Germany, western to central Poland")
    parts.append(f'<text x="320" y="90" font-family="Fira Sans" font-size="17" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(sub1)}</text>')
    parts.append(f'<text x="320" y="118" font-family="Fira Sans" font-size="14.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(sub2)}</text>')

    # -- two regional panels ---------------------------------------------------
    py = 180
    lx, lw = 60, 790
    rx, rw = 890, 790
    parts.append(vu.svg_dashed_container(lx, py, lw, 640,
                                          tt("Deutschland \u2014 362 Fundstellen (5 Bundesl\u00e4nder, nach bundesland-Spalte)",
                                             "Germany \u2014 362 sites (5 federal states, by the bundesland column)")))
    _bars(parts, lx + 40, py + 70, lw - 80, 108, 40, DE_REGIONS, DE_REGIONS[0][1], GEO)

    parts.append(vu.svg_dashed_container(rx, py, rw, 640,
                                          tt("Polen \u2014 178 Fundstellen (10 Wojewodschaften)",
                                             "Poland \u2014 178 sites (10 voivodeships)")))
    _bars(parts, rx + 40, py + 60, rw - 80, 56, 32, PL_REGIONS, PL_REGIONS[0][1], SITE)

    note = tt("Paper-Text nennt \u201eneun Wojewodschaften\u201c und \u201e350\u201c f\u00fcr Deutschland \u2014 beide Z\u00e4hlungen "
              "sind korrekt, nur an verschiedenen Pipeline-Stufen: 350 z\u00e4hlt die CSV-Spalte land vor der "
              "Fallback-Regel (12 leere Brandenburg-Zellen \u2192 Deutschland); diese Grafik z\u00e4hlt nach der "
              "immer vollst\u00e4ndigen Spalte bundesland (350 + 12 = 362). Woj. Pomorskie (3 Fundstellen) ist "
              "real, keine Rundungskorrektur.",
              "The paper's prose says \u201cnine Wojewodschaften\u201d and \u201c350\u201d for Germany \u2014 both counts "
              "are correct, just at different pipeline stages: 350 counts the CSV's land column before the "
              "fallback rule (12 empty Brandenburg cells \u2192 Germany); this figure counts by the always-complete "
              "bundesland column instead (350 + 12 = 362). Woj. Pomorskie (3 sites) is real data, not a rounding fix.")
    words = note.split()
    lines = []
    cur = []
    curlen = 0
    for w in words:
        if curlen + len(w) + 1 > 130:
            lines.append(" ".join(cur))
            cur = []
            curlen = 0
        cur.append(w)
        curlen += len(w) + 1
    if cur:
        lines.append(" ".join(cur))
    ny = 850
    for line in lines:
        parts.append(f'<text x="60" y="{ny:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        ny += 19

    # -- dataset-scale footer strip ---------------------------------------------
    stats = [
        ("65", tt("CSV-Spalten", "CSV columns")),
        ("15", tt("Ontologie-Klassen", "ontology classes")),
        ("~21 700", tt("Tripel (Daten)", "triples (data)")),
        ("~22 400", tt("Tripel (Bundle)", "triples (bundle)")),
    ]
    sx = 60
    for value, label in stats:
        parts.append(f'<text x="{sx:.1f}" y="{ny + 20:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="18" fill="{vu.TEXT_DARK}">{vu.xml_escape(value)}</text>')
        parts.append(f'<text x="{sx:.1f}" y="{ny + 40:.1f}" font-family="Fira Sans" font-size="11.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(label)}</text>')
        sx += 400

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"stats-infographic.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

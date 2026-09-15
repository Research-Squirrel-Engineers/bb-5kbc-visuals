#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_11_literature_enrichment.py -- Modus A: code dictionary as source of truth
====================================================================================

Source: paper section 3.1 ("Literaturbezogene Anreicherung") and Tab. 2
(the four-case logic). The two dictionaries (``QID_PUBLIKATION``,
``QID_QUELLE_GEOREF``) and their entry counts (46, 34) are named
explicitly in the paper; this is the counterpart to 01/02, which only
cover the *geographic* half of the enrichment (Wikidata fuzzy matching).
Literature enrichment works completely differently: a maintained
dictionary is authoritative over the CSV, not a similarity score.

Bilingual (revision) -- see step_00 docstring for the convention.

**Revision 2026-09-15 (correction):** the worked "overwritten" example
originally claimed a specific row ("CSV, Zeile 214") and a specific old
value ("Q100"). Checked against ``fst_wgs84_lit_enriched.csv``: FID 214
is real ("Brzesc Kujawski 10") but its actual publikation_arch is
"Grygiel 2008" with QID Q139304642 -- nothing to do with Pyzel 2019 or
"Q100", which doesn't appear anywhere in the data. The enrichment output
file only ever shows the *post*-correction state, so no live conflict is
observable in it to point to. Reworded as an explicitly illustrative
example (generic "Q_alt", no FID claimed) -- the one part that stays
real is the mapping itself, ``QID_PUBLIKATION["Pyzel 2019"] ==
"Q139460445"``, verified directly against ``enrich_qids.py`` (that file
also documents several genuine historical corrections to this same
dictionary -- e.g. a "Raddatz 1959" entry that turned out to be a typo
for "Raddatz 1958" -- confirming the *mechanism* this figure describes
is real, even though this specific worked example is not tied to one
row).

Writes: literature-enrichment.de.svg/.png, literature-enrichment.en.svg/.png
Run standalone: ``python py/step_11_literature_enrichment.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["11-literature-enrichment"]
C = vu.PIPELINE_COLORS["enrich"]
C_OK = vu.PIPELINE_COLORS["lod"]
C_WARN = vu.PIPELINE_COLORS["validate"]
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("Modus A: the code dictionary is the source of truth, the CSV is derived")]

    # -- top: the two dictionaries -------------------------------------------
    dw, dh = 620, 90
    d1x, d2x = 150, 980
    dy = 60
    parts.append(vu.svg_box(d1x, dy, dw, dh, "QID_PUBLIKATION", tt("46 Eintr\u00e4ge \u00b7 enrich_qids.py",
                                                                     "46 entries \u00b7 enrich_qids.py"),
                             fill=C["fill"], stroke=C["stroke"]))
    parts.append(vu.svg_box(d2x, dy, dw, dh, "QID_QUELLE_GEOREF", tt("34 Eintr\u00e4ge \u00b7 enrich_qids.py",
                                                                       "34 entries \u00b7 enrich_qids.py"),
                             fill=C["fill"], stroke=C["stroke"]))

    modus_label = tt("Modus A: Code-Dictionary = single source of truth, CSV = abgeleiteter Speicher",
                      "Modus A: the code dictionary is the single source of truth, the CSV is a derived store")
    parts.append(f'<text x="875" y="{dy + dh + 45:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="16" fill="{vu.BB5KBC_MAGENTA}">{vu.xml_escape(modus_label)}</text>')

    # -- four-case table -------------------------------------------------------
    ty0 = 230
    headers = [tt("Fall", "Case"), tt("Zelle in CSV", "CSV cell"), tt("Mapping", "Mapping"),
               tt("Aktion", "Action")]
    col_x = [90, 330, 700, 1000]
    col_w = [220, 350, 280, 600]
    for x, w, h in zip(col_x, col_w, headers):
        parts.append(f'<text x="{x:.1f}" y="{ty0:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="13" fill="{vu.TEXT_MUTED}">{vu.xml_escape(h)}</text>')
    parts.append(f'<line x1="90" y1="{ty0 + 14:.1f}" x2="1630" y2="{ty0 + 14:.1f}" stroke="#dedcd4" stroke-width="1"/>')

    rows = [
        ("filled", C_OK, tt("leer", "empty"), tt("QID vorhanden", "QID present"),
         tt("Zelle f\u00fcllen", "fill the cell")),
        ("confirmed", NEUTRAL, tt("QID stimmt \u00fcberein", "QID matches"), tt("QID vorhanden", "QID present"),
         tt("unver\u00e4ndert (No-op)", "unchanged (no-op)")),
        ("overwritten", C_WARN, tt("abweichender QID", "differing QID"), tt("QID vorhanden", "QID present"),
         tt("\u00fcberschreiben + Konflikt loggen (alter/neuer QID, Zeile)",
            "overwrite + log the conflict (old/new QID, row)")),
        ("noop", NEUTRAL, tt("egal", "any"), tt("kein Eintrag", "no entry"),
         tt("unver\u00e4ndert (Miss-Log-Eintrag)", "unchanged (miss-log entry)")),
    ]
    ry = ty0 + 46
    pitch = 90
    for case, colors, cell, mapping, action in rows:
        badge_w = vu.text_width(case, 13) + 32
        parts.append(f'<rect x="{col_x[0]:.1f}" y="{ry - 24:.1f}" width="{badge_w:.1f}" height="32" rx="16" '
                     f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.6"/>')
        parts.append(f'<text x="{col_x[0] + badge_w/2:.1f}" y="{ry - 8:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" font-size="13" '
                     f'fill="{colors["stroke"]}">{vu.xml_escape(case)}</text>')
        parts.append(f'<text x="{col_x[1]:.1f}" y="{ry - 8:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(cell)}</text>')
        parts.append(f'<text x="{col_x[2]:.1f}" y="{ry - 8:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(mapping)}</text>')
        parts.append(f'<text x="{col_x[3]:.1f}" y="{ry - 8:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(action)}</text>')
        ry += pitch

    # -- worked example: overwritten -------------------------------------------
    wy = ry + 20
    parts.append(vu.svg_dashed_container(60, wy, 1630, 280,
                                          tt("Beispiel: der Fall \u201eoverwritten\u201c (illustrativ, kein konkreter FID)",
                                             "Worked example: the \u201coverwritten\u201d case (illustrative, no specific FID)")))
    ex_y = wy + 60
    b1w = 460
    b1h = 64
    parts.append(vu.svg_box(100, ex_y, b1w, b1h, tt("CSV-Zeile (Beispiel)", "CSV row (example)"),
                             "QID_publikation = \u201eQ_alt\u201c", fill=NEUTRAL["fill"], stroke=NEUTRAL["stroke"]))
    parts.append(vu.svg_box(100, ex_y + 90, b1w, b1h, "QID_PUBLIKATION[\u201ePyzel 2019\u201c]",
                             "= \u201eQ139460445\u201c", fill=C["fill"], stroke=C["stroke"]))
    arrow_label = tt("weicht ab \u2192", "differs \u2192")
    parts.append(vu.svg_arrow_L(100 + b1w, ex_y + 32, 700, ex_y + 77, bend="h", marker=None,
                                 label=arrow_label, font_size=12))
    parts.append(vu.svg_arrow_L(100 + b1w, ex_y + 90 + 32, 700, ex_y + 77, bend="h", marker=None))
    parts.append(vu.svg_arrow(700, ex_y + 77, 720, ex_y + 77))
    parts.append(vu.svg_box(720, ex_y + 32, 420, 90, tt("Konflikt geloggt", "Conflict logged"),
                             "alt=Q_alt, neu=Q139460445", fill=C_WARN["fill"], stroke=C_WARN["stroke"]))
    parts.append(vu.svg_arrow(720 + 420, ex_y + 77, 1240, ex_y + 77))
    parts.append(vu.svg_box(1240, ex_y + 32, 350, 90, tt("CSV \u00fcberschrieben", "CSV overwritten"),
                             "QID_publikation = \u201eQ139460445\u201c", fill=C_OK["fill"], stroke=C_OK["stroke"]))

    coverage = tt("Literaturabdeckung nach Anreicherung: 100 % \u2014 0 Misses, 0 Konflikte offen",
                  "Literature coverage after enrichment: 100% \u2014 0 misses, 0 open conflicts")
    parts.append(f'<text x="100" y="{ex_y + 90 + b1h + 34:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(coverage)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"literature-enrichment.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_13_validation_layers.py -- four independent checks, plus a doc-drift check
====================================================================================

Source: paper section 6 and Tab. 8 (the five sections of
``validate_lod.py``), plus the SHACL-shape generation paragraph: exactly
one hard rule (every Fundstelle needs exactly one ``hatFID``, a
``sh:Violation``), every other domain/range constraint is a
``sh:Warning`` because external identifiers such as Wikidata URIs carry
no RDF type and a strict range check would produce systematic
false positives.

Bilingual (revision) -- see step_00 docstring for the convention.

Writes: validation-layers.de.svg/.png, validation-layers.en.svg/.png
Run standalone: ``python py/step_13_validation_layers.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["13-validation-layers"]
VALIDATE = vu.PIPELINE_COLORS["validate"]
LOD = vu.PIPELINE_COLORS["lod"]
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("validate_lod.py: four independent checks, plus a documentation-drift check")]

    intro = tt("validate_lod.py pr\u00fcft nach jedem Lauf f\u00fcnf voneinander unabh\u00e4ngige Fragen:",
               "After every run, validate_lod.py checks five independent questions:")
    parts.append(f'<text x="60" y="75" font-family="Fira Sans" font-size="15" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(intro)}</text>')

    headers = [tt("Sektion", "Section"), tt("Ebene", "Level"), tt("Was gepr\u00fcft wird", "What is checked")]
    col_x = [90, 260, 520]
    ty0 = 120
    for x, h in zip(col_x, headers):
        parts.append(f'<text x="{x:.1f}" y="{ty0:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="13" fill="{vu.TEXT_MUTED}">{vu.xml_escape(h)}</text>')
    parts.append(f'<line x1="90" y1="{ty0+14:.1f}" x2="1690" y2="{ty0+14:.1f}" stroke="#dedcd4" stroke-width="1"/>')

    rows = [
        ("1", tt("Strukturell", "Structural"),
         tt("SHACL-Konformit\u00e4t (Daten- und Bundle-Graph)", "SHACL conformance (data and bundle graph)")),
        ("2", tt("CSV \u2194 RDF", "CSV \u2194 RDF"),
         tt("Pro-Spalten-Tripel-Erwartungen, Audit-Spalten ausgeschlossen",
            "per-column triple expectations, audit columns excluded")),
        ("3", tt("Ontologie", "Ontology"),
         tt("genutzte vs. deklarierte Klassen und Properties", "classes and properties used vs. declared")),
        ("4", tt("CRM-Verankerung", "CRM anchoring"),
         tt("jede bb5kbc:-Klasse erreicht einen crm:E*-Vorfahren", "every bb5kbc: class reaches a crm:E* ancestor")),
        ("4b", tt("Doku-Drift", "Doc drift"),
         tt("OWL-Vorfahren \u2194 csv-mapping.md (Tab. 6)", "OWL ancestors \u2194 csv-mapping.md (Tab. 6)")),
    ]
    ry = ty0 + 60
    pitch = 78
    for sec, level, desc in rows:
        colors = VALIDATE if sec != "4b" else LOD
        badge_w = vu.text_width(sec, 14) + 32
        parts.append(f'<rect x="{col_x[0]:.1f}" y="{ry - 24:.1f}" width="{max(badge_w, 50):.1f}" height="34" rx="17" '
                     f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.8"/>')
        parts.append(f'<text x="{col_x[0] + max(badge_w, 50)/2:.1f}" y="{ry - 7:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" font-size="14" '
                     f'fill="{colors["stroke"]}">{sec}</text>')
        parts.append(f'<text x="{col_x[1]:.1f}" y="{ry - 6:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="14" fill="{vu.TEXT_DARK}">{vu.xml_escape(level)}</text>')
        parts.append(f'<text x="{col_x[2]:.1f}" y="{ry - 6:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(desc)}</text>')
        ry += pitch

    drift_note = tt("4b ist ein maschineller Abgleich gegen die Doku selbst \u2014 nicht gegen die Ontologie-Datei "
                     "ein zweites Mal, sondern gegen csv-mapping.md: schleichendes Auseinanderlaufen von Modell "
                     "und Beschreibung wird bei jedem Lauf sichtbar, nicht erst beim n\u00e4chsten Review.",
                     "4b is a machine check against the documentation itself, not the ontology file a second "
                     "time, but against csv-mapping.md: model and description silently drifting apart becomes "
                     "visible on every run, not only at the next review.")
    words = drift_note.split()
    dlines = []
    cur = []
    curlen = 0
    for w in words:
        if curlen + len(w) + 1 > 95:
            dlines.append(" ".join(cur))
            cur = []
            curlen = 0
        cur.append(w)
        curlen += len(w) + 1
    if cur:
        dlines.append(" ".join(cur))
    dy = ry + 10
    for line in dlines:
        parts.append(f'<text x="90" y="{dy:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        dy += 20

    # -- hard rule vs. warnings --------------------------------------------------
    wy = dy + 30
    parts.append(vu.svg_dashed_container(60, wy, 1630, 220,
                                          tt("SHACL-Shapes: eine harte Regel, alles andere ist Warning",
                                             "SHACL shapes: one hard rule, everything else is a warning")))
    b1x, bw, bh = 100, 640, 100
    by = wy + 60
    parts.append(vu.svg_box(b1x, by, bw, bh, tt("sh:Violation (hart)", "sh:Violation (hard)"),
                             tt("jede Fundstelle braucht genau ein hatFID", "every Fundstelle needs exactly one hatFID"),
                             fill=U_FILL, stroke=U_STROKE, stroke_width=2.0))
    parts.append(vu.svg_box(b1x + bw + 80, by, bw + 190, bh, tt("sh:Warning (alles andere)", "sh:Warning (everything else)"),
                             tt("Domain-/Range-Constraints, weil externe URIs (z. B. Wikidata) keinen RDF-Typ tragen",
                                "domain/range constraints, because external URIs (e.g. Wikidata) carry no RDF type"),
                             fill=NEUTRAL["fill"], stroke=NEUTRAL["stroke"]))
    why = tt("Ein harter Range-Check w\u00fcrde bei jedem externen Identifikator einen False Positive erzeugen.",
             "A strict range check would produce a false positive on every external identifier.")
    parts.append(f'<text x="{b1x:.1f}" y="{by + bh + 34:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(why)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"validation-layers.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_07_geo_entities.py -- geo-entities: hierarchy, dedup, five identifiers
================================================================================

Source: ``modelling-rules.md`` Regel 2 (dedup hash nodes) and Regel 5 (one
property, ``bb5kbc:hasExternalIdentifier``, for all five authorities) for
the top half; paper Tab. 5 ("Ableitung des Sicherheitsgrades der
Verortung aus genauigkeit_m") for the FSL location-certainty table,
reproduced with its real four rows rather than invented examples.

Bilingual (revision 2026-09-10c) -- see step_00 docstring for the
translation convention. The Turtle code example (data:land_3c2f8b8c ...)
is real serialised RDF and is never translated except for the German
rdfs:label literal, which is real data ("Deutschland"@de is genuinely
what the graph stores, in both language versions of this figure).

Writes: geo-entities.de.svg/.png, geo-entities.en.svg/.png
Run standalone: ``python py/step_07_geo_entities.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["07-geo-entities"]
GEO = vu.GEO
SITE = vu.SITE
ACTIVITY = vu.WORLD_COLORS["prov"]
AUTH = vu.WORLD_COLORS["authority"]
FSL = vu.WORLD_COLORS["fsl"]


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    p = lambda n: vu.prop(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)

    parts = [vu.svg_open("Geo-entities: admin hierarchy, deduplication, five external identifiers")]

    # -- top chain --------------------------------------------------------------
    cy = 155
    r = 60
    land = (190, cy)
    bundesland = (460, cy)
    kreis = (730, cy)
    gemeinde = (1000, cy)
    fx, fy, fw, fh = 1200, cy - 58, 240, 116

    parts.append(vu.svg_hash_node(*land, r, c("Land"), "land_{hash}", fill=GEO["fill"], stroke=GEO["stroke"]))
    parts.append(vu.svg_hash_node(*bundesland, r, c("Bundesland"), "bundesland_{hash}", fill=GEO["fill"], stroke=GEO["stroke"]))
    parts.append(vu.svg_hash_node(*kreis, r, c("Kreis"), "kreis_{hash}", fill=GEO["fill"], stroke=GEO["stroke"]))
    parts.append(vu.svg_hash_node(*gemeinde, r, c("Gemeinde"), "gemeinde_{hash}", fill=GEO["fill"], stroke=GEO["stroke"]))
    parts.append(vu.svg_box(fx, fy, fw, fh, c("Fundstelle"), "crm:E27_Site", fill=SITE["fill"], stroke=SITE["stroke"],
                             stroke_width=2.0))

    parts.append(vu.svg_arrow_labeled(fx, cy, gemeinde[0] + r, cy, p("inGemeinde")))
    parts.append(vu.svg_arrow_labeled(gemeinde[0] - r, cy, kreis[0] + r, cy, p("inKreis")))
    parts.append(vu.svg_arrow_labeled(kreis[0] - r, cy, bundesland[0] + r, cy, p("inBundesland")))
    parts.append(vu.svg_arrow_labeled(bundesland[0] - r, cy, land[0] + r, cy, p("inLand")))

    # -- five external identifiers, shown once as a shared key -----------------
    intro = tt("Jede der vier Ebenen kann zus\u00e4tzlich bis zu f\u00fcnf externe Identifikatoren tragen:",
               "Each of the four levels can additionally carry up to five external identifiers:")
    parts.append(f'<text x="60" y="272" font-family="Fira Sans" font-size="14.5" fill="{vu.TEXT_DARK}">'
                 f'{intro}</text>')
    badges = [("QID", "Wikidata"), ("GN", "GeoNames"), ("TGN", "Getty TGN"), ("iDAI", "iDAI.gazetteer"),
              ("OSM", tt("OSM-Relation", "OSM relation"))]
    bx = 92
    for short, full in badges:
        parts.append(vu.svg_authority_badge(bx, 325, short, r=26, fill=AUTH["fill"], stroke=AUTH["stroke"]))
        parts.append(f'<text x="{bx:.1f}" y="368" text-anchor="middle" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(full)}</text>')
        bx += 150

    # -- bottom-left: one property for all -------------------------------------
    lx, ly, lw, lh = 60, 420, 790, 490
    parts.append(vu.svg_dashed_container(lx, ly, lw, lh,
                                          tt("Eine Property f\u00fcr alle externen IDs \u2014 bb5kbc:hasExternalIdentifier",
                                             "One property for all external IDs \u2014 bb5kbc:hasExternalIdentifier")))
    code_lines = [
        ("data:land_3c2f8b8c", vu.TEXT_DARK, False),
        ("    a bb5kbc:Land ;", vu.TEXT_DARK, False),
        ("    rdfs:label \u201eDeutschland\u201c@de ;", vu.TEXT_DARK, False),
        ("    bb5kbc:hasExternalIdentifier", vu.BB5KBC_MAGENTA, True),
        ("        <...tgn/7000084> ,", vu.TEXT_MUTED, False),
        ("        <...gazetteer/2044274> ,", vu.TEXT_MUTED, False),
        ("        <...openstreetmap.org/relation/51477> ,", vu.TEXT_MUTED, False),
        ("        <...wikidata.org/entity/Q183> .", vu.TEXT_MUTED, False),
    ]
    cy2 = ly + 74
    for text, color, bold in code_lines:
        parts.append(f'<text x="{lx + 28:.1f}" y="{cy2:.1f}" font-family="Fira Sans" font-size="14" '
                     f'font-weight="{"600" if bold else "400"}" fill="{color}">{vu.xml_escape(text)}</text>')
        cy2 += 30
    parts.append(f'<line x1="{lx + 22:.1f}" y1="{cy2 + 12:.1f}" x2="{lx + lw - 22:.1f}" y2="{cy2 + 12:.1f}" '
                 f'stroke="#dedcd4" stroke-width="1"/>')
    note_lines = tt(
        ["Egal ob QID, GeoNames, TGN, iDAI oder OSM: eine einzige Property.",
         "3 Audit-Spalten (Match-Label, -Score, matchReason) bleiben CSV-only \u2014",
         "sie gehen NICHT ins RDF, nur in fst_standortanalysen_ref_report.csv."],
        ["Whichever of QID, GeoNames, TGN, iDAI or OSM: a single property.",
         "3 audit columns (match label, score, matchReason) stay CSV-only \u2014",
         "they do NOT go into the RDF, only into fst_standortanalysen_ref_report.csv."])
    ny = cy2 + 44
    for line in note_lines:
        parts.append(f'<text x="{lx + 28:.1f}" y="{ny:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        ny += 24

    # -- bottom-right: location-certainty table (paper Tab. 5) -----------------
    rx, ry_, rw, rh = 890, 420, 800, 490
    parts.append(vu.svg_dashed_container(rx, ry_, rw, rh,
                                          tt(f"{c('GeoreferenzierungsAktivitaet')} tr\u00e4gt den Sicherheitsgrad "
                                             "der Verortung",
                                             f"{c('GeoreferenzierungsAktivitaet')} carries the location's "
                                             "certainty grade")))
    rows = [
        ("genauigkeit_m = 0", "fslwb:Q23", "high", tt("direkte DB-\u00dcbernahme", "direct database take-over")),
        ("50\u2013500 m", "fslwb:Q15", "medium",
         tt(f"{c('Gemeinde')}teil-/Flur-zuordenbar", "assignable to a Flur/Gemeindeteil")),
        ("800\u20135000 m", "fslwb:Q24", "low",
         tt(f"nur {c('Gemeinde')}-Ebene (Mittelpunkt)", f"{c('Gemeinde')} level only (centroid)")),
        ("x = y = 0", "fslwb:Q113", "dubious", tt("Koordinatenfehler, kein sf:Point", "coordinate error, no sf:Point")),
    ]
    ty = ry_ + 74
    for cond, item, label, meaning in rows:
        parts.append(vu.svg_box(rx + 26, ty, 200, 64, cond, "", fill="#f1efe8", stroke=vu.LINE_NEUTRAL, rx=8))
        parts.append(vu.svg_box(rx + 246, ty, 160, 64, item, label, fill=FSL["fill"], stroke=FSL["stroke"], rx=8))
        parts.append(f'<text x="{rx + 428:.1f}" y="{ty + 34:.1f}" dominant-baseline="central" '
                     f'font-family="Fira Sans" font-size="13.5" fill="{vu.TEXT_DARK}">'
                     f'{vu.xml_escape(meaning)}</text>')
        ty += 90

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"geo-entities.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

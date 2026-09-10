#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_04_crm_crosswalk.py -- application ontology -> CIDOC CRM crosswalk
============================================================================

Source: paper section 5 ("Erweiterungsontologie"), specifically the "Drei
Vererbungsstrategien" paragraph and Tab. 6 (transitive Vorfahrenmengen).
Rather than re-drawing Abb. 2/3 of the paper verbatim, this figure makes
the paper's own three-way classification the structure of the diagram:
every bb5kbc: class is either single-, double- or triple-anchored, and
the reason differs each time (a second vocabulary contributes a genuinely
different viewpoint, not a synonym).

Writes: crm-crosswalk.svg / .png
Run standalone: ``python py/step_04_crm_crosswalk.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["04-crm-crosswalk"]
APP = vu.WORLD_COLORS["app"]
CRM = vu.WORLD_COLORS["crm"]
CRMSCI = vu.WORLD_COLORS["crmsci"]
PROV = vu.WORLD_COLORS["prov"]
TIME = vu.WORLD_COLORS["time"]
FSL = vu.WORLD_COLORS["fsl"]
LADO = vu.WORLD_COLORS["lado"]


def row(parts, x, y, w, h, title, subtitle, colors, **kw):
    parts.append(vu.svg_box(x, y, w, h, title, subtitle, fill=colors["fill"], stroke=colors["stroke"], **kw))


def build() -> list[str]:
    parts = [vu.svg_open("Application ontology to CIDOC CRM crosswalk -- three inheritance strategies")]

    # ================= Band A -- single anchor ================================
    ay, ah = 50, 150
    parts.append(vu.svg_dashed_container(60, ay, 1630, ah,
                                          "Single inheritance \u2014 exactly one CRM anchor (rdfs:subClassOf)"))
    ry = ay + 55
    row(parts, 90, ry, 430, 70, "Land \u00b7 Bundesland \u00b7 Kreis \u00b7 Gemeinde", "bb5kbc: application ontology", APP)
    parts.append(vu.svg_arrow(90 + 430, ry + 35, 610, ry + 35))
    row(parts, 610, ry, 230, 70, "crm:E53_Place", "", CRM)

    row(parts, 960, ry, 430, 70, "EntdeckungsartType \u00b7 DatierungsMethodeType", "bb5kbc: application ontology", APP)
    parts.append(vu.svg_arrow(960 + 430, ry + 35, 1480, ry + 35))
    row(parts, 1480, ry, 210, 70, "crm:E55_Type", "", CRM)

    # ================= Band B -- double anchor =================================
    by, bh = 230, 430
    parts.append(vu.svg_dashed_container(60, by, 1630, bh, "Double-anchored \u2014 two orthogonal parents"))
    pitch = 92
    top0 = by + 75
    bx1, bw1 = 90, 330
    bx2, bw2 = bx1 + bw1 + 90, 330
    bx3, bw3 = bx2 + bw2 + 90, 400
    rows = [
        ("Datierung", "site_{FID}_dating", APP, "crm:E52_Time-Span", CRM,
         "owl-time:Interval \u2014 Allen relations between phases", TIME),
        ("GeoreferenzierungsAktivitaet", "site_{FID}_activity", APP, "crm:E13_Attribute_Assignment", CRM,
         "prov:Activity \u2014 PROV visibility of the enrichment run", PROV),
        ("FundstellenartType", "shared \u00b7 hash node", APP, "crm:E55_Type", CRM,
         "fsl:SiteType/Type + lado:PlaceType \u2014 vocabulary linkage", FSL),
        ("KulturelleZuordnung", "site_{FID}_culture", APP, "crm:E92_Spacetime_Volume", CRM,
         "lado:SpaceTimeItem \u2014 assignment as a space-time volume", LADO),
    ]
    for i, (t1, s1, c1, t2, c2, t3, c3) in enumerate(rows):
        y = top0 + i * pitch
        h = 62
        row(parts, bx1, y, bw1, h, t1, s1, c1)
        row(parts, bx2, y, bw2, h, t2, "", c2)
        row(parts, bx3, y, bw3, h, t3, "", c3, rx=8)
        parts.append(vu.svg_arrow(bx1 + bw1, y + h / 2, bx2, y + h / 2))
        parts.append(vu.svg_arrow(bx2 + bw2, y + h / 2, bx3, y + h / 2))

    # ================= Band C -- triple anchor (Fundstelle) ====================
    cy, ch = 700, 250
    parts.append(vu.svg_dashed_container(60, cy, 1630, ch,
                                          "Triple-anchored \u2014 Fundstelle (three parallel views, none replaces another)"))
    fh = 80
    fx, fy, fw = 90, cy + (ch - 55 - fh) / 2 + 55, 260
    parts.append(vu.svg_box(fx, fy, fw, fh, "Fundstelle", "crm:E27_Site \u00b7 site_{FID}",
                             fill=vu.SITE["fill"], stroke=vu.SITE["stroke"], stroke_width=2.0))
    tx, tw = 420, 700
    triples = [
        ("CIDOC CRM \u2014 E18 \u2192 E26 \u2192 E27_Site \u2192 E70 \u2192 E72", CRM),
        ("FSL + PROV-O + GeoSPARQL \u2014 fsl:Location/Site, prov:Location, geo:SpatialObject", FSL),
        ("LADO + Pleiades \u2014 lado:Location, pleiades:Location", LADO),
    ]
    ty0 = cy + 60
    for i, (label, colors) in enumerate(triples):
        ty = ty0 + i * 62
        row(parts, tx, ty, tw, 46, label, "", colors, rx=8)
        parts.append(vu.svg_arrow(fx + fw, fy + fh / 2, tx, ty + 23))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "crm-crosswalk", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

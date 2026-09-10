#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_03_application_ontology.py -- the 15-class application ontology
=========================================================================

Source: ``data/raw/bb-5kbc-sites/bb5kbc-classes.mmd`` (the actual mermaid
classDiagram shipped in the ontology folder) -- every class, stereotype
and object property below is taken from that file, not re-derived from
the paper's prose. Colour-codes each class by its primary CRM/CRMsci
anchor family, reusing the same palette as the other figures so the
"world" a box belongs to stays legible across the whole set.

Class and property names are the actual bb5kbc: identifiers (German, as
in the ontology); the legend and all other text is English.

Writes: application-ontology.svg / .png
Run standalone: ``python py/step_03_application_ontology.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["03-application-ontology"]

CULTURE = {"fill": "#eef0d6", "stroke": "#6b7a1f"}
DATING = vu.WORLD_COLORS["time"]
TYPE = vu.WORLD_COLORS["authority"]
EVENT = vu.WORLD_COLORS["crmsci"]
DOC = vu.WORLD_COLORS["crm"]
ACTIVITY = vu.WORLD_COLORS["prov"]
ZUORDNUNG = vu.WORLD_COLORS["lado"]
GEO = vu.GEO
SITE = vu.SITE


def build() -> list[str]:
    parts = [vu.svg_open("bb5kbc: application ontology -- 15 classes, object properties")]

    def box(x, y, w, h, title, stereo, colors):
        return vu.svg_box(x, y, w, h, title, stereotype=stereo,
                           fill=colors["fill"], stroke=colors["stroke"])

    # -- columns --------------------------------------------------------------
    AW, AH = 220, 64
    T2W, T2H = 210, 70
    T3W, T3H = 210, 70
    T4W, T4H = 200, 70
    ADMIN_X, FUND_X, T2_X, T3_X, T4_X = 90, 400, 810, 1160, 1490
    PITCH = 150
    ROW = [50 + i * PITCH for i in range(6)]  # 50 200 350 500 650 800

    # admin hierarchy (aligned with tier-2 rows 1..4)
    land = (ADMIN_X, ROW[1])
    bundesland = (ADMIN_X, ROW[2])
    kreis = (ADMIN_X, ROW[3])
    gemeinde = (ADMIN_X, ROW[4])
    parts.append(box(*land, AW, AH, "Land", "crm:E53_Place", GEO))
    parts.append(box(*bundesland, AW, AH, "Bundesland", "crm:E53_Place", GEO))
    parts.append(box(*kreis, AW, AH, "Kreis", "crm:E53_Place", GEO))
    parts.append(box(*gemeinde, AW, AH, "Gemeinde", "crm:E53_Place", GEO))
    parts.append(vu.svg_arrow_labeled(gemeinde[0] + AW / 2, gemeinde[1], kreis[0] + AW / 2, kreis[1] + AH,
                                       "inKreis"))
    parts.append(vu.svg_arrow_labeled(kreis[0] + AW / 2, kreis[1], bundesland[0] + AW / 2, bundesland[1] + AH,
                                       "inBundesland"))
    parts.append(vu.svg_arrow_labeled(bundesland[0] + AW / 2, bundesland[1], land[0] + AW / 2, land[1] + AH,
                                       "inLand"))

    # Fundstelle, vertically centred on the admin block
    fh = 130
    fcy = (land[1] + gemeinde[1] + AH) / 2
    fx, fy, fw = FUND_X, fcy - fh / 2, 230
    parts.append(vu.svg_box(fx, fy, fw, fh, "Fundstelle", stereotype="crm:E27_Site",
                             fill=SITE["fill"], stroke=SITE["stroke"], stroke_width=2.2))
    parts.append(vu.svg_arrow_labeled(fx, fy + fh - 25, gemeinde[0] + AW, gemeinde[1] + AH / 2, "inGemeinde"))

    # tier 2 -- direct Fundstelle neighbours
    kz = (T2_X, ROW[0])
    ent = (T2_X, ROW[1])
    fat = (T2_X, ROW[2])
    geo_akt = (T2_X, ROW[3])
    pub = (T2_X, ROW[4])
    sch = (T2_X, ROW[5])
    parts.append(box(*kz, T2W, T2H, "KulturelleZuordnung", "crm:E92_Spacetime_Volume", ZUORDNUNG))
    parts.append(box(*ent, T2W, T2H, "Entdeckung", "crmsci:S19_Encounter_Event", EVENT))
    parts.append(box(*fat, T2W, T2H, "FundstellenartType", "crm:E55_Type", TYPE))
    parts.append(box(*geo_akt, T2W, T2H, "GeoreferenzierungsAktivitaet", "crm:E13_Attribute_Assignment", ACTIVITY))
    parts.append(box(*pub, T2W, T2H, "Publikation", "crm:E32_Authority_Document", DOC))
    parts.append(box(*sch, T2W, T2H, "Scherbe", "crm:E22_Human-Made_Object", DOC))

    fright, fmidy = fx + fw, fy + fh / 2
    for (bx, by), label in [
        (kz, "hatKulturelleZuordnung"), (ent, "wurdeEntdecktDurch"), (fat, "hatFundstellenart"),
        (geo_akt, "wurdeGeoreferenziertDurch"), (pub, "hatPublikation"), (sch, "hatScherbe"),
    ]:
        parts.append(vu.svg_arrow_labeled(fright, fmidy, bx, by + T2H / 2, label, font_size=11))

    # tier 3 (aligned with tier-2 rows 0..2)
    kg = (T3_X, ROW[0])
    dat = (T3_X, ROW[1])
    eat = (T3_X, ROW[2])
    parts.append(box(*kg, T3W, T3H, "Kulturgruppe", "crm:E4_Period", CULTURE))
    parts.append(box(*dat, T3W, T3H, "Datierung", "crm:E52_Time-Span", DATING))
    parts.append(box(*eat, T3W, T3H, "EntdeckungsartType", "crm:E55_Type", TYPE))
    parts.append(vu.svg_arrow_labeled(kz[0] + T2W, kz[1] + T2H / 2, kg[0], kg[1] + T3H / 2, "hatKulturgruppe",
                                       font_size=11))
    parts.append(vu.svg_arrow_labeled(kz[0] + T2W, kz[1] + T2H / 2, dat[0], dat[1] + T3H / 2, "hatDatierung",
                                       font_size=11))
    parts.append(vu.svg_arrow_labeled(ent[0] + T2W, ent[1] + T2H / 2, eat[0], eat[1] + T3H / 2, "hatEntdeckungsart",
                                       font_size=11))

    # tier 4 (aligned with tier-3 Datierung row)
    dmt = (T4_X, ROW[1])
    parts.append(box(*dmt, T4W, T4H, "DatierungsMethodeType", "crm:E55_Type", TYPE))
    parts.append(vu.svg_arrow_labeled(dat[0] + T3W, dat[1] + T3H / 2, dmt[0], dmt[1] + T4H / 2, "datierungMethode",
                                       font_size=11))

    parts.append(vu.svg_legend(60, 900, [
        ("bb5kbc: E27_Site (Fundstelle)", SITE),
        ("E53_Place (admin. hierarchy)", GEO),
        ("E92 / LADO (KulturelleZuordnung)", ZUORDNUNG),
        ("E4_Period (Kulturgruppe)", CULTURE),
        ("E52_Time-Span (Datierung)", DATING),
        ("E13 / PROV-O (Georeferenzierung)", ACTIVITY),
        ("crmsci:S19 (Entdeckung)", EVENT),
        ("E32 / E22 (Publikation, Scherbe)", DOC),
        ("E55_Type (\u00d7 3)", TYPE),
    ], columns=5, col_w=330, row_h=22))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "application-ontology", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

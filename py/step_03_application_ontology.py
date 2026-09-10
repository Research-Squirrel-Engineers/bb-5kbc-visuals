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

Bilingual (revision 2026-09-10c): class and property names are the real
bb5kbc: identifiers in the German figure, translated via ``vu.cls()`` /
``vu.prop()`` in the English one -- see step_00 docstring / utils for the
convention. CRM/CRMsci stereotype strings (crm:E27_Site, ...) are never
translated, they are the standard's own vocabulary.

Writes: application-ontology.de.svg/.png, application-ontology.en.svg/.png
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


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    p = lambda n: vu.prop(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)

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
    parts.append(box(*land, AW, AH, c("Land"), "crm:E53_Place", GEO))
    parts.append(box(*bundesland, AW, AH, c("Bundesland"), "crm:E53_Place", GEO))
    parts.append(box(*kreis, AW, AH, c("Kreis"), "crm:E53_Place", GEO))
    parts.append(box(*gemeinde, AW, AH, c("Gemeinde"), "crm:E53_Place", GEO))
    parts.append(vu.svg_arrow_labeled(gemeinde[0] + AW / 2, gemeinde[1], kreis[0] + AW / 2, kreis[1] + AH,
                                       p("inKreis")))
    parts.append(vu.svg_arrow_labeled(kreis[0] + AW / 2, kreis[1], bundesland[0] + AW / 2, bundesland[1] + AH,
                                       p("inBundesland")))
    parts.append(vu.svg_arrow_labeled(bundesland[0] + AW / 2, bundesland[1], land[0] + AW / 2, land[1] + AH,
                                       p("inLand")))

    # Fundstelle, vertically centred on the admin block
    fh = 130
    fcy = (land[1] + gemeinde[1] + AH) / 2
    fx, fy, fw = FUND_X, fcy - fh / 2, 230
    parts.append(vu.svg_box(fx, fy, fw, fh, c("Fundstelle"), stereotype="crm:E27_Site",
                             fill=SITE["fill"], stroke=SITE["stroke"], stroke_width=2.2))
    parts.append(vu.svg_arrow_labeled(fx, fy + fh - 25, gemeinde[0] + AW, gemeinde[1] + AH / 2, p("inGemeinde")))

    # tier 2 -- direct Fundstelle neighbours
    kz = (T2_X, ROW[0])
    ent = (T2_X, ROW[1])
    fat = (T2_X, ROW[2])
    geo_akt = (T2_X, ROW[3])
    pub = (T2_X, ROW[4])
    sch = (T2_X, ROW[5])
    parts.append(box(*kz, T2W, T2H, c("KulturelleZuordnung"), "crm:E92_Spacetime_Volume", ZUORDNUNG))
    parts.append(box(*ent, T2W, T2H, c("Entdeckung"), "crmsci:S19_Encounter_Event", EVENT))
    parts.append(box(*fat, T2W, T2H, c("FundstellenartType"), "crm:E55_Type", TYPE))
    parts.append(box(*geo_akt, T2W, T2H, c("GeoreferenzierungsAktivitaet"), "crm:E13_Attribute_Assignment", ACTIVITY))
    parts.append(box(*pub, T2W, T2H, c("Publikation"), "crm:E32_Authority_Document", DOC))
    parts.append(box(*sch, T2W, T2H, c("Scherbe"), "crm:E22_Human-Made_Object", DOC))

    fright, fmidy = fx + fw, fy + fh / 2
    for (bx, by), label in [
        (kz, p("hatKulturelleZuordnung")), (ent, p("wurdeEntdecktDurch")), (fat, p("hatFundstellenart")),
        (geo_akt, p("wurdeGeoreferenziertDurch")), (pub, p("hatPublikation")), (sch, p("hatScherbe")),
    ]:
        parts.append(vu.svg_arrow_labeled(fright, fmidy, bx, by + T2H / 2, label, font_size=11))

    # tier 3 (aligned with tier-2 rows 0..2)
    kg = (T3_X, ROW[0])
    dat = (T3_X, ROW[1])
    eat = (T3_X, ROW[2])
    parts.append(box(*kg, T3W, T3H, c("Kulturgruppe"), "crm:E4_Period", CULTURE))
    parts.append(box(*dat, T3W, T3H, c("Datierung"), "crm:E52_Time-Span", DATING))
    parts.append(box(*eat, T3W, T3H, c("EntdeckungsartType"), "crm:E55_Type", TYPE))
    parts.append(vu.svg_arrow_labeled(kz[0] + T2W, kz[1] + T2H / 2, kg[0], kg[1] + T3H / 2, p("hatKulturgruppe"),
                                       font_size=11))
    parts.append(vu.svg_arrow_labeled(kz[0] + T2W, kz[1] + T2H / 2, dat[0], dat[1] + T3H / 2, p("hatDatierung"),
                                       font_size=11))
    parts.append(vu.svg_arrow_labeled(ent[0] + T2W, ent[1] + T2H / 2, eat[0], eat[1] + T3H / 2,
                                       p("hatEntdeckungsart"), font_size=11))

    # tier 4 (aligned with tier-3 Datierung row)
    dmt = (T4_X, ROW[1])
    parts.append(box(*dmt, T4W, T4H, c("DatierungsMethodeType"), "crm:E55_Type", TYPE))
    parts.append(vu.svg_arrow_labeled(dat[0] + T3W, dat[1] + T3H / 2, dmt[0], dmt[1] + T4H / 2,
                                       p("datierungMethode"), font_size=11))

    parts.append(vu.svg_legend(60, 900, [
        (f"bb5kbc: E27_Site ({c('Fundstelle')})", SITE),
        (f"E53_Place ({tt('Verwaltungshierarchie', 'admin. hierarchy')})", GEO),
        (f"E92 / LADO ({c('KulturelleZuordnung')})", ZUORDNUNG),
        (f"E4_Period ({c('Kulturgruppe')})", CULTURE),
        (f"E52_Time-Span ({c('Datierung')})", DATING),
        (f"E13 / PROV-O ({c('GeoreferenzierungsAktivitaet')})", ACTIVITY),
        (f"crmsci:S19 ({c('Entdeckung')})", EVENT),
        (f"E32 / E22 ({c('Publikation')}, {c('Scherbe')})", DOC),
        (tt("E55_Type (\u00d7 3)", "E55_Type (\u00d7 3)"), TYPE),
    ], columns=5, col_w=330, row_h=22))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"application-ontology.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

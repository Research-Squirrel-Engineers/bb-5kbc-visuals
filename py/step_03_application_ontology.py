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

**Revision 2026-09-15:** every Fundstelle-to-tier-2 connection, plus
inGemeinde/hatDatierung/hatEntdeckungsart, used to be a diagonal; now
orthogonal (house rule, PRIMER.md A3).

**Revision 2026-09-15b (Florian flagged this figure specifically as
still tangled after the first pass):** two problems the first pass
missed. (1) The six Fundstelle spokes' rails weren't ordered by how far
each one travels, so short-hop connectors (fat, geo_akt) crossed the
rails of long-hop ones (kz, ent, pub, sch) even though none of them
crossed an actual box -- reassigned so the rail order matches travel
distance (kz/sch, which each skip two boxes, get the outer rail; ent/pub,
which each skip one, get the inner rail; fat/geo_akt skip none and go
direct) and the fan-out is now provably crossing-free (see the inline
comment for the reasoning). (2) hatDatierung/hatEntdeckungsart entered
Datierung/EntdeckungsartType from the side at a height that happens to
coincide with Entdeckung's own row -- reading, misleadingly, as if the
line came out of Entdeckung rather than KulturelleZuordnung. Both now
enter their target from above instead, which sidesteps the coincidence
entirely.

**Revision 2026-09-15d:** inGemeinde turned immediately at Fundstelle's
own left edge with no visible lead-out (unlike the fan-out spokes,
which all clear Fundstelle's edge with their own rail first); now
routed via ``svg_arrow_elbow_v`` with a short stub for the same
"visibly clears the box before turning" look as the rest of the figure
(PRIMER.md S37).

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
    parts.append(vu.svg_arrow_elbow_v(fx, fy + fh - 25, gemeinde[0] + AW, gemeinde[1] + AH / 2, fx - 30,
                                       label=p("inGemeinde"), font_size=11))

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

    fright = fx + fw
    # Six spokes fan out from Fundstelle to six stacked tier-2 boxes, all
    # entered on their left edge -- every spoke therefore needs a
    # *horizontal* final approach (svg_arrow_elbow_v, not a direct
    # svg_arrow_L "bend=h", which would end on a vertical approach and
    # visibly enter from above/below instead of from the side; that
    # mismatch was the second bug Florian flagged after S35).
    #
    # Six rails, reused in two groups of three (kz/ent/fat above
    # Fundstelle's height, geo_akt/pub/sch below) since the two groups'
    # y-ranges never overlap. Within each group of three, the rail
    # closest to Fundstelle goes to whichever spoke travels *farthest*
    # (kz, sch), and the rail closest to the tier-2 column goes to
    # whichever travels *least* (fat, geo_akt) -- verified pairwise
    # (every "does this spoke's approach segment cross that spoke's
    # rail segment" check) so none of the six cross each other.
    rail_near, rail_mid, rail_far = 645, 665, 685
    exit_ys = [fy + fh * (i + 0.5) / 6 for i in range(6)]
    spokes = [
        (kz, p("hatKulturelleZuordnung"), rail_near),
        (ent, p("wurdeEntdecktDurch"), rail_mid),
        (fat, p("hatFundstellenart"), rail_far),
        (geo_akt, p("wurdeGeoreferenziertDurch"), rail_far),
        (pub, p("hatPublikation"), rail_mid),
        (sch, p("hatScherbe"), rail_near),
    ]
    for i, ((bx, by), label, rail_x) in enumerate(spokes):
        parts.append(vu.svg_arrow_elbow_v(fright, exit_ys[i], bx, by + T2H / 2, rail_x,
                                           label=label, font_size=10.5))

    # tier 3 (aligned with tier-2 rows 0..2)
    kg = (T3_X, ROW[0])
    dat = (T3_X, ROW[1])
    eat = (T3_X, ROW[2])
    parts.append(box(*kg, T3W, T3H, c("Kulturgruppe"), "crm:E4_Period", CULTURE))
    parts.append(box(*dat, T3W, T3H, c("Datierung"), "crm:E52_Time-Span", DATING))
    parts.append(box(*eat, T3W, T3H, c("EntdeckungsartType"), "crm:E55_Type", TYPE))
    parts.append(vu.svg_arrow_labeled(kz[0] + T2W, kz[1] + T2H / 2, kg[0], kg[1] + T3H / 2, p("hatKulturgruppe"),
                                       font_size=11))
    # kz->dat and ent->eat both skip one row in the same crowded column
    # (a direct side-entry would also coincidentally land at the same
    # height as Entdeckung's own row, reading as if the line came out of
    # that box instead of KulturelleZuordnung -- see PRIMER.md S35) --
    # routed instead to enter dat/eat from above, via a rail in the gap
    # between tier-2 and tier-3 rows.
    kz_bottom = (kz[0] + T2W / 2, kz[1] + T2H)
    dat_top = (dat[0] + T3W / 2, dat[1])
    parts.append(vu.svg_arrow_elbow(kz_bottom[0], kz_bottom[1], dat_top[0], dat_top[1], 160,
                                     label=p("hatDatierung"), font_size=10.5))
    ent_bottom = (ent[0] + T2W / 2, ent[1] + T2H)
    eat_top = (eat[0] + T3W / 2, eat[1])
    parts.append(vu.svg_arrow_elbow(ent_bottom[0], ent_bottom[1], eat_top[0], eat_top[1], 310,
                                     label=p("hatEntdeckungsart"), font_size=10.5))

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

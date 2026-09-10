#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_00_fundstelle_hub.py -- the mental model on one diagram
=================================================================

Source: ``data/raw/bb-5kbc-sites/modelling-rules.md``, section "Das
Mentalmodell auf einer Seite" (the ASCII diagram) and "Sechs
Modellierungsregeln" (which nodes are shared/deduplicated vs. per-site).

A good opening or closing figure: the Fundstelle sits at the centre, seven
relationship spokes radiate out, and the visual language introduced here
(double-ring circle = shared/deduplicated concept node, plain box = node
that exists once per Fundstelle/FID) is reused throughout the rest of the
set (07-geo-entities, 08-dating-entities, 09-kulturen).

Bilingual (revision 2026-09-10c): built once per language. In the German
figure, class/property names are the real bb5kbc: identifiers (Fundstelle,
Gemeinde, hatKulturelleZuordnung, ...), unchanged. In the English figure
they are translated via ``vu.cls()``/``vu.prop()`` -- see the glossary and
its rationale in ``bb5kbc_visuals_utils.py``. CSV data values (Siedlung,
Grab) are never translated.

Writes: fundstelle-hub.de.svg/.png, fundstelle-hub.en.svg/.png
Run standalone: ``python py/step_00_fundstelle_hub.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["00-fundstelle-hub"]

CULTURE = {"fill": "#eef0d6", "stroke": "#6b7a1f"}
DATING = vu.WORLD_COLORS["time"]
TYPE = vu.WORLD_COLORS["authority"]
EVENT = vu.WORLD_COLORS["crmsci"]
DOC = vu.WORLD_COLORS["crm"]
ACTIVITY = vu.WORLD_COLORS["prov"]
ZUORDNUNG = vu.WORLD_COLORS["lado"]


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    p = lambda n: vu.prop(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)
    shared = tt("geteilt", "shared")
    per_site = tt("pro Fundstelle", "per site")

    parts = [vu.svg_open("Fundstelle as the hub -- the bb5kbc mental model on one diagram")]

    # -- Fundstelle, centred ------------------------------------------------
    fw, fh = 280, 110
    fcx, fcy = 875, 500
    fx, fy = fcx - fw / 2, fcy - fh / 2
    parts.append(vu.svg_box(fx, fy, fw, fh, c("Fundstelle"), f"crm:E27_Site \u00b7 site_{{FID}}",
                             fill=vu.SITE["fill"], stroke=vu.SITE["stroke"], stroke_width=2.2))

    # -- admin hierarchy: Gemeinde -> Kreis -> Bundesland -> Land ------------
    gy = 145
    gemeinde = (fcx, gy)
    kreis = (fcx - 220, gy)
    bundesland = (fcx - 440, gy)
    land = (fcx - 660, gy)
    r = 58
    for (cx, cy), label, sub in [
        (gemeinde, c("Gemeinde"), f"{shared} \u00b7 gemeinde_{{hash}}"),
        (kreis, c("Kreis"), f"{shared} \u00b7 kreis_{{hash}}"),
        (bundesland, c("Bundesland"), f"{shared} \u00b7 bundesland_{{hash}}"),
        (land, c("Land"), f"{shared} \u00b7 land_{{hash}}"),
    ]:
        parts.append(vu.svg_hash_node(cx, cy, r, label, sub, fill=vu.GEO["fill"], stroke=vu.GEO["stroke"]))
    parts.append(vu.svg_arrow_labeled(gemeinde[0] - r, gemeinde[1], kreis[0] + r, kreis[1], p("inKreis")))
    parts.append(vu.svg_arrow_labeled(kreis[0] - r, kreis[1], bundesland[0] + r, bundesland[1], p("inBundesland")))
    parts.append(vu.svg_arrow_labeled(bundesland[0] - r, bundesland[1], land[0] + r, land[1], p("inLand")))
    parts.append(vu.svg_arrow_labeled(fcx, fy, gemeinde[0], gemeinde[1] + r, p("inGemeinde"), above=False))

    # -- KulturelleZuordnung -> Kulturgruppe (shared) + Datierung (per site) -
    kz_x, kz_y, kz_w, kz_h = 265, 465, 235, 84
    kz_cx, kz_cy = kz_x + kz_w / 2, kz_y + kz_h / 2
    parts.append(vu.svg_box(kz_x, kz_y, kz_w, kz_h, c("KulturelleZuordnung"), f"{per_site} \u00b7 crm:E92",
                             fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx, fcy - 8, kz_x + kz_w, kz_cy - 8, p("hatKulturelleZuordnung")))

    kg_cx, kg_cy, kg_r = 135, 285, 68
    parts.append(vu.svg_hash_node(kg_cx, kg_cy, kg_r, c("Kulturgruppe"), f"{shared} \u00b7 kultur_{{hash}}",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))
    parts.append(vu.svg_arrow_labeled(kz_x + 15, kz_y, kg_cx + 10, kg_cy + kg_r, p("hatKulturgruppe"), above=False))

    dat_x, dat_y, dat_w, dat_h = 85, 700, 220, 90
    parts.append(vu.svg_box(dat_x, dat_y, dat_w, dat_h, c("Datierung"), f"{per_site} \u00b7 crm:E52 + time:Interval",
                             fill=DATING["fill"], stroke=DATING["stroke"]))
    parts.append(vu.svg_arrow_labeled(kz_x + 15, kz_y + kz_h, dat_x + dat_w - 20, dat_y, p("hatDatierung")))

    # -- Fundstellenart (shared) ---------------------------------------------
    fa_cx, fa_cy, fa_r = 1500, 210, 78
    parts.append(vu.svg_hash_node(fa_cx, fa_cy, fa_r, c("FundstellenartType"),
                                   f"{shared} \u00b7 {tt('z. B. Siedlung, Grab', 'e.g. Siedlung, Grab')}",
                                   fill=TYPE["fill"], stroke=TYPE["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx + fw, fy + 15, fa_cx - fa_r * 0.8, fa_cy + fa_r * 0.7,
                                       p("hatFundstellenart")))

    # -- Entdeckung (shared, incl. Entdeckungsart as subtitle) --------------
    ed_cx, ed_cy, ed_r = 1620, fcy, 80
    parts.append(vu.svg_hash_node(ed_cx, ed_cy, ed_r, c("Entdeckung"),
                                   f"{shared} \u00b7 {tt('inkl. Entdeckungsart', 'incl. discovery type')}",
                                   fill=EVENT["fill"], stroke=EVENT["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx + fw, fcy, ed_cx - ed_r, ed_cy, p("wurdeEntdecktDurch")))

    # -- Publikation (shared) -------------------------------------------------
    pub_cx, pub_cy, pub_r = 1500, 800, 72
    parts.append(vu.svg_hash_node(pub_cx, pub_cy, pub_r, c("Publikation"), f"{shared} \u00b7 pub_{{hash}}",
                                   fill=DOC["fill"], stroke=DOC["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx + fw - 10, fy + fh, pub_cx - pub_r * 0.7, pub_cy - pub_r * 0.7,
                                       p("hatPublikation"), above=False))

    # -- Scherbe (1..n, shared per QID) --------------------------------------
    sh_cx, sh_cy, sh_r = 1140, 850, 66
    parts.append(vu.svg_hash_node(sh_cx, sh_cy, sh_r, c("Scherbe"),
                                   tt("1..n \u00b7 geteilt pro QID", "1..n \u00b7 shared per QID"),
                                   fill=DOC["fill"], stroke=DOC["stroke"]))
    parts.append(vu.svg_arrow_labeled(fcx + 20, fy + fh, sh_cx, sh_cy - sh_r, p("hatScherbe"), above=False))

    # -- Georeferenzierung + Punkt (per site) --------------------------------
    geo_x, geo_y, geo_w, geo_h = 470, 800, 290, 100
    parts.append(vu.svg_box(geo_x, geo_y, geo_w, geo_h, c("GeoreferenzierungsAktivitaet"),
                             tt(f"{per_site} \u00b7 Punkt (WGS84) + Aktivit\u00e4t",
                                f"{per_site} \u00b7 point (WGS84) + activity"),
                             fill=ACTIVITY["fill"], stroke=ACTIVITY["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx + 20, fy + fh, geo_x + geo_w - 30, geo_y,
                                       p("wurdeGeoreferenziertDurch"), above=False))

    # -- legend ---------------------------------------------------------------
    parts.append(vu.svg_legend(60, 924, [
        (tt("Doppelring = geteilter Konzeptknoten, dedupliziert",
            "double ring = shared concept node, deduplicated"), vu.GEO),
        (tt("Kasten = eigener Knoten pro Fundstelle (FID-basiert)",
            f"box = own node per {c('Fundstelle')} (FID-based)"), vu.SITE),
    ], columns=2, col_w=760))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"fundstelle-hub.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

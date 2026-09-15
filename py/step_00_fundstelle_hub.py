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

**Revision 2026-09-15 (house rule: no diagonal lines):** every connector
here used to be a straight diagonal from the Fundstelle box to whichever
angle its target happened to sit at. Redrawn with orthogonal-only
connectors (``vu.svg_arrow_L`` / straight ``vu.svg_arrow_labeled`` where
source and target already share an axis) -- see PRIMER.md A3 for the
house rule and S32 for this pass. A few satellite positions were nudged
so more connections land on a shared axis outright (e.g. KulturelleZuordnung
now sits at the same mid-height as Fundstelle, so that spoke is a single
straight horizontal line, not a corner).

Bilingual (revision 2026-09-10c): built once per language. In the German
figure, class/property names are the real bb5kbc: identifiers (Fundstelle,
Gemeinde, hatKulturelleZuordnung, ...), unchanged. In the English figure
they are translated via ``vu.cls()``/``vu.prop()`` -- see the glossary and
its rationale in ``bb5kbc_visuals_utils.py``. CSV data values (Siedlung,
Grab) are never translated.

**Revision 2026-09-15c:** hasDating, hasSherd and wasGeoreferencedBy used
to turn immediately at their source box's edge with no visible "lead-out"
before the corner (unlike the fan-out spokes elsewhere in this figure,
which all visibly clear their source box first); now routed via
``svg_arrow_elbow`` so each one has a short stub before it turns,
matching that same visual language (PRIMER.md S37).

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

    parts = [vu.svg_open("Fundstelle as the hub -- the bb5kbc mental model, orthogonal connectors only")]

    # -- Fundstelle, centred ------------------------------------------------
    fw, fh = 280, 110
    fcx, fcy = 875, 500
    fx, fy = fcx - fw / 2, fcy - fh / 2
    parts.append(vu.svg_box(fx, fy, fw, fh, c("Fundstelle"), f"crm:E27_Site \u00b7 site_{{FID}}",
                             fill=vu.SITE["fill"], stroke=vu.SITE["stroke"], stroke_width=2.2))

    # -- admin hierarchy: Gemeinde -> Kreis -> Bundesland -> Land ------------
    # already on Fundstelle's own x, so this spoke and the whole chain are
    # straight lines with no corner needed.
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
    # nudged to Fundstelle's own mid-height so this spoke is one straight line
    kz_w, kz_h = 235, 84
    kz_x = 265
    kz_cy = fcy
    kz_y = kz_cy - kz_h / 2
    parts.append(vu.svg_box(kz_x, kz_y, kz_w, kz_h, c("KulturelleZuordnung"), f"{per_site} \u00b7 crm:E92",
                             fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx, fcy, kz_x + kz_w, kz_cy, p("hatKulturelleZuordnung")))

    kg_cx, kg_cy, kg_r = 135, 260, 68
    parts.append(vu.svg_hash_node(kg_cx, kg_cy, kg_r, c("Kulturgruppe"), f"{shared} \u00b7 kultur_{{hash}}",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))
    parts.append(vu.svg_arrow_L(kz_x, kz_cy - 20, kg_cx, kg_cy + kg_r, bend="h",
                                 label=p("hatKulturgruppe"), font_size=11))

    dat_x, dat_y, dat_w, dat_h = 85, 760, 220, 90
    dat_cx = dat_x + dat_w / 2
    parts.append(vu.svg_box(dat_x, dat_y, dat_w, dat_h, c("Datierung"), f"{per_site} \u00b7 crm:E52 + time:Interval",
                             fill=DATING["fill"], stroke=DATING["stroke"]))
    parts.append(vu.svg_arrow_elbow(kz_x + 60, kz_cy + kz_h / 2, dat_cx, dat_y, kz_cy + kz_h / 2 + 25,
                                     label=p("hatDatierung"), font_size=11))

    # -- Fundstellenart (shared) ---------------------------------------------
    fa_cx, fa_cy, fa_r = 1500, 190, 78
    parts.append(vu.svg_hash_node(fa_cx, fa_cy, fa_r, c("FundstellenartType"),
                                   f"{shared} \u00b7 {tt('z. B. Siedlung, Grab', 'e.g. Siedlung, Grab')}",
                                   fill=TYPE["fill"], stroke=TYPE["stroke"]))
    parts.append(vu.svg_arrow_L(fx + fw, fy + 20, fa_cx, fa_cy + fa_r, bend="h",
                                 label=p("hatFundstellenart"), font_size=11))

    # -- Entdeckung (shared, incl. Entdeckungsart as subtitle) --------------
    # same y as Fundstelle's centre, so this spoke is one straight line
    ed_cx, ed_cy, ed_r = 1620, fcy, 80
    parts.append(vu.svg_hash_node(ed_cx, ed_cy, ed_r, c("Entdeckung"),
                                   f"{shared} \u00b7 {tt('inkl. Entdeckungsart', 'incl. discovery type')}",
                                   fill=EVENT["fill"], stroke=EVENT["stroke"]))
    parts.append(vu.svg_arrow_labeled(fx + fw, fcy, ed_cx - ed_r, ed_cy, p("wurdeEntdecktDurch")))

    # -- Publikation (shared) -------------------------------------------------
    pub_cx, pub_cy, pub_r = 1500, 830, 72
    parts.append(vu.svg_hash_node(pub_cx, pub_cy, pub_r, c("Publikation"), f"{shared} \u00b7 pub_{{hash}}",
                                   fill=DOC["fill"], stroke=DOC["stroke"]))
    parts.append(vu.svg_arrow_L(fx + fw, fy + fh - 20, pub_cx, pub_cy - pub_r, bend="h",
                                 label=p("hatPublikation"), font_size=11))

    # -- Scherbe (1..n, shared per QID) --------------------------------------
    sh_cx, sh_cy, sh_r = 1140, 870, 66
    parts.append(vu.svg_hash_node(sh_cx, sh_cy, sh_r, c("Scherbe"),
                                   tt("1..n \u00b7 geteilt pro QID", "1..n \u00b7 shared per QID"),
                                   fill=DOC["fill"], stroke=DOC["stroke"]))
    parts.append(vu.svg_arrow_elbow(fcx + 60, fy + fh, sh_cx, sh_cy - sh_r, fy + fh + 25,
                                     label=p("hatScherbe"), font_size=11))

    # -- Georeferenzierung + Punkt (per site) --------------------------------
    geo_x, geo_y, geo_w, geo_h = 470, 820, 290, 100
    geo_cx = geo_x + geo_w / 2
    parts.append(vu.svg_box(geo_x, geo_y, geo_w, geo_h, c("GeoreferenzierungsAktivitaet"),
                             tt(f"{per_site} \u00b7 Punkt (WGS84) + Aktivit\u00e4t",
                                f"{per_site} \u00b7 point (WGS84) + activity"),
                             fill=ACTIVITY["fill"], stroke=ACTIVITY["stroke"]))
    parts.append(vu.svg_arrow_elbow(fx + 40, fy + fh, geo_cx, geo_y, fy + fh + 25,
                                     label=p("wurdeGeoreferenziertDurch"), font_size=11))

    # -- legend ---------------------------------------------------------------
    parts.append(vu.svg_legend(60, 950, [
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

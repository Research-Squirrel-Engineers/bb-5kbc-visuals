#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_05_uncertainty_markers.py -- the "?" marker, two different anchors
============================================================================

Source: ``data/raw/bb-5kbc-sites/modelling-rules.md``, Regel 3
"Sonderfall Unsicherheit" -- the anchor point for ``fsl:certaintyDesc
"uncertain"@en`` deliberately depends on the domain: at the
KulturelleZuordnung link node for a culture guess ("SBK?"), but directly
on the Type node itself for a site-type guess ("Grab?"), because there is
no link node between Fundstelle and FundstellenartType to hang it on.
Both variants still resolve to the *same* Wikidata QID as the certain
value, so QID-based queries find them and label-based queries keep them
apart (paper's own worked example, reused here almost verbatim).

Bilingual (revision 2026-09-10c) -- see step_00 docstring for the
translation convention. "SBK"/"SBK?"/"Grab"/"Grab?" are real CSV/culture
values and are never translated in either language.

**Revision 2026-09-11 (correction):** the example FIDs (site_12/57 for
SBK/SBK?, site_3/88/144 for Grab/Grab?) were placeholders that happened
to be real rows but did not actually carry those values -- FID 144, for
instance, is real but is "Grab" (certain), not "Grab?". Replaced with
FIDs verified against ``fst_wgs84_lit_enriched.csv`` 2026-09-11: FID 1
("Tuengeda", kultur=SBK) and FID 81 ("Gartz ?", kultur=SBK?) on the left;
FID 98 and FID 107 (both fundstellenart=Grab) and FID 54 (Grab?) on the
right.

**Revision 2026-09-15f:** the right panel's wd-badge x-position (``qx2``)
was computed from the Grab circle's own radius alone, on the assumption
that both sources feeding the badge were the same size (true on the
left panel, where SBK and SBK? are both circles of radius KG_R). On the
right, Grab? is a wide box (230px) that extends well past Grab circle's
own right edge, so that assumption put the shared turn point *inside*
Grab?'s own span -- its connector had to double back leftward before
heading toward the badge, instead of cleanly leaving the box to the
right first (Florian: "die linien zu wikidata passen nicht"). Fixed by
basing the turn point on whichever of the two sources' right edges is
actually farther right.

Writes: uncertainty-markers.de.svg/.png, uncertainty-markers.en.svg/.png
Run standalone: ``python py/step_05_uncertainty_markers.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["05-uncertainty-markers"]
CULTURE = {"fill": "#eef0d6", "stroke": "#6b7a1f"}
ZUORDNUNG = vu.WORLD_COLORS["lado"]
TYPE = vu.WORLD_COLORS["authority"]
SITE = vu.SITE
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE

FW, FH = 160, 64
KZW, KZH = 210, 64
KG_R = 58
BADGE_R = 26
ROW1_CY, ROW2_CY = 215, 740


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)
    same_qid_for = tt("dieselbe QID f\u00fcr", "same QID for")
    sbk_label = tt("\u201eSBK\u201c und \u201eSBK?\u201c", "\u201eSBK\u201c and \u201eSBK?\u201c")
    grab_label = tt("\u201eGrab\u201c und \u201eGrab?\u201c", "\u201eGrab\u201c and \u201eGrab?\u201c")

    parts = [vu.svg_open("The '?' marker: certaintyDesc anchors differently for culture vs. site type")]

    # ============ LEFT: Kulturgruppe -- anchored at KulturelleZuordnung =======
    lx, ly, lw, lh = 60, 50, 800, 850
    parts.append(vu.svg_dashed_container(lx, ly, lw, lh,
                                          tt(f"{c('Kulturgruppe')} (SBK?, SRK?) \u2014 Unsicherheit an der "
                                             f"{c('KulturelleZuordnung')} verankert",
                                             f"{c('Kulturgruppe')} (SBK?, SRK?) \u2014 uncertainty anchored at "
                                             f"{c('KulturelleZuordnung')}")))

    fx = lx + 45
    kzx = fx + FW + 55
    kgcx = kzx + KZW + 70 + KG_R
    qx = kgcx + KG_R + 55 + BADGE_R

    # certain row -- FID 1 (Tuengeda), real kultur=SBK (see step_08)
    f1y, kz1y = ROW1_CY - FH / 2, ROW1_CY - KZH / 2
    parts.append(vu.svg_box(fx, f1y, FW, FH, f"{c('Fundstelle')} A", "site_1", fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx + FW, ROW1_CY, kzx, ROW1_CY))
    parts.append(vu.svg_box(kzx, kz1y, KZW, KZH, c("KulturelleZuordnung"), "site_1_culture",
                             fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
    parts.append(vu.svg_arrow(kzx + KZW, ROW1_CY, kgcx - KG_R, ROW1_CY))
    parts.append(vu.svg_hash_node(kgcx, ROW1_CY, KG_R, "\u201eSBK\u201c", "kultur_a36e9d6d",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))

    # uncertain row -- FID 81 ("Gartz ?"), real kultur=SBK?
    f2y, kz2y = ROW2_CY - FH / 2, ROW2_CY - KZH / 2
    parts.append(vu.svg_box(fx, f2y, FW, FH, f"{c('Fundstelle')} B", "site_81", fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx + FW, ROW2_CY, kzx, ROW2_CY))
    parts.append(vu.svg_box(kzx, kz2y, KZW, KZH, c("KulturelleZuordnung"), "site_81_culture",
                             fill=U_FILL, stroke=U_STROKE, dashed=True))
    parts.append(f'<text x="{kzx:.1f}" y="{kz2y + KZH + 24:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{U_STROKE}">+ certaintyDesc \u201euncertain\u201c@en</text>')
    parts.append(vu.svg_arrow(kzx + KZW, ROW2_CY, kgcx - KG_R, ROW2_CY))
    parts.append(vu.svg_hash_node(kgcx, ROW2_CY, KG_R, "\u201eSBK?\u201c", "kultur_7a001224",
                                   fill=CULTURE["fill"], stroke=U_STROKE))

    # shared QID badge both rows converge on -- both legs travel right,
    # then bend to meet the badge (bracket shape, no diagonal). The two
    # legs stop short of the badge with no arrowhead of their own (two
    # markers meeting at one point draw as a colliding "X"); one final
    # short hop carries the single arrowhead into the badge.
    qy = (ROW1_CY + ROW2_CY) / 2
    parts.append(vu.svg_arrow_L(kgcx + KG_R, ROW1_CY, qx - BADGE_R - 20, qy, bend="h", marker=None))
    parts.append(vu.svg_arrow_L(kgcx + KG_R, ROW2_CY, qx - BADGE_R - 20, qy, bend="h", marker=None))
    parts.append(vu.svg_arrow(qx - BADGE_R - 20, qy, qx - BADGE_R, qy))
    parts.append(vu.svg_authority_badge(qx, qy, "wd", r=BADGE_R, fill=vu.WORLD_COLORS["authority"]["fill"],
                                         stroke=vu.WORLD_COLORS["authority"]["stroke"]))
    parts.append(f'<text x="{qx:.1f}" y="{qy + 54:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{same_qid_for}</text>')
    parts.append(f'<text x="{qx:.1f}" y="{qy + 70:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{sbk_label}</text>')

    # ============ RIGHT: Fundstellenart -- anchored at the Type node ===========
    rx, ry_, rw, rh = 890, 50, 800, 850
    parts.append(vu.svg_dashed_container(rx, ry_, rw, rh,
                                          tt(f"{c('FundstellenartType')} (Grab?) \u2014 kein Verkn\u00fcpfungsknoten \u2192 "
                                             "Unsicherheit direkt am Typ verankert",
                                             f"{c('FundstellenartType')} (Grab?) \u2014 no link node \u2192 "
                                             "uncertainty anchored directly on the type")))

    fx2 = rx + 45
    tcx2 = fx2 + FW + 100 + KG_R
    tx2u = fx2 + FW + 100
    tuw, tuh = 230, 76
    # qx2 (and therefore the wd badge's x) must clear whichever of the
    # two sources extends farther right -- Grab? is a wide box (tuw=230)
    # whose right edge sits well past Grab circle's own edge, so basing
    # this on the circle alone (as a first version did) left the Grab?
    # line's turn point *inside* the box's own span: it had to double
    # back leftward before heading up to the badge instead of cleanly
    # leaving the box to the right first.
    right_edge = max(tcx2 + KG_R, tx2u + tuw)
    qx2 = right_edge + 70 + BADGE_R

    parts.append(vu.svg_box(fx2, ROW1_CY - 40 - FH / 2, FW, FH, f"{c('Fundstelle')} X", "site_98",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_box(fx2, ROW1_CY + 40 - FH / 2, FW, FH, f"{c('Fundstelle')} Y", "site_107",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow_L(fx2 + FW, ROW1_CY - 40, tcx2 - KG_R - 20, ROW1_CY, bend="h", marker=None))
    parts.append(vu.svg_arrow_L(fx2 + FW, ROW1_CY + 40, tcx2 - KG_R - 20, ROW1_CY, bend="h", marker=None))
    parts.append(vu.svg_arrow(tcx2 - KG_R - 20, ROW1_CY, tcx2 - KG_R, ROW1_CY))
    parts.append(vu.svg_hash_node(tcx2, ROW1_CY, KG_R, "\u201eGrab\u201c", tt("geteilt, viele Fundstellen", "shared, many sites"),
                                   fill=TYPE["fill"], stroke=TYPE["stroke"]))

    parts.append(vu.svg_box(fx2, ROW2_CY - FH / 2, FW, FH, f"{c('Fundstelle')} Z", "site_54",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx2 + FW, ROW2_CY, tx2u, ROW2_CY))
    parts.append(vu.svg_box(tx2u, ROW2_CY - tuh / 2, tuw, tuh, "\u201eGrab?\u201c",
                             tt("eigener Knoten, FID-gesalzen", "own node, FID-salted"),
                             fill=U_FILL, stroke=U_STROKE, dashed=True))
    grab_type_note = tt("+ certaintyDesc \u201euncertain\u201c@en (am Typ-Knoten selbst)",
                         "+ certaintyDesc \u201euncertain\u201c@en (on the type node itself)")
    parts.append(f'<text x="{tx2u:.1f}" y="{ROW2_CY + tuh/2 + 24:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{U_STROKE}">{grab_type_note}</text>')

    parts.append(vu.svg_arrow_L(tcx2 + KG_R, ROW1_CY, qx2 - BADGE_R - 20, qy, bend="h", marker=None))
    parts.append(vu.svg_arrow_L(tx2u + tuw, ROW2_CY, qx2 - BADGE_R - 20, qy, bend="h", marker=None))
    parts.append(vu.svg_arrow(qx2 - BADGE_R - 20, qy, qx2 - BADGE_R, qy))
    parts.append(vu.svg_authority_badge(qx2, qy, "wd", r=BADGE_R, fill=vu.WORLD_COLORS["authority"]["fill"],
                                         stroke=vu.WORLD_COLORS["authority"]["stroke"]))
    parts.append(f'<text x="{qx2:.1f}" y="{qy + 54:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{same_qid_for}</text>')
    parts.append(f'<text x="{qx2:.1f}" y="{qy + 70:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{grab_label}</text>')

    parts.append(vu.svg_legend(60, 924, [
        (tt("gestrichelt = tr\u00e4gt fsl:certaintyDesc \u201euncertain\u201c@en",
            "dashed = carries fsl:certaintyDesc \u201euncertain\u201c@en"), {"fill": U_FILL, "stroke": U_STROKE}),
        (tt("Doppelring = geteilter Knoten (dedupliziert)", "double ring = shared node (deduplicated)"), TYPE),
        (tt("einfacher Kasten/Ring = eigener, nicht geteilter Knoten", "plain box/ring = own, non-shared node"),
         vu.SITE),
    ], columns=3, col_w=540))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"uncertainty-markers.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

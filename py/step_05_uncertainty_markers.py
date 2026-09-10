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

    # certain row
    f1y, kz1y = ROW1_CY - FH / 2, ROW1_CY - KZH / 2
    parts.append(vu.svg_box(fx, f1y, FW, FH, f"{c('Fundstelle')} A", "site_12", fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx + FW, ROW1_CY, kzx, ROW1_CY))
    parts.append(vu.svg_box(kzx, kz1y, KZW, KZH, c("KulturelleZuordnung"), "site_12_culture",
                             fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
    parts.append(vu.svg_arrow(kzx + KZW, ROW1_CY, kgcx - KG_R, ROW1_CY))
    parts.append(vu.svg_hash_node(kgcx, ROW1_CY, KG_R, "\u201eSBK\u201c", "kultur_a36e9d6d",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))

    # uncertain row
    f2y, kz2y = ROW2_CY - FH / 2, ROW2_CY - KZH / 2
    parts.append(vu.svg_box(fx, f2y, FW, FH, f"{c('Fundstelle')} B", "site_57", fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx + FW, ROW2_CY, kzx, ROW2_CY))
    parts.append(vu.svg_box(kzx, kz2y, KZW, KZH, c("KulturelleZuordnung"), "site_57_culture",
                             fill=U_FILL, stroke=U_STROKE, dashed=True))
    parts.append(f'<text x="{kzx:.1f}" y="{kz2y + KZH + 24:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{U_STROKE}">+ certaintyDesc \u201euncertain\u201c@en</text>')
    parts.append(vu.svg_arrow(kzx + KZW, ROW2_CY, kgcx - KG_R, ROW2_CY))
    parts.append(vu.svg_hash_node(kgcx, ROW2_CY, KG_R, "\u201eSBK?\u201c", "kultur_{hash}",
                                   fill=CULTURE["fill"], stroke=U_STROKE))

    # shared QID badge both rows converge on
    qy = (ROW1_CY + ROW2_CY) / 2
    parts.append(vu.svg_arrow(kgcx + KG_R, ROW1_CY, qx - BADGE_R, qy - 6))
    parts.append(vu.svg_arrow(kgcx + KG_R, ROW2_CY, qx - BADGE_R, qy + 6))
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
    qx2 = tcx2 + KG_R + 70 + BADGE_R

    parts.append(vu.svg_box(fx2, ROW1_CY - 40 - FH / 2, FW, FH, f"{c('Fundstelle')} X", "site_3",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_box(fx2, ROW1_CY + 40 - FH / 2, FW, FH, f"{c('Fundstelle')} Y", "site_88",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx2 + FW, ROW1_CY - 40, tcx2 - KG_R, ROW1_CY - 10))
    parts.append(vu.svg_arrow(fx2 + FW, ROW1_CY + 40, tcx2 - KG_R, ROW1_CY + 10))
    parts.append(vu.svg_hash_node(tcx2, ROW1_CY, KG_R, "\u201eGrab\u201c", tt("geteilt, viele Fundstellen", "shared, many sites"),
                                   fill=TYPE["fill"], stroke=TYPE["stroke"]))

    parts.append(vu.svg_box(fx2, ROW2_CY - FH / 2, FW, FH, f"{c('Fundstelle')} Z", "site_144",
                             fill=SITE["fill"], stroke=SITE["stroke"]))
    parts.append(vu.svg_arrow(fx2 + FW, ROW2_CY, tx2u, ROW2_CY))
    parts.append(vu.svg_box(tx2u, ROW2_CY - tuh / 2, tuw, tuh, "\u201eGrab?\u201c",
                             tt("eigener Knoten, FID-gesalzen", "own node, FID-salted"),
                             fill=U_FILL, stroke=U_STROKE, dashed=True))
    grab_type_note = tt("+ certaintyDesc \u201euncertain\u201c@en (am Typ-Knoten selbst)",
                         "+ certaintyDesc \u201euncertain\u201c@en (on the type node itself)")
    parts.append(f'<text x="{tx2u:.1f}" y="{ROW2_CY + tuh/2 + 24:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{U_STROKE}">{grab_type_note}</text>')

    parts.append(vu.svg_arrow(tcx2 + KG_R, ROW1_CY, qx2 - BADGE_R, qy - 6))
    parts.append(vu.svg_arrow(tx2u + tuw, ROW2_CY, qx2 - BADGE_R, qy + 6))
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

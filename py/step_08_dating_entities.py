#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_08_dating_entities.py -- fan-in to one culture, fan-out to N datings
=============================================================================

Source: ``modelling-rules.md`` Regel 4 ("Kulturelle Zuordnung tr\u00e4gt
eigene Datierung -- 1:1 zur Fundstelle"), and -- **revision 2026-09-11,
correction** -- ``data/fst_wgs84_lit_enriched.csv`` itself, actually
queried for three real FIDs that share ``kultur=SBK`` but carry
genuinely different ``dating_start``/``dating_end`` values:

* FID 1, "Tuengeda": -4800 / -4750
* FID 6, "Quedlinburg KGA 2": -4735 / -4550
* FID 53, "Zoellmersdorf": -4700 / -4400

The first version of this figure used "FBG" with three invented
start/end pairs (and invented FIDs 12/57/101 that are real rows, but not
FBG, and not carrying those values). SBK replaces FBG here because it
actually has this shape: 183 real SBK sites span 7 distinct start/end
pairs -- so three of them genuinely differing is the true picture. FBG,
checked afterwards, does not illustrate this well: all 14 real FBG sites
share the identical -4550/-3900 pair, so it would show fan-in correctly
but accidentally suggest fan-out variation that isn't there for that
culture. ``kultur_cc414e20`` is the real ``hashlib.md5("SBK")[:8]`` per
Regel 2/3, computed the same way as step_09's ``kultur_a36e9d6d`` (FBG).

Bilingual (revision) -- see step_00 docstring for the convention. "SBK"
and all three FIDs' real values are never translated.

**Revision 2026-09-15:** the three branches into the shared Kulturgruppe
node were diagonal; now orthogonal (the middle row sits at the circle's
own height already and stays a straight line, top/bottom rows get one
corner) -- house rule, see PRIMER.md A3.

Writes: dating-entities.de.svg/.png, dating-entities.en.svg/.png
Run standalone: ``python py/step_08_dating_entities.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["08-dating-entities"]
SITE = vu.SITE
ZUORDNUNG = vu.WORLD_COLORS["lado"]
CULTURE = {"fill": "#eef0d6", "stroke": "#6b7a1f"}
DATING = vu.WORLD_COLORS["time"]
AUTH = vu.WORLD_COLORS["authority"]

# Real FIDs, real dating values -- verified 2026-09-11 against
# fst_wgs84_lit_enriched.csv. All three share kultur=SBK.
ROWS = [
    (1, "T\u00fcngeda", "\u22124800", "\u22124750"),
    (6, "Quedlinburg KGA 2", "\u22124735", "\u22124550"),
    (53, "Z\u00f6llmersdorf", "\u22124700", "\u22124400"),
]


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    p = lambda n: vu.prop(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)
    shared = tt("geteilt", "shared")

    parts = [vu.svg_open("One shared Kulturgruppe (SBK), three individual per-site Datierung nodes -- real FIDs")]

    row_centers = [180, 480, 780]
    fw, fh = 260, 64
    kzw, kzh = 220, 64
    dw, dh = 320, 96

    fx, kzx, kgcx, dx = 90, 450, 1030, 1220
    kg_cy = row_centers[1]
    kg_r = 82

    # shared Kulturgruppe node, drawn first so arrows sit on top
    parts.append(vu.svg_hash_node(kgcx, kg_cy, kg_r, "\u201eSBK\u201c", f"kultur_cc414e20 \u00b7 {shared}",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))
    qx, qy = kgcx, kg_cy - kg_r - 70
    parts.append(vu.svg_arrow(kgcx, kg_cy - kg_r, qx, qy + 27))
    parts.append(vu.svg_authority_badge(qx, qy, "wd", r=27, fill=AUTH["fill"], stroke=AUTH["stroke"]))
    qid_all_label = tt("1 Wikidata-QID f\u00fcr alle", "1 Wikidata QID for all")
    parts.append(f'<text x="{qx:.1f}" y="{qy - 38:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{qid_all_label}</text>')
    sbk_note = tt("SBK-Fundstellen (183 real)", "SBK sites (183 real)")
    parts.append(f'<text x="{qx:.1f}" y="{qy - 22:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">{sbk_note}</text>')

    for (fid, name, start, end), cy in zip(ROWS, row_centers):
        fy = cy - fh / 2
        kzy = cy - kzh / 2
        dy = cy - dh / 2
        title = f"{c('Fundstelle')} \u00b7 FID {fid}"
        parts.append(vu.svg_box(fx, fy, fw, fh, title, name, fill=SITE["fill"], stroke=SITE["stroke"]))
        parts.append(vu.svg_arrow(fx + fw, cy, kzx, cy))
        parts.append(vu.svg_box(kzx, kzy, kzw, kzh, c("KulturelleZuordnung"), f"site_{fid}_culture",
                                 fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
        # branch to shared Kulturgruppe -- orthogonal; the middle row sits
        # at the circle's own height already, so it's a straight line,
        # the top/bottom rows get a single corner
        kg_target_y = kg_cy if cy == kg_cy else (kg_cy - 45 if cy < kg_cy else kg_cy + 45)
        if cy == kg_cy:
            parts.append(vu.svg_arrow(kzx + kzw, cy - 8, kgcx - kg_r * 0.85, kg_target_y))
        else:
            parts.append(vu.svg_arrow_L(kzx + kzw, cy - 8, kgcx - kg_r * 0.85, kg_target_y, bend="h"))
        # branch to individual Datierung
        parts.append(vu.svg_arrow(kzx + kzw, cy + 12, dx, cy + 12))
        parts.append(f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh:.1f}" rx="10" '
                     f'fill="{DATING["fill"]}" stroke="{DATING["stroke"]}" stroke-width="1.4"/>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 28:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="14.5" fill="{vu.TEXT_DARK}">{c("Datierung")} \u00b7 site_{fid}_dating</text>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 56:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{p("datierungStart")} = {start}</text>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 78:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{p("datierungEnd")} = {end}</text>')

    parts.append(vu.svg_legend(60, 900, [
        (tt(f"Doppelring = geteilt (Fan-in): 1 {c('Kulturgruppe')} f\u00fcr alle SBK-Fundstellen",
            f"double ring = shared (fan-in): 1 {c('Kulturgruppe')} for all SBK sites"), CULTURE),
        (tt(f"Kasten = eigener Knoten pro {c('Fundstelle')} (Fan-out): 3 echte, unterschiedliche "
            f"{c('Datierung')}-Werte",
            f"box = own node per {c('Fundstelle')} (fan-out): 3 real, differing {c('Datierung')} values"), DATING),
    ], columns=2, col_w=820))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"dating-entities.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

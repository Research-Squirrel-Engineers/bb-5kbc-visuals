#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_08_dating_entities.py -- fan-in to one culture, fan-out to N datings
=============================================================================

Source: ``modelling-rules.md`` Regel 4 ("Kulturelle Zuordnung tr\u00e4gt
eigene Datierung -- 1:1 zur Fundstelle"). Rather than one abstract triple
(as in step_00's hub view), this figure makes the shared-vs-per-site
contrast concrete with three example Fundstelle rows that share one
Kulturgruppe but each carry their own start/end dates -- the exact
scenario the paper's v0.10 bug report was about (see step_06's callout
for that story; this figure stays with the structural contrast itself).

Writes: dating-entities.svg / .png
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


def build() -> list[str]:
    parts = [vu.svg_open("One shared Kulturgruppe, three individual per-site Datierung nodes")]

    rows_data = [
        ("Fundstelle A", "site_12", "site_12_culture", "site_12_dating", "\u22124550", "\u22123900"),
        ("Fundstelle B", "site_57", "site_57_culture", "site_57_dating", "\u22124300", "\u22123800"),
        ("Fundstelle C", "site_101", "site_101_culture", "site_101_dating", "\u22124600", "\u22124100"),
    ]
    row_centers = [180, 480, 780]
    fw, fh = 190, 64
    kzw, kzh = 220, 64
    dw, dh = 320, 96

    fx, kzx, kgcx, dx = 90, 380, 1030, 1220
    kg_cy = row_centers[1]
    kg_r = 82

    # shared Kulturgruppe node, drawn first so arrows sit on top
    parts.append(vu.svg_hash_node(kgcx, kg_cy, kg_r, "\u201eFBG\u201c", "kultur_a1b2c3d4 \u00b7 shared",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))
    qx, qy = kgcx, kg_cy - kg_r - 70
    parts.append(vu.svg_arrow(kgcx, kg_cy - kg_r, qx, qy + 27))
    parts.append(vu.svg_authority_badge(qx, qy, "wd", r=27, fill=AUTH["fill"], stroke=AUTH["stroke"]))
    parts.append(f'<text x="{qx:.1f}" y="{qy - 38:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">1 Wikidata QID for all</text>')
    parts.append(f'<text x="{qx:.1f}" y="{qy - 22:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" fill="{vu.TEXT_MUTED}">FBG sites</text>')

    for (title, sub, kzsub, dsub, start, end), cy in zip(rows_data, row_centers):
        fy = cy - fh / 2
        kzy = cy - kzh / 2
        dy = cy - dh / 2
        parts.append(vu.svg_box(fx, fy, fw, fh, title, sub, fill=SITE["fill"], stroke=SITE["stroke"]))
        parts.append(vu.svg_arrow(fx + fw, cy, kzx, cy))
        parts.append(vu.svg_box(kzx, kzy, kzw, kzh, "KulturelleZuordnung", kzsub,
                                 fill=ZUORDNUNG["fill"], stroke=ZUORDNUNG["stroke"]))
        # branch to shared Kulturgruppe
        parts.append(vu.svg_arrow(kzx + kzw, cy - 8, kgcx - kg_r * 0.85, kg_cy - (kg_cy - cy) * 0.35 - 8))
        # branch to individual Datierung
        parts.append(vu.svg_arrow(kzx + kzw, cy + 12, dx, cy + 12))
        parts.append(f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh:.1f}" rx="10" '
                     f'fill="{DATING["fill"]}" stroke="{DATING["stroke"]}" stroke-width="1.4"/>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 28:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="14.5" fill="{vu.TEXT_DARK}">Datierung \u00b7 {sub}</text>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 56:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">datierungStart = {start}</text>')
        parts.append(f'<text x="{dx + 22:.1f}" y="{dy + 78:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">datierungEnd = {end}</text>')

    parts.append(vu.svg_legend(60, 900, [
        ("double ring = shared (fan-in): 1 Kulturgruppe for all three sites", CULTURE),
        ("box = own node per Fundstelle (fan-out): 3 individual Datierung nodes", DATING),
    ], columns=2, col_w=820))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "dating-entities", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

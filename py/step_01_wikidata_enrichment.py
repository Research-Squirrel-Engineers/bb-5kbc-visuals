#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_01_wikidata_enrichment.py -- Wikidata as the linking hub
==================================================================

Source: paper section 3.2 ("Geographische Anreicherung ueber Wikidata") and
``data/raw/bb-5kbc-sites/wikidata_map.py`` (constants ``FUZZY_THRESHOLD``,
``KREIS_FUZZY_THRESHOLD``, ``GEMEINDE_FUZZY_THRESHOLD``,
``SPARQL_TIMEOUT_STAGE2`` -- verified against the actual script, not
retyped from the paper alone).

Two panels below a four-stage pipeline banner: how the SPARQL index is
built per administrative level (global vs. scoped, and the two guard
clauses every fetch applies), and the two-stage Gemeinde resolution that
was the hardest methodological problem in that section (direct P131 misses
German Ortsteile that hang off an intermediate Gemeinde rather than
directly off the Kreis). The fuzzy-matching step itself (stage 4) is
covered in detail in 02-fuzzy-matching, not repeated here.

Writes: wikidata-enrichment.svg / .png
Run standalone: ``python py/step_01_wikidata_enrichment.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["01-wikidata-enrichment"]
C = vu.PIPELINE_COLORS["enrich"]
C_OK = vu.PIPELINE_COLORS["lod"]
C_WARN = vu.PIPELINE_COLORS["validate"]


def _caption(x: float, y: float, lines: list[str], *, size: int = 11.5) -> str:
    parts = []
    for i, line in enumerate(lines):
        parts.append(f'<text x="{x:.1f}" y="{y + i * 18:.1f}" font-family="Fira Sans" '
                      f'font-size="{size}" fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
    return "\n".join(parts)


def build() -> list[str]:
    parts = [vu.svg_open("Wikidata as the linking hub -- the four-stage geo-matching pipeline")]

    # -- four-stage pipeline banner ------------------------------------------
    bw, bh, gap = 260, 96, 60
    total = 4 * bw + 3 * gap
    x0 = 60 + (1630 - total) / 2
    y0 = 70
    steps = [
        ("1 Build index", "SPARQL per level"),
        ("2 Normalise", "prefix strip + alias"),
        ("3 Override layer", "manually verified"),
        ("4 Fuzzy match", "rapidfuzz, staged \u2014 see next figure"),
    ]
    xs = [x0 + i * (bw + gap) for i in range(4)]
    for x, (title, subtitle) in zip(xs, steps):
        parts.append(vu.svg_box(x, y0, bw, bh, title, subtitle, fill=C["fill"], stroke=C["stroke"]))
    for i in range(3):
        parts.append(vu.svg_arrow(xs[i] + bw, y0 + bh / 2, xs[i + 1], y0 + bh / 2))

    captions = [
        ["Land/Bundesland: global, once.", "Kreis: scoped per Bundesland."],
        ["\u201eLandkreis X\u201c \u2192 X.", "Alias lists deliberately small (1/2/2)."],
        ["Ambiguous / outdated names.", "1 / 33 / 62 entries (BL/KR/GE)."],
        ["token_sort_ratio, staged thresholds.", "matchReason: exact/fuzzy/override/transitive."],
    ]
    for x, cap in zip(xs, captions):
        parts.append(_caption(x, y0 + bh + 26, cap))

    # -- left panel: index building per level --------------------------------
    lp_x, lp_y, lp_w, lp_h = 60, 300, 790, 610
    parts.append(vu.svg_dashed_container(lp_x, lp_y, lp_w, lp_h, "Stage 1: index building per level"))
    idx_rows = [
        ("Land / Bundesland", "Global, one-off SPARQL fetch over the whole class "
         "(wdt:P31 souverainer Staat / Land in Deutschland / polnische Woiwodschaft)."),
        ("Kreis", "Scoped per Bundesland (wdt:P131 direct, not transitive) \u2014 a single global fetch "
         "would push the SPARQL response past the endpoint's timeout."),
        ("Gemeinde", "Scoped per Kreis; see the two-stage fallback for Ortsteile that hang off an "
         "intermediate Gemeinde instead of the Kreis directly."),
    ]
    ry = lp_y + 66
    for level, text in idx_rows:
        parts.append(vu.svg_box(lp_x + 30, ry, 200, 56, level, fill=C["fill"], stroke=C["stroke"]))
        words = text.split()
        line, lines, cur_len = [], [], 0
        for w in words:
            if cur_len + len(w) + 1 > 62:
                lines.append(" ".join(line))
                line, cur_len = [], 0
            line.append(w)
            cur_len += len(w) + 1
        if line:
            lines.append(" ".join(line))
        for i, ln in enumerate(lines):
            parts.append(f'<text x="{lp_x + 250:.1f}" y="{ry + 16 + i * 19:.1f}" font-family="Fira Sans" '
                         f'font-size="12.5" fill="{vu.TEXT_DARK}">{vu.xml_escape(ln)}</text>')
        ry += 150
    guard_y = ry + 10
    parts.append(vu.svg_box(lp_x + 30, guard_y, 700, 68, "Two guards applied to every index fetch",
                             "MINUS {{ ?item wdt:P582 [] }} excludes dissolved units \u2014 "
                             "FILTER(STRLEN(?label) > 3) drops vehicle-plate skos:altLabels",
                             fill="#f1efe8", stroke=vu.LINE_NEUTRAL))

    # -- right panel: two-stage Gemeinde resolution --------------------------
    rp_x, rp_y, rp_w, rp_h = 900, 300, 790, 610
    parts.append(vu.svg_dashed_container(rp_x, rp_y, rp_w, rp_h, "Gemeinde level: two-stage SPARQL fallback"))

    cw = 650
    cx0 = rp_x + (rp_w - cw) / 2
    y = rp_y + 66
    parts.append(vu.svg_box(cx0, y, cw, 58, "CSV value, e.g. \u201eBabekuhl\u201c",
                             "Gemeinde Putlitz, Landkreis Prignitz",
                             fill="#f1efe8", stroke=vu.LINE_NEUTRAL))
    y2 = y + 58 + 46
    parts.append(vu.svg_arrow(cx0 + cw / 2, y + 58, cx0 + cw / 2, y2))
    parts.append(vu.svg_box(cx0, y2, cw, 68, "Phase 1", "P131 direct, index scoped to the Kreis QID",
                             fill=C["fill"], stroke=C["stroke"]))
    y3 = y2 + 68 + 54
    parts.append(vu.svg_arrow_labeled(cx0 + cw / 2, y2 + 68, cx0 + cw / 2, y3,
                                       "no match (Ortsteil hangs off an intermediate Gemeinde)"))
    parts.append(vu.svg_box(cx0, y3, cw, 68, "Phase 2 (fallback)",
                             "P131+ transitive + exact label filter, 90 s timeout",
                             fill=C_WARN["fill"], stroke=C_WARN["stroke"]))

    y4 = y3 + 68 + 50
    half = (cw - 40) / 2
    parts.append(vu.svg_box(cx0, y4, half, 68, "Match",
                             "matchReason=transitive, matchScore logged",
                             fill=C_OK["fill"], stroke=C_OK["stroke"]))
    parts.append(vu.svg_box(cx0 + half + 40, y4, half, 68, "Timeout \u2192 no match",
                             "run continues, matchReason=timeout, triage report",
                             fill=C_WARN["fill"], stroke=C_WARN["stroke"]))
    parts.append(vu.svg_arrow(cx0 + cw * 0.28, y3 + 68, cx0 + half / 2, y4))
    parts.append(vu.svg_arrow(cx0 + cw * 0.72, y3 + 68, cx0 + half + 40 + half / 2, y4))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "wikidata-enrichment", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

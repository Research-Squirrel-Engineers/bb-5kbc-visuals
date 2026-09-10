#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_06_uncertainty_dating.py -- absolute dating: numbers + free-text tolerance
====================================================================================

Source: ``data/raw/bb-5kbc-sites/bb5kbc-classes.mmd`` (the five Datierung
attributes, verbatim) and ``modelling-rules.md`` sections "Regel 4" (why
Datierung is per-site, not deduplicated -- the v0.10 data-loss lesson) and
"Numerische Unsicherheits-Toleranz" under "Was die Modellierung nicht
kann" (the free-text limitation, not invented for the figure).

Writes: uncertainty-dating.svg / .png
Run standalone: ``python py/step_06_uncertainty_dating.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["06-uncertainty-dating"]
DATING = vu.WORLD_COLORS["time"]
CRM = vu.WORLD_COLORS["crm"]
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE


def _uml_box(x, y, w, h, stereotypes, title, subtitle, rows):
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" '
             f'fill="{DATING["fill"]}" stroke="{DATING["stroke"]}" stroke-width="1.8"/>']
    cx = x + w / 2
    sy = y + 32
    for i, st in enumerate(stereotypes):
        parts.append(f'<text x="{cx:.1f}" y="{sy + i * 17:.1f}" text-anchor="middle" font-family="Fira Sans" '
                      f'font-size="12" font-style="italic" fill="{vu.TEXT_DARK}" opacity="0.75">'
                      f'\u00ab{vu.xml_escape(st)}\u00bb</text>')
    ty = sy + len(stereotypes) * 17 + 12
    parts.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="21" fill="{vu.TEXT_DARK}">{vu.xml_escape(title)}</text>')
    parts.append(f'<text x="{cx:.1f}" y="{ty + 22:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="13" fill="{vu.TEXT_MUTED}">{vu.xml_escape(subtitle)}</text>')
    divider_y = ty + 40
    parts.append(f'<line x1="{x:.1f}" y1="{divider_y:.1f}" x2="{x + w:.1f}" y2="{divider_y:.1f}" '
                 f'stroke="{DATING["stroke"]}" stroke-width="1.2"/>')
    ry = divider_y + 40
    for label, typ, example, uncertain in rows:
        col = U_STROKE if uncertain else vu.TEXT_DARK
        parts.append(f'<text x="{x + 30:.1f}" y="{ry:.1f}" font-family="Fira Sans" font-size="15" '
                     f'font-weight="500" fill="{col}">{vu.xml_escape(label)}</text>')
        parts.append(f'<text x="{x + 30:.1f}" y="{ry + 20:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(typ)} = {vu.xml_escape(example)}</text>')
        ry += 68
    return "\n".join(parts)


def build() -> list[str]:
    parts = [vu.svg_open("Absolute dating: numeric start/end plus free-text tolerance, not structured")]

    # -- left: UML attribute box ----------------------------------------------
    ux, uy, uw, uh = 90, 50, 650, 470
    rows = [
        ("datierungStart", "xsd:integer", "\u22124550", False),
        ("datierungEnd", "xsd:integer", "\u22123900", False),
        ("datierungSicherheitStart", "xsd:string", "\u201e\u00b1 100 Jahre\u201c", True),
        ("datierungSicherheitEnd", "xsd:string", "\u201eunsicher\u201c", True),
        ("datierungSicherheitRange", "xsd:string", "\u201egrob\u201c", True),
    ]
    parts.append(_uml_box(ux, uy, uw, uh, ["crm:E52_Time-Span", "time:Interval"],
                           "Datierung", "site_{FID}_dating", rows))

    # -- top-right: double CRM/OWL-Time anchor --------------------------------
    cx1 = 860
    cw1, ch1 = 320, 64
    cy1, cy2 = 70, 190
    parts.append(vu.svg_box(cx1, cy1, cw1, ch1, "crm:E52_Time-Span", "CRM-conformant time span",
                             fill=CRM["fill"], stroke=CRM["stroke"]))
    parts.append(vu.svg_arrow(ux + uw, uy + 110, cx1, cy1 + ch1 / 2))

    parts.append(vu.svg_box(cx1, cy2, cw1, ch1, "time:Interval", "owl-time:TemporalEntity",
                             fill=DATING["fill"], stroke=DATING["stroke"]))
    parts.append(vu.svg_arrow(ux + uw, uy + 260, cx1, cy2 + ch1 / 2))
    parts.append(f'<text x="{cx1:.1f}" y="{cy2 + ch1 + 30:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">\u2192 opens Allen relations: \u201ePhase A ends</text>')
    parts.append(f'<text x="{cx1:.1f}" y="{cy2 + ch1 + 48:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">before Phase B begins\u201c</text>')

    # -- "why per Fundstelle?" callout ----------------------------------------
    wx, wy, ww, wh = 860, 350, 780, 170
    parts.append(vu.svg_dashed_container(wx, wy, ww, wh, "Why 1:1 per Fundstelle, not shared?"))
    lines = [
        "If Datierung were deduplicated per Kulturgruppe (v0.10), all ~200 SBK sites would",
        "converge on one shared node \u2014 individual start/end values would blend into an",
        "unrecoverable multi-set. The bug only surfaced under end-to-end validation",
        "(validate_lod.py); from v0.11 the assignment is site-specific.",
    ]
    for i, line in enumerate(lines):
        parts.append(f'<text x="{wx + 26:.1f}" y="{wy + 54 + i * 21:.1f}" font-family="Fira Sans" '
                     f'font-size="13" fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')

    # -- bottom: free-text tolerance -------------------------------------------
    by, bh = 570, 330
    parts.append(vu.svg_dashed_container(60, by, 1630, bh,
                                          "Numeric uncertainty tolerance stays free text \u2014 no xsd:duration, no structured field"))
    chips = ["\u201e\u00b1 100 Jahre\u201c", "\u201egrob\u201c", "\u201eunsicher\u201c", "\u201eca. 50 a\u201c",
             "\u201eunclear\u201c", "\u201e+/- 50 years\u201c", "\u201eSch\u00e4tzung\u201c"]
    cx = 100
    cy_chip = by + 66
    for chip in chips:
        w = vu.text_width(chip, 14) + 38
        parts.append(vu.svg_box(cx, cy_chip, w, 48, chip, fill=U_FILL, stroke=U_STROKE, rx=24))
        cx += w + 24
    note1 = "Values are heterogeneous (German/English, with typo variants) and are stored 1:1 as xsd:string."
    note2 = "Anyone filtering for \u201etolerance < 50 years\u201c has to parse these strings themselves first."
    parts.append(f'<text x="100" y="{by + 150:.1f}" font-family="Fira Sans" font-size="14" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(note1)}</text>')
    parts.append(f'<text x="100" y="{by + 176:.1f}" font-family="Fira Sans" font-size="14" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(note2)}</text>')
    parts.append(f'<text x="100" y="{by + 216:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{vu.TEXT_MUTED}">A deliberately accepted limitation \u2014 see modelling-rules.md, '
                 f'\u201eWas die Modellierung nicht kann\u201c</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "uncertainty-dating", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

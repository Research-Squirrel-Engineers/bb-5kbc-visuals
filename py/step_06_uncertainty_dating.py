#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_06_uncertainty_dating.py -- absolute dating: numbers + free-text tolerance
====================================================================================

Source: ``data/raw/bb-5kbc-sites/bb5kbc-classes.mmd`` (the five Datierung
attributes, verbatim), ``modelling-rules.md`` Regel 4 (why Datierung is
per-site, not deduplicated) and section "Numerische Unsicherheits-Toleranz",
and -- unlike the first version of this figure --
``data/fst_wgs84_lit_enriched.csv`` itself, actually opened and queried,
plus ``data/bb5kbc-csv-issues.md`` item 6 for the cleanup history.

**Revision 2026-09-11 (correction):** the first version of this figure
used invented example values (a German/English mix of short tags like
"grob", "unsicher", "Schaetzung") that were never in the data, in any
state, and claimed in this docstring that they were real. They were not
-- nobody had actually opened the CSV when that version was written.
This version fixes that: the UML box uses a real FID (see below), and
the free-text panel shows the *actual* distinct values of
``dating_certainty_range`` with their real counts, computed once via
``Counter()`` over all 540 rows (verified 2026-09-11). The
``dating_certainty_start``/``_end`` columns are, as of the current file,
already cleanly normalised to four "+/- N years" patterns -- the
German/whitespace heterogeneity this figure originally (wrongly)
illustrated with those two columns was a real, but *already-fixed*,
issue logged in ``bb5kbc-csv-issues.md`` item 6; that history is now
shown explicitly instead of being conflated with the present state.

Bilingual (revision) -- see step_00 docstring for the convention. FID 1
("Tuengeda") and its real values, and every ``dating_certainty_range``
string quoted below, are real CSV content and are never translated,
paraphrased, or altered in either language.

**Revision 2026-09-15g:** two issues Florian flagged from the same
screenshot. (1) The two connectors into crm:E52_Time-Span/time:Interval
already carry the ``bend="v"`` fix from S36 (horizontal entry, not
vertical) -- re-confirmed here, since the screenshot showed the older
vertical-entry behaviour, most likely from a not-yet-rebuilt or
not-yet-repatched copy rather than a regression in this file. (2) The
real bug: the widest bar (n=299) plus its count label could run past
the dashed container's right edge -- ``bar_w`` was a fixed 1560px that
was never checked against how wide "n=299" actually renders. Now
computed from the container's real right edge minus the widest "n=NNN"
label's actual rendered width (``vu.text_width``), so the longest bar
can never push its label past the border, whatever the counts turn out
to be.

Writes: uncertainty-dating.de.svg/.png, uncertainty-dating.en.svg/.png
Run standalone: ``python py/step_06_uncertainty_dating.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["06-uncertainty-dating"]
DATING = vu.WORLD_COLORS["time"]
CRM = vu.WORLD_COLORS["crm"]
U_FILL, U_STROKE = vu.UNCERTAIN_FILL, vu.UNCERTAIN_STROKE
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}

# Real dating_certainty_range values, Counter() over all 540 rows of
# fst_wgs84_lit_enriched.csv, verified 2026-09-11. Only the four largest
# groups are charted; the remaining 10 singleton/near-singleton values
# (7 more distinct sentences, 14 rows total) are summarised, not listed
# individually, to keep the panel legible -- see the docstring above for
# where to find the full breakdown if needed.
RANGE_VALUES = [
    ("low precision, as only stylistic dating", 299),
    ("dating still very uncertain, for the whole group only few 14C dates available", 203),
    ("very uncertain, no dated features", 24),
    ("high certainty due to excessive radiocarbon dating and Bayesian modelling", 1),
]


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
    ry = divider_y + 34
    for label, typ, example, uncertain in rows:
        col = U_STROKE if uncertain else vu.TEXT_DARK
        parts.append(f'<text x="{x + 30:.1f}" y="{ry:.1f}" font-family="Fira Sans" font-size="14.5" '
                     f'font-weight="500" fill="{col}">{vu.xml_escape(label)}</text>')
        parts.append(f'<text x="{x + 30:.1f}" y="{ry + 19:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(typ)} = {vu.xml_escape(example)}</text>')
        ry += 58
    return "\n".join(parts)


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    p = lambda n: vu.prop(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)

    parts = [vu.svg_open("Absolute dating: real FID, real certainty values -- verified against the CSV")]

    fid_note = tt("FID 1 \u00b7 \u201eT\u00fcngeda\u201c \u00b7 kultur = SBK", "FID 1 \u00b7 \u201eT\u00fcngeda\u201c \u00b7 kultur = SBK")
    parts.append(f'<text x="90" y="42" font-family="Fira Sans" font-size="13" font-style="italic" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(fid_note)}</text>')

    # -- left: UML attribute box, real FID 1 values ---------------------------
    ux, uy, uw, uh = 90, 55, 650, 470
    rows = [
        (p("datierungStart"), "xsd:integer", "\u22124800", False),
        (p("datierungEnd"), "xsd:integer", "\u22124750", False),
        (p("datierungSicherheitStart"), "xsd:string", "\u201e+/- 100 years\u201c", True),
        (p("datierungSicherheitEnd"), "xsd:string", "\u201e+/- 100 years\u201c", True),
        (p("datierungSicherheitRange"), "xsd:string", "\u201elow precision, as only stylistic dating\u201c", True),
    ]
    parts.append(_uml_box(ux, uy, uw, uh, ["crm:E52_Time-Span", "time:Interval"],
                           c("Datierung"), "site_1_dating", rows))

    # -- top-right: double CRM/OWL-Time anchor --------------------------------
    cx1 = 860
    cw1, ch1 = 320, 64
    cy1, cy2 = 75, 195
    parts.append(vu.svg_box(cx1, cy1, cw1, ch1, "crm:E52_Time-Span",
                             tt("CRM-konforme Zeitspanne", "CRM-conformant time span"),
                             fill=CRM["fill"], stroke=CRM["stroke"]))
    parts.append(vu.svg_arrow_L(ux + uw, uy + 115, cx1, cy1 + ch1 / 2, bend="v"))

    parts.append(vu.svg_box(cx1, cy2, cw1, ch1, "time:Interval", "owl-time:TemporalEntity",
                             fill=DATING["fill"], stroke=DATING["stroke"]))
    parts.append(vu.svg_arrow_L(ux + uw, uy + 265, cx1, cy2 + ch1 / 2, bend="v"))
    allen1 = tt("\u2192 \u00f6ffnet Allen-Relationen: \u201ePhase A endet,",
                "\u2192 opens Allen relations: \u201ePhase A ends")
    allen2 = tt("bevor Phase B beginnt\u201c", "before Phase B begins\u201c")
    parts.append(f'<text x="{cx1:.1f}" y="{cy2 + ch1 + 30:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">{allen1}</text>')
    parts.append(f'<text x="{cx1:.1f}" y="{cy2 + ch1 + 48:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">{allen2}</text>')

    # -- "why per Fundstelle?" callout ----------------------------------------
    wx, wy, ww, wh = 860, 365, 780, 155
    parts.append(vu.svg_dashed_container(wx, wy, ww, wh,
                                          tt(f"Warum 1:1 zur {c('Fundstelle')}, nicht geteilt?",
                                             f"Why 1:1 per {c('Fundstelle')}, not shared?")))
    lines_de = [
        f"W\u00e4re {c('Datierung')} pro {c('Kulturgruppe')} dedupliziert (v0.10), l\u00e4gen alle ~200 SBK-",
        f"{c('Fundstelle')}n am selben Datierungs-Knoten \u2014 individuelle Start/End-Werte w\u00fcrden sich zu",
        "einem nicht mehr aufl\u00f6sbaren Multi-Set vermischen. Die End-to-End-Validierung",
        "(validate_lod.py) deckte das auf; ab v0.11 ist die Zuordnung site-spezifisch.",
    ]
    lines_en = [
        f"If {c('Datierung')} were deduplicated per {c('Kulturgruppe')} (v0.10), all ~200 SBK sites would",
        "converge on the same dating node \u2014 individual start/end values would blend into an",
        "unrecoverable multi-set. End-to-end validation (validate_lod.py) surfaced this;",
        "from v0.11 the assignment is site-specific.",
    ]
    for i, line in enumerate(tt(lines_de, lines_en)):
        parts.append(f'<text x="{wx + 26:.1f}" y="{wy + 42 + i * 21:.1f}" font-family="Fira Sans" '
                     f'font-size="12.5" fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')

    # -- bottom: real free-text heterogeneity, with real counts -----------------
    by, bh = 545, 400
    parts.append(vu.svg_dashed_container(60, by, 1630, bh,
                                          tt("dating_certainty_range: echte Freitext-Heterogenit\u00e4t, "
                                             "mit echten H\u00e4ufigkeiten (n=540)",
                                             "dating_certainty_range: real free-text heterogeneity, "
                                             "with real counts (n=540)")))
    bar_x, bar_y0 = 100, by + 60
    label_w = 620
    max_val = RANGE_VALUES[0][1]
    # right edge of the container, minus a margin, minus room for the
    # widest "n=NNN" label -- so the longest bar (n=299) can never push
    # its own count label past the dashed border (the overflow Florian
    # flagged: bar_w was set once and never checked against the actual
    # rendered width of "n=299").
    widest_n_label = max(vu.text_width(f"n={c}", 12.5) for _, c in RANGE_VALUES)
    container_right = 60 + 1630
    bar_w = container_right - 20 - widest_n_label - 10 - bar_x - label_w
    ry = bar_y0
    for text, count in RANGE_VALUES:
        parts.append(f'<text x="{bar_x:.1f}" y="{ry + 15:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_DARK}">\u201e{vu.xml_escape(text)}\u201c</text>')
        bw = max(4, count / max_val * (bar_w - label_w))
        parts.append(f'<rect x="{bar_x + label_w:.1f}" y="{ry - 12:.1f}" width="{bw:.1f}" height="22" rx="5" '
                     f'fill="{DATING["fill"]}" stroke="{DATING["stroke"]}" stroke-width="1.2"/>')
        parts.append(f'<text x="{bar_x + label_w + bw + 10:.1f}" y="{ry + 4:.1f}" font-family="Fira Sans" '
                     f'font-weight="500" font-size="12.5" fill="{vu.TEXT_DARK}">n={count}</text>')
        ry += 42

    rest_note = tt("+ 10 weitere distinkte S\u00e4tze, je 1\u20132 Zeilen (z. B. \u201every certain because of "
                   "detailed modelling of several 14C dates\u201c) \u2014 volle Liste in fst_wgs84_lit_enriched.csv.",
                   "+ 10 more distinct sentences, 1\u20132 rows each (e.g. \u201every certain because of "
                   "detailed modelling of several 14C dates\u201c) \u2014 full list in fst_wgs84_lit_enriched.csv.")
    parts.append(f'<text x="{bar_x:.1f}" y="{ry + 6:.1f}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(rest_note)}</text>')

    parts.append(f'<line x1="{bar_x:.1f}" y1="{ry + 26:.1f}" x2="{bar_x + bar_w:.1f}" y2="{ry + 26:.1f}" '
                 f'stroke="#dedcd4" stroke-width="1"/>')

    hist_title = tt("Zum Vergleich: dating_certainty_start/end sind heute sauber \u2014 waren es nicht immer",
                     "By contrast: dating_certainty_start/end are clean today \u2014 they weren't always")
    parts.append(f'<text x="{bar_x:.1f}" y="{ry + 52:.1f}" font-family="Fira Sans" font-weight="500" '
                 f'font-size="12.5" fill="{vu.TEXT_DARK}">{vu.xml_escape(hist_title)}</text>')
    hist_lines = tt(
        ["Heute: alle 540 Zeilen gef\u00fcllt, genau 4 Muster \u2014 \u201e+/- 100/50/200/10 years\u201c.",
         "Fr\u00fcher: 68 leere Zellen, plus Schreibvarianten (\u201e+ / - 100 years\u201c "
         "vs. \u201e+/- 200 years\u201c) und eine deutsche Variante (\u201e+ /- 100 Jahre\u201c, 51 Zeilen) \u2014 "
         "von Sophie vereinheitlicht."],
        ["Today: all 540 rows filled, exactly 4 patterns \u2014 \u201e+/- 100/50/200/10 years\u201c.",
         "Before: 68 empty cells, plus spelling variants (\u201e+ / - 100 years\u201c "
         "vs. \u201e+/- 200 years\u201c) and a German variant (\u201e+ /- 100 Jahre\u201c, 51 rows) \u2014 "
         "unified by Sophie."])
    hy = ry + 74
    for line in hist_lines:
        parts.append(f'<text x="{bar_x:.1f}" y="{hy:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        hy += 20

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"uncertainty-dating.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_02_fuzzy_matching.py -- how token_sort_ratio actually decides a match
================================================================================

Source: paper section 3.2 (step 4, "Fuzzy-Matching mit gestaffelten
Schwellwerten") and ``data/raw/bb-5kbc-sites/wikidata_map.py`` for the
mechanism (``rapidfuzz.process.extractOne`` with ``fuzz.token_sort_ratio``,
score divided by 100 to sit on the same 0-1 scale as ``FUZZY_THRESHOLD`` /
``KREIS_FUZZY_THRESHOLD`` / ``GEMEINDE_FUZZY_THRESHOLD``) and the four
per-level thresholds (0.85 / 0.85 / 0.75 / 0.82).

The four worked examples are not invented: each score is the real output
of ``rapidfuzz.fuzz.token_sort_ratio(a, b)``, computed once while building
this figure (see the numbers in ``EXAMPLES`` below) against string pairs
that mirror the paper's own cases (the "Landkreis X" prefix problem; the
"MVP" / "sommerda" aliases the paper names explicitly in section 3.2).
This shows *why* prefix-stripping and the alias layer exist: fuzzy
tolerance alone does not rescue an acronym or a prefix that dominates a
short name.

Writes: fuzzy-matching.svg / .png
Run standalone: ``python py/step_02_fuzzy_matching.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["02-fuzzy-matching"]
C = vu.PIPELINE_COLORS["enrich"]
PASS_C = vu.PIPELINE_COLORS["lod"]
FAIL_C = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}

# (csv_value, wikidata_label, level, threshold_pct, score_pct, passes, note)
# Scores are real rapidfuzz.fuzz.token_sort_ratio(csv_value, wikidata_label)
# output, verified 2026-09-10 against rapidfuzz 3.14.6.
EXAMPLES = [
    ("Kreis Ostprignitz-Ruppin", "Ostprignitz-Ruppin", "KREIS", 75, 85.71, True,
     "A short prefix on a long name barely moves the score \u2014 fuzzy tolerance alone is enough."),
    ("Landkreis Havelland", "Havelland", "KREIS", 75, 64.29, False,
     "The same kind of prefix on a short name drags the score under threshold \u2014 needs the "
     "prefix-strip step first (stripped: \u201eHavelland\u201c \u2192 100.00)."),
    ("sommerda", "S\u00f6mmerda", "GEMEINDE", 82, 75.00, False,
     "A transliteration typo just misses the Gemeinde threshold \u2014 resolved via the alias "
     "list (paper \u00a73.2), not by loosening the threshold."),
    ("MVP", "Mecklenburg-Vorpommern", "BUNDESLAND", 85, 16.00, False,
     "An acronym shares almost no characters with the full name \u2014 fuzzy matching cannot "
     "help at all; the alias list is the only fix."),
]


def _wrap(text: str, width: int) -> list[str]:
    words, line, lines, cur = text.split(), [], [], 0
    for w in words:
        if cur + len(w) + 1 > width:
            lines.append(" ".join(line))
            line, cur = [], 0
        line.append(w)
        cur += len(w) + 1
    if line:
        lines.append(" ".join(line))
    return lines


def _mechanism_row(parts, y):
    bw, gap = 340, 46
    total = 4 * bw + 3 * gap
    x0 = 60 + (1630 - total) / 2
    steps = [
        ("1 Tokenise", "split the string on whitespace"),
        ("2 Sort tokens", "alphabetical order \u2014 word order stops mattering"),
        ("3 Rejoin", "compare the two sorted strings"),
        ("4 Score", "Levenshtein-based ratio, 0\u2013100"),
    ]
    xs = [x0 + i * (bw + gap) for i in range(4)]
    for x, (title, sub) in zip(xs, steps):
        parts.append(vu.svg_box(x, y, bw, 74, title, sub, fill=C["fill"], stroke=C["stroke"]))
    for i in range(3):
        parts.append(vu.svg_arrow(xs[i] + bw, y + 37, xs[i + 1], y + 37))
    return y + 74


def _gauge(parts, x, y, w, score, threshold, passed):
    """0-100 bar: filled track up to score, a tick + label at the threshold."""
    h = 26
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" '
                 f'fill="#f1efe8" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    fw = w * score / 100
    fill, stroke = (PASS_C if passed else FAIL_C["fill"], None)
    col = PASS_C["stroke"] if passed else vu.UNCERTAIN_STROKE
    bg = PASS_C["fill"] if passed else vu.UNCERTAIN_FILL
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{fw:.1f}" height="{h:.1f}" rx="6" '
                 f'fill="{bg}" stroke="{col}" stroke-width="1.4"/>')
    tx = x + w * threshold / 100
    parts.append(f'<line x1="{tx:.1f}" y1="{y - 6:.1f}" x2="{tx:.1f}" y2="{y + h + 6:.1f}" '
                 f'stroke="{vu.TEXT_DARK}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    parts.append(f'<text x="{tx:.1f}" y="{y - 12:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="11" fill="{vu.TEXT_DARK}">threshold {threshold}</text>')
    parts.append(f'<text x="{x + w + 14:.1f}" y="{y + h/2:.1f}" dominant-baseline="central" '
                 f'font-family="Fira Sans" font-weight="500" font-size="15" fill="{col}">'
                 f'{score:.2f}</text>')


def build() -> list[str]:
    parts = [vu.svg_open("How rapidfuzz.token_sort_ratio decides a Wikidata match, with real scores")]

    y_after_mech = _mechanism_row(parts, 60)

    row_y0 = y_after_mech + 70
    pitch = 178
    for i, (csv_val, wd_label, level, threshold, score, passed, note) in enumerate(EXAMPLES):
        ry = row_y0 + i * pitch

        parts.append(f'<text x="60" y="{ry + 4:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="14.5" fill="{vu.TEXT_DARK}">CSV \u201e{vu.xml_escape(csv_val)}\u201c</text>')
        parts.append(f'<text x="60" y="{ry + 26:.1f}" font-family="Fira Sans" font-size="13" '
                     f'fill="{vu.TEXT_MUTED}">vs. Wikidata label \u201e{vu.xml_escape(wd_label)}\u201c</text>')
        parts.append(f'<rect x="60" y="{ry + 40:.1f}" width="86" height="24" rx="12" '
                     f'fill="#ece9e2" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
        parts.append(f'<text x="103" y="{ry + 52:.1f}" text-anchor="middle" dominant-baseline="central" '
                     f'font-family="Fira Sans" font-size="11" fill="{vu.TEXT_DARK}">{level}</text>')

        _gauge(parts, 470, ry + 6, 560, score, threshold, passed)

        badge_x = 1150
        col = PASS_C["stroke"] if passed else vu.UNCERTAIN_STROKE
        bg = PASS_C["fill"] if passed else vu.UNCERTAIN_FILL
        label = "PASS" if passed else "FAIL"
        parts.append(f'<rect x="{badge_x:.1f}" y="{ry - 4:.1f}" width="86" height="30" rx="15" '
                     f'fill="{bg}" stroke="{col}" stroke-width="1.6"/>')
        parts.append(f'<text x="{badge_x + 43:.1f}" y="{ry + 11:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" '
                     f'font-size="13" fill="{col}">{label}</text>')

        note_lines = _wrap(note, 58)
        for j, ln in enumerate(note_lines):
            parts.append(f'<text x="1260" y="{ry + 2 + j * 19:.1f}" font-family="Fira Sans" '
                         f'font-size="12.5" fill="{vu.TEXT_DARK}">{vu.xml_escape(ln)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, "fuzzy-matching", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build()


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

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

Bilingual (revision 2026-09-10c) -- see step_00 docstring for the
translation convention. The CSV values and Wikidata labels compared
(e.g. "Landkreis Havelland", "sommerda") are real strings, never
translated; the level badge (KREIS/GEMEINDE/...) uses ``vu.cls()``.

Writes: fuzzy-matching.de.svg/.png, fuzzy-matching.en.svg/.png
Run standalone: ``python py/step_02_fuzzy_matching.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["02-fuzzy-matching"]
C = vu.PIPELINE_COLORS["enrich"]
PASS_C = vu.PIPELINE_COLORS["lod"]
FAIL_C = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}

# (csv_value, wikidata_label, level_class, threshold_pct, score_pct, passes, note_de, note_en)
# Scores are real rapidfuzz.fuzz.token_sort_ratio(csv_value, wikidata_label)
# output, verified 2026-09-10 against rapidfuzz 3.14.6.
EXAMPLES = [
    ("Kreis Ostprignitz-Ruppin", "Ostprignitz-Ruppin", "Kreis", 75, 85.71, True,
     "Ein kurzes Pr\u00e4fix bei einem langen Namen bewegt den Score kaum \u2014 Fuzzy-Toleranz allein reicht aus.",
     "A short prefix on a long name barely moves the score \u2014 fuzzy tolerance alone is enough."),
    ("Landkreis Havelland", "Havelland", "Kreis", 75, 64.29, False,
     "Dasselbe Pr\u00e4fix bei einem kurzen Namen zieht den Score unter die Schwelle \u2014 braucht erst den "
     "Pr\u00e4fix-Strip-Schritt (gestrippt: \u201eHavelland\u201c \u2192 100.00).",
     "The same kind of prefix on a short name drags the score under threshold \u2014 needs the "
     "prefix-strip step first (stripped: \u201eHavelland\u201c \u2192 100.00)."),
    ("sommerda", "S\u00f6mmerda", "Gemeinde", 82, 75.00, False,
     "Ein Transliterations-Tippfehler verfehlt die {level}-Schwelle knapp \u2014 gel\u00f6st \u00fcber die Alias-"
     "Liste, nicht durch eine niedrigere Schwelle.",
     "A transliteration typo just misses the {level} threshold \u2014 resolved via the alias "
     "list, not by loosening the threshold."),
    ("MVP", "Mecklenburg-Vorpommern", "Bundesland", 85, 16.00, False,
     "Ein Akronym teilt fast keine Zeichen mit dem vollen Namen \u2014 Fuzzy-Matching kann hier gar nicht "
     "helfen; die Alias-Liste ist der einzige Fix.",
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


def _mechanism_row(parts, y, lang):
    tt = lambda de, en: vu.t(lang, de, en)
    bw, gap = 340, 46
    total = 4 * bw + 3 * gap
    x0 = 60 + (1630 - total) / 2
    steps = [
        (tt("1 Tokenisieren", "1 Tokenise"), tt("String an Leerzeichen trennen", "split the string on whitespace")),
        (tt("2 Tokens sortieren", "2 Sort tokens"),
         tt("alphabetisch \u2014 Wortreihenfolge wird irrelevant", "alphabetical order \u2014 word order stops mattering")),
        (tt("3 Wieder zusammenf\u00fcgen", "3 Rejoin"),
         tt("die beiden sortierten Strings vergleichen", "compare the two sorted strings")),
        (tt("4 Score", "4 Score"), tt("Levenshtein-basiertes Verh\u00e4ltnis, 0\u2013100",
                                        "Levenshtein-based ratio, 0\u2013100")),
    ]
    xs = [x0 + i * (bw + gap) for i in range(4)]
    for x, (title, sub) in zip(xs, steps):
        parts.append(vu.svg_box(x, y, bw, 74, title, sub, fill=C["fill"], stroke=C["stroke"]))
    for i in range(3):
        parts.append(vu.svg_arrow(xs[i] + bw, y + 37, xs[i + 1], y + 37))
    return y + 74


def _gauge(parts, x, y, w, score, threshold, passed, threshold_label):
    """0-100 bar: filled track up to score, a tick + label at the threshold."""
    h = 26
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" '
                 f'fill="#f1efe8" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    fw = w * score / 100
    col = PASS_C["stroke"] if passed else vu.UNCERTAIN_STROKE
    bg = PASS_C["fill"] if passed else vu.UNCERTAIN_FILL
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{fw:.1f}" height="{h:.1f}" rx="6" '
                 f'fill="{bg}" stroke="{col}" stroke-width="1.4"/>')
    tx = x + w * threshold / 100
    parts.append(f'<line x1="{tx:.1f}" y1="{y - 6:.1f}" x2="{tx:.1f}" y2="{y + h + 6:.1f}" '
                 f'stroke="{vu.TEXT_DARK}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    parts.append(f'<text x="{tx:.1f}" y="{y - 12:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="11" fill="{vu.TEXT_DARK}">{threshold_label} {threshold}</text>')
    parts.append(f'<text x="{x + w + 14:.1f}" y="{y + h/2:.1f}" dominant-baseline="central" '
                 f'font-family="Fira Sans" font-weight="500" font-size="15" fill="{col}">'
                 f'{score:.2f}</text>')


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("How rapidfuzz.token_sort_ratio decides a Wikidata match, with real scores")]

    y_after_mech = _mechanism_row(parts, 60, lang)

    row_y0 = y_after_mech + 70
    pitch = 178
    csv_label = tt("CSV", "CSV")
    vs_label = tt("vs. Wikidata-Label", "vs. Wikidata label")
    threshold_label = tt("Schwelle", "threshold")
    pass_label = tt("BESTANDEN", "PASS")
    fail_label = tt("DURCHGEFALLEN", "FAIL")

    for i, (csv_val, wd_label, level_cls, threshold, score, passed, note_de, note_en) in enumerate(EXAMPLES):
        ry = row_y0 + i * pitch
        note = tt(note_de, note_en).format(level=vu.cls(level_cls, lang))
        level = vu.cls(level_cls, lang).upper()

        parts.append(f'<text x="60" y="{ry + 4:.1f}" font-family="Fira Sans" font-weight="500" '
                     f'font-size="14.5" fill="{vu.TEXT_DARK}">{csv_label} \u201e{vu.xml_escape(csv_val)}\u201c</text>')
        parts.append(f'<text x="60" y="{ry + 26:.1f}" font-family="Fira Sans" font-size="13" '
                     f'fill="{vu.TEXT_MUTED}">{vs_label} \u201e{vu.xml_escape(wd_label)}\u201c</text>')
        badge_w = max(86, vu.text_width(level, 11) + 24)
        parts.append(f'<rect x="60" y="{ry + 40:.1f}" width="{badge_w:.1f}" height="24" rx="12" '
                     f'fill="#ece9e2" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
        parts.append(f'<text x="{60 + badge_w/2:.1f}" y="{ry + 52:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-size="11" '
                     f'fill="{vu.TEXT_DARK}">{level}</text>')

        _gauge(parts, 470, ry + 6, 560, score, threshold, passed, threshold_label)

        col = PASS_C["stroke"] if passed else vu.UNCERTAIN_STROKE
        bg = PASS_C["fill"] if passed else vu.UNCERTAIN_FILL
        label = pass_label if passed else fail_label
        badge2_w = max(86, vu.text_width(label, 13) + 26)
        badge_x = 1150
        parts.append(f'<rect x="{badge_x:.1f}" y="{ry - 4:.1f}" width="{badge2_w:.1f}" height="30" rx="15" '
                     f'fill="{bg}" stroke="{col}" stroke-width="1.6"/>')
        parts.append(f'<text x="{badge_x + badge2_w/2:.1f}" y="{ry + 11:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" '
                     f'font-size="13" fill="{col}">{label}</text>')

        note_lines = _wrap(note, 50)
        for j, ln in enumerate(note_lines):
            parts.append(f'<text x="1300" y="{ry + 2 + j * 19:.1f}" font-family="Fira Sans" '
                         f'font-size="12.5" fill="{vu.TEXT_DARK}">{vu.xml_escape(ln)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"fuzzy-matching.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

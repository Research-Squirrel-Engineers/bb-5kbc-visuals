#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_16_persistent_uris.py -- what happens when a bb5kbc: URI is dereferenced
===================================================================================

Source: the two-rule ``.htaccess`` configuration behind
``http://w3id.org/bb5kbc/``: ontology terms
(``http://w3id.org/bb5kbc/ont/...``) redirect (303 See Other) to a
fragment anchor on the single ontology HTML page; data resources
(``http://w3id.org/bb5kbc/site_*``) redirect to an individually
generated ``index.html`` page per resource. Both rules use Apache's
``[NE]`` (noescape) rewrite flag, kept here as the one implementation
detail worth naming rather than glossed over.

Bilingual (revision) -- see step_00 docstring for the convention. URIs,
file paths and the HTTP status line are literal and never translated.

Writes: persistent-uris.de.svg/.png, persistent-uris.en.svg/.png
Run standalone: ``python py/step_16_persistent_uris.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["16-persistent-uris"]
SITE = vu.SITE
ARTEFACT = vu.PIPELINE_COLORS["artefact"]


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("What happens when a w3id.org/bb5kbc URI is dereferenced")]

    intro = tt("w3id.org ist ein Redirect-Dienst: zwei Regeln in der .htaccess entscheiden, wohin eine bb5kbc-URI zeigt.",
               "w3id.org is a redirect service: two rules in the .htaccess decide where a bb5kbc URI points.")
    parts.append(f'<text x="60" y="60" font-family="Fira Sans" font-size="15.5" '
                 f'fill="{vu.TEXT_DARK}">{vu.xml_escape(intro)}</text>')

    def panel(x, w, title, uri, target, note_lines):
        py = 120
        ph = 700
        parts.append(vu.svg_dashed_container(x, py, w, ph, title))
        ux = x + 40
        uw = w - 80
        parts.append(vu.svg_box(ux, py + 60, uw, 90, uri, "", fill=SITE["fill"], stroke=SITE["stroke"], stroke_width=2.0))
        parts.append(vu.svg_arrow_labeled(ux + uw / 2, py + 150, ux + uw / 2, py + 280,
                                           "303 See Other", font_size=13))
        nx2 = tt("[NE]-Flag: verhindert doppeltes URL-Escaping beim Rewrite",
                 "[NE] flag: prevents double URL-escaping during rewrite")
        parts.append(f'<text x="{ux:.1f}" y="{py + 220:.1f}" font-family="Fira Sans" font-size="11" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(nx2)}</text>')
        parts.append(vu.svg_box(ux, py + 280, uw, 100, target, "", fill=ARTEFACT["fill"], stroke=ARTEFACT["stroke"]))
        ny = py + 420
        for line in note_lines:
            parts.append(f'<text x="{ux:.1f}" y="{ny:.1f}" font-family="Fira Sans" font-size="13" '
                         f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
            ny += 24

    left_note = tt(
        ["Ein einziges HTML-Dokument f\u00fcr die", "gesamte Ontologie \u2014 jeder Begriff", "ist ein Fragment-Anker darin."],
        ["One single HTML document for the", "whole ontology \u2014 every term is", "a fragment anchor within it."])
    panel(60, 780, tt("Ontologie-Begriffe (http://w3id.org/bb5kbc/ont/...)",
                       "Ontology terms (http://w3id.org/bb5kbc/ont/...)"),
          "http://w3id.org/bb5kbc/ont/Fundstelle",
          ".../ontology/index.html#Fundstelle", left_note)

    right_note = tt(
        ["Jede Fundstelle bekommt eine", "eigene, generierte Seite \u2014", "540 individuelle index.html-Dateien."],
        ["Every Fundstelle gets its own,", "generated page \u2014", "540 individual index.html files."])
    panel(910, 780, tt("Daten-Ressourcen (http://w3id.org/bb5kbc/site_*)",
                        "Data resources (http://w3id.org/bb5kbc/site_*)"),
          "http://w3id.org/bb5kbc/site_142",
          ".../site_142/index.html", right_note)

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"persistent-uris.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

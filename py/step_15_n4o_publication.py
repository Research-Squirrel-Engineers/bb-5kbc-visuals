#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_15_n4o_publication.py -- from hand-maintained metadata to the N4O KG
==============================================================================

Source: ``bb-5kbc-public`` README (fetched directly, not paraphrased from
memory): one hand-maintained file (``metadata.yaml``), everything else
generated on every push by ``n4o-kg-profile`` pinned to ``@v1``. Real
numbers from that README: 28,531 triples / 33 classes / 81 properties;
CRM alignment anchors 16 of the bundle's 21 domain classes (measured, not
restated); byte-reproducible build; SHA-256 per distribution recorded in
``dist/metadata.ttl`` as the only statement that later proves which
version was loaded.

Bilingual (revision) -- see step_00 docstring for the convention. File
and output names are real artefact names and are never translated.

Writes: n4o-publication.de.svg/.png, n4o-publication.en.svg/.png
Run standalone: ``python py/step_15_n4o_publication.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["15-n4o-publication"]
INPUT = vu.PIPELINE_COLORS["input"]
LOD = vu.PIPELINE_COLORS["lod"]
ARTEFACT = vu.PIPELINE_COLORS["artefact"]
VALIDATE = vu.PIPELINE_COLORS["validate"]
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("From hand-maintained metadata.yaml to the NFDI4Objects Knowledge Graph")]

    # -- left: the one hand-maintained input ------------------------------------
    mx, my, mw, mh = 90, 380, 260, 100
    parts.append(vu.svg_box(mx, my, mw, mh, "metadata.yaml", tt("einzige Handarbeit", "the only hand-maintained file"),
                             fill=INPUT["fill"], stroke=INPUT["stroke"], stroke_width=2.0))
    bundle_y = my - 160
    parts.append(vu.svg_box(mx, bundle_y, mw, 90, "bb5kbc-bundle.ttl", tt("einmal geholt, hier archiviert",
                                                                            "fetched once, archived here"),
                             fill=INPUT["fill"], stroke=INPUT["stroke"]))
    # -- middle: the generated build (n4o-kg-profile @v1) ------------------------
    px, pw = 460, 380
    parts.append(vu.svg_dashed_container(px - 20, 60, pw + 40, 780,
                                          tt("n4o-kg-profile @v1 (generiert bei jedem Push)",
                                             "n4o-kg-profile @v1 (regenerated on every push)")))
    outs = [
        ("dist/n4o-collection.ttl", tt("Registrierungsdatensatz f\u00fcr N4O", "the registration record N4O reads")),
        ("dist/metadata.ttl", tt("DCAT + VoID-Statistik + CRM-Alignment", "DCAT + VoID stats + CRM alignment")),
        ("dist/metadata.jsonld", tt("dasselbe als JSON-LD", "the same, as JSON-LD")),
        ("dist/crm-alignment.ttl", tt("rdfs:subClassOf zu CIDOC CRM, einzeln ladbar",
                                        "rdfs:subClassOf to CIDOC CRM, loadable alone")),
    ]
    oy = 100
    rail_x = mx + mw + 60
    for name, desc in outs:
        parts.append(vu.svg_box(px, oy, pw, 76, name, desc, fill=LOD["fill"], stroke=LOD["stroke"]))
        parts.append(vu.svg_arrow_elbow_v(mx + mw, my + mh / 2, px, oy + 38, rail_x))
        oy += 100

    # bb5kbc-bundle.ttl feeds the same build -- lands on the first output
    # row (dist/n4o-collection.ttl), on the same rail so it reads as part
    # of the same bus rather than a second, crossing fan.
    parts.append(vu.svg_arrow_elbow_v(mx + mw, bundle_y + 45, px, 100 + 38, rail_x + 20))

    docs_y = oy + 10
    parts.append(vu.svg_box(px, docs_y, pw, 76, "docs/", tt("GitHub Pages: Landing-Page, Query-Seite, .rq-Dateien",
                                                              "GitHub Pages: landing page, query page, .rq files"),
                             fill=LOD["fill"], stroke=LOD["stroke"]))

    checks_y = docs_y + 110
    checks_h = 160
    parts.append(f'<rect x="{px:.1f}" y="{checks_y:.1f}" width="{pw:.1f}" height="{checks_h}" rx="10" '
                 f'fill="{VALIDATE["fill"]}" stroke="{VALIDATE["stroke"]}" stroke-width="1.4"/>')
    checks_title = tt("Was der Build pr\u00fcft", "What the build checks")
    parts.append(f'<text x="{px + pw/2:.1f}" y="{checks_y + 28:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="14" fill="{vu.TEXT_DARK}">{vu.xml_escape(checks_title)}</text>')
    check_lines = tt(
        ["SHACL: Titel, Publikations-URL, Wikidata-Item, Lizenz + NCMDP",
         "Jede der 12 Beispiel-Queries liefert Zeilen (0 Zeilen = Build-Fehler)",
         "Byte-Reproduzierbarkeit: zweiter Lauf = identische Dateien",
         "SHA-256 je Distribution in dist/metadata.ttl"],
        ["SHACL: title, publication URL, Wikidata item, licence + NCMDP",
         "Every one of the 12 example queries returns rows (0 rows = build fails)",
         "Byte reproducibility: a second run = identical files",
         "SHA-256 per distribution, recorded in dist/metadata.ttl"])
    cy = checks_y + 54
    for line in check_lines:
        bullet_line = vu.xml_escape("\u2022 " + line)
        parts.append(f'<text x="{px + 20:.1f}" y="{cy:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_DARK}">{bullet_line}</text>')
        cy += 27

    # -- right: outcome numbers + N4O KG ----------------------------------------
    rx, rw = 940, 350
    stats_h = 150
    parts.append(f'<rect x="{rx:.1f}" y="100" width="{rw:.1f}" height="{stats_h}" rx="10" '
                 f'fill="{ARTEFACT["fill"]}" stroke="{ARTEFACT["stroke"]}" stroke-width="2.0"/>')
    stats_title = tt("Der Graph, in Zahlen", "The graph, in numbers")
    parts.append(f'<text x="{rx + rw/2:.1f}" y="135" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="15" fill="{vu.TEXT_MUTED}">{vu.xml_escape(stats_title)}</text>')
    stat_lines = ["28 531 " + tt("Tripel", "triples"), "33 " + tt("Klassen", "classes"),
                  "81 " + tt("Properties", "properties")]
    sy = 168
    for line in stat_lines:
        parts.append(f'<text x="{rx + rw/2:.1f}" y="{sy:.1f}" text-anchor="middle" font-family="Fira Sans" '
                     f'font-weight="500" font-size="17" fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        sy += 28

    crm_note = tt("CRM-Alignment verankert 16 von 21 Domain-Klassen \u2014 gemessen aus dem Bundle, nicht in "
                  "metadata.yaml restatiert.",
                  "CRM alignment anchors 16 of 21 domain classes \u2014 measured from the bundle, not restated in metadata.yaml.")
    words = crm_note.split()
    lines = []
    cur = []
    curlen = 0
    for w in words:
        if curlen + len(w) + 1 > 44:
            lines.append(" ".join(cur))
            cur = []
            curlen = 0
        cur.append(w)
        curlen += len(w) + 1
    if cur:
        lines.append(" ".join(cur))
    cny = 270
    for line in lines:
        parts.append(f'<text x="{rx:.1f}" y="{cny:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        cny += 20

    # freshness check
    fy = cny + 40
    parts.append(vu.svg_dashed_container(rx, fy, rw, 160,
                                          tt("Freshness-Check", "Freshness check")))
    fresh_lines = tt(
        ["SHA-256-Pr\u00fcfsumme des Bundles warnt,",
         "wenn sich das Bundle \u00e4ndert, aber",
         "modified:/version: in metadata.yaml",
         "nicht mitgezogen wurde."],
        ["A SHA-256 checksum on the bundle warns",
         "when the bundle changes but",
         "modified:/version: in metadata.yaml",
         "wasn't bumped along with it."])
    fny = fy + 40
    for line in fresh_lines:
        parts.append(f'<text x="{rx + 16:.1f}" y="{fny:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        fny += 22

    n4o_y = 660
    parts.append(vu.svg_box(rx, n4o_y, rw, 100, tt("NFDI4Objects Knowledge Graph", "NFDI4Objects Knowledge Graph"),
                             "graph.nfdi4objects.net", fill=vu.SITE["fill"], stroke=vu.SITE["stroke"], stroke_width=2.0))
    parts.append(vu.svg_arrow(px + pw, checks_y + 70, rx, n4o_y + 50))
    parts.append(vu.svg_arrow(rx + rw / 2, fy + 160, rx + rw / 2, n4o_y))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"n4o-publication.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

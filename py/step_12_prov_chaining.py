#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_12_prov_chaining.py -- one Activity per run, chained across two stages
================================================================================

Source: paper section 6 ("PROV-O-Verkettung ueber zwei Pipeline-Stufen").
At start-up the LOD stage looks for ``csv_enrichment_run.ttl`` in its
input directory; if found, it parses the manifest, identifies the
top-level Activity in it (the one with no outgoing ``prov:wasInformedBy``
edge), and links its own new Activity to that one -- across the
namespace boundary between ``https://example.org/bb-5kbc-sites/``
(enrichment stage) and ``http://w3id.org/bb5kbc/`` (LOD stage). All
~90 triples of the upstream manifest are physically embedded into the
LOD graph, so a consumer of either output file sees the complete
provenance chain in one graph. If no manifest is found, the script still
writes its own PROV-Activity, just without the link (standalone mode).

Bilingual (revision) -- see step_00 docstring for the convention.

Writes: prov-chaining.de.svg/.png, prov-chaining.en.svg/.png
Run standalone: ``python py/step_12_prov_chaining.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["12-prov-chaining"]
PROV = vu.PIPELINE_COLORS["prov"]
LOD = vu.PIPELINE_COLORS["lod"]
ARTEFACT = vu.PIPELINE_COLORS["artefact"]
AUTH = vu.WORLD_COLORS["authority"]
NEUTRAL = {"fill": "#f1efe8", "stroke": vu.LINE_NEUTRAL}


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("PROV-O chaining: one Activity per run, linked across two pipeline stages")]

    # -- namespace containers ---------------------------------------------------
    lx, lw = 60, 480
    rx, rw = 580, 1110
    parts.append(vu.svg_dashed_container(lx, 50, lw, 850,
                                          tt("Namespace https://example.org/bb-5kbc-sites/ (Anreicherungs-Stufe)",
                                             "Namespace https://example.org/bb-5kbc-sites/ (enrichment stage)")))
    parts.append(vu.svg_dashed_container(rx, 50, rw, 850,
                                          tt("Namespace http://w3id.org/bb5kbc/ (LOD-Stufe)",
                                             "Namespace http://w3id.org/bb5kbc/ (LOD stage)")))

    # -- left: upstream manifest -------------------------------------------------
    mx, mw = lx + 40, lw - 80
    parts.append(vu.svg_box(mx, 130, mw, 90, "csv_enrichment_run.ttl", tt("~90 Tripel", "~90 triples"),
                             fill=PROV["fill"], stroke=PROV["stroke"]))
    top_level = (mx, 320)
    parts.append(vu.svg_box(*top_level, mw, 100, tt("Top-Level-Activity", "top-level Activity"),
                             tt("z. B. stage_literature", "e.g. stage_literature"),
                             fill=PROV["fill"], stroke=PROV["stroke"], dashed=True))
    parts.append(vu.svg_arrow(mx + mw / 2, 220, mx + mw / 2, 320))
    badge_text = tt("keine ausgehende wasInformedBy-Kante", "no outgoing wasInformedBy edge")
    parts.append(f'<text x="{mx:.1f}" y="{320 + 122:.1f}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(badge_text)}</text>')

    note_lines = tt(
        ["Die LOD-Stufe sucht diese Datei im Eingabeverzeichnis,",
         "parst sie und identifiziert darin die Top-Level-Activity."],
        ["The LOD stage looks for this file in its input directory,",
         "parses it and identifies the top-level Activity within it."])
    ny = 500
    for line in note_lines:
        parts.append(f'<text x="{mx:.1f}" y="{ny:.1f}" font-family="Fira Sans" font-size="13" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        ny += 22

    parts.append(vu.svg_dashed_container(mx, 620, mw, 100, ""))
    fallback_lines = tt(
        ["Kein Manifest gefunden \u2192 Standalone-Modus:", "eigene Activity, keine Verkettung."],
        ["No manifest found \u2192 standalone mode:", "own Activity, no chaining."])
    for i, line in enumerate(fallback_lines):
        parts.append(f'<text x="{mx + 16:.1f}" y="{658 + i * 20:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')

    # -- right: the LOD Activity hub ---------------------------------------------
    acy = 470
    aw, ah = 420, 110
    ax = 760
    ay = acy - ah / 2
    acx = ax + aw / 2
    parts.append(vu.svg_box(ax, ay, aw, ah, "pipeline_run_2026-04-27T09-22-28Z",
                             tt("\u00abprov:Activity\u00bb \u00b7 eine Activity pro Lauf, nicht pro Zeile",
                                "\u00abprov:Activity\u00bb \u00b7 one Activity per run, not per row"),
                             fill=LOD["fill"], stroke=LOD["stroke"], stroke_width=2.0))

    # spoke: wasInformedBy across the namespace boundary
    parts.append(vu.svg_arrow_labeled(ax, acy - 10, top_level[0] + mw, top_level[1] + 40,
                                       "wasInformedBy", dashed=True, stroke=PROV["stroke"], font_size=12))

    # spoke: inputs (used)
    inputs_box = (ax, 130)
    parts.append(vu.svg_box(*inputs_box, aw, 78, tt("Eingaben (prov:used)", "Inputs (prov:used)"),
                             "fst_wgs84.csv + bb5kbc-ontology.ttl (file://)", fill=NEUTRAL["fill"], stroke=NEUTRAL["stroke"]))
    parts.append(vu.svg_arrow(acx, ay, acx, inputs_box[1] + 78))

    # spoke: agents (wasAssociatedWith)
    agents_box = (ax + aw + 60, acy - 45)
    agents_w = 320
    parts.append(vu.svg_box(*agents_box, agents_w, 90, tt("Agents (wasAssociatedWith)", "Agents (wasAssociatedWith)"),
                             tt("2 \u00d7 ORCID (Autor:innen) + Software-Agent", "2 \u00d7 ORCID (authors) + software agent"),
                             fill=AUTH["fill"], stroke=AUTH["stroke"]))
    parts.append(vu.svg_arrow(ax + aw, acy, agents_box[0], agents_box[1] + 45))

    # spokes: outputs (wasGeneratedBy), each also wasDerivedFrom the CSV input
    data_ttl = (630, 660)
    bundle_ttl = (1060, 660)
    dw2 = 380
    parts.append(vu.svg_box(data_ttl[0], data_ttl[1], dw2, 78, "bb5kbc-data.ttl", "~21 700 triples",
                             fill=ARTEFACT["fill"], stroke=ARTEFACT["stroke"]))
    parts.append(vu.svg_box(bundle_ttl[0], bundle_ttl[1], dw2, 78, "bb5kbc-bundle.ttl", "~22 400 triples",
                             fill=ARTEFACT["fill"], stroke=ARTEFACT["stroke"]))
    parts.append(vu.svg_arrow_labeled(ax + 100, ay + ah, data_ttl[0] + dw2 / 2, data_ttl[1],
                                       "wasGeneratedBy", font_size=11))
    parts.append(vu.svg_arrow(ax + aw - 100, ay + ah, bundle_ttl[0] + dw2 / 2, bundle_ttl[1]))
    derived_note = tt("beide: wasDerivedFrom \u2192 fst_wgs84.csv (Pfeil weggelassen, um Kreuzungen zu vermeiden)",
                       "both: wasDerivedFrom \u2192 fst_wgs84.csv (arrow omitted to avoid crossing other lines)")
    parts.append(f'<text x="{data_ttl[0]:.1f}" y="{660 + 78 + 28:.1f}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(derived_note)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"prov-chaining.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

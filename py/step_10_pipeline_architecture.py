#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_10_pipeline_architecture.py -- the whole pipeline, end to end
=======================================================================

Source: ``data/raw/bb-5kbc-sites/architecture.mmd`` -- every node, edge
and colour class below is taken directly from that file (the published
Fig. 4 of the paper), redrawn in the bb5kbc-visuals house style rather
than Mermaid's. The ``PIPELINE_COLORS`` palette in the utils module was
already lifted from this file's own ``classDef`` block, so the colours
match the paper's figure exactly, not just approximately.

Bilingual (revision) -- see step_00 docstring for the convention. File,
script and column-count labels (fst_wgs84.csv, 540 rows x 65 cols, ...)
are real artefact names/counts and are never translated.

**Revision 2026-09-15:** most connectors in this figure were still
diagonal (only two had been fixed in an earlier pass). All now
orthogonal -- house rule, PRIMER.md A3. Several routes go through a
rail in whichever gap is clear of other boxes rather than landing
straight on a crowded column (see ``svg_arrow_elbow_v``'s docstring).

Writes: pipeline-architecture.de.svg/.png, pipeline-architecture.en.svg/.png
Run standalone: ``python py/step_10_pipeline_architecture.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["10-pipeline-architecture"]
P = vu.PIPELINE_COLORS


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("The full BB-5KBC pipeline: enrichment, LOD transformation, validation")]

    def box(x, y, w, h, title, sub, kind, **kw):
        c = P[kind]
        return vu.svg_box(x, y, w, h, title, sub, fill=c["fill"], stroke=c["stroke"], **kw)

    # -- Stage A: inputs ---------------------------------------------------
    ax, aw, ah = 90, 220, 78
    a_ys = [70, 290, 510, 730]
    csv_in = (ax, a_ys[0])
    ref_in = (ax, a_ys[1])
    onto = (ax, a_ys[2])
    map_md = (ax, a_ys[3])
    parts.append(box(*csv_in, aw, ah, "fst_wgs84_comma.csv", "540 rows \u00d7 32 cols", "input"))
    parts.append(box(*ref_in, aw, ah, "fst_standortanalysen", "_ref.csv", "input"))
    parts.append(box(*onto, aw, ah, "bb5kbc-ontology.ttl", tt("15 Klassen", "15 classes"), "input"))
    parts.append(box(*map_md, aw, ah, "csv-mapping.md", tt("(Vorfahren-Tabelle)", "(ancestor table)"), "input"))

    # -- Stage B: CSV enrichment -------------------------------------------
    bx, bw = 400, 250
    parts.append(vu.svg_dashed_container(bx - 20, 55, bw + 40, 660,
                                          tt("CSV-Anreicherung", "CSV enrichment")))
    sh = 78
    s1 = (bx, 140)
    s2 = (bx, 580)
    s3 = (bx, 360)
    parts.append(box(*s1, bw, sh, "Stage 1: enrich_qids.py", tt("Literatur-Mappings (46+34 QIDs)",
                                                                  "literature mappings (46+34 QIDs)"), "enrich"))
    parts.append(box(*s2, bw, sh, "Stage 2: wikidata_map.py", tt("SPARQL Fuzzy-Match LAND/BL/KR/GE",
                                                                   "SPARQL fuzzy match LAND/BL/KR/GE"), "enrich"))
    parts.append(box(*s3, bw, sh, "Stage 3: enrich_fst.py", tt("Merge auf FID", "merge on FID"), "enrich"))
    parts.append(vu.svg_arrow_L(csv_in[0] + aw, csv_in[1] + ah / 2, s1[0], s1[1] + sh / 2, bend="h"))
    parts.append(vu.svg_arrow_elbow_v(ref_in[0] + aw, ref_in[1] + ah / 2, s2[0], s2[1] + sh / 2, 350))
    parts.append(vu.svg_arrow_L(s1[0] + bw / 2, s1[1] + sh, s3[0] + bw / 2 - 30, s3[1], bend="h"))
    parts.append(vu.svg_arrow_L(s2[0] + bw / 2, s2[1], s3[0] + bw / 2 + 30, s3[1] + sh, bend="h"))

    # -- Stage C: merged CSV artefact + PROV --------------------------------
    cx, cw, csh = 720, 190, 78
    csv_final = (cx, 360)
    parts.append(box(*csv_final, cw, csh, "fst_wgs84.csv", "540 \u00d7 65 cols", "artefact"))
    parts.append(vu.svg_arrow(s3[0] + bw, s3[1] + sh / 2, cx, csv_final[1] + csh / 2))
    prov_enrich = (cx - 10, 560)
    parts.append(box(*prov_enrich, cw + 20, 56, "csv_enrichment_run.ttl", "", "prov"))
    parts.append(vu.svg_arrow(cx + cw / 2, csv_final[1] + csh, prov_enrich[0] + (cw + 20) / 2, prov_enrich[1],
                               dashed=True, stroke=P["prov"]["stroke"]))

    # -- Stage D: LOD transformation -----------------------------------------
    dx, dw = 990, 250
    parts.append(vu.svg_dashed_container(dx - 20, 55, dw + 40, 660,
                                          tt("LOD-Transformation", "LOD transformation")))
    build_ = (dx, 300)
    shapes = (dx, 460)
    shacl_val = (dx, 620)
    parts.append(box(*build_, dw, sh, "bb5kbc_lod_pipeline.py", tt("12 Builder \u00d7 540 Zeilen",
                                                                     "12 builders \u00d7 540 rows"), "lod"))
    parts.append(box(*shapes, dw, sh, tt("SHACL-Shapes-Generierung", "SHACL shape generation"),
                      tt("aus der Ontologie", "from the ontology"), "lod"))
    parts.append(box(*shacl_val, dw, sh, "pyshacl.validate()", "", "lod"))
    parts.append(vu.svg_arrow_L(csv_final[0] + cw, csv_final[1] + csh / 2 - 10, dx, build_[1] + sh / 2 - 10, bend="h"))
    parts.append(vu.svg_arrow_elbow_v(onto[0] + aw, onto[1] + ah / 2, dx, build_[1] + sh / 2 + 10, 950))
    parts.append(vu.svg_arrow_elbow_v(prov_enrich[0] + (cw + 20), prov_enrich[1] + 28, dx, build_[1] + sh - 10, 960,
                                       dashed=True, stroke=P["prov"]["stroke"]))
    parts.append(vu.svg_arrow(build_[0] + dw / 2, build_[1] + sh, shapes[0] + dw / 2, shapes[1]))
    parts.append(vu.svg_arrow(shapes[0] + dw / 2, shapes[1] + sh, shacl_val[0] + dw / 2, shacl_val[1]))

    # -- Stage E: LOD artefacts + PROV ---------------------------------------
    ex, ew = 1280, 210
    data_ttl = (ex, 70)
    bundle_ttl = (ex, 220)
    shacl_rep = (ex, 480)
    prov_lod = (ex, 630)
    eh = 78
    parts.append(box(*data_ttl, ew, eh, "bb5kbc-data.ttl", "~21 700 triples", "artefact"))
    parts.append(box(*bundle_ttl, ew, eh, "bb5kbc-bundle.ttl", "~22 400 triples", "artefact"))
    parts.append(box(*shacl_rep, ew, eh, "shacl-report.ttl", "+ shacl-report-bundle.ttl", "artefact"))
    parts.append(box(*prov_lod, ew, 56, "csv_to_lod_run.ttl", "", "prov"))
    parts.append(vu.svg_arrow_L(build_[0] + dw, build_[1] + sh / 2 - 6, ex, data_ttl[1] + eh - 10, bend="v"))
    parts.append(vu.svg_arrow_L(build_[0] + dw, build_[1] + sh / 2 + 6, ex, bundle_ttl[1] + eh / 2, bend="v"))
    parts.append(vu.svg_arrow_L(build_[0] + dw, build_[1] + sh / 2 + 20, ex, prov_lod[1] + 10, bend="v",
                                 dashed=True, stroke=P["prov"]["stroke"]))
    parts.append(vu.svg_arrow_L(shacl_val[0] + dw, shacl_val[1] + sh / 2, ex, shacl_rep[1] + eh / 2, bend="v"))

    # -- Stage F: validation + report -----------------------------------------
    fx, fw = 1560, 150
    val = (fx, 400)
    report = (fx, 620)
    vh = 96
    parts.append(box(*val, fw, vh, "validate_lod.py", tt("4 + 1 Sektionen", "4 + 1 sections"), "validate"))
    parts.append(box(*report, fw, eh, "validation_report.md", "", "artefact"))
    parts.append(vu.svg_arrow_elbow_v(data_ttl[0] + ew, data_ttl[1] + eh / 2, fx, val[1] + 15, 1510))
    parts.append(vu.svg_arrow_elbow_v(bundle_ttl[0] + ew, bundle_ttl[1] + eh / 2, fx, val[1] + 35, 1520))
    parts.append(vu.svg_arrow_elbow_v(shacl_rep[0] + ew, shacl_rep[1] + eh / 2, fx, val[1] + 55, 1530))
    parts.append(vu.svg_arrow_elbow_v(csv_final[0] + cw, csv_final[1] + csh / 2 + 10, fx, val[1] + 75, 1545))
    parts.append(vu.svg_arrow_elbow(map_md[0] + aw / 2, map_md[1] + ah, fx + 40, val[1] + vh, 808))
    parts.append(vu.svg_arrow(val[0] + fw / 2, val[1] + vh, report[0] + fw / 2, report[1]))

    # -- legend -----------------------------------------------------------------
    legend_items = [
        (tt("Eingabe", "input"), P["input"]),
        (tt("Anreicherung", "enrichment"), P["enrich"]),
        (tt("LOD-Transformation", "LOD transformation"), P["lod"]),
        (tt("Validierung", "validation"), P["validate"]),
        (tt("Artefakt", "artefact"), P["artefact"]),
        (tt("PROV (gestrichelt)", "PROV (dashed)"), P["prov"]),
    ]
    parts.append(vu.svg_legend(60, 900, legend_items, columns=6, col_w=270))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"pipeline-architecture.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

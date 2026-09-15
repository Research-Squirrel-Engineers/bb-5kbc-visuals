#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_09_kulturen.py -- how Kulturgruppe itself is modelled
=================================================================

Source: ``modelling-rules.md`` Regel 2/3 (dedup hash nodes, one node per
distinct CSV string) and the URI-convention table (``kultur_{hash}``);
``bb5kbc-classes.mmd`` for the ``crm:E4_Period`` stereotype and the two
attributes (``rdfs:label``, ``bb5kbc:hasExternalIdentifier``). This is a
structural/modelling figure, not a statistics chart: the one real number
it carries (9 distinct values across the 540-row CSV) is a single
grounding fact, not the figure's subject.

**Revision 2026-09-11 (correction):** the fan-in example originally used
placeholder FIDs (site_12/57/101/205, none of them actually FBG) and a
placeholder hash (``kultur_a1b2c3d4``, not a real MD5 digest). Fixed
against ``fst_wgs84_lit_enriched.csv``: FBG has exactly 14 real members
(FIDs 32, 33, 61, 77, 278, 504-508, 510, 563-565), four of which are now
shown by their real FID; the hash is the real
``hashlib.md5("FBG")[:8] == "a36e9d6d"``, verified the same way step_08's
SBK hash was.

Bilingual (revision 2026-09-10c) -- see step_00 docstring for the
translation convention. "FBG"/"SBK"/"SBK?" are real culture values,
never translated.

**Revision 2026-09-15:** the four fan-in arrows and the SBK/SBK? -> wd
convergence were diagonal; now orthogonal (house rule, PRIMER.md A3).
The four fan-in arrows land on four distinct points on the circle so
they keep their own arrowheads; the two-way convergence uses a shared
final hop with a single arrowhead, same pattern as step_05.

Writes: kulturen.de.svg/.png, kulturen.en.svg/.png
Run standalone: ``python py/step_09_kulturen.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["09-kulturen"]
CULTURE = {"fill": "#eef0d6", "stroke": "#6b7a1f"}
SITE = vu.SITE
AUTH = vu.WORLD_COLORS["authority"]
U_STROKE = vu.UNCERTAIN_STROKE
U_FILL = vu.UNCERTAIN_FILL


def _uml_box(x, y, w, h, title, subtitle):
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" '
             f'fill="{CULTURE["fill"]}" stroke="{CULTURE["stroke"]}" stroke-width="1.8"/>']
    cx = x + w / 2
    sy = y + 34
    parts.append(f'<text x="{cx:.1f}" y="{sy:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12" font-style="italic" fill="{vu.TEXT_DARK}" opacity="0.75">'
                 f'\u00abcrm:E4_Period\u00bb</text>')
    ty = sy + 30
    parts.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="22" fill="{vu.TEXT_DARK}">{vu.xml_escape(title)}</text>')
    parts.append(f'<text x="{cx:.1f}" y="{ty + 23:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="13.5" fill="{vu.TEXT_MUTED}">{vu.xml_escape(subtitle)}</text>')
    divider_y = ty + 42
    parts.append(f'<line x1="{x:.1f}" y1="{divider_y:.1f}" x2="{x + w:.1f}" y2="{divider_y:.1f}" '
                 f'stroke="{CULTURE["stroke"]}" stroke-width="1.2"/>')
    rows = [
        ("rdfs:label", "xsd:string @de", "\u201eFBG\u201c"),
        ("bb5kbc:hasExternalIdentifier", "URI", "wd:Q<Wikidata item>"),
    ]
    ry = divider_y + 42
    for label, typ, example in rows:
        parts.append(f'<text x="{x + 30:.1f}" y="{ry:.1f}" font-family="Fira Sans" font-size="15" '
                     f'font-weight="500" fill="{vu.TEXT_DARK}">{vu.xml_escape(label)}</text>')
        parts.append(f'<text x="{x + 30:.1f}" y="{ry + 20:.1f}" font-family="Fira Sans" font-size="12.5" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(typ)} = {vu.xml_escape(example)}</text>')
        ry += 68
    return "\n".join(parts)


def build(lang: str = "en") -> list[str]:
    c = lambda n: vu.cls(n, lang)
    tt = lambda de, en: vu.t(lang, de, en)
    shared = tt("geteilt", "shared")

    parts = [vu.svg_open("How Kulturgruppe itself is modelled: a shared crm:E4_Period concept node")]

    # -- left: UML attribute box -----------------------------------------------
    ux, uy, uw, uh = 90, 60, 580, 380
    parts.append(_uml_box(ux, uy, uw, uh, c("Kulturgruppe"),
                           f"kultur_{{hash}} \u00b7 {shared} / {tt('dedupliziert', 'deduplicated')}"))

    # -- right: how the node comes to exist -------------------------------------
    nx, ny, nw, nh = 710, 60, 880, 380
    parts.append(vu.svg_dashed_container(nx, ny, nw, nh,
                                          tt(f"Wie ein {c('Kulturgruppe')}-Knoten entsteht",
                                             f"How a {c('Kulturgruppe')} node is created")))
    para1 = tt(
        ["Jeder distinkte String in der kultur-Spalte der CSV wird zu",
         "genau einem Knoten. Der Hash in der URI sind die ersten 8 Zeichen eines",
         "MD5-Digests \u00fcber den Wert (UTF-8) \u2014 deterministisch, derselbe String",
         "f\u00fchrt immer zum selben Knoten, Umlaute kollidieren nie."],
        ["Every distinct string in the CSV's kultur column becomes exactly",
         "one node. The URI's hash is the first 8 characters of an MD5 digest over the",
         "value (UTF-8) \u2014 deterministic, so the same string always resolves to the",
         "same node, and umlauts never collide."])
    ty = ny + 54
    for line in para1:
        parts.append(f'<text x="{nx + 26:.1f}" y="{ty:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        ty += 22
    ty += 20
    parts.append(f'<line x1="{nx + 20:.1f}" y1="{ty:.1f}" x2="{nx + nw - 20:.1f}" y2="{ty:.1f}" '
                 f'stroke="#dedcd4" stroke-width="1"/>')
    ty += 34
    para2 = tt(
        ["Mit echten Daten unterlegt: in der 540-zeiligen fst_wgs84.csv nimmt die",
         f"kultur-Spalte 9 distinkte Werte an \u2014 9 {c('Kulturgruppe')}-Knoten tragen alle 540",
         f"{c('Fundstelle')}-zu-Kultur-Zuordnungen (per Counter() \u00fcber die Spalte verifiziert,",
         "nicht gesch\u00e4tzt)."],
        ["Grounded in the real data: across the 540-row fst_wgs84.csv, the kultur",
         f"column takes 9 distinct values \u2014 9 {c('Kulturgruppe')} nodes carry all 540",
         f"{c('Fundstelle')}-to-culture assignments (verified by Counter() over the column,",
         "not estimated)."])
    for line in para2:
        parts.append(f'<text x="{nx + 26:.1f}" y="{ty:.1f}" font-family="Fira Sans" font-size="13.5" '
                     f'fill="{vu.TEXT_DARK}">{vu.xml_escape(line)}</text>')
        ty += 22

    # -- bottom-left: fan-in from several Fundstelle rows -----------------------
    # FIDs 32, 33, 61, 77 are four of the 14 real FBG sites in
    # fst_wgs84_lit_enriched.csv (verified 2026-09-11); kultur_a36e9d6d is
    # the real hashlib.md5("FBG")[:8].
    kgcx, kg_cy, kg_r = 620, 680, 95
    parts.append(vu.svg_hash_node(kgcx, kg_cy, kg_r, "\u201eFBG\u201c", "kultur_a36e9d6d",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))

    chip_w, chip_h = 190, 50
    centers = [560, 650, 740, 830]
    labels = ["FID 32", "FID 33", "FID 61", "FID 77"]
    # four different points on the circle's left arc, evenly spread, so
    # each arrow lands on a distinct point -- no shared endpoint, so no
    # arrowhead collision, and each corner stays a single clean bend
    kg_targets = [kg_cy - 60, kg_cy - 20, kg_cy + 20, kg_cy + 60]
    for cy, lbl, kgt in zip(centers, labels, kg_targets):
        cy0 = cy - chip_h / 2
        parts.append(vu.svg_box(90, cy0, chip_w, chip_h, c("Fundstelle"), lbl,
                                 fill=SITE["fill"], stroke=SITE["stroke"]))
        parts.append(vu.svg_arrow_L(90 + chip_w, cy, kgcx - kg_r * 0.9, kgt, bend="h"))
    intro1 = tt(f"Jede {c('Fundstelle')} mit dieser Kultur h\u00e4ngt \u00fcber eine eigene",
                f"Every {c('Fundstelle')} with this culture links in via its own")
    intro2 = tt(f"{c('KulturelleZuordnung')} daran \u2014 alle laufen in diesem einen geteilten Knoten zusammen.",
                f"{c('KulturelleZuordnung')} \u2014 all of them fan in to this one shared node.")
    parts.append(f'<text x="90" y="{centers[0] - 70:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">{intro1}</text>')
    parts.append(f'<text x="90" y="{centers[0] - 50:.1f}" font-family="Fira Sans" font-size="13" '
                 f'fill="{vu.TEXT_MUTED}">{intro2}</text>')

    bx, by = kgcx + kg_r + 90, kg_cy
    parts.append(vu.svg_arrow(kgcx + kg_r, kg_cy, bx - 30, by))
    parts.append(vu.svg_authority_badge(bx, by, "wd", r=30, fill=AUTH["fill"], stroke=AUTH["stroke"]))
    one_qid_label = tt("eine Wikidata-QID", "one Wikidata QID")
    per_site_label = tt("f\u00fcr jede FBG-Fundstelle", "for every FBG site")
    parts.append(f'<text x="{bx:.1f}" y="{by + 60:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12.5" fill="{vu.TEXT_MUTED}">{one_qid_label}</text>')
    parts.append(f'<text x="{bx:.1f}" y="{by + 78:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-size="12.5" fill="{vu.TEXT_MUTED}">{per_site_label}</text>')

    # -- bottom-right: "?" variant reminder --------------------------------------
    rx, ry_, rw, rh = 1050, 480, 580, 420
    parts.append(vu.svg_dashed_container(rx, ry_, rw, rh,
                                          tt("Erinnerung \u2014 die \u201e?\u201c-Variante ist ein eigener Knoten, "
                                             "dieselbe QID",
                                             "Reminder \u2014 the \u201c?\u201d variant is a separate node, same QID")))
    n1cx, n1cy, nr = rx + 130, ry_ + 100, 55
    n2cx, n2cy = rx + 130, ry_ + 280
    parts.append(vu.svg_hash_node(n1cx, n1cy, nr, "\u201eSBK\u201c", "",
                                   fill=CULTURE["fill"], stroke=CULTURE["stroke"]))
    parts.append(vu.svg_hash_node(n2cx, n2cy, nr, "\u201eSBK?\u201c", "",
                                   fill=CULTURE["fill"], stroke=U_STROKE))
    bqx, bqy = rx + 360, (n1cy + n2cy) / 2
    parts.append(vu.svg_arrow_L(n1cx + nr, n1cy, bqx - 28 - 20, bqy, bend="h", marker=None))
    parts.append(vu.svg_arrow_L(n2cx + nr, n2cy, bqx - 28 - 20, bqy, bend="h", marker=None))
    parts.append(vu.svg_arrow(bqx - 28 - 20, bqy, bqx - 28, bqy))
    parts.append(vu.svg_authority_badge(bqx, bqy, "wd", r=28, fill=AUTH["fill"], stroke=AUTH["stroke"]))
    same_qid_note = tt("Dieselbe QID, aber ein eigener Knoten \u2014 weil \u201eSBK?\u201c die",
                        "Same QID, but a separate node \u2014 because \u201eSBK?\u201c carries the")
    same_qid_note2 = tt("Unsicherheits-Markierung fsl:certaintyDesc \u201euncertain\u201c@en tr\u00e4gt.",
                         "fsl:certaintyDesc \u201euncertain\u201c@en uncertainty marker.")
    parts.append(f'<text x="{rx + 26:.1f}" y="{ry_ + 360:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(same_qid_note)}</text>')
    parts.append(f'<text x="{rx + 26:.1f}" y="{ry_ + 382:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(same_qid_note2)}</text>')

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"kulturen.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

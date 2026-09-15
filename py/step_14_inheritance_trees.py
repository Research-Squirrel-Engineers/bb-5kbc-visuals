#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_14_inheritance_trees.py -- how deep does each chain really go?
=========================================================================

Source: paper Tab. 6 (transitive Vorfahrenmengen) for *which* ancestors
each class reaches, and the published CIDOC CRM / CRMsci / OWL-Time
class hierarchies (public standards, not bb5kbc-specific) for the
*order* those ancestors chain in -- Table 6 gives a flattened set, not a
sequence, so the CRM-internal chain order here (E1->E70->E72->E18->E26,
E1->E2->E4->E5->E7->E13, E4->S4->S19, E1->E52) is standard CIDOC
CRM/CRMsci structure, applied to the set Table 6 already establishes.
Where step_04 shows *how many* parents a class has (including the
FSL/LADO/PROV/OWL-Time side branches), this figure deliberately shows
only the primary CRM/CRMsci chain in isolation -- *how deep* it actually
runs, from 2 hops (Datierung) to 8 (Entdeckung, via two extra CRMsci hops
before rejoining the CRM Activity chain). The other parents are step_04's
job, not repeated here.

Bilingual (revision) -- see step_00 docstring for the convention. CRM
class labels (crm:E27_Site, ...) are the standard's own vocabulary and
are never translated.

Writes: inheritance-trees.de.svg/.png, inheritance-trees.en.svg/.png
Run standalone: ``python py/step_14_inheritance_trees.py``
"""

from __future__ import annotations

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["14-inheritance-trees"]
CRM = vu.WORLD_COLORS["crm"]
CRMSCI = vu.WORLD_COLORS["crmsci"]
SITE = vu.SITE

ROOT_Y = 880
NODE_W = 300
NODE_H = 56
PITCH = 78
COL_X = [90, 523, 956, 1389]


def _chain(parts, x, chain):
    """Draw one bottom-up chain. ``chain[0]`` is the bb5kbc: root (drawn in
    SITE colour), the rest are ancestors in nearest-to-farthest order,
    each ``(label, colors)``. Returns the y of the topmost node's top edge."""
    y = ROOT_Y
    prev_center = None
    top_edge = ROOT_Y
    for i, (label, colors) in enumerate(chain):
        by = y - NODE_H
        top_edge = by
        parts.append(vu.svg_box(x, by, NODE_W, NODE_H, label,
                                 fill=colors["fill"], stroke=colors["stroke"],
                                 stroke_width=2.2 if i == 0 else 1.4))
        if prev_center is not None:
            parts.append(vu.svg_arrow(x + NODE_W / 2, prev_center, x + NODE_W / 2, by + NODE_H))
        prev_center = by
        y -= PITCH
    return top_edge


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    c = lambda n: vu.cls(n, lang)
    parts = [vu.svg_open("Four full inheritance chains: from 2 hops (Datierung) to 8 (Entdeckung)")]

    intro = tt("Nur die prim\u00e4re CRM/CRMsci-Kette \u2014 jede Klasse hat au\u00dferdem weitere, hier nicht gezeigte Eltern (FSL, LADO, PROV-O, OWL-Time).",
               "Only the primary CRM/CRMsci chain \u2014 every class also has further parents not shown here (FSL, LADO, PROV-O, OWL-Time).")
    parts.append(f'<text x="60" y="45" font-family="Fira Sans" font-size="13.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(intro)}</text>')

    chains = [
        [(c("Fundstelle"), SITE), ("crm:E27_Site", CRM), ("crm:E26_Physical_Feature", CRM),
         ("crm:E18_Physical_Thing", CRM), ("crm:E72_Legal_Object", CRM), ("crm:E70_Thing", CRM),
         ("crm:E1_CRM_Entity", CRM)],
        [(c("GeoreferenzierungsAktivitaet"), SITE), ("crm:E13_Attribute_Assignment", CRM),
         ("crm:E7_Activity", CRM), ("crm:E5_Event", CRM), ("crm:E4_Period", CRM),
         ("crm:E2_Temporal_Entity", CRM), ("crm:E1_CRM_Entity", CRM)],
        [(c("Entdeckung"), SITE), ("crmsci:S19_Encounter_Event", CRMSCI), ("crmsci:S4_Observation", CRMSCI),
         ("crm:E13_Attribute_Assignment", CRM), ("crm:E7_Activity", CRM), ("crm:E5_Event", CRM),
         ("crm:E4_Period", CRM), ("crm:E2_Temporal_Entity", CRM), ("crm:E1_CRM_Entity", CRM)],
        [(c("Datierung"), SITE), ("crm:E52_Time-Span", CRM), ("crm:E1_CRM_Entity", CRM)],
    ]
    tops = []
    for x, chain in zip(COL_X, chains):
        tops.append(_chain(parts, x, chain))

    hop_counts = [len(ch) - 1 for ch in chains]
    for x, top, hops in zip(COL_X, tops, hop_counts):
        label = tt(f"{hops} Hops", f"{hops} hops")
        parts.append(f'<text x="{x + NODE_W/2:.1f}" y="{top - 18:.1f}" text-anchor="middle" '
                     f'font-family="Fira Sans" font-weight="500" font-size="13" '
                     f'fill="{vu.BB5KBC_MAGENTA}">{vu.xml_escape(label)}</text>')

    parts.append(vu.svg_legend(60, 924, [
        (tt("bb5kbc: Klasse (Wurzel)", "bb5kbc: class (root)"), SITE),
        ("CIDOC CRM", CRM),
        ("CRMsci", CRMSCI),
    ], columns=3, col_w=420))

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"inheritance-trees.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

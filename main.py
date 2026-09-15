#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py -- bb5kbc-visuals orchestrator
=========================================

The single entry point of this repository. Every step draws one diagram
(7:4, 1750x1000, no title header and no source footer baked in -- see
PRIMER.md A4) once per language (German and English -- see PRIMER.md A4
"Bilingual") as SVG (versioned, in ``img/<step>/<name>.<lang>.svg``) and
rasterises each to PNG via resvg-py, in-process, with the vendored Fira
Sans -- no Mermaid CLI, no Node, no system fonts required. Same house
pattern as the sibling repo ``crossy-visuals`` (see there for the
reasoning behind each convention); adapted here for general-purpose
diagram assets rather than a banner/badge/detail split, since every
figure in this repo is meant to be dropped into whatever needs it -- a
slide, a paper figure, a poster.

Usage (from the repository root)::

    python main.py                     all steps, in order
    python main.py --list              print steps and exit
    python main.py --only 03           one step (id prefix match)
    python main.py --from 04           this step and everything after
    python main.py --skip 08           everything but this
    python main.py --dry-run           print the plan, run nothing
    python main.py --strict            warnings become errors (what CI runs)

Content: see PRIMER.md Teil C for what each step draws and why.

Author: Florian Thiery (LEIZA / Research Squirrel Engineers Network),
        with Claude (Anthropic) for implementation.
Licence: MIT (this script) / CC BY 4.0 (the figures it produces)
"""

from __future__ import annotations

import argparse
import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "py"))

# Ordered steps: (id, module name, one-line description)
STEPS: list[tuple[str, str, str]] = [
    ("00", "step_00_fundstelle_hub", "Fundstelle as the hub -- the mental model on one diagram"),
    ("01", "step_01_wikidata_enrichment", "Wikidata pipeline overview -- index building, two-stage Gemeinde fallback"),
    ("02", "step_02_fuzzy_matching", "Fuzzy matching mechanism -- token_sort_ratio with real computed scores"),
    ("03", "step_03_application_ontology", "bb5kbc: application ontology -- 15 classes, object properties"),
    ("04", "step_04_crm_crosswalk", "Application ontology -> CIDOC CRM crosswalk, incl. multi-inheritance"),
    ("05", "step_05_uncertainty_markers", "Uncertainty (1/2) -- the '?' marker and where certaintyDesc anchors"),
    ("06", "step_06_uncertainty_dating", "Uncertainty (2/2) -- absolute dating: start/end + free-text tolerance"),
    ("07", "step_07_geo_entities", "Geo-entities -- admin hierarchy, dedup, five external identifiers"),
    ("08", "step_08_dating_entities", "Dating-entities -- KulturelleZuordnung, shared culture vs. per-site dating"),
    ("09", "step_09_kulturen", "Kulturen -- how Kulturgruppe itself is modelled (crm:E4_Period, dedup)"),
    ("10", "step_10_pipeline_architecture", "Full pipeline architecture (paper Fig. 4), redrawn in house style"),
    ("11", "step_11_literature_enrichment", "Literature enrichment -- Modus A, the four-case dictionary logic"),
    ("12", "step_12_prov_chaining", "PROV-O chaining -- one Activity per run, linked across two stages"),
    ("13", "step_13_validation_layers", "validate_lod.py -- the 4+1 validation sections, hard vs. soft SHACL"),
    ("14", "step_14_inheritance_trees", "Full inheritance chains -- 2 to 8 hops, CRM/CRMsci depth compared"),
    ("15", "step_15_n4o_publication", "From metadata.yaml to the NFDI4Objects Knowledge Graph"),
    ("16", "step_16_persistent_uris", "w3id.org URI dereferencing -- ontology terms vs. data resources"),
    ("17", "step_17_stats_infographic", "540 sites: dataset scale and real regional distribution"),
    ("18", "step_18_site_map", "All 540 sites plotted from their real WGS84 coordinates"),
    ("19", "step_19_allen_freksa_relations", "Allen's 13 relations + a Freksa/semi-interval sketch, real site pairs"),
]
STEP_IDS = [s[0] for s in STEPS]


def _match(prefix: str) -> str:
    hits = [i for i in STEP_IDS if i == prefix or i.startswith(prefix)]
    if not hits:
        raise SystemExit(f"unknown step '{prefix}'; choices: {', '.join(STEP_IDS)}")
    if len(hits) > 1:
        raise SystemExit(f"ambiguous step '{prefix}': matches {', '.join(hits)}")
    return hits[0]


def resolve_selection(only: str | None, frm: str | None, skip: str | None) -> list[str]:
    ids = list(STEP_IDS)
    if only:
        return [_match(only)]
    if frm:
        start = _match(frm)
        return ids[ids.index(start):]
    if skip:
        drop = _match(skip)
        return [s for s in ids if s != drop]
    return ids


def run_step(step_id: str, module_name: str, *, strict: bool) -> tuple[int, float]:
    module = importlib.import_module(module_name)  # lazy: only on actual run
    start = time.perf_counter()
    try:
        written = module.main()
    except Exception as exc:  # noqa: BLE001 -- surfaced to the caller below
        if strict:
            raise
        print(f"  ! {step_id} failed: {exc}", file=sys.stderr)
        written = []
    elapsed = time.perf_counter() - start
    count = len(written) if written else 0
    label = f"{count} file(s) written" if count else "nothing to do"
    print(f"  - {step_id}: {label} ({elapsed:.2f}s)")
    return count, elapsed


def main() -> None:
    parser = argparse.ArgumentParser(description="bb5kbc-visuals build orchestrator")
    parser.add_argument("--list", action="store_true", help="print steps and exit")
    parser.add_argument("--only", metavar="STEP", help="run exactly one step (id or id prefix)")
    parser.add_argument("--from", dest="frm", metavar="STEP", help="run this step and everything after")
    parser.add_argument("--skip", metavar="STEP", help="run everything but this step")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    parser.add_argument("--strict", action="store_true", help="warnings become errors (CI mode)")
    args = parser.parse_args()

    if args.list:
        for step_id, module_name, desc in STEPS:
            print(f"{step_id:4s} {module_name:32s} {desc}")
        return

    selected = resolve_selection(args.only, args.frm, args.skip)

    if args.dry_run:
        print("plan:")
        for step_id, module_name, desc in STEPS:
            marker = "->" if step_id in selected else "  "
            print(f" {marker} {step_id:4s} {desc}")
        return

    import bb5kbc_visuals_utils as vu
    vu.ensure_dirs()

    print(f"bb5kbc-visuals: running {len(selected)} step(s)")
    totals: list[tuple[str, int, float]] = []
    for step_id, module_name, _desc in STEPS:
        if step_id not in selected:
            continue
        count, elapsed = run_step(step_id, module_name, strict=args.strict)
        totals.append((step_id, count, elapsed))

    total_time = sum(t for _, _, t in totals) or 1e-9
    print("\ntiming:")
    for step_id, count, elapsed in totals:
        share = 100 * elapsed / total_time
        print(f"  {step_id:4s} {elapsed:6.2f}s  {share:5.1f}%  ({count} file(s))")


if __name__ == "__main__":
    main()

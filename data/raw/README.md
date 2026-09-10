# data/raw/ -- read-only source mirror

Unchanged copies of the exact files each figure's docstring cites, pinned to
the commit they were taken from. Nothing under here is a render input in the
mechanical sense (no step parses these files at build time) -- they are the
structural/factual reference a human (or Claude) reads while hand-authoring
the SVG geometry in `py/step_*.py`, and they let a reviewer check a figure's
claims against the real source instead of trusting the docstring alone. Same
convention as the sibling repo `crossy-visuals` (see its PRIMER.md A3).

## bb-5kbc-sites/

Mirrored from `Research-Squirrel-Engineers/bb-5kbc-sites`, commit
`5857df43da5675279afb3410a84d84b7fa80f15d` (2026-09-10):

| File | Used by | Why |
|---|---|---|
| `bb5kbc-ontology.ttl` | 03, 04 | the authoritative Turtle source, v0.11, 15 classes |
| `bb5kbc-classes.mmd` | 00, 03, 09 | the maintained mermaid classDiagram -- every class, stereotype and object property in step 03 is read from here, not re-typed from the paper |
| `architecture.mmd` | (reference for a future pipeline-restyle step, not yet built) | the published Fig. 4 pipeline diagram source |
| `modelling-rules.md` | 00, 05, 06, 07, 08, 09 | Regeln 1-6, the uncertainty special case, the numeric-tolerance limitation |
| `bb5kbc-csv-mapping.md` | 04 (cross-checked) | Tab. 6-equivalent Vorfahrenmengen, CRM crosswalk detail |
| `wikidata_map.py` | 01, 02 | the actual `FUZZY_THRESHOLD` / `KREIS_FUZZY_THRESHOLD` / `GEMEINDE_FUZZY_THRESHOLD` / `SPARQL_TIMEOUT_STAGE2` constants, verified against code rather than retyped from the paper; step 02's worked examples were additionally computed once with the real `rapidfuzz` package (authoring-time only, not a repo dependency -- see the score provenance note in that step's docstring) rather than invented |

Not mirrored: `dist/*.ttl` (generated, 1.4 MB each, no figure needs the
actual triples), `data/fst_wgs84.csv` (540x65, only the `kultur` column's
value counts were needed for step 08 -- computed once, recorded in that
step's docstring, not shipped as a 580 KB dependency).

## Updating this mirror

If bb-5kbc-sites moves past the pinned commit and a figure's claim needs
re-checking: re-clone, diff the relevant file against its copy here, and
note the new commit + what changed in `PRIMER.md` A1.

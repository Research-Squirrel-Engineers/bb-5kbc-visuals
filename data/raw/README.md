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
| `architecture.mmd` | 10 | the published Fig. 4 pipeline diagram source -- every node, edge and colour class in step 10 is taken directly from here |
| `modelling-rules.md` | 00, 05, 06, 07, 08, 09 | Regeln 1-6, the uncertainty special case, the numeric-tolerance limitation |
| `bb5kbc-csv-mapping.md` | 04, 14 (cross-checked) | Tab. 6-equivalent Vorfahrenmengen, CRM crosswalk detail; step 14's chain order additionally relies on the published CIDOC CRM/CRMsci class hierarchy (a public standard, not bb5kbc-specific) applied to this table's ancestor sets |
| `wikidata_map.py` | 01, 02 | the actual `FUZZY_THRESHOLD` / `KREIS_FUZZY_THRESHOLD` / `GEMEINDE_FUZZY_THRESHOLD` / `SPARQL_TIMEOUT_STAGE2` constants, verified against code rather than retyped from the paper; step 02's worked examples were additionally computed once with the real `rapidfuzz` package (authoring-time only, not a repo dependency -- see the score provenance note in that step's docstring) rather than invented |
| `site_coordinates.csv` | 18 | **not** an upstream file -- extracted once from `data/fst_wgs84.csv`'s `wgs84_x`/`wgs84_y`/`land` columns (540 rows) and checked in here as plain data. The one documented exception to "read during authoring only": step 18 parses this file at build time, because 540 real coordinates cannot be hand-placed as geometry the way every other figure's boxes are. See that step's docstring for the full rationale. |

Additionally referenced without a local mirror: the `bb-5kbc-public` README
(fetched live, not cloned) for step 15's numbers (28,531 triples / 33
classes / 81 properties, the CRM-alignment count, the freshness-check and
build-check descriptions) and the two-rule `.htaccess` behind
`w3id.org/bb5kbc/` for step 16 (no local file to mirror -- the rules were
read directly).

Not mirrored: `dist/*.ttl` (generated, 1.4 MB each, no figure needs the
actual triples), the rest of `data/fst_wgs84.csv` beyond what
`site_coordinates.csv` and the `kultur`-column counts (step 09's
docstring) already extract.

## Updating this mirror

If bb-5kbc-sites moves past the pinned commit and a figure's claim needs
re-checking: re-clone, diff the relevant file against its copy here, and
note the new commit + what changed in `PRIMER.md` A1.

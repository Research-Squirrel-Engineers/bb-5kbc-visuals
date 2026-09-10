# bb5kbc-visuals

Slide-format figures explaining the **BB-5KBC** Linked Open Data pipeline --
built for a CAA JCM Muenster 2026 talk, from the actual ontology, scripts and
modelling docs in [bb-5kbc-sites][source], not redrawn from memory.

Every figure is a single self-contained 7:4 diagram (1750x1000 px), built
once per language (German and English), generated as versioned SVG and
rasterised to PNG in-process via [resvg-py][resvg], with the vendored Fira
Sans -- no Mermaid CLI, no Node, no system fonts required. No title header
or source-citation footer is baked in: these are general-purpose diagram
assets meant to be dropped into a slide, a paper figure or a poster, each
of which supplies its own caption. Same house pattern as the sibling repo
[crossy-visuals][crossy].

**Bilingual by design.** Class and property names (Kreis, hatFundstellenart,
...) are the real `bb5kbc:` identifiers in the German figures, unchanged;
in the English figures they are translated (Kreis -> District,
hatFundstellenart -> hasSiteType, ...) via a small glossary in
`bb5kbc_visuals_utils.py`. This treats the ontology's labelling as if it
were fully bilingual (`rdfs:label`@de / @en), extending a pattern the real
ontology already uses for some terms. CSV data values -- culture names,
site types (SBK, Grab, FBG, Siedlung, ...) -- are never translated in
either language: they are archaeological source data, not our label
choice.

[source]: https://github.com/Research-Squirrel-Engineers/bb-5kbc-sites
[resvg]: https://pypi.org/project/resvg-py/
[crossy]: https://github.com/crossy-graph/crossy-visuals

## Figures

Each row below is built as four files: `<name>.de.svg`, `<name>.de.png`,
`<name>.en.svg`, `<name>.en.png`.

| # | Title | What it shows |
|---|---|---|
| 00 | Fundstelle hub / Site hub | The mental model: a Fundstelle at the centre of seven relationships |
| 01 | Wikidata pipeline overview | Index building per admin level, the two-stage Gemeinde fallback |
| 02 | Fuzzy matching | How `token_sort_ratio` decides a match, with four real computed scores |
| 03 | Application ontology | All 15 `bb5kbc:` classes and their object properties |
| 04 | CRM crosswalk | Single/double/triple CRM anchoring, per the paper's own typology |
| 05 | Uncertainty (1/2) | The `"?"` marker: `certaintyDesc` anchors differently for culture vs. site type |
| 06 | Uncertainty (2/2) | Absolute dating: numeric start/end plus free-text tolerance (not structured) |
| 07 | Geo-entities | Admin hierarchy, deduplication, the five external identifiers, location certainty |
| 08 | Dating-entities | One shared Kulturgruppe, per-site KulturelleZuordnung + Datierung |
| 09 | Kulturen / Culture groups | How Kulturgruppe itself is modelled (`crm:E4_Period`, dedup, external ID) |

## Running it

```bash
pip install -r requirements.txt
python main.py                # all figures, into img/<NN-topic>/*.<lang>.svg + *.<lang>.png
python main.py --list         # print the step table
python main.py --only 04      # one figure (both languages)
python main.py --from 05      # this figure and everything after
python main.py --dry-run      # print the plan, run nothing
```

Running `python main.py` twice leaves `git status` clean -- every writer in
`py/bb5kbc_visuals_utils.py` is deterministic (no timestamps, no random ids).
Box and circle labels auto-shrink their font size (and, for circles, wrap to
a second line) when text would otherwise overflow the shape -- this is what
keeps both language versions legible without per-figure tuning, since
translated labels rarely have the same length as the original.

## Repository layout

```
PRIMER.md                  internal work plan (German) -- read this first if extending the repo
main.py                    the orchestrator, the only entry point
py/bb5kbc_visuals_utils.py palette, canvas constants, SVG/PNG writers
py/step_NN_*.py            one module per figure, each runnable standalone
data/raw/bb-5kbc-sites/    read-only mirror of the source facts each figure is built from
fonts/                     vendored Fira Sans (OFL), same as crossy-visuals
img/NN-topic/              generated SVG + PNG, .de. and .en. pairs (versioned; see PRIMER.md A3)
```

## Provenance

Every figure's docstring names the exact source file and section in
`data/raw/bb-5kbc-sites/` it was built from -- thresholds, class lists and
attribute names are copied from the actual ontology/scripts, not
re-derived from the published paper's prose alone. See `PRIMER.md` Teil A1
for the dated findings from inspecting those sources, and Teil C for what
each step draws and why.

## Licence

Code: MIT. Figures under `img/`: CC BY 4.0, matching the licence of the
BB-5KBC data and ontology they illustrate. See `LICENSE` and `CITATION.cff`.

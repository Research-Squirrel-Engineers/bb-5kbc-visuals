# PRIMER -- bb5kbc-visuals

Interner Arbeitsplan. Wird zu Beginn jedes Chats hochgeladen (zusammen mit
dem Repo-Bundle, siehe A5) und am Ende zur\u00fcckgeschrieben.

**Sprachregel dieses Projekts (seit 2026-09-10b, explizit von Florian
bestaetigt):** Chat-Kommunikation mit Florian auf Deutsch. `PRIMER.md` auf
Deutsch. Alles andere -- Code, Kommentare, README, die Diagramme selbst,
Commit-Messages -- auf British English.

## Teil A -- Immer g\u00fcltig

### A1 Ausgangslage

| Repo / Datei | Rolle | Befund |
|---|---|---|
| `Research-Squirrel-Engineers/bb-5kbc-sites` | Quelle der Fakten | geklont, commit `5857df43da5675279afb3410a84d84b7fa80f15d` (2026-09-10). Enth\u00e4lt Ontologie (`bb5kbc-ontology.ttl` v0.11, 15 Klassen), gepflegtes Mermaid-Klassendiagramm (`bb5kbc-classes.mmd`), `modelling-rules.md` (Regeln 1--6), `wikidata_map.py` (echte Schwellwerte: `FUZZY_THRESHOLD=0.85`, `KREIS_FUZZY_THRESHOLD=0.75`, `GEMEINDE_FUZZY_THRESHOLD=0.82`, `SPARQL_TIMEOUT_STAGE2=90`) |
| `Research-Squirrel-Engineers/bb-5kbc-public` | N4O-KG-Publikationsseite | geklont, commit `18b5f72ee0877093587c6c72c5762bfc415dfe40`. Noch nicht f\u00fcr eine Grafik verwendet -- Kandidat f\u00fcr Teil D |
| `crossy-graph/crossy-visuals` (Florians Vorbild-Repo) | Hausmuster | geklont, commit `5adc399b367a7e156e8e5a022c76fec37dbba66a`. Pure-Python-SVG + resvg-py + vendored Fira Sans, `main.py`-Orchestrator. Ab Revision 2026-09-10b bewusst NICHT mehr 1:1 \u00fcbernommen: crossy-visuals nutzt einen Banner/Badge/Detail-Split ohne Titel-Header auf jedem Einzelbild; dieses Repo hat gar keinen Header/Footer auf irgendeiner Grafik (siehe A4) |
| `SqP_8_1__5_bb_5kbc__1_.pdf` (hochgeladenes Paper) | Goldstandard f\u00fcr Inhalt | Schmidt & Thiery 2026, Squirrel Papers 8(1), doi:10.5281/zenodo.19830968 |
| `fst_wgs84.csv` (540 Zeilen) | Datengrundlage f\u00fcr S10 | Spalte `kultur` ausgez\u00e4hlt: 9 distinkte Werte, Summe 540. In Revision 2026-09-10b nur noch als eine einzelne Grounding-Aussage in Schritt 09 verwendet, nicht mehr als eigenst\u00e4ndiges Balkendiagramm (siehe A4, Florians Feedback) |
| `rapidfuzz` (PyPI) | Autoring-Hilfsmittel f\u00fcr S12 | lokal installiert, NICHT Teil von `requirements.txt` (nur zur einmaligen Berechnung echter `token_sort_ratio`-Werte f\u00fcr die neue Fuzzy-Matching-Grafik genutzt, siehe S12) |

**Befund 2026-09-10b (Florians Feedback nach dem ersten Durchlauf):**
1. Alles auf British English, kein Titel-Header, kein Footer auf den Grafiken.
2. "Kulturen" (damals ein Balkendiagramm mit echten H\u00e4ufigkeiten) sollte
   wieder ein Modellierungs-Diagramm werden -- die Statistik war nicht
   gefragt.
3. Diverse Positionen/Layouts waren nicht ausgereift ("vom Design muss was
   ge\u00e4ndert werden") -- generelles Ger\u00fcst-Feedback, keine Einzelpunkte.
4. Zus\u00e4tzlich gew\u00fcnscht: eine eigene Grafik zum Fuzzy-Matching-Mechanismus
   selbst (nicht nur der Pipeline-\u00dcbersicht).
5. Klarstellung: die Grafiken sollen generisch nutzbar sein (Paper, Poster,
   *und* Folien), nicht folienspezifisch gestaltet -- das ist der Grund f\u00fcr
   Punkt 1 (kein Header/Footer).

### A2 Zielbild

```
data/raw/bb-5kbc-sites/*     Struktur-/Faktenquelle (read-only, unver\u00e4ndert)
      \u2502
      \u25bc  py/step_NN_*.py          Geometrie + Text je Diagramm (Fakten aus data/raw/, Layout von Hand)
      \u2502
      \u25bc  main.py
img/NN-topic/*.svg           Quelle, versioniert, ein File = ein Diagramm (7:4, randlos nutzbar)
      \u2502
      \u25bc  resvg-py (in-process)
img/NN-topic/*.png           fertige Grafik, wei\u00dfer Hintergrund
```

Eigenschaften, an denen sich ein fertiges Diagramm messen lassen muss:

- Zweimaliger Lauf von `python main.py` \u2192 `git status` bleibt leer.
- Jede Grafik ist 1750\u00d71000 px (7:4), **ohne** Titel-Header und **ohne**
  Footer -- der volle Canvas geh\u00f6rt dem Diagramminhalt.
- Farben kommen ausschlie\u00dflich aus `py/bb5kbc_visuals_utils.py`.
- Klassen-/Property-Namen (Fundstelle, hatKulturelleZuordnung, \u2026) bleiben
  deutsch, weil es die echten `bb5kbc:`-Bezeichner sind; jeder erkl\u00e4rende
  Text (Panel-Titel, Captions, Legenden) ist English.
- Jede Zahl/jeder Klassenname/jede Schwelle ist im Docstring auf eine Datei
  in `data/raw/` zur\u00fcckgef\u00fchrt.
- L\u00e4uft ohne externe CLI-Tools -- nur `pip install -r requirements.txt`.

### A3 Querschnittsregeln

- Rohdaten liegen unter `data/raw/`, unver\u00e4ndert, read-only (siehe
  `data/raw/README.md`).
- **`img/` wird versioniert, nicht ignoriert** -- die SVG/PNG sind das
  eigentliche Produkt.
- Kein Zeitstempel im Output. `RELEASE` in `bb5kbc_visuals_utils.py` ist von
  Hand zu pflegen.
- Zweimal laufen lassen, `git status` muss leer bleiben -- verifiziert nach
  jedem Schritt (SHA-256 je Datei).
- Netzzugriff ist auf die Recherche-Phase beschr\u00e4nkt; kein Schritt in
  `main.py` greift zur Laufzeit auf das Netz zu.
- **Sprachregel:** siehe Kopf dieses Dokuments.
- Windows ist die Referenzplattform f\u00fcr Befehle an Florian (`cmd`/
  `PowerShell`, `findstr`/`Select-String` statt `grep`).

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Render-Pipeline | pure-Python + resvg-py, identisch zu crossy-visuals | 2026-09-10 |
| Canvas | fest 1750\u00d71000 px (7:4) | 2026-09-10 |
| Hintergrund | wei\u00df (nicht transparent) | 2026-09-10 |
| Hausfarben-Paar | Magenta `#9c2860` (bb5kbc: eigene Knoten) + Ocker `#8a5a2a` (CIDOC-CRM-Anker) | 2026-09-10 |
| "Welt"-Palette | je eine Farbe pro CRM/CRMsci/PROV-O/OWL-Time/FSL/LADO-Familie, \u00fcber alle Grafiken konsistent | 2026-09-10 |
| Symbolsprache | Doppelring-Kreis = geteilter/deduplizierter Knoten; einfacher Kasten = eigener Knoten pro Fundstelle/FID; gestrichelt = tr\u00e4gt `fsl:certaintyDesc "uncertain"@en` | 2026-09-10 |
| Schrift | Fira Sans, vendored aus crossy-visuals \u00fcbernommen | 2026-09-10 |
| **Kein Titel-Header, kein Footer** | **Revision 2026-09-10b:** alle Grafiken verlieren den Kicker/Titel-Block oben und die Quellenzeile unten. Die Diagramme sind generische Assets (Paper, Poster, Folien), nicht folienspezifische Einzelst\u00fccke -- der aufrufende Kontext liefert Titel/Zitation selbst. `svg_header()`/`svg_footer()` aus den Utils entfernt, `MARGIN_TOP`/`MARGIN_BOTTOM`/`CONTENT_Y0`/`CONTENT_Y1` neu eingef\u00fchrt (50px Rand statt 150/95px Header/Footer-Reservierung) | 2026-09-10b |
| **Sprache: durchgehend British English** | **Revision 2026-09-10b:** alle Panel-Titel, Captions, Legenden \u00fcbersetzt. Klassen-/Property-Namen und CSV-Werte (Fundstelle, hatFundstellenart, SBK, Grab, \u2026) bleiben deutsch, weil es die echten Bezeichner/Datenwerte sind -- keine \u00dcbersetzung von Identifiern | 2026-09-10b |
| **09-kulturen: Modellierung statt Statistik** | **Revision 2026-09-10b:** das fr\u00fchere Balkendiagramm (echte H\u00e4ufigkeiten aus der CSV) ersetzt durch eine Modellierungs-Grafik (Kulturgruppe als `crm:E4_Period`, Dedup-Mechanismus, Fan-in-Illustration, "?"-Reminder). Die reale 9-Werte-Zahl bleibt als einzelner Grounding-Satz erhalten, ist aber nicht mehr der Bildinhalt | 2026-09-10b |
| **Neue Grafik: Fuzzy-Matching-Mechanismus** | **Revision 2026-09-10b:** 01-wikidata-enrichment zeigt nur noch die Pipeline-\u00dcbersicht + Index-Aufbau + Gemeinde-Fallback. Der eigentliche `token_sort_ratio`-Mechanismus bekommt eine eigene neue Grafik (02-fuzzy-matching) mit vier echten, berechneten Score-Beispielen | 2026-09-10b |
| **Umnummerierung** | 00 unver\u00e4ndert; 01 (Wikidata-\u00dcbersicht, verschlankt); 02 NEU (Fuzzy-Matching); alte 02--07 \u2192 neue 03--08; alte 08 (Kulturen-Statistik) gel\u00f6scht, neue 09 (Kulturen-Modellierung) | 2026-09-10b |

### A5 Was in welchem Chat hochgeladen wird

```
robocopy . ..\bb5kbc-visuals-bundle /E /XD .git __pycache__ fonts
Compress-Archive -Path ..\bb5kbc-visuals-bundle\* -DestinationPath ..\bb5kbc-visuals-bundle.zip -Force
```

Nicht hochladen: `fonts/*.ttf`, `__pycache__/`, `.git/`.

### A6 IRI-Landkarte

Entf\u00e4llt -- dieses Repo publiziert kein eigenes RDF.

## Teil B -- Schrittübersicht

| ID | Schritt | Datei | h\u00e4ngt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen: Canvas, Palette, Symbolsprache | \u2014 | \u2014 | erledigt 2026-09-10 |
| S1 | Skeleton: `main.py`, `bb5kbc_visuals_utils.py`, Fonts, Lizenz | \u2014 | S0 | erledigt 2026-09-10 |
| S2 | 00 Fundstelle-Hub | `step_00_fundstelle_hub.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S3 | 01 Wikidata-Pipeline-\u00dcbersicht | `step_01_wikidata_enrichment.py` | S1 | erledigt 2026-09-10, verschlankt 2026-09-10b |
| S4 | 03 Application Ontology | `step_03_application_ontology.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S5 | 04 CRM-Crosswalk | `step_04_crm_crosswalk.py` | S4 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S6 | 05 Unsicherheit (1/2, "?"-Marker) | `step_05_uncertainty_markers.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S7 | 06 Unsicherheit (2/2, Datierung) | `step_06_uncertainty_dating.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S8 | 07 Geo-Entit\u00e4ten | `step_07_geo_entities.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S9 | 08 Dating-Entit\u00e4ten | `step_08_dating_entities.py` | S1 | erledigt 2026-09-10, \u00fcberarbeitet 2026-09-10b |
| S10 | 08-alt Kulturen (Statistik) | \u2014 | S1 | **hinf\u00e4llig 2026-09-10b** -- ersetzt durch S13 |
| S11 | Revision: kein Header/Footer, durchg\u00e4ngig English | alle `step_*.py` + Utils | S2--S10 | erledigt 2026-09-10b |
| S12 | 02 Fuzzy-Matching-Mechanismus (neu) | `step_02_fuzzy_matching.py` | S3 | erledigt 2026-09-10b |
| S13 | 09 Kulturen -- Modellierung statt Statistik (neu) | `step_09_kulturen.py` | S11 | erledigt 2026-09-10b |

Alle Diagramm-Schritte sind voneinander unabh\u00e4ngig (jeder importiert nur
`bb5kbc_visuals_utils`) und k\u00f6nnen einzeln per `--only NN` neu gebaut werden.

## Teil C -- Die Schritte

### S11 -- Revision: kein Header/Footer, durchg\u00e4ngig English

**Ziel:** alle neun (jetzt zehn) Grafiken von "Folie mit Titel-Header und
Quellen-Footer" auf "randloses, generisches Diagramm" umstellen und
komplett auf English \u00fcbersetzen, ohne die Faktentreue der Docstrings zu
verlieren.

**Substanz:**
- `bb5kbc_visuals_utils.py`: `svg_header()`/`svg_footer()` entfernt;
  `MARGIN_X/TOP/BOTTOM` und `CONTENT_X0/X1/Y0/Y1` neu (50px statt vormals
  150px oben / 95px unten) -- pro Grafik dadurch ca. 200px mehr nutzbare
  H\u00f6he.
- Jede `step_*.py`-Datei einzeln durchgegangen: Panel-Titel, Legenden,
  Captions und Fu\u00dfnoten \u00fcbersetzt; bb5kbc:-Klassen-/Property-Namen und
  CSV-Werte (Fundstelle, hatFundstellenart, SBK, Grab, \u2026) bewusst NICHT
  \u00fcbersetzt, weil es reale Bezeichner/Datenwerte sind, keine Prosa.
- Layouts an die gr\u00f6\u00dfere Fl\u00e4che angepasst (gr\u00f6\u00dfere Kreise/K\u00e4sten, mehr
  Row-Pitch), nicht nur hochskaliert -- sonst h\u00e4tte "mehr Platz" nur zu
  mehr Leerraum gef\u00fchrt statt zu besserer Lesbarkeit.

**Erledigt 2026-09-10b:** beim ersten Rendern von 00 (Land-Kreis-Kette am
oberen Rand) und 03 (Application Ontology, Spalten zu eng) je ein
Kollisions-/Layoutproblem gefunden und direkt korrigiert (Spaltenabst\u00e4nde
bzw. Legenden-Position). Alle zehn Grafiken nach der \u00dcberarbeitung
visuell gepr\u00fcft, keine Text-/Element-\u00dcberlappungen mehr.

**Abnahme:** `python main.py` (alle 10 Schritte), zweimal hintereinander \u2192
`git status` sauber; kein Diagramm enth\u00e4lt einen Titel-Header oder eine
Footer-Zeile; kein deutsches Wort au\u00dferhalb von Klassen-/Property-Namen
und CSV-Beispielwerten.

### S12 -- 02 Fuzzy-Matching-Mechanismus (neu)

**Ziel:** zeigen, *wie* `rapidfuzz.fuzz.token_sort_ratio` eine
Match-Entscheidung trifft -- nicht nur, dass es sie trifft (das leistete
bereits die Pipeline-\u00dcbersicht in 01).

**Substanz:** vier-stufiger Mini-Ablauf (Tokenise \u2192 Sort tokens \u2192 Rejoin
\u2192 Score) plus vier Beispielzeilen mit **echten, berechneten** Scores (nicht
erfunden): `rapidfuzz` lokal installiert und
`fuzz.token_sort_ratio(a, b)` f\u00fcr vier String-Paare ausgef\u00fchrt, die den
im Paper genannten F\u00e4llen entsprechen ("Landkreis X"-Pr\u00e4fixproblem;
die im Paper explizit genannten Alias-Beispiele "MVP" und "sommerda").
Ergebnisse: `Kreis Ostprignitz-Ruppin` vs. `Ostprignitz-Ruppin` = 85.71
(besteht); `Landkreis Havelland` vs. `Havelland` = 64.29 (scheitert, braucht
Pr\u00e4fix-Strip); `sommerda` vs. `S\u00f6mmerda` = 75.00 (scheitert knapp an der
Gemeinde-Schwelle 82, braucht Alias); `MVP` vs.
`Mecklenburg-Vorpommern` = 16.00 (scheitert deutlich, nur Alias hilft).
Jede Zeile: Gauge-Balken (0--100) mit Schwellwert-Markierung, PASS/FAIL-
Badge, Konsequenz-Text.

**Abnahme:** `python main.py --only 02`, 2 Dateien; alle vier Scores
stimmen mit einem frischen `rapidfuzz`-Lauf \u00fcberein (siehe Docstring).

### S13 -- 09 Kulturen: Modellierung statt Statistik (neu)

**Ziel:** Florians Korrektur umsetzen -- "Kulturen" zeigt wieder, *wie*
Kulturgruppe modelliert ist, nicht *wie oft* welcher Wert vorkommt.

**Substanz:** UML-artige Attributbox f\u00fcr Kulturgruppe (`crm:E4_Period`,
`rdfs:label`, `bb5kbc:hasExternalIdentifier`) links; rechts ein Kasten, der
den Dedup-Mechanismus (Regel 2/3, MD5-Hash der ersten 8 Zeichen) erkl\u00e4rt
und die reale 9-Werte-Zahl als einzelnen Grounding-Satz nennt (nicht als
Diagramm). Unten links eine Fan-in-Illustration (vier Beispiel-Fundstellen
\u2192 ein geteilter Kulturgruppe-Knoten \u2192 eine Wikidata-QID); unten rechts ein
kompakter Reminder des "?"-Mechanismus aus 05 (zwei Knoten, eine QID), mit
Verweis auf die ausf\u00fchrliche Grafik statt Wiederholung.

**Erledigt 2026-09-10b:** erster Entwurf lie\u00df die zweizeilige Caption \u00fcber
den Fundstelle-Chips in die erste Box hineinlaufen (zu knapper Abstand) --
Caption-Position nach oben verschoben, Chip-Reihen leicht neu zentriert.

**Abnahme:** `python main.py --only 09`, 2 Dateien; keine Statistik-Balken
mehr im Bild; die reale 9-Werte-Aussage ist ein Satz, nicht das
Bildzentrum; keine \u00dcberlappungen.

## Teil D -- Offene Punkte

- **Pipeline-Architektur neu im Hausstil.** `architecture.mmd` (Paper
  Abb. 4) existiert bereits inhaltlich vollst\u00e4ndig -- br\u00e4uchte nur die
  `bb5kbc_visuals_utils`-Palette und das randlose 7:4-Format.
- **N4O-KG-Publikationspipeline.** `bb-5kbc-public` ist geklont, aber noch
  f\u00fcr keine Grafik verwendet: `metadata.yaml` \u2192 SHACL \u2192
  `n4o-collection.ttl`, mit den echten Zahlen 28\u2009531 Tripel / 33 Klassen /
  81 Properties aus dessen README.
- **PROV-O-Verkettung \u00fcber zwei Pipeline-Stufen.** Die Cross-Namespace
  `wasInformedBy`-Verbindung zwischen `csv_enrichment_run.ttl` und
  `csv_to_lod_run.ttl` (Paper Abschnitt 6).
- **SHACL-Validierungs-Gate.** Warning- vs. die eine harte Violation-Regel.
- **Mehrfachvererbung als B\u00e4ume neu gezeichnet.** Paper Abb. 2 (vier
  Klassen als Baum) w\u00e4re eine Erg\u00e4nzung zu 04, nicht redundant.
- **Statistik-/Kartenfolie.** 540 Fundstellen, 350 DE + 178 PL \u00fcber neun
  Wojewodschaften -- noch nicht visualisiert. (Das w\u00e4re der richtige Ort
  f\u00fcr eine Statistik-Grafik, falls gew\u00fcnscht -- nicht mehr 09-kulturen.)

Wenn einer dieser Punkte zum n\u00e4chsten Schritt wird: nach S13 einsortieren
(S14, S15, \u2026), hier streichen, in Teil B eintragen.

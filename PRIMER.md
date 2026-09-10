# PRIMER -- bb5kbc-visuals

Interner Arbeitsplan. Wird zu Beginn jedes Chats hochgeladen (zusammen mit
dem Repo-Bundle, siehe A5) und am Ende zurückgeschrieben.

**Sprachregel dieses Projekts (seit 2026-09-10b, explizit von Florian
bestaetigt):** Chat-Kommunikation mit Florian auf Deutsch. `PRIMER.md` auf
Deutsch. Alles andere -- Code, Kommentare, README, die Diagramme selbst,
Commit-Messages -- auf British English.

## Teil A -- Immer gültig

### A1 Ausgangslage

| Repo / Datei | Rolle | Befund |
|---|---|---|
| `Research-Squirrel-Engineers/bb-5kbc-sites` | Quelle der Fakten | geklont, commit `5857df43da5675279afb3410a84d84b7fa80f15d` (2026-09-10). Enthält Ontologie (`bb5kbc-ontology.ttl` v0.11, 15 Klassen), gepflegtes Mermaid-Klassendiagramm (`bb5kbc-classes.mmd`), `modelling-rules.md` (Regeln 1--6), `wikidata_map.py` (echte Schwellwerte: `FUZZY_THRESHOLD=0.85`, `KREIS_FUZZY_THRESHOLD=0.75`, `GEMEINDE_FUZZY_THRESHOLD=0.82`, `SPARQL_TIMEOUT_STAGE2=90`) |
| `Research-Squirrel-Engineers/bb-5kbc-public` | N4O-KG-Publikationsseite | geklont, commit `18b5f72ee0877093587c6c72c5762bfc415dfe40`. Noch nicht für eine Grafik verwendet -- Kandidat für Teil D |
| `crossy-graph/crossy-visuals` (Florians Vorbild-Repo) | Hausmuster | geklont, commit `5adc399b367a7e156e8e5a022c76fec37dbba66a`. Pure-Python-SVG + resvg-py + vendored Fira Sans, `main.py`-Orchestrator. Ab Revision 2026-09-10b bewusst NICHT mehr 1:1 übernommen: crossy-visuals nutzt einen Banner/Badge/Detail-Split ohne Titel-Header auf jedem Einzelbild; dieses Repo hat gar keinen Header/Footer auf irgendeiner Grafik (siehe A4) |
| `SqP_8_1__5_bb_5kbc__1_.pdf` (hochgeladenes Paper) | Goldstandard für Inhalt | Schmidt & Thiery 2026, Squirrel Papers 8(1), doi:10.5281/zenodo.19830968 |
| `fst_wgs84.csv` (540 Zeilen) | Datengrundlage für S10 | Spalte `kultur` ausgezählt: 9 distinkte Werte, Summe 540. In Revision 2026-09-10b nur noch als eine einzelne Grounding-Aussage in Schritt 09 verwendet, nicht mehr als eigenständiges Balkendiagramm (siehe A4, Florians Feedback) |
| `rapidfuzz` (PyPI) | Autoring-Hilfsmittel für S12 | lokal installiert, NICHT Teil von `requirements.txt` (nur zur einmaligen Berechnung echter `token_sort_ratio`-Werte für die neue Fuzzy-Matching-Grafik genutzt, siehe S12) |
| `Research-Squirrel-Engineers/bb-5kbc-visuals` (dieses Repo) | committed von Florian | auf GitHub gesichert. Beim Review danach: ein echter Darstellungsfehler gefunden (siehe Befund 2026-09-10c) und der Wunsch nach zwei kompletten Sprachversionen je Grafik (DE/EN), inkl. Übersetzung von Klassennamen wie „Kreis" — siehe A4 |

**Befund 2026-09-10c (Review nach dem Commit):**
1. **Text-Overflow in den „geteilt"-Kreisen.** Längere Subtitles (z. B. „shared · bundesland_{hash}") liefen über den Kreisrand hinaus — sichtbar in 00, latent auch in 07/08/09. Kein Einzelfall, sondern ein systematisches Problem der festen Schriftgröße in `svg_hash_node`/`svg_box` gegenüber variabler Textlänge (Klassennamen, später auch Sprachen).
2. **Zwei Komplettversionen je Grafik gewünscht:** eine ganz auf Deutsch, eine ganz auf Englisch — inklusive Übersetzung der bb5kbc:-Klassen-/Property-Namen selbst (z. B. „Kreis" → „District"), nicht nur der Prosa. Florians eigene Einordnung: das ist eine bewusste Fiktion („tun wir mal so als wäre das Label im Graph zweisprachig") — die echte Ontologie nutzt für einzelne Terme bereits `rdfs:label`@de + `skos:altLabel`@en (siehe Erfahrung aus anderen bb5kbc-Chats), hier wird dasselbe Prinzip konsequent auf alle Klassen/Properties ausgedehnt, ohne dass sich an der TTL etwas ändert.

**Befund 2026-09-10b (Florians Feedback nach dem ersten Durchlauf):**
1. Alles auf British English, kein Titel-Header, kein Footer auf den Grafiken.
2. "Kulturen" (damals ein Balkendiagramm mit echten Häufigkeiten) sollte
   wieder ein Modellierungs-Diagramm werden -- die Statistik war nicht
   gefragt.
3. Diverse Positionen/Layouts waren nicht ausgereift ("vom Design muss was
   geändert werden") -- generelles Gerüst-Feedback, keine Einzelpunkte.
4. Zusätzlich gewünscht: eine eigene Grafik zum Fuzzy-Matching-Mechanismus
   selbst (nicht nur der Pipeline-Übersicht).
5. Klarstellung: die Grafiken sollen generisch nutzbar sein (Paper, Poster,
   *und* Folien), nicht folienspezifisch gestaltet -- das ist der Grund für
   Punkt 1 (kein Header/Footer).

**Befund 2026-09-10d (Florian hat das Repo committed und main.py laufen lassen):**
1. Traceback beim Lauf auf Windows/Python 3.10: `SyntaxError: f-string expression
   part cannot include a backslash` in `step_05_uncertainty_markers.py` Zeile 94.
   Ursache: die Sandbox hier läuft auf Python 3.12, wo PEP 701 Backslashes in
   f-string-Ausdrücken erlaubt -- ein stiller Versionsunterschied, der beim
   Testen in der Sandbox nicht auffiel (Python 3.10 war hier nicht installierbar,
   Fix stattdessen per AST-Scanner verifiziert, siehe A4).
2. Florian: künftige Änderungen an diesem (jetzt existierenden, von ihm
   verwalteten) Repo sollen als Patch-ZIP kommen, nicht als kompletter
   Ersatz-Export -- siehe A4.

**Befund 2026-09-10e (S16-Patch angewendet, neuer Fehler):** `main.py`-Log
zeigt Schritte 00--04, 06, 07 mit je "2 file(s)" (nicht 4) und Schritte
05, 08, 09 mit `AttributeError: module 'bb5kbc_visuals_utils' has no
attribute 't'`. Daraus folgt zweifelsfrei: Florians Repo enthielt zum
Zeitpunkt des S16-Patches noch die einsprachige `bb5kbc_visuals_utils.py`
und einsprachige Versionen von 00--04/06/07 -- die vollständige bilinguale
Lieferung aus S15 war nie (oder nicht vollständig) angekommen. Der
S16-Patch hat das nicht bemerkt und drei Schritt-Dateien isoliert
ausgetauscht, was das Repo in einen inkonsistenten Zustand brachte. Siehe
S17.

### A2 Zielbild

```
data/raw/bb-5kbc-sites/*     Struktur-/Faktenquelle (read-only, unverändert)
      │
      ▼  py/step_NN_*.py          Geometrie + Text je Diagramm, build(lang) für DE/EN
      │
      ▼  main.py
img/NN-topic/*.<lang>.svg    Quelle, versioniert, ein File = ein Diagramm in einer Sprache (7:4, randlos)
      │
      ▼  resvg-py (in-process)
img/NN-topic/*.<lang>.png    fertige Grafik, weißer Hintergrund
```

Eigenschaften, an denen sich ein fertiges Diagramm messen lassen muss:

- Zweimaliger Lauf von `python main.py` → `git status` bleibt leer.
- Jede Grafik ist 1750×1000 px (7:4), **ohne** Titel-Header und **ohne**
  Footer -- der volle Canvas gehört dem Diagramminhalt.
- Jede Grafik existiert als **DE- und EN-Fassung** (`<name>.de.svg/png`,
  `<name>.en.svg/png`); Klassen-/Property-Namen sind in der DE-Fassung
  die echten `bb5kbc:`-Bezeichner, in der EN-Fassung übersetzt (siehe A4);
  CSV-/Kulturwerte (SBK, Grab, ...) bleiben in beiden Fassungen unverändert.
- Text in Kreisen/Kästen übersteht unterschiedliche Textlängen: Schriftgröße
  passt sich automatisch an (siehe A4, S14), kein manuelles Nachjustieren
  pro Sprache nötig.
- Farben kommen ausschließlich aus `py/bb5kbc_visuals_utils.py`.
- Jede Zahl/jeder Klassenname/jede Schwelle ist im Docstring auf eine Datei
  in `data/raw/` zurückgeführt.
- Läuft ohne externe CLI-Tools -- nur `pip install -r requirements.txt`.

### A3 Querschnittsregeln

- Rohdaten liegen unter `data/raw/`, unverändert, read-only (siehe
  `data/raw/README.md`).
- **`img/` wird versioniert, nicht ignoriert** -- die SVG/PNG sind das
  eigentliche Produkt.
- Kein Zeitstempel im Output. `RELEASE` in `bb5kbc_visuals_utils.py` ist von
  Hand zu pflegen.
- Zweimal laufen lassen, `git status` muss leer bleiben -- verifiziert nach
  jedem Schritt (SHA-256 je Datei).
- Netzzugriff ist auf die Recherche-Phase beschränkt; kein Schritt in
  `main.py` greift zur Laufzeit auf das Netz zu.
- **Sprachregel:** siehe Kopf dieses Dokuments.
- Windows ist die Referenzplattform für Befehle an Florian (`cmd`/
  `PowerShell`, `findstr`/`Select-String` statt `grep`).

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Render-Pipeline | pure-Python + resvg-py, identisch zu crossy-visuals | 2026-09-10 |
| Canvas | fest 1750×1000 px (7:4) | 2026-09-10 |
| Hintergrund | weiß (nicht transparent) | 2026-09-10 |
| Hausfarben-Paar | Magenta `#9c2860` (bb5kbc: eigene Knoten) + Ocker `#8a5a2a` (CIDOC-CRM-Anker) | 2026-09-10 |
| "Welt"-Palette | je eine Farbe pro CRM/CRMsci/PROV-O/OWL-Time/FSL/LADO-Familie, über alle Grafiken konsistent | 2026-09-10 |
| Symbolsprache | Doppelring-Kreis = geteilter/deduplizierter Knoten; einfacher Kasten = eigener Knoten pro Fundstelle/FID; gestrichelt = trägt `fsl:certaintyDesc "uncertain"@en` | 2026-09-10 |
| Schrift | Fira Sans, vendored aus crossy-visuals übernommen | 2026-09-10 |
| **Kein Titel-Header, kein Footer** | **Revision 2026-09-10b:** alle Grafiken verlieren den Kicker/Titel-Block oben und die Quellenzeile unten. Die Diagramme sind generische Assets (Paper, Poster, Folien), nicht folienspezifische Einzelstücke -- der aufrufende Kontext liefert Titel/Zitation selbst. `svg_header()`/`svg_footer()` aus den Utils entfernt, `MARGIN_TOP`/`MARGIN_BOTTOM`/`CONTENT_Y0`/`CONTENT_Y1` neu eingeführt (50px Rand statt 150/95px Header/Footer-Reservierung) | 2026-09-10b |
| **Sprache: durchgehend British English** | **Revision 2026-09-10b:** alle Panel-Titel, Captions, Legenden übersetzt. Klassen-/Property-Namen und CSV-Werte (Fundstelle, hatFundstellenart, SBK, Grab, …) bleiben deutsch, weil es die echten Bezeichner/Datenwerte sind -- keine Übersetzung von Identifiern | 2026-09-10b |
| **09-kulturen: Modellierung statt Statistik** | **Revision 2026-09-10b:** das frühere Balkendiagramm (echte Häufigkeiten aus der CSV) ersetzt durch eine Modellierungs-Grafik (Kulturgruppe als `crm:E4_Period`, Dedup-Mechanismus, Fan-in-Illustration, "?"-Reminder). Die reale 9-Werte-Zahl bleibt als einzelner Grounding-Satz erhalten, ist aber nicht mehr der Bildinhalt | 2026-09-10b |
| **Neue Grafik: Fuzzy-Matching-Mechanismus** | **Revision 2026-09-10b:** 01-wikidata-enrichment zeigt nur noch die Pipeline-Übersicht + Index-Aufbau + Gemeinde-Fallback. Der eigentliche `token_sort_ratio`-Mechanismus bekommt eine eigene neue Grafik (02-fuzzy-matching) mit vier echten, berechneten Score-Beispielen | 2026-09-10b |
| **Umnummerierung** | 00 unverändert; 01 (Wikidata-Übersicht, verschlankt); 02 NEU (Fuzzy-Matching); alte 02--07 → neue 03--08; alte 08 (Kulturen-Statistik) gelöscht, neue 09 (Kulturen-Modellierung) | 2026-09-10b |
| **Auto-Fit-Schriftgröße für Kreise/Kästen** | **Revision 2026-09-10c:** `svg_hash_node` und `svg_box` schrumpfen Titel-/Subtitle-Schriftgröße jetzt automatisch (mit Untergrenze), `svg_hash_node` bricht ein zu langes Subtitle zusätzlich auf zwei Zeilen um (Trennpunkt = ausgewogenster Leerzeichen-Schnitt). Behebt den Overflow-Fehler aus Befund 2026-09-10c und macht beide Sprachversionen robust gegen unterschiedliche Textlängen, ohne dass jede Grafik einzeln nachjustiert werden muss | 2026-09-10c |
| **Bilingual: `vu.t()` + Glossar statt Duplikat-Dateien** | **Revision 2026-09-10c:** ein Übersetzungshelfer `vu.t(lang, de, en)` plus zwei Glossar-Dicts `CLASS_EN`/`PROP_EN` (+ `vu.cls()`/`vu.prop()`) in den Utils. Jede `step_*.py` bekommt `build(lang="en")` statt `build()`, `main()` ruft `build("de")` und `build("en")` auf und hängt die Ergebnislisten zusammen. Kein Duplikat-Code je Sprache -- dieselbe Geometrie, unterschiedlicher Text | 2026-09-10c |
| **Was übersetzt wird, was nicht** | Klassen-/Property-Namen (Kreis→District, hatFundstellenart→hasSiteType, ...) werden in der EN-Fassung übersetzt, in der DE-Fassung bleiben sie die echten `bb5kbc:`-Bezeichner. CSV-/Datenwerte (SBK, Grab, FBG, Siedlung, Mesolithikum, ...) werden **nie** übersetzt -- sie sind reale archäologische Quelldaten, keine Beschriftung. `hasExternalIdentifier` bleibt in beiden Sprachen gleich, weil es in der echten Ontologie bereits Englisch ist | 2026-09-10c |
| **Dateinamen** | `<name>.de.svg`/`.png` und `<name>.en.svg`/`.png` statt einer sprachneutralen Datei -- jeder Schritt liefert jetzt 4 statt 2 Dateien | 2026-09-10c |
| **Python-3.10-Kompatibilität: kein Backslash in f-string-Ausdrücken** | **Revision 2026-09-10d:** Florians Python ist 3.10; dort ist ein Backslash innerhalb der `{...}`-Ausdrucksklammer eines f-strings ein `SyntaxError` (erst PEP 701 / Python 3.12 erlaubt das, und die Sandbox hier lief unbemerkt auf 3.12). Jede Stelle mit `{tt("...\u...", "...\u...")}` direkt in einem f-string-Ausdruck refaktoriert: Übersetzung vorher in eine lokale Variable gezogen, im f-string nur noch `{variable}` referenziert. Mit einem AST-basierten Scanner (`ast.walk` + `ast.get_source_segment` auf jedem `JoinedStr`/`FormattedValue`) repo-weit nach Backslashes in f-string-Ausdrücken gesucht -- präziser als Grep, weil er tatsächlich den Ausdrucksteil isoliert statt nur Zeilen zu mustern | 2026-09-10d |
| **Auslieferung künftiger Änderungen an diesem Repo: patch-zip-delivery** | **Revision 2026-09-10d:** Florian hat das komplette Repo von der letzten Antwort committed und mich darauf hingewiesen, dass ich für ein bereits existierendes, von ihm verwaltetes Repo den `patch-zip-delivery`-Skill hätte nutzen sollen statt eines vollständigen Ersatz-ZIPs. Ab jetzt gilt: Änderungen an diesem Repo gehen als Patch-ZIP (nur geänderte Quelldateien + `PATCH-README.md`), nicht als kompletter Repo-Export -- generierte Dateien (`img/*.svg`/`*.png`) reisen als Befehl (`python main.py`), nicht als Datei, weil Florian die Pipeline bereits lauffähig hat | 2026-09-10d |

### A5 Was in welchem Chat hochgeladen wird

```
robocopy . ..\bb5kbc-visuals-bundle /E /XD .git __pycache__ fonts
Compress-Archive -Path ..\bb5kbc-visuals-bundle\* -DestinationPath ..\bb5kbc-visuals-bundle.zip -Force
```

Nicht hochladen: `fonts/*.ttf`, `__pycache__/`, `.git/`.

### A6 IRI-Landkarte

Entfällt -- dieses Repo publiziert kein eigenes RDF.

## Teil B -- Schrittübersicht

| ID | Schritt | Datei | hängt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen: Canvas, Palette, Symbolsprache | — | — | erledigt 2026-09-10 |
| S1 | Skeleton: `main.py`, `bb5kbc_visuals_utils.py`, Fonts, Lizenz | — | S0 | erledigt 2026-09-10 |
| S2 | 00 Fundstelle-Hub | `step_00_fundstelle_hub.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S3 | 01 Wikidata-Pipeline-Übersicht | `step_01_wikidata_enrichment.py` | S1 | erledigt 2026-09-10, verschlankt 2026-09-10b |
| S4 | 03 Application Ontology | `step_03_application_ontology.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S5 | 04 CRM-Crosswalk | `step_04_crm_crosswalk.py` | S4 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S6 | 05 Unsicherheit (1/2, "?"-Marker) | `step_05_uncertainty_markers.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S7 | 06 Unsicherheit (2/2, Datierung) | `step_06_uncertainty_dating.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S8 | 07 Geo-Entitäten | `step_07_geo_entities.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S9 | 08 Dating-Entitäten | `step_08_dating_entities.py` | S1 | erledigt 2026-09-10, überarbeitet 2026-09-10b |
| S10 | 08-alt Kulturen (Statistik) | — | S1 | **hinfällig 2026-09-10b** -- ersetzt durch S13 |
| S11 | Revision: kein Header/Footer, durchgängig English | alle `step_*.py` + Utils | S2--S10 | erledigt 2026-09-10b |
| S12 | 02 Fuzzy-Matching-Mechanismus (neu) | `step_02_fuzzy_matching.py` | S3 | erledigt 2026-09-10b |
| S13 | 09 Kulturen -- Modellierung statt Statistik (neu) | `step_09_kulturen.py` | S11 | erledigt 2026-09-10b |
| S14 | Bugfix: Auto-Fit-Schriftgröße (Text-Overflow in Kreisen/Kästen) | `bb5kbc_visuals_utils.py` | S11 | erledigt 2026-09-10c |
| S15 | Bilingual: alle 10 Grafiken DE + EN | alle `step_*.py` + Utils | S14 | erledigt 2026-09-10c |
| S16 | Bugfix: Python-3.10-Kompatibilität (f-string-Backslash) | `step_05/08/09_*.py` | S15 | erledigt 2026-09-10d |
| S17 | Bugfix: S16-Patch war unvollständig (utils.py fehlte) | `bb5kbc_visuals_utils.py` + alle `step_*.py` + `main.py` | S16 | erledigt 2026-09-10e |

Alle Diagramm-Schritte sind voneinander unabhängig (jeder importiert nur
`bb5kbc_visuals_utils`) und können einzeln per `--only NN` neu gebaut werden.

## Teil C -- Die Schritte

### S11 -- Revision: kein Header/Footer, durchgängig English

**Ziel:** alle neun (jetzt zehn) Grafiken von "Folie mit Titel-Header und
Quellen-Footer" auf "randloses, generisches Diagramm" umstellen und
komplett auf English übersetzen, ohne die Faktentreue der Docstrings zu
verlieren.

**Substanz:**
- `bb5kbc_visuals_utils.py`: `svg_header()`/`svg_footer()` entfernt;
  `MARGIN_X/TOP/BOTTOM` und `CONTENT_X0/X1/Y0/Y1` neu (50px statt vormals
  150px oben / 95px unten) -- pro Grafik dadurch ca. 200px mehr nutzbare
  Höhe.
- Jede `step_*.py`-Datei einzeln durchgegangen: Panel-Titel, Legenden,
  Captions und Fußnoten übersetzt; bb5kbc:-Klassen-/Property-Namen und
  CSV-Werte (Fundstelle, hatFundstellenart, SBK, Grab, …) bewusst NICHT
  übersetzt, weil es reale Bezeichner/Datenwerte sind, keine Prosa.
- Layouts an die größere Fläche angepasst (größere Kreise/Kästen, mehr
  Row-Pitch), nicht nur hochskaliert -- sonst hätte "mehr Platz" nur zu
  mehr Leerraum geführt statt zu besserer Lesbarkeit.

**Erledigt 2026-09-10b:** beim ersten Rendern von 00 (Land-Kreis-Kette am
oberen Rand) und 03 (Application Ontology, Spalten zu eng) je ein
Kollisions-/Layoutproblem gefunden und direkt korrigiert (Spaltenabstände
bzw. Legenden-Position). Alle zehn Grafiken nach der Überarbeitung
visuell geprüft, keine Text-/Element-Überlappungen mehr.

**Abnahme:** `python main.py` (alle 10 Schritte), zweimal hintereinander →
`git status` sauber; kein Diagramm enthält einen Titel-Header oder eine
Footer-Zeile; kein deutsches Wort außerhalb von Klassen-/Property-Namen
und CSV-Beispielwerten.

### S12 -- 02 Fuzzy-Matching-Mechanismus (neu)

**Ziel:** zeigen, *wie* `rapidfuzz.fuzz.token_sort_ratio` eine
Match-Entscheidung trifft -- nicht nur, dass es sie trifft (das leistete
bereits die Pipeline-Übersicht in 01).

**Substanz:** vier-stufiger Mini-Ablauf (Tokenise → Sort tokens → Rejoin
→ Score) plus vier Beispielzeilen mit **echten, berechneten** Scores (nicht
erfunden): `rapidfuzz` lokal installiert und
`fuzz.token_sort_ratio(a, b)` für vier String-Paare ausgeführt, die den
im Paper genannten Fällen entsprechen ("Landkreis X"-Präfixproblem;
die im Paper explizit genannten Alias-Beispiele "MVP" und "sommerda").
Ergebnisse: `Kreis Ostprignitz-Ruppin` vs. `Ostprignitz-Ruppin` = 85.71
(besteht); `Landkreis Havelland` vs. `Havelland` = 64.29 (scheitert, braucht
Präfix-Strip); `sommerda` vs. `Sömmerda` = 75.00 (scheitert knapp an der
Gemeinde-Schwelle 82, braucht Alias); `MVP` vs.
`Mecklenburg-Vorpommern` = 16.00 (scheitert deutlich, nur Alias hilft).
Jede Zeile: Gauge-Balken (0--100) mit Schwellwert-Markierung, PASS/FAIL-
Badge, Konsequenz-Text.

**Abnahme:** `python main.py --only 02`, 2 Dateien; alle vier Scores
stimmen mit einem frischen `rapidfuzz`-Lauf überein (siehe Docstring).

### S13 -- 09 Kulturen: Modellierung statt Statistik (neu)

**Ziel:** Florians Korrektur umsetzen -- "Kulturen" zeigt wieder, *wie*
Kulturgruppe modelliert ist, nicht *wie oft* welcher Wert vorkommt.

**Substanz:** UML-artige Attributbox für Kulturgruppe (`crm:E4_Period`,
`rdfs:label`, `bb5kbc:hasExternalIdentifier`) links; rechts ein Kasten, der
den Dedup-Mechanismus (Regel 2/3, MD5-Hash der ersten 8 Zeichen) erklärt
und die reale 9-Werte-Zahl als einzelnen Grounding-Satz nennt (nicht als
Diagramm). Unten links eine Fan-in-Illustration (vier Beispiel-Fundstellen
→ ein geteilter Kulturgruppe-Knoten → eine Wikidata-QID); unten rechts ein
kompakter Reminder des "?"-Mechanismus aus 05 (zwei Knoten, eine QID), mit
Verweis auf die ausführliche Grafik statt Wiederholung.

**Erledigt 2026-09-10b:** erster Entwurf ließ die zweizeilige Caption über
den Fundstelle-Chips in die erste Box hineinlaufen (zu knapper Abstand) --
Caption-Position nach oben verschoben, Chip-Reihen leicht neu zentriert.

**Abnahme:** `python main.py --only 09`, 2 Dateien; keine Statistik-Balken
mehr im Bild; die reale 9-Werte-Aussage ist ein Satz, nicht das
Bildzentrum; keine Überlappungen.

### S14 -- Bugfix: Auto-Fit-Schriftgröße

**Ziel:** den beim Review gefundenen Text-Overflow in den "geteilt"-Kreisen
systematisch beheben, nicht nur an den sichtbar betroffenen Stellen
flicken.

**Substanz:** `svg_hash_node` misst jetzt die tatsächliche Textbreite
(`text_width()`) gegen die verfügbare Sehnenbreite des Kreises und senkt
die Schriftgröße in 0.5px-Schritten bis zu einer Untergrenze (Titel 11px,
Subtitle 8px). Reicht das nicht, wird das Subtitle am ausgewogensten
Leerzeichen in zwei Zeilen gebrochen (beide Zeilen erneut einzeln
gefittet). `svg_box` bekam dieselbe Fit-Logik für Titel/Subtitle/
Stereotype, ohne Zweizeilen-Fallback (Boxen sind breiter, ein Overflow
dort war beim Review nicht aufgefallen, aber dieselbe Robustheit schadet
nicht angesichts variabler Sprachlängen).

**Erledigt 2026-09-10c:** Ursache war eine feste Schriftgröße (13px Titel,
10.5px Subtitle) unabhängig vom tatsächlichen Kreisradius und von der
Textlänge -- fiel bei "shared · bundesland_{hash}" (26 Zeichen, Radius
58px) am deutlichsten auf, war aber latent auch in 07/08/09 vorhanden
(dort nur, weil die Radien dort zufällig etwas größer gewählt waren,
nicht weil das Problem grundsätzlich anders lag). Nach dem Fix: 00 (DE)
nachgeprüft, Zweizeilen-Umbruch greift sauber, keine Überlappung mit
Nachbarknoten.

**Abnahme:** `python py/step_00_fundstelle_hub.py`, visuell geprüft: kein
Text kreuzt mehr eine Kreis-/Kastenkontur.

### S15 -- Bilingual: alle 10 Grafiken DE + EN

**Ziel:** Florians Wunsch nach zwei kompletten Sprachversionen je Grafik
umsetzen, inklusive übersetzter Klassen-/Property-Namen in der
Englisch-Fassung, ohne den Code je Sprache zu duplizieren.

**Substanz:** `vu.t(lang, de, en)` als generischer Zweisprachigkeits-Helfer
(funktioniert auch mit Listen, nicht nur Strings -- praktisch für
mehrzeilige Absätze). `CLASS_EN`/`PROP_EN`-Glossare plus `vu.cls()`/
`vu.prop()` für die 15 Klassen- und 19 Property-Namen der Ontologie.
Jede `step_*.py`-Datei: `build()` → `build(lang: str = "en")`, jede
zu übersetzende Zeichenkette durch `tt(de, en)` (lokale Closure um
`vu.t`) ersetzt; `main()` ruft `build("de")` und `build("en")` auf und
hängt die Dateilisten zusammen. `write_figure()` bekommt den
sprachtragenden Dateinamen direkt übergeben (`f"{name}.{lang}"`) --
keine Änderung an der Utils-Schreibfunktion nötig.

**Entscheidung, was übersetzt wird:** siehe A4. Kurzfassung: Bezeichner
(Klassen, Properties) ja, weil Florian das explizit so wollte ("tun wir
mal so als wäre das Label im Graph zweisprachig"); CSV-/Kulturwerte nein,
weil es echte Quelldaten sind, kein Beschriftungstext.

**Erledigt 2026-09-10c:** zwei kleinere Bugs beim Durchgehen gefunden und
behoben, jeweils sofort:
- 02-fuzzy-matching: das deutsche PASS/FAIL-Badge ("DURCHGEFALLEN", 13
  Zeichen) war breiter als der für das englische "FAIL" (4 Zeichen)
  bemessene Abstand zur Notiz-Spalte -- Badge-Breite jetzt dynamisch
  (`text_width()`-basiert), Notiz-Spalte von x=1260 auf x=1300 verschoben.
- 02-fuzzy-matching: die Sommerda-Notiz nannte im Englischen weiterhin
  "the Gemeinde threshold" statt "the Municipality threshold" -- Notiztext
  auf einen `{level}`-Platzhalter umgestellt, der mit `vu.cls()` gefüllt
  wird, statt die Übersetzung hart in den Fließtext zu schreiben.

Außerdem beim Schreiben von `PRIMER.md` selbst ein Fehler gefunden: die
Datei enthielt 133 literale `\u00fc`-artige Escape-Sequenzen statt echter
Umlaute (ein Python-Autoring-Reflex, der in einer Markdown-Datei nicht
interpretiert wird, anders als in `.py`-Stringliteralen). pauschal per
Skript durch die echten Unicode-Zeichen ersetzt; alle anderen `.md`-Dateien
im Repo waren nicht betroffen (geprüft).

Alle zehn Grafiken je zweimal (DE/EN) gerendert und visuell geprüft --
keine offenen Überlappungen mehr gefunden.

**Abnahme:** `python main.py`, 10 Schritte × 4 Dateien = 40 Dateien (20
SVG + 20 PNG); zweimal hintereinander → `git status` sauber (SHA-256 je
Datei verifiziert); jede Grafik existiert als `.de.` und `.en.`-Paar.

### S16 -- Bugfix: Python-3.10-Kompatibilität (f-string-Backslash)

**Ziel:** den von Florian gemeldeten `SyntaxError` beheben, der `python
main.py` auf seiner Windows/Python-3.10-Umgebung nach Schritt 04 abbrechen
ließ.

**Substanz:** Python verbietet vor Version 3.12 (PEP 701) einen Backslash
innerhalb der `{...}`-Ausdrucksklammer eines f-strings -- auch wenn der
Backslash nur Teil eines verschachtelten String-Literals ist, wie bei
`{tt("\u201eSBK\u201c ...", ...)}`. Die Sandbox hier läuft auf Python
3.12.3, wo das erlaubt ist, weshalb der Fehler beim Bauen in S15 nicht
auffiel. Ein AST-basierter Scanner (`ast.walk` über jeden `JoinedStr`-Knoten,
`ast.get_source_segment` auf dessen `FormattedValue`-Kindern, Suche nach
`\` im extrahierten Quelltext) fand sechs betroffene Stellen in drei
Dateien -- präziser als ein textbasiertes Grep, weil er den tatsächlichen
Python-Ausdrucksteil isoliert statt nur nach verdächtigen Zeichenfolgen zu
suchen. An jeder Stelle: die `tt(...)`-Übersetzung in eine lokale Variable
vorgezogen, im f-string nur noch `{variable}` referenziert -- keine
inhaltliche Änderung, nur eine Umstrukturierung des Python-Ausdrucks.

**Betroffene Dateien:**
- `step_05_uncertainty_markers.py` (3 Stellen: `sbk_label`, `grab_label`,
  `grab_type_note`)
- `step_08_dating_entities.py` (1 Stelle: `qid_all_label`)
- `step_09_kulturen.py` (2 Stellen: `one_qid_label`/`per_site_label`,
  `same_qid_note`)

**Erledigt 2026-09-10d:** Python 3.10 war in der Sandbox nicht
installierbar (kein passendes Paket im Ubuntu-24.04-Repository, keine
Deadsnakes-PPA im erlaubten Netzwerkzugriff) -- der Fix wurde daher nicht
gegen einen echten 3.10-Interpreter getestet, sondern gegen die exakte
Grammatikregel verifiziert (AST-Scan nach dem Fix: 0 verbleibende Treffer
in allen `step_*.py` und `main.py`). `python main.py` in der Sandbox
danach erneut komplett durchlaufen lassen (Python 3.12), Ergebnis
byte-identisch zu vorher -- die Umstrukturierung hat den Output nicht
verändert, nur die Syntax.

**Abnahme:** `python main.py` läuft auf Florians Python 3.10 ohne
`SyntaxError` durch (von ihm zu bestätigen -- siehe PATCH-README.md
"Verified here" für die Grenzen der hiesigen Prüfung).

### S17 -- Bugfix: Patch S16 war unvollständig (utils.py fehlte)

**Ziel:** den Folgefehler beheben, den der S16-Patch verursacht hat:
`module 'bb5kbc_visuals_utils' has no attribute 't'` in den Schritten 05,
08, 09.

**Ursache:** S16 lieferte nur `step_05/08/09_*.py` aus, in der Annahme,
Florians Repo enthalte bereits die bilinguale `bb5kbc_visuals_utils.py`
(mit `t()`/`cls()`/`prop()`/Glossaren). Das war falsch -- sein Repo stand
tatsächlich noch auf dem allerersten, einsprachigen Stand (Schritte
00--04, 06, 07 liefen deshalb weiter mit "2 file(s)" statt der erwarteten
4, ohne Fehler, weil ihr `build()` kein `lang`-Argument braucht). Der
S16-Patch hat drei Schritt-Dateien durch bilinguale Versionen ersetzt,
die `vu.t()` aufrufen -- ohne die dafür nötige Utils-Version mitzuliefern.
Ergebnis: ein inkonsistentes Repo, in dem 7 Schritte einsprachig und 3
Schritte (kaputt) bilingual waren.

**Substanz:** dieses Mal das vollständige, konsistente Quell-Set liefern:
`bb5kbc_visuals_utils.py` (mit `t()`/`cls()`/`prop()`/`CLASS_EN`/`PROP_EN`
und dem Auto-Fit-Fix aus S14) plus alle zehn `step_*.py` plus `main.py`
plus `README.md` -- nicht nur die zuletzt kaputten Dateien. Lehre für
künftige Patches an diesem Repo: vor dem Zusammenstellen eines Patches
den tatsächlichen Stand des Zielrepos erfragen oder zumindest nicht
stillschweigend voraussetzen, dass frühere Lieferungen vollständig
angekommen sind.

**Abnahme:** `python main.py` auf Florians Maschine liefert 10 × 4 = 40
Dateien ohne Fehler.

## Teil D -- Offene Punkte

- **Pipeline-Architektur neu im Hausstil.** `architecture.mmd` (Paper
  Abb. 4) existiert bereits inhaltlich vollständig -- bräuchte nur die
  `bb5kbc_visuals_utils`-Palette und das randlose 7:4-Format.
- **N4O-KG-Publikationspipeline.** `bb-5kbc-public` ist geklont, aber noch
  für keine Grafik verwendet: `metadata.yaml` → SHACL →
  `n4o-collection.ttl`, mit den echten Zahlen 28 531 Tripel / 33 Klassen /
  81 Properties aus dessen README.
- **PROV-O-Verkettung über zwei Pipeline-Stufen.** Die Cross-Namespace
  `wasInformedBy`-Verbindung zwischen `csv_enrichment_run.ttl` und
  `csv_to_lod_run.ttl` (Paper Abschnitt 6).
- **SHACL-Validierungs-Gate.** Warning- vs. die eine harte Violation-Regel.
- **Mehrfachvererbung als Bäume neu gezeichnet.** Paper Abb. 2 (vier
  Klassen als Baum) wäre eine Ergänzung zu 04, nicht redundant.
- **Statistik-/Kartenfolie.** 540 Fundstellen, 350 DE + 178 PL über neun
  Wojewodschaften -- noch nicht visualisiert. (Das wäre der richtige Ort
  für eine Statistik-Grafik, falls gewünscht -- nicht mehr 09-kulturen.)

Wenn einer dieser Punkte zum nächsten Schritt wird: nach S17 einsortieren
(S18, S19, …), hier streichen, in Teil B eintragen.

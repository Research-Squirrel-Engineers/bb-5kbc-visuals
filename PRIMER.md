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

**Befund 2026-09-10f (neun weitere Grafiken angefragt):** Florian fragte
nach weiteren Visualisierungsideen; auf die Konzeptliste (Pipeline-
Architektur, literaturbezogene Anreicherung, PROV-O-Verkettung,
Validierungsschichten, Vererbungsbäume, N4O-Publikationspipeline,
persistente URIs, Statistik-Infografik, Karte) antwortete er "kannst du
alles so umsetzen" und wünschte sich bei der Statistik/Karte explizit
beides (Infografik UND Karte, nicht nur eins). Zusätzliche Quellen
dafür in dieser Session herangezogen: `bb-5kbc-public/README.md` (frisch
gefetcht, nicht aus dem Gedächtnis -- lieferte präzisere Zahlen als die
früheren Notizen: 28 531 Tripel, CRM-Alignment 16/21 Domainklassen, die
Time-Slice-Beispielzahlen); `data/fst_wgs84.csv` direkt ausgewertet für
17 (regionale Verteilung) und 18 (echte WGS84-Koordinaten aller 540
Fundstellen) -- dabei eine echte Diskrepanz zum Paper-Text gefunden (10
Wojewodschaften in den Daten, nicht 9 wie im Fließtext) und dokumentiert
statt stillschweigend "korrigiert".

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
- **Nur orthogonale Linien (2026-09-15).** Jede Verbindung zwischen zwei
  Boxen ist entweder eine gerade Linie (beide Enden auf gleicher x- oder
  y-Achse) oder ein rechtwinkliger Verbinder (`svg_arrow_L` für einen
  Knick, `svg_arrow_elbow`/`svg_arrow_elbow_v` für eine gemeinsame
  Schiene bei mehreren Verbindungen durch denselben engen Bereich) --
  nie eine Diagonale. Bei mehreren Linien, die exakt am selben Punkt
  enden, `marker=None` für alle bis auf einen letzten kurzen Hop
  verwenden, sonst kollidieren zwei Pfeilspitzen zu einem "X" (siehe
  S33 für den Fund).
- **Keine internen Verweise im gerenderten Text (2026-09-15).** Keine
  "Regel N", "Tab. N", "§N", "Sektion N" und keine Querverweise auf
  andere Diagrammnummern ("siehe 05-...", "(08)") in Text, der tatsächlich
  ins SVG gerendert wird -- jedes Diagramm muss für sich allein
  verständlich sein. Solche Referenzen sind in Docstrings weiterhin
  erlaubt (die sind nicht Teil des Bildes, sondern Dokumentation für
  künftige Bearbeitung).

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
| **Umfang: neun weitere Grafiken (10--18)** | **Revision 2026-09-10f:** alle vier Teil-D-Punkte aus der vorigen Revision umgesetzt, plus Statistik-Infografik und Karte (Florian wollte explizit beides). Teil D ist nach dieser Revision leer -- neue Ideen kommen erst wieder durch ein neues Gespräch | 2026-09-10f |
| **`site_coordinates.csv`: dokumentierte Ausnahme vom "kein Runtime-Parsing"-Prinzip** | **Revision 2026-09-10f:** 18-site-map ist der einzige Schritt, der eine Datei aus `data/raw/` zur Laufzeit einliest statt nur beim Autoring zu lesen -- 540 reale Koordinaten lassen sich nicht von Hand als Geometrie eintragen wie ein Dutzend Kästen. Die Datei ist einmalig aus `fst_wgs84.csv` extrahiert und eingecheckt, keine Live-Abhängigkeit von `bb-5kbc-sites` zur Laufzeit | 2026-09-10f |
| **Karte: schematischer Scatterplot, keine projizierte Karte** | **Revision 2026-09-10f:** ohne Basiskarten-/Grenzdaten im Repo wäre eine "echte" Karte (mit Küstenlinien, Grenzen) Fabrikation. Stattdessen: echte WGS84-Koordinaten aller 540 Fundstellen, äquirechteckig mit cos(mittlere Breite)-Korrektur geplottet, explizit als schematisch beschriftet | 2026-09-10f |
| **Statistik-Infografik: echte Datenwerte statt Paper-Prosa** | **Revision 2026-09-10f:** regionale Verteilung aus `fst_wgs84.csv` direkt berechnet (nicht aus dem Paper-Fließtext übernommen) -- ergab 362/178 statt 350/178 (Land-Spalte hat 12 leere Zellen, die erst beim LOD-Build auf Deutschland zurückfallen) und 10 statt 9 polnische Wojewodschaften (Woj. Pomorskie, 3 Fundstellen, real vorhanden). Beide Diskrepanzen zum Paper-Text in der Grafik selbst benannt, nicht still "korrigiert" | 2026-09-10f |

| **Rechtwinklige Linienführung für weite Verbindungen** | **Revision 2026-09-11:** neue Utils-Funktionen `svg_arrow_elbow` (horizontale Schiene) und `svg_arrow_elbow_v` (vertikale Schiene) -- für Verbindungen, die sonst diagonal durch fremde Boxen/Container liefen. Erste Anwendung in 10 (zwei Verbindungen) und 15 (Fan-out von metadata.yaml als "Bus" statt Diagonalen-Fächer) | 2026-09-11 |
| **Redundante Pfeile durch Text ersetzen statt umrouten** | **Revision 2026-09-11:** in 12 erzeugte eine gestrichelte `wasDerivedFrom`-Linie eine Kreuzung, obwohl der Fakt bereits als Text ("beide: wasDerivedFrom → fst_wgs84.csv") vorhanden war -- Linie ersatzlos gestrichen statt umgeroutet. Nicht jede Beziehung braucht einen gezeichneten Pfeil, wenn ein Satz genügt und das Zeichnen nur Unordnung erzeugt | 2026-09-11 |
| **18: echter Baselayer aus Natural-Earth-Daten** | **Revision 2026-09-11:** drei neue Dateien (`admin_boundaries.json`, `country_boundaries.json`, `major_cities.csv`), einmalig von `raw.githubusercontent.com/nvkelso/natural-earth-vector` geladen, gefiltert auf den relevanten Ausschnitt, eingecheckt. Zweite dokumentierte Ausnahme vom "kein Runtime-Parsing"-Prinzip (neben `site_coordinates.csv`) -- aus demselben Grund: echte Grenz-/Stadtgeometrie lässt sich nicht von Hand als SVG-Boxen nachbauen | 2026-09-11 |
| **Kein Hillshade** | **Revision 2026-09-11:** bewusst nicht umgesetzt. Echtes Relief-Shading braucht ein Höhenmodell (SRTM/GMTED) und eine Raster-Rendering-Pipeline, die dieses Repo nicht hat; Natural Earths eigene Shaded-Relief-Raster sind selbst bei grober Auflösung zu groß (zig bis hunderte MB), um sie hier sinnvoll einzubinden. Ein erfundenes Relief ohne echte Höhendaten wäre Fabrikation -- die Grafik sagt das stattdessen direkt und verweist auf ein echtes GIS-Tool für diesen speziellen Layer | 2026-09-11 |

### A5 Was in welchem Chat hochgeladen wird

```
robocopy . ..\bb5kbc-visuals-bundle /E /XD .git __pycache__ fonts
Compress-Archive -Path ..\bb5kbc-visuals-bundle\* -DestinationPath ..\bb5kbc-visuals-bundle.zip -Force
```

Nicht hochladen: `fonts/*.ttf`, `__pycache__/`, `.git/`.

### A6 IRI-Landkarte

Entfällt -- dieses Repo publiziert kein eigenes RDF.

**Befund 2026-09-11 (Florian: committed, erste Feinjustierung):** "erstmal
gut ein paar design buggs sind überall drin, aber dazu später" -- generelles
Signal zurückgestellt (keine Einzelpunkte genannt, also nichts vorsorglich
geändert), aber zwei konkrete Punkte sofort adressiert: (1) in 10/12/15
laufen Linien "durcheinander" -- diagonale Verbindungen kreuzen durch
fremde Boxen/Container; (2) 18 (Karte) braucht dringend einen "Baselayer",
konkret genannt: Landesgrenzen, Großstädte, Hillshade. Für (2) wurden
reale Natural-Earth-Daten (public domain) über GitHub geladen (Grenzen,
Großstädte); Hillshade wurde bewusst NICHT nachgebaut, da dafür ein
echtes Geländemodell (SRTM/GMTED) und eine Raster-Rendering-Pipeline
nötig wären, die dieses SVG-basierte Repo nicht hat -- ein erfundenes
Relief wäre genau die Art von vorgetäuschter kartografischer Präzision,
die dieses Projekt sonst vermeidet. Stattdessen ein ehrlicher Hinweis
direkt in der Grafik.

**Befund 2026-09-11b (Florian, mit Screenshot von 06-uncertainty-dating):**
"insbesondere hier der free text irritiert. kannst du da nochmal schauen
auf welcher Grundlage du da welche Diagramme gebaut hast?" -- Nachprüfung
ergab: die Freitext-Beispiele in 06 ("grob", "unsicher", "Schaetzung")
waren erfunden, nicht aus der CSV. Der Docstring hatte fälschlich
"real heterogeneous CSV values" behauptet, ohne dass die Datei je
geöffnet worden war. Vollständige Aufarbeitung: siehe S31.

**Befund 2026-09-15 (Florian, nach dem letzten Commit):** drei Aufträge
auf einmal: (1) "kannst du bitte alle anderen grafiken auch überprüfen?"
-- die Datengrundlagen-Prüfung aus S31 sollte über die vier
Datierungs-Grafiken hinaus gehen; (2) "die linien immer 'nur' vertikal
und horizontal zeichnen, nicht diagonal" -- neue verbindliche
Layout-Regel für alle Grafiken, nicht nur die drei zuvor gemeldeten; (3)
"Dinge wie 'Regel x' oder so rausnehmen, die Grafiken sollen für sich
alleine stehen, teilweise stehen auch texte in linien" -- interne
Verweise (Regel-Nummern, Tab.-Nummern, §-Abschnitte, Querverweise auf
andere Diagrammnummern) sollen aus jedem gerenderten Text verschwinden,
nicht nur aus Docstrings. Vollständige Umsetzung: siehe S32--S34.

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
| S18 | 10 Pipeline-Architektur (Fig. 4 neu gezeichnet) | `step_10_pipeline_architecture.py` | S17 | erledigt 2026-09-10f |
| S19 | 11 Literaturbezogene Anreicherung (Modus A) | `step_11_literature_enrichment.py` | S17 | erledigt 2026-09-10f |
| S20 | 12 PROV-O-Verkettung über zwei Stufen | `step_12_prov_chaining.py` | S17 | erledigt 2026-09-10f |
| S21 | 13 Vierschichtige Validierung (4+1 Sektionen) | `step_13_validation_layers.py` | S17 | erledigt 2026-09-10f |
| S22 | 14 Vererbungsketten als Bäume | `step_14_inheritance_trees.py` | S17 | erledigt 2026-09-10f |
| S23 | 15 N4O-KG-Publikationspipeline | `step_15_n4o_publication.py` | S17 | erledigt 2026-09-10f |
| S24 | 16 Persistente URIs (w3id.org) | `step_16_persistent_uris.py` | S17 | erledigt 2026-09-10f |
| S25 | 17 Statistik-Infografik (echte Zahlen) | `step_17_stats_infographic.py` | S17 | erledigt 2026-09-10f |
| S26 | 18 Karte (echte WGS84-Koordinaten) | `step_18_site_map.py` | S17 | erledigt 2026-09-10f |
| S27 | Bugfix: Python-3.10-Backslash erneut in S23 gefunden | `step_15_n4o_publication.py` | S18--S26 | erledigt 2026-09-10f |
| S28 | Linienführung in 10/12/15 überarbeitet | `bb5kbc_visuals_utils.py`, `step_10/12/15_*.py` | S27 | erledigt 2026-09-11 |
| S29 | 18: echter Baselayer (Grenzen, Großstädte); kein Hillshade | `step_18_site_map.py` + 3 neue Geodaten-Dateien | S28 | erledigt 2026-09-11 |
| S30 | Bugfix: Python-3.10-Backslash erneut in S29 gefunden | `step_18_site_map.py` | S29 | erledigt 2026-09-11 |
| S31 | Korrektur: erfundene Datierungs-Beispielwerte durch echte ersetzt | `step_05/06/08/09_*.py` | S30 | erledigt 2026-09-11 |
| S32 | Interne Verweise (Regel/Tab./§/Querverweise) aus gerendertem Text entfernt | `step_02/06/07/09/10/13/14_*.py` | S31 | erledigt 2026-09-15 |
| S33 | Alle Diagramme auf orthogonale Linienführung umgestellt | `bb5kbc_visuals_utils.py`, `step_00/01/03/04/05/06/08/09/10/11/12/15_*.py` | S32 | erledigt 2026-09-15 |
| S34 | Korrektur: erfundenes Beispiel in 11 (Zeile 214/Q100) als illustrativ gekennzeichnet | `step_11_literature_enrichment.py` | S33 | erledigt 2026-09-15 |
| S35 | 03 nach Florians Rückmeldung noch mal überarbeitet -- zwei Ursachen für "immer noch durcheinander" behoben | `step_03_application_ontology.py` | S34 | erledigt 2026-09-15 |
| S36 | Systematischer bend=h/v-Fehler in `svg_arrow_L` gefunden und über 8 Grafiken hinweg behoben | `step_00/01/03/04/06/10/12/15_*.py` | S35 | erledigt 2026-09-15 |
| S37 | Sichtbares "Herausragen" vor dem Knick ergänzt (00, 03) | `step_00_fundstelle_hub.py`, `step_03_application_ontology.py` | S36 | erledigt 2026-09-15 |
| S38 | Label-Fehlplatzierung im Fundstelle-Fan-out behoben (03) | `step_03_application_ontology.py` | S37 | erledigt 2026-09-15 |
| S39 | Rückwärtslaufende Linie zum wd-Badge in 05 (rechtes Panel) behoben | `step_05_uncertainty_markers.py` | S38 | erledigt 2026-09-15 |
| S40 | Balken-Überlauf in 06 behoben, Linien-Fix aus S36 re-bestätigt | `step_06_uncertainty_dating.py` | S39 | erledigt 2026-09-15 |
| S41 | 19 Allen-/Freksa-Relationen (neu, Skizze) | `step_19_allen_freksa_relations.py` | S17 | erledigt 2026-09-15 |

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

### S18-S26 -- neun weitere Grafiken (10--18)

Florian fragte nach weiteren Visualisierungsideen; die Antwort listete neun
Konzepte in fünf Themenblöcken (Pipeline & Anreicherung, Validierung &
Qualität, Modellierung, Publikation & FAIR-Infrastruktur, Kontext).
Florian: "Klingt alles gut ... kannst du alles so umsetzen" -- bei Punkt E
(Kontext) explizit beide Unterpunkte (Infografik *und* Karte).

**Gemeinsame Substanz aller neun:** exakt dasselbe bilinguale Muster wie
00--09 (`build(lang="en")`, `vu.t()`/`vu.cls()`/`vu.prop()`, kein
Header/Footer, Auto-Fit-Schriftgröße). Jede Grafik einzeln geplant, gebaut,
gerendert, visuell geprüft, Fehler sofort behoben -- siehe die einzelnen
Befunde unten.

**10 Pipeline-Architektur.** 1:1 aus `architecture.mmd` (18 Knoten, ~20
Kanten). Erster Entwurf zu kompakt (~40 % des Canvas leer, viele
Linien liefen quer durch fremde Kästen) -- Y-Koordinaten neu verteilt,
zweiter Durchlauf deutlich lesbarer.

**11 Literaturbezogene Anreicherung.** Die *andere* Hälfte der
Anreicherung (01/02 zeigen nur die geografische) -- Modus A,
Vier-Fälle-Tabelle (Tab. 2), Beispiel für den Fall "overwritten". Zwei
Kollisionen gefunden und behoben: das "Modus A"-Label saß auf den
kreuzenden Pfeilen; der Fußtext im Beispielblock überlappte die untere
Box.

**12 PROV-O-Verkettung.** Namespace-Grenze als zwei nebeneinanderliegende
gestrichelte Container dargestellt, mit der zentralen LOD-Activity als
Hub. Zwei Overflow-Bugs: die "Agents"-Box lief zunächst weit über den
rechten Rand hinaus (falsch berechnetes `acx`), nach der ersten Korrektur
überlappte sie stattdessen die Activity-Box selbst -- erst beim dritten
Anlauf mit festen statt abgeleiteten Koordinaten sauber.

**13 Vierschichtige Validierung.** Tab. 8 als Tabelle (Sektionen 1--4b)
plus ein Panel zur harten SHACL-Regel (`hatFID`) vs. Warnings. Keine
Layoutfehler beim ersten Rendern.

**14 Vererbungsketten als Bäume.** Ursprünglich als volle Drei-Welten-Bäume
geplant (CRM-Kette + Seiten-Chips für FSL/LADO/PROV/OWL-Time je Klasse) --
erster Entwurf hatte gravierende Fehler: Seiten-Chips liefen bei der
letzten Spalte weit über den Canvas-Rand hinaus, und `svg_box`s
Stereotyp-Text überlappte den Titel, weil die Boxen für zwei Textzeilen
zu niedrig waren. Statt einzeln zu flicken: Umfang bewusst verkleinert
auf die reine CRM/CRMsci-Kette (die Seiten-Äste zeigt bereits 04) -- damit
verschwanden beide Fehlerursachen zugleich, und die eigentliche Aussage
(Kettentiefe variiert von 2 bis 8 Hops) kommt klarer heraus als im
ursprünglich überladenen Entwurf.

**15 N4O-KG-Publikationspipeline.** `bb-5kbc-public/README.md` frisch
gefetcht (nicht aus dem Gedächtnis) für die genauen Zahlen und den
Freshness-Check-Mechanismus. Zwei Kollisionen: sowohl die
"Der Graph, in Zahlen"-Box als auch die "Was der Build prüft"-Box nutzten
`svg_box`s automatisch zentrierten Titel *und* zusätzlich manuell
platzierten Text an nahezu derselben Position -- in beiden Fällen auf
reine `<rect>` + manuelles Text-Layout umgestellt. Dabei auch eine
funktionslose Pfeil-Anweisung mit vertauschten Koordinaten entfernt.

**16 Persistente URIs.** Zwei-Regel-`.htaccess` (Ontologie-Begriffe vs.
Daten-Ressourcen), beide über 303 See Other. Keine Layoutfehler.

**17 Statistik-Infografik.** `fst_wgs84.csv` direkt mit `Counter()`
ausgewertet statt Paper-Prosa zu übernehmen -- siehe A1/A4 für die dabei
gefundene Diskrepanz (362 statt 350 Fundstellen in Deutschland, 10 statt 9
Wojewodschaften). Keine Layoutfehler.

**18 Karte.** Bewusste Ausnahme vom Repo-Prinzip "kein Runtime-Parsing"
(siehe A4): `site_coordinates.csv` wird zur Baubuildzeit eingelesen, weil
540 reale Koordinaten nicht von Hand platzierbar sind. Schematischer
äquirechteckiger Scatterplot (Longitude × cos(mittlere Breite)), explizit
nicht als projizierte Karte ausgegeben, da keine Basiskarten-/Grenzdaten
im Repo liegen. Zwei kleine Korrekturen: ein Datenpunkt lag exakt am
oberen Rand der Plot-Fläche (20px Padding ergänzt, damit Extrempunkte
nicht die Rahmenlinie durchstoßen); der Nordpfeil saß zunächst zufällig
über einem echten Datenpunkt (in die leere obere linke Ecke verschoben).

**Abnahme (alle neun):** `python main.py`, Schritte 10--18 melden je
"4 file(s) written"; zweimal hintereinander → `git status` sauber.

### S27 -- Bugfix: Python-3.10-Backslash erneut gefunden (in S23)

**Ziel:** denselben Fehlertyp wie in S16 systematisch ausschließen, nicht
nur an den drei damals gemeldeten Stellen.

**Substanz:** der AST-Scanner aus S16 (Suche nach Backslashes im
Ausdrucksteil jedes `JoinedStr`/`FormattedValue`-Knotens) diesmal über
*alle* 19 `step_*.py` plus `main.py` laufen lassen, nicht nur über die
zuletzt geänderten Dateien. Fund: eine Stelle in
`step_15_n4o_publication.py` (`{vu.xml_escape("\u2022 " + line)}` direkt
im f-string-Ausdruck). Gleiches Muster wie zuvor: Ausdruck vorher in eine
Variable gezogen (`bullet_line = vu.xml_escape(...)`), im f-string nur
noch `{bullet_line}` referenziert.

**Erledigt 2026-09-10f:** nach dem Fix erneuter Scan über alle 19+1
Dateien -- 0 Treffer. Betroffene Grafik danach neu gerendert und mit der
Vorher-Version verglichen: inhaltlich identisch, nur die Ausdrucksform im
Python-Quelltext hat sich geändert.

**Lehre für künftige Schritte:** den AST-Scan ab jetzt routinemäßig nach
*jeder* Session laufen lassen, die neue oder geänderte `step_*.py`-Dateien
enthält -- nicht erst, wenn ein Fehlerbericht kommt. Ein Einzeiler dafür:

```
python3 -c "
import ast, glob
def scan(p):
    src = open(p, encoding='utf-8').read()
    t = ast.parse(src, filename=p)
    return [(p, v.lineno, ast.get_source_segment(src, v.value))
            for n in ast.walk(t) if isinstance(n, ast.JoinedStr)
            for v in n.values if isinstance(v, ast.FormattedValue)
            and '\\\\' in (ast.get_source_segment(src, v.value) or '')]
hits = [h for f in glob.glob('py/*.py') + ['main.py'] for h in scan(f)]
print(hits or 'OK: keine Backslashes in f-string-Ausdruecken')
"
```

**Abnahme:** `python main.py` läuft auf Python 3.10 durch (von Florian zu
bestätigen).

### S28 -- Linienführung in 10/12/15 überarbeitet

**Ziel:** Florians Rückmeldung umsetzen, dass in den Grafiken 10, 12, 15
Linien "durcheinanderlaufen".

**Substanz:** zwei neue generische Verbinder in den Utils:
`svg_arrow_elbow(x1,y1,x2,y2,rail_y)` routet rechtwinklig über eine
gemeinsame horizontale Schiene (runter/rauf -- quer -- rauf/runter),
`svg_arrow_elbow_v` dasselbe über eine vertikale Schiene. Beide nehmen
optional ein Label, das auf dem geraden (Schienen-)Teilstück sitzt, wo am
meisten Platz ist.

**10 (Pipeline-Architektur):** zwei Verbindungen liefen komplett diagonal
durch fremde Container: `bb5kbc-ontology.ttl → bb5kbc_lod_pipeline.py`
schnitt quer durch die CSV-Anreicherungs-Box, `csv-mapping.md →
validate_lod.py` querte praktisch die gesamte Grafik einschließlich der
LOD-Transformation-Box. Beide auf Elbow-Routing umgestellt: die
Ontologie-Verbindung nutzt eine vertikale Schiene knapp links vom
LOD-Container (verläuft dadurch durch die Lücke zwischen den
Anreicherungs-Stages, nicht durch eine Box); die csv-mapping.md-Verbindung
nutzt eine horizontale Schiene unterhalb aller Boxen (dort ist durchgehend
freier Raum bis zur Legende).

**12 (PROV-Verkettung):** hier war die Ursache keine fehlende
Routing-Logik, sondern eine schlicht überflüssige Linie: die gestrichelte
`wasDerivedFrom`-Verbindung von den Output-Dateien zurück zu "Eingaben"
kreuzte die `wasInformedBy`-Linie und die `wasGeneratedBy`-Pfeile, obwohl
derselbe Fakt bereits als Text unter den Boxen stand ("beide:
wasDerivedFrom → fst_wgs84.csv"). Linie ersatzlos entfernt, Text um einen
Hinweis ergänzt, warum kein Pfeil gezeichnet ist.

**15 (N4O-Publikation):** vier Diagonalen von `metadata.yaml` zu den
`dist/*`-Zieldateien liefen als Fächer zusammen -- nicht falsch, aber
unruhig. Auf `svg_arrow_elbow_v` mit gemeinsamer Schiene umgestellt (ein
klarer "Bus" statt vier einzelner Diagonalen). Dabei auch bemerkt:
`bb5kbc-bundle.ttl` hatte bisher gar keine Verbindung zum Build-Prozess --
eine echte inhaltliche Lücke, nicht nur ein Linien-Problem. Ergänzt, auf
einer eigenen, parallel liegenden Schiene, damit sie nicht mit dem
metadata.yaml-Bus verschmilzt.

**Abnahme:** alle drei Grafiken (DE+EN) neu gerendert und visuell
geprüft -- keine Linie kreuzt mehr eine fremde Box; verbleibende
Kreuzungen sind Linie-mit-Linie an höchstens einem Punkt, nicht
Linie-durch-Box.

### S29 -- 18: echter Baselayer; kein Hillshade

**Ziel:** Florians Rückmeldung umsetzen: "18 benötigt dringend einen
'Baselayer' vllt eine Kombination aus Landesgrenzen, großen Städten und
Hillshade?"

**Substanz:** drei neue Datendateien, alle public domain (Natural Earth),
einmalig von `raw.githubusercontent.com/nvkelso/natural-earth-vector`
geladen (siehe `data/raw/README.md` für Details und Herkunfts-Commit):

- `admin_boundaries.json` -- Brandenburg + 4 Nachbar-Bundesländer, 10
  polnische Wojewodschaften (aus `ne_10m_admin_1_states_provinces`,
  gefiltert auf die Regionen, die im Datensatz tatsächlich vorkommen,
  Koordinaten auf 3 Nachkommastellen gerundet).
- `country_boundaries.json` -- Deutschland, Polen + 3 Nachbarländer für
  Kontext (aus `ne_50m_admin_0_countries`).
- `major_cities.csv` -- 23 Großstädte im Kartenausschnitt (aus
  `ne_10m_populated_places`, nach Bevölkerung sortiert, nah beieinander
  liegende Ballungsraum-Duplikate unterdrückt; Potsdam von Hand wieder
  ergänzt, da Brandenburgs eigene Hauptstadt trotz Nähe zu Berlin
  inhaltlich relevant für diesen Datensatz ist).

`step_18_site_map.py` liest jetzt vier Dateien zur Baubuildzeit
(`site_coordinates.csv` + die drei neuen) -- zweite dokumentierte
Ausnahme vom "kein Runtime-Parsing"-Prinzip, siehe A4.

**Kein Hillshade.** Bewusste Entscheidung, nicht umgesetzt: echtes
Relief-Shading braucht ein Höhenmodell (SRTM/GMTED oder ähnlich) und eine
Raster-Rendering-Pipeline; beides existiert in diesem SVG-basierten Repo
nicht. Eine Suche nach einer leichtgewichtigen Elevation-Quelle auf
GitHub blieb erfolglos -- verfügbare Optionen sind entweder Raster-Dateien
(GeoTIFF, zu groß für dieses Repo) oder API-Dienste außerhalb der
erlaubten Netzwerk-Domains. Ein erfundenes Relief ohne echte Höhendaten
wäre exakt die Art von vorgetäuschter kartografischer Präzision, die
dieses Projekt sonst konsequent vermeidet -- die Grafik benennt die
Lücke stattdessen direkt in ihrem eigenen Text.

**Erledigt 2026-09-11:** zwei Layout-Korrekturen nach dem ersten Rendern:
(1) ein Datenpunkt lag exakt auf der Nordpfeil-Position (Zufall der realen
Daten, nicht geplant) -- Nordpfeil in die leere obere linke Ecke verschoben;
(2) das Potsdam-Label überlappte das Berlin-Label (die Städte liegen real
nur ~25 km auseinander) -- Potsdam bekommt als einzige Stadt eine
Sonderbehandlung (Label unten-links statt rechts vom Punkt).

**Abnahme:** `python main.py --only 18`, 4 Dateien; DE+EN visuell
geprüft -- erkennbare Grenzlinien, lesbare Stadt-Labels, keine
Überlappungen, Ausdehnungs- und Quellenangabe vorhanden.

### S30 -- Bugfix: Python-3.10-Backslash erneut gefunden (in S29)

**Ziel:** wie S27, diesmal in der neuen `step_18_site_map.py`.

**Substanz:** derselbe Scan wie in S27 (siehe dortiger Einzeiler) über
alle Dateien laufen lassen -- Fund: eine Stelle
(`{tt("Gro\u00dfstadt", "major city")}` direkt im f-string-Ausdruck).
Gleiches Muster, gleicher Fix: Ausdruck vorher in `city_label` gezogen.

**Erledigt 2026-09-11:** nach dem Fix erneuter Scan über alle 19+1
Dateien -- 0 Treffer. Diese Art Fehler ist jetzt dreimal aufgetreten
(S16, S27, S30), immer in neu hinzugekommenem Code, nie in Code, der
schon einmal gescannt wurde. Das spricht dafür, den Scan tatsächlich als
letzten Schritt jeder Session einzubauen, nicht nur als Reaktion auf
einen Fehlerbericht -- siehe Teil D, falls das nicht zuverlässig genug
passiert.

**Abnahme:** `python main.py`, alle 19 Schritte, keine Fehler; zweimal
hintereinander → `git status` sauber.

### S31 -- Korrektur: erfundene Datierungs-Beispielwerte durch echte ersetzt

**Ziel:** Florians Nachfrage nachgehen, auf welcher Datengrundlage die
Datierungs-Grafiken tatsächlich gebaut wurden -- ausgelöst durch einen
Screenshot von 06-uncertainty-dating mit der konkreten Frage nach dem
Freitext.

**Befund:** kein einziges Diagramm dieser Session hatte tatsächlich
``fst_wgs84_lit_enriched.csv`` geöffnet. 06s Freitext-Chips ("grob",
"unsicher", "ca. 50 a", "unclear", "+/- 50 years", "Schätzung") waren
plausibel klingende Erfindungen, keine echten Werte -- und der eigene
Docstring behauptete das Gegenteil ("real heterogeneous CSV values").
Die echten Spalten zeigen ein anderes Bild:

- ``dating_certainty_start``/``_end``: **heute sauber**, nur 4 Muster
  („+/- 100/50/200/10 years“), alle 540 Zeilen gefüllt.
- ``dating_certainty_range``: **das** ist die tatsächlich heterogene
  Spalte -- 14 echte, größtenteils englische Sätze
  („low precision, as only stylistic dating“, n=299 von 540).
- ``bb5kbc-csv-issues.md`` Punkt 6 dokumentiert eine echte, aber
  **bereits behobene** Vorgeschichte: früher Deutsch/Englisch-Mischung
  bei genau den Spalten, die 06 fälschlich als aktuell heterogen
  darstellte („+ /- 100 Jahre“, 51 Zeilen, von Sophie vereinheitlicht).

Beim Gegenprüfen der in 05/08/09 verwendeten Beispiel-FIDs fielen
weitere, unabhängige Fehler auf: FID 12/57/101 (Diagramm 08/09) sind
reale Zeilen, aber kultur=SBK, nicht FBG wie dargestellt, mit erfundenen
Datierungswerten. FID 144 (Diagramm 05) ist real fundstellenart=Grab
(sicher) -- das genaue Gegenteil der dort gezeigten Unsicherheits-Markierung.

**Korrigiert, alle gegen ``fst_wgs84_lit_enriched.csv`` verifiziert:**

- **06**: komplett neu. UML-Box zeigt FID 1 ("Tüngeda", SBK, echte
  Start/End- und Certainty-Werte). Freitext-Panel zeigt die vier
  häufigsten echten ``dating_certainty_range``-Werte als Balken mit
  echten Häufigkeiten (n=299/203/24/1), plus die echte
  Cleanup-Geschichte von ``dating_certainty_start``/``_end`` unter
  Verweis auf ``bb5kbc-csv-issues.md`` #6.
- **08**: FBG durch SBK ersetzt -- alle 14 echten FBG-Fundstellen teilen
  zufällig exakt dieselbe Datierung (−4550/−3900), zeigen also keine
  Varianz; SBK hat real 7 distinkte Start/End-Paare unter 183
  Fundstellen. Drei echte FIDs (1, 6, 53) mit drei echten,
  unterschiedlichen Datierungen.
- **09**: die vier Fan-in-Beispiele sind jetzt echte FBG-FIDs (32, 33,
  61, 77 von 14 real existierenden); der Platzhalter-Hash
  ``kultur_a1b2c3d4`` durch den echten ``hashlib.md5("FBG")[:8]`` ersetzt.
- **05**: SBK/SBK?-Beispiel auf FID 1 (sicher) / FID 81 ("Gartz ?",
  real kultur=SBK?) umgestellt; Grab/Grab?-Beispiel auf FID 98 + 107
  (real fundstellenart=Grab) / FID 54 (real Grab?). Auch der
  Platzhalter ``kultur_{hash}`` für "SBK?" durch den echten
  ``hashlib.md5("SBK?")[:8]`` ersetzt. Der "FID-Salt"-Mechanismus für
  Grab? selbst war bereits korrekt (wörtlich aus modelling-rules.md
  übernommen) -- nur die Beispiel-FIDs waren falsch.

**Nicht geändert, weil bereits korrekt:** die Struktur-Aussagen selbst
(1:1-Zuordnung, geteilter vs. eigener Knoten, CRM/OWL-Time-Doppelanker,
FID-Salt-Mechanismus, die "~200 SBK-Fundstellen"-Zahl aus Regel 4) waren
alle bereits wortgetreu aus ``modelling-rules.md`` übernommen und
stimmten. Betroffen waren ausschließlich erfundene *Beispielwerte* und
ein erfundener Platzhalter-Hash -- nicht die Modellierungsaussagen selbst.

**Lehre für künftige Diagramme:** eine Quellenangabe im Docstring ist
keine Garantie, dass die Datei tatsächlich geöffnet wurde. Ab jetzt gilt
verbindlich: sobald ein Diagramm einen konkreten CSV-Beispielwert zeigt
(FID, Datierung, Freitext, Hash), wird die betreffende CSV *in dieser
Session* tatsächlich mit ``python3 -c "import csv; ..."`` geöffnet und
der Wert direkt daraus gelesen -- nicht aus einer früheren
Zusammenfassung, einer Doku-Beschreibung oder Plausibilität heraus
konstruiert. Wenn keine CSV-Prüfung stattgefunden hat, sagt der
Docstring das auch so (z. B. "strukturell aus modelling-rules.md, kein
Beispielwert gegen die CSV verifiziert") statt "real value" zu behaupten.

**Abnahme:** alle vier Grafiken (DE+EN) neu gerendert, visuell geprüft;
jeder in den Diagrammen sichtbare FID wurde nochmals einzeln gegen
``fst_wgs84_lit_enriched.csv`` abgeglichen (siehe Tabelle oben). `python
main.py` läuft komplett durch, zweimal hintereinander byte-identisch.

### S32 -- Interne Verweise aus gerendertem Text entfernt

**Ziel:** "Dinge wie 'Regel x' oder so rausnehmen, die Grafiken sollen
für sich alleine stehen."

**Substanz:** systematisch nach ``Regel\s*\d``, ``Tab\.\s*\d``,
``Abb\.\s*\d``, ``\u00a7\d`` und Diagramm-Querverweisen
(``0[0-9]-[a-z-]*``, ``(0[0-9])``) im gerenderten Text jeder Datei
gesucht -- ausdrücklich nur in dem, was tatsächlich ins SVG geht, nicht
in Docstrings (die sind Dokumentation für künftige Bearbeitung, kein
Bildinhalt). Funde und Fixes:

- **07**: "Regel 5" aus einem Container-Titel entfernt, "(Tab. 5)" aus
  einem zweiten. Dabei die referenzierten Zahlen selbst (fslwb:Q23/15/24/113)
  gegen den echten Pipeline-Code (`bb5kbc_lod_pipeline.py`) verifiziert --
  die stimmten exakt.
- **09**: "Regel 3"/"Regel 2/3" aus Box-Untertitel und Fließtext entfernt;
  ein Querverweis "05-uncertainty-markers." durch einen eigenständigen
  Satz ersetzt, der den Grund (fsl:certaintyDesc) direkt nennt statt auf
  ein anderes Diagramm zu verweisen; ein übersehener Querverweis "(08)"
  im Fließtext nachträglich gefunden und ebenfalls entfernt.
- **14**: Querverweis "...zeigt 04-crm-crosswalk." durch einen
  eigenständigen Satz ersetzt.
- **13**: "(Tab. 6)" entfernt.
- **02**: "(Paper §3.2)" entfernt.
- **10**: "(§3)"/"(§6)" aus zwei Container-Titeln entfernt.
- **06**: "(bb5kbc-csv-issues.md #6)" aus zwei Fließtext-Zeilen entfernt,
  reiner Fließtext bleibt.

**Abnahme:** ein Python-Scanner (liest jede Datei, überspringt
Docstring-Blöcke, sucht die obigen Muster) lief nach den Fixes über alle
19 `step_*.py` -- 0 Treffer im gerenderten Text.

### S33 -- Alle Diagramme auf orthogonale Linienführung umgestellt

**Ziel:** "die linien immer 'nur' vertikal und horiontal zeichnen, nicht
diagonal, etc, das wird teilw. sehr wild."

**Substanz:** zwei neue Utility-Funktionen in `bb5kbc_visuals_utils.py`:

- `svg_arrow_L(x1,y1,x2,y2,bend="h"|"v")` -- ein Knick. `bend="h"`
  verlässt die Quelle horizontal, biegt dann zur Ziel-y; `bend="v"`
  umgekehrt. Degradiert zu einer geraden Linie, wenn x1==x2 oder
  y1==y2 bereits gilt. Optionales Label sitzt auf dem längeren
  Teilstück.
- `marker: str | None` auf `svg_arrow_L` ergänzt -- `marker=None`
  unterdrückt die Pfeilspitze, für Zubringer-Linien, die an einem
  gemeinsamen Punkt mit einer anderen Linie zusammenlaufen (siehe
  unten, S05-Fund).

Dazu zwei bereits vorhandene Funktionen erweitert: `svg_arrow_elbow`
(horizontale Schiene) und `svg_arrow_elbow_v` (vertikale Schiene) haben
jetzt beide ein optionales `label`, das auf dem Schienen-Segment sitzt.

**Durchgearbeitet, je mit den gefundenen Problemen:**

- **00 (Fundstelle-Hub):** komplett neu -- alle 7 Speichen orthogonal,
  teils durch Verschieben von Boxen auf Fundstelles eigene Achse (z. B.
  KulturelleZuordnung auf Fundstelles Mittelhöhe), teils durch
  Eck-Routing.
- **05 (Unsicherheits-Marker, Florians Screenshot):** beim Umbau der
  Konvergenz-Pfeile zum "wd"-Badge ein **neuer Bug**: zwei Pfeilspitzen,
  die exakt am selben Punkt enden, überlagern sich zu einem "X".
  Ursache identifiziert, `marker=None` ergänzt (siehe oben) -- beide
  Zubringer ohne eigene Spitze, ein letzter kurzer Hop trägt die einzige
  Pfeilspitze. Dasselbe Muster danach in 09 und 11 wiederverwendet.
- **08, 09:** Fan-in-Speichen zu geteilten Knoten umgebaut; wo mehrere
  Quellen denselben Zielknoten erreichen, auf unterschiedliche Punkte
  am Kreisrand verteilt (kein Konvergenzpunkt = keine Kollision, keine
  `marker=None`-Klausel nötig).
- **03 (application-ontology):** der aufwändigste Fall. Erster Versuch
  routete alle sechs Fundstelle-Speichen direkt auf die linke Kante der
  Tier-2-Spalte -- lief dadurch quer durch die vier anderen Boxen in
  derselben Spalte. Zweiter Versuch: nur die vier Verbindungen, die
  tatsächlich eine Box überspringen (kz, ent, pub, sch), über eine
  Schiene in der Lücke vor der Spalte geroutet; die zwei direkten
  Nachbarn (fat, geo_akt) einfacher direkt. Dieselbe Diagnose bei
  kz->dat und ent->eat: ein direkter Vertikal-Abgang von der Quellbox
  aus schnitt durch die jeweils dazwischenliegende Box (ent bzw. fat) --
  ebenfalls auf eine Schiene in der Spalten-Lücke umgestellt.
- **10 (Pipeline-Architektur):** hier waren aus einer früheren,
  unvollständigen Session nur 2 von etwa 16 diagonalen Verbindungen
  gefixt. Alle übrigen jetzt ebenfalls umgestellt, mehrheitlich über
  Schienen in den jeweils freien Spaltenlücken.
- **12 (PROV-Chaining):** drei Verbindungen (wasInformedBy, zwei
  Output-Speichen) umgestellt. Bei den Output-Speichen ein **zweiter
  Eintrittswinkel-Fehler**: `bend="v"` ließ die Pfeile seitlich statt von
  oben in ihre Zielboxen laufen (technisch korrekt verbunden, aber der
  falsche Eintrittswinkel). Auf `svg_arrow_elbow` mit einer Schiene
  zwischen Aktivitäts-Box und Artefakt-Zeile umgestellt -- jetzt
  laufen beide Pfeile sauber von oben ein.
- **01, 04, 11, 15:** je 1--2 übersehene Diagonalen gefunden und
  gefixt (Phase-2-Verzweigung in 01; Fundstelle-Fan-out in 04;
  Konflikt-Beispiel-Konvergenz in 11 -- mit demselben
  `marker=None`-Muster wie 05; ein Pfeil zu NFDI4Objects in 15).
- **07, 02, 13, 14, 16:** bereits sauber, keine Änderung nötig.

**Abnahme:** jedes geänderte Diagramm einzeln gerendert und visuell
geprüft (DE, teils EN); abschließend `python main.py` komplett, zweimal
hintereinander byte-identisch, 0 AST-Scan-Treffer.

### S34 -- Korrektur: erfundenes Beispiel in 11 als illustrativ gekennzeichnet

**Ziel:** im Zuge der Linien-Überarbeitung von 11 fiel auf, dass das
"overwritten"-Beispiel ("CSV, Zeile 214", "QID_publikation = Q100")
nie gegen echte Daten geprüft worden war -- derselbe Fehlertyp wie in
S31, nur in einem fünften Diagramm gefunden statt gemeldet.

**Befund:** FID 214 ist real ("Brześć Kujawski 10"), aber die
tatsächliche `publikation_arch` ist "Grygiel 2008" mit
QID `Q139304642` -- nichts mit Pyzel 2019 oder "Q100" zu tun, das an
keiner Stelle in den Daten vorkommt. Grundsätzliches Problem:
`fst_wgs84_lit_enriched.csv` zeigt nur den Zustand *nach* der
Anreicherung -- ein "live" Konflikt ist darin grundsätzlich nicht
beobachtbar, jede Zeile ist per Definition bereits aufgelöst.

**Korrigiert:** Beispiel als ausdrücklich illustrativ gekennzeichnet
("CSV-Zeile (Beispiel)", "Q_alt" statt einer konkreten FID/QID). Der
reale Anker bleibt: `QID_PUBLIKATION["Pyzel 2019"] == "Q139460445"` ist
gegen `enrich_qids.py` verifiziert echt. Beim Nachschauen in dieser
Datei zusätzlich gefunden: mehrere echte, dokumentierte
Korrektur-Fälle im Dictionary selbst (z. B. ein "Raddatz 1959"-Eintrag,
der sich als Tippfehler für "Raddatz 1958" herausstellte) -- bestätigt,
dass der beschriebene *Mechanismus* real ist, auch wenn dieses konkrete
Beispiel keiner einzelnen Zeile zugeordnet werden kann.

**Abnahme:** DE+EN neu gerendert, Docstring dokumentiert den Befund und
die Korrektur vollständig.

### S35 -- 03 nach Florians Rückmeldung noch mal überarbeitet

**Ziel:** Florian schickte einen Screenshot von 03-application-ontology
mit "hier sind die linien noch sehr durcheinander" -- S33 hatte diese
Grafik zwar orthogonal gemacht, aber nicht wirklich entwirrt.

**Befund, zwei getrennte Ursachen:**

1. **Rail-Reihenfolge nicht an Reiseweite angepasst.** Die sechs
   Fundstelle-Speichen bekamen in S33 zwar je eine eigene Schiene, aber
   die Zuordnung war willkürlich (nicht nach Entfernung sortiert) --
   dadurch kreuzten sich Schienen von kurzen Verbindungen (fat, geo_akt:
   direkt, kein Umweg nötig) mit Schienen von langen Verbindungen (kz,
   ent, pub, sch: überspringen 1-2 Boxen), obwohl keine einzige Box
   selbst durchquert wurde -- der Effekt sah trotzdem nach Chaos aus.
2. **Zufällige Höhen-Koinzidenz bei hatDatierung/hatEntdeckungsart.**
   `Datierung` (Tier 3) sitzt in derselben Zeile wie `Entdeckung`
   (Tier 2, dieselbe ROW[1]). Die S33-Routing näherte sich `Datierung`
   von der Seite auf genau dieser Höhe -- optisch sah es dadurch so
   aus, als käme die `hatDatierung`-Linie aus `Entdeckung` heraus,
   obwohl sie tatsächlich von `KulturelleZuordnung` kommt. Dasselbe bei
   `hatEntdeckungsart`/`EntdeckungsartType` (Zeile deckt sich mit
   `FundstellenartType`).

**Korrigiert:**

1. Die sechs Schienen jetzt nach Reiseweite sortiert: kz und sch
   (überspringen je zwei Boxen) bekommen die äußere Schiene (x=650),
   ent und pub (überspringen je eine Box) die innere (x=680), fat und
   geo_akt (kein Umweg) bleiben direkt. Da das "nach oben"-Paar
   (kz/ent) und das "nach unten"-Paar (pub/sch) sich in y nie
   überschneiden, lässt sich jede der beiden Schienen-x-Positionen
   zweimal verwenden, ohne dass sich die vier Leitungen je kreuzen --
   nachvollziehbar, nicht nur optisch geprüft.
2. hatDatierung und hatEntdeckungsart treten jetzt von **oben** in ihre
   Zielbox ein (eigene Schiene im Zeilenzwischenraum, dann senkrecht
   nach unten), nicht mehr seitlich auf Zufallshöhe. Die
   Höhen-Koinzidenz mit Entdeckung/FundstellenartType spielt dadurch
   keine Rolle mehr.

**Abnahme:** DE+EN neu gerendert, Fundstelle-Kante und der
hatDatierung/hatDiscoveryType-Bereich beide vergrößert geprüft -- keine
Linie kreuzt mehr eine fremde Box oder eine andere Linie auf eine Art,
die den Ursprung einer Beziehung verschleiert. `python main.py`
komplett, zweimal hintereinander byte-identisch, 0 AST-Treffer.

### S36 -- Systematischer bend=h/v-Fehler gefunden und über 8 Grafiken behoben

**Ziel:** Florian schickte einen weiteren Screenshot von 03 ("noch nicht
commited!") und zeigte, dass die Pfeile bei Municipality, Site type und
Georeferencing activity senkrecht statt waagerecht ankommen -- also
falscher Eintrittswinkel, nicht (nur) Kreuzung.

**Befund, die eigentliche Ursache:** `svg_arrow_L`s zwei Modi wurden in
S33/S35 mehrfach verwechselt:

- `bend="h"` (horizontal zuerst) endet mit einem **senkrechten**
  Segment -- richtig für den Eintritt an einer Ober-/Unterkante.
- `bend="v"` (vertikal zuerst) endet mit einem **waagerechten**
  Segment -- richtig für den Eintritt an einer Links-/Rechtskante.

An mehreren Stellen war das vertauscht: das Ziel war eine Links-/Rechtskante
(erwartet waagerechten Eintritt), aber der Code nutzte `bend="h"`
(liefert senkrechten Eintritt) -- die Pfeilspitze traf dadurch von
oben/unten auf die Box statt sauber von der Seite, sichtbar als kurzer
Haken ins Eck statt als glatte Linie.

**Systematisch durch alle Dateien mit `svg_arrow_L`-Aufrufen gegangen
(nicht nur 03) und jedes Ziel einzeln geprüft: welche Kante wird
angesteuert, passt der `bend`-Wert dazu?** Acht Grafiken hatten den
Fehler an insgesamt 15 Stellen:

- **03**: die drei von Florian gezeigten (inMunicipality, hasSiteType,
  wasGeoreferencedBy) plus alle sechs Fundstelle-Speichen (jetzt
  einheitlich `svg_arrow_elbow_v`, siehe unten) -- die eigentliche Ursache
  der ursprünglichen Meldung.
- **00**: hasDating, hasSherd, wasGeoreferencedBy (traten seitlich an der
  Oberkante ihrer Zielboxen ein statt sauber von oben).
- **01**: die beiden Treffer-/Timeout-Verzweigungen (kleiner seitlicher
  Haken statt glattem Eintritt von oben -- am wenigsten auffällig von
  allen Funden, aber derselbe Fehler).
- **04**: der Dreifach-Fan-out von Fundstelle zu den drei
  CRM-Ansichten-Zeilen (stach von unten ins Eck statt seitlich
  einzutreten).
- **06**: die beiden Pfeile von Datierung zu crm:E52_Time-Span und
  time:Interval.
- **10**: csv_in→Stage 1 und fst_wgs84.csv→bb5kbc_lod_pipeline.py.
- **12**: wasInformedBy (hakte von unten in Top-Level-Activity statt von
  der Seite).
- **15**: der Pfeil zu NFDI4Objects Knowledge Graph -- bei normaler
  Zoomstufe kaum sichtbar, erst beim Hineinzoomen als Haken ins
  obere linke Eck erkennbar.

**Bewusst nicht geändert:** die vielen `svg_arrow_L`/`bend="h"`-Aufrufe,
die auf **Kreise** zielen (05, 08, 09, 11 -- die Doppelring-Knoten und
wd-Badges). Kreise haben keine harte Kante wie Rechtecke; ein waagerechter
Eintritt an einem leicht von der Mitte versetzten Punkt sieht dort nicht
falsch aus, sondern ist die übliche Darstellung für "trifft den Kreisrand
von der Seite" -- geprüft und bestätigt sauber, keine Änderung nötig.

**Abnahme:** jede der acht Dateien einzeln gerendert, jede betroffene
Stelle vor und nach dem Fix vergrößert verglichen (nicht nur die
Gesamtansicht -- der 15-Fehler wäre bei normaler Zoomstufe übersehen
worden). `python main.py` komplett, zweimal hintereinander
byte-identisch, 0 AST-Treffer.

**Lehre:** ein einzelner falsch verdrahteter Modus-Parameter in einer
gemeinsam genutzten Utility-Funktion pflanzt sich lautlos durch viele
Aufrufstellen fort, ohne dass es beim Bauen einer einzelnen Grafik
auffällt (jede Stelle sah für sich genommen "nicht offensichtlich falsch"
aus). Bei künftigen neuen `svg_arrow_L`/`svg_arrow_elbow*`-Aufrufen: vor
dem Commit bewusst prüfen, welche Kante das Ziel tatsächlich ist, und
den Modus danach wählen -- nicht nach Bauchgefühl.

### S37 -- Sichtbares "Herausragen" vor dem Knick ergänzt

**Ziel:** Florian schickte einen dritten Screenshot ("noch nciht
commited!") und benannte ein neues, feineres Detail: bei Site (03) auf
der linken Seite muss die Linie noch etwas "herausragen" wie auf der
rechten Seite, gleiches Problem bei Fundstelle-Hub (00) von Cultural
assignment zu Dating und von Site zu Georeferencing/Sherd.

**Befund:** ein Unterschied im *Stil* des Knicks, nicht in der
Kreuzungsfreiheit (die war nach S33/S35/S36 bereits gegeben). Auf der
rechten Seite von 03 und beim Fan-out in 00 verlässt jede Linie ihre
Quellbox zuerst ein Stück sichtbar in die eigene Richtung (ein kurzer
"Stummel"), bevor sie zur Ziel-Achse abbiegt -- das kommt daher, dass
diese Verbindungen über `svg_arrow_elbow`/`svg_arrow_elbow_v` mit einer
eigenen Schiene geroutet sind. Die drei jetzt gemeldeten Verbindungen
(inGemeinde in 03; hasDating, hasSherd, wasGeoreferencedBy in 00) nutzten
dagegen die einfachere `svg_arrow_L` (nur ein Knick) -- das erste
Segment beginnt exakt auf der Boxkante und biegt sofort ab, ohne
sichtbaren Stummel davor. Funktional identisch (keine Kreuzung, korrekter
Eintrittswinkel dank S36), aber optisch inkonsistent mit dem Rest der
Grafik.

**Korrigiert:** alle vier Verbindungen auf `svg_arrow_elbow`/
`svg_arrow_elbow_v` mit einer kurzen eigenen Schiene (ca. 25-30 px)
umgestellt, damit sie denselben "erst sichtbar herausragen, dann
abbiegen"-Stil zeigen wie der Rest der jeweiligen Grafik.

**Abnahme:** DE+EN beider Dateien neu gerendert, visuell mit den
bereits bekannten "guten" Stellen (Fundstelle-Fan-out in 03, restliche
Speichen in 00) verglichen -- jetzt einheitlich. `python main.py`
komplett, zweimal hintereinander byte-identisch, 0 AST-Treffer.

### S38 -- Label-Fehlplatzierung im Fundstelle-Fan-out behoben

**Ziel:** Florian, nach dem Commit von S37: "hassherd" "haspublication"
"has cultural assignment" "wasdicoveredby" sind auf jeden Fall
verrutscht und müssen zu den korrekten Linien.

**Befund:** ein neuer, dritter Fehlertyp in derselben Ecke der Grafik
(nach Kreuzung in S33/S35 und Eintrittswinkel in S36) -- diesmal die
Label-*Platzierung*. `svg_arrow_elbow_v` setzt sein Label standardmäßig
auf den geometrischen Mittelpunkt der vertikalen Schiene. Das
funktioniert, wenn Start- und Zielbereich ähnlich weit auseinander
liegen -- bricht aber zusammen, wenn (wie hier) alle sechs Austrittspunkte
dicht bei Fundstelle geclustert sind, während die sechs Zielzeilen über
750px verteilt sind: der Mittelpunkt der Schiene landet dann nicht in
der Nähe des Ziels, sondern irgendwo dazwischen -- und das kann
zufällig genau auf Höhe einer **anderen** Box liegen.

Konkret nachgerechnet: `hasCulturalAssignment`s Schienen-Mittelpunkt lag
bei y≈244 -- innerhalb der Zeile von `Entdeckung` (200-270), nicht in
der Nähe von `Cultural assignment` (50-120). `wasDiscoveredBy`s
Mittelpunkt lag bei y≈330, nahe an `Site type`s Zeile. `hasPublication`
und `hasSherd` waren ähnlich verschoben. Rein zufällige Artefakte der
Mittelpunkt-Formel, kein Fehler in der Linienführung selbst (die Linien
selbst waren korrekt, nur die Beschriftung schwamm).

**Korrigiert:** jedes der sechs Labels sitzt jetzt auf dem *eigenen*
finalen Annäherungssegment, direkt neben der Box, die es beschriftet --
nicht auf der Schiene. Ein erster Versuch (Labels direkt am Stummel bei
Fundstelle clustern) wurde verworfen, bevor er gerendert wurde: sechs
Labels, manche davon lang ("wurdeGeoreferenziertDurch"), hätten sich in
den knapp 40px Stummel-Bereich gegenseitig und die durchlaufenden
Schienen überlappt. Die Zielzeilen haben dagegen reichlich Platz (je
~130px eigener Zeilenabstand).

**Abnahme:** DE+EN neu gerendert, jedes der sechs Labels visuell direkt
neben seiner Box bestätigt (nicht nur "irgendwo auf der richtigen
Linie", sondern eindeutig zuordenbar auch ohne der Linie zu folgen).
Längere deutsche Labels (wurdeGeoreferenziertDurch) auf Kollision mit
der Zielbox geprüft -- passt mit Rand. `python main.py` komplett,
zweimal hintereinander byte-identisch, 0 AST-Treffer.

### S39 -- Rückwärtslaufende Linie zum wd-Badge in 05 behoben

**Ziel:** Florian, zu 05-uncertainty-markers (schon committed): "hier
passen insb. rechts die linien zu wikidata nicht!"

**Befund:** ein echter Koordinatenfehler, kein Wahrnehmungsproblem --
im rohen SVG nachgeprüft, nicht nur im PNG. Die x-Position des rechten
wd-Badges (`qx2`) wurde ausschließlich aus dem Radius des
"Grab"-Kreises berechnet. Das war auf der linken Seite unproblematisch,
weil dort beide Quellen ("SBK" und "SBK?") gleich große Kreise mit
demselben Radius `KG_R` sind -- die Annahme "beide Quellen gleich
breit" stimmte dort. Auf der rechten Seite gilt sie nicht: "Grab?" ist
eine 230px breite Box, die deutlich weiter rechts reicht als der
"Grab"-Kreis. Der gemeinsame Abbiegepunkt lag dadurch *innerhalb* der
"Grab?"-Box selbst (x=1361 bei einer Box, die bis x=1425 reicht) --
die Linie von "Grab?" musste dadurch erst nach **links** zurück
laufen, bevor sie zum Badge abbog, statt die Box sauber nach rechts zu
verlassen wie alle anderen Verbindungen in der Grafik.

**Korrigiert:** `qx2` wird jetzt aus dem **weiter rechts liegenden** der
beiden Quell-Ränder berechnet (`max(Grab-Kreis-Rand, Grab?-Box-Rand)`),
nicht mehr nur aus dem Kreis. Das Badge rückt dadurch etwas weiter nach
rechts (mehr Platz für die breitere Box), beide Zubringer-Linien laufen
jetzt konsistent nach rechts, symmetrisch zum linken Panel.

**Abnahme:** rohes SVG vor und nach dem Fix verglichen (Pfad-Koordinaten
direkt geprüft, nicht nur das PNG angesehen), DE+EN neu gerendert und
visuell mit dem linken Panel verglichen -- jetzt strukturell
symmetrisch. `python main.py` komplett, zweimal hintereinander
byte-identisch, 0 AST-Treffer.

**Lehre:** wenn zwei Konvergenz-Linien zu einem gemeinsamen Punkt aus
unterschiedlich geformten/großen Quellen kommen (hier: Kreis + breite
Box), reicht es nicht, den Zielpunkt aus einer der beiden Quellen
abzuleiten -- er muss aus dem tatsächlich weiter außen liegenden Rand
berechnet werden. Bei rein visueller PNG-Prüfung wäre das an dieser
Stelle leicht zu übersehen gewesen; das Nachrechnen im rohen SVG-Pfad
hat den Fehler eindeutig bestätigt.

### S40 -- Balken-Überlauf in 06 behoben, Linien-Fix aus S36 re-bestätigt

**Ziel:** Florian schickte einen Screenshot von 06-uncertainty-dating:
"hier stimmt auch die linien-logik nicht und n=299 ragt über den kasten
hinaus".

**Befund, zwei getrennte Sachverhalte:**

1. **Linien-Logik:** der Screenshot zeigte die beiden Pfeile zu
   crm:E52_Time-Span/time:Interval mit senkrechtem statt waagerechtem
   Eintritt -- genau das Muster, das S36 bereits für diese Datei behoben
   hatte (`bend="v"`). Im aktuellen Code hier nachgeprüft: die Zeile
   steht bereits auf `bend="v"`, der eigene Render zeigt sauberen
   waagerechten Eintritt. Der Screenshot zeigte vermutlich einen nicht
   neu gebauten oder nicht vollständig gepatchten Stand, keine Regression
   in dieser Datei -- sicherheitshalber trotzdem erneut ausgeliefert,
   um jeden Zweifel auszuräumen.
2. **Balken-Überlauf (der echte, neue Fund):** `bar_w` war ein fest
   codierter Wert (1560px), nie gegen die tatsächliche gerenderte Breite
   von "n=299" (der längste Zahlen-Text neben dem längsten Balken)
   geprüft. Nachgerechnet: Balkenende + Textanfang + Textbreite lag bei
   rund x=1712, der gestrichelte Rahmen endet bei x=1690 -- der Text lief
   also tatsächlich über den Rahmen hinaus.

**Korrigiert:** `bar_w` wird jetzt aus dem tatsächlichen rechten
Rahmenrand minus der echten gerenderten Breite des längsten "n=NNN"-
Labels (`vu.text_width()`, nicht geschätzt) berechnet -- der längste
Balken kann seinen Zahlen-Text dadurch nie mehr über den Rahmen hinaus
schieben, unabhängig davon, welche Häufigkeiten die Daten irgendwann
liefern.

**Abnahme:** DE+EN neu gerendert, n=299-Balken samt Label liegt jetzt
mit sichtbarem Rand innerhalb des Rahmens; beide Linien zu
crm:E52_Time-Span/time:Interval zeigen sauberen waagerechten Eintritt.
`python main.py` komplett, zweimal hintereinander byte-identisch,
0 AST-Treffer.

### S41 -- 19 Allen-/Freksa-Relationen (neu, Skizze)

**Ziel:** Florian bat um eine weitere Grafik zu 06-uncertainty-dating, die
zeigt, wie Allens Interval-Relationen und darauf aufbauend Freksas
Relationen aussehen könnten -- als eigenständige neue Nummer (19), nicht
als Eingriff in die bestehende, im Paper referenzierte 06.

**Verifikation vor dem Bauen:** `fst_wgs84_lit_enriched.csv` enthält nur
18 distinkte (dating_start, dating_end)-Intervalle über alle 540 Zeilen.
Alle Paarungen dieser 18 Intervalle wurden per Skript gegen
handgeschriebene Allen-Prädikate klassifiziert; für jede der 13
Relationen ein echtes, real existierendes Paar (FID, Name, Kultur,
Jahre) ausgewählt und die Klassifikation einzeln noch einmal bestätigt,
bevor es in den Code kam. Keine erfundenen Beispiele (vgl. S31).

**Substanz:**
- Linkes Panel: sieben kanonische Allen-Zeilen (Relation + Inverse in
  einem Bild, Standarddarstellung nach Allen 1983), je mit lokal
  skalierter Mini-Zeitachse (nicht global über den ganzen Datensatz,
  damit z. B. die 4000 Jahre breite Mesolithikum-Spanne die enge
  SBK-Spanne nicht unsichtbar macht) und echten
  FID/Name/Kultur/Jahres-Beschriftungen.
- Rechtes Panel: Skizze zu Freksas Semi-Intervallen, aufgehängt am
  echten "meets"-Paar (FID78/FID153, Grenze bei -4350) mit deren
  echten datingCertaintyStart/End-Werten (±100/±50 Jahre) als
  Unsicherheitsbänder; explizit als Skizze markiert, nicht als
  Berechnung (eigener gestrichelter Kasten unten, Farbsprache
  terracotta/`UNCERTAIN_*` wie in 05).
- Relationsnamen bewusst unübersetzt englisch in beiden
  Sprachversionen (Begründung im Docstring) -- Ausnahme vom sonstigen
  `vu.cls()`/`vu.prop()`-Muster, weil es keine bb5kbc:-Vokabel ist.

**Abnahme:** DE+EN gerendert und visuell geprüft (kein Overflow, Umlaute
korrekt); `python py/step_19_allen_freksa_relations.py` zweimal →
byte-identisch; kompletter `python main.py` (jetzt 20 Schritte,
80 Dateien) zweimal → alle 80 Dateien byte-identisch. AST-Scan auf das
f-string-Backslash-Muster: 0 Treffer -- drei verschachtelte f-strings,
die beim Schreiben den Parser stolpern ließen, vorsorglich in eigene
Variablen ausgelagert (siehe S16/S27/S30-Historie).

## Teil D -- Offene Punkte

- **AST-Scan nicht automatisiert.** Weiterhin von Hand geprüft statt
  automatisch (siehe S16/S27/S30).
- **Fest codierte Balkenbreiten sind ein wiederkehrendes Risiko**
  (S40): mindestens eine Stelle gefunden, wo eine Breite als fixer Wert
  gesetzt war statt gegen die tatsächliche Textbreite geprüft. Andere
  balkenartige Elemente (17-stats-infographic hat ähnliche Bars) wurden
  nicht auf dasselbe Muster durchsucht.
- **Nach einem Patch immer prüfen, ob der Screenshot den Stand *nach*
  dem letzten Patch zeigt** (S40 Punkt 1) -- ein bereits gefixtes Detail
  erneut gemeldet zu bekommen ist harmlos, aber ein Hinweis, dass
  Patch-Anwendung/Neu-Build zwischen den Runden nicht immer
  nachvollziehbar ist. Keine Aktion nötig, nur als Beobachtung notiert.
- **Konvergenzpunkte aus ungleich großen/geformten Quellen** (S39),
  **Label-Platzierung, Linienführungs-Stil, bend=h/v** (S36-S38) --
  jeweils nur an gemeldeten Stellen gefixt, nicht flächendeckend.
- **Datengrundlage: 11 vollständig geprüft (S34), 12 und 16 nur
  stichprobenartig.**
- **19s Freksa-Panel ist eine Skizze, keine Implementierung** (S41): die
  Beispielrelationen im "könnte real sein"-Beispiel sind von Hand aus
  den echten ±100/±50-Jahres-Spannen abgeleitet, nicht aus einer
  Punktalgebra berechnet. Eine echte Freksa(1992)-Semi-Intervall-/
  Nachbarschafts-Umsetzung (und ob sie als eigene `.rq`/`queries.yaml`-
  View in `bb-5kbc-public` oder nur hier als Grafik leben soll) ist
  offen.

Wenn ein neuer Punkt ansteht: nach S41 einsortieren (S42, S43, …), hier
eintragen, nach Erledigung wieder streichen und in Teil B übernehmen.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_18_site_map.py -- all 540 sites, on a real (if schematic) basemap
================================================================================

Source, three data files, all under ``data/raw/bb-5kbc-sites/``:

* ``site_coordinates.csv`` -- the 540 real ``wgs84_x``/``wgs84_y``/country
  values from ``fst_wgs84.csv`` (see that file's note in ``data/raw/README.md``).
* ``admin_boundaries.json`` -- Brandenburg and its four German neighbours
  (Sachsen, Sachsen-Anhalt, Thueringen, Mecklenburg-Vorpommern, Berlin)
  plus the ten Polish voivodeships the data actually touches, extracted
  from Natural Earth's ``ne_10m_admin_1_states_provinces`` (public domain,
  https://www.naturalearthdata.com) and reduced to 3 decimal places.
* ``country_boundaries.json`` -- Germany, Poland and three neighbours
  (Czechia, Austria, Denmark) for context, from Natural Earth's
  ``ne_50m_admin_0_countries``.
* ``major_cities.csv`` -- 23 cities within the map's extent, from Natural
  Earth's ``ne_10m_populated_places``, sorted by population with
  near-duplicates (e.g. Ruhr-style conurbations) suppressed; Potsdam
  added back by hand despite being close to Berlin, because it is
  Brandenburg's own capital and directly relevant to this dataset.

All three boundary/city files were fetched once from
``raw.githubusercontent.com/nvkelso/natural-earth-vector`` and are
checked in here as plain, static data -- same documented exception to
"read during authoring only" as ``site_coordinates.csv`` already is (see
that file's note and ``PRIMER.md`` A4).

What this is not: a hillshade/terrain layer. That needs a real
elevation raster (SRTM/GMTED or similar) and a rendering pipeline built
for rasters; neither is available here, and faking relief shading from
nothing would be exactly the kind of fabricated cartographic precision
this figure otherwise avoids. Borders and cities are real data; the
ground between them is left blank rather than invented.

Bilingual (revision) -- see step_00 docstring for the convention. City
and region names are real place names and are never translated.

Writes: site-map.de.svg/.png, site-map.en.svg/.png
Run standalone: ``python py/step_18_site_map.py``
"""

from __future__ import annotations

import csv
import json
import math

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["18-site-map"]
COORDS_FILE = vu.SOURCE_REPO / "site_coordinates.csv"
ADMIN_FILE = vu.SOURCE_REPO / "admin_boundaries.json"
COUNTRY_FILE = vu.SOURCE_REPO / "country_boundaries.json"
CITIES_FILE = vu.SOURCE_REPO / "major_cities.csv"

DE_COLOR = vu.GEO
PL_COLOR = vu.SITE
STATE_LINE = "#c9c7bc"
COUNTRY_LINE = "#9b9a8f"
CITY_DOT = "#5f5e5a"


def _load_points():
    pts = []
    with open(COORDS_FILE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pts.append((float(row["wgs84_x"]), float(row["wgs84_y"]), row["country"]))
    return pts


def _load_cities():
    out = []
    with open(CITIES_FILE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append((row["name"], float(row["lon"]), float(row["lat"]), int(row["pop_max"])))
    return out


def _ring_to_path(ring, project):
    pts = [project(lon, lat) for lon, lat in ring]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    d += " ".join(f"L {x:.1f} {y:.1f}" for x, y in pts[1:])
    return d + " Z"


def _geom_to_path(geometry, project):
    parts = []
    if geometry["type"] == "Polygon":
        for ring in geometry["coordinates"]:
            parts.append(_ring_to_path(ring, project))
    elif geometry["type"] == "MultiPolygon":
        for poly in geometry["coordinates"]:
            for ring in poly:
                parts.append(_ring_to_path(ring, project))
    return " ".join(parts)


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("All 540 BB-5KBC sites on a real basemap: admin boundaries, cities, real coordinates")]

    points = _load_points()
    admin = json.loads(ADMIN_FILE.read_text(encoding="utf-8"))
    countries = json.loads(COUNTRY_FILE.read_text(encoding="utf-8"))
    cities = _load_cities()

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    lon_min, lon_max = min(lons), max(lons)
    lat_min, lat_max = min(lats), max(lats)
    mean_lat = (lat_min + lat_max) / 2
    cos_f = math.cos(math.radians(mean_lat))

    plot_x0, plot_x1 = 160, 1350
    plot_y0, plot_y1 = 90, 860
    plot_w, plot_h = plot_x1 - plot_x0, plot_y1 - plot_y0
    pad = 20

    lon_span = (lon_max - lon_min) * cos_f
    lat_span = lat_max - lat_min
    scale = min((plot_w - 2 * pad) / lon_span, (plot_h - 2 * pad) / lat_span)
    used_w, used_h = lon_span * scale, lat_span * scale
    off_x = plot_x0 + (plot_w - used_w) / 2
    off_y = plot_y0 + (plot_h - used_h) / 2

    def project(lon, lat):
        px = off_x + (lon - lon_min) * cos_f * scale
        py = off_y + (lat_max - lat) * scale
        return px, py

    clip_id = "mapclip"
    parts.append(f'<clipPath id="{clip_id}"><rect x="{plot_x0:.1f}" y="{plot_y0:.1f}" '
                 f'width="{plot_w:.1f}" height="{plot_h:.1f}"/></clipPath>')
    parts.append(f'<rect x="{plot_x0:.1f}" y="{plot_y0:.1f}" width="{plot_w:.1f}" height="{plot_h:.1f}" '
                 f'fill="#fafaf7" stroke="#dedcd4" stroke-width="1"/>')

    parts.append(f'<g clip-path="url(#{clip_id})">')

    for feat in admin:
        d = _geom_to_path(feat["geometry"], project)
        parts.append(f'<path d="{d}" fill="none" stroke="{STATE_LINE}" stroke-width="1.1"/>')

    for feat in countries:
        d = _geom_to_path(feat["geometry"], project)
        parts.append(f'<path d="{d}" fill="none" stroke="{COUNTRY_LINE}" stroke-width="2.0"/>')

    for lon, lat, country in points:
        px, py = project(lon, lat)
        col = DE_COLOR if country == "DE" else PL_COLOR
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{col["stroke"]}" opacity="0.55"/>')

    for name, lon, lat, pop in cities:
        px, py = project(lon, lat)
        r = 5.5 if pop > 1_000_000 else (4 if pop > 400_000 else 3)
        fs = 12.5 if pop > 1_000_000 else (11.5 if pop > 400_000 else 10.5)
        fw = "600" if pop > 1_000_000 else "500"
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="#ffffff" '
                     f'stroke="{CITY_DOT}" stroke-width="1.6"/>')
        # Potsdam sits ~25km from Berlin -- right-of-dot placement collides
        # with Berlin's own label at this map scale, so it gets a
        # below-left label instead. Every other city uses the default.
        if name == "Potsdam":
            parts.append(f'<text x="{px - r - 5:.1f}" y="{py + fs + 2:.1f}" text-anchor="end" '
                         f'font-family="Fira Sans" font-weight="{fw}" font-size="{fs}" '
                         f'fill="{CITY_DOT}">{vu.xml_escape(name)}</text>')
        else:
            parts.append(f'<text x="{px + r + 5:.1f}" y="{py + 4:.1f}" font-family="Fira Sans" '
                         f'font-weight="{fw}" font-size="{fs}" fill="{CITY_DOT}">{vu.xml_escape(name)}</text>')

    parts.append("</g>")

    nx, ny = plot_x0 + 50, plot_y0 + 60
    parts.append(f'<line x1="{nx:.1f}" y1="{ny + 30:.1f}" x2="{nx:.1f}" y2="{ny - 10:.1f}" '
                 f'stroke="{vu.TEXT_DARK}" stroke-width="1.6" marker-end="url(#arrow)"/>')
    parts.append(f'<text x="{nx:.1f}" y="{ny - 18:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="13" fill="{vu.TEXT_DARK}">N</text>')

    extent = tt(f"Ausdehnung: {lon_min:.1f}\u2013{lon_max:.1f}\u00b0 O, {lat_min:.1f}\u2013{lat_max:.1f}\u00b0 N",
                f"Extent: {lon_min:.1f}\u2013{lon_max:.1f}\u00b0 E, {lat_min:.1f}\u2013{lat_max:.1f}\u00b0 N")
    parts.append(f'<text x="{plot_x0:.1f}" y="{plot_y1 + 28:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(extent)}</text>')
    basemap_note = tt("Grundkarte: echte Verwaltungsgrenzen (Natural Earth) + Gro\u00dfst\u00e4dte, "
                       "\u00e4quirechteckig projiziert (Longitude \u00d7 cos(mittl. Breite)) \u2014 kein H\u00f6henrelief "
                       "(dazu fehlt eine Gel\u00e4ndemodell-Rasterquelle in dieser Pipeline)",
                       "Basemap: real administrative boundaries (Natural Earth) + major cities, "
                       "equirectangular (longitude \u00d7 cos(mean latitude)) \u2014 no terrain relief "
                       "(that needs a DEM raster source this pipeline doesn't have)")
    parts.append(f'<text x="{plot_x0:.1f}" y="{plot_y1 + 48:.1f}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(basemap_note)}</text>')

    rx = 1420
    n_de = sum(1 for p in points if p[2] == "DE")
    n_pl = sum(1 for p in points if p[2] == "PL")
    parts.append(vu.svg_legend(rx, 100, [
        (tt(f"Deutschland (n={n_de})", f"Germany (n={n_de})"), DE_COLOR),
        (tt(f"Polen (n={n_pl})", f"Poland (n={n_pl})"), PL_COLOR),
    ], columns=1, col_w=250, row_h=32))

    line_legend_y = 175
    parts.append(f'<line x1="{rx:.1f}" y1="{line_legend_y:.1f}" x2="{rx + 32:.1f}" y2="{line_legend_y:.1f}" '
                 f'stroke="{COUNTRY_LINE}" stroke-width="2.0"/>')
    parts.append(f'<text x="{rx + 40:.1f}" y="{line_legend_y + 4:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{vu.TEXT_DARK}">{tt("Landesgrenze", "country border")}</text>')
    parts.append(f'<line x1="{rx:.1f}" y1="{line_legend_y+26:.1f}" x2="{rx + 32:.1f}" y2="{line_legend_y+26:.1f}" '
                 f'stroke="{STATE_LINE}" stroke-width="1.1"/>')
    parts.append(f'<text x="{rx + 40:.1f}" y="{line_legend_y + 30:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{vu.TEXT_DARK}">{tt("Bundesland/Wojewodschaft", "state/voivodeship")}</text>')
    parts.append(f'<circle cx="{rx + 8:.1f}" cy="{line_legend_y+50:.1f}" r="4" fill="#ffffff" '
                 f'stroke="{CITY_DOT}" stroke-width="1.6"/>')
    city_label = tt("Gro\u00dfstadt", "major city")
    parts.append(f'<text x="{rx + 40:.1f}" y="{line_legend_y + 54:.1f}" font-family="Fira Sans" font-size="12" '
                 f'fill="{vu.TEXT_DARK}">{city_label}</text>')

    prec_note = tt(
        ["Ver\u00f6ffentlichte Fundstellen-", "Koordinaten sind auf 2", "Nachkommastellen reduziert",
         "(Schutz vor Raubgrabungen)."],
        ["Published site coordinates", "are reduced to 2 decimal", "places (protection against",
         "looting)."])
    py2 = 300
    for line in prec_note:
        parts.append(f'<text x="{rx:.1f}" y="{py2:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        py2 += 20

    src_note = tt(
        ["Grenzen/St\u00e4dte: Natural Earth", "(public domain),", "naturalearthdata.com"],
        ["Boundaries/cities: Natural", "Earth (public domain),", "naturalearthdata.com"])
    py3 = py2 + 30
    for line in src_note:
        parts.append(f'<text x="{rx:.1f}" y="{py3:.1f}" font-family="Fira Sans" font-size="11" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        py3 += 18

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"site-map.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

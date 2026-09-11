#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_18_site_map.py -- all 540 sites, plotted from their real coordinates
================================================================================

Source: ``data/raw/bb-5kbc-sites/site_coordinates.csv`` -- the
``wgs84_x``/``wgs84_y``/country of all 540 rows in ``fst_wgs84.csv``,
extracted once and checked into this repo as plain data. This is a
deliberate, documented exception to the "read-only reference,
hand-authored geometry" pattern every other figure in this repo follows:
540 real coordinates cannot be hand-placed the way a dozen boxes can, so
this is the one step that parses a data file at build time rather than
only reading it during authoring. The published coordinates are already
reduced to two decimal places (paper section on data publication:
protection against looting), so nothing more precise than what is
already public is used here.

This is a schematic equirectangular scatter (longitude scaled by
cos(mean latitude) to avoid east-west stretching), not a projected map --
there is no coastline, border or basemap data in this repository to draw
one honestly, so none is drawn. The point cloud is real; the visual
context around it is not.

Bilingual (revision) -- see step_00 docstring for the convention.

Writes: site-map.de.svg/.png, site-map.en.svg/.png
Run standalone: ``python py/step_18_site_map.py``
"""

from __future__ import annotations

import csv
import math

import bb5kbc_visuals_utils as vu

OUT = vu.OUT_DIRS["18-site-map"]
COORDS_FILE = vu.SOURCE_REPO / "site_coordinates.csv"
DE_COLOR = vu.GEO
PL_COLOR = vu.SITE


def _load_points() -> list[tuple[float, float, str]]:
    pts = []
    with open(COORDS_FILE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pts.append((float(row["wgs84_x"]), float(row["wgs84_y"]), row["country"]))
    return pts


def build(lang: str = "en") -> list[str]:
    tt = lambda de, en: vu.t(lang, de, en)
    parts = [vu.svg_open("All 540 BB-5KBC sites, plotted from their real WGS84 coordinates")]

    points = _load_points()
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

    parts.append(f'<rect x="{plot_x0:.1f}" y="{plot_y0:.1f}" width="{plot_w:.1f}" height="{plot_h:.1f}" '
                 f'fill="#fafaf7" stroke="#dedcd4" stroke-width="1"/>')

    for lon, lat, country in points:
        px, py = project(lon, lat)
        col = DE_COLOR if country == "DE" else PL_COLOR
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{col["stroke"]}" '
                     f'opacity="0.55"/>')

    # north arrow + orientation (placed top-left, where the point cloud is sparse)
    nx, ny = plot_x0 + 50, plot_y0 + 60
    parts.append(f'<line x1="{nx:.1f}" y1="{ny + 30:.1f}" x2="{nx:.1f}" y2="{ny - 10:.1f}" '
                 f'stroke="{vu.TEXT_DARK}" stroke-width="1.6" marker-end="url(#arrow)"/>')
    parts.append(f'<text x="{nx:.1f}" y="{ny - 18:.1f}" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="13" fill="{vu.TEXT_DARK}">N</text>')

    extent = tt(f"Ausdehnung: {lon_min:.1f}\u2013{lon_max:.1f}\u00b0 O, {lat_min:.1f}\u2013{lat_max:.1f}\u00b0 N",
                f"Extent: {lon_min:.1f}\u2013{lon_max:.1f}\u00b0 E, {lat_min:.1f}\u2013{lat_max:.1f}\u00b0 N")
    parts.append(f'<text x="{plot_x0:.1f}" y="{plot_y1 + 28:.1f}" font-family="Fira Sans" font-size="12.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(extent)}</text>')
    schematic_note = tt("schematischer Punktplot (Longitude \u00d7 cos(mittl. Breite)), keine projizierte Karte \u2014 "
                         "keine Basiskarten-/Grenzdaten in diesem Repo",
                         "schematic point plot (longitude \u00d7 cos(mean latitude)), not a projected map \u2014 "
                         "no basemap/boundary data in this repository")
    parts.append(f'<text x="{plot_x0:.1f}" y="{plot_y1 + 48:.1f}" font-family="Fira Sans" font-size="11.5" '
                 f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(schematic_note)}</text>')

    # -- right side: legend + stats ---------------------------------------------
    rx = 1420
    n_de = sum(1 for p in points if p[2] == "DE")
    n_pl = sum(1 for p in points if p[2] == "PL")
    parts.append(vu.svg_legend(rx, 120, [
        (tt(f"Deutschland (n={n_de})", f"Germany (n={n_de})"), DE_COLOR),
        (tt(f"Polen (n={n_pl})", f"Poland (n={n_pl})"), PL_COLOR),
    ], columns=1, col_w=250, row_h=32))

    prec_note = tt(
        ["Ver\u00f6ffentlichte Koordinaten sind", "auf 2 Nachkommastellen", "reduziert (Schutz vor",
         "Raubgrabungen) \u2014 diese Grafik", "nutzt keine h\u00f6here Genauigkeit."],
        ["Published coordinates are", "reduced to 2 decimal places", "(protection against looting)",
         "\u2014 this figure uses no", "higher precision than that."])
    py2 = 230
    for line in prec_note:
        parts.append(f'<text x="{rx:.1f}" y="{py2:.1f}" font-family="Fira Sans" font-size="12" '
                     f'fill="{vu.TEXT_MUTED}">{vu.xml_escape(line)}</text>')
        py2 += 20

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"site-map.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    return build("de") + build("en")


if __name__ == "__main__":
    written = main()
    print(f"wrote {len(written)} file(s)")
    for p in written:
        print(" ", p)

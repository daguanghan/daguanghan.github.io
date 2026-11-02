#!/usr/bin/env python3
"""Build network.html from the institution list that 0.0 exports.

    python3 tools/build_network.py [--basemap path/to/ne_50m_admin_0_countries.geojson]

Input:  ../../0-command-center/state/handoff_2026-11-02_global-network_public.json
        (institution names, region and tier only; no personal names).
Basemap: tools/basemap_panels.json, cut once from Natural Earth (public domain).
         Pass --basemap to rebuild it from a Natural Earth GeoJSON file.
Output: network.html (static inline SVG; no external map service, no tracking).
"""
import argparse, html, json, math
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
SRC = SITE.parents[1] / "0-command-center/state/handoff_2026-11-02_global-network_public.json"
BASEMAP = SITE / "tools/basemap_panels.json"

# Institution -> (country, lat, lon), from each institution's main campus address.
COORDS = {
    "Cardiff University": ("United Kingdom", 51.487, -3.179),
    "Delft University of Technology": ("Netherlands", 52.002, 4.373),
    "Loughborough University": ("United Kingdom", 52.765, -1.229),
    "NTNU": ("Norway", 63.419, 10.402),
    "UCL": ("United Kingdom", 51.525, -0.134),
    "University of Bristol": ("United Kingdom", 51.458, -2.603),
    "University of Cambridge": ("United Kingdom", 52.204, 0.115),
    "University of Manchester": ("United Kingdom", 53.467, -2.234),
    "University of Nottingham": ("United Kingdom", 52.938, -1.195),
    "University of Salford": ("United Kingdom", 53.486, -2.272),
    "Aalborg University": ("Denmark", 57.015, 9.985),
    "Aston U.": ("United Kingdom", 52.486, -1.888),
    "Bauhaus-Universität Weimar": ("Germany", 50.974, 11.329),
    "Brunel University London": ("United Kingdom", 51.533, -0.473),
    "Chalmers": ("Sweden", 57.689, 11.974),
    "City St George’s, U. London": ("United Kingdom", 51.528, -0.102),
    "Heriot-Watt University": ("United Kingdom", 55.909, -3.320),
    "Institution of Civil Engineers": ("United Kingdom", 51.501, -0.128),
    "KU Leuven": ("Belgium", 50.878, 4.700),
    "National Technical University of Athens": ("Greece", 37.979, 23.783),
    "Newcastle University": ("United Kingdom", 54.980, -1.615),
    "Technical University of Denmark (DTU)": ("Denmark", 55.786, 12.524),
    "U. Bath": ("United Kingdom", 51.380, -2.328),
    "University of Birmingham": ("United Kingdom", 52.450, -1.930),
    "University of Edinburgh": ("United Kingdom", 55.944, -3.188),
    "University of Leeds": ("United Kingdom", 53.807, -1.555),
    "University of Oxford": ("United Kingdom", 51.754, -1.254),
    "University of Strathclyde": ("United Kingdom", 55.862, -4.242),
    "University of Surrey": ("United Kingdom", 51.243, -0.590),
    "University of Warwick": ("United Kingdom", 52.384, -1.562),
    "Western University": ("Canada", 43.009, -81.273),
    "Carnegie Mellon University": ("United States", 40.443, -79.943),
    "Imperial College London": ("United Kingdom", 51.498, -0.175),
    "Oslo Metropolitan University": ("Norway", 59.920, 10.735),
    "University College Dublin": ("Ireland", 53.307, -6.222),
    "University of Cyprus": ("Cyprus", 35.145, 33.413),
    "University of Sheffield": ("United Kingdom", 53.381, -1.489),
    "University of Southampton": ("United Kingdom", 50.935, -1.396),
    "Universität der Bundeswehr München": ("Germany", 48.080, 11.638),
}
# Public display names where the source uses an abbreviation.
DISPLAY = {"UCL": "University College London (UCL)", "Aston U.": "Aston University", "U. Bath": "University of Bath", "Chalmers": "Chalmers University of Technology",
           "NTNU": "Norwegian University of Science and Technology (NTNU)",
           "City St George’s, U. London": "City St George’s, University of London"}

TIERS = [("collaborating", "Agreed joint work", "joint papers or proposals agreed", "#7c8cff"),
         ("in_discussion", "In discussion", "met, or a meeting arranged, to discuss joint work", "#d5b16d"),
         ("in_contact", "In contact", "corresponding about possible joint work", "#9fb3c8"),
         ("past", "Past", "where I studied or worked", "#5fc4a8")]
TIER_RANK = {t[0]: i for i, t in enumerate(TIERS)}

# Map panels: (key, title, lon_min, lon_max, lat_min, lat_max, width_px)
PANELS = [("gb", "Great Britain and Ireland", -10.8, 2.2, 49.8, 59.2, 520),
          ("eu", "Continental Europe", -1.0, 35.0, 34.0, 65.5, 520),
          ("na", "North America", -90.0, -70.0, 37.0, 47.0, 520)]
# Which countries each panel plots (so London is not drawn again at the edge of the Europe panel).
PANEL_COUNTRIES = {"gb": {"United Kingdom", "Ireland"}, "na": {"United States", "Canada"}}


def project(lon, lat, p):
    _, _, x0, x1, y0, y1, w = p
    k = math.cos(math.radians((y0 + y1) / 2))
    h = w * (y1 - y0) / ((x1 - x0) * k)
    return (lon - x0) / (x1 - x0) * w, (y1 - lat) / (y1 - y0) * h, h


def cut_basemap(geojson_path):
    """Clip Natural Earth country polygons to each panel and store them as SVG path strings."""
    feats = json.loads(Path(geojson_path).read_text())["features"]
    out = {}
    for p in PANELS:
        key, _, x0, x1, y0, y1, w = p
        h = project(x0, y0, p)[2]
        paths = []
        for f in feats:
            g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            d = []
            for poly in polys:
                for ring in poly:
                    lons = [c[0] for c in ring]; lats = [c[1] for c in ring]
                    if max(lons) < x0 - 2 or min(lons) > x1 + 2 or max(lats) < y0 - 2 or min(lats) > y1 + 2:
                        continue
                    pts = [project(lo, la, p)[:2] for lo, la in ring]
                    d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
            if d:
                paths.append("".join(d))
        out[key] = {"h": round(h, 1), "paths": paths}
    BASEMAP.write_text(json.dumps(out))


def svg_panel(p, base, pts):
    key, title, *_ , w = p
    h = base[key]["h"]
    land = "".join(f'<path d="{d}"/>' for d in base[key]["paths"])
    dots = []
    keep = PANEL_COUNTRIES.get(key)
    for name, tier, lat, lon, country in sorted(pts, key=lambda t: -TIER_RANK[t[1]]):
        if (keep and country not in keep) or (not keep and country in set().union(*PANEL_COUNTRIES.values())):
            continue
        x, y, _ = project(lon, lat, p)
        if 0 <= x <= w and 0 <= y <= h:
            col = next(t[3] for t in TIERS if t[0] == tier)
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}"><title>{html.escape(name)}</title></circle>')
    return (f'<figure class="map-panel"><figcaption>{title}</figcaption>'
            f'<svg viewBox="0 0 {w} {h:.0f}" role="img" aria-label="Map: {title}">'
            f'<rect width="{w}" height="{h:.0f}" class="sea"/><g class="land">{land}</g><g class="dots">{"".join(dots)}</g></svg></figure>')


def build():
    data = json.loads(SRC.read_text())
    base = json.loads(BASEMAP.read_text())
    rows, missing = [], []
    for it in data["institutions"]:
        n = it["institution"]
        if n not in COORDS:
            missing.append(n); continue
        c, la, lo = COORDS[n]
        note = it.get("also_past", "").split(" (")[0]
        rows.append((DISPLAY.get(n, n), it["tier"], c, la, lo, note))
    if missing:
        raise SystemExit(f"No coordinates for: {missing}")
    pts = [(n, t, la, lo, c) for n, t, c, la, lo, _ in rows]
    panels = "".join(svg_panel(p, base, pts) for p in PANELS)
    counts = {t[0]: sum(1 for r in rows if r[1] == t[0]) for t in TIERS}
    legend = "".join(f'<li><i style="background:{col}"></i><b>{lab}</b> &mdash; {desc} ({counts[k]})</li>' for k, lab, desc, col in TIERS)
    by_country = {}
    for n, t, c, _, _, note in rows:
        by_country.setdefault(c, []).append((TIER_RANK[t], n, t, note))
    order = sorted(by_country, key=lambda c: (c != "United Kingdom", c))
    lists = []
    for c in order:
        items = "".join(f'<li><i style="background:{next(x[3] for x in TIERS if x[0] == t)}"></i>{html.escape(n)}'
                        + (f' <span class="inst-note">&middot; {html.escape(note)}</span>' if note else '') + '</li>'
                        for _, n, t, note in sorted(by_country[c]))
        lists.append(f'<div class="country"><h3>{html.escape(c)}</h3><ul class="inst-list">{items}</ul></div>')
    tpl = (SITE / "tools/network.template.html").read_text()
    out = (tpl.replace("{{PANELS}}", panels).replace("{{LEGEND}}", legend).replace("{{LISTS}}", "".join(lists))
              .replace("{{UPDATED}}", date.today().strftime("%-d %B %Y")).replace("{{N}}", str(len(rows))))
    (SITE / "network.html").write_text(out)
    print(f"network.html: {len(rows)} institutions, {len(order)} countries, tiers {counts}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--basemap")
    a = ap.parse_args()
    if a.basemap:
        cut_basemap(a.basemap)
    build()

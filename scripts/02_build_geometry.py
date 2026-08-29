#!/usr/bin/env python3
"""Construit la géométrie des 13 écorégions (et les couches de comparaison) en
coordonnées écran, de façon à ce que la page HTML finale n'ait besoin d'aucune
bibliothèque cartographique.

Source : sous-bassins DCE administratifs (Sandre/OFB, WFS), Lambert-93 (EPSG:2154).
Sortie : data/out/geometry.json — chemins SVG, 1 unité = 1 km.
"""
import json, os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely import make_valid
from groups import ECOREGIONS, SB2ECO

RAW = "data/raw"; OUT = "data/out"
SIMPL = 0.6          # tolérance de simplification, en km
MIN_RING = 3.0       # surface minimale d'un anneau conservé, en km²

def to_svg(geom, xmin, ymax):
    """Lambert-93 (m) -> unités écran (km), origine en haut à gauche."""
    from shapely.ops import transform
    return transform(lambda x, y, z=None: ((x - xmin) / 1000.0, (ymax - y) / 1000.0), geom)

def clean(geom, simpl=SIMPL, min_ring=MIN_RING):
    g = make_valid(geom).simplify(simpl, preserve_topology=True).buffer(0)
    parts = list(getattr(g, "geoms", [g]))
    parts = [p for p in parts if p.area >= min_ring]
    if not parts:
        parts = [max(getattr(g, "geoms", [g]), key=lambda p: p.area)]
    return unary_union(parts)

def path_d(geom, prec=1):
    """Chemin SVG d'un (Multi)Polygon ou (Multi)LineString."""
    out = []
    def ring(coords, close):
        pts = [f"{round(x, prec)},{round(y, prec)}" for x, y in coords]
        # dédoublonnage des points identiques après arrondi
        ded = [pts[0]] + [p for i, p in enumerate(pts[1:], 1) if p != pts[i - 1]]
        if len(ded) < 2: return
        out.append("M" + ded[0] + "L" + "L".join(ded[1:]) + ("Z" if close else ""))
    for g in getattr(geom, "geoms", [geom]):
        if g.geom_type == "Polygon":
            ring(g.exterior.coords, True)
            for h in g.interiors: ring(h.coords, True)
        elif g.geom_type == "LineString":
            ring(g.coords, False)
    return "".join(out)

def load(name):
    return json.load(open(f"{RAW}/{name}"))["features"]

def main():
    # --- sous-bassins -> écorégions -------------------------------------------
    sb_feats = load("SsBassinDCEAdmin_FXX.geojson")
    sb = {}
    for f in sb_feats:
        p = f["properties"]
        sb[p["CdEuSsBassinDCEAdmin"]] = (p["NomSsBassinDCEAdmin"], p["CdEuBassinDCE"],
                                        make_valid(shape(f["geometry"])))
    missing = set(SB2ECO) - set(sb)
    assert not missing, f"sous-bassins absents de la source : {missing}"

    eco_geom = {}
    for key, name, sbs in ECOREGIONS:
        eco_geom[key] = unary_union([sb[s][2] for s in sbs]).buffer(0)

    france = unary_union(list(eco_geom.values()))
    xmin, ymin, xmax, ymax = france.bounds
    print(f"emprise L93 : {xmin:.0f},{ymin:.0f} -> {xmax:.0f},{ymax:.0f}")
    W, H = (xmax - xmin) / 1000, (ymax - ymin) / 1000
    print(f"viewBox {W:.0f} x {H:.0f} km ; surface totale {france.area/1e6:,.0f} km2")

    out = {"viewBox": [0, 0, round(W, 1), round(H, 1)],
           "crs": "EPSG:2154 (Lambert-93), 1 unité SVG = 1 km",
           "outline": "", "ecoregions": [], "subbasins": [], "basins": [],
           "regionsHydro": [], "regionsAdmin": [], "rivers": []}

    france_svg = clean(to_svg(france, xmin, ymax), simpl=0.6, min_ring=3.0)
    out["outline"] = path_d(france_svg)

    for key, name, sbs in ECOREGIONS:
        g = clean(to_svg(eco_geom[key], xmin, ymax))
        big = max(getattr(g, "geoms", [g]), key=lambda p: p.area)
        lab = big.representative_point()
        out["ecoregions"].append({
            "key": key, "name": name, "subbasins": sbs,
            "area_km2": round(eco_geom[key].area / 1e6),
            "path": path_d(g),
            "label": [round(lab.x, 1), round(lab.y, 1)],
        })
        print(f"  {key:14s} {len(out['ecoregions'][-1]['path'])/1024:6.1f} ko de chemin")

    # 34 sous-bassins (couche de comparaison, trait fin)
    for code, (name, bassin, geom) in sorted(sb.items()):
        g = clean(to_svg(geom, xmin, ymax), simpl=1.0, min_ring=5.0)
        out["subbasins"].append({"code": code, "name": name, "basin": bassin,
                                 "eco": SB2ECO[code], "path": path_d(g, 0)})

    # 7 circonscriptions de bassin (loi sur l'eau de 1964)
    bas = {}
    for code, (name, bassin, geom) in sb.items():
        bas.setdefault(bassin, []).append(geom)
    LB = {"FRA": "Artois-Picardie", "FRB1": "Meuse", "FRB2": "Sambre", "FRC": "Rhin",
          "FRD": "Rhône-Méditerranée", "FRE": "Corse", "FRF": "Adour-Garonne",
          "FRG": "Loire-Bretagne", "FRH": "Seine-Normandie"}
    for code, geoms in sorted(bas.items()):
        g = clean(to_svg(unary_union(geoms).buffer(0), xmin, ymax), simpl=1.0, min_ring=5.0)
        out["basins"].append({"code": code, "name": LB.get(code, code), "path": path_d(g, 0)})

    # 24 régions hydrographiques (Sandre) : le tracé hydrographique « vrai »,
    # non recalé sur les limites communales — sert à montrer l'écart avec le découpage retenu
    for f in load("RegionHydro.geojson"):
        p = f["properties"]
        if p["CdRegionHydro"] == "Z":                      # îles marines
            continue
        g = clean(to_svg(make_valid(shape(f["geometry"])), xmin, ymax), simpl=1.0, min_ring=5.0)
        out["regionsHydro"].append({"code": p["CdRegionHydro"],
                                    "name": p["LbRegionHydro"].strip(), "path": path_d(g, 0)})

    # régions administratives 2016 (WGS84 -> L93 -> écran)
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
    from shapely.ops import transform
    for f in load("regions_admin.geojson"):
        g = transform(lambda x, y, z=None: tr.transform(x, y), shape(f["geometry"]))
        g = clean(to_svg(g, xmin, ymax), simpl=1.5, min_ring=10.0)
        out["regionsAdmin"].append({"name": f["properties"]["nom"], "path": path_d(g, 0)})

    # cours d'eau de classe 1 (habillage)
    dom = france_svg.buffer(2.0)                       # découpe des tronçons hors frontières
    for f in load("CoursEau1.geojson"):
        g = to_svg(shape(f["geometry"]), xmin, ymax).simplify(0.8).intersection(dom)
        if g.is_empty or g.length < 15: continue           # on écarte les tronçons < 15 km
        out["rivers"].append({"name": f["properties"]["NomEntiteHydrographique"],
                              "path": path_d(g, 0)})

    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/geometry.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"écrit {OUT}/geometry.json : {os.path.getsize(f'{OUT}/geometry.json')/1024/1024:.2f} Mo, "
          f"{len(out['rivers'])} cours d'eau, {len(out['regionsAdmin'])} régions")

if __name__ == "__main__":
    main()

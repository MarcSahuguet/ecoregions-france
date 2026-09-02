#!/usr/bin/env python3
"""Les bassins ne s'arrêtent pas à la frontière.

Reconstitue les bassins versants complets (parties étrangères comprises) à partir de
HydroBASINS (HydroSHEDS, WWF, CC-BY 4.0, niveau 6 dissous par MAIN_BAS), mesure la part
française de chacun, et prépare une carte d'ensemble européenne.
Surfaces calculées en ETRS89-LAEA (EPSG:3035), projection équivalente.
Sortie : data/out/transfrontalier.json
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import shapefile
from shapely.geometry import shape
from shapely.ops import unary_union, transform
from shapely import make_valid
from pyproj import Transformer
from groups import SB2ECO, ECOREGIONS

RAW, OUT = "data/raw", "data/out"
MIN_FR = 4000            # km² en France, en deçà on ignore le bassin

# HydroBASINS ne nomme pas les bassins : on les nomme d'après les sous-bassins français
# qu'ils contiennent, du plus englobant au plus local.
FLEUVES = [("Rhin", {"FRC_RHIN", "FRC_MOSE"}), ("Meuse", {"FRB1_MEUS", "FRB2_SAMB"}),
           ("Escaut", {"FRA_ESCA"}),
           ("Rhône", {"FRD_SAON", "FRD_RHON", "FRD_HRHO", "FRD_ISER", "FRD_DURA", "FRD_DOUB"}),
           ("Seine", {"FRH_SEAM", "FRH_SEAV", "FRH_MARN", "FRH_OISE", "FRH_IF"}),
           ("Loire", {"FRG_ALA", "FRG_LMOY"}), ("Côtiers vendéens", {"FRG_LACV"}),
           ("Maine", {"FRG_MSL"}), ("Vienne", {"FRG_VICR"}),
           ("Garonne", {"FRF_GARO", "FRF_TARN", "FRF_LOT"}), ("Adour", {"FRF_ADOU"}),
           ("Dordogne", {"FRF_DORD"}), ("Charente", {"FRF_CHAR"}),
           ("Vilaine", {"FRG_VICO"}), ("Corse", {"FRE_CORS"}),
           ("Côtiers de la Côte d'Azur", {"FRD_COCA"}),
           ("Côtiers du Languedoc", {"FRD_COLR"})]
NOMS = dict((k, n) for k, n, _ in ECOREGIONS)

to3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True).transform
l93to3035 = Transformer.from_crs("EPSG:2154", "EPSG:3035", always_xy=True).transform

def main():
    # --- France et sous-bassins, en 3035 ---------------------------------------
    sb = {}
    for f in json.load(open(f"{RAW}/SsBassinDCEAdmin_FXX.geojson"))["features"]:
        p = f["properties"]
        g = transform(l93to3035, make_valid(shape(f["geometry"])))
        g = g.simplify(1000, preserve_topology=True).buffer(0)
        sb[p["CdEuSsBassinDCEAdmin"]] = (p["NomSsBassinDCEAdmin"], g)
    france = unary_union([g for _, g in sb.values()]).buffer(0)
    pts = {code: (nom, g.representative_point()) for code, (nom, g) in sb.items()}
    from shapely.prepared import prep
    print(f"France : {france.area/1e6:,.0f} km²")

    # --- HydroBASINS niveau 6, dissous par bassin principal --------------------
    r = shapefile.Reader(f"{RAW}/hybas_eu/hybas_eu_lev06_v1c.shp")
    champs = [f[0] for f in r.fields[1:]]
    # Deux passes : on repère d'abord les bassins principaux qui touchent l'emprise,
    # puis on prend TOUS leurs polygones — y compris ceux qui en sortent. Filtrer
    # polygone par polygone tronquerait la surface totale publiée du bassin.
    EMPRISE = (-8, 38, 20, 56)                           # en degrés
    brut = []
    proches = set()
    for sr in r.iterShapeRecords():
        rec = dict(zip(champs, sr.record))
        x0, y0, x1, y1 = sr.shape.bbox
        brut.append((rec["MAIN_BAS"], sr.shape))
        if not (x1 < EMPRISE[0] or x0 > EMPRISE[2] or y1 < EMPRISE[1] or y0 > EMPRISE[3]):
            proches.add(rec["MAIN_BAS"])
    groupes = collections.defaultdict(list)
    for mb, sh in brut:
        if mb not in proches: continue
        g = transform(to3035, shape(sh.__geo_interface__)).simplify(1500, preserve_topology=True)
        groupes[mb].append(make_valid(g).buffer(0))
    print(f"{len(groupes)} bassins principaux dans l'emprise, "
          f"{sum(len(v) for v in groupes.values())} polygones (parties étrangères comprises)")

    res = []
    for mb, parts in groupes.items():
        bassin = unary_union(parts).buffer(0)
        inter = bassin.intersection(france)
        if inter.is_empty or inter.area / 1e6 < MIN_FR:
            continue
        # nom : d'après les sous-bassins français dont le point représentatif tombe dedans
        pb = prep(bassin)
        dedans = [(code, nom) for code, (nom, pt) in pts.items() if pb.contains(pt)]
        if not dedans:
            continue
        codes = {c for c, _ in dedans}
        best = next(((nom, nom) for nom, cs in FLEUVES if cs & codes),
                    max(dedans, key=lambda cn: sb[cn[0]][1].area))
        eco = collections.Counter()
        for code, _ in dedans:
            eco[SB2ECO[code]] += sb[code][1].area
        res.append({"main_bas": mb, "sous_bassin": best[1], "eco": eco.most_common(1)[0][0],
                    "total_km2": round(bassin.area / 1e6),
                    "france_km2": round(inter.area / 1e6),
                    "part_fr": round(100 * inter.area / bassin.area, 1),
                    "geom": bassin})
    res.sort(key=lambda d: -d["total_km2"])
    for d in res:
        print(f"  {d['sous_bassin'][:28]:28s} {d['total_km2']:8,d} km²  "
              f"dont France {d['france_km2']:7,d}  ({d['part_fr']:5.1f} %)  -> {NOMS[d['eco']]}")

    # --- cadre de la carte d'ensemble ------------------------------------------
    tout = unary_union([d["geom"] for d in res] + [france]).buffer(0)
    xmin, ymin, xmax, ymax = tout.bounds
    ech = 900.0 / (xmax - xmin)
    def svg(g, simpl=4000):
        g = g.simplify(simpl, preserve_topology=True).buffer(0)
        out = []
        for p in getattr(g, "geoms", [g]):
            if p.geom_type != "Polygon" or p.area < 3e8: continue
            pts = [f"{(x-xmin)*ech:.1f},{(ymax-y)*ech:.1f}" for x, y in p.exterior.coords]
            ded = [pts[0]] + [q for i, q in enumerate(pts[1:], 1) if q != pts[i-1]]
            if len(ded) > 3: out.append("M" + ded[0] + "L" + "L".join(ded[1:]) + "Z")
        return "".join(out)

    # --- tracés réels des 4 fleuves transfrontaliers (WGS84 → 3035 → SVG) ------
    def pt(lon, lat):
        x3, y3 = to3035(lon, lat)
        return f"{(x3-xmin)*ech:.1f},{(ymax-y3)*ech:.1f}"

    RIVER_PTS = {
        "Rhin": [   # source → Constance → Bâle → Strasbourg → Mannheim → Coblence → Cologne → Rotterdam
            (9.05,46.61),(9.37,47.17),(9.47,47.65),(9.38,47.53),
            (7.59,47.55),(7.67,47.90),(7.72,48.30),(7.78,48.58),
            (8.23,49.00),(8.38,49.01),(8.27,49.50),(8.20,49.99),
            (7.60,50.35),(7.15,50.70),(6.96,50.94),(6.69,51.19),
            (6.17,51.50),(5.80,51.82),(4.48,51.92)],
        "Rhône": [  # glacier du Rhône → Lac Léman → Genève → Belley → Lyon → Valence → Avignon → Arles → mer
            (8.31,46.61),(7.55,46.40),(6.55,46.45),(6.15,46.20),
            (5.82,45.90),(5.47,45.60),(5.02,45.73),(4.84,45.76),
            (4.83,45.40),(4.87,45.05),(4.89,44.93),(4.78,44.55),
            (4.81,43.95),(4.72,43.68),(4.63,43.43),(4.73,43.43)],
        "Meuse": [  # Pouilly-en-Bassigny → Bar-le-Duc → Verdun → Sedan → Namur → Liège → Maastricht → mer
            (5.70,47.88),(5.45,48.55),(5.38,49.16),(5.15,49.40),
            (4.94,49.70),(4.70,50.05),(4.87,50.46),(5.10,50.55),
            (5.57,50.64),(5.69,50.85),(5.62,51.20),(5.50,51.55),(4.48,51.92)],
        "Escaut": [ # Saint-Quentin → Cambrai → Valenciennes → Tournai → Gand → Anvers → mer du Nord
            (3.32,49.85),(3.22,50.17),(3.39,50.37),(3.39,50.61),
            (3.55,50.75),(3.72,51.05),(3.98,51.05),(4.40,51.22),(3.59,51.45)],
    }
    def river_path(pts):
        coords = [pt(lon, lat) for lon, lat in pts]
        return "M" + coords[0] + "L" + "L".join(coords[1:])

    rivers = [{"nom": n, "path": river_path(pts)} for n, pts in RIVER_PTS.items()]

    data = {"viewBox": [0, 0, round((xmax-xmin)*ech, 1), round((ymax-ymin)*ech, 1)],
            "france": svg(france),
            "bassins": [{"nom": d["sous_bassin"], "eco": d["eco"], "ecoNom": NOMS[d["eco"]],
                         "total_km2": d["total_km2"], "france_km2": d["france_km2"],
                         "part_fr": d["part_fr"], "path": svg(d["geom"])} for d in res],
            "rivers": rivers}
    json.dump(data, open(f"{OUT}/transfrontalier.json", "w"), ensure_ascii=False,
              separators=(",", ":"))
    print(f"écrit {OUT}/transfrontalier.json "
          f"({os.path.getsize(f'{OUT}/transfrontalier.json')/1024:.0f} ko)")

if __name__ == "__main__":
    main()

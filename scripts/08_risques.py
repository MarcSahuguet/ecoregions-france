#!/usr/bin/env python3
"""Exposition au risque d'inondation et de submersion, par écorégion.

Sources : base GASPAR (Géorisques, millésime 2026-08-19) — arrêtés de catastrophe naturelle
et plans de prévention des risques naturels, tous deux au niveau communal.
Sortie : data/out/risques.json
"""
import csv, glob, json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from groups import SB2ECO, ECOREGIONS
import commune_map

RAW, OUT = "data/raw", "data/out"
DEPUIS = "2015"                      # fenêtre récente pour les arrêtés
NOMS = dict((k, n) for k, n, _ in ECOREGIONS)

def lire(motif):
    p = glob.glob(f"{RAW}/gaspar/{motif}")[0]
    return list(csv.DictReader(open(p, encoding="utf-8-sig"), delimiter=";"))

def main():
    c2sb = commune_map.load()
    eco = lambda code: SB2ECO[c2sb[code][0]] if code in c2sb else None
    pop = {c["code"]: (c.get("population") or 0)
           for c in json.load(open(f"{RAW}/geoapi_communes.json"))}

    agg = {k: {"communes": 0, "pop": 0, "catnat_communes": set(), "catnat_arretes": 0,
               "pprn_i": set(), "pprn_sub": set()} for k, _, _ in ECOREGIONS}
    for code, sbs in c2sb.items():
        k = SB2ECO[sbs[0]]
        if code in pop:
            agg[k]["communes"] += 1; agg[k]["pop"] += pop[code]

    for r in lire("catnat_*.csv"):
        if "Inondation" not in r["lib_risque_jo"] and "Inondations" not in r["lib_risque_jo"]:
            continue
        if (r["date_debut"] or "")[:4] < DEPUIS: continue
        k = eco(r["code_commune"])
        if not k: continue
        agg[k]["catnat_arretes"] += 1
        agg[k]["catnat_communes"].add(r["code_commune"])

    for r in lire("pprn_*.csv"):
        if r["LIBELLE ETAT"] != "Opposable": continue
        k = eco(r["CODE INSEE COMMUNE"])
        if not k: continue
        libs = " ".join(r.get(f"LIBELLE RISQUE {i}") or "" for i in (1, 2, 3))
        if "submersion" in libs.lower(): agg[k]["pprn_sub"].add(r["CODE INSEE COMMUNE"])
        if "Inondation" in libs or "crue" in libs or "ruissellement" in libs.lower():
            agg[k]["pprn_i"].add(r["CODE INSEE COMMUNE"])

    res, tot = {}, collections.Counter()
    for k, nom, _ in ECOREGIONS:
        a = agg[k]
        pop_pprn = sum(pop.get(c, 0) for c in a["pprn_i"])
        pop_sub = sum(pop.get(c, 0) for c in a["pprn_sub"])
        res[k] = {
            "communes": a["communes"],
            "catnat_arretes": a["catnat_arretes"],
            "catnat_communes": len(a["catnat_communes"]),
            "catnat_part": round(100 * len(a["catnat_communes"]) / a["communes"], 1),
            "pprn_communes": len(a["pprn_i"]),
            "pprn_part_pop": round(100 * pop_pprn / a["pop"], 1),
            "pprn_pop": pop_pprn,
            "sub_communes": len(a["pprn_sub"]),
            "sub_pop": pop_sub,
        }
        for f in ("catnat_arretes", "catnat_communes", "communes", "pprn_communes"):
            tot[f] += res[k][f] if f != "communes" else a["communes"]
        tot["pprn_pop"] += pop_pprn; tot["pop"] += a["pop"]; tot["sub_pop"] += pop_sub
    res["_national"] = {"catnat_arretes": tot["catnat_arretes"],
                        "catnat_part": round(100 * tot["catnat_communes"] / tot["communes"], 1),
                        "pprn_part_pop": round(100 * tot["pprn_pop"] / tot["pop"], 1),
                        "sub_pop": tot["sub_pop"], "depuis": int(DEPUIS)}
    json.dump(res, open(f"{OUT}/risques.json", "w"), ensure_ascii=False, indent=1)
    for k, nom, _ in ECOREGIONS:
        r = res[k]
        print(f"{nom[:24]:24s} catnat {r['catnat_arretes']:6d} arrêtés, {r['catnat_part']:5.1f} % des communes | "
              f"PPRN inond. {r['pprn_part_pop']:5.1f} % de la population | submersion {r['sub_pop']/1000:6.0f} k hab")
    print("national :", res["_national"])

if __name__ == "__main__":
    main()

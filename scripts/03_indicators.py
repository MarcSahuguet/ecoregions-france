#!/usr/bin/env python3
"""Calcule les indicateurs par écorégion depuis les données ouvertes.

Sorties : data/out/indicators.json
Sources : INSEE (population légale, PIB régional), SDES/Corine Land Cover 2018,
BNPE via Hub'Eau (prélèvements 2020-2022), Sandre/OFB (table commune -> sous-bassin).
"""
import csv, json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from groups import ECOREGIONS, SB2ECO
import commune_map

RAW, OUT = "data/raw", "data/out"
KEYS = [k for k, _, _ in ECOREGIONS]
NOMS = dict((k, n) for k, n, _ in ECOREGIONS)

REGIONS = {"11": "Île-de-France", "24": "Centre-Val de Loire", "27": "Bourgogne-Franche-Comté",
           "28": "Normandie", "32": "Hauts-de-France", "44": "Grand Est", "52": "Pays de la Loire",
           "53": "Bretagne", "75": "Nouvelle-Aquitaine", "76": "Occitanie",
           "84": "Auvergne-Rhône-Alpes", "93": "Provence-Alpes-Côte d'Azur", "94": "Corse"}

USAGES = {"AEP": "Eau potable", "IRR": "Irrigation", "IND": "Industrie",
          "ENE": "Refroidissement des centrales", "CAN": "Canaux",
          "BAR": "Turbinage hydroélectrique"}
CONSO = ["AEP", "IRR", "IND", "ENE", "CAN"]     # prélèvements hors turbinage

def pib_par_hab():
    """PIB/hab régional 2024 (INSEE, comptes régionaux base 2020)."""
    import openpyxl
    ws = openpyxl.load_workbook(f"{RAW}/insee_pib_reg.xlsx", data_only=True)["PIB par habitant"]
    rows = list(ws.iter_rows(values_only=True))
    head = next(r for r in rows if str(r[1]).strip() == "1990")
    col = [i for i, v in enumerate(head) if str(v).strip() == "2024"][0]
    out = {}
    for r in rows:
        lab = (r[0] or "").strip()
        for code, nom in REGIONS.items():
            if lab == nom and isinstance(r[col], (int, float)):
                out[code] = r[col]
    assert len(out) == 13, out
    return out

def clc_par_commune():
    """CLC 2018, 5 postes, en ha, par code commune (COG 2010)."""
    out = {}
    with open(f"{RAW}/clc5_communes.csv", encoding="utf-8-sig") as f:
        for row in csv.reader(f, delimiter=";"):
            if len(row) < 8 or row[1] != "2018":
                continue
            try:
                vals = [float(v.replace(",", ".")) if v not in ("", "n/a") else 0.0 for v in row[3:8]]
            except ValueError:
                continue
            out[row[0]] = vals
    return out

def prelevements():
    """Volumes prélevés par commune et par usage, moyenne 2020-2022 (m3/an)."""
    acc = collections.defaultdict(lambda: collections.Counter())
    years = 0
    for an in (2020, 2021, 2022):
        p = f"{RAW}/bnpe_{an}.json"
        if not os.path.exists(p): continue
        years += 1
        for r in json.load(open(p)):
            c = r.get("code_commune_insee")
            if not c: continue
            acc[c][r["code_usage"]] += r.get("volume") or 0
    for c in acc:
        for u in acc[c]: acc[c][u] /= max(years, 1)
    return acc

def main():
    c2sb = commune_map.load()
    communes = json.load(open(f"{RAW}/geoapi_communes.json"))
    pibh, clc, prel = pib_par_hab(), clc_par_commune(), prelevements()

    agg = {k: {"pop": 0.0, "area_km2": 0.0, "communes": 0, "pib_meur": 0.0,
               "clc": [0.0] * 5, "clc_ha": 0.0,
               "prel": collections.Counter(), "regions": collections.Counter(),
               "departements": set(),
               "villes": [], "subbasins": collections.Counter()} for k in KEYS}
    sb_pop = collections.Counter()
    hors = {"communes": 0, "pop": 0}

    for c in communes:
        code = c["code"]
        if code.startswith(("97", "98")): continue
        sbs = c2sb.get(code)
        if not sbs:
            hors["communes"] += 1; hors["pop"] += c.get("population") or 0; continue
        ecos = sorted(set(SB2ECO[s] for s in sbs))
        w = 1.0 / len(ecos)
        pop = (c.get("population") or 0) * w
        area = (c.get("surface") or 0) / 100.0 * w          # ha -> km2
        for s in sbs: sb_pop[s] += (c.get("population") or 0) / len(sbs)
        for k in ecos:
            a = agg[k]
            a["pop"] += pop; a["area_km2"] += area; a["communes"] += w
            a["regions"][c["codeRegion"]] += pop
            a["departements"].add(c["codeDepartement"])
            a["pib_meur"] += pop * pibh.get(c["codeRegion"], 0) / 1e6
            for s in sbs:
                if SB2ECO[s] == k: a["subbasins"][s] += pop / len(sbs)
            v = clc.get(code)
            if v:
                for i in range(5): a["clc"][i] += v[i] * w
                a["clc_ha"] += sum(v) * w
            p = prel.get(code)
            if p:
                for u, vol in p.items(): a["prel"][u] += vol * w
            if (c.get("population") or 0) > 40000:
                a["villes"].append((c["nom"], c.get("population") or 0))

    partagees = sum(1 for c in communes if len(set(SB2ECO[s] for s in c2sb.get(c["code"], []))) > 1)
    multi_sb = sum(1 for c in communes if len(set(c2sb.get(c["code"], []))) > 1)

    # --- ampleur du bouleversement : ce qui fonde le coût de la réforme -----------
    deps = {d["code"]: d["nom"] for d in json.load(open(f"{RAW}/geoapi_departements.json"))}
    dep_eco, reg_eco = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for c in communes:
        if c["code"].startswith(("97", "98")): continue
        sbs = c2sb.get(c["code"])
        if not sbs: continue
        # même règle que l'agrégation principale : une commune à cheval est répartie
        ecos = sorted(set(SB2ECO[s] for s in sbs))
        pop_c = (c.get("population") or 0) / len(ecos)
        for k in ecos:
            dep_eco[c["codeDepartement"]][k] += pop_c
            reg_eco[c["codeRegion"]][k] += pop_c

    def parts(counter):
        t = counter.total()
        return sorted(((100 * v / t, k) for k, v in counter.items()), reverse=True)

    dep_partages = {}
    for seuil in (1, 5, 10, 25):
        dep_partages[seuil] = sum(1 for v in dep_eco.values()
                                  if sum(1 for p, _ in parts(v) if p >= seuil) > 1)
    ecarteles = []
    for code, v in dep_eco.items():
        pp = parts(v)
        if len(pp) > 1 and pp[1][0] >= 10:
            ecarteles.append({"code": code, "nom": deps.get(code, code),
                              "parts": [{"eco": k, "part": round(p, 1)} for p, k in pp if p >= 1]})
    ecarteles.sort(key=lambda d: -d["parts"][1]["part"])

    regions_eclatees = []
    for r, v in reg_eco.items():
        pp = [(p, k) for p, k in parts(v) if p >= 5]
        regions_eclatees.append({"region": REGIONS[r], "n": len(pp),
                                 "parts": [{"eco": k, "part": round(p, 1)} for p, k in pp]})
    regions_eclatees.sort(key=lambda d: (-d["n"], -d["parts"][0]["part"]))

    tot_pop = sum(a["pop"] for a in agg.values())
    tot_area = sum(a["area_km2"] for a in agg.values())
    tot_prel = collections.Counter()
    for a in agg.values(): tot_prel.update(a["prel"])

    res = {"meta": {"pop_totale": round(tot_pop), "surface_totale_km2": round(tot_area),
                    "communes_non_rattachees": hors,
                    "communes_sur_2_sous_bassins": multi_sb,
                    "communes_sur_2_ecoregions": partagees,
                    "perturbation": {
                        "departements_total": len(dep_eco),
                        "departements_partages": dep_partages,
                        "departements_ecarteles": ecarteles,
                        "regions_eclatees": regions_eclatees},
                    "prelevements_nationaux_Mm3": {u: round(tot_prel[u] / 1e6) for u in USAGES},
                    "sources": {
                        "decoupage": "Sous-bassins DCE administratifs, Sandre/OFB (WFS, 2026)",
                        "population": "INSEE, populations légales (API Découpage administratif)",
                        "occupation_sol": "Corine Land Cover 2018, SDES — 5 postes, par commune",
                        "prelevements": "BNPE via Hub'Eau, moyenne 2020-2022",
                        "pib": "INSEE, comptes régionaux base 2020, PIB/hab 2024 (estimation par répartition démographique)"}},
           "ecoregions": []}

    for key, nom, sbs in ECOREGIONS:
        a = agg[key]
        clc_tot = max(a["clc_ha"], 1)
        pc = [100 * v / clc_tot for v in a["clc"]]
        pr = a["prel"]
        conso = sum(pr[u] for u in CONSO)
        regs = sorted(a["regions"].items(), key=lambda kv: -kv[1])
        res["ecoregions"].append({
            "key": key, "nom": nom,
            "pop": round(a["pop"]), "pop_part": round(100 * a["pop"] / tot_pop, 1),
            "area_km2": round(a["area_km2"]), "area_part": round(100 * a["area_km2"] / tot_area, 1),
            "densite": round(a["pop"] / a["area_km2"], 1),
            "communes": round(a["communes"]),
            "departements": len(a["departements"]),
            "pib_meur": round(a["pib_meur"]),
            "pib_hab": round(a["pib_meur"] * 1e6 / a["pop"]),
            "clc_pct": {"artificialise": round(pc[0], 1), "agricole": round(pc[1], 1),
                        "foret_naturel": round(pc[2], 1), "zones_humides": round(pc[3], 2),
                        "eau": round(pc[4], 2)},
            "prel_Mm3": {u: round(pr[u] / 1e6, 1) for u in USAGES},
            "prel_conso_Mm3": round(conso / 1e6, 1),
            "prel_conso_part": round(100 * conso / sum(tot_prel[u] for u in CONSO), 1),
            "prel_hab_m3": round(conso / a["pop"]),
            "prel_part_irrigation": round(100 * pr["IRR"] / conso, 1) if conso else 0,
            "regions_recoupees": [{"nom": REGIONS[r], "part_pop": round(100 * v / a["pop"], 1)}
                                  for r, v in regs if 100 * v / a["pop"] >= 0.5],
            "villes": [{"nom": n, "pop": p} for n, p in sorted(a["villes"], key=lambda t: -t[1])[:8]],
            "sous_bassins": [{"code": s, "pop": round(a["subbasins"][s])} for s in sbs],
        })

    deb = json.load(open(f"{OUT}/debits.json")) if os.path.exists(f"{OUT}/debits.json") else {}
    for e in res["ecoregions"]:
        d = deb.get(e["key"])
        if d:
            e["hydro"] = dict(d, debit_specifique_ls_km2=round(d["module_m3s"] * 1000 / d["surface_bv_km2"], 1),
                              volume_annuel_Mm3=round(d["module_m3s"] * 31.5576, 0))

    os.makedirs(OUT, exist_ok=True)
    chg = sum(a["pop"] - max(a["regions"].values()) for a in agg.values())
    res["meta"]["perturbation"]["pop_changeant_de_collectivite"] = round(chg)
    res["meta"]["perturbation"]["part_changeant_de_collectivite"] = round(100 * chg / tot_pop, 1)

    json.dump(res, open(f"{OUT}/indicators.json", "w"), ensure_ascii=False, indent=1)

    print(f"population totale {tot_pop/1e6:.2f} M, surface {tot_area:,.0f} km2")
    print(f"communes non rattachées : {hors}")
    print(f"prélèvements hors turbinage : {sum(tot_prel[u] for u in CONSO)/1e9:.1f} Md m3/an")
    for e in res["ecoregions"]:
        print(f"{e['key']:14s} {e['pop']/1e6:5.2f}M {e['densite']:6.0f}h/km2 "
              f"PIB/hab {e['pib_hab']:6d}€ art{e['clc_pct']['artificialise']:5.1f}% "
              f"agri{e['clc_pct']['agricole']:5.1f}% forêt{e['clc_pct']['foret_naturel']:5.1f}% "
              f"prél {e['prel_conso_Mm3']:8.0f} Mm3 ({e['prel_part_irrigation']:4.1f}% irrig) "
              f"régions {len(e['regions_recoupees'])}")

if __name__ == "__main__":
    main()

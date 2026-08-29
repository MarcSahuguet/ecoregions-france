#!/usr/bin/env python3
"""Module (débit moyen interannuel) de l'exutoire principal de chaque écorégion.

Méthode : parmi les sites hydrométriques Hub'Eau situés dans l'écorégion, on retient
celui qui draine le plus grand bassin et qui dispose d'au moins 5 ans de débits
journaliers (QmnJ) sur 2015-2024. Sortie : data/out/debits.json
"""
import json, os, sys, time, urllib.request, urllib.error, collections
sys.path.insert(0, os.path.dirname(__file__))
from groups import SB2ECO, ECOREGIONS
import commune_map

MIN_JOURS = 1800

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(8 * (i + 1))
        except Exception:
            time.sleep(8 * (i + 1))
    return None

def module(code):
    """Débit moyen (m3/s) et nombre de jours disponibles, 2015-2024."""
    tot = n = 0
    page = 1
    while True:
        d = get("https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
                f"?code_entite={code}&grandeur_hydro_elab=QmnJ"
                "&date_debut_obs_elab=2015-01-01&date_fin_obs_elab=2024-12-31"
                f"&size=20000&page={page}&fields=resultat_obs_elab")
        if not d or not d.get("data"): break
        for o in d["data"]:
            v = o.get("resultat_obs_elab")
            if v is not None and v >= 0: tot += v; n += 1
        if not d.get("next"): break
        page += 1
    return (tot / n / 1000.0 if n else None), n     # L/s -> m3/s

def main():
    c2sb = commune_map.load()
    sites = json.load(open("data/raw/hydro_sites.json"))["data"]
    cand = collections.defaultdict(list)
    for s in sites:
        sb = next((c2sb[c][0] for c in (s.get("code_commune_site") or []) if c in c2sb), None)
        if not sb or not s.get("surface_bv"): continue
        cand[SB2ECO[sb]].append(s)
    out = {}
    for key, nom, _ in ECOREGIONS:
        for s in sorted(cand[key], key=lambda x: -x["surface_bv"])[:8]:
            q, n = module(s["code_site"])
            print(f"  {key:14s} essai {s['code_site']} {s['libelle_site'][:48]:48s} "
                  f"{s['surface_bv']:8.0f} km2 -> {q if q is None else round(q,1)} m3/s ({n} j)")
            if q and n >= MIN_JOURS:
                out[key] = {"station": s["libelle_site"], "code": s["code_site"],
                            "cours_eau": s.get("libelle_cours_eau"),
                            "surface_bv_km2": s["surface_bv"],
                            "module_m3s": round(q, 1), "jours": n}
                break
        else:
            print(f"  {key}: aucune station exploitable")
    json.dump(out, open("data/out/debits.json", "w"), ensure_ascii=False, indent=1)
    for k, v in out.items():
        print(f"{k:14s} {v['module_m3s']:8.1f} m3/s  {v['station'][:60]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Saisonnalité du débit : moyenne par mois calendaire, 2015-2024.

Source : Hub'Eau hydrométrie, débits moyens journaliers (QmnJ) de la station retenue pour
chaque écorégion (cf. 04_debits.py). Mesures officielles, pas un modèle.
Sortie : data/out/saisonnalite.json
"""
import json, os, sys, time, urllib.request, urllib.error, collections

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

def mensuel(code):
    somme, n = collections.Counter(), collections.Counter()
    page = 1
    while True:
        d = get("https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
                f"?code_entite={code}&grandeur_hydro_elab=QmnJ"
                "&date_debut_obs_elab=2015-01-01&date_fin_obs_elab=2024-12-31"
                f"&size=20000&page={page}&fields=date_obs_elab,resultat_obs_elab")
        if not d or not d.get("data"): break
        for o in d["data"]:
            v, dt = o.get("resultat_obs_elab"), o.get("date_obs_elab")
            if v is None or v < 0 or not dt: continue
            m = int(dt[5:7])
            somme[m] += v / 1000.0                      # L/s -> m3/s
            n[m] += 1
        if not d.get("next"): break
        page += 1
    if len(n) < 12:                       # un mois calendaire sans aucune mesure
        return None
    return [round(somme[m] / n[m], 1) for m in range(1, 13)]

def main():
    deb = json.load(open("data/out/debits.json"))
    out = {}
    for key, d in deb.items():
        mois = mensuel(d["code"])
        if not mois:
            print(f"  {key}: série mensuelle incomplète, écorégion ignorée"); continue
        hi = max(range(12), key=lambda i: mois[i])
        lo = min(range(12), key=lambda i: mois[i])
        out[key] = {"station": d["station"], "mois": mois,
                    "mois_haut": hi + 1, "mois_bas": lo + 1,
                    "rapport": round(mois[hi] / mois[lo], 1) if mois[lo] else None}
        print(f"  {key:14s} max {mois[hi]:8.1f} (mois {hi+1:2d})  min {mois[lo]:7.1f} "
              f"(mois {lo+1:2d})  rapport {out[key]['rapport']}")
    json.dump(out, open("data/out/saisonnalite.json", "w"), ensure_ascii=False, indent=1)
    print(f"écrit data/out/saisonnalite.json ({len(out)} écorégions)")

if __name__ == "__main__":
    main()

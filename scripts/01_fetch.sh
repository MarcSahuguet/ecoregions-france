#!/bin/bash
# Téléchargements idempotents des sources ouvertes (Licence Ouverte 2.0).
set -euo pipefail
cd "$(dirname "$0")/../data/raw"

wfs() { # wfs <endpoint> <layer> [extra curl args...]
  local ep=$1 layer=$2; shift 2
  [ -s "$layer.geojson" ] && { echo "skip $layer"; return; }
  echo "fetch $layer"
  curl -sS --max-time 1800 -o "$layer.geojson" -G \
    "https://services.sandre.eaufrance.fr/geo/$ep" \
    --data-urlencode "SERVICE=WFS" --data-urlencode "VERSION=2.0.0" \
    --data-urlencode "REQUEST=GetFeature" --data-urlencode "TYPENAMES=sa:$layer" \
    --data-urlencode "OUTPUTFORMAT=application/json; subtype=geojson" \
    --data-urlencode "SRSNAME=EPSG:2154" "$@"
}

# --- Géométries hydrographiques (Sandre / OFB / IGN) ---
wfs sandre SsBassinDCEAdmin_FXX          # 34 sous-bassins DCE administratifs -> briques des écorégions
wfs sandre SousBassinDCE_Communes        # table commune -> sous-bassin
wfs zonage RegionHydro                   # 24 régions hydrographiques (couche de comparaison)
wfs sandre Hydroecoregion1_FXX           # 22 hydro-écorégions HER1 (Wasson) - comparaison naturaliste

# --- BD TOPAGE 2025 (bassins + cours d'eau) ---
topage() { # topage <couche>
  local l=$1
  [ -s "$l.zip" ] || curl -sSL --max-time 1800 -o "$l.zip" \
    "https://services.sandre.eaufrance.fr/telechargement/geo/ETH/BDTopage/2025/$l/${l}_FXX-geojson.zip"
  [ -d "$(echo "$l" | tr 'A-Z' 'a-z')" ] || unzip -o -q "$l.zip" -d "$(echo "$l" | tr 'A-Z' 'a-z')"
}
topage BassinHydrographique               # 7 circonscriptions de bassin métropolitaines

# --- Habillage : cours d'eau principaux (Sandre, classés par importance) ---
wfs zonage CoursEau1
wfs zonage CoursEau2

# --- Régions administratives 2016 (comparaison) ---
[ -s regions_admin.geojson ] || curl -sSL --max-time 600 -o regions_admin.geojson \
  "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"

# --- Communes (population, surface, centroïde) : API Découpage administratif ---
[ -s geoapi_communes.json ] || curl -sSL --max-time 600 -o geoapi_communes.json \
  "https://geo.api.gouv.fr/communes?fields=code,nom,population,surface,centre,codeDepartement,codeRegion&format=json"

# --- Occupation du sol par commune (CLC 2018, SDES, 5 postes) ---
[ -s clc5_communes.csv ] || curl -sSL --max-time 900 -o clc5_communes.csv \
  "https://www.statistiques.developpement-durable.gouv.fr/media/2546/download?inline"

# --- Prélèvements d'eau par ouvrage (BNPE via Hub'Eau) ---
for an in 2020 2021 2022; do
  [ -s "bnpe_$an.json" ] && continue
  python3 - "$an" <<'PY'
import json, sys, urllib.request
an = sys.argv[1]; rows = []; page = 1
while True:
    u = ("https://hubeau.eaufrance.fr/api/v1/prelevements/chroniques?"
         f"annee={an}&size=20000&page={page}"
         "&fields=code_commune_insee,code_departement,volume,code_usage,annee")
    with urllib.request.urlopen(u, timeout=300) as r:
        d = json.load(r)
    rows += d["data"]
    print(f"{an} page {page}: {len(rows)}/{d['count']}", file=sys.stderr)
    if not d.get("next") or len(rows) >= d["count"]: break
    page += 1
json.dump(rows, open(f"bnpe_{an}.json", "w"))
PY
done

# --- Hydrométrie : débits moyens des stations (Hub'Eau) ---
[ -s hydro_stations.json ] || curl -sSL --max-time 600 -o hydro_stations.json \
  "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/stations?size=10000&format=json&fields=code_station,libelle_station,code_commune_station,longitude_station,latitude_station,influence_locale_station,en_service"

# --- Hydrométrie : sites de mesure (Hub'Eau) + débits journaliers des exutoires ---
[ -s hydro_sites.json ] || curl -sSL --max-time 900 -o hydro_sites.json \
  "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/sites?size=10000&format=json&fields=code_site,libelle_site,surface_bv,code_commune_site,libelle_cours_eau,longitude_site,latitude_site,statut_site"

# --- Départements (noms) : API Découpage administratif ---
[ -s geoapi_departements.json ] || curl -sSL --max-time 300 -o geoapi_departements.json \
  "https://geo.api.gouv.fr/departements?fields=code,nom,codeRegion&format=json"

# --- PIB régional (INSEE, comptes régionaux base 2020) : requis par 03_indicators.py ---
[ -s insee_pib_reg.xlsx ] || curl -sSL --max-time 600 -o insee_pib_reg.xlsx \
  "https://www.insee.fr/fr/statistiques/fichier/8391986/PIB_REG_fr.xlsx"

# --- HydroBASINS Europe (HydroSHEDS, WWF, CC-BY 4.0) : requis par 07_transfrontalier.py ---
# 361 Mo ; seul le niveau 6 est utilisé, mais l'archive amont est monolithique.
[ -s hybas_eu.zip ] || curl -sSL --max-time 3600 -o hybas_eu.zip \
  "https://data.hydrosheds.org/file/hydrobasins/standard/hybas_eu_lev01-12_v1c.zip"
[ -f hybas_eu/hybas_eu_lev06_v1c.shp ] || unzip -o -q hybas_eu.zip -d hybas_eu

# --- Base GASPAR (Géorisques) : requise par 08_risques.py ---
[ -s gaspar.zip ] || curl -sSL --max-time 900 -o gaspar.zip \
  "http://files.georisques.fr/GASPAR/gaspar.zip"
ls gaspar/catnat_*.csv >/dev/null 2>&1 || unzip -o -q gaspar.zip -d gaspar

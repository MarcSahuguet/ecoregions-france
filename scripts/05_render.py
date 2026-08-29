#!/usr/bin/env python3
"""Injecte les données dans le gabarit et produit site/index.html (fichier autonome)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from recits import RECITS
from couts import (OPINION, CONDITIONS, REPERES,
                   ESTIMATION, ESTIMATION_TOTAL, RATIONALISATIONS)

geo = json.load(open("data/out/geometry.json"))
saison = json.load(open("data/out/saisonnalite.json"))
transf = json.load(open("data/out/transfrontalier.json"))
risques = json.load(open("data/out/risques.json"))
ind = json.load(open("data/out/indicators.json"))
keys = {e["key"] for e in ind["ecoregions"]}
assert keys == set(RECITS), f"récits manquants : {keys ^ set(RECITS)}"

data = {"geometry": geo, "indicators": ind, "recits": RECITS,
        "saison": saison, "transfrontalier": transf, "risques": risques,
        "couts": {"opinion": OPINION,
                  "conditions": CONDITIONS, "reperes": REPERES,
                  "estimation": ESTIMATION, "estimationTotal": ESTIMATION_TOTAL,
                  "rationalisations": RATIONALISATIONS}}
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

tpl = open("site/template.html").read()
assert "/*__DATA__*/" in tpl
html = tpl.replace("/*__DATA__*/", blob)
open("site/index.html", "w").write(html)
print(f"site/index.html : {os.path.getsize('site/index.html')/1024/1024:.2f} Mo")

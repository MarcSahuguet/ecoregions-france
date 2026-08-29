#!/usr/bin/env python3
"""Cartes haute définition pour les réseaux sociaux.

Produit un HTML autonome par format, puis le rastérise via Chrome headless.
Sortie : export/carte-ecoregions-<format>.png
"""
import json, os, subprocess, sys

OUT = "export"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
REPO = "github.com/MarcSahuguet/ecoregions-france"

TINT = {"escaut":"#5b8ea6","rhinmeuse":"#7ba57e","idf":"#c0797f","seineamont":"#b9a86a",
        "normandie":"#7fa8bd","bretagne":"#8f8fbb","loireaval":"#9dba79","loireamont":"#cfa96b",
        "garonne":"#d19a70","dordogne":"#a98a7d","saone":"#74b0a4","rhone":"#a882b5",
        "mediterranee":"#d0b167"}
COURT = {"escaut":"Flandre-Artois-Picardie","rhinmeuse":"Vosges-Ardenne","idf":"Île-de-France",
         "seineamont":"Champagne-Brie","normandie":"Normandie","bretagne":"Bretagne",
         "loireaval":"Anjou-Vendée","loireamont":"Val de Loire-Auvergne",
         "garonne":"Gascogne-Pyrénées","dordogne":"Périgord-Saintonge","saone":"Bourgogne-Comté",
         "rhone":"Rhône-Alpes","mediterranee":"Provence-Languedoc-Corse"}
# décalages de libellé, en unités de la carte (1 = 1 km)
NUDGE = {"idf":(-6,-14),"seineamont":(42,26),"normandie":(-24,6),"loireaval":(-30,30),
         "garonne":(-20,20),"dordogne":(-10,-10),"mediterranee":(-60,10),"rhone":(6,10),
         "saone":(0,10)}

FORMATS = {                     # nom : (largeur, hauteur, échelle de la carte, taille libellé)
    "carre":    (1200, 1200, 0.80, 15),
    "paysage":  (1600,  900, 0.92, 14),
    "portrait": (1080, 1350, 0.84, 15),
}

def fr(n, d=0):
    return f"{n:,.{d}f}".replace(",", " ").replace(".", ",")

def html(fmt, w, h, ech, taille):
    geo = json.load(open("data/out/geometry.json"))
    ind = json.load(open("data/out/indicators.json"))
    byk = {e["key"]: e for e in ind["ecoregions"]}
    vb = geo["viewBox"]
    paths = "".join(
        f'<path d="{g["path"]}" fill="{TINT[g["key"]]}" fill-opacity=".82" '
        f'stroke="#f2f4f0" stroke-width="1.4" fill-rule="evenodd"/>'
        for g in geo["ecoregions"])
    rivieres = "".join(f'<path d="{r["path"]}" fill="none" stroke="#1c6580" '
                       f'stroke-width=".7" stroke-opacity=".35"/>' for r in geo["rivers"])
    labels = ""
    for g in geo["ecoregions"]:
        e, o = byk[g["key"]], NUDGE.get(g["key"], (0, 0))
        x = 100 * (g["label"][0] + o[0] + 12) / (vb[2] + 24)
        y = 100 * (g["label"][1] + o[1] + 12) / (vb[3] + 24)
        labels += (f'<div class="lbl" style="left:{x:.2f}%;top:{y:.2f}%">'
                   f'<b>{COURT[g["key"]]}</b><span>{fr(e["pop"]/1e6,1)} M hab.</span></div>')
    vertical = fmt != "paysage"
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;background:#e9ece8;color:#12222a;
  font-family:"Source Sans 3",sans-serif;overflow:hidden;
  display:flex;flex-direction:{'column' if vertical else 'row'}}}
.txt{{padding:{'54px 60px 0' if vertical else '58px 0 58px 62px'};
  {'flex:0 0 auto' if vertical else 'flex:0 0 40%;display:flex;flex-direction:column;justify-content:center'}}}
.eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:15px;letter-spacing:.19em;
  text-transform:uppercase;color:#75878d;margin-bottom:14px}}
h1{{font-family:"Fraunces",serif;font-weight:700;font-size:{58 if vertical else 52}px;
  line-height:.99;letter-spacing:-.02em;max-width:{'none' if vertical else '11ch'}}}
h1 em{{font-style:normal;color:#1c6580}}
p.sub{{font-size:{22 if vertical else 20}px;line-height:1.42;color:#4c6068;margin-top:16px;
  max-width:{'62ch' if vertical else '30ch'}}}
.stage{{position:relative;flex:1;display:flex;align-items:center;justify-content:center;
  padding:0 40px {'96px' if vertical else '70px'}}}
svg{{width:100%;height:auto;display:block;overflow:visible}}
.map{{position:relative;width:{ech*100:.0f}%}}
.lbl{{position:absolute;transform:translate(-50%,-50%);text-align:center;line-height:1.12;
  text-shadow:0 0 4px #eef0ec,0 0 4px #eef0ec,0 0 9px #eef0ec}}
.lbl b{{display:block;font-size:{taille}px;font-weight:700}}
.lbl span{{display:block;font-family:"IBM Plex Mono",monospace;font-size:{taille-3}px;
  color:#3d5157;margin-top:1px}}
.pied{{position:absolute;left:{60 if vertical else 62}px;right:{60 if vertical else 40}px;
  bottom:{40 if vertical else 44}px;display:flex;justify-content:space-between;
  align-items:flex-end;gap:28px;font-size:15px;color:#4c6068;line-height:1.35}}
.pied b{{color:#12222a}}
.repo{{font-family:"IBM Plex Mono",monospace;font-size:15px;color:#1c6580;white-space:nowrap}}
</style></head><body>
<div class="txt">
  <p class="eyebrow">Découpage hydrographique · France métropolitaine</p>
  <h1>La France que<br>dessine <em>l'eau</em></h1>
  <p class="sub">Treize écorégions calées sur les bassins versants, construites à partir des
    34 sous-bassins officiels. Aucune commune coupée en deux.</p>
</div>
<div class="stage"><div class="map">
  <svg viewBox="-12 -12 {vb[2]+24} {vb[3]+24}">{paths}{rivieres}</svg>{labels}
</div></div>
<div class="pied">
  <span>Sources ouvertes : Sandre / OFB, IGN, INSEE, Hub'Eau, Corine Land Cover, Géorisques.<br>
    <b>Données, méthode et code ouverts — contributions bienvenues.</b></span>
  <span class="repo">{REPO}</span>
</div>
</body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for fmt, (w, h, ech, taille) in FORMATS.items():
        src = f"{OUT}/_{fmt}.html"
        open(src, "w", encoding="utf-8").write(html(fmt, w, h, ech, taille))
        png = f"{OUT}/carte-ecoregions-{fmt}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", f"--window-size={w},{h}",
                        "--virtual-time-budget=12000", f"--screenshot={png}",
                        f"file://{os.path.abspath(src)}"],
                       check=True, capture_output=True)
        print(f"{png}  {w}×{h} @2x  {os.path.getsize(png)/1024:.0f} ko")

if __name__ == "__main__":
    main()

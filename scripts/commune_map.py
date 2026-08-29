"""Table commune -> sous-bassin(s) DCE, avec correction du code mal formé côté source."""
import json, collections
def load(path="data/raw/SousBassinDCE_Communes.geojson"):
    feats = json.load(open(path))["features"]
    key = [k for k in feats[0]["properties"] if k.strip() == "CdEuSsBassinDCEAdmin"][0]
    fix = {"FRDCOCA": "FRD_COCA"}          # anomalie du référentiel Sandre
    m = collections.defaultdict(list)
    for f in feats:
        p = f["properties"]
        sb = fix.get(p[key], p[key])
        if sb.startswith(("FRI", "FRJ", "FRK", "FRL", "FRM")):   # DOM : hors périmètre
            continue
        m[p["CdCommune"]].append(sb)
    return m

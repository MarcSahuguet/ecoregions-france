# Agrégation des 34 sous-bassins DCE administratifs (Sandre/OFB) en 13 écorégions.
# Contraintes explicites : contiguïté hydrographique (amont/aval d'un même réseau),
# respect des limites de circonscription de bassin (loi sur l'eau de 1964),
# et recherche d'un équilibre démographique — la Seine aval fait exception (voir carte).
ECOREGIONS = [
 ("escaut",   "Flandre-Artois-Picardie",                 ["FRA_ESCA"]),
 ("rhinmeuse",   "Vosges-Ardenne",           ["FRC_RHIN","FRC_MOSE","FRB1_MEUS","FRB2_SAMB"]),
 ("idf",   "Île-de-France", ["FRH_IF"]),
 ("seineamont",   "Champagne-Brie",      ["FRH_SEAM","FRH_MARN","FRH_OISE"]),
 ("normandie",   "Normandie",         ["FRH_SEAV","FRH_CONO"]),
 ("bretagne",   "Bretagne",             ["FRG_VICO"]),
 ("loireaval",   "Anjou-Vendée",             ["FRG_LACV","FRG_MSL"]),
 ("loireamont",   "Val de Loire-Auvergne",  ["FRG_LMOY","FRG_VICR","FRG_ALA"]),
 ("garonne",   "Gascogne-Pyrénées",       ["FRF_GARO","FRF_TARN","FRF_LOT","FRF_ADOU"]),
 ("dordogne",   "Périgord-Saintonge", ["FRF_DORD","FRF_CHAR","FRF_COAC"]),
 ("saone",   "Bourgogne-Comté",                  ["FRD_SAON","FRD_DOUB"]),
 ("rhone",   "Rhône-Alpes",            ["FRD_HRHO","FRD_ISER","FRD_RHON"]),
 ("mediterranee",   "Provence-Languedoc-Corse",        ["FRD_DURA","FRD_COCA","FRD_GARD","FRD_COLR","FRE_CORS"]),
]
SB2ECO = {sb: key for key, _, sbs in ECOREGIONS for sb in sbs}

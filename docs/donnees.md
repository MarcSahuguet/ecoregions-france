# Provenance des données

Chaque chiffre publié est calculé par un script de ce dépôt à partir d'une source ouverte.
Aucune valeur n'est saisie à la main, à deux exceptions près, signalées ci-dessous.

## Sources et licences

| Donnée | Source | Millésime | Licence | Script |
|---|---|---|---|---|
| Sous-bassins DCE administratifs (34) | Sandre / OFB, service WFS | 2026 | Licence Ouverte 2.0 | `01_fetch.sh` |
| Table commune → sous-bassin | Sandre / OFB | 2026 | Licence Ouverte 2.0 | `commune_map.py` |
| Régions hydrographiques (24) | Sandre / OFB | 2026 | Licence Ouverte 2.0 | `02_build_geometry.py` |
| Bassins hydrographiques | BD TOPAGE®, IGN & OFB | 2025 | Licence Ouverte 2.0 | `01_fetch.sh` |
| Cours d'eau de classe 1 | Sandre | 2026 | Licence Ouverte 2.0 | `02_build_geometry.py` |
| Population, surface, centroïde par commune | INSEE via API Découpage administratif (Etalab) | en vigueur | Licence Ouverte 2.0 | `03_indicators.py` |
| Occupation du sol, 5 postes par commune | Corine Land Cover 2018, SDES / Copernicus | 2018 | Licence Ouverte 2.0 | `03_indicators.py` |
| Prélèvements d'eau par ouvrage | BNPE via Hub'Eau | moyenne 2020-2022 | Licence Ouverte 2.0 | `03_indicators.py` |
| Débits journaliers | Hub'Eau hydrométrie | 2015-2024 | Licence Ouverte 2.0 | `04_debits.py`, `06_saisonnalite.py` |
| PIB par habitant régional | INSEE, comptes régionaux base 2020 | 2024 | Licence Ouverte 2.0 | `03_indicators.py` |
| Bassins versants mondiaux | HydroBASINS niveau 6, HydroSHEDS / WWF | v1c | **CC-BY 4.0** | `07_transfrontalier.py` |
| Arrêtés CatNat, PPRN | Base GASPAR, Géorisques | août 2026 | Licence Ouverte 2.0 | `08_risques.py` |

## Les deux valeurs qui ne sont pas calculées

1. **Le PIB par écorégion** est une *estimation* : le PIB par habitant régional de l'INSEE est
   réparti au prorata de la population communale. Une écorégion à cheval sur deux régions hérite
   donc d'une moyenne pondérée, pas d'une mesure. Signalé comme estimation sur la carte.
2. **Les chiffres de coût et d'opinion** (`scripts/couts.py`) sont *cités*, pas calculés : chaque
   ligne porte sa source et son lien. Ils vivent dans un fichier séparé pour cette raison.

## Ce qui est un choix, pas une donnée

- **Le regroupement des 34 sous-bassins en 13 écorégions** (`scripts/groups.py`) applique trois
  contraintes — continuité hydrographique, respect des circonscriptions de bassin de 1964,
  équilibre démographique — mais l'arbitrage final est discutable. Le nombre 13 vient du débat
  public, pas de l'hydrographie.
- **Les noms d'écorégions** sont des propositions, fondées sur des provinces et des massifs
  existants plutôt que sur des hydronymes. Voir la section « Objections » de la carte.

## Limites connues

- Périmètre : France métropolitaine. Les cinq bassins ultramarins formeraient cinq écorégions
  supplémentaires ; ils ne sont pas traités.
- Le découpage utilise la version *administrative* des sous-bassins : les limites suivent les
  frontières communales, pas la crête topographique. Aucune commune n'est coupée, au prix d'un
  écart faible mais réel avec la ligne de partage des eaux.
- Les débits proviennent d'une station par écorégion : ils mesurent ce que draine cette station,
  pas toute l'eau du territoire.
- Les contours HydroBASINS sont modélisés à l'échelle mondiale et diffèrent des référentiels
  nationaux — l'écart peut dépasser 10 % sur un grand bassin comme le Rhin.

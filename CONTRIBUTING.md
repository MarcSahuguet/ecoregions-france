# Contribuer

Ce dépôt existe pour être contesté. Si un chiffre vous paraît faux, il est traçable :
chaque indicateur est produit par un script, à partir d'une source ouverte listée dans
[docs/donnees.md](docs/donnees.md).

## Contester un chiffre

Ouvrez une issue en indiquant :
1. **le chiffre** tel qu'il apparaît (écorégion, indicateur, valeur) ;
2. **ce que vous obtenez** et par quelle méthode ;
3. **la source** sur laquelle vous vous appuyez.

Les désaccords les plus utiles portent sur la méthode, pas sur la valeur : une moyenne pondérée
mal choisie, un usage compté deux fois, une station non représentative.

## Discuter le découpage

Le regroupement des 34 sous-bassins en 13 écorégions est un choix, pas un résultat. Il tient en
vingt lignes dans [`scripts/groups.py`](scripts/groups.py) : modifier ce fichier et relancer le
pipeline suffit à produire une carte alternative complète, chiffres compris. Les propositions de
découpage argumentées sont bienvenues — idéalement sous forme de pull request accompagnée des
chiffres qu'elle produit.

## Contributions particulièrement recherchées

- **Hydrologie** : représentativité des stations retenues, régimes, soutien d'étiage.
- **Statistique publique** : meilleure ventilation du PIB que le prorata démographique.
- **Cartographie** : généralisation des tracés, projection, lisibilité.
- **Outre-mer** : étendre le périmètre aux cinq bassins ultramarins.
- **Comparaison internationale** : appliquer la méthode à l'Espagne, l'Allemagne, les Pays-Bas.

## Relancer le pipeline

Voir la section « Reproduire » du [README](README.md). Comptez environ 600 Mo de téléchargement
et une vingtaine de minutes, dont l'essentiel sur les API Hub'Eau.

## Ce que ce dépôt n'est pas

Une proposition politique. C'est un instrument de mesure : il sert autant à défendre le découpage
par bassins versants qu'à en montrer les limites — la section « Objections » de la carte est
alimentée par les mêmes données que le reste.

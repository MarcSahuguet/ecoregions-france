# -*- coding: utf-8 -*-
"""Récits par écorégion. Chaque chiffre cité provient de data/out/indicators.json."""

RECITS = {
 "escaut": dict(
   sous_titre="La France des canaux et des nappes",
   texte="Le plus petit territoire de la carte, et l'un des plus denses : 4,6 millions "
         "d'habitants sur 18 800 km², à 244 habitants au km². Les rivières y sont courtes et "
         "lentes — la Somme n'évacue que 42 m³/s — et la ressource vient surtout des nappes de la "
         "craie. Quatre cinquièmes du sol sont cultivés, un huitième est bâti : c'est le taux "
         "d'artificialisation le plus élevé après l'Île-de-France. Particularité unique en France, "
         "les canaux prélèvent ici plus d'eau que l'industrie. Toute sa population vit en "
         "Hauts-de-France — avec l'Île-de-France, le seul cas où une écorégion tient dans une "
         "seule région actuelle. L'inverse est faux : il y manque un quart des Hauts-de-France, "
         "l'Oise et l'essentiel de l'Aisne s'écoulant vers la Seine.",
   tension="Nappes sous pression, rivières à faible débit, sols très artificialisés.",
   presse=[
     dict(titre="Sécheresse : de nouvelles restrictions d'eau renforcées dans les Hauts-de-France",
          source='France 3 Hauts-de-France', date='juillet 2026',
          url='https://france3-regions.franceinfo.fr/hauts-de-france/secheresse-de-nouvelles-restrictions-d-eau-renforcees-dans-les-hauts-de-france-3391894.html'),
     dict(titre="Nappes d'eau souterraine au 15 août 2026 : les nappes de la craie se vidangent",
          source='BRGM', date='15 août 2026',
          url='https://www.brgm.fr/fr/actualite/actualite/nappes-eau-souterraine-au-15-aout-2026'),
   ]),
 "rhinmeuse": dict(
   sous_titre="Un fleuve international, une forêt et des frontières",
   texte="Trois bassins transfrontaliers réunis : le Rhin, la Moselle-Sarre et la Meuse-Sambre. "
         "Le Rhin apporte à lui seul 1 155 m³/s à Lauterbourg, le débit spécifique le plus élevé "
         "de la carte hors montagne (23 l/s/km²). L'eau est abondante, mais très sollicitée par "
         "l'industrie (449 Mm³) et les canaux (686 Mm³), et la nappe d'Alsace — la plus grande "
         "réserve d'eau douce d'Europe de l'Ouest — reste marquée par les pollutions héritées. "
         "Plus d'un tiers du territoire est boisé. Toute décision prise ici engage les Pays-Bas, "
         "l'Allemagne, le Luxembourg et la Belgique : la coopération internationale y est la règle, "
         "pas l'exception.",
   tension="Qualité de la nappe d'Alsace, usages industriels, gouvernance partagée à cinq pays.",
   presse=[
     dict(titre="« Une pollution généralisée » : la plus grande nappe phréatique d'Europe regorge d'un cocktail de micropolluants",
          source='Vert', date='mai 2026',
          url='https://vert.eco/sante-environnement/pollutions/une-pollution-generalisee-la-plus-grande-nappe-phreatique-deurope-regorge-dun-cocktail-de-micropolluants-chimiques/'),
     dict(titre='PFAS et pesticides : 96 % de la nappe phréatique intoxiquée',
          source='Rue89 Strasbourg', date='',
          url='https://www.rue89strasbourg.com/pfas-pesticides-96-nappe-phreatique-intoxiquee-387501'),
     dict(titre="« 96 % des points de mesure présentent des micropolluants » : l'ampleur inédite de la pollution du Rhin",
          source='ICI Grand Est', date='',
          url='https://www.ici.fr/grand-est/96-des-points-de-mesure-presentent-des-micropolluants-une-etude-demontre-l-ampleur-inedite-de-la-pollution-du-rhin-5067065'),
   ]),
 "idf": dict(
   sous_titre="12,4 millions de personnes sur 371 m³/s",
   texte="L'écorégion la plus peuplée et la plus riche — 18,7 % de la population, 856 milliards "
         "d'euros de PIB — tient sur 2,4 % du territoire national. Elle boit 787 Mm³ par an, le "
         "premier prélèvement d'eau potable de France, dans une Seine qui ne roule à Paris que "
         "371 m³/s en moyenne. Un habitant sur cinq du pays dépend donc d'un fleuve modeste, "
         "dont la qualité se décide en amont, sur les terres agricoles de la Champagne et de la "
         "Bourgogne. C'est l'illustration la plus nette de l'asymétrie amont-aval : ici, on "
         "consomme une eau que l'on ne produit pas.",
   tension="Dépendance à l'amont, étiages, un habitant sur cinq du pays sur un fleuve de 371 m³/s.",
   presse=[
     dict(titre="Baignade dans la Seine : fréquentation, qualité de l'eau… quel bilan pour la nouvelle attraction parisienne ?",
          source='franceinfo', date='',
          url='https://www.franceinfo.fr/france/ile-de-france/baignade-dans-la-seine-frequentation-qualite-de-l-eau-quel-bilan-pour-la-nouvelle-attraction-parisienne_7447078.html'),
     dict(titre="Résidus de pesticides dans l'eau potable : la décontamination pourrait coûter jusqu'à 5,7 milliards d'euros par an",
          source='CNews', date='juillet 2026',
          url='https://www.cnews.fr/france/2026-07-31/residus-de-pesticides-dans-leau-potable-une-decontamination-pourrait-couter'),
   ]),
 "seineamont": dict(
   sous_titre="Le château d'eau de Paris",
   texte="Le territoire qui alimente la capitale : Seine amont, Marne et Oise, 49 300 km² pour "
         "seulement 2,9 millions d'habitants — 59 au km², la densité la plus faible du nord de la "
         "France. Deux tiers du sol sont agricoles, et ce sont ces terres qui déterminent la qualité "
         "de l'eau bue en aval. On y trouve les grands lacs-réservoirs qui écrêtent les crues de "
         "Paris et soutiennent ses étiages, ainsi que les 1 461 Mm³ prélevés pour les canaux : le "
         "premier poste d'un territoire qui gère l'eau autant pour les autres que pour lui-même.",
   tension="Nitrates et pesticides agricoles, service rendu à l'aval largement non rémunéré.",
   presse=[
     dict(titre="Trop de nitrates dans l'eau potable : des mesures de restriction pour les plus fragiles",
          source='France 3 Grand Est', date='',
          url='https://france3-regions.franceinfo.fr/grand-est/marne/chalons-en-champagne/trop-de-nitrates-dans-l-eau-potable-des-mesures-de-restriction-mises-en-place-pour-les-plus-fragiles-2958263.html'),
     dict(titre="En 45 ans, 6 090 captages d'eau potable ont été fermés à cause des pesticides",
          source='La Relève et La Peste', date='',
          url='https://lareleveetlapeste.fr/en-45-ans-6-090-captages-deau-potable-ont-ete-fermes-a-cause-des-pesticides/'),
   ]),
 "normandie": dict(
   sous_titre="L'estuaire, l'élevage et la mer",
   texte="De la baie du Mont-Saint-Michel à la Bresle : l'estuaire de la Seine et les fleuves "
         "côtiers normands. Quatre cinquièmes du territoire sont agricoles, largement en herbe et "
         "en élevage, et les rivières y sont courtes — l'Eure, le plus grand cours d'eau jaugé de "
         "l'écorégion, ne fait que 22 m³/s. Le prélèvement total, 574 Mm³, est le deuxième plus "
         "faible de la carte : l'eau est là, ce qui compte ici c'est sa qualité, celle des nappes de "
         "la craie et celle des eaux littorales qui reçoivent tout ce que la Seine a transporté "
         "depuis Paris.",
   tension="Qualité des eaux littorales, algues vertes, érosion et submersion du trait de côte.",
   presse=[
     dict(titre='Le recul inexorable du trait de côte inquiète les habitants du littoral',
          source='France 3 Normandie', date='',
          url='https://france3-regions.franceinfo.fr/normandie/le-recul-inexorable-du-trait-de-cote-inquiete-les-habitants-du-littoral-2542312.html'),
     dict(titre='Érosion côtière : le trait de côte recule en 2026',
          source='Actualités News Environnement', date='2026',
          url='https://www.actualites-news-environnement.com/erosion-cotiere-france-2026/'),
   ]),
 "bretagne": dict(
   sous_titre="Le socle, l'eau de pluie et l'élevage",
   texte="La seule écorégion qui coïncide avec une identité historique déjà constituée — et la "
         "seule dont le sous-bassin, « Vilaine et côtiers bretons », est presque un synonyme de "
         "région. Sur un socle granitique sans grandes nappes, tout se joue en surface : l'eau "
         "vient de la pluie et repart vite. C'est le plus faible prélèvement de France, 282 Mm³, "
         "79 m³ par habitant, huit fois moins que la moyenne. Quatre cinquièmes du sol sont "
         "agricoles, avec la plus forte densité d'élevage du pays : l'enjeu n'est pas la quantité "
         "d'eau mais l'azote qu'elle emporte vers la mer.",
   tension="Nitrates, algues vertes, absence de réserve souterraine en cas de sécheresse longue.",
   presse=[
     dict(titre="Algues vertes en Bretagne : l'État épinglé par la Cour des comptes",
          source='Agronews', date='juin 2026',
          url='https://agronews.com/fr/fr/news/breaking-news/2026-06-16/96130'),
     dict(titre='Algues vertes et nitrates : la phase réglementaire se durcit',
          source='Paysan Breton', date='juin 2026',
          url='https://www.paysan-breton.fr/2026/06/poursuivre-la-reduction-des-nitrates/'),
   ]),
 "loireaval": dict(
   sous_titre="Le dernier fleuve sauvage, et son estuaire",
   texte="La Loire arrive ici avec 779 m³/s à Saint-Nazaire, après avoir traversé la moitié du "
         "pays. Sur 45 700 km², 83 % du sol est agricole — le taux le plus élevé de la carte — et "
         "l'irrigation représente 23 % des prélèvements, contre 9 % à l'échelle nationale. "
         "S'y ajoute la centrale de Chinon-Avoine et ses 725 Mm³ de refroidissement. Le territoire "
         "réunit Nantes, Angers, Le Mans, La Rochelle et Niort, aujourd'hui répartis entre quatre "
         "régions administratives : c'est la partie de la carte où le découpage par bassin "
         "recompose le plus visiblement les solidarités existantes.",
   tension="Conflits d'usage estivaux entre irrigation, refroidissement et milieux.",
   presse=[
     dict(titre="Mégabassines : pourquoi la justice n'écoute pas la science",
          source='Reporterre', date='',
          url='https://reporterre.net/Megabassines-pourquoi-la-justice-n-ecoute-pas-la-science'),
     dict(titre='Sécheresse en Loire-Atlantique : deux bassins en crise, le préfet durcit les restrictions',
          source='info.fr', date='juillet 2026',
          url='https://info.fr/secheresse-loire-atlantique-prefet-durcit-restrictions-eau-deux-bassins-crise/'),
   ]),
 "loireamont": dict(
   sous_titre="Le plus vaste, le plus fragmenté",
   texte="81 200 km² — 15 % du territoire national — pour 5 millions d'habitants et 23 "
         "départements répartis sur quatre régions actuelles. C'est le cœur hydrologique du pays : "
         "l'Allier, la Loire moyenne, la Vienne et la Creuse, les têtes de bassin du Massif "
         "central, et la nappe de Beauce partagée avec la Seine. Deux centrales nucléaires y "
         "prélèvent 693 Mm³, l'irrigation 252 Mm³, et pourtant la densité n'est que de 62 "
         "habitants au km². Saint-Étienne, Clermont-Ferrand, Tours, Limoges, Orléans et Poitiers "
         "n'ont aujourd'hui aucune institution commune : cette écorégion est la seule à leur en "
         "donner une.",
   tension="Étiages sévères de la Loire, têtes de bassin vulnérables, gouvernance très éclatée.",
   presse=[
     dict(titre='« Débit de crise », biodiversité menacée : la sécheresse historique qui touche la Loire',
          source='ICI Centre-Val de Loire', date='2026',
          url='https://www.ici.fr/centre-val-de-loire/debit-de-crise-biodiversite-menacee-ce-que-l-on-sait-de-la-secheresse-historique-qui-touche-la-loire-8836185'),
     dict(titre='Le niveau de la Loire est bas cet été, mais les centrales nucléaires ne sont pas en danger selon EDF',
          source='France 3 Centre-Val de Loire', date='2026',
          url='https://france3-regions.franceinfo.fr/centre-val-de-loire/secheresse-le-niveau-de-la-loire-est-bas-cet-ete-mais-les-centrales-nucleaires-ne-sont-pas-en-danger-selon-edf-3396646.html'),
   ]),
 "garonne": dict(
   sous_titre="La France où l'eau sert d'abord à irriguer",
   texte="42 % des prélèvements y vont à l'irrigation — le taux le plus élevé de France, contre 9 % "
         "en moyenne — pour 609 Mm³ par an. La Garonne, alimentée par les Pyrénées, ne roule que "
         "500 m³/s à La Réole, avec des étiages estivaux qui s'aggravent à mesure que le stock "
         "nival diminue. Le territoire réunit Toulouse et Bordeaux, deux métropoles aujourd'hui "
         "dans deux régions différentes mais sur le même fleuve, ainsi que Golfech et ses 177 Mm³ "
         "de refroidissement. La ressource est la plus tendue du pays en été : c'est ici que le "
         "partage de l'eau est déjà, concrètement, un sujet politique.",
   tension="Étiages estivaux critiques, perte du stock nival pyrénéen, arbitrage irrigation/milieux.",
   presse=[
     dict(titre="La Garonne dans un état critique, de nouvelles restrictions d'eau envisagées",
          source='La France Agricole', date='2026',
          url='https://www.lafranceagricole.fr/irrigation/article/901820/la-garonne-dans-un-etat-critique-de-nouvelles-restrictions-d-eau-envisagees'),
     dict(titre="Soutien d'étiage de la Garonne : le démarrage le plus précoce depuis 1993",
          source='France Nature Environnement Occitanie', date='août 2026',
          url='https://www.fne-op.fr/2026/08/03/soutien-etiage-garonne/'),
   ]),
 "dordogne": dict(
   sous_titre="Peu d'habitants, beaucoup d'eau prélevée",
   texte="Un paradoxe : 2,5 millions d'habitants — la plus faible population de la carte — et "
         "15,4 % des prélèvements nationaux. L'explication tient à un seul site, la centrale du "
         "Blayais, qui prélève 4 773 Mm³ dans l'estuaire de la Gironde pour son refroidissement, "
         "presque intégralement restitués. Retirez-la, et il ne reste que 581 Mm³, dont la moitié "
         "pour l'irrigation. Le territoire est le plus boisé de la façade atlantique (41 %), "
         "compte 1,8 % de surfaces en eau, et n'abrite aucune ville de plus de 60 000 habitants : "
         "une écorégion rurale qui rend à la France un service énergétique majeur.",
   tension="Dépendance à l'estuaire, salinisation, irrigation du maïs et étiages de la Charente.",
   presse=[
     dict(titre="Canicule : EDF met à l'arrêt trois réacteurs nucléaires et bride huit autres",
          source="L'EnerGeek", date='juillet 2026',
          url='https://lenergeek.com/2026/07/13/reacteurs-nucleaires-canicule-edf-met-arret-3/'),
     dict(titre='Adaptation de la production de la centrale du Blayais en raison des conditions climatiques',
          source='EDF, communiqué', date='juillet 2026',
          url='https://www.edf.fr/la-centrale-nucleaire-du-blayais/les-actualites-de-la-centrale-nucleaire-du-blayais/adaptation-de-la-production-de-la-centrale-du-blayais-en-raison-des-conditions-climatiques'),
   ]),
 "saone": dict(
   sous_titre="Le couloir, ses canaux et ses forêts",
   texte="La Saône et le Doubs, 26 900 km² et 2,2 millions d'habitants : la plus petite population "
         "de la carte après avoir été, historiquement, l'un des grands couloirs de circulation "
         "d'Europe. L'eau est abondante — 360 m³/s à Mâcon, 13,8 l/s/km² — et c'est le seul "
         "territoire où les canaux (542 Mm³) prélèvent trois fois plus que l'agriculture et "
         "l'industrie réunies. Plus d'un tiers du sol est boisé, le karst jurassien y est "
         "particulièrement vulnérable aux pollutions, et l'écorégion joue un rôle décisif pour "
         "l'aval : c'est la Saône qui soutient le Rhône en été.",
   tension="Karst vulnérable, soutien d'étiage du Rhône, réchauffement des eaux.",
   presse=[
     dict(titre="Sécheresse : « c'est lunaire », à la frontière suisse, le Doubs a disparu",
          source='Le Matin', date='2026',
          url='https://www.lematin.ch/story/secheresse-c-est-lunaire-a-la-frontiere-suisse-le-doubs-a-disparu-103600527'),
     dict(titre='Au milieu de la Loue coule… la pollution : la rivière de Courbet victime de nouveaux rejets',
          source='France 3 Bourgogne-Franche-Comté', date='',
          url='https://france3-regions.franceinfo.fr/bourgogne-franche-comte/doubs/au-milieu-de-la-loue-coule-la-pollution-dans-le-doubs-la-riviere-de-gustave-courbet-victime-de-nouveaux-rejets-inquietants-2537964.html'),
   ]),
 "rhone": dict(
   sous_titre="34,7 % des prélèvements français",
   texte="Un tiers de l'eau prélevée en France l'est ici, sur 6 % du territoire : 12 015 Mm³, dont "
         "10 758 pour refroidir les centrales de Bugey, Saint-Alban, Cruas et Tricastin — une eau "
         "en grande partie restituée, mais réchauffée. S'y ajoute le premier parc hydroélectrique "
         "du pays. Le Rhône, alimenté par les glaciers et les neiges alpines, roule 1 261 m³/s à "
         "Valence ; c'est aussi le fleuve dont le régime changera le plus avec le retrait glaciaire. "
         "57 % du territoire est forestier ou semi-naturel, et le PIB par habitant y est le "
         "deuxième de France après l'Île-de-France.",
   tension="Retrait glaciaire, réchauffement du fleuve, concentration nucléaire et hydroélectrique.",
   presse=[
     dict(titre='Changement climatique : le Rhône menacé par la fonte des glaciers',
          source='franceinfo', date='',
          url='https://www.franceinfo.fr/environnement/crise-climatique/changement-climatique-le-rhone-menace-par-la-fonte-des-glaciers_7143951.html'),
     dict(titre="Canicules : dans les Alpes, la fonte des glaciers s'emballe",
          source='We Demain', date='2026',
          url='https://www.wedemain.fr/sauver-la-planete/risques-environnementaux/canicules-dans-les-alpes-la-fonte-des-glaciers-semballe-1155795'),
   ]),
 "mediterranee": dict(
   sous_titre="Le sud, l'aridité et la Corse",
   texte="8,8 millions d'habitants, deuxième écorégion la plus peuplée, sur les territoires les "
         "plus secs du pays : la Durance, le Gard, le Languedoc, la Côte d'Azur et la Corse. "
         "Les deux tiers du sol sont forestiers ou semi-naturels — d'où le premier risque incendie "
         "de France — et un quart des prélèvements vont à l'irrigation. Le système Durance-Verdon "
         "alimente Marseille, Aix et une partie de la Provence agricole par un réseau de canaux "
         "qui prélève 1 497 Mm³ : l'eau y est transportée, stockée et arbitrée depuis un siècle. "
         "La Corse, seul bassin insulaire, y est rattachée comme dans l'organisation actuelle.",
   tension="Déficit structurel, pointe touristique estivale, incendies, biseau salin littoral.",
   presse=[
     dict(titre="La sécheresse gagne du terrain dans les Pyrénées-Orientales : nouvelles restrictions d'eau",
          source='France 3 Occitanie', date='2026',
          url='https://france3-regions.franceinfo.fr/occitanie/pyrenees-orientales/perpignan/la-secheresse-gagne-du-terrain-dans-les-pyrenees-orientales-cette-prefecture-declenche-de-nouvelles-mesures-de-restrictions-de-l-eau-3387826.html'),
     dict(titre="Réchauffement climatique et sécheresses : la Provence s'adapte déjà au manque d'eau",
          source='Made in Marseille', date='',
          url='https://madeinmarseille.net/actualite/204071-rechauffement-climatique-et-secheresses-la-provence-sadapte-deja-au-manque-deau/'),
   ]),
}

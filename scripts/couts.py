# -*- coding: utf-8 -*-
"""Coûts et acceptabilité : chiffres repris de sources publiques, chacun avec sa référence.
Contrairement aux indicateurs de la carte, ces valeurs ne sont pas calculées ici — elles sont
citées. D'où la source attachée à chaque ligne."""

# --- ce qu'a coûté la fusion des régions de 2015 -------------------------------
# --- ce que dit l'opinion -----------------------------------------------------
OPINION = [
 dict(chiffre="95 %", texte="des Français estiment que l'organisation territoriale doit être réformée",
      source="CSA pour la délégation aux collectivités du Sénat, février-mars 2020, 1 007 personnes",
      url="https://territorial.zepros.fr/75-des-francais-souhaitent-renforcer-la-decentralisation--89024",
      sens="pour"),
 dict(chiffre="71 %", texte="souhaitent une France plus fédérale, aux régions renforcées",
      source="Ifop pour Régions et Peuples Solidaires, août 2025, 2 000 personnes",
      url="https://abp.bzh/vers-une-france-federale-le-sondage-ifop-qui-bouscule-le-central-72071",
      sens="pour"),
 dict(chiffre="64 %", texte="craignent de manquer d'eau dans leur région — 73 % en PACA, 71 % en Occitanie",
      source="Centre d'information sur l'eau, attentes des Français 2026",
      url="https://www.cieau.com/qualite-micropolluants-climat-ce-que-les-francais-attendent-desormais-de-leur-eau-du-robinet/",
      sens="pour"),
 dict(chiffre="68 %", texte="jugent le redécoupage de 2015 raté et en réclament un autre — mais fondé sur "
                            "les « réalités culturelles et historiques ». Jusqu'à 84 % en Alsace, 80 % en Corse, "
                            "72 % en Bretagne",
      source="Ifop pour Régions et Peuples Solidaires, août 2025",
      url="https://abp.bzh/vers-une-france-federale-le-sondage-ifop-qui-bouscule-le-central-72071",
      sens="contre"),
 dict(chiffre="45 %", texte="seulement citent la région comme échelon à renforcer : elle arrive dernière, "
                            "derrière la commune (60 %), le département (49 %) et l'intercommunalité (48 %)",
      source="CSA pour le Sénat, février-mars 2020",
      url="https://territorial.zepros.fr/75-des-francais-souhaitent-renforcer-la-decentralisation--89024",
      sens="contre"),
 dict(chiffre="26 %", texte="des particuliers acceptent de payer le traitement de la pollution de l'eau ; "
                            "68 % désignent les industriels, 37 % les agriculteurs. Or les ménages acquittent "
                            "déjà 88 % des redevances des agences de l'eau",
      source="Institut Terram ; Filière Eau pour la répartition des redevances",
      url="https://institut-terram.org/publications/municipales-lecologie-a-lepreuve-des-territoires/",
      sens="contre"),
]

# --- conditions d'acceptabilité ----------------------------------------------
CONDITIONS = [
 dict(titre="Ne pas promettre d'économies",
      texte="C'est l'erreur qui a tué la réforme de 2015 et qui sert depuis d'argument à tous ses "
            "opposants : 10 milliards d'euros annoncés, aucun réalisé. Annoncer un coût chiffré et "
            "plafonné, présenté comme un investissement, est plus solide qu'une promesse "
            "d'économies que la Cour des comptes viendra démentir quatre ans plus tard."),
 dict(titre="Financer par redéploiement",
      texte="65 % des Français acceptent des politiques environnementales financées par la "
            "réorientation de dépenses existantes : l'acceptabilité dépend moins du contenu que de "
            "la lisibilité et de la justice perçue du financement. Corollaire : sans rééquilibrage "
            "du 88/12 des redevances entre ménages et autres usagers, la réforme sera lue comme "
            "une facture de plus."),
 dict(titre="Ne pas opposer l'eau à l'identité",
      texte="C'est le seul terrain où le débat est perdu d'avance, et l'adhésion à un redécoupage "
            "culturel culmine là où un découpage par bassin ferait le plus de dégâts. La version "
            "qui satisfait les deux attentes n'est pas la substitution mais la superposition : une "
            "écorégion titulaire des compétences écologiques, absorbant l'agence de bassin, et les "
            "régions maintenues. Aucun département scindé, coût marginal."),
]

REPERES = [
 dict(valeur="39,7 Md€", texte="budget agrégé des régions en 2024 : le surcoût estimé plus bas "
                               "en représente 0,25 à 0,3 %"),
 dict(valeur="2 Md€/an", texte="programme 2025-2030 des agences de l'eau. La compétence n'est pas à "
                               "créer, elle est à transférer"),
 dict(valeur="88 %", texte="des redevances des agences de l'eau sont acquittées par les ménages"),
]

# --- estimation du coût, par transposition du précédent de 2015 ---------------
# Ce n'est pas un chiffrage officiel : c'est un modèle explicite, dont chaque ligne
# indique sa méthode. Les régions comptent environ 91 000 agents (4,6 % des 1,98 million
# d'agents de la fonction publique territoriale, DGCL) ; les sept régions fusionnées en
# 2015 représentaient environ 37,6 millions d'habitants.
ESTIMATION = [
 dict(poste="Harmonisation indemnitaire des agents", montant="90 à 100 M€/an", nature="pérenne",
      methode="53 M€/an constatés pour ~52 000 agents en 2015, soit ~1 000 €/agent/an, "
              "appliqués aux ~91 000 agents des régions. La transposition par habitant "
              "(1,4 €/hab/an × 66 M) donne 95 M€ : les deux méthodes convergent.",
      hypothese=False),
 dict(poste="Indemnités des élus", montant="5 à 7 M€/an", nature="pérenne",
      methode="3,8 M€/an pour sept régions en 2015, soit ~0,5 M€ par assemblée, "
              "étendu aux treize écorégions.",
      hypothese=False),
 dict(poste="Systèmes d'information", montant="90 à 110 M€", nature="non récurrent",
      methode="plus de 30 M€ pour quatre régions en 2015, soit ~7,5 M€ par région, "
              "appliqués aux treize écorégions.",
      hypothese=False),
 dict(poste="Scission des 32 départements partagés", montant="30 à 95 M€", nature="non récurrent",
      methode="aucun précédent : la réforme de 2015 n'a scindé aucun département. "
              "Hypothèse de 1 à 3 M€ par département pour les conventions, les transferts "
              "d'agents et la réconciliation des systèmes.",
      hypothese=True),
]
ESTIMATION_TOTAL = dict(
  perenne="95 à 110 M€/an",
  unique="120 à 205 M€",
  reperes="soit 0,25 à 0,3 % des budgets régionaux, et 1,50 à 1,70 € par habitant et par an")

RATIONALISATIONS = [
 dict(titre="Absorber les agences de bassin", montant="9 à 14 M€/an",
      texte="Les six agences de l'eau emploient 1 563 ETPT (plafond de la loi de finances 2024) "
            "et occupent six sièges. Le budget de l'État fixe déjà comme objectif la "
            "« mutualisation inter-agences des fonctions métiers et supports » : une écorégion "
            "qui absorbe son agence réalise cette mutualisation par construction. Gain estimé "
            "sur 10 à 15 % des fonctions support."),
 dict(titre="Un seul document de planification", montant="quelques M€ par cycle",
      texte="Aujourd'hui six SDAGE et treize SRADDET, élaborés séparément, avec deux "
            "concertations et deux évaluations environnementales. Des périmètres alignés "
            "permettent un document unique par écorégion — treize au lieu de dix-neuf."),
 dict(titre="Ne pas répéter l'erreur de 2015", montant="le plus gros gisement",
      texte="La Cour des comptes attribue l'essentiel du surcoût au maintien des effectifs dans "
            "les anciennes capitales régionales et à la juxtaposition des structures. Une règle "
            "posée d'emblée — un siège par écorégion, dans les locaux de l'agence de bassin "
            "existante — annule le poste le plus lourd du modèle ci-dessus."),
 dict(titre="Supprimer le coût de coordination", montant="non chiffrable",
      texte="Le bassin de la Loire est aujourd'hui géré par quatre régions et une agence, avec "
            "autant de conventions, de comités et de calendriers à accorder. Un périmètre unique "
            "supprime cette coordination plutôt que de l'organiser."),
]

# Compte rendu mensuel : gouvernement et Parlement (France)

Un rapport mensuel, visuel et lisible dès 14 ans, sur l'actualité du gouvernement, de l'Assemblée nationale et du Sénat :
décisions du mois, lois en discussion (qui les porte, à quelle étape du parcours), zoom sur un texte (le budget),
qui dépose le plus de propositions de loi, lobbying (registre de la HATVP), place de la France dans des classements
internationaux, rappel du parcours d'une loi et de ses garde-fous, annexes.

**Règle de sources : officielles uniquement** (État français, Union européenne, OCDE, FMI, ONU). Aucune source privée.
Ce qui n'a pas pu être vérifié est écrit « non vérifié » dans le rapport.

## Ce que contient ce dépôt

| Dossier | Contenu |
|---|---|
| `site/` | Le site prêt à publier : `index.html` (historique par année et par mois) et `rapports/AAAA-MM.html` |
| `data/` | **Un fichier JSON par type de données**, réutilisables (voir `data/README.md`) |
| `src/` | Le code Python qui calcule les données et fabrique le rapport (aucune dépendance externe) |

## Fabriquer le rapport

```bash
python3 src/prepare_hatvp.py        # télécharge le registre HATVP (~140 Mo) et recalcule data/hatvp_*.json
python3 src/prepare_assemblee.py    # télécharge l'open data de l'Assemblée et recalcule data/assemblee_*.json
python3 src/build_report.py         # assemble les blocs du rapport (build/blocks.json)
python3 src/make_html.py            # produit build/rapport.html (un seul fichier HTML, SVG intégré)
python3 src/make_site.py 2026-10 build/rapport.html   # range le rapport dans site/ et régénère l'historique
```

Les données `gouvernement_ministres.json` et `classements_internationaux.json` sont tenues à la main : elles sont à
mettre à jour chaque mois depuis les pages officielles citées dans chaque fichier.

## Design

Le texte et les tableaux sont du HTML (lisible sur téléphone, par les lecteurs d'écran, sélectionnable).
Les diagrammes sont des SVG interactifs : chaque élément est cliquable et affiche son détail et un lien vers la
source officielle, à droite du diagramme sur grand écran, en bandeau en bas sur mobile. Chaque diagramme a une
version tableau.

## Licence

Code : MIT (voir `LICENSE`). Les données viennent de sources publiques : respecter leurs licences d'origine
(Licence Ouverte pour les données de l'État, conditions de l'Assemblée nationale, de la HATVP, etc.).
Ce projet n'est affilié à aucune institution.

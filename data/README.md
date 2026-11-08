# Données

Un fichier JSON par type de données. Chaque fichier a la forme `{"meta": {...}, "data": ...}` : `meta` donne la description, la source officielle, la date de génération ; `data` contient les données.

| Fichier | Contenu | Source |
|---|---|---|
| `assemblee_propositions_loi_par_groupe.json` | Propositions de loi déposées par groupe politique, avec l'effectif du groupe | https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs |
| `assemblee_propositions_loi_top_deputes.json` | Les 20 députés en poste ayant déposé le plus de propositions de loi (premier signataire) | https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs |
| `assemblee_propositions_loi_total.json` | Total des propositions de loi, dont celles d'anciens députés non attribuées à un groupe | https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs |
| `classements_internationaux.json` | Position de la France dans des classements internationaux, sources officielles ou intergouvernementales uniquement | Eurostat, OCDE (PISA), Commission européenne, OMPI, PNUD, FMI, Agence France Trésor |
| `gouvernement_ministres.json` | Membres du gouvernement (octobre 2026) : poste, parti, année de naissance, parcours, activité du mois | https://www.info.gouv.fr/ (composition du gouvernement) |
| `hatvp_categories_organisations.json` | Catégorie HATVP de chaque organisation : {nom: [code, libellé]} | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `hatvp_publications_par_mois.json` | Fiches publiées par mois (date de publication), depuis novembre 2024 | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `hatvp_top10_octobre_2026.json` | Organisations ayant publié le plus de fiches en octobre 2026 : [organisation, catégorie, fiches] | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `hatvp_top20_entreprises.json` | Top 20 des entreprises (catégorie ENTREPRISE) par actions déclarées en 2025, séries 2021-2025 | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `hatvp_top20_organisations.json` | Top 20 des organisations par actions déclarées en 2025, séries 2021-2025 | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `hatvp_totaux_par_annee.json` | Nombre de fiches d'action déclarées par année d'exercice | https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json |
| `journal_runs.json` | Pages en échec et empreinte de chaque run | runs mensuels |

`index.json` liste tous les fichiers. Les fichiers `hatvp_*` et `assemblee_*` sont recalculables avec les scripts de `src/`. Les deux autres sont tenus à la main.

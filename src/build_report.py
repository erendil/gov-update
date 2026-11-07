# -*- coding: utf-8 -*-
# Généré par make_build2.py : rapport en blocs, diagrammes avec tableau en option.
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def data(name):
    return json.load(open(os.path.join(ROOT, 'data', name), encoding='utf-8'))['data']
exec(open(os.path.join(ROOT, 'src', 'helpers_core.py'), encoding='utf-8').read())
from diagrams import timeline, pipeline, tracks, votes, rankchart, hbars
H = globals()
BLOCKS = []; SECBLK = []
def begin():
    global out, y
    out = []; y = 10; SEGS.clear()
def pack(y0, yend):
    """découpe le bloc courant en segments : HTML (texte, tableaux) et SVG (diagrammes)"""
    segs = []; pn, py = 0, y0
    def svg_chunk(n0, n1, ya, yb):
        body = "\n".join(out[n0:n1])
        if body.strip() and yb - ya > 1:
            segs.append(["svg", body, ya, yb - ya])
    for frag, n, ya, yb in SEGS:
        svg_chunk(pn, n, py, ya); segs.append(["html", frag]); pn, py = n, yb
    svg_chunk(pn, len(out), py, yend)
    return segs
def block():
    global out, y
    segs = pack(10, y + 10)
    if segs:
        BLOCKS.append({"kind": "seg", "segs": segs})
    begin()
def pair(pid, title, diag_fn, table_fn):
    global out, y
    block()
    begin(); y = 6; diag_fn(); d = pack(6, y + 10)
    begin(); y = 6; table_fn(); t = pack(6, y + 10)
    BLOCKS.append({"kind": "pair", "id": pid, "title": title, "diag": d, "table": t})
    begin()
_h2 = h2
def h2(s, sub=None, simple=None):
    block(); SECBLK.append((s, len(BLOCKS)))
    _h2(s, sub=sub, simple=simple)
begin()
y = 20
hraw('''<header class="top"><h1>Actualité gouvernementale et parlementaire</h1><p class="lead">Compte rendu du mois d'octobre 2026</p><p class="meta">Établi le 7 novembre 2026 · sources officielles uniquement (Élysée, Assemblée nationale, Sénat, HATVP, Eurostat, OCDE…) · sigles écrits en clair, lexique en fin de document</p><div class="how"><b>Comment lire ce rapport</b><p>Chaque section commence par un encadré vert « En clair » : une ou deux phrases simples qui résument l'essentiel. Si vous n'avez que trois minutes, lisez seulement ces encadrés. Les tableaux et graphiques donnent le détail ; le schéma de la section 10 explique comment une loi se fabrique, et la colonne « Étape » des tableaux y renvoie. Tous les mots techniques sont expliqués dans le lexique (section 13).</p></div></header>''', 280)

h2("1. L'essentiel du mois", simple="En octobre, le Parlement a dit non au budget 2027 proposé par le gouvernement, sans proposer autre chose à la place. Résultat : les agences qui notent la France ont pris peur, et le dossier repart au Sénat.")
p("Le budget, c'est la liste des dépenses et des impôts de l'année prochaine. Déposé le 1er octobre, il a été démonté par une Assemblée sans majorité : budget de la Sécu rejeté le 23 octobre (115 contre 1), budget de l'État le 4 novembre (458 contre 0). Pas de 49.3 ; les deux textes repartent au Sénat.")
p("Hors budget : un projet de loi nucléaire (14 octobre), une loi contre les ingérences étrangères votée à l'unanimité au Sénat (20 octobre), l'autonomie de la Corse refusée par le Sénat (26 octobre), et des annonces du Premier ministre face aux lycéens, aux prix des carburants et aux agriculteurs (7 octobre).")
p("Côté classements : l'Agence France Trésor annonce la revue de Fitch le 30 octobre et celle de S&P le 27 novembre ; une baisse de la note rendrait les emprunts de la France plus chers.")

# ---------------------------------------------------------------- 2
h2("2. Le gouvernement en octobre", simple="Le gouvernement, c'est le Premier ministre et ses ministres : ils préparent les lois et dirigent l'administration. En octobre, il a surtout présenté le budget, un texte sur le nucléaire, et répondu à trois crises (lycéens, carburants, agriculteurs).", sub="Gouvernement Lecornu II, minoritaire, en place depuis le 10 octobre 2025 ; aucun changement en octobre (organigramme en section 11).")
_r = [
    ["1er octobre", "Budgets 2027 de l'État et de la Sécurité sociale présentés en Conseil des ministres", "Déficit visé 5,0 % du produit intérieur brut en 2027 (5,4 % en 2026), 43 Md€ de mesures nouvelles, dette 119,3 % fin 2026, charge d'intérêts 91,2 Md€ en 2027"],
    ["1er octobre", "Décret sur le travail d'intérêt général des mineurs dans l'économie sociale et solidaire", "Habilitation des structures confiée aux directeurs territoriaux de la protection judiciaire de la jeunesse"],
    ["1er octobre", "Nominations à la Cour des comptes", "Nathalie Casas et Paul Serre présidents de chambre"],
    ["7 octobre", "Annonces du Premier ministre", "Lycéens : +1,2 Md€ pour l'Éducation nationale (64 Md€), un mois pour chiffrer 40 000 contributions ; carburants : 10 millions de barils de gazole libérés des stocks stratégiques (-12 à -18 c/L attendus) ; électricité : pas de hausse cet hiver ; agriculture : plan d'urgence dans le budget 2027"],
    ["14 octobre", "Projet de loi « secteur nucléaire »", "Étend les simplifications de la loi de 2023 à l'aval du cycle (retraitement, projet Aval du futur d'Orano à La Hague) ; décret d'accélération des chantiers de nouveaux réacteurs (EPR2 de Penly)"],
    ["14 octobre", "Projet de loi de ratification d'une ordonnance fiscale technique", "Report au 1er janvier 2027 du transfert de la TVA dans le code des impositions sur les biens et services"],
    ["14 octobre", "Nominations", "Marie Fontanel conseillère d'État ; Grégoire Dulin secrétaire général adjoint de la Justice ; Alexis Vuillemin commissaire aux transports"],
    ["27 octobre", "Groupe de pilotage nucléaire France-Finlande", "Première réunion à Paris"],
]
pair("gouv", "Décisions du mois sur une frise", lambda: timeline(H, _r, (10, 1), (10, 31), headers=["Date", "Décision", "Détail"]), lambda: table(["Date", "Décision", "Détail"], _r, [1, 3, 5]))
note("Comptes rendus des 7, 22 et 28 octobre non consultés (info.gouv.fr inaccessible).")

# ---------------------------------------------------------------- 3
h2("3. Les textes du mois : qui les porte, ce qu'ils font", simple="Une loi peut venir du gouvernement (on dit alors « projet de loi ») ou d'un député ou sénateur (« proposition de loi »). Ce tableau dit qui a écrit chaque texte, à quoi il sert, et où il en est dans son parcours.", sub="Cinq projets de loi du gouvernement, huit propositions de loi de parlementaires ; deux sont devenues des lois.")
_pjl = [
    ["Lutte contre les ingérences étrangères", "Laurent Nuñez (Intérieur)", "Renforce les outils contre l'influence étrangère dans la vie démocratique ; voté au Sénat le 20 octobre sans voix contre (340 pour)", "Étape 4, navette : Sénat terminé, attend l'Assemblée en 1re lecture"],
    ["Réparation des dégradations dans l'espace public", "Nuñez, Darmanin (Justice), Rist (Santé)", "Facilite l'indemnisation des dégâts de violences urbaines et le recouvrement des dommages et intérêts auprès des auteurs ; voté au Sénat le 27 octobre", "Étape 4, navette : Sénat terminé, attend l'Assemblée en 1re lecture"],
    ["Protection des enfants", "Darmanin, Geffray (Éducation), Rist", "Voté par l'Assemblée le 21 juillet, réécrit par le Sénat (séance 28-29 octobre, vote 3 novembre)", "Étape 4, navette : 2e lecture à l'Assemblée, puis étape 5 (commission mixte paritaire) si désaccord"],
    ["Corse autonome (révision constitutionnelle)", "Françoise Gatel (Décentralisation)", "Inscrit un statut d'autonomie de la Corse dans la Constitution ; adopté par l'Assemblée le 23 juin, rejeté par le Sénat le 26 octobre", "Étape 4, navette bloquée : une révision constitutionnelle exige le même texte dans les deux chambres, puis Congrès ou référendum"],
    ["Secteur nucléaire", "Ministre déléguée à l'Énergie", "Simplifie les procédures pour l'aval du cycle (retraitement à La Hague) et la surveillance des sous-traitants", "Étape 1, dépôt : présenté en Conseil des ministres le 14 octobre, pas encore examiné en commission"],
]
_ppl = [
    ["Rapatriés d'Indochine", "Olivier Faure, député (Socialistes)", "Reconnaissance de la Nation et réparation pour les conditions d'accueil indignes dans les centres de rapatriés", "Étape 7 franchie : loi n° 2026-1008 du 29 octobre 2026 ; reste l'étape 8 (décrets d'application)"],
    ["Abrogation du Code noir", "Max Mathiasin, député (LIOT : indépendants, centristes et outre-mer)", "Abroge formellement l'ordonnance de 1685 et ses textes d'application ; rapport demandé sur le droit colonial encore en vigueur outre-mer", "Étape 7 franchie : loi n° 2026-1015 du 2 novembre 2026 ; pas de décret nécessaire"],
    ["Victimes de violences sexistes et sexuelles", "Laure Miller, députée (Ensemble pour la République, macronistes)", "Information systématique de la victime à la libération de l'agresseur, interdictions judiciaires, guichet unique national ; modifiée par le Sénat le 20 octobre", "Étape 4, navette : 2e lecture à l'Assemblée"],
    ["Rapports locatifs", "Inaki Echaniz, député (Socialistes)", "Pérennise l'encadrement des loyers et lutte contre les congés abusifs ; le Sénat (21 octobre) a remplacé la pérennisation par une prolongation de deux ans", "Étape 4, navette : 2e lecture à l'Assemblée, séance le 18 novembre"],
    ["Accès aux soins des Ultramarins", "Mereana Reid Arbelot, députée (Gauche démocrate et républicaine)", "Égalité d'accès aux soins pour les ressortissants ultramarins dans l'Hexagone ; modifiée par le Sénat le 19 octobre", "Étape 4, navette : 2e lecture à l'Assemblée"],
    ["Titre-restaurant", "Christophe Naegelen, député (LIOT)", "Modernise et rééquilibre le fonctionnement du titre-restaurant ; adoptée par l'Assemblée le 12 octobre", "Étape 4, navette : au Sénat, commission passée (3 novembre), séance le 19 novembre"],
    ["Stocks de sécurité de médicaments", "Jean-François Rapin, sénateur (Les Républicains)", "Révise l'obligation de stocks pour limiter les pénuries ; adoptée au Sénat le 13 octobre", "Étape 4, navette : attend l'Assemblée en 1re lecture"],
    ["Modernisation de la radio", "Laurent Lafon, sénateur (Union centriste)", "Adapte le cadre de la radio (radio numérique terrestre, diffusion) ; adoptée au Sénat le 13 octobre", "Étape 4, navette : attend l'Assemblée en 1re lecture"],
]
pair("textes", "Les textes du mois placés sur le parcours d'une loi", lambda: pipeline(H, [("Projets de loi du gouvernement", BLUE, _pjl, ["Texte", "Porté par", "Ce qu'il fait", "Étape"]), ("Propositions de loi de parlementaires", ORANGE, _ppl, ["Texte", "Premier signataire (groupe)", "Ce qu'elle fait", "Étape"])]), lambda: (h3("Projets de loi du gouvernement"), table(["Texte", "Porté par", "Ce qu'il fait", "Étape (voir schéma, section 10)"], _pjl, [2.2, 1.7, 3.6, 3]), h3("Propositions de loi de parlementaires"), table(["Texte", "Premier signataire (groupe)", "Ce qu'elle fait", "Étape (voir schéma, section 10)"], _ppl, [2.1, 2.3, 3.4, 2.7])))

# ---------------------------------------------------------------- 4
h2("4. Zoom sur un texte : le budget 2027", simple="Le gouvernement voulait réduire le déficit, c'est-à-dire l'écart entre ce que l'État dépense et ce qu'il gagne, en économisant 43 milliards d'euros. Les députés ont rejeté le plan sans en proposer un autre. Le Sénat prend le relais en novembre.", sub="Deux textes déposés le 1er octobre (État n° 3210, Sécu n° 3211), rejetés par l'Assemblée ; pas de 49.3 ; retour au Sénat sur le texte initial.")
_f = [
    ["Porté par", "Roland Lescure (Économie) et David Amiel (Comptes publics)", "Stéphanie Rist (Santé), Jean-Pierre Farandou (Travail), avec Lescure et Amiel"],
    ["Déposé", "1er octobre 2026 à l'Assemblée (étape 1)", "1er octobre 2026 à l'Assemblée (étape 1)"],
    ["Commission (étape 2)", "Finances : partie recettes rejetée le 9 octobre (31 contre 3)", "Affaires sociales : rejeté du 12 au 16 octobre"],
    ["Séance (étape 3)", "Du 13 octobre au 4 novembre ; partie recettes rejetée 458 contre 0", "Du 20 au 23 octobre ; partie recettes rejetée 115 contre 1"],
    ["Étape actuelle", "Étape 4, navette : Sénat du 20 novembre au 9 décembre, sur le texte initial", "Étape 4, navette : Sénat du 9 au 18 novembre, sur le texte initial"],
    ["Délai constitutionnel", "70 jours, jusqu'au 17 décembre", "50 jours, jusqu'au 26 novembre environ"],
    ["Garde-fous déjà intervenus", "Haut Conseil des finances publiques : croissance « optimiste », retour sous 3 % en 2029 « très peu vraisemblable »", "Haut Conseil des finances publiques, même avis"],
    ["Issues possibles", "Étape 5 (commission mixte paritaire) puis 6, ou raccourcis : 49.3, ordonnance, loi spéciale", "Étape 5 puis 6, ou ordonnance après le délai de 50 jours"],
]
_info = lambda c: {1: _f[1][c], 2: _f[2][c], 3: _f[3][c], 4: _f[4][c], 5: _f[7][c], 6: _f[7][c]}
pair("fiche", "Où en sont les deux budgets sur le parcours", lambda: tracks(H, [("Budget de l'État", 4, _info(1), _f, 1), ("Budget de la Sécurité sociale", 4, _info(2), _f, 2)]), lambda: table(["", "Budget de l'État (projet de loi de finances)", "Budget de la Sécurité sociale"], _f, [1.6, 3.7, 3.7], size=12))
h3("Les chiffres du projet")
stat_tiles([
    ("5,0 %", "Déficit public visé 2027", "contre 5,4 % en 2026"),
    ("121,7 %", "Dette publique fin 2027", "119,3 % fin 2026"),
    ("91,2 Md€", "Charge d'intérêts 2027", "79,2 Md€ en 2026"),
    ("43 Md€", "Mesures nouvelles", "25 en économies, 18 en recettes"),
    ("12,7 Md€", "Déficit Sécu visé 2027", "21,8 Md€ attendus en 2026"),
])
p("Le Haut Conseil des finances publiques (expert indépendant) juge la croissance 2027 « optimiste », l'effort réel à 28 Md€ et le retour sous 3 % de déficit en 2029 « très peu vraisemblable ».", 13.5)
h3("Principales mesures proposées")
bullets([
    "Pas de hausse générale d'impôt ; barème de l'impôt sur le revenu indexé sur l'inflation.",
    "Retraités : abattement de 10 % plafonné à 3 000 € (contre 4 439 €) ; pensions au-dessus de 1 260 € par mois gelées ou sous-indexées (4,1 Md€ d'économies).",
    "Grandes entreprises : surtaxe exceptionnelle prolongée un an mais réduite d'un tiers ; contribution minimale de 20 % sur les très hauts revenus prolongée.",
    "Fonction publique : point d'indice gelé, 1 076 postes supprimés ; prestations familiales et aides au logement non revalorisées ; crédits des ministères gelés sauf Défense (+6,5 Md€).",
    "Santé : dépenses d'assurance maladie limitées à +2 % (+3 % pour les hôpitaux), suivi renforcé des arrêts de travail longs, 5,1 Md€ d'économies sur les soins, extension de la taxe sur les sodas.",
    "Entreprises : suramortissement de 30 % (60 % pour les très petites) pour la reprise par les salariés (« pacte Papin ») ; régime des locations meublées durci ; nouvelles taxes sur les grandes infrastructures de transport, le kérosène et les avoirs en déshérence.",
], 13)
_v = [
    ["9 octobre", "La commission des finances rejette la partie recettes du budget de l'État", "31 contre 3"],
    ["12-16 octobre", "La commission des affaires sociales rejette le budget de la Sécu", ""],
    ["15 octobre", "Séance : la baisse de l'abattement des retraités est supprimée", "116 contre 30"],
    ["16 octobre", "« Taxe Zucman » sur les patrimoines et retour de l'ISF rejetés", ""],
    ["20 octobre", "Séance Sécu : la motion de rejet de La France insoumise est repoussée, puis les articles sont supprimés un à un", "128 contre 259"],
    ["22 octobre", "Extension de la taxe sodas supprimée", "86 contre 58"],
    ["23 octobre", "Partie recettes du budget de la Sécu rejetée, texte « considéré comme rejeté »", "115 contre 1"],
    ["27 octobre", "Prolongation de la surtaxe des grandes entreprises supprimée", "79 contre 77"],
    ["27-28 octobre", "Dispositif contre l'optimisation fiscale des multinationales adopté", "74 contre 72"],
    ["30 octobre", "Avantages fiscaux agricoles élargis contre l'avis du gouvernement ; taxes sur les superdividendes (5 %) et rachats d'actions (10 %) adoptées", "35 contre 29 (épargne de précaution)"],
    ["4 novembre", "Partie recettes du budget de l'État rejetée en bloc", "458 contre 0, 2 abstentions"],
]
pair("votes", "Les votes du mois, pour et contre", lambda: votes(H, _v, headers=["Date", "Événement", "Vote"], fallback="https://www.assemblee-nationale.fr/dyn/17/dossiers/PLF_2027"), lambda: table(["Date", "Événement", "Vote"], _v, [1.2, 5.5, 1.8]))
p("Chaque camp a supprimé les mesures de l'autre ; le texte final ne convenait plus à personne. Délais : 50 jours pour la Sécu, 70 pour l'État (17 décembre). Au-delà : ordonnance ou loi spéciale, comme en 2024 et 2025.", 13.5)

# ---------------------------------------------------------------- 5
h2("5. Ce qu'octobre change pour les classements internationaux", simple="Des organismes publics (Union européenne, OCDE, FMI, ONU) comparent les pays : qui est le plus endetté, où les élèves ont le meilleur niveau, où l'on juge la corruption répandue. En octobre, rien n'a bougé pour l'école ni la corruption, et la dette reste un point faible.")
table(["Classement", "Dernière position de la France", "Ce qu'octobre change"], [
    ["Notation de la dette (Fitch)", "Revue prévue le 30 octobre 2026 (calendrier de l'Agence France Trésor) ; résultat non vérifié dans une source officielle", "Le rejet du budget à 458 voix contre 0 (scrutin public de l'Assemblée) reste le principal risque pour la note."],
    ["Notation de la dette (Moody's)", "Aa3, perspective négative (communiqué du ministère de l'Économie ; date non vérifiée)", "S&P se prononce le 27 novembre (calendrier de l'Agence France Trésor)."],
    ["Déficit et dette (Union européenne)", "5,4 % de déficit en 2026 (Conseil des ministres du 1er octobre) ; 119,1 % de dette au 2e trimestre 2026 (Eurostat), 3e rang de l'UE derrière la Grèce et l'Italie", "L'objectif de 5,0 % pour 2027 repose sur un budget que l'Assemblée a rejeté (458 voix contre 0)."],
    ["Éducation (PISA 2025, OCDE)", "Maths 458 points (OCDE : 463, -16 depuis 2022), lecture 456 (OCDE : 461, -18), sciences 483 (OCDE : 482, -4)", "Aucune mesure pédagogique de fond n'a été votée en octobre. Effets visibles au plus tôt dans PISA 2029."],
    ["Corruption (Eurobaromètre, Commission européenne)", "77 % des Français jugent la corruption répandue (UE : 71 %)", "Octobre n'apporte rien sur ce point. À noter : la loi sur les ingérences étrangères, adoptée par le Sénat le 20 octobre (340 voix pour, 0 contre). Le plan national anticorruption 2025-2029 compte 36 mesures (rapport 2026 sur l'État de droit)."],
], [1.8, 2.8, 4.4])
note("Ces classements paraissent avec un à trois ans de retard : octobre 2026 se lira dans l'indice de corruption de février 2027, les notations de fin 2026 et PISA 2029.")

# ---------------------------------------------------------------- 6
h2("6. À surveiller en novembre", simple="En novembre, tout se joue au Sénat : il examine les deux budgets. Et le 27 novembre, une troisième agence de notation, S&P, donne son verdict sur la France.")
_s = [
    ["9 au 18 novembre", "Budget de la Sécu au Sénat (texte initial du gouvernement)", "Le Sénat, à majorité droite et centre, votera probablement un texte durci ; ensuite commission mixte paritaire ou nouvelle lecture"],
    ["18 novembre", "Loi de finances de fin de gestion 2026 au Sénat ; rapports locatifs en 2e lecture à l'Assemblée", "Ajustement des comptes 2026"],
    ["19 novembre", "Titre-restaurant au Sénat", ""],
    ["20 novembre au 9 décembre", "Budget de l'État au Sénat (texte initial), sous réserve de transmission", "Le vrai débat budgétaire se déplace au Sénat"],
    ["26 novembre environ", "Fin du délai de 50 jours pour le budget de la Sécu", "Ordonnance possible si pas de vote"],
    ["27 novembre", "Décision de S&P sur la note de la France", "Troisième agence en un mois ; une perspective négative ferait l'unanimité des agences"],
    ["17 décembre", "Fin du délai de 70 jours pour le budget de l'État", "Ordonnance, loi spéciale ou 49.3"],
]
pair("suivre", "Le calendrier des prochaines semaines", lambda: timeline(H, _s, (11, 9), (12, 17), default_month=11, headers=["Date", "Quoi", "Enjeu"]), lambda: table(["Date", "Quoi", "Enjeu"], _s, [1.6, 3.6, 3.8]))

# ---------------------------------------------------------------- 7  QUI BOSSE LE PLUS
h2("7. Qui travaille le plus ? Propositions de loi par famille politique et par député", simple="Un député peut écrire des propositions de loi. Certains en déposent des dizaines, d'autres presque aucune. Mais déposer beaucoup ne veut pas dire faire adopter : seule 1 proposition sur 20 devient une loi.", sub="Du 20 juillet 2024 au 4 novembre 2026 : 1 717 propositions de loi déposées à l'Assemblée nationale (données ouvertes de l'Assemblée nationale).")
SHORT = {'DR': 'Droite républicaine', 'LFI-NFP': 'La France insoumise', 'SOC': 'Socialistes', 'UDR': 'UDR (alliés du RN)', 'ECOS': 'Écologistes', 'EPR': 'Ensemble pour la République', 'RN': 'Rassemblement national', 'LIOT': 'LIOT', 'DEM': 'Démocrates (MoDem)', 'GDR': 'Gauche démocrate et rép.', 'HOR': 'Horizons', 'NI': 'Non inscrits'}
# calcul officiel : open data de l'Assemblée nationale (7 novembre 2026), premier signataire, groupe actuel
groups = [(g['groupe_court'] if 'groupe_court' in g else SHORT.get(g['sigle'], g['groupe']), g['deputes'], g['propositions']) for g in data('assemblee_propositions_loi_par_groupe.json')]
tot = sorted([(g, n) for g, e, n in groups], key=lambda t: -t[1])
per = sorted([(g, round(n / e, 1)) for g, e, n in groups], key=lambda t: -t[1])
half = (CW - 30) / 2
y0 = y
h_a = hbar_chart("Propositions de loi déposées par groupe", tot, x=M, width=half,
                 note_txt="Comptées en premier signataire, par groupe actuel du député, du 20 juillet 2024 au 4 novembre 2026 (données ouvertes de l'Assemblée nationale). Les gros groupes dominent en volume.")
y = y0
h_b = hbar_chart("Propositions de loi par député, selon le groupe", per, x=M + half + 30, width=half, color=ORANGE, fmt=lambda v: f"{v:.1f}".replace(".", ","),
                 note_txt="Rapporté à l'effectif, ce sont les petits groupes de droite (UDR, Droite républicaine, LIOT) qui déposent le plus ; le Rassemblement national et Horizons le moins.")
y = y0 + max(h_a, h_b) + 10
_top = [r for r in data('assemblee_propositions_loi_top_deputes.json')][:10]
_gs = {g['groupe']: SHORT.get(g['sigle'], g['groupe']) for g in data('assemblee_propositions_loi_par_groupe.json')}
_d = [[str(i + 1), _top[i]['depute'], f"{_gs[_top[i]['groupe']]} ({_top[i]['departement']})", str(_top[i]['propositions']),
       str(i + 6), _top[i + 5]['depute'], f"{_gs[_top[i + 5]['groupe']]} ({_top[i + 5]['departement']})", str(_top[i + 5]['propositions'])] for i in range(5)]
_dep = [(r[1] + " (" + r[2].split(" (")[0] + ")", int(r[3])) for r in _d] + [(r[5] + " (" + r[6].split(" (")[0] + ")", int(r[7])) for r in _d]
pair("deputes", "Les députés qui déposent le plus de propositions de loi", lambda: hbars(H, "Propositions de loi déposées en premier signataire", _dep, labw=330, color=lambda i, l: ORANGE if "insoumise" in l or "Écolog" in l else BLUE, details=(["Rang", "Député", "Groupe", "Propositions de loi (premier signataire)"], [[r[0], r[1], r[2], r[3]] for r in _d] + [[r[4], r[5], r[6], r[7]] for r in _d]), fallback="https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs"), lambda: table(["Rang", "Député", "Groupe", "Propositions", "Rang", "Député", "Groupe", "Propositions"], _d, [0.5, 1.6, 2.1, 1, 0.5, 2, 2.1, 1], size=12))
note("Source : données ouvertes de l'Assemblée nationale (data.assemblee-nationale.fr), recalculées le 7 novembre 2026. Seuls les députés en poste sont classés ; 137 propositions de loi déposées par d'anciens députés ne sont pas attribuées à un groupe.")

# ---------------------------------------------------------------- 8  LOBBY
h2("8. Lobbying : qui intervient de l'extérieur, et combien", simple="Les lobbies sont des entreprises, des associations ou des syndicats qui essaient de convaincre les élus et les ministres. C'est légal, mais ils doivent s'inscrire dans un registre public et déclarer ce qu'ils font. Les plus actifs sont des cabinets spécialisés qui travaillent pour des clients.", sub="Calculé sur le fichier open data du registre HATVP, téléchargé le 7 novembre 2026 : 4 111 organisations, 113 548 actions déclarées.")
LD = {'totals': data('hatvp_totaux_par_annee.json'), 'monthly': data('hatvp_publications_par_mois.json'), 'all': data('hatvp_top20_organisations.json'),
      'ent': data('hatvp_top20_entreprises.json'), 'octtop': data('hatvp_top10_octobre_2026.json')}
y0 = y
tot = LD['totals']
h_a = line_chart("Actions de lobbying déclarées, par année d'exercice", [("fiches", BLUE, [(yv, tot[str(yv)]) for yv in range(2019, 2026)])], M, half, 230,
                 note_txt="Une fiche = une action déclarée (un objet, un ou plusieurs interlocuteurs). L'exercice 2026 (422 fiches à ce jour) sera déclaré avant le 31 mars 2027. Les totaux dépassent ceux des bilans HATVP, qui arrêtent les compteurs au 30 avril.")
y = y0
mon = LD['monthly']
h_b = line_chart("Fiches publiées chaque mois, novembre 2024 à octobre 2026", [("publiées", ORANGE, [(i + 1, v) for i, (_, v) in enumerate(mon)])], M + half + 30, half, 230, xlabels=[{"01":"janv.","02":"févr.","03":"mars","04":"avr.","05":"mai","06":"juin","07":"juil.","08":"août","09":"sept.","10":"oct.","11":"nov.","12":"déc."}[m[5:]] + " " + m[2:4] for m, _ in mon], every=3,
                 note_txt="Les pics (13 091 en mars 2025, 14 549 en mars 2026) sont la date limite de déclaration annuelle. Octobre 2026 : 461 fiches publiées, contre 523 en octobre 2025.")
y = y0 + max(h_a, h_b) + 6
p("Le registre est annuel et sans date d'action : un « mois » ne mesure que les fiches publiées. Les grands cabinets déclarent tout en mars ; le top d'octobre ne montre que ceux qui déclarent au fil de l'eau.", 13)

NICE = {
 "MOUVEMENT DES ENTREPRISES DE FRANCE": "Medef", "ANTHENOR PUBLIC AFFAIRS": "Anthenor Public Affairs", "BOURY TALLON & ASSOCIES": "Boury Tallon & Associés",
 "APF France Handicap": "APF France Handicap", "CONFEDERATION DES PETITES ET MOYENNES ENTREPRISES": "CPME", "FEDERATION FRANCAISE DE L ASSURANCE (FFA)": "France Assureurs (FFA)",
 "ESL & NETWORK FRANCE SAS": "ESL & Network", "COMFLUENCE": "Comfluence", "COM'PUBLICS": "Com'Publics", "LYSIOS": "Lysios", "COMMUNICATION & INSTITUTIONS": "Communication & Institutions",
 "SYNDICAT DES ENERGIES RENOUVELABLES": "Syndicat des énergies renouvelables", "TADDEO": "Taddeo", "AI2P": "AI2P", "CONSEIL NATIONAL DES BARREAUX": "Conseil national des barreaux",
 "UNION  TRANSPORTS PUBLICS FERROVIAIRES": "Union des transports publics et ferroviaires", "KAIROS MSC": "Kairos MSC", "FEDER SYNDICATS EXPLOIT AGRICOL MAYENNE": "FDSEA Mayenne",
 "GOOGLE FRANCE": "Google France", "IMAGE 7": "Image 7", "VALOBAT": "Valobat (éco-organisme bâtiment)", "CA CONSUMER FINANCE": "CA Consumer Finance (Crédit agricole)",
 "SANOFI WINTHROP INDUSTRIE": "Sanofi", "VALOREM": "Valorem (énergies renouvelables)", "ELECTRICITE DE FRANCE": "EDF", "ICADE": "Icade", "SOCIETE NATIONALE SNCF": "SNCF",
 "DB CARGO FRANCE": "DB Cargo France", "VEOLIA ENVIRONNEMENT": "Veolia", "SNC ALTAREA MANAGEMENT": "Altarea", "COVEA": "Covéa (MAAF, MMA, GMF)", "HAVAS PARIS": "Havas Paris",
 "JUNG S.A.S": "Jung", "MSD FRANCE": "MSD France", "TOTALENERGIES SE": "TotalEnergies", "SOLVEO ENERGIES": "Solveo Énergies", "CARREFOUR MANAGEMENT": "Carrefour", "ENEDIS": "Enedis", "SUEZ": "Suez",
 "GROUPEMENT DES HOTELLERIES ET RESTAURATIONS DE FRANCE": "Groupement des hôtelleries et restaurations de France", "COMITE DE LIAISON DES ENTREPRISES AYANT EXERCE LEUR ELIGIBILITE": "Comité de liaison des entreprises ayant exercé leur éligibilité (électricité)",
 "CERCLE NATIONAL DU RECYCLAGE": "Cercle national du recyclage", "BUREAU NATIONAL INTERPR COGNAC": "Bureau national interprofessionnel du cognac", "FONDAMENTAL": "FondaMental (fondation santé mentale)",
 "CONFEDERATION NATIONALE AGRICOLE DES EXPLOITANTS FAMILIAUX MODEF": "Modef (agriculteurs familiaux)", "FEDERATION FRANCAISE DES PRODUCTEURFED FR": "Fédération française des producteurs (FFP)", "REV Mobilities": "REV Mobilities",
 "COMITE REG PECHE MARITIME ELEVAGE MARIN": "Comité régional des pêches maritimes", "SYND GENERAL DES VIGNERONS DE CHAMPAGNE": "Syndicat général des vignerons de Champagne",
}
CATN = {"Cabinet de conseil": "Cabinet de conseil", "Organisation syndicale et professionnelle": "Fédération / syndicat", "Association": "Association / ONG",
        "Société commerciale et civile (autre que cabinet d’avocats et société de conseil)": "Entreprise"}
def nice(o): return NICE.get(o, o.title())
def catn(c): return CATN.get(c or "", (c or "")[:22])
yrs = ["2021", "2022", "2023", "2024", "2025"]
_t = [[str(i + 1), nice(t["org"]), catn(t["cat"])] + [str(t["years"][yv]) for yv in yrs] for i, t in enumerate(LD["all"])]
pair("top20", "Top 20 toutes catégories, actions déclarées en 2025 (survol : 2021 à 2025)", lambda: hbars(H, "Actions déclarées en 2025", [(r[1], int(r[7])) for r in _t], tips=[r[1] + " (" + r[2] + ") : " + " · ".join(f"{y} : {v}" for y, v in zip(yrs, r[3:8])) for r in _t], labw=330, color=lambda i, l: BLUE if _t[i][2] != "Cabinet de conseil" else ORANGE, sub=[r[2] for r in _t], trend=(yrs, [[int(v) for v in r[3:8]] for r in _t]), details=(["Rang", "Organisation", "Type"] + yrs, _t), fallback="https://www.hatvp.fr/le-repertoire/"), lambda: table(["#", "Organisation", "Type"] + yrs, _t, [0.35, 3.2, 1.6, 0.6, 0.6, 0.6, 0.6, 0.6], size=12, bold_first=False))
p("11 des 20 premiers sont des cabinets de conseil qui déclarent pour leurs clients ; une seule entreprise en propre (Google), une seule association (APF France Handicap, ×7 en cinq ans).", 13)
_e = [[str(i + 1), nice(t["org"]), sec] + [str(t["years"][yv]) for yv in yrs] for i, (t, sec) in enumerate(zip(LD["ent"], [
    "Numérique", "Déchets du bâtiment", "Crédit à la consommation", "Pharmacie", "Énergies renouvelables", "Électricité", "Immobilier", "Ferroviaire", "Fret ferroviaire", "Eau, déchets",
    "Immobilier", "Assurance", "Communication", "Appareillage électrique", "Pharmacie", "Pétrole, énergie", "Énergies renouvelables", "Distribution", "Réseau électrique", "Eau, déchets"]))]
pair("top20e", "Top 20 des entreprises, actions déclarées en 2025 (survol : 2021 à 2025)", lambda: hbars(H, "Actions déclarées en 2025", [(r[1], int(r[7])) for r in _e], tips=[r[1] + " (" + r[2] + ") : " + " · ".join(f"{y} : {v}" for y, v in zip(yrs, r[3:8])) for r in _e], labw=330, sub=[r[2] for r in _e], trend=(yrs, [[int(v) for v in r[3:8]] for r in _e]), details=(["Rang", "Entreprise", "Secteur"] + yrs, _e), fallback="https://www.hatvp.fr/le-repertoire/"), lambda: table(["#", "Entreprise", "Secteur"] + yrs, _e, [0.35, 3.2, 1.6, 0.6, 0.6, 0.6, 0.6, 0.6], size=12, bold_first=False))
p("Les entreprises déclarent peu en propre (82 pour Google, contre 355 pour le Medef). Énergie, immobilier, santé et transports dominent ; entrées rapides : CA Consumer Finance et Icade.", 13)
_m = [[str(i + 1), nice(o), catn(c), str(n)] for i, (o, c, n) in enumerate(LD["octtop"])]
pair("mois", "Qui a publié des fiches en octobre 2026", lambda: hbars(H, "Fiches publiées en octobre 2026", [(r[1], int(r[3])) for r in _m], labw=420, color=lambda i, l: ORANGE, sub=[r[2] for r in _m], details=(["Rang", "Organisation", "Type", "Fiches publiées en octobre 2026"], _m), fallback="https://www.hatvp.fr/le-repertoire/"), lambda: table(["#", "Organisation", "Type", "Fiches publiées en octobre"], _m, [0.35, 4.4, 2, 1.8], size=12, bold_first=False))
note("Fiches de l'exercice 2026 en cours, dans des secteurs touchés par le budget 2027. Source : HATVP, open data du répertoire.")

# ---------------------------------------------------------------- 9  CLASSEMENTS
h2("9. Où en est la France dans les classements internationaux ?", simple="La France est 3e pays le plus endetté de l'Union européenne ; 77 % des Français jugent la corruption répandue (71 % dans l'UE) ; et le niveau des élèves de 15 ans est proche de la moyenne de l'OCDE en sciences, un peu en dessous en maths et en lecture.")
_c = [[r[k] for k in ('domaine', 'classement', 'rang_france', 'tendance', 'edition')] for r in data('classements_internationaux.json')]
pair("classements", "La place de la France dans chaque classement", lambda: rankchart(H, _c, headers=["Domaine", "Classement (organisme)", "Rang de la France", "Tendance", "Édition"]), lambda: table(["Domaine", "Classement (organisme)", "Rang de la France", "Tendance", "Édition"], _c, [1.4, 2.2, 2.6, 2.4, 1.4], size=12))
note("Seules des sources officielles sont retenues : l'État français, l'Union européenne, l'OCDE, le FMI et l'ONU. Les classements d'organisations privées (corruption, liberté de la presse, démocratie, compétitivité) ne sont plus utilisés : il n'existe pas d'équivalent public pour la presse et la démocratie. Non vérifiés : rang de la France au PISA, note Fitch, tendance de l'Eurobaromètre. Détails en section 14.")

# ---------------------------------------------------------------- 10  PARCOURS D'UNE LOI
h2("10. Rappel : le parcours d'un projet de loi et ses garde-fous", simple="Une loi passe par au moins six étapes avant d'exister, et plusieurs institutions peuvent la bloquer ou la corriger en chemin. Les cases bleues sont le chemin normal, les rouges les contrôles, les jaunes les raccourcis du gouvernement.")
d0 = y + 10
bw, bh = 176, 122
gapx = (CW - 6 * bw) / 5
xs6 = [M + i * (bw + gapx) for i in range(6)]
row1 = d0
box(xs6[0], row1, bw, bh, "1. Dépôt", ["Projet de loi : le gouvernement, après avis du Conseil d'État et étude d'impact", "Proposition de loi : un député ou un sénateur"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"1\" data-tip=\"Le texte est déposé : projet de loi (gouvernement) ou proposition de loi (parlementaire)\"")
box(xs6[1], row1, bw, bh, "2. Commission", ["Des parlementaires spécialisés auditionnent et réécrivent le texte ; c'est leur version qui va en séance"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"2\" data-tip=\"Une commission spécialisée auditionne et réécrit le texte\"")
box(xs6[2], row1, bw, bh, "3. Séance publique", ["Débat, amendements, vote article par article puis vote d'ensemble dans la première chambre"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"3\" data-tip=\"Débat, amendements et vote dans la première chambre\"")
box(xs6[3], row1, bw, bh, "4. Navette", ["Même parcours dans l'autre chambre ; aller-retour jusqu'à un texte identique"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"4\" data-tip=\"Le texte passe dans l&apos;autre chambre, aller-retour jusqu&apos;à accord\"")
box(xs6[4], row1, bw, bh, "5. Commission mixte", ["7 députés et 7 sénateurs cherchent un compromis ; en cas d'échec, l'Assemblée a le dernier mot"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"5\" data-tip=\"7 députés et 7 sénateurs cherchent un compromis\"")
box(xs6[5], row1, bw, bh, "6. Adoption définitive", ["Le même texte a été voté par les deux chambres (ou par l'Assemblée seule, en dernier mot)"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"6\" data-tip=\"Les deux chambres ont voté le même texte\"")
for i in range(5):
    arrow(xs6[i] + bw, row1 + bh / 2, xs6[i + 1] - 2, row1 + bh / 2)
# ligne 2 : garde-fous et raccourcis, un par colonne
row2 = row1 + bh + 56
gh = 118
box(xs6[0], row2, bw, gh, "Conseil d'État", ["Avis juridique obligatoire sur tout projet de loi, avant le Conseil des ministres"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[1], row2, bw, gh, "Haut Conseil des finances publiques", ["Juge le réalisme des prévisions des textes budgétaires (avis public)"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[2], row2, bw, gh, "Motions de rejet et de censure", ["Les députés peuvent refuser d'examiner le texte, ou renverser le gouvernement"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[3], row2, bw, gh, "Le Sénat", ["Peut amender, rejeter, retarder ; bloque à lui seul une révision de la Constitution"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[4], row2, bw, gh, "Raccourci : article 49.3", ["Adoption sans vote, sauf si une motion de censure renverse le gouvernement"], fill="#f9eeda", stroke=WARN, tcolor=INK, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[5], row2, bw, gh, "Conseil constitutionnel", ["Saisi par 60 députés ou 60 sénateurs, il annule les articles contraires à la Constitution"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
for i in range(6):
    col = WARN if i == 4 else CRIT
    arrow(xs6[i] + bw / 2, row2 - 2, xs6[i] + bw / 2, row1 + bh + 4, color=col, dash=True)
# ligne 3 : après l'adoption
row3 = row2 + gh + 70
box(xs6[0], row3, bw, bh, "7. Promulgation", ["Signature par le Président de la République sous 15 jours, publication au Journal officiel"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"7\" data-tip=\"Signature du Président, publication au Journal officiel\"")
box(xs6[1], row3, bw, bh, "8. Décrets d'application", ["Pris par le gouvernement ; sans eux, beaucoup d'articles restent lettre morte"], fill=BLUE_L, stroke=BLUE, attrs="class=\"step\" data-step=\"8\" data-tip=\"Le gouvernement prend les textes qui rendent la loi applicable\"")
box(xs6[2], row3, bw, bh, "9. Contrôle après coup", ["Cour des comptes (exécution des budgets), question prioritaire de constitutionnalité, évaluation par le Parlement"], fill=SURF, stroke=CRIT, tcolor=CRIT, attrs="class=\"step\" data-step=\"9\" data-tip=\"Cour des comptes, question prioritaire de constitutionnalité, évaluation\"")
box(xs6[3], row3, bw, bh, "Raccourci : ordonnance", ["Budget non voté dans les 50 ou 70 jours, ou habilitation votée par le Parlement : le gouvernement légifère seul"], fill="#f9eeda", stroke=WARN, tcolor=INK, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
box(xs6[4], row3, bw * 2 + gapx, bh, "Hors schéma : les lobbies", ["Interviennent à chaque étape, surtout 1 à 3 ; obligation de s'inscrire au répertoire de la Haute Autorité pour la transparence et de déclarer leurs actions chaque année"], fill="#f3f2ee", stroke=MUTED, attrs="class=\"guard\" data-tip=\"Garde-fou ou raccourci : survolez pour lire, cliquez sur une étape bleue pour voir les textes qui y sont\"")
arrow(xs6[0] + bw, row3 + bh / 2, xs6[1] - 2, row3 + bh / 2)
arrow(xs6[1] + bw, row3 + bh / 2, xs6[2] - 2, row3 + bh / 2)
# retour 6 -> 7 : par la droite puis le couloir entre les lignes 2 et 3
xr = xs6[5] + bw + 18
yc = row2 + gh + 34
out.append(f'<path d="M{xs6[5] + bw},{row1 + bh/2} L{xr},{row1 + bh/2} L{xr},{yc} L{xs6[0] + bw/2},{yc} L{xs6[0] + bw/2},{row3 - 2}" fill="none" stroke="{INK2}" stroke-width="1.8" marker-end="url(#arr)"/>')
out.append(f'<text x="{(xs6[0] + xs6[5]) / 2}" y="{yc - 6}" font-size="11.5" fill="{INK2}" text-anchor="middle">après l\'adoption définitive</text>')
y = row3 + bh + 24
p("Budget 2027 : étapes 1 à 3 franchies à l'Assemblée, rejet en bloc, donc étape 4 au Sénat sur le texte initial. Sans accord dans les délais : 49.3 (risque de censure), ordonnance ou loi spéciale.", 13)


# ---------------------------------------------------------------- 11  ANNEXE : QUI GOUVERNE, QUI SIÈGE
h2("11. Annexe : qui gouverne, qui siège", simple="Qui sont les ministres, et combien de députés et de sénateurs a chaque parti. À l'Assemblée, il faut 289 voix pour avoir la majorité : personne ne les a, c'est pour cela que le budget bloque.", sub="Sources : assemblee-nationale.fr, senat.fr (6 novembre 2026) ; composition du gouvernement : info.gouv.fr, à recouper au prochain rapport.")
h3("Organigramme du gouvernement")
PARTY = {"Laurent Nuñez": "RE", "Catherine Vautrin": "RE", "Gérald Darmanin": "DVD", "Roland Lescure": "RE", "David Amiel": "RE", "Jean-Pierre Farandou": "SE",
         "Stéphanie Rist": "RE", "Édouard Geffray": "SE", "Jean-Noël Barrot": "MoDem", "Monique Barbut": "SE", "Annie Genevard": "LR", "Serge Papin": "SE",
         "Françoise Gatel": "UDI", "Philippe Baptiste": "SE", "Catherine Pégard": "SE", "Naïma Moutchou": "HOR", "Philippe Tabarot": "LR", "Vincent Jeanbrun": "LR", "Marina Ferrari": "MoDem", "Sébastien Lecornu": "RE"}
PCOL = {"RE": "#eda100", "MoDem": "#f4c24d", "HOR": "#d08a00", "LR": "#2a78d6", "DVD": "#6da7ec", "UDI": "#5598e7", "SE": "#898781"}
PLAB = {"RE": "Renaissance (macroniste)", "MoDem": "MoDem (centre)", "HOR": "Horizons (centre droit)", "LR": "Les Républicains (droite)", "DVD": "Divers droite", "UDI": "UDI (centre droit)", "SE": "Société civile, sans parti"}
def medal(cx, cy, name, r=17):
    p = PARTY.get(name, "SE"); ini = "".join(w[0] for w in name.replace("-", " ").split() if w[0].isupper())[:2]
    out.append(f'<g data-tip="{esc(name)} : {esc(PLAB[p])}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{PCOL[p]}"/><text x="{cx}" y="{cy + 5}" font-size="{r*0.75:.0f}" font-weight="700" fill="#ffffff" text-anchor="middle">{esc(ini)}</text></g>')
g0 = y + 6
pmw = 420
box(M + (CW - pmw) / 2, g0, pmw, 54, "Sébastien Lecornu, Premier ministre", ["chargé de la Planification écologique et énergétique"], fill=BLUE_L, stroke=BLUE, attrs='class="person" data-person="Sébastien Lecornu"')
medal(M + (CW - pmw) / 2 + 28, g0 + 27, "Sébastien Lecornu", r=20)
# délégués auprès du PM
dw = (CW - 2 * 16) / 3
dl = [("Laurent Panifous", "Relations avec le Parlement"), ("Maud Bregeon", "Porte-parole du Gouvernement ; Énergie (avec l'Économie)"), ("Aurore Bergé", "Égalité femmes-hommes, lutte contre les discriminations")]
yd = g0 + 54 + 36
for i, (n, f) in enumerate(dl):
    x = M + i * (dw + 16)
    box(x, yd, dw, 68, n, ["ministre déléguée auprès du Premier ministre : " + f if n != "Laurent Panifous" else "ministre délégué auprès du Premier ministre : " + f], fill="#f3f2ee", stroke=MUTED, size=11.5, attrs=f'class="person" data-person="{esc(n)}"')
    medal(x + 22, yd + 20, n, r=13)
    arrow(M + CW / 2, g0 + 54, x + dw / 2, yd - 2)
# ministères
mins = [
 ("Intérieur", "Laurent Nuñez", ["Jean-Didier Berger (délégué)", "Marie-Pierre Vedrenne (Citoyenneté)"]),
 ("Armées et Anciens combattants", "Catherine Vautrin", ["Alice Rufo (déléguée)"]),
 ("Justice (garde des Sceaux)", "Gérald Darmanin", []),
 ("Économie, Finances, Souveraineté industrielle, énergétique et numérique", "Roland Lescure", ["Sébastien Martin (Industrie)", "Anne Le Hénanff (IA et Numérique)", "Maud Bregeon (Énergie)"]),
 ("Action et Comptes publics", "David Amiel", []),
 ("Travail et Solidarités", "Jean-Pierre Farandou", ["Sabrina Roubache (Formation professionnelle, avec l'Éducation)"]),
 ("Santé, Familles, Autonomie, Personnes handicapées", "Stéphanie Rist", ["Camille Galliard-Minier (Autonomie, handicap)"]),
 ("Éducation nationale", "Édouard Geffray", ["Sabrina Roubache (Enseignement professionnel)"]),
 ("Europe et Affaires étrangères", "Jean-Noël Barrot", ["Benjamin Haddad (Europe)", "Nicolas Forissier (Commerce extérieur)", "Éléonore Caroit (Francophonie, Français de l'étranger)"]),
 ("Transition écologique, Biodiversité, Climat", "Monique Barbut", ["Catherine Chabaud (Mer et Pêche)", "Mathieu Lefèvre (Transition écologique)"]),
 ("Agriculture et Souveraineté alimentaire", "Annie Genevard", []),
 ("PME, Commerce, Artisanat, Tourisme, Pouvoir d'achat", "Serge Papin", []),
 ("Aménagement du territoire et Décentralisation", "Françoise Gatel", ["Ruralité reprise depuis le 22 septembre"]),
 ("Enseignement supérieur, Recherche, Espace", "Philippe Baptiste", []),
 ("Culture", "Catherine Pégard", []),
 ("Outre-mer", "Naïma Moutchou", []),
 ("Transports", "Philippe Tabarot", []),
 ("Ville et Logement", "Vincent Jeanbrun", []),
 ("Sports, Jeunesse, Vie associative", "Marina Ferrari", []),
]
cols = 4; gap = 14; mw = (CW - gap * (cols - 1)) / cols; mh = 106
ym = yd + 68 + 40
out.append(f'<line x1="{M + CW/2}" y1="{yd + 68}" x2="{M + CW/2}" y2="{ym - 16}" stroke="{INK2}" stroke-width="1.8"/>')
out.append(f'<line x1="{M + mw/2}" y1="{ym - 16}" x2="{M + CW - mw/2}" y2="{ym - 16}" stroke="{INK2}" stroke-width="1.8"/>')
for i, (minist, name, dels) in enumerate(mins):
    r, c = divmod(i, cols)
    x = M + c * (mw + gap); yy = ym + r * (mh + gap)
    if r == 0:
        out.append(f'<line x1="{x + mw/2}" y1="{ym - 16}" x2="{x + mw/2}" y2="{yy - 2}" stroke="{INK2}" stroke-width="1.8"/>')
    out.append(f'<g class="person" data-person="{esc(name)}"><rect x="{x}" y="{yy}" width="{mw}" height="{mh}" rx="6" fill="{SURF}" stroke="{BLUE}" stroke-width="1.2"/>')
    medal(x + 24, yy + 26, name)
    tx = x + 50
    yy2 = yy + 18
    for ln in wrap(minist, 11.5, mw - 58)[:2]:
        out.append(f'<text x="{tx}" y="{yy2}" font-size="11.5" fill="{INK2}">{esc(ln)}</text>'); yy2 += 14
    out.append(f'<text class="pname" x="{tx}" y="{yy2 + 4}" font-size="13.5" font-weight="700" fill="{INK}">{esc(name)}</text>')
    out.append(f'<text class="pmask" x="{tx}" y="{yy2 + 4}" font-size="12" font-weight="700" fill="{BLUE}">Qui est-ce ? Cliquez</text>'); yy2 += 22
    for d in dels:
        for ln in wrap(d, 10.5, mw - 16)[:2]:
            out.append(f'<text x="{x + 8}" y="{yy2}" font-size="10.5" fill="{MUTED}">{esc(ln)}</text>'); yy2 += 13
    out.append('</g>')
y = ym + ((len(mins) - 1) // cols + 1) * (mh + gap) + 8
lx = M
for p_ in ["RE", "MoDem", "HOR", "LR", "DVD", "UDI", "SE"]:
    out.append(f'<circle cx="{lx + 6}" cy="{y + 7}" r="6" fill="{PCOL[p_]}"/>')
    out.append(f'<text x="{lx + 17}" y="{y + 11}" font-size="11.5" fill="{INK2}">{esc(PLAB[p_])}</text>')
    lx += 17 + text_width(PLAB[p_], 11.5) + 22
y += 24
note("Cliquez sur un ministre pour ouvrir sa fiche (parcours, parti, dossiers du mois, lien vers le site officiel du gouvernement) ; le bouton « Qui est-ce ? » du sommaire cache les noms pour s'entraîner. Médaillons : initiales et couleur de la famille politique. 19 ministres, 14 ministres délégués (en gris). Depuis octobre 2025 : Montchalin remplacée par Amiel (22 février 2026), Dati par Pégard (26 février), départ de Fournier, Ruralité (22 septembre).")

h3("Répartition des sièges par groupe")
import math
an = [("Rassemblement national", 121, "rn"), ("Ensemble pour la République (macronistes)", 90, "centre"), ("La France insoumise", 70, "gauche"), ("Socialistes", 68, "gauche"),
      ("Droite républicaine (ex-LR)", 46, "droite"), ("Écologiste et social", 38, "gauche"), ("Les Démocrates (MoDem)", 37, "centre"), ("Horizons et indépendants", 35, "centre"),
      ("LIOT (indépendants, outre-mer)", 24, "divers"), ("Gauche démocrate et républicaine", 17, "gauche"), ("UDR (alliés du RN)", 17, "rn"), ("Non inscrits", 11, "divers")]
sen = [("Les Républicains", 124, "droite"), ("Union centriste et indépendants", 63, "centre"), ("Socialiste, écologiste et républicain", 62, "gauche"), ("Communiste, républicain, citoyen, écologiste", 18, "gauche"),
       ("RDSE (radicaux)", 18, "centre"), ("RDPI (macronistes)", 16, "centre"), ("Écologiste, solidarité et territoires", 15, "gauche"), ("Union nationale pour les territoires (RN)", 15, "rn"),
       ("Les Indépendants, République et territoires", 14, "droite"), ("Non inscrits", 3, "divers")]
GCOL = {  # couleur par groupe, nuances par bloc
 "La France insoumise": "#b3261e", "Socialistes": "#e34948", "Écologiste et social": "#2e8b57", "Gauche démocrate et républicaine": "#8b1a1a",
 "Ensemble pour la République (macronistes)": "#eda100", "Les Démocrates (MoDem)": "#f4c24d", "Horizons et indépendants": "#d08a00",
 "Droite républicaine (ex-LR)": "#2a78d6", "LIOT (indépendants, outre-mer)": "#898781", "Non inscrits": "#c3c2b7",
 "UDR (alliés du RN)": "#1c4f8a", "Rassemblement national": "#0d366b",
 "Socialiste, écologiste et républicain": "#e34948", "Communiste, républicain, citoyen, écologiste": "#8b1a1a", "Écologiste, solidarité et territoires": "#2e8b57",
 "RDSE (radicaux)": "#f4c24d", "RDPI (macronistes)": "#eda100", "Union centriste et indépendants": "#d08a00",
 "Les Républicains": "#2a78d6", "Les Indépendants, République et territoires": "#6da7ec", "Union nationale pour les territoires (RN)": "#0d366b",
}
# ordre gauche -> droite dans l'hémicycle
an_order = ["La France insoumise", "Gauche démocrate et républicaine", "Écologiste et social", "Socialistes", "LIOT (indépendants, outre-mer)", "Les Démocrates (MoDem)", "Ensemble pour la République (macronistes)", "Horizons et indépendants", "Droite républicaine (ex-LR)", "Non inscrits", "UDR (alliés du RN)", "Rassemblement national"]
sen_order = ["Communiste, républicain, citoyen, écologiste", "Écologiste, solidarité et territoires", "Socialiste, écologiste et républicain", "RDSE (radicaux)", "RDPI (macronistes)", "Union centriste et indépendants", "Les Républicains", "Les Indépendants, République et territoires", "Non inscrits", "Union nationale pour les territoires (RN)"]
an_n = {n: v for n, v, _ in an}; sen_n = {n: v for n, v, _ in sen}

def hemicycle(title, order, counts, total, x, width, vacant=0, subtitle=""):
    """Hémicycle en points : une pastille par siège, rangées concentriques, de gauche à droite."""
    global y
    out.append(f'<text x="{x}" y="{y + 14}" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>')
    if subtitle:
        out.append(f'<text x="{x}" y="{y + 30}" font-size="11.5" fill="{MUTED}">{esc(subtitle)}</text>')
    cx = x + width / 2; R = min(width / 2 - 10, 250); r0 = R * 0.42; cy = y + 44 + R
    seats = total
    # répartir les sièges sur des rangées selon leur longueur d'arc
    rows = 9 if seats > 400 else 7
    radii = [r0 + (R - r0) * i / (rows - 1) for i in range(rows)]
    weights = [math.pi * r for r in radii]; wsum = sum(weights)
    per_row = [max(1, round(seats * w / wsum)) for w in weights]
    diff = seats - sum(per_row); per_row[-1] += diff
    dot = max(3.2, min(5.5, (math.pi * radii[-1] / per_row[-1]) * 0.42))
    # positions triées par angle (gauche = angle pi -> droite = 0)
    pts = []
    for r, n in zip(radii, per_row):
        for k in range(n):
            a = math.pi - math.pi * (k + 0.5) / n
            pts.append((a, cx + r * math.cos(a), cy - r * math.sin(a)))
    pts.sort(key=lambda t: -t[0])
    cols = []
    for g in order:
        cols += [GCOL[g]] * counts.get(g, 0)
    cols += ["#ffffff"] * vacant
    grp = []
    for g in order:
        grp += [g] * counts.get(g, 0)
    grp += ["Siège vacant"] * vacant
    for (a, px, py), c, g in zip(pts, cols, grp):
        stroke = f' stroke="{AXIS}" stroke-width="0.8"' if c == "#ffffff" else ''
        tip = f"{g} : {counts.get(g, 0)} sièges" if g != "Siège vacant" else "Siège vacant"
        out.append(f'<circle class="seat" data-group="{esc(g)}" data-tip="{esc(tip)}" cx="{px:.1f}" cy="{py:.1f}" r="{dot:.1f}" fill="{c}"{stroke}/>')
    out.append(f'<text x="{cx}" y="{cy - 6}" font-size="26" font-weight="700" fill="{INK}" text-anchor="middle">{total}</text>')
    out.append(f'<text x="{cx}" y="{cy + 12}" font-size="11.5" fill="{MUTED}" text-anchor="middle">sièges</text>')
    # légende en deux colonnes
    ly = cy + 26; lx0 = x; colw = width / 2
    for i, g in enumerate(order):
        lx = lx0; yy = ly + i * 18
        lab = f"{g} : {counts.get(g, 0)}"
        out.append(f'<g class="lg" data-group="{esc(g)}"><rect x="{lx - 4}" y="{yy - 3}" width="{width/2}" height="17" fill="transparent"/><rect x="{lx}" y="{yy}" width="11" height="11" rx="2" fill="{GCOL[g]}"/>')
        out.append(f'<text x="{lx + 16}" y="{yy + 9.5}" font-size="11.5" fill="{INK2}">{esc(lab)}</text></g>')
    nrows = len(order)
    if vacant:
        yy = ly + nrows * 18
        out.append(f'<circle cx="{lx0 + 5.5}" cy="{yy + 5.5}" r="5" fill="#ffffff" stroke="{AXIS}"/>')
        out.append(f'<text x="{lx0 + 16}" y="{yy + 9.5}" font-size="11.5" fill="{INK2}">Sièges vacants : {vacant}</text>')
        nrows += 1
    return (ly + nrows * 18 + 8) - y

y0 = y
ha = hemicycle("Assemblée nationale", an_order, an_n, 577, M, half, vacant=3, subtitle="577 sièges, majorité absolue à 289 ; de gauche à droite comme dans l'hémicycle")
y = y0
hb = hemicycle("Sénat", sen_order, sen_n, 348, M + half + 30, half, subtitle="348 sièges, renouvelé pour moitié en septembre 2026 ; majorité absolue à 175")
y = y0 + max(ha, hb) + 8
p("Assemblée : gauche 193, centre 162, Rassemblement national et alliés 138, droite 46 ; personne n'atteint 289. Sénat : Républicains et centristes 187 sur 348. Présidents : Yaël Braun-Pivet, Gérard Larcher.", 13)


# ---------------------------------------------------------------- 12  COÛT ENVIRONNEMENTAL
h2("12. Annexe : ce que ce rapport a coûté à la planète", simple="Faire travailler une intelligence artificielle consomme de l'électricité et de l'eau (pour refroidir les ordinateurs). Ce rapport a demandé environ 1,6 kilowattheure, soit l'équivalent de 10 km en voiture électrique, ou de deux jours d'un réfrigérateur.", sub="Mesure sur toute la session du 7 novembre 2026, essais et corrections compris. Anthropic ne publie pas de chiffre par requête : hypothèses détaillées dans le tableau.")
stat_tiles([
    ("20 millions", "Tokens traités (pondérés)", "1 token ≈ un morceau de mot"),
    ("≈ 1,6 kWh", "Électricité estimée", "fourchette 0,5 à 3 kWh"),
    ("≈ 0,6 kg CO2", "Émissions estimées", "fourchette 0,2 à 1,2 kg"),
    ("≈ 1,5 litre", "Eau de refroidissement", "fourchette 0,5 à 3 litres"),
    ("14", "Sous-agents de recherche", "pages web lues : ~110"),
])
y0 = y
usage = [("Rédaction et raisonnement de l'assistant principal", 3.0), ("Scripts, fichiers, rendu du SVG", 2.1), ("Sous-agents de recherche (lecture de pages)", 11.9), ("Recherche web (requêtes)", 0.7), ("Gestion des tâches, documents, livraison", 1.7), ("Relecture des instructions à chaque tour", 0.8)]
usage = sorted(usage, key=lambda t: -t[1])
h_a = hbar_chart("Où sont allés les tokens (millions, pondérés)", usage, x=M, width=CW, labw=340, fmt=lambda v: f"{v:.1f}".replace(".", ","),
                 note_txt="Pondération : une lecture de contexte déjà en cache compte 0,1, une écriture en cache 2, un token généré 5, par rapport à un token lu normalement. Chiffres bruts : 50,1 millions de lectures en cache, 5,4 millions d'écritures, 842 000 tokens générés, 210 appels au modèle.")
y = y0 + h_a + 8
table(["Poste", "Hypothèse retenue", "Résultat", "D'où vient l'hypothèse"], [
    ["Tokens générés (842 000)", "1 wattheure pour 1 000 tokens générés", "0,84 kWh", "Google (août 2025) : 0,24 Wh par requête Gemini médiane ; Sam Altman (juin 2025) : 0,34 Wh par requête ChatGPT ; une réponse longue de grand modèle est 2 à 4 fois plus coûteuse"],
    ["Tokens écrits en cache (5,4 millions)", "0,05 Wh pour 1 000 tokens", "0,27 kWh", "La lecture d'un texte (« prefill ») coûte environ 10 à 20 fois moins que la génération"],
    ["Tokens relus depuis le cache (50 millions)", "0,01 Wh pour 1 000 tokens", "0,50 kWh", "Le cache évite de recalculer ; coût résiduel de mémoire et de transfert"],
    ["Téléchargements et calculs annexes", "139 Mo (registre HATVP) + ~110 pages web + rendu du SVG", "< 0,02 kWh", "Environ 0,03 kWh par gigaoctet transféré ; calculs locaux négligeables"],
    ["Total électricité", "", "≈ 1,6 kWh", "Incertitude d'un facteur 2 à 3 dans chaque sens"],
    ["Émissions", "0,37 kg CO2 par kWh", "≈ 0,6 kg CO2", "Moyenne du réseau électrique américain, où tournent la plupart des serveurs d'IA ; 0,05 kg/kWh en France, 0,7 en Pologne"],
    ["Eau", "1 litre par kWh", "≈ 1,5 litre", "Google : 0,26 ml par requête de 0,24 Wh (eau de refroidissement sur site)"],
], [2, 2.4, 1.1, 3.5], size=12)
p("Repères : 1,6 kWh = deux jours de réfrigérateur, 50 heures d'ordinateur portable, 10 km en voiture électrique ; 0,6 kg de CO2 = 4 à 5 km en voiture à essence. La version mensuelle automatique visera deux à trois fois moins.", 13)
note("Méthode : comptage des tokens dans le journal de la session (fichiers de transcription de l'assistant et de ses 14 sous-agents), puis application des hypothèses ci-dessus. Sources des ordres de grandeur : Google, « Measuring the environmental impact of AI inference » (août 2025) ; Sam Altman, « The Gentle Singularity » (juin 2025) ; Mistral AI, étude d'impact environnemental (juillet 2025) ; facteur d'émission EPA eGRID pour le réseau américain.")

# ---------------------------------------------------------------- 13  LEXIQUE
h2("13. Lexique", simple="Les mots du rapport, expliqués simplement.")
table(["Terme", "Ce que c'est"], [
    ["Déficit et dette", "Le déficit, c'est ce qui manque chaque année quand l'État dépense plus qu'il ne gagne ; la dette, c'est le total de tout ce qu'il a emprunté pour combler ces déficits (environ 3 500 milliards d'euros, soit 119 % de ce que le pays produit en un an)"],
    ["Amendement", "Une modification proposée à un texte de loi, article par article ; les députés en déposent des dizaines de milliers chaque année"],
    ["Lobby (représentant d'intérêts)", "Une organisation qui cherche à influencer une décision publique pour défendre ses intérêts : entreprise, syndicat, association, cabinet spécialisé"],
    ["Token", "Unité de texte traitée par une intelligence artificielle, à peu près un morceau de mot (un mot français fait environ 1,5 token)"],
    ["Projet de loi / proposition de loi", "Texte du gouvernement (après avis du Conseil d'État) / texte d'un ou plusieurs parlementaires, examiné surtout dans les semaines réservées aux groupes (« niches »)"],
    ["Budget de l'État (projet de loi de finances)", "Première partie = recettes et équilibre, seconde = dépenses par mission. Si la première est rejetée, tout le texte l'est. Délai de 70 jours au Parlement"],
    ["Budget de la Sécu (projet de loi de financement de la Sécurité sociale)", "Maladie, retraites, famille, autonomie, accidents du travail. Délai de 50 jours. Comprend l'objectif de dépenses d'assurance maladie (Ondam)"],
    ["Procédure accélérée", "Décidée par le gouvernement : une seule lecture par chambre avant la commission mixte paritaire"],
    ["Vote conforme", "La seconde chambre adopte le texte sans le modifier : il est définitif"],
    ["Scrutin public", "Vote où la position de chaque parlementaire est enregistrée et publiée"],
    ["Loi spéciale", "Loi minimale autorisant l'État à percevoir les impôts existants quand le budget n'est pas voté au 31 décembre (décembre 2024 et 2025)"],
    ["Groupes à l'Assemblée", "Rassemblement national (121) ; Ensemble pour la République, macronistes (90) ; La France insoumise (70) ; Socialistes (68) ; Droite républicaine, ex-LR (46) ; Écologistes (38) ; Démocrates, MoDem (37) ; Horizons (35) ; LIOT, indépendants et outre-mer (24) ; UDR, alliés de Ciotti (17) ; Gauche démocrate et républicaine, communistes (17) ; non inscrits (11)"],
    ["Groupes au Sénat", "Les Républicains (majoritaires avec l'Union centriste) ; Socialistes ; Union centriste ; RDPI (macronistes) ; RDSE (radicaux) ; Communistes ; Écologistes ; Indépendants"],
    ["Notation financière", "Note des agences (S&P, Moody's, Fitch) sur la capacité de l'État à rembourser ; AAA = meilleure ; A+ ou Aa3 = très bonne mais dégradée ; une « perspective négative » annonce une possible baisse dans les 12 à 24 mois"],
    ["PISA", "Enquête de l'OCDE tous les trois ans sur le niveau des élèves de 15 ans en maths, lecture et sciences"],
], [2.2, 6.8], size=12)

# ---------------------------------------------------------------- 12  SOURCES
h2("14. Sources consultées (7 novembre 2026)")
bullets([
    "Gouvernement : comptes rendus des Conseils des ministres des 1er et 14 octobre (elysee.fr) ; composition du gouvernement : info.gouv.fr (ancien gouvernement.fr), page non lue ce mois-ci, bloquée aux accès automatiques.",
    "Budget de l'État : dossier législatif et scrutin n° 9759 du 4 novembre (assemblee-nationale.fr) ; page « La loi en clair » du Sénat (senat.fr) ; projet de loi de finances de fin de gestion n° 3434 (assemblee-nationale.fr).",
    "Budget de la Sécu : rejet en commission (assemblee-nationale.fr) ; dossier du Sénat (senat.fr/dossier-legislatif/plfss2027).",
    "Textes en navette : dossiers législatifs et scrutins publics du Sénat (senat.fr) et de l'Assemblée nationale (assemblee-nationale.fr).",
    "Activité parlementaire : données ouvertes de l'Assemblée nationale (data.assemblee-nationale.fr), propositions de loi et députés, recalculées le 7 novembre 2026.",
    "Lobbying : répertoire de la Haute Autorité pour la transparence de la vie publique (hatvp.fr), données ouvertes.",
    "Classements : Eurostat (21 octobre 2026) ; OCDE, PISA 2025 ; Commission européenne : rapport sur l'État de droit 2026, tableau de bord de l'innovation 2026 ; OMPI, indice mondial de l'innovation 2025 ; PNUD, rapport 2025 ; FMI, consultation du 22 juillet 2026 ; Agence France Trésor (calendrier des agences de notation).",
    "Les faits du budget et des textes rapportés dans ce rapport avant cette règle viennent en partie d'articles de presse ; ils sont à recouper avec les sources officielles listées ci-dessus lors du prochain rapport.",
], 12)
y += 30


block()
import json
json.dump({"blocks": BLOCKS, "sections": SECBLK, "W": W, "defs": '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>'}, open(os.path.join(ROOT, 'build', 'blocks.json'), 'w'), ensure_ascii=False)
print("blocks", len(BLOCKS), "pairs", sum(1 for b in BLOCKS if b["kind"] == "pair"))

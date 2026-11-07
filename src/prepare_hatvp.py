# -*- coding: utf-8 -*-
"""Calcule les agrégats du répertoire des représentants d'intérêts (HATVP, données ouvertes).
Usage : python3 src/prepare_hatvp.py [chemin/agora.json]   (télécharge le fichier s'il est absent)
Source : https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json (~140 Mo)"""
import json, collections, re, sys, os, urllib.request, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json"
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "build", "agora.json")
if not os.path.exists(path):
    req = urllib.request.Request(URL, headers={"User-Agent": "compte-rendu-mensuel/1.0 (donnees ouvertes)"})
    with urllib.request.urlopen(req) as r, open(path, "wb") as f: f.write(r.read())
pubs = json.load(open(path, encoding="utf-8"))["publications"]
YEARS = ["2021", "2022", "2023", "2024", "2025"]
rows, orgcat = [], {}
for p in pubs:
    name = p["denomination"].strip(); co = p.get("categorieOrganisation") or {}
    orgcat[name] = [co.get("categorie"), co.get("label")]
    for e in p["exercices"]:
        pc = e["publicationCourante"]; yr = pc["dateDebut"][-4:]
        for a in pc.get("activites") or []:
            m = re.match(r"(\d\d)/(\d\d)/(\d{4})", a["publicationCourante"].get("publicationDate") or "")
            rows.append((name, co.get("categorie"), yr, f"{m.group(3)}-{m.group(2)}" if m else None))
def series(org): return {y: sum(1 for r in rows if r[0] == org and r[2] == y) for y in YEARS}
c25 = collections.Counter(r[0] for r in rows if r[2] == "2025")
c25e = collections.Counter(r[0] for r in rows if r[2] == "2025" and r[1] == "ENTREPRISE")
oct26 = collections.Counter(r[0] for r in rows if r[3] == "2026-10")
MOIS_COURANT = datetime.date.today().strftime("%Y-%m")
mois = collections.Counter(r[3] for r in rows if r[3] and "2024-11" <= r[3] < MOIS_COURANT)
out = {
 "totaux": dict(sorted(collections.Counter(r[2] for r in rows).items())),
 "mensuel": sorted(mois.items()),
 "top20": [{"org": o, "cat": orgcat[o][1], "years": series(o), "oct2026": oct26.get(o, 0)} for o, _ in c25.most_common(20)],
 "top20_entreprises": [{"org": o, "cat": orgcat[o][1], "years": series(o), "oct2026": oct26.get(o, 0)} for o, _ in c25e.most_common(20)],
 "top10_octobre_2026": [[o, orgcat[o][1], n] for o, n in oct26.most_common(10)],
}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
meta = lambda desc: {"source": URL, "licence": "Données ouvertes de la HATVP (hatvp.fr)", "genere": datetime.date.today().isoformat(), "description": desc}
def dump(name, desc, data):
    json.dump({"meta": meta(desc), "data": data}, open(os.path.join(ROOT, "data", name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dump("hatvp_totaux_par_annee.json", "Nombre de fiches d'action déclarées par année d'exercice", out["totaux"])
dump("hatvp_publications_par_mois.json", "Fiches publiées par mois (date de publication), depuis novembre 2024", out["mensuel"])
dump("hatvp_top20_organisations.json", "Top 20 des organisations par actions déclarées en 2025, séries 2021-2025", out["top20"])
dump("hatvp_top20_entreprises.json", "Top 20 des entreprises (catégorie ENTREPRISE) par actions déclarées en 2025, séries 2021-2025", out["top20_entreprises"])
dump("hatvp_top10_octobre_2026.json", "Organisations ayant publié le plus de fiches en octobre 2026 : [organisation, catégorie, fiches]", out["top10_octobre_2026"])
dump("hatvp_categories_organisations.json", "Catégorie HATVP de chaque organisation : {nom: [code, libellé]}", orgcat)
print({k: (len(v) if hasattr(v, "__len__") else v) for k, v in out.items()})

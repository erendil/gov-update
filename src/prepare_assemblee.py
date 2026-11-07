# -*- coding: utf-8 -*-
"""Propositions de loi déposées à l'Assemblée nationale (XVIIe législature), par premier signataire.
Sources (données ouvertes de l'Assemblée nationale) :
 - dossiers législatifs : https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs
 - députés et groupes en cours : https://data.assemblee-nationale.fr/acteurs/deputes-en-exercice
Usage : python3 src/prepare_assemblee.py"""
import json, glob, collections, os, io, zipfile, urllib.request, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://data.assemblee-nationale.fr/static/openData/repository/17/"
ZIPS = {"dossiers": B + "loi/dossiers_legislatifs/Dossiers_Legislatifs.json.zip",
        "amo": B + "amo/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes.json.zip"}
work = os.path.join(ROOT, "build", "assemblee"); os.makedirs(work, exist_ok=True)
for k, u in ZIPS.items():
    d = os.path.join(work, k)
    if not os.path.isdir(d):
        req = urllib.request.Request(u, headers={"User-Agent": "compte-rendu-mensuel/1.0 (donnees ouvertes)"})
        zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req).read())).extractall(d)
act, org = {}, {}
for f in glob.glob(f"{work}/amo/json/acteur/*.json"):
    a = json.load(open(f, encoding="utf-8"))["acteur"]; act[a["uid"]["#text"]] = a
for f in glob.glob(f"{work}/amo/json/organe/*.json"):
    o = json.load(open(f, encoding="utf-8"))["organe"]; org[o["uid"]] = o
def mandats(a):
    m = a["mandats"]["mandat"]; return m if isinstance(m, list) else [m]
def groupe(a):
    for x in mandats(a):
        if x.get("typeOrgane") == "GP" and not (x.get("dateFin") and not isinstance(x["dateFin"], dict)):
            return x["organes"]["organeRef"]
def circo(a):
    for x in mandats(a):
        if x.get("typeOrgane") == "ASSEMBLEE": return (x.get("election") or {}).get("lieu", {}).get("departement", "")
cnt, dates = collections.Counter(), []
for f in glob.glob(f"{work}/dossiers/json/document/PIONANR5L17B*.json"):
    d = json.load(open(f, encoding="utf-8"))["document"]
    if not (d.get("denominationStructurelle") or "").startswith("Proposition de loi"): continue
    au = (d.get("auteurs") or {}).get("auteur")
    if not au: continue
    au = au if isinstance(au, list) else [au]
    first = [x for x in au if x.get("acteur", {}).get("qualite") == "auteur"]
    if first:
        cnt[first[0]["acteur"]["acteurRef"]] += 1; dates.append(d["cycleDeVie"]["chrono"]["dateDepot"][:10])
eff, bygrp, rows = collections.Counter(), collections.Counter(), []
for ref, a in act.items():
    g = groupe(a)
    if g: eff[g] += 1
for ref, n in cnt.items():
    a = act.get(ref)
    if a and groupe(a):
        bygrp[groupe(a)] += n
    if a:
        i = a["etatCivil"]["ident"]; rows.append((n, f'{i["prenom"]} {i["nom"]}', org.get(groupe(a), {}).get("libelle"), circo(a)))
    else:
        rows.append((n, None, None, None))      # ancien député, non présent dans le fichier des députés en cours
rows.sort(key=lambda r: (-r[0], r[1] or ""))
meta = {"source": "https://data.assemblee-nationale.fr/travaux-parlementaires/dossiers-legislatifs", "licence": "Données ouvertes de l'Assemblée nationale", "genere": datetime.date.today().isoformat(),
        "periode": f"{min(dates)} au {max(dates)}", "regle": "Propositions de loi (dénomination commençant par « Proposition de loi »), comptées pour leur premier signataire, groupe actuel du député."}
def dump(name, desc, data):
    json.dump({"meta": dict(meta, description=desc), "data": data}, open(os.path.join(ROOT, "data", name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dump("assemblee_propositions_loi_par_groupe.json", "Propositions de loi déposées par groupe politique, avec l'effectif du groupe",
     [{"groupe": org[g]["libelle"], "sigle": org[g]["libelleAbrev"], "deputes": eff[g], "propositions": n, "par_depute": round(n / eff[g], 1)} for g, n in bygrp.most_common()])
dump("assemblee_propositions_loi_top_deputes.json", "Les 20 députés en poste ayant déposé le plus de propositions de loi (premier signataire)",
     [{"rang": i + 1, "depute": r[1], "groupe": r[2], "departement": r[3], "propositions": r[0]} for i, r in enumerate([r for r in rows if r[1]][:20])])
dump("assemblee_propositions_loi_total.json", "Total des propositions de loi, dont celles d'anciens députés non attribuées à un groupe",
     {"total": sum(cnt.values()), "anciens_deputes": sum(r[0] for r in rows if not r[1])})
print(sum(cnt.values()), len(rows))

# -*- coding: utf-8 -*-
import json, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'build', 'blocks.json'), encoding='utf-8'))
PEOPLE = {m.pop('nom'): m for m in json.load(open(os.path.join(ROOT, 'data', 'gouvernement_ministres.json'), encoding='utf-8'))['data']}
W = D["W"]; FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

def svg(body, ya, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {ya:.1f} {W} {h:.1f}" width="{W}" height="{h:.1f}" style="width:100%;height:auto;display:block" font-family="{FONT}" role="img" {extra}>'
            f'{D["defs"]}<rect y="{ya:.1f}" width="{W}" height="{h:.1f}" fill="#fcfcfb"/>{body}</svg>')

def segs_html(segs):
    out, buf = [], []
    for sg in segs:
        if sg[0] == "html": buf.append(sg[1])
        else:
            if buf: out.append('<div class="prose">' + "".join(buf) + '</div>'); buf = []
            out.append('<div class="hint">↔ Faites glisser le schéma de gauche à droite</div>')
            out.append(f'<div class="svgscroll">{svg(sg[1], sg[2], sg[3])}</div>')
    if buf: out.append('<div class="prose">' + "".join(buf) + '</div>')
    return "".join(out)

ASIDE = '<aside class="side"><div class="sidehead"><span>Détail</span><button class="unpin" type="button" hidden title="Fermer">✕</button></div><div class="sidebody"><p class="empty">Survolez ou touchez un élément : son détail s’affiche ici, avec le lien vers la source. Cliquez pour le garder affiché.</p></div></aside>'
parts = []
for i, b in enumerate(D["blocks"]):
    if b["kind"] == "seg":
        body = segs_html(b["segs"])
        has = 'data-detail' in body or 'data-tip' in body
        parts.append(f'<div class="blk{" hasside" if has else ""}" id="blk{i}"><div class="col">{body}</div>' + (ASIDE if has else '') + '</div>')
    else:
        parts.append(f'''<div class="blk hasside pair" id="blk{i}" data-pair="{b["id"]}">
  <div class="pairhead"><span class="ptitle">{html.escape(b["title"])}</span>
    <span class="toggle" role="group" aria-label="Affichage"><button class="on" data-view="diag" type="button">Diagramme</button><button data-view="table" type="button">Tableau</button></span></div>
  <div class="col"><div class="view diag">{segs_html(b["diag"])}</div><div class="view table" hidden>{segs_html(b["table"])}</div></div>{ASIDE}
</div>''')

nav = "".join(f'<a href="#blk{idx}">{html.escape(t.split(".")[0])}<span>{html.escape(t.split(". ",1)[1] if ". " in t else t)}</span></a>' for t, idx in D["sections"])

people_json = json.dumps(PEOPLE, ensure_ascii=False)
PCOL = {'Renaissance': '#eda100', 'Renaissance (ex-LR)': '#eda100', 'MoDem': '#f4c24d', 'Horizons': '#d08a00', 'Les Républicains': '#2a78d6', 'Les Républicains (dissidente)': '#2a78d6', 'Divers droite (ex-LR, ex-Renaissance)': '#6da7ec', 'UDI (centre droit)': '#5598e7', 'Sans parti': '#898781', 'LIOT (indépendants)': '#898781'}
for k, v in PEOPLE.items(): v['col'] = PCOL.get(v['parti'], '#898781'); v['ini'] = ''.join(w[0] for w in k.replace('-', ' ').split() if w[0].isupper())[:2]
page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Actualité gouvernementale — octobre 2026</title>
<style>
  html, body {{ margin: 0; padding: 0; background: #f9f9f7; font-family: {FONT}; }}
  .wrap {{ display: flex; gap: 16px; max-width: 1760px; margin: 0 auto; padding: 0 8px 40px; }}
  main {{ flex: 1 1 auto; max-width: 1540px; min-width: 0; background: #fcfcfb; border: 1px solid #e1e0d9; border-radius: 10px; overflow: hidden; }}
  .blk {{ scroll-margin-top: 12px; }}
  nav.toc {{ position: sticky; top: 12px; align-self: flex-start; width: 200px; flex: 0 0 200px; background: #fcfcfb; border: 1px solid #e1e0d9; border-radius: 8px; padding: 10px 8px; font-size: 12.5px; max-height: calc(100vh - 24px); overflow: auto; }}
  nav.toc h4 {{ margin: 4px 6px 8px; font-size: 12px; color: #898781; text-transform: uppercase; letter-spacing: .04em; }}
  nav.toc a {{ display: flex; gap: 8px; align-items: baseline; padding: 5px 6px; color: #0b0b0b; text-decoration: none; border-radius: 5px; line-height: 1.25; }}
  nav.toc a span {{ color: #52514e; }}
  nav.toc a:hover, nav.toc a.on {{ background: #cde2fb; }}
  nav.toc .all {{ margin: 10px 6px 2px; padding-top: 8px; border-top: 1px solid #e1e0d9; display: flex; gap: 6px; }}
  nav.toc .all button {{ flex: 1; font-size: 11.5px; padding: 4px 6px; border: 1px solid #c3c2b7; background: #fff; border-radius: 5px; cursor: pointer; color: #0b0b0b; }}
  nav.toc .all button:hover {{ background: #cde2fb; }}
  .blk.hasside {{ display: flex; align-items: flex-start; gap: 0; }}
  .blk .col {{ flex: 1 1 320px; min-width: 0; }}
  .blk.pair {{ flex-wrap: wrap; }}
  .blk.pair .pairhead {{ flex: 0 0 100%; box-sizing: border-box; }}
  aside.side {{ flex: 0 0 290px; width: 290px; position: sticky; top: 12px; align-self: flex-start; margin: 12px 12px 12px 0; background: #ffffff; border: 1px solid #c3c2b7; border-radius: 8px; font-size: 12.5px; line-height: 1.45; max-height: calc(100vh - 24px); overflow: auto; }}
  aside.side .sidehead {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; border-bottom: 1px solid #e1e0d9; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: #898781; background: #f3f2ee; border-radius: 8px 8px 0 0; position: sticky; top: 0; }}
  aside.side .sidehead.pinned {{ background: #cde2fb; color: #0b0b0b; }}
  aside.side .unpin {{ border: 0; background: none; cursor: pointer; font-size: 13px; color: #52514e; }}
  aside.side .sidebody {{ padding: 10px 12px; }}
  aside.side .empty {{ color: #898781; margin: 0; }}
  aside.side h4 {{ margin: 0 0 8px; font-size: 14px; color: #0b0b0b; }}
  aside.side dt {{ font-size: 10.5px; text-transform: uppercase; letter-spacing: .04em; color: #898781; margin-top: 7px; }}
  aside.side dd {{ margin: 1px 0 0; }}
  aside.side .src {{ margin-top: 10px; padding-top: 8px; border-top: 1px solid #e1e0d9; }}
  aside.side .src a {{ color: #2a78d6; }}
  #tip {{ display: none !important; }}
  /* ---------- texte HTML ---------- */
  .prose {{ max-width: 880px; padding: 4px 28px; font-size: 16px; line-height: 1.6; color: #0b0b0b; }}
  .prose h2.sec {{ margin: 34px 0 12px; font-size: 24px; line-height: 1.25; padding-left: 14px; border-left: 6px solid #2a78d6; scroll-margin-top: 16px; }}
  .prose h3 {{ margin: 22px 0 6px; font-size: 18px; }}
  .prose p {{ margin: 0 0 12px; }}
  .prose p.note {{ font-size: 13px; color: #6b6a65; }}
  .prose p.muted, .prose p.sub {{ color: #52514e; font-size: 15px; }}
  .prose ul {{ margin: 0 0 12px; padding-left: 22px; }} .prose li {{ margin: 0 0 6px; }}
  .clair {{ background: #e5f4e4; border-radius: 8px; padding: 10px 14px; margin: 0 0 14px; display: flex; gap: 14px; align-items: baseline; }}
  .clair b {{ color: #006300; font-size: 12.5px; letter-spacing: .04em; flex: 0 0 auto; }} .clair p {{ margin: 0; }}
  header.top h1 {{ margin: 24px 0 4px; font-size: 34px; line-height: 1.15; }}
  header.top .lead {{ font-size: 20px; color: #52514e; margin: 0 0 6px; }} header.top .meta {{ font-size: 13px; color: #898781; }}
  .how {{ background: #cde2fb; border-radius: 8px; padding: 12px 16px; margin: 12px 0 6px; }} .how p {{ margin: 4px 0 0; font-size: 15px; }}
  .tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 0 0 14px; }}
  .tile {{ border: 1px solid #e1e0d9; background: #fff; border-radius: 8px; padding: 10px 14px; display: flex; flex-direction: column; gap: 2px; }}
  .tile .tl {{ font-size: 12.5px; color: #52514e; }} .tile .tv {{ font-size: 28px; font-weight: 700; line-height: 1.2; }} .tile .ts {{ font-size: 11.5px; color: #898781; }}
  .tblwrap {{ overflow-x: auto; margin: 0 0 14px; }}
  table.rt {{ border-collapse: collapse; width: 100%; font-size: 14px; line-height: 1.45; table-layout: fixed; }}
  table.rt th {{ background: #cde2fb; text-align: left; padding: 8px 10px; font-size: 13px; }}
  table.rt td {{ padding: 8px 10px; border-bottom: 1px solid #e1e0d9; vertical-align: top; overflow-wrap: anywhere; }}
  table.rt td.first {{ font-weight: 600; }} table.rt tr:nth-child(even) td {{ background: #f6f5f1; }}
  table.rt tr.det {{ cursor: pointer; }} table.rt tr.det:hover td, table.rt tr.det.sel td {{ background: #dbe9fb; }}
  .svgscroll {{ overflow-x: auto; }} .hint {{ display: none; font-size: 12px; color: #898781; padding: 4px 16px 0; }}
  @media (max-width: 1099px) {{ .hint {{ display: block; }} .help {{ display: none; }} }}
  #tocbtn {{ display: none; position: fixed; left: 10px; top: 10px; z-index: 40; border: 1px solid #c3c2b7; background: #fff; border-radius: 8px; padding: 8px 12px; font: 600 14px system-ui; box-shadow: 0 2px 8px rgba(0,0,0,.12); cursor: pointer; }}
  #scrim {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,.35); z-index: 38; }}
  @media (max-width: 1699px) {{
    nav.toc {{ position: fixed; top: 0; left: 0; bottom: 0; width: min(86vw, 330px); max-height: none; border-radius: 0 10px 10px 0; z-index: 39; transform: translateX(-102%); transition: transform .2s; font-size: 15px; }}
    nav.toc a {{ padding: 9px 8px; }}
    body.tocopen nav.toc {{ transform: none; }} body.tocopen #scrim {{ display: block; }}
    #tocbtn {{ display: block; }} .wrap {{ padding: 52px 8px 40px; }} .wrap > nav.toc {{ flex: none; }}
  }}
  @media (max-width: 1099px) {{
    .svgscroll svg {{ min-width: 960px; }}
    aside.side {{ position: fixed; left: 0; right: 0; bottom: 0; top: auto; width: auto; flex: none; margin: 0; max-height: 48vh; border-radius: 14px 14px 0 0; border-width: 1px 0 0; z-index: 30; box-shadow: 0 -6px 24px rgba(0,0,0,.2); font-size: 14.5px; display: none; }}
    aside.side.open {{ display: block; }} aside.side .unpin {{ display: inline-block !important; font-size: 18px; padding: 2px 8px; }}
    aside.side .sidehead {{ border-radius: 14px 14px 0 0; }}
    .prose {{ padding: 4px 16px; font-size: 16.5px; }}
    .pairhead {{ padding: 10px 14px 0; flex-wrap: wrap; }}
  }}
  @media (max-width: 700px) {{
    .prose h2.sec {{ font-size: 21px; }} header.top h1 {{ font-size: 27px; }} .clair {{ flex-direction: column; gap: 2px; }}
    table.rt, table.rt tbody, table.rt tr, table.rt td {{ display: block; width: 100% !important; }}
    table.rt thead, table.rt colgroup {{ display: none; }}
    table.rt tr {{ border: 1px solid #e1e0d9; border-radius: 8px; margin: 0 0 10px; background: #fff; overflow: hidden; }}
    table.rt td {{ border: 0; padding: 6px 12px; background: none !important; }}
    table.rt td::before {{ content: attr(data-label); display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: #898781; }}
    table.rt td.first {{ background: #f3f2ee !important; font-size: 15px; }}
  }}
  .pairhead {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 12px 56px 0; }}
  .ptitle {{ font-size: 15px; font-weight: 700; color: #0b0b0b; }}
  .toggle {{ display: inline-flex; border: 1px solid #c3c2b7; border-radius: 6px; overflow: hidden; }}
  .toggle button {{ border: 0; background: #fff; padding: 5px 12px; font-size: 12.5px; cursor: pointer; color: #52514e; font-family: inherit; }}
  .toggle button.on {{ background: #2a78d6; color: #fff; }}
  .toggle button:not(.on):hover {{ background: #cde2fb; color: #0b0b0b; }}
  #tip {{ position: fixed; pointer-events: none; background: #0b0b0b; color: #f0efec; font-size: 13px; padding: 7px 10px; border-radius: 6px; max-width: 340px; line-height: 1.35; opacity: 0; transition: opacity .12s; z-index: 10; box-shadow: 0 4px 14px rgba(0,0,0,.18); }}
  svg .seat, svg .lg, svg .step, svg .guard, svg .stepcell, svg .bar, svg .pt, svg .card {{ cursor: pointer; }}
  svg .seat {{ transition: opacity .15s; }}
  svg.dim .seat {{ opacity: .15; }}
  svg.dim .seat.on {{ opacity: 1; }}
  svg .step rect, svg .guard rect, svg .card rect {{ transition: stroke-width .15s, filter .15s; }}
  svg .step:hover rect, svg .step.on rect, svg .card:hover rect:first-child {{ stroke-width: 3; filter: drop-shadow(0 2px 6px rgba(42,120,214,.45)); }}
  svg .guard:hover rect {{ stroke-width: 2.4; }}
  svg .stepcell rect:first-child {{ transition: fill .15s; }}
  svg .stepcell:hover rect:first-child, svg .stepcell.on rect:first-child {{ fill: #cde2fb !important; }}
  svg .stepcell.on circle {{ stroke-width: 4; }}
  svg .bar:hover, svg .pt:hover {{ filter: brightness(1.15); }}
  svg .lg:hover text {{ font-weight: 700; }}
  svg .person {{ cursor: pointer; }}
  svg .person:hover rect:first-child {{ stroke-width: 2.6; filter: drop-shadow(0 2px 6px rgba(42,120,214,.35)); }}
  svg .pmask {{ display: none; }}
  body.quiz svg .pname {{ display: none; }}
  body.quiz svg .pmask {{ display: inline; }}
  body.quiz svg .person.revealed .pname {{ display: inline; }}
  body.quiz svg .person.revealed .pmask {{ display: none; }}
  #fiche {{ position: fixed; right: 16px; bottom: 16px; width: 360px; max-width: calc(100vw - 32px); background: #fcfcfb; border: 1px solid #c3c2b7; border-radius: 10px; box-shadow: 0 8px 28px rgba(0,0,0,.18); padding: 14px 16px 12px; z-index: 20; display: none; font-size: 13px; line-height: 1.4; }}
  #fiche.on {{ display: block; }}
  #fiche .close {{ position: absolute; right: 8px; top: 6px; border: 0; background: none; font-size: 18px; cursor: pointer; color: #52514e; }}
  #fiche .head {{ display: flex; gap: 12px; align-items: center; margin-bottom: 8px; }}
  #fiche .medal {{ width: 46px; height: 46px; border-radius: 50%; color: #fff; font-weight: 700; font-size: 17px; display: flex; align-items: center; justify-content: center; flex: 0 0 46px; }}
  #fiche h3 {{ margin: 0; font-size: 16px; }}
  #fiche .role {{ color: #52514e; font-size: 12.5px; }}
  #fiche .tag {{ display: inline-block; font-size: 11px; padding: 2px 7px; border-radius: 10px; background: #e5f4e4; color: #006300; margin: 2px 6px 6px 0; }}
  #fiche p {{ margin: 6px 0; }}
  #fiche p b {{ color: #2a78d6; }}
  #fiche a {{ color: #2a78d6; }}
  #fiche .nav {{ display: flex; justify-content: space-between; margin-top: 8px; }}
  #fiche .nav button {{ border: 1px solid #c3c2b7; background: #fff; border-radius: 5px; padding: 3px 9px; cursor: pointer; font-size: 12px; }}
  nav.toc .quiz {{ margin: 6px 6px 2px; display: flex; gap: 6px; }}
  nav.toc .quiz button {{ flex: 1; font-size: 11.5px; padding: 4px 6px; border: 1px solid #c3c2b7; background: #fff; border-radius: 5px; cursor: pointer; color: #0b0b0b; }}
  nav.toc .quiz button.on {{ background: #fab219; }}
  svg .det {{ cursor: pointer; }}
  svg .det:hover > rect:first-child {{ fill: rgba(42,120,214,.08) !important; }}
  svg .det.sel > rect:first-child {{ fill: rgba(42,120,214,.16) !important; }}
  svg circle.det.sel {{ stroke: #0b0b0b !important; stroke-width: 2.5 !important; }}
  #detail {{ position: fixed; right: 16px; bottom: 16px; width: 400px; max-width: calc(100vw - 32px); max-height: calc(100vh - 32px); overflow: auto; background: #fcfcfb; border: 1px solid #c3c2b7; border-radius: 10px; box-shadow: 0 8px 28px rgba(0,0,0,.18); padding: 14px 16px 12px; z-index: 21; display: none; font-size: 13px; line-height: 1.45; }}
  #detail.on {{ display: block; }}
  #detail .close {{ position: absolute; right: 8px; top: 6px; border: 0; background: none; font-size: 18px; cursor: pointer; color: #52514e; }}
  #detail h3 {{ margin: 0 24px 8px 0; font-size: 15px; }}
  #detail dl {{ margin: 0; display: grid; grid-template-columns: 1fr; gap: 6px; }}
  #detail dt {{ font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: #898781; }}
  #detail dd {{ margin: 0 0 4px; }}
  #detail .src {{ margin-top: 10px; padding-top: 8px; border-top: 1px solid #e1e0d9; font-size: 12.5px; }}
  #detail .src a {{ color: #2a78d6; word-break: break-all; }}
  .help {{ max-width: 1240px; margin: 8px auto 0; padding: 0 8px; font-size: 12.5px; color: #52514e; }}
</style>
</head>
<body>
<div class="help">Interactif : survolez un élément d'un diagramme (carte, barre, point, pastille, ligne de tableau) et son détail s'affiche dans l'encadré à droite, avec un lien vers la source ; cliquez pour le garder affiché ; chaque diagramme a un bouton « Tableau » ; survolez les cartes, pastilles, barres et points pour le détail ; survolez une étape du schéma (section 10) pour retrouver les textes qui en sont là ; un clic fige la sélection.</div>
<button id="tocbtn" type="button" aria-label="Ouvrir le sommaire">☰ Sommaire</button><div id="scrim"></div>
<div class="wrap">
<main>
{"".join(parts)}
</main>
<nav class="toc"><h4>Sommaire</h4>{nav}<div class="all"><button type="button" data-all="diag">Tout en diagrammes</button><button type="button" data-all="table">Tout en tableaux</button></div><div class="quiz"><button type="button" id="quizbtn">Qui est-ce ? (cacher les noms des ministres)</button></div></nav>
</div>
<div id="tip"></div>

<div id="fiche" role="dialog" aria-live="polite"><button class="close" type="button" aria-label="Fermer">×</button>
  <div class="head"><div class="medal"></div><div><h3></h3><div class="role"></div></div></div>
  <div class="tags"></div>
  <p class="parcours"></p>
  <p class="octobre"></p>
  <p class="lien"></p>
  <div class="nav"><button type="button" data-dir="-1">◀ précédent</button><span class="count"></span><button type="button" data-dir="1">suivant ▶</button></div>
</div>
<script>const PEOPLE = {people_json};</script>
<script>
window.initReport = function(PEOPLE){{
  if (window.__cleanup) window.__cleanup();
  const tip = document.getElementById('tip');
  // Bascule diagramme / tableau
  const setView = (pair, v) => {{
    pair.querySelectorAll('.view').forEach(d => d.hidden = !d.classList.contains(v));
    pair.querySelectorAll('.toggle button').forEach(b => b.classList.toggle('on', b.dataset.view === v));
  }};
  document.querySelectorAll('.pair').forEach(pair => pair.querySelectorAll('.toggle button').forEach(b => b.addEventListener('click', () => setView(pair, b.dataset.view))));
  document.querySelectorAll('nav.toc [data-all]').forEach(b => b.addEventListener('click', () => document.querySelectorAll('.pair').forEach(p => setView(p, b.dataset.all))));
  // Sommaire : section courante
  const anchors = [...document.querySelectorAll('nav.toc a')];
  const onScroll = () => {{
    let cur = null;
    anchors.forEach(a => {{ const el = document.querySelector(a.getAttribute('href')); if (el && el.getBoundingClientRect().top - 60 <= 0) cur = a; }});
    anchors.forEach(a => a.classList.toggle('on', a === cur));
  }};
  window.addEventListener('scroll', onScroll, {{passive: true}}); onScroll();
  const onKey = e => {{ if (e.key === 'Escape') {{ fiche.classList.remove('on'); }} }};
  window.__cleanup = () => {{ window.removeEventListener('scroll', onScroll); document.removeEventListener('keydown', onKey); }};
  // Panneau latéral : survol = aperçu, clic = verrouillage
  const escH = t => String(t).replace(/[&<>"]/g, c => ({{'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}}[c]));
  const render = (aside, el0) => {{
    const el = el0.closest('[data-detail]') || el0;
    const body = aside.querySelector('.sidebody');
    let d = null; try {{ d = el.dataset.detail ? JSON.parse(el.dataset.detail) : null; }} catch (e) {{}}
    if (d) {{
      const host = d.source ? d.source.replace(/^https?:[/][/](www[.])?/, '').split('/')[0] : '';
      body.innerHTML = '<h4>' + escH(d.titre) + '</h4><dl>' + d.champs.map(([k, v]) => '<dt>' + escH(k) + '</dt><dd>' + escH(v) + '</dd>').join('') + '</dl>' +
        (d.source ? '<div class="src">Source : <a href="' + d.source + '" target="_blank" rel="noopener">' + escH(host) + ' ↗</a><br><span style="color:#898781">Pour aller plus loin, ouvrir la page d’origine.</span></div>' : '');
    }} else if (el.dataset.tip) {{
      body.innerHTML = '<p>' + escH(el.dataset.tip) + '</p>';
    }}
  }};
  document.querySelectorAll('.blk.hasside').forEach(blk => {{
    const aside = blk.querySelector('aside.side'); if (!aside) return;
    const head = aside.querySelector('.sidehead'); const unpin = aside.querySelector('.unpin');
    let pinnedEl = null;
    const setPin = el => {{
      if (pinnedEl) pinnedEl.classList.remove('sel');
      pinnedEl = el; unpin.hidden = !el; head.classList.toggle('pinned', !!el);
      head.firstElementChild.textContent = el ? 'Détail (gardé affiché)' : 'Détail';
      aside.classList.toggle('open', !!el);
      if (el) {{ el.classList.add('sel'); render(aside, el); }}
    }};
    blk.querySelectorAll('[data-detail], [data-tip]').forEach(el => {{
      el.addEventListener('mouseenter', () => {{ if (!pinnedEl) render(aside, el); }});
      el.addEventListener('click', e => {{ e.stopPropagation(); const t = el.closest('[data-detail]') || el; setPin(pinnedEl === t ? null : t); if (!pinnedEl) render(aside, t); }});
      el.addEventListener('touchstart', () => {{ if (!pinnedEl) render(aside, el); }}, {{passive: true}});
    }});
    unpin.addEventListener('click', () => setPin(null));
    blk.addEventListener('click', e => {{ if (pinnedEl && !e.target.closest('[data-detail], [data-tip], aside')) setPin(null); }});
  }});
  const tb = document.getElementById('tocbtn');
  const closeToc = () => document.body.classList.remove('tocopen');
  tb.addEventListener('click', () => document.body.classList.toggle('tocopen'));
  document.getElementById('scrim').addEventListener('click', closeToc);
  document.querySelectorAll('nav.toc a').forEach(a => a.addEventListener('click', closeToc));
  // Fiches des ministres
  const fiche = document.getElementById('fiche'); const names = Object.keys(PEOPLE); let cur = -1;
  const openFiche = name => {{
    const p = PEOPLE[name]; if (!p) return; cur = names.indexOf(name);
    fiche.querySelector('.medal').style.background = p.col; fiche.querySelector('.medal').textContent = p.ini;
    fiche.querySelector('h3').textContent = name; fiche.querySelector('.role').textContent = p.role;
    fiche.querySelector('.tags').innerHTML = '<span class="tag">' + p.parti + '</span>' + (p.ne ? '<span class="tag">né(e) en ' + p.ne + ', ' + (2026 - p.ne) + ' ans</span>' : '');
    fiche.querySelector('.parcours').innerHTML = '<b>Parcours.</b> ' + p.parcours;
    fiche.querySelector('.octobre').innerHTML = '<b>En octobre.</b> ' + p.octobre;
    fiche.querySelector('.lien').innerHTML = '<a href="' + p.url + '" target="_blank" rel="noopener">Site officiel du gouvernement (composition) ↗</a>';
    fiche.querySelector('.count').textContent = (cur + 1) + ' / ' + names.length;
    fiche.classList.add('on');
    document.querySelectorAll('svg .person').forEach(el => {{ if (el.dataset.person === name) el.classList.add('revealed'); }});
  }};
  document.querySelectorAll('svg .person').forEach(el => el.addEventListener('click', () => openFiche(el.dataset.person)));
  fiche.querySelector('.close').addEventListener('click', () => fiche.classList.remove('on'));
  fiche.querySelectorAll('.nav button').forEach(b => b.addEventListener('click', () => openFiche(names[(cur + parseInt(b.dataset.dir) + names.length) % names.length])));
  document.addEventListener('keydown', onKey);
  // Mode quiz : cacher les noms, les révéler au clic
  const qb = document.getElementById('quizbtn');
  qb.addEventListener('click', () => {{
    const on = document.body.classList.toggle('quiz'); qb.classList.toggle('on', on);
    document.querySelectorAll('svg .person').forEach(el => el.classList.remove('revealed'));
    qb.textContent = on ? 'Quiz en cours : cliquez sur un ministre pour révéler son nom (cliquer ici pour arrêter)' : 'Qui est-ce ? (cacher les noms des ministres)';
    if (on) {{ const org = document.querySelector('svg .person'); if (org) org.closest('.blk').scrollIntoView({{behavior: 'smooth'}}); }}
  }});
}};
initReport(PEOPLE);
</script>
</body>
</html>
'''
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'build', 'rapport.html')
open(OUT, 'w', encoding='utf-8').write(page)
print(len(page))

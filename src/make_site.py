# -*- coding: utf-8 -*-
"""Assemble LA page unique du site : site/index.html, avec un menu d'historique par année et par mois.
Chaque rapport mensuel complet est conservé dans archive/AAAA-MM.html (produit par make_html.py).
Usage : python3 src/make_site.py [AAAA-MM chemin/rapport.html]   (ajoute ou remplace ce mois, puis reconstruit la page)"""
import sys, re, os, glob, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
os.makedirs(os.path.join(ROOT, "archive"), exist_ok=True)
if len(sys.argv) == 3:
    open(os.path.join(ROOT, "archive", sys.argv[1] + ".html"), "w", encoding="utf-8").write(open(sys.argv[2], encoding="utf-8").read())
files = sorted(glob.glob(os.path.join(ROOT, "archive", "*.html")))
keys = [os.path.basename(f)[:-5] for f in files]
pages = {k: open(f, encoding="utf-8").read() for k, f in zip(keys, files)}
latest = keys[-1]
css = re.search(r"<style>(.*?)</style>", pages[latest], re.S).group(1)
tpls, people, titles = [], {}, {}
for k, s in pages.items():
    body = s[s.index("<body>") + 6: s.index("<script>const PEOPLE")]
    people[k] = json.loads(re.search(r"const PEOPLE = (.*?);</script>", s, re.S).group(1))
    titles[k] = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).strip()
    tpls.append(f'<template id="t-{k}">{body}</template>')
script = re.search(r"<script>\s*window\.initReport = .*?\n};\n", pages[latest], re.S).group(0)[len("<script>"):]
data = json.dumps({"titles": titles, "mois": MOIS, "years": sorted({k[:4] for k in keys}, reverse=True), "keys": keys, "people": people}, ensure_ascii=False).replace("</", "<\\/")
page = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compte rendu mensuel : gouvernement et Parlement</title>
<meta name="description" content="Chaque mois, ce qui s'est passé au gouvernement, à l'Assemblée nationale et au Sénat, expliqué simplement. Sources officielles uniquement.">
<style>{css}
  #histbar {{ position: sticky; top: 0; z-index: 50; background: #fff; border-bottom: 1px solid #e1e0d9; display: flex; align-items: center; gap: 12px; padding: 6px 12px; font: 14px system-ui, sans-serif; }}
  #histbar b {{ flex: 1; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  #histbtn {{ border: 1px solid #c3c2b7; background: #fff; border-radius: 8px; padding: 6px 12px; font: 600 14px system-ui; cursor: pointer; }}
  #histpanel {{ display: none; position: fixed; top: 46px; right: 8px; z-index: 60; width: min(420px, calc(100vw - 16px)); background: #fff; border: 1px solid #c3c2b7; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.2); padding: 12px; max-height: 80vh; overflow: auto; font: 14px system-ui, sans-serif; }}
  #histpanel.on {{ display: block; }}
  #histpanel .yt {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }}
  #histpanel .yt button {{ font: inherit; padding: 4px 14px; border: 1px solid #e1e0d9; background: #fff; border-radius: 999px; cursor: pointer; }}
  #histpanel .yt button[aria-pressed=true] {{ background: #cde2fb; border-color: #2a78d6; font-weight: 700; }}
  #histpanel .mg {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
  #histpanel .mg a, #histpanel .mg span {{ padding: 9px 6px; border: 1px solid #e1e0d9; border-radius: 8px; text-align: center; text-transform: capitalize; text-decoration: none; color: #0b0b0b; }}
  #histpanel .mg a:hover, #histpanel .mg a.cur {{ background: #cde2fb; border-color: #2a78d6; }}
  #histpanel .mg span {{ color: #b0afa8; border-style: dashed; }}
  nav.toc {{ top: 58px; max-height: calc(100vh - 70px); }} aside.side {{ top: 58px; max-height: calc(100vh - 70px); }}
  #tocbtn {{ top: 56px; }}
  @media (max-width: 1699px) {{ nav.toc {{ top: 45px; max-height: none; }} .help {{ display: none; }} }}
  @media (max-width: 1099px) {{ aside.side {{ top: auto; max-height: 48vh; }} }}
</style></head>
<body>
<div id="histbar"><b id="histtitle"></b><button id="histbtn" type="button" aria-expanded="false">☰ Historique</button></div>
<div id="histpanel" role="dialog" aria-label="Historique des rapports"><div class="yt" id="hy"></div><div class="mg" id="hm"></div></div>
<div id="rpt"></div>
{"".join(tpls)}
<script>const SITE = {data};</script>
<script>
{script}
(function(){{
  const rpt = document.getElementById('rpt'), panel = document.getElementById('histpanel'), btn = document.getElementById('histbtn');
  let year = null;
  const lab = k => SITE.mois[+k.slice(5) - 1] + ' ' + k.slice(0, 4);
  function drawPanel(cur) {{
    year = year || cur.slice(0, 4);
    const hy = document.getElementById('hy'); hy.innerHTML = '';
    SITE.years.forEach(y => {{ const b = document.createElement('button'); b.textContent = y; b.setAttribute('aria-pressed', y === year); b.onclick = () => {{ year = y; drawPanel(cur); }}; hy.appendChild(b); }});
    document.getElementById('hm').innerHTML = SITE.mois.map((m, i) => {{ const k = year + '-' + String(i + 1).padStart(2, '0'); return SITE.keys.includes(k) ? '<a href="#' + k + '"' + (k === cur ? ' class="cur"' : '') + '>' + m + '</a>' : '<span>' + m + '</span>'; }}).join('');
  }}
  function show(k) {{
    if (!SITE.keys.includes(k)) k = SITE.keys[SITE.keys.length - 1];
    rpt.innerHTML = ''; rpt.appendChild(document.getElementById('t-' + k).content.cloneNode(true));
    document.body.classList.remove('quiz', 'tocopen');
    initReport(SITE.people[k]);
    document.getElementById('histtitle').textContent = 'Compte rendu : ' + lab(k);
    document.title = SITE.titles[k]; drawPanel(k); panel.classList.remove('on'); btn.setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0);
  }}
  btn.addEventListener('click', () => {{ const on = panel.classList.toggle('on'); btn.setAttribute('aria-expanded', on); }});
  document.addEventListener('click', e => {{ if (!e.target.closest('#histpanel, #histbtn')) panel.classList.remove('on'); }});
  window.addEventListener('hashchange', () => {{ if (/^#\\d{{4}}-\\d{{2}}$/.test(location.hash)) show(location.hash.slice(1)); }});
  show(/^#\\d{{4}}-\\d{{2}}$/.test(location.hash) ? location.hash.slice(1) : SITE.keys[SITE.keys.length - 1]);
}})();
</script></body></html>'''
os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
open(os.path.join(ROOT, "site", "index.html"), "w", encoding="utf-8").write(page)
print("rapports", keys, len(page))

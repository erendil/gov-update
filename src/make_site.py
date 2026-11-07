# -*- coding: utf-8 -*-
"""Assemble le site : rapports/AAAA-MM.html + index.html (historique par année et par mois).
Usage : python3 make_site.py AAAA-MM chemin_du_rapport.html   (ajoute/remplace ce mois puis régénère tout)"""
import sys, re, glob, os, json, html
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def lab(k): return f"{MOIS[int(k[5:])-1]} {k[:4]}"
def bar(k, keys):
    i = keys.index(k)
    prev = f'<a href="{keys[i-1]}.html">‹ {lab(keys[i-1])}</a>' if i > 0 else '<span></span>'
    nxt = f'<a href="{keys[i+1]}.html">{lab(keys[i+1])} ›</a>' if i < len(keys)-1 else '<span></span>'
    return ('<!--histbar--><nav class="histbar" style="display:flex;justify-content:space-between;gap:12px;align-items:center;max-width:1760px;margin:0 auto;padding:8px 14px;font:14px system-ui,sans-serif">'
            f'{prev}<a href="../index.html" style="font-weight:700">☰ Historique des rapports</a>{nxt}</nav><!--/histbar-->')
if len(sys.argv) == 3:
    k, src = sys.argv[1], sys.argv[2]
    open(f'{SITE}/rapports/{k}.html', 'w', encoding='utf-8').write(open(src, encoding='utf-8').read())
files = sorted(glob.glob(f'{SITE}/rapports/*.html'))
keys = [os.path.basename(f)[:-5] for f in files]
reports = {}
for f, k in zip(files, keys):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!--histbar-->.*?<!--/histbar-->', '', s, flags=re.S)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + bar(k, keys), s, count=1)
    open(f, 'w', encoding='utf-8').write(s)
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    reports[k] = html.unescape(t.group(1)).strip() if t else lab(k)
years = sorted({k[:4] for k in keys} | {str(__import__('datetime').date.today().year)}, reverse=True)
data = json.dumps({"reports": reports, "years": years, "mois": MOIS}, ensure_ascii=False)
page = '''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compte rendu mensuel : gouvernement et Parlement</title>
<meta name="description" content="Chaque mois, ce qui s'est passé au gouvernement, à l'Assemblée nationale et au Sénat, expliqué simplement.">
<style>
:root{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--line:#e1e0d9;--blue:#2a78d6;--soft:#cde2fb;--surf:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:900px;margin:0 auto;padding:28px 16px 60px}
h1{font-size:28px;line-height:1.2;margin:0 0 8px}.lead{color:var(--ink2);margin:0 0 20px}
.last{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;padding:10px 16px;border-radius:8px;font-weight:600;margin-bottom:26px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
.tabs button{font:inherit;padding:6px 16px;border:1px solid var(--line);background:var(--surf);border-radius:999px;cursor:pointer;color:var(--ink)}
.tabs button[aria-pressed=true]{background:var(--soft);border-color:var(--blue);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.m{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--surf);min-height:78px;text-decoration:none;color:var(--ink);display:block}
a.m:hover,a.m:focus-visible{border-color:var(--blue);background:var(--soft)}
.m b{display:block;text-transform:capitalize}.m span{font-size:13px;color:var(--ink2)}
.m.off{background:transparent;color:var(--muted);border-style:dashed}.m.off span{color:var(--muted)}
footer{margin-top:34px;color:var(--muted);font-size:13px}
</style></head><body><main>
<h1>Compte rendu mensuel : gouvernement et Parlement</h1>
<p class="lead">Chaque mois : les décisions du gouvernement, les lois en discussion, qui les propose, et la place de la France dans les classements internationaux. Écrit pour être compris dès 14 ans.</p>
<a id="last" class="last" href="#">Lire le dernier rapport</a>
<div class="tabs" id="tabs" role="group" aria-label="Choisir une année"></div>
<div class="grid" id="grid"></div>
<footer>Un nouveau rapport est publié au début de chaque mois. Les mois sans lien n’ont pas été produits. Sources : sites officiels (assemblee-nationale.fr, senat.fr, vie-publique.fr, hatvp.fr) et classements internationaux, citées dans chaque rapport.</footer>
</main><script>
const D=__DATA__;const R=D.reports,keys=Object.keys(R).sort();
const last=keys[keys.length-1];document.getElementById('last').href='rapports/'+last+'.html';
document.getElementById('last').textContent='Lire le dernier rapport : '+D.mois[+last.slice(5)-1]+' '+last.slice(0,4);
const tabs=document.getElementById('tabs'),grid=document.getElementById('grid');
function show(y){tabs.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.y===y));
 grid.innerHTML=D.mois.map((n,i)=>{const k=y+'-'+String(i+1).padStart(2,'0');
  return R[k]?'<a class="m" href="rapports/'+k+'.html"><b>'+n+'</b><span>Lire le rapport</span></a>':'<div class="m off"><b>'+n+'</b><span>pas de rapport</span></div>'}).join('')}
D.years.forEach(y=>{const b=document.createElement('button');b.textContent=y;b.dataset.y=y;b.onclick=()=>show(y);tabs.appendChild(b)});
show(last.slice(0,4));
</script></body></html>'''.replace('__DATA__', data)
open(f'{SITE}/index.html', 'w', encoding='utf-8').write(page)
print('rapports', keys)

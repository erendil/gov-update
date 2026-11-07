# -*- coding: utf-8 -*-
"""Génère le compte rendu d'octobre 2026 en un seul fichier SVG."""
import html, json, re

W = 1240
M = 56           # marge
CW = W - 2 * M   # largeur utile
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; AXIS = "#c3c2b7"; SURF = "#fcfcfb"; PLANE = "#f9f9f7"
BLUE = "#2a78d6"; ORANGE = "#eb6834"; AQUA = "#1baf7a"; RED = "#e34948"
GOOD = "#0ca30c"; CRIT = "#d03b3b"; WARN = "#fab219"
BLUE_L = "#cde2fb"; ROWALT = "#f3f2ee"

out = []
y = 0  # curseur vertical
SECTIONS = []


def esc(s):
    return html.escape(s, quote=True)


def text_width(s, size):
    # estimation de largeur pour une sans-serif : ~0.5 em par caractère, moins pour les fins
    w = 0
    for c in s:
        if c in "iljtf.,;:'|!I ":
            w += 0.33
        elif c in "mwMW":
            w += 0.90
        elif c.isupper() or c.isdigit():
            w += 0.68
        else:
            w += 0.57
    return w * size


def wrap(s, size, width):
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(t, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rich(s):
    """**gras** -> tspan bold ; retourne du SVG inline."""
    parts = s.split("**")
    res = ""
    for i, p in enumerate(parts):
        if i % 2 == 1:
            res += f'<tspan font-weight="600">{esc(p)}</tspan>'
        else:
            res += esc(p)
    return res


def para(x, yy, width, s, size=14, color=INK, lh=None, weight="400"):
    lh = lh or round(size * 1.45)
    lines = wrap(s, size, width)
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{yy + lh * (i + 1) - round(size*0.3)}" font-size="{size}" fill="{color}" font-weight="{weight}">{rich(ln)}</text>')
    return lh * len(lines)


def h1(s):
    global y
    y += 10
    out.append(f'<text x="{M}" y="{y + 30}" font-size="30" font-weight="700" fill="{INK}">{esc(s)}</text>')
    y += 44


def _s_h2(s, sub=None, simple=None):
    global y
    y += 26
    SECTIONS.append((s, y))
    out.append(f'<g id="sec{len(SECTIONS)}"></g>')
    out.append(f'<rect x="{M}" y="{y}" width="6" height="26" rx="2" fill="{BLUE}"/>')
    out.append(f'<text x="{M + 16}" y="{y + 20}" font-size="21" font-weight="700" fill="{INK}">{esc(s)}</text>')
    y += 36
    if simple:
        lines = wrap(simple, 14, CW - 110)
        hh = 20 * len(lines) + 16
        out.append(f'<rect x="{M}" y="{y}" width="{CW}" height="{hh}" rx="6" fill="#e5f4e4"/>')
        out.append(f'<text x="{M + 12}" y="{y + 24}" font-size="13" font-weight="700" fill="#006300">EN CLAIR</text>')
        for i, ln in enumerate(lines):
            out.append(f'<text x="{M + 96}" y="{y + 24 + 20 * i}" font-size="14" fill="{INK}">{rich(ln)}</text>')
        y += hh + 10
    if sub:
        y += para(M, y, CW, sub, 13, INK2)
        y += 4


def _s_h3(s):
    global y
    y += 12
    out.append(f'<text x="{M}" y="{y + 15}" font-size="15" font-weight="700" fill="{INK}">{esc(s)}</text>')
    y += 24


def _s_p(s, size=14, color=INK):
    global y
    y += para(M, y, CW, s, size, color)
    y += 8


def _s_note(s):
    global y
    y += para(M, y, CW, s, 12, MUTED)
    y += 6


def _s_bullets(items, size=14):
    global y
    for it in items:
        out.append(f'<circle cx="{M + 6}" cy="{y + 10}" r="2.5" fill="{BLUE}"/>')
        y += para(M + 18, y, CW - 18, it, size)
        y += 3
    y += 6


def _s_table(headers, rows, widths, size=12.5, x=M, bold_first=True):
    """widths : fractions de CW. Cellules avec retour à la ligne automatique."""
    global y
    total = sum(widths)
    cols = [CW * w / total for w in widths]
    pad = 8
    lh = round(size * 1.4)
    # header
    hh = lh + 2 * pad
    out.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{hh}" fill="{BLUE_L}" rx="3"/>')
    cx = x
    for h, cw in zip(headers, cols):
        out.append(f'<text x="{cx + pad}" y="{y + pad + lh - 4}" font-size="{size}" font-weight="700" fill="{INK}">{esc(h)}</text>')
        cx += cw
    y += hh
    for ri, row in enumerate(rows):
        wrapped = [wrap(c, size, cw - 2 * pad) for c, cw in zip(row, cols)]
        n = max(len(w) for w in wrapped)
        rh = n * lh + 2 * pad
        if ri % 2 == 1:
            out.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{rh}" fill="{ROWALT}"/>')
        out.append(f'<line x1="{x}" y1="{y + rh}" x2="{x + CW}" y2="{y + rh}" stroke="{GRID}" stroke-width="1"/>')
        cx = x
        rowtxt = " ".join(row)
        ms = re.match(r"Étape (\d)", row[-1] or "")
        if ms:
            out.append(f'<g class="stepcell" data-step="{ms.group(1)}" data-tip="Étape {ms.group(1)} du schéma (section 10)"><rect x="{x}" y="{y}" width="{CW}" height="{rh}" fill="transparent"/>')
        out.append(f'<g{det_attr(headers, row, rowsrc(row, CUR_FALLBACK[0]))}><rect x="{x}" y="{y}" width="{CW}" height="{rh}" fill="transparent"/>')
        for ci, (lines, cw) in enumerate(zip(wrapped, cols)):
            wt = "600" if (ci == 0 and bold_first) else "400"
            for li, ln in enumerate(lines):
                out.append(f'<text x="{cx + pad}" y="{y + pad + lh * (li + 1) - 4}" font-size="{size}" font-weight="{wt}" fill="{INK}">{rich(ln)}</text>')
            cx += cw
        out.append('</g>')
        if ms:
            out.append('</g>')
        y += rh
    y += 10


def _s_stat_tiles(tiles):
    """tiles : liste de (valeur, libellé, sous-texte)"""
    global y
    n = len(tiles)
    gap = 12
    tw = (CW - gap * (n - 1)) / n
    th = 92
    for i, (v, lab, sub) in enumerate(tiles):
        x = M + i * (tw + gap)
        out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="{SURF}" stroke="{GRID}"/>')
        out.append(f'<text x="{x + 14}" y="{y + 24}" font-size="12" fill="{INK2}">{esc(lab)}</text>')
        out.append(f'<text x="{x + 14}" y="{y + 58}" font-size="28" font-weight="700" fill="{INK}">{esc(v)}</text>')
        out.append(f'<text x="{x + 14}" y="{y + 78}" font-size="11.5" fill="{MUTED}">{esc(sub)}</text>')
    y += th + 14


def hbar_chart(title, data, unit="", width=None, x=None, note_txt=None, color=BLUE, fmt=lambda v: f"{v:g}", labw=150):
    """data : liste (label, valeur), barres horizontales triées, une seule série."""
    global y
    x = x or M
    width = width or CW
    out.append(f'<text x="{x}" y="{y + 14}" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>')
    yy = y + 28
    plotw = width - labw - 70
    vmax = max(v for _, v in data)
    bh = 16; gap = 8
    for lab, v in data:
        bw = plotw * v / vmax
        out.append(f'<text x="{x + labw - 8}" y="{yy + 12}" font-size="12" fill="{INK2}" text-anchor="end">{esc(lab)}</text>')
        out.append(f'<rect class="bar" data-tip="{esc(lab)} : {esc(fmt(v) + unit)}" x="{x + labw}" y="{yy}" width="{max(bw,2):.1f}" height="{bh}" rx="3" fill="{color}"/>')
        out.append(f'<text x="{x + labw + bw + 6:.1f}" y="{yy + 12}" font-size="12" fill="{INK}">{esc(fmt(v) + unit)}</text>')
        yy += bh + gap
    out.append(f'<line x1="{x + labw}" y1="{y + 24}" x2="{x + labw}" y2="{yy - gap + 2}" stroke="{AXIS}"/>')
    h = yy - y
    if note_txt:
        h += para(x, yy + 4, width, note_txt, 11.5, MUTED) + 6
    return h


def line_chart(title, series, x, width, height=200, unit="", note_txt=None, ylab="", xlabels=None, every=1):
    """series : liste de (nom, couleur, [(x,y)...]) ; même échelle. Une série -> pas de légende."""
    global y
    out.append(f'<text x="{x}" y="{y + 14}" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>')
    top = y + 34; left = x + 60; pw = width - 80; ph = height - 70
    xs = sorted({px for _, _, pts in series for px, _ in pts})
    ymax = max(py for _, _, pts in series for _, py in pts)
    # grille
    step = 10 ** (len(str(int(ymax))) - 1)
    if ymax / step < 3:
        step /= 2
    gy = 0
    while gy <= ymax * 1.05:
        yy = top + ph - ph * gy / (ymax * 1.05)
        out.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{left + pw}" y2="{yy:.1f}" stroke="{GRID}"/>')
        out.append(f'<text x="{left - 8}" y="{yy + 4:.1f}" font-size="11" fill="{MUTED}" text-anchor="end">{gy:g}</text>')
        gy += step
    def X(v): return left + pw * (v - xs[0]) / (xs[-1] - xs[0])
    def Y(v): return top + ph - ph * v / (ymax * 1.05)
    for i, xv in enumerate(xs):
        if i % every: continue
        lab = xlabels[i] if xlabels else str(xv)
        out.append(f'<text x="{X(xv):.1f}" y="{top + ph + 18}" font-size="11" fill="{MUTED}" text-anchor="middle">{esc(lab)}</text>')
    out.append(f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="{AXIS}"/>')
    for name, col, pts in series:
        d = " ".join(f"{'M' if i == 0 else 'L'}{X(px):.1f},{Y(py):.1f}" for i, (px, py) in enumerate(pts))
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round"/>')
        for i, (px, py) in enumerate(pts):
            lab = xlabels[xs.index(px)] if xlabels else str(px)
            val = f"{py:,}".replace(",", " ")
            _d = esc(json.dumps({"titre": f"{name} — {lab}", "champs": [["Période", lab], [name, val]], "source": "https://www.hatvp.fr/le-repertoire/"}, ensure_ascii=False))
            out.append(f'<circle class="pt det" data-detail="{_d}" data-tip="{esc(lab)} : {val}" cx="{X(px):.1f}" cy="{Y(py):.1f}" r="5" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
        # étiquette dernier point
        px, py = pts[-1]
        out.append(f'<text x="{X(px) + 8:.1f}" y="{Y(py) + 4:.1f}" font-size="11.5" font-weight="600" fill="{INK}">{esc(f"{py:,}".replace(",", " ") + unit)}</text>')
        px, py = pts[0]
        out.append(f'<text x="{X(px) + 8:.1f}" y="{Y(py) - 10:.1f}" font-size="11.5" fill="{INK}" text-anchor="start">{esc(f"{py:,}".replace(",", " ") + unit)}</text>')
    if ylab:
        out.append(f'<text x="{left}" y="{top - 8}" font-size="11" fill="{MUTED}">{esc(ylab)}</text>')
    h = height
    if note_txt:
        h += para(x, y + height, width, note_txt, 11.5, MUTED) + 4
    return h


def box(x, yy, w, h, title, lines, fill=SURF, stroke=GRID, tcolor=INK, size=12, attrs=""):
    if attrs and 'data-person' not in attrs:
        src = "https://www.vie-publique.fr/fiches/19499-quelles-sont-les-etapes-du-vote-dune-loi"
        d = {"titre": title, "champs": [["Rôle", " ".join(lines)]], "source": src}
        attrs = attrs.replace('class="', 'class="det ', 1) + ' data-detail="' + esc(json.dumps(d, ensure_ascii=False)) + '"'
    out.append(f'<g {attrs}><rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
    tl = wrap(title, size + 1, w - 14)
    for i, t in enumerate(tl):
        out.append(f'<text x="{x + w/2}" y="{yy + 20 + i * (size + 4)}" font-size="{size + 1}" font-weight="700" fill="{tcolor}" text-anchor="middle">{esc(t)}</text>')
    yy2 = yy + 30 + (len(tl) - 1) * (size + 4)
    for ln in lines:
        for sub in wrap(ln, size - 1, w - 16):
            out.append(f'<text x="{x + w/2}" y="{yy2 + 10}" font-size="{size - 1}" fill="{INK2}" text-anchor="middle">{esc(sub)}</text>')
            yy2 += size + 3
    out.append('</g>')


def arrow(x1, y1, x2, y2, color=INK2, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8" marker-end="url(#arr)"{d}/>')


import math
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
        dsrc = "https://www.senat.fr/senateurs/grp.html" if "Sénat" in title else "https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"
        dd = {"titre": g, "champs": [["Chambre", title], ["Sièges", str(counts.get(g, 0)) if g != "Siège vacant" else str(vacant)], ["Part des sièges", f"{100*counts.get(g,0)/total:.1f} %" if g != "Siège vacant" else ""]], "source": dsrc}
        out.append(f'<circle class="seat det" data-detail="{esc(json.dumps(dd, ensure_ascii=False))}" data-group="{esc(g)}" data-tip="{esc(tip)}" cx="{px:.1f}" cy="{py:.1f}" r="{dot:.1f}" fill="{c}"{stroke}/>')
    out.append(f'<text x="{cx}" y="{cy - 6}" font-size="26" font-weight="700" fill="{INK}" text-anchor="middle">{total}</text>')
    out.append(f'<text x="{cx}" y="{cy + 12}" font-size="11.5" fill="{MUTED}" text-anchor="middle">sièges</text>')
    # légende en deux colonnes
    ly = cy + 26; lx0 = x; colw = width / 2
    for i, g in enumerate(order):
        lx = lx0; yy = ly + i * 18
        lab = f"{g} : {counts.get(g, 0)}"
        dsrc = "https://www.senat.fr/senateurs/grp.html" if "Sénat" in title else "https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif"
        dd = {"titre": g, "champs": [["Chambre", title], ["Sièges", str(counts.get(g, 0))], ["Part des sièges", f"{100*counts.get(g,0)/total:.1f} %"]], "source": dsrc}
        out.append(f'<g class="lg det" data-detail="{esc(json.dumps(dd, ensure_ascii=False))}" data-group="{esc(g)}"><rect x="{lx - 4}" y="{yy - 3}" width="{width/2}" height="17" fill="transparent"/><rect x="{lx}" y="{yy}" width="11" height="11" rx="2" fill="{GCOL[g]}"/>')
        out.append(f'<text x="{lx + 16}" y="{yy + 9.5}" font-size="11.5" fill="{INK2}">{esc(lab)}</text></g>')
    nrows = len(order)
    if vacant:
        yy = ly + nrows * 18
        out.append(f'<circle cx="{lx0 + 5.5}" cy="{yy + 5.5}" r="5" fill="#ffffff" stroke="{AXIS}"/>')
        out.append(f'<text x="{lx0 + 16}" y="{yy + 9.5}" font-size="11.5" fill="{INK2}">Sièges vacants : {vacant}</text>')
        nrows += 1
    return (ly + nrows * 18 + 8) - y

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
box(M + (CW - pmw) / 2, g0, pmw, 54, "Sébastien Lecornu, Premier ministre", ["chargé de la Planification écologique et énergétique"], fill=BLUE_L, stroke=BLUE)
medal(M + (CW - pmw) / 2 + 28, g0 + 27, "Sébastien Lecornu", r=20)
# délégués auprès du PM
dw = (CW - 2 * 16) / 3
dl = [("Laurent Panifous", "Relations avec le Parlement"), ("Maud Bregeon", "Porte-parole du Gouvernement ; Énergie (avec l'Économie)"), ("Aurore Bergé", "Égalité femmes-hommes, lutte contre les discriminations")]
yd = g0 + 54 + 36
for i, (n, f) in enumerate(dl):
    x = M + i * (dw + 16)
    box(x, yd, dw, 68, n, ["ministre déléguée auprès du Premier ministre : " + f if n != "Laurent Panifous" else "ministre délégué auprès du Premier ministre : " + f], fill="#f3f2ee", stroke=MUTED, size=11.5)
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



# ---- Sources par ligne (clé = fragment distinctif de la ligne) et fallback par section
ROWSRC = [
 ("Budgets 2027 de l'État", "https://www.elysee.fr/emmanuel-macron/2026/10/01/compte-rendu-du-conseil-des-ministres-du-1-octobre-2026"),
 ("travail d'intérêt général", "https://www.elysee.fr/emmanuel-macron/2026/10/01/compte-rendu-du-conseil-des-ministres-du-1-octobre-2026"),
 ("Cour des comptes", "https://www.elysee.fr/emmanuel-macron/2026/10/01/compte-rendu-du-conseil-des-ministres-du-1-octobre-2026"),
 ("Annonces du Premier ministre", "https://www.info.gouv.fr/"),
 ("secteur nucléaire", "https://www.elysee.fr/emmanuel-macron/2026/10/14/compte-rendu-du-conseil-des-ministres-du-14-octobre-2026"),
 ("Secteur nucléaire", "https://www.elysee.fr/emmanuel-macron/2026/10/14/compte-rendu-du-conseil-des-ministres-du-14-octobre-2026"),
 ("ordonnance fiscale", "https://www.elysee.fr/emmanuel-macron/2026/10/14/compte-rendu-du-conseil-des-ministres-du-14-octobre-2026"),
 ("Marie Fontanel", "https://www.elysee.fr/emmanuel-macron/2026/10/14/compte-rendu-du-conseil-des-ministres-du-14-octobre-2026"),
 ("France-Finlande", "https://www.elysee.fr/emmanuel-macron/2026/10/29/la-france-et-la-finlande-ont-tenu-leur-premiere-reunion-du-groupe-de-pilotage-nucleaire-a-paris-le-mardi-27-octobre"),
 ("ingérences étrangères", "https://www.senat.fr/dossier-legislatif/pjl25-913.html"),
 ("dégradations dans l'espace public", "https://www.senat.fr/dossier-legislatif/pjl25-952.html"),
 ("Protection des enfants", "https://www.senat.fr/dossier-legislatif/pjl25-911.html"),
 ("Corse autonome", "https://www.senat.fr/dossier-legislatif/pjl24-869.html"),
 ("Rapatriés d'Indochine", "https://www.senat.fr/dossier-legislatif/ppl24-685.html"),
 ("Code noir", "https://www.senat.fr/dossier-legislatif/ppl25-672.html"),
 ("violences sexistes", "https://www.senat.fr/dossier-legislatif/ppl25-619.html"),
 ("Rapports locatifs", "https://www.senat.fr/dossier-legislatif/ppl25-217.html"),
 ("rapports locatifs", "https://www.senat.fr/dossier-legislatif/ppl25-217.html"),
 ("Ultramarins", "https://www.senat.fr/dossier-legislatif/ppl25-740.html"),
 ("Titre-restaurant", "https://www.senat.fr/dossier-legislatif/ppl26-032.html"),
 ("Stocks de sécurité", "https://www.senat.fr/dossier-legislatif/ppl25-610.html"),
 ("Modernisation de la radio", "https://www.senat.fr/dossier-legislatif/ppl25-743.html"),
 ("Sécu", "https://www.senat.fr/dossier-legislatif/plfss2027.html"),
 ("Sécurité sociale", "https://www.senat.fr/dossier-legislatif/plfss2027.html"),
 ("affaires sociales", "https://www.assemblee-nationale.fr/dyn/actualites-accueil-hub/plfss-pour-2027-examen-et-rejet-du-projet-de-loi-en-commission-des-affaires-sociales"),
 ("30 octobre", "https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/seance/session-ordinaire-de-2026-2027/troisieme-seance-du-vendredi-30-octobre-2026"),
 ("4 novembre", "https://www.assemblee-nationale.fr/dyn/17/dossiers/PLF_2027"),
 ("fin de gestion", "https://www.assemblee-nationale.fr/dyn/17/textes/l17b3434_projet-loi.pdf"),
 ("S&P", "https://www.aft.gouv.fr/fr"),
 ("17 décembre", "https://www.senat.fr/travaux-parlementaires/textes-legislatifs/la-loi-en-clair/projet-de-loi-de-finances-pour-2027.html"),
 ("délai de 70 jours", "https://www.senat.fr/travaux-parlementaires/textes-legislatifs/la-loi-en-clair/projet-de-loi-de-finances-pour-2027.html"),
 ("Budget de l'État au Sénat", "https://www.assemblee-nationale.fr/dyn/17/dossiers/PLF_2027"),
 ("Dette publique", "https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-21102026-bp"),
 ("Qualité de crédit", "https://www.aft.gouv.fr/fr"),
 ("Fitch", "https://www.aft.gouv.fr/fr"),
 ("Moody", "https://www.aft.gouv.fr/fr"),
 ("Union européenne", "https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-21102026-bp"),
 ("PISA", "https://gpseducation.oecd.org/CountryProfile?primaryCountry=FRA&treshold=10&topic=PI"),
 ("Eurobaromètre", "https://commission.europa.eu/document/download/e6577383-66c2-48d2-8a2e-d029d254a4ec_en?filename=Country+chapter+-+France+-+EN.pdf"),
 ("Justice", "https://commission.europa.eu/document/download/e6577383-66c2-48d2-8a2e-d029d254a4ec_en?filename=Country+chapter+-+France+-+EN.pdf"),
 ("Tableau de bord européen", "https://ec.europa.eu/assets/rtd/eis/2026/ec_rtd_eis-country-profile-fr.pdf"),
 ("OMPI", "https://www.wipo.int/edocs/gii-ranking/2025/fr.pdf"),
 ("PNUD", "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Statistical_Annex_HDI_Trends_Table.pdf"),
 ("FMI", "https://www.imf.org/en/news/articles/2026/07/22/pr26255-france-imf-executive-board-concludes-2026-article-iv-consultation"),
 ("Déficit visé", "https://www.elysee.fr/emmanuel-macron/2026/10/01/compte-rendu-du-conseil-des-ministres-du-1-octobre-2026"),
]
def rowsrc(row, fallback):
    joined = " | ".join(str(c) for c in row)
    for k, u in ROWSRC:
        if k in joined:
            return u
    return fallback
CUR_FALLBACK = ['https://www.assemblee-nationale.fr/dyn/17/dossiers']
FALLBACK = {"default": "https://www.assemblee-nationale.fr/dyn/17/dossiers"}
def det_attr(headers, row, url, titre=None):
    """attribut data-detail (JSON) : toutes les colonnes + source"""
    d = {"titre": titre or str(row[0]), "champs": [[str(h), str(c)] for h, c in zip(headers, row) if str(c).strip()], "source": url}
    return ' class="det" data-detail="' + esc(json.dumps(d, ensure_ascii=False)) + '"'


# ================= Jumeau HTML des éléments de texte (lisible sur mobile et par les lecteurs d'écran) =================
SEGS = []   # (html, index dans out, y avant, y après)
def _hseg(frag, fn):
    """exécute fn (dessin SVG, utilisé seulement pour mesurer la hauteur), jette le SVG et garde le HTML"""
    global y
    n = len(out); y0 = y
    fn()
    del out[n:]
    SEGS.append((frag, n, y0, y))

def hraw(frag, dy):
    global y
    SEGS.append((frag, len(out), y, y + dy)); y += dy

def rich_html(s):
    parts = s.split("**")
    return "".join(f"<strong>{esc(t)}</strong>" if i % 2 else esc(t) for i, t in enumerate(parts))

def h2(s, sub=None, simple=None):
    n = len(SECTIONS) + 1
    frag = f'<h2 class="sec" id="sec{n}">{esc(s)}</h2>'
    if simple: frag += f'<div class="clair"><b>EN CLAIR</b><p>{rich_html(simple)}</p></div>'
    if sub: frag += f'<p class="sub">{rich_html(sub)}</p>'
    _hseg(frag, lambda: _s_h2(s, sub=sub, simple=simple))

def h3(s): _hseg(f'<h3>{esc(s)}</h3>', lambda: _s_h3(s))

def p(s, size=14, color=INK):
    cls = "note" if color == MUTED else ("muted" if color == INK2 else "")
    _hseg(f'<p class="{cls}">{rich_html(s)}</p>', lambda: _s_p(s, size, color))

def note(s): _hseg(f'<p class="note">{rich_html(s)}</p>', lambda: _s_note(s))

def bullets(items, size=14):
    _hseg('<ul>' + "".join(f"<li>{rich_html(i)}</li>" for i in items) + '</ul>', lambda: _s_bullets(items, size))

def stat_tiles(tiles):
    f = '<div class="tiles">' + "".join(f'<div class="tile"><span class="tl">{esc(l)}</span><span class="tv">{esc(v)}</span><span class="ts">{esc(sb)}</span></div>' for v, l, sb in tiles) + '</div>'
    _hseg(f, lambda: _s_stat_tiles(tiles))

def table(headers, rows, widths, size=12.5, x=M, bold_first=True):
    tot = sum(widths)
    f = '<div class="tblwrap"><table class="rt"><colgroup>' + "".join(f'<col style="width:{100 * w / tot:.1f}%">' for w in widths) + '</colgroup><thead><tr>' + "".join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>'
    for row in rows:
        det = det_attr(headers, row, rowsrc(row, CUR_FALLBACK[0]))
        ms = re.match(r"Étape (\d)", row[-1] or "")
        if ms:
            det = det.replace('class="det"', 'class="det stepcell"') + f' data-step="{ms.group(1)}"'
        f += f'<tr{det}>' + "".join(f'<td data-label="{esc(h)}"{" class=first" if (i == 0 and bold_first) else ""}>{rich_html(str(c))}</td>' for i, (h, c) in enumerate(zip(headers, row))) + '</tr>'
    f += '</tbody></table></div>'
    _hseg(f, lambda: _s_table(headers, rows, widths, size, x, bold_first))

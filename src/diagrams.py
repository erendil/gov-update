# -*- coding: utf-8 -*-
"""Diagrammes interactifs remplaçant les tableaux (chaque tableau reste disponible en option)."""
import re

MONTHS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12}
MABR = {10: "oct.", 11: "nov.", 12: "déc.", 1: "janv.", 2: "févr.", 3: "mars"}

def parse_date(s, default_month=10):
    """'1er octobre' -> (10,1) ; '27-28 octobre' -> (10,27) ; '20 novembre au 9 décembre' -> (11,20) ; '17 décembre' -> (12,17)"""
    s = s.lower().replace("1er", "1")
    m = re.search(r"(\d{1,2})(?:-\d{1,2})?\s*(?:au \d{1,2} )?(?:(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre))", s)
    if m:
        return (MONTHS[m.group(2)], int(m.group(1)))
    m = re.search(r"(\d{1,2})", s)
    return (default_month, int(m.group(1))) if m else None

def dayindex(md, origin):
    (m, d), (m0, d0) = md, origin
    days = 0; mm, dd = m0, d0
    # approximation : mois de 31/30 jours
    length = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    while (mm, dd) != (m, d):
        dd += 1; days += 1
        if dd > length[mm]:
            dd = 1; mm = mm % 12 + 1
        if days > 120: break
    return days


def timeline(H, rows, origin, end, label_col=1, detail_col=2, default_month=10, color=None, headers=None, fallback=None):
    """H = helpers module (dict-like globals). rows : (date, libellé, détail[, vote]). Axe horizontal, cartes empilées par couloir."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, GRID, AXIS, SURF, BLUE, BLUE_L, ORANGE = (H[k] for k in ("INK", "INK2", "MUTED", "GRID", "AXIS", "SURF", "BLUE", "BLUE_L", "ORANGE"))
    esc, wrap = H["esc"], H["wrap"]
    y0 = H["y"]
    total = dayindex(end, origin)
    axis_y = y0 + 22
    def X(md): return M + 40 + (CW - 80) * dayindex(md, origin) / max(total, 1)
    # ticks : chaque semaine
    out.append(f'<line x1="{M + 40}" y1="{axis_y}" x2="{M + CW - 40}" y2="{axis_y}" stroke="{AXIS}" stroke-width="2"/>')
    mm, dd = origin
    length = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    i = 0
    while i <= total:
        md = (mm, dd)
        if dd == 1 or dd % 7 == 1 or i == 0:
            out.append(f'<line x1="{X(md):.1f}" y1="{axis_y - 5}" x2="{X(md):.1f}" y2="{axis_y + 5}" stroke="{AXIS}"/>')
            out.append(f'<text x="{X(md):.1f}" y="{axis_y - 10}" font-size="11" fill="{MUTED}" text-anchor="middle">{dd} {MABR.get(mm, "")}</text>')
        dd += 1; i += 1
        if dd > length[mm]: dd = 1; mm = mm % 12 + 1
    # cartes
    cw_, ch = 196, 58
    lanes = []  # x de fin par couloir
    cards = []
    for r in rows:
        md = parse_date(r[0], default_month)
        if not md: continue
        x = X(md)
        bx = min(max(x - cw_ / 2, M), M + CW - cw_)
        lane = 0
        while lane < len(lanes) and lanes[lane] > bx - 8:
            lane += 1
        if lane == len(lanes): lanes.append(0)
        lanes[lane] = bx + cw_
        cards.append((x, bx, lane, r))
    for x, bx, lane, r in cards:
        cy = axis_y + 26 + lane * (ch + 14)
        col = color(r) if color else BLUE
        out.append(f'<line x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" y2="{cy}" stroke="{GRID}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="5" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
        tip = esc(r[0] + " : " + (r[detail_col] if len(r) > detail_col and r[detail_col] else r[label_col]) + (("  |  Vote : " + r[3]) if len(r) > 3 and r[3] else ""))
        da = H["det_attr"](headers or [], r, H["rowsrc"](r, fallback or H["CUR_FALLBACK"][0]), titre=r[label_col]).replace('class="det"', 'class="det card"')
        out.append(f'<g{da} data-tip="{tip}"><rect x="{bx:.1f}" y="{cy}" width="{cw_}" height="{ch}" rx="6" fill="{SURF}" stroke="{col}" stroke-width="1.4"/>')
        out.append(f'<text x="{bx + 8:.1f}" y="{cy + 15}" font-size="10.5" font-weight="700" fill="{col}">{esc(r[0])}</text>')
        for li, ln in enumerate(wrap(r[label_col], 11, cw_ - 16)[:3]):
            out.append(f'<text x="{bx + 8:.1f}" y="{cy + 29 + li * 13}" font-size="11" fill="{INK}">{esc(ln)}</text>')
        out.append('</g>')
    H["y"] = axis_y + 26 + len(lanes) * (ch + 14) + 6


def pipeline(H, groups, fallback=None):
    """groups : liste de (titre, couleur, rows) ; rows = (texte, porteur, ce qu'il fait, état 'Étape N, ...'). Colonnes = étapes 1..9."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, GRID, AXIS, SURF, BLUE_L = (H[k] for k in ("INK", "INK2", "MUTED", "GRID", "AXIS", "SURF", "BLUE_L"))
    esc, wrap = H["esc"], H["wrap"]
    y0 = H["y"]
    names = {1: "Dépôt", 2: "Commission", 3: "Séance", 4: "Navette", 5: "Comm. mixte", 6: "Adoption", 7: "Promulgation", 8: "Décrets", 9: "Contrôle"}
    ncol = 9; gap = 8
    import math as _m
    counts = [0] * ncol
    for g_ in groups:
        for r in g_[2]:
            m = re.match(r"Étape (\d)", r[3]); counts[(int(m.group(1)) if m else 1) - 1] += 1
    subs = [max(1, _m.ceil(c / 4)) for c in counts]
    units = sum(subs); unitw = (CW - gap * (ncol - 1)) / units
    xs = []; x = M
    for i in range(ncol):
        xs.append((x, unitw * subs[i])); x += unitw * subs[i] + gap
    cardw = unitw
    # en-têtes de colonnes
    for i in range(ncol):
        x, colw = xs[i]
        out.append(f'<rect x="{x}" y="{y0}" width="{colw}" height="34" rx="6" fill="{BLUE_L}"/>')
        out.append(f'<text x="{x + colw/2}" y="{y0 + 14}" font-size="12" font-weight="700" fill="{INK}" text-anchor="middle">Étape {i + 1}</text>')
        out.append(f'<text x="{x + colw/2}" y="{y0 + 28}" font-size="10.5" fill="{INK2}" text-anchor="middle">{names[i + 1]}</text>')
    top = y0 + 44
    heights = [top] * ncol
    placed = [0] * ncol
    ch = 64
    for g_ in groups:
        gtitle, col, rows = g_[0], g_[1], g_[2]; hdr = g_[3] if len(g_) > 3 else []
        for r in rows:
            m = re.match(r"Étape (\d)", r[3]); step = int(m.group(1)) if m else 1
            i = step - 1
            k = placed[i]; sub = k % subs[i]; row_ = k // subs[i]; placed[i] += 1
            x = xs[i][0] + sub * unitw; cy = top + row_ * (ch + 8); colw = cardw - (0 if subs[i] == 1 else 6)
            heights[i] = max(heights[i], cy + ch + 8)
            tip = esc(f"{r[0]} — {r[1]}. {r[2]} État : {r[3]}")
            da = H["det_attr"](hdr, r, H["rowsrc"](r, fallback or H["CUR_FALLBACK"][0])).replace('class="det"', 'class="det stepcell card"')
            out.append(f'<g{da} data-step="{step}" data-tip="{tip}"><rect x="{x}" y="{cy}" width="{colw}" height="{ch}" rx="6" fill="{SURF}" stroke="{col}" stroke-width="1.6"/>')
            out.append(f'<rect x="{x}" y="{cy}" width="5" height="{ch}" rx="2" fill="{col}"/>')
            for li, ln in enumerate(wrap(r[0], 10.5, colw - 16)[:3]):
                out.append(f'<text x="{x + 10}" y="{cy + 14 + li * 12}" font-size="10.5" font-weight="700" fill="{INK}">{esc(ln)}</text>')
            who = r[1].split(",")[0].split(" (")[0]
            w0 = wrap(who, 9.5, colw - 16)[0]
            if w0 != who: w0 = w0.rstrip() + "…"
            out.append(f'<text x="{x + 10}" y="{cy + ch - 8}" font-size="9.5" fill="{MUTED}">{esc(w0)}</text>')
            out.append('</g>')
    # colonnes vides : grille légère
    bottom = max(heights)
    for i in range(ncol):
        x, colw = xs[i]
        if counts[i] == 0:
            out.append(f'<line x1="{x + colw/2}" y1="{top}" x2="{x + colw/2}" y2="{bottom}" stroke="{GRID}" stroke-dasharray="2 4"/>')
    # légende
    ly = bottom + 10; lx = M
    for g_ in groups:
        gtitle, col, rows = g_[0], g_[1], g_[2]
        out.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="2" fill="{col}"/>')
        out.append(f'<text x="{lx + 18}" y="{ly + 10}" font-size="11.5" fill="{INK2}">{esc(gtitle)} ({len(rows)})</text>')
        lx += 18 + H["text_width"](gtitle, 11.5) + 50
    out.append(f'<text x="{M + CW}" y="{ly + 10}" font-size="11" fill="{MUTED}" text-anchor="end">Survolez une carte pour le détail ; survolez une étape du schéma (section 10) pour relier</text>')
    H["y"] = ly + 24


def tracks(H, tracks_data, steps_total=9, headers=None, fallback=None):
    """tracks_data : liste de (nom, étape courante, {étape: texte}) ; chemin à étapes avec disques remplis."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, GRID, AXIS, SURF, BLUE, BLUE_L, GOOD = (H[k] for k in ("INK", "INK2", "MUTED", "GRID", "AXIS", "SURF", "BLUE", "BLUE_L", "GOOD"))
    esc, wrap = H["esc"], H["wrap"]
    y0 = H["y"]
    names = {1: "Dépôt", 2: "Commission", 3: "Séance", 4: "Navette", 5: "Comm. mixte", 6: "Adoption", 7: "Promulgation", 8: "Décrets", 9: "Contrôle"}
    labw = 230; left = M + labw; right = M + CW - 30
    for ti, td in enumerate(tracks_data):
        name, cur, info = td[0], td[1], td[2]
        frows = td[3] if len(td) > 3 else []; fcol = td[4] if len(td) > 4 else 1
        detail_row = [name] + [r[fcol] for r in frows]; detail_hdr = ["Texte"] + [r[0] for r in frows]
        cy = y0 + 30 + ti * 96
        out.append(f'<text x="{M}" y="{cy + 4}" font-size="13" font-weight="700" fill="{INK}">{esc(name)}</text>')
        out.append(f'<line x1="{left}" y1="{cy}" x2="{right}" y2="{cy}" stroke="{GRID}" stroke-width="4"/>')
        xcur = left + (right - left) * (cur - 1) / (steps_total - 1)
        out.append(f'<line x1="{left}" y1="{cy}" x2="{xcur:.1f}" y2="{cy}" stroke="{BLUE}" stroke-width="4"/>')
        for s in range(1, steps_total + 1):
            x = left + (right - left) * (s - 1) / (steps_total - 1)
            done = s < cur; now = s == cur
            fill = BLUE if done else (SURF if not now else "#fab219")
            stroke = BLUE if (done or not now) else "#d08a00"
            tip = esc(f"Étape {s}, {names[s]} : " + info.get(s, "pas encore atteinte" if s > cur else "franchie"))
            da = H["det_attr"](detail_hdr, detail_row, H["rowsrc"](detail_row, fallback or H["CUR_FALLBACK"][0]), titre=f"{name} — étape {s}, {names[s]}").replace('class="det"', 'class="det stepcell"')
            out.append(f'<g{da} data-step="{s}" data-tip="{tip}"><circle cx="{x:.1f}" cy="{cy}" r="{13 if now else 10}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            out.append(f'<text x="{x:.1f}" y="{cy + 4}" font-size="11" font-weight="700" fill="{"#ffffff" if done else INK}" text-anchor="middle">{s}</text>')
            out.append(f'<text x="{x:.1f}" y="{cy + 28}" font-size="10.5" fill="{INK2 if s <= cur else MUTED}" text-anchor="middle">{esc(names[s])}</text></g>')
        # texte de l'étape courante sous la piste
        txt = info.get(cur, "")
        for li, ln in enumerate(wrap("Maintenant : " + txt, 11.5, right - left)[:2]):
            out.append(f'<text x="{left}" y="{cy + 48 + li * 14}" font-size="11.5" fill="{INK}">{esc(ln)}</text>')
    H["y"] = y0 + 30 + len(tracks_data) * 96


def votes(H, rows, headers=None, fallback=None):
    """rows : (date, événement, vote 'a contre b') ; barres pour/contre."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, GRID, AXIS, SURF, BLUE, RED = (H[k] for k in ("INK", "INK2", "MUTED", "GRID", "AXIS", "SURF", "BLUE", "RED"))
    esc, wrap = H["esc"], H["wrap"]
    y0 = H["y"]
    labw = 470; plotw = CW - labw - 70; vmax = 460
    rh = 38
    out.append(f'<text x="{M + labw + plotw/2}" y="{y0 + 10}" font-size="11" fill="{MUTED}" text-anchor="middle">voix pour la décision décrite (bleu) / voix contre (rouge)</text>')
    yy = y0 + 20
    for row in rows:
        date, ev, vote = row[0], row[1], row[2]
        da = H["det_attr"](headers or ["Date", "Événement", "Vote"], row, H["rowsrc"](row, fallback or H["CUR_FALLBACK"][0]), titre=f"{date} : {ev[:60]}")
        out.append(f'<g{da}><rect x="{M}" y="{yy}" width="{CW}" height="{rh - 2}" fill="transparent"/>')
        lines = wrap(ev, 11.5, labw - 90)[:2]
        out.append(f'<text x="{M}" y="{yy + 14}" font-size="11.5" font-weight="700" fill="{INK}">{esc(date)}</text>')
        for li, ln in enumerate(lines):
            out.append(f'<text x="{M + 88}" y="{yy + 14 + li * 13}" font-size="11.5" fill="{INK2}">{esc(ln)}</text>')
        m = re.match(r"(\d+) contre (\d+)", vote or "")
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            wa, wb = plotw * a / vmax, plotw * b / vmax
            out.append(f'<rect class="bar" data-tip="{esc(date)} : {a} pour" x="{M + labw}" y="{yy + 2}" width="{max(wa,2):.1f}" height="11" rx="2" fill="{BLUE}"/>')
            out.append(f'<rect class="bar" data-tip="{esc(date)} : {b} contre" x="{M + labw}" y="{yy + 15}" width="{max(wb,2):.1f}" height="11" rx="2" fill="{RED}"/>')
            out.append(f'<text x="{M + labw + max(wa, wb) + 6:.1f}" y="{yy + 18}" font-size="11" fill="{INK}">{a} / {b}</text>')
        else:
            out.append(f'<text x="{M + labw}" y="{yy + 16}" font-size="11" fill="{MUTED}">sans scrutin chiffré</text>')
        out.append(f'<line x1="{M}" y1="{yy + rh - 2}" x2="{M + CW}" y2="{yy + rh - 2}" stroke="{GRID}"/>')
        out.append('</g>')
        yy += rh
    H["y"] = yy + 6


def rankchart(H, rows, headers=None, fallback=None):
    """rows : (domaine, classement, rang, tendance, édition). Position de la France de 1 à N."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, GRID, AXIS, SURF, BLUE, ORANGE, GOOD, CRIT = (H[k] for k in ("INK", "INK2", "MUTED", "GRID", "AXIS", "SURF", "BLUE", "ORANGE", "GOOD", "CRIT"))
    esc, wrap = H["esc"], H["wrap"]
    y0 = H["y"]
    labw = 260; plotw = CW - labw - 230; rh = 36
    out.append(f'<text x="{M + labw}" y="{y0 + 10}" font-size="11" fill="{MUTED}">1er</text>')
    out.append(f'<text x="{M + labw + plotw}" y="{y0 + 10}" font-size="11" fill="{MUTED}" text-anchor="end">dernier</text>')
    out.append(f'<text x="{M + labw + plotw/2}" y="{y0 + 10}" font-size="11" fill="{MUTED}" text-anchor="middle">position de la France parmi les pays classés (plus à gauche = mieux)</text>')
    yy = y0 + 22
    for row in rows:
        dom, cls, rang, tend, ed = row
        da = H["det_attr"](headers or ["Domaine", "Classement", "Rang de la France", "Tendance", "Édition"], row, H["rowsrc"](row, fallback or H["CUR_FALLBACK"][0]))
        out.append(f'<g{da}><rect x="{M}" y="{yy}" width="{CW}" height="{rh}" fill="transparent"/>')
        out.append(f'<text x="{M}" y="{yy + 15}" font-size="12" font-weight="700" fill="{INK}">{esc(dom)}</text>')
        out.append(f'<text x="{M}" y="{yy + 28}" font-size="10.5" fill="{MUTED}">{esc(cls[:48])}</text>')
        mr = re.search(r"(\d+)e", rang); mn = re.search(r"\((\d+)", cls) or re.search(r"(\d+) pays", cls) or (re.search(r"(91)", "91") if "PISA" in cls else None)
        if "endetté" in rang: mr = re.search(r"(\d)e", rang); mn = re.search(r"\((\d+)", cls)
        col = CRIT if tend.lower().startswith(("en baisse", "dégradation", "en hausse", "léger recul")) else (GOOD if tend.lower().startswith("stable") else BLUE)
        out.append(f'<line x1="{M + labw}" y1="{yy + 16}" x2="{M + labw + plotw}" y2="{yy + 16}" stroke="{GRID}" stroke-width="6" stroke-linecap="round"/>')
        tip = esc(f"{dom} ({cls}) : {rang}. Tendance : {tend or 'non précisée'}. Édition : {ed}")
        if mr and mn:
            r, n = int(mr.group(1)), int(mn.group(1))
            x = M + labw + plotw * (r - 1) / max(n - 1, 1)
            out.append(f'<circle class="pt" data-tip="{tip}" cx="{x:.1f}" cy="{yy + 16}" r="8" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
            out.append(f'<text x="{M + labw + plotw + 12}" y="{yy + 20}" font-size="12" font-weight="700" fill="{INK}">{r}e sur {n}</text>')
        else:
            out.append(f'<g class="pt" data-tip="{tip}"><rect x="{M + labw}" y="{yy + 6}" width="{plotw}" height="20" fill="transparent"/></g>')
            out.append(f'<text x="{M + labw + plotw + 12}" y="{yy + 20}" font-size="12" font-weight="700" fill="{INK}">{esc(rang[:34])}</text>')
        tcol = CRIT if col == CRIT else (GOOD if col == GOOD else INK2)
        out.append(f'<text x="{M + labw + plotw + 12}" y="{yy + 32}" font-size="10.5" fill="{tcol}">{esc(tend[:40])}</text>')
        out.append('</g>')
        yy += rh
    H["y"] = yy + 6


def hbars(H, title, data, tips=None, color=None, labw=260, fmt=lambda v: f"{v:g}", unit="", sub=None, details=None, fallback=None, trend=None, ref=None):
    """Barres horizontales avec infobulle personnalisée par ligne (tips) ; sous-libellé optionnel (sub) par ligne."""
    out, M, CW = H["out"], H["M"], H["CW"]
    INK, INK2, MUTED, AXIS, BLUE = (H[k] for k in ("INK", "INK2", "MUTED", "AXIS", "BLUE"))
    esc = H["esc"]
    y0 = H["y"]
    out.append(f'<text x="{M}" y="{y0 + 14}" font-size="14" font-weight="700" fill="{INK}">{esc(title)}</text>')
    yy = y0 + 28; plotw = CW - labw - 90 - (280 if trend else 0) - (150 if sub else 0); vmax = max(v for _, v in data) or 1; bh = 16; gp = 8
    for i, (lab, v) in enumerate(data):
        bw = plotw * v / vmax
        c = color(i, lab) if color else BLUE
        out.append(f'<text x="{M + labw - 8}" y="{yy + 12}" font-size="12" fill="{INK2}" text-anchor="end">{esc(lab[:44])}</text>')
        tip = esc(tips[i] if tips else f"{lab} : {fmt(v)}{unit}")
        if details:
            hdr, row = details[0], details[1][i]
            da = H["det_attr"](hdr, row, H["rowsrc"](row, fallback or H["CUR_FALLBACK"][0]), titre=lab)
            out.append(f'<g{da} data-tip="{tip}"><rect x="{M}" y="{yy - 2}" width="{CW}" height="{bh + 4}" fill="transparent"/>')
        out.append(f'<rect class="bar" data-tip="{tip}" x="{M + labw}" y="{yy}" width="{max(bw,2):.1f}" height="{bh}" rx="3" fill="{c}"/>')
        out.append(f'<text x="{M + labw + bw + 6:.1f}" y="{yy + 12}" font-size="12" fill="{INK}">{esc(fmt(v) + unit)}</text>')
        if sub:
            out.append(f'<text x="{M + labw + bw + 6 + H["text_width"](fmt(v) + unit, 12) + 8:.1f}" y="{yy + 12}" font-size="10.5" fill="{MUTED}">{esc(sub[i])}</text>')
        if details:
            out.append('</g>')
        if trend:
            tl, tv = trend[0], trend[1][i]
            sx0 = M + CW - 150; sw = 130; mx = max(tv) or 1
            pts = [(sx0 + sw * k / (len(tv) - 1), yy + bh - 1 - (bh - 2) * v_ / mx) for k, v_ in enumerate(tv)]
            out.append('<polyline fill="none" stroke="#898781" stroke-width="1.8" points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '"/>')
            for k, ((a, b), v_) in enumerate(zip(pts, tv)):
                out.append(f'<circle class="pt" data-tip="{esc(lab)} · {tl[k]} : {v_} actions" cx="{a:.1f}" cy="{b:.1f}" r="3" fill="{c}"/>')
            out.append(f'<text x="{sx0 - 5}" y="{yy + 12}" font-size="10" fill="{MUTED}" text-anchor="end">{tv[0]}</text>')
            out.append(f'<text x="{sx0 + sw + 6}" y="{yy + 12}" font-size="10" fill="{INK}">{tv[-1]}</text>')
        yy += bh + gp
    if ref:
        rx = M + labw + plotw * ref[0] / vmax
        out.append(f'<line x1="{rx:.1f}" y1="{y0 + 22}" x2="{rx:.1f}" y2="{yy - gp + 4}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{rx + 5:.1f}" y="{yy + 10}" font-size="11.5" fill="{INK}">{esc(ref[1])}</text>')
        yy += 16
    if trend:
        out.append(f'<text x="{M + CW - 150}" y="{y0 + 24}" font-size="10.5" fill="{MUTED}">évolution {trend[0][0]} → {trend[0][-1]}</text>')
    out.append(f'<line x1="{M + labw}" y1="{y0 + 24}" x2="{M + labw}" y2="{yy - gp + 2}" stroke="{AXIS}"/>')
    H["y"] = yy + 4

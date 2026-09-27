#!/usr/bin/env python3
"""Duesluse v3 – tre moduler (A: rett spole, M: elektronikk, B: diamantspole) med svalehaleskjøt.
Lager 4 SVG-ark: oversikt + ett per modul. Mål i mm. Lokalt per modul: x 0..Lm, Y -75..75, Z 0..32 (gulv).
"""
import os
import math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
# ---------- felles geometri ----------
LANE = 110; FOOT = 20; HALF = 75; WALL_T = 2.4; FLOOR_T = 4; POCKET_D = 6; LID_T = 3
Z_FLOOR = 32; Z_POCKET0 = Z_FLOOR - FLOOR_T - POCKET_D            # 22
OPEN_H = 120; Z_ROOF = Z_FLOOR + OPEN_H; ROOF_T = 6; PANEL_T = 6; FOOT_T = 4
RAIL_B = 12; RAIL_T = 10; SLAT = 8; POST = 8
COIL = 100; DIAG = COIL * math.sqrt(2)
WALL_Y = [(-LANE / 2 - PANEL_T, -LANE / 2), (LANE / 2, LANE / 2 + PANEL_T)]
ROOF_Y0, ROOF_Y1 = WALL_Y[0][0], WALL_Y[1][1]
PCB_L, PCB_W = 60.0, 53.1; RDR_L, RDR_W = 45, 30
# svalehale (vertikal, skyves ned ovenfra): to per skjøt ved Y = ±48
DT_Y = (-48, 48); DT_BASE = 10; DT_TIP = 14; DT_DEPTH = 6; DT_CLR = 0.3; DT_H = Z_FLOOR - 2
BOB_N, BOB_PITCH, BOB_D, BOB_LEN = 5, 22, 6, 112
MODULES = [
    dict(key='A', title='MODUL A – RETT SPOLE (inngang)', L=110, coil='square', chamber=False, j0=None, j1='female', bobs=False, ramp=True),
    dict(key='M', title='MODUL M – ELEKTRONIKK (midt)', L=90, coil=None, chamber=True, j0='male', j1='male', bobs=False, ramp=False),
    dict(key='B', title='MODUL B – DIAMANTSPOLE (utgang, bobs)', L=150, coil='diamond', chamber=False, j0='female', j1=None, bobs=True, ramp=False),
]
def slats_for(L):
    n = max(2, round((L - 2 * POST + 22) / 30)); gap = (L - 2 * POST - n * SLAT) / (n + 1)
    while gap > 25: n += 1; gap = (L - 2 * POST - n * SLAT) / (n + 1)
    return [POST + gap + i * (SLAT + gap) for i in range(n)], gap
# ---------- SVG ----------
S = 2.0; out = []
def add(s): out.append(s)
def rect(x, y, w, h, fill='none', stroke='#222', sw=1.2, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''; o = f' opacity="{opacity}"' if opacity is not None else ''
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
def line(x1, y1, x2, y2, stroke='#222', sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def poly(pts, fill='none', stroke='#222', sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def circle(cx, cy, r, fill='none', stroke='#222', sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def text(x, y, s, size=12, anchor='start', fill='#111', weight='normal', rotate=None):
    r = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ''
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}"{r}>{s}</text>')
def lbl(x, y, s, size=10, fill='#111', anchor='start', weight='normal'):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="#fff" stroke="#fff" stroke-width="4" font-weight="{weight}">{s}</text>')
    text(x, y, s, size=size, anchor=anchor, fill=fill, weight=weight)
DIMC = '#1a4d8f'
def dim_h(x1, x2, y, label, ext_from=None, size=11):
    if ext_from is not None:
        for x in (x1, x2): line(x, ext_from, x, y + 4, stroke=DIMC, sw=0.7)
    line(x1, y, x2, y, stroke=DIMC, sw=0.9)
    for x in (x1, x2): line(x - 3, y + 3, x + 3, y - 3, stroke=DIMC, sw=1.1)
    text((x1 + x2) / 2, y - 4, label, size=size, anchor='middle', fill=DIMC)
def dim_v(y1, y2, x, label, ext_from=None, size=11, side='right'):
    if ext_from is not None:
        for y in (y1, y2): line(ext_from, y, x - 4 if side == 'right' else x + 4, y, stroke=DIMC, sw=0.7)
    line(x, y1, x, y2, stroke=DIMC, sw=0.9)
    for y in (y1, y2): line(x - 3, y + 3, x + 3, y - 3, stroke=DIMC, sw=1.1)
    tx = x + 4 if side == 'right' else x - 4
    text(tx, (y1 + y2) / 2, label, size=size, anchor='middle', fill=DIMC, rotate=-90 if side == 'right' else 90)
def group(tx, ty): add(f'<g transform="translate({tx:.1f},{ty:.1f})">')
def endg(): add('</g>')
C_BASE = '#e6e6e6'; C_WALL = '#cfdcec'; C_ROOF = '#efe3cf'; C_CH = '#e9efe6'; C_COIL = '#e07a10'; C_COIL2 = '#b5651d'; C_HID = '#777'; C_PCB = '#2e7d32'; C_DT = '#8e44ad'
def sheet_open(W, H, title, sub):
    out.clear()
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
    add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'); add(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#222" stroke-width="2"/>')
    text(30, 40, title, size=22, weight='bold'); text(30, 62, sub, size=12, fill='#333')
    text(W - 30, 40, 'PigeonPal · sluse v3', size=12, anchor='end', fill='#333'); text(W - 30, 58, 'Skala: 2 px/mm (detalj 6 px/mm)', size=11, anchor='end', fill='#555')
def sheet_close(name):
    add('</svg>'); p = OUT + name; open(p, 'w', encoding='utf-8').write('\n'.join(out)); print('skrev', p)

# ---------- svalehale-geometri i plan (lokale mm) ----------
def dovetail_male_pts(x_face, direction, yc):
    """Hann-list som stikker ut fra endeveggen ved x_face i retning direction (+1/-1)."""
    x_tip = x_face + direction * DT_DEPTH
    return [(x_face, yc - DT_BASE / 2), (x_tip, yc - DT_TIP / 2), (x_tip, yc + DT_TIP / 2), (x_face, yc + DT_BASE / 2)]
def dovetail_female_pts(x_face, direction, yc):
    """Hunn-spor inn i endeveggen/karet ved x_face, direction = inn i modulen."""
    c = DT_CLR; x_in = x_face + direction * (DT_DEPTH + c)
    return [(x_face, yc - DT_BASE / 2 - c), (x_in, yc - DT_TIP / 2 - c), (x_in, yc + DT_TIP / 2 + c), (x_face, yc + DT_BASE / 2 + c)]

# ---------- PLAN for én modul ----------
def plan_module(m, ox, oy, show_dims=True, title=True, labels=True):
    L = m['L']; slat_x, gap = slats_for(L)
    px = lambda x: x * S; py = lambda y: (y + HALF) * S
    group(ox, oy)
    if title: text(0, -34, f"PLAN – {m['title']}", size=13, weight='bold')
    rect(px(0), py(-HALF), L * S, 2 * HALF * S, fill=C_BASE)
    rect(px(0), py(-HALF), L * S, FOOT * S, fill='#dadada', stroke='#555'); rect(px(0), py(HALF - FOOT), L * S, FOOT * S, fill='#dadada', stroke='#555')
    if m['chamber']:
        rect(px(WALL_T), py(-HALF + WALL_T), (L - 2 * WALL_T) * S, (2 * HALF - 2 * WALL_T) * S, fill=C_CH, stroke=C_HID, dash='5,3')
        # PCB på tvers (53 langs Y ... legges 60 langs Y for plass), E1 mot -Y-siden
        rect(px(18), py(-66), PCB_W * S, PCB_L * S, stroke=C_PCB, sw=1.3, dash='6,3')
        if labels:
            text(px(34), py(-24), 'PCB 60×53', size=9, fill=C_PCB, weight='bold')
            text(px(34), py(-60), 'E1 ↑', size=8, fill=C_PCB); text(px(34), py(-9), 'J3/J4 ↓', size=8, fill=C_PCB)
        for (ry, lab) in ((8, 'Leser A'), (42, 'Leser B')):
            rect(px(22), py(ry), RDR_L * S, RDR_W * S, stroke=C_PCB, sw=1.3, dash='6,3')
            if labels: text(px(24), py(ry + 18), lab, size=9, fill=C_PCB)
        if labels: lbl(px(L / 2), py(-HALF) - 8, 'KAMMER under gulvet · innv. 85 × 145 × 25 · lokk fra undersiden', size=9, fill='#3a5a2a', anchor='middle', weight='bold')
        for yy in (-58, 58): circle(px(WALL_T), py(yy), 4 * S, dash='3,2', stroke=C_COIL); circle(px(L - WALL_T), py(yy), 4 * S, dash='3,2', stroke=C_COIL2)
        if labels: lbl(px(L / 2), py(HALF) + 12, 'kabelhull Ø8 i begge endevegger (Y = ±58)', size=8.5, fill='#444', anchor='middle')
    # føtter + vegger + skruer
    rect(px(0), py(-HALF), L * S, FOOT * S, fill='#dadada', stroke='#555'); rect(px(0), py(HALF - FOOT), L * S, FOOT * S, fill='#dadada', stroke='#555')
    for (y0, y1) in WALL_Y: rect(px(0), py(y0), L * S, PANEL_T * S, fill=C_WALL, stroke='#335')
    for hx in (10, L / 2, L - 10):
        for hy in (-68, 68): circle(px(hx), py(hy), 2.25 * S, stroke='#333')
    # tak
    for y0 in (ROOF_Y0, ROOF_Y1 - 6): rect(px(0), py(y0), L * S, 6 * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.8)
    for x0 in [0] + slat_x + [L - POST]: rect(px(x0), py(ROOF_Y0), SLAT * S, (ROOF_Y1 - ROOF_Y0) * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.6)
    # spole
    if m['coil'] == 'square':
        cx = L / 2; rect(px(cx - COIL / 2), py(-COIL / 2), COIL * S, COIL * S, stroke=C_COIL, sw=3.5, dash='9,5')
        lbl(px(cx), py(2), 'SPOLE A – rett', size=11, fill=C_COIL, anchor='middle', weight='bold'); lbl(px(cx), py(14), 'tråder på tvers', size=9, fill=C_COIL, anchor='middle')
        rect(px(cx - 20), py(-72), 40 * S, 18 * S, stroke=C_COIL, sw=1, dash='4,3'); lbl(px(cx - 18), py(-55), 'lomme kort 36×15', size=8.5, fill=C_COIL)
        line(px(cx + 20), py(-70), px(L), py(-58), stroke=C_COIL, sw=2, dash='3,2'); lbl(px(cx + 22), py(-62), 'kabel → M', size=8.5, fill=C_COIL)
    if m['coil'] == 'diamond':
        cx = L / 2; d = DIAG / 2
        poly([(px(cx + d), py(0)), (px(cx), py(d)), (px(cx - d), py(0)), (px(cx), py(-d))], stroke=C_COIL2, sw=3.5, dash='9,5')
        lbl(px(cx), py(2), 'SPOLE B – diamant 45°', size=11, fill=C_COIL2, anchor='middle', weight='bold'); lbl(px(cx), py(14), 'tråder på skrå', size=9, fill=C_COIL2, anchor='middle')
        rect(px(cx - 20), py(-72), 40 * S, 18 * S, stroke=C_COIL2, sw=1, dash='4,3'); lbl(px(cx - 18), py(-55), 'lomme kort 36×15', size=8.5, fill=C_COIL2)
        line(px(cx - 20), py(-70), px(0), py(-58), stroke=C_COIL2, sw=2, dash='3,2'); lbl(px(cx - 60), py(-62), 'kabel → M', size=8.5, fill=C_COIL2)
    # bobs
    if m['bobs']:
        bx = L - 12
        for i in range(BOB_N): circle(px(bx), py((i - (BOB_N - 1) / 2) * BOB_PITCH), BOB_D / 2 * S, fill='#fff', stroke='#111', sw=1.4)
        line(px(bx), py(ROOF_Y0), px(bx), py(ROOF_Y1), stroke='#111', sw=0.8, dash='2,2'); line(px(bx - 6), py(-LANE / 2), px(bx - 6), py(LANE / 2), stroke='#111', sw=2.5)
        lbl(px(bx - 10), py(66), 'stoppstang', size=8.5, anchor='end'); text(px(L + 8), py(-40), 'bobs ×5', size=9); text(px(L + 8), py(-30), 'deling 22', size=9)
    # svalehaler
    for (side, kind) in ((0, m['j0']), (1, m['j1'])):
        if not kind: continue
        x_face = 0 if side == 0 else L; dirn = 1 if side == 0 else -1
        for yc in DT_Y:
            if kind == 'male': poly([(px(x), py(y)) for x, y in dovetail_male_pts(x_face, -dirn, yc)], fill='#e8daef', stroke=C_DT, sw=1.3)
            else: poly([(px(x), py(y)) for x, y in dovetail_female_pts(x_face, dirn, yc)], fill='#fff', stroke=C_DT, sw=1.3)
        if labels: lbl(px(x_face + dirn * 16), py(-38 if kind == 'male' else -30), ('hann' if kind == 'male' else 'hunn') + ' ×2', size=8.5, fill=C_DT, anchor='middle')
    if m['ramp']:
        poly([(px(-40), py(-LANE / 2)), (px(0), py(-LANE / 2)), (px(0), py(LANE / 2)), (px(-40), py(LANE / 2))], fill='#f4f4f4', stroke='#333', dash='4,3')
        lbl(px(-20), py(2), 'rampe', size=9, anchor='middle', fill='#444'); lbl(px(-20), py(13), '(valgfri)', size=8, anchor='middle', fill='#444')
    if show_dims:
        dim_h(px(0), px(L), py(HALF) + 40, f'{L}', ext_from=py(HALF))
        if m['coil'] == 'square': dim_h(px(L / 2 - 50), px(L / 2 + 50), py(HALF) + 22, 'lomme 100', ext_from=py(HALF))
        if m['coil'] == 'diamond': dim_h(px(L / 2 - DIAG / 2), px(L / 2 + DIAG / 2), py(HALF) + 22, 'diagonal 141', ext_from=py(HALF))
        dim_v(py(-LANE / 2), py(LANE / 2), px(L) + 46, '110 innv.', ext_from=px(L)); dim_v(py(-HALF), py(HALF), px(L) + 72, '150', ext_from=px(L))
        dim_h(px(slat_x[0] + SLAT), px(slat_x[1]), py(HALF - FOOT) - 4, f'{gap:.0f}'); dim_h(px(slat_x[0]), px(slat_x[0] + SLAT), py(HALF - FOOT) - 18, '8')
    endg()

# ---------- LENGDESNITT for én modul (Y = 0) ----------
def section_module(m, ox, oy, title=True, dims=True):
    L = m['L']; slat_x, gap = slats_for(L)
    px = lambda x: x * S; pz = lambda z: (170 - z) * S
    group(ox, oy)
    if title: text(0, -14, f"LENGDESNITT A–A (Y = 0) – {m['title']}", size=13, weight='bold')
    rect(px(0), pz(Z_FLOOR + RAIL_B), L * S, RAIL_B * S, fill=C_WALL, stroke='#88a', sw=0.8); rect(px(0), pz(Z_ROOF), L * S, RAIL_T * S, fill=C_WALL, stroke='#88a', sw=0.8)
    for x0 in [0] + slat_x + [L - POST]: rect(px(x0), pz(Z_ROOF - RAIL_T), SLAT * S, (OPEN_H - RAIL_B - RAIL_T) * S, fill=C_WALL, stroke='#88a', sw=0.8)
    rect(px(0), pz(Z_FLOOR), L * S, FLOOR_T * S, fill=C_BASE, stroke='#333')
    for xw in (0, L - WALL_T): rect(px(xw), pz(Z_FLOOR - FLOOR_T), WALL_T * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    if m['chamber']:
        rect(px(WALL_T), pz(Z_FLOOR - FLOOR_T), (L - 2 * WALL_T) * S, (Z_FLOOR - FLOOR_T - LID_T) * S, fill=C_CH, stroke='#333', sw=0.6)
        rect(px(-1), pz(LID_T), (L + 2) * S, LID_T * S, fill='#c5dcbf', stroke='#333')
        rect(px(15), pz(LID_T + 5 + 1.6), 53.1 * S, 1.6 * S, fill=C_PCB, stroke=C_PCB)
        lbl(px(L / 2), pz(20) + 3, 'kammer 25 innv.', size=9, fill='#3a5a2a', anchor='middle'); lbl(px(L / 2), pz(13) + 3, 'PCB på 5 mm', size=8.5, fill='#3a5a2a', anchor='middle')
        lbl(px(L / 2), pz(-8) + 3, 'lokk 3 mm + pakning, skrus fra undersiden', size=8.5, fill='#3a5a2a', anchor='middle')
        for xh in (0, L): circle(px(xh), pz(10), 4 * S, dash='3,2', stroke='#444')
    else:
        rect(px(L / 2 - 1.2), pz(Z_FLOOR - FLOOR_T), 2.4 * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333', sw=0.8)
        w = COIL if m['coil'] == 'square' else DIAG; x0 = L / 2 - w / 2; col = C_COIL if m['coil'] == 'square' else C_COIL2
        rect(px(x0), pz(Z_FLOOR - FLOOR_T), w * S, POCKET_D * S, fill='#fff', stroke='#333')
        for xx in (x0, x0 + w - 2): rect(px(xx), pz(Z_POCKET0 + 2), 2 * S, 2 * S, fill=col, stroke=col)
        rect(px(x0 - 3), pz(Z_POCKET0), (w + 6) * S, 2 * S, fill='#bbb', stroke='#333', sw=0.8)
        lbl(px(L / 2), pz(Z_POCKET0 + 3) + 3, f'lomme {w:.0f} bred i Y=0 · sperrelist 2 mm', size=9, fill=col, anchor='middle')
        lbl(px(L / 2), pz(9) + 3, 'hult – står rett på landingsbrettet', size=9, fill='#444', anchor='middle')
    for x0 in [0] + slat_x + [L - POST]: rect(px(x0), pz(Z_ROOF + ROOF_T), SLAT * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    # svalehaler i snitt: vertikale lister/spor ved endene (vises som stiplede rektangler, Y=±48 er utenfor snittplanet)
    for (side, kind) in ((0, m['j0']), (1, m['j1'])):
        if not kind: continue
        x_face = 0 if side == 0 else L; dirn = 1 if side == 0 else -1
        if kind == 'male': rect(px(min(x_face, x_face - dirn * DT_DEPTH)), pz(DT_H + 2), DT_DEPTH * S, DT_H * S, fill='#e8daef', stroke=C_DT, dash='4,2')
        else: rect(px(min(x_face, x_face + dirn * DT_DEPTH)), pz(DT_H + 2), DT_DEPTH * S, DT_H * S, fill='#fff', stroke=C_DT, dash='4,2')
    if m['bobs']:
        bx = L - 12
        rect(px(bx - 3), pz(Z_ROOF - 4), 6 * S, BOB_LEN * S, fill='#fff', stroke='#111', sw=1.4); circle(px(bx), pz(Z_ROOF - 4), 1.7 * S, fill='#111')
        circle(px(bx - 6), pz(Z_FLOOR + 17), 3 * S, fill='#fff', stroke='#111', sw=1.4)
        lbl(px(bx - 8), pz(Z_ROOF + 4), 'aksel Ø3 rustfri', size=8.5, anchor='end'); lbl(px(bx - 10), pz(Z_FLOOR + 6), 'stopp', size=8.5, anchor='end')
    if m['coil'] == 'square':
        lx = L / 2; line(px(lx), pz(Z_FLOOR), px(lx + 8), pz(Z_FLOOR + 62), stroke='#7a4b1e', sw=3); line(px(lx - 9), pz(Z_FLOOR), px(lx + 9), pz(Z_FLOOR), stroke='#7a4b1e', sw=3)
        rect(px(lx - 3), pz(Z_FLOOR + 15), 8 * S, 8 * S, fill='#f5c26b', stroke='#7a4b1e', sw=1.2)
        lbl(px(lx + 14), pz(Z_FLOOR + 20), 'ring 5–10 over gulv → 9–14 til vikling', size=9, fill='#7a4b1e')
    if m['ramp']:
        poly([(px(-60), pz(0)), (px(0), pz(0)), (px(0), pz(Z_FLOOR))], fill='#f4f4f4', stroke='#333', dash='4,3'); lbl(px(-30), pz(-7) + 3, 'rampe (valgfri)', size=9, fill='#444', anchor='middle')
    if dims:
        dim_v(pz(Z_ROOF), pz(Z_FLOOR), px(L) + 44, '120', ext_from=px(L)); dim_v(pz(Z_FLOOR), pz(0), px(L) + 44, '32', ext_from=px(L))
        dim_h(px(0), px(L), pz(0) + 40, f'{L}', ext_from=pz(0))
    endg()

# ---------- TVERRSNITT midt i modulen ----------
def cross_module(m, ox, oy, title=True):
    L = m['L']
    px = lambda y: (y + HALF) * S; pz = lambda z: (170 - z) * S
    group(ox, oy)
    if title: text(0, -14, f"TVERRSNITT B–B (x = {L/2:.0f}) – {m['title']}", size=13, weight='bold')
    rect(px(-HALF), pz(Z_FLOOR), 2 * HALF * S, FLOOR_T * S, fill=C_BASE, stroke='#333')
    for yw in (-HALF, HALF - WALL_T): rect(px(yw), pz(Z_FLOOR - FLOOR_T), WALL_T * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    if m['chamber']:
        rect(px(-HALF + WALL_T), pz(Z_FLOOR - FLOOR_T), (2 * HALF - 2 * WALL_T) * S, (Z_FLOOR - FLOOR_T - LID_T) * S, fill=C_CH, stroke='#333', sw=0.6)
        rect(px(-HALF - 1), pz(LID_T), (2 * HALF + 2) * S, LID_T * S, fill='#c5dcbf', stroke='#333')
        rect(px(-64), pz(LID_T + 5 + 1.6), PCB_L * S, 1.6 * S, fill=C_PCB, stroke=C_PCB); text(px(-64), pz(LID_T + 8) - 2, 'PCB (E1 mot -Y)', size=8, fill=C_PCB)
        for ry in (-62, 34): rect(px(ry), pz(LID_T + 5 + 8), RDR_W * S, 8 * S, fill='none', stroke=C_PCB, dash='3,2');
        text(px(20), pz(LID_T + 16) - 2, 'lesermoduler', size=8, fill=C_PCB)
        lbl(px(0), pz(-8) + 3, 'lokk 3 mm + pakning (Ø2 silikonsnor i spor), M3 heat-set ×6', size=8.5, fill='#3a5a2a', anchor='middle')
    else:
        w = COIL if m['coil'] == 'square' else DIAG; col = C_COIL if m['coil'] == 'square' else C_COIL2
        rect(px(-w / 2), pz(Z_FLOOR - FLOOR_T), w * S, POCKET_D * S, fill='#fff', stroke='#333')
        for yy in (-w / 2, w / 2 - 2): rect(px(yy), pz(Z_POCKET0 + 2), 2 * S, 2 * S, fill=col, stroke=col)
        rect(px(-w / 2 - 3), pz(Z_POCKET0), (w + 6) * S, 2 * S, fill='#bbb', stroke='#333', sw=0.8)
        for rr in (-30, 30): rect(px(rr - 1.2), pz(Z_FLOOR - FLOOR_T), 2.4 * S, 10 * S, fill=C_BASE, stroke='#333', sw=0.7)
        lbl(px(0), pz(Z_POCKET0 + 3) + 3, f'lomme {w:.0f} bred · sperrelist under', size=9, fill=col, anchor='middle')
        lbl(px(0), pz(8) + 3, 'hult – åpent mot brettet', size=9, fill='#444', anchor='middle')
    for y0 in (-HALF, HALF - FOOT): rect(px(y0), pz(Z_FLOOR + FOOT_T), FOOT * S, FOOT_T * S, fill='#c0cfe0', stroke='#335')
    for (y0, y1) in WALL_Y: rect(px(y0), pz(Z_ROOF), PANEL_T * S, OPEN_H * S, fill=C_WALL, stroke='#335')
    rect(px(ROOF_Y0), pz(Z_ROOF + ROOF_T), (ROOF_Y1 - ROOF_Y0) * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    dim_h(px(-LANE / 2), px(LANE / 2), pz(Z_ROOF + ROOF_T) - 14, '110', ext_from=pz(Z_ROOF + ROOF_T))
    dim_h(px(-HALF), px(HALF), pz(0) + 40, '150', ext_from=pz(0))
    dim_v(pz(Z_ROOF), pz(Z_FLOOR), px(HALF) + 44, '120', ext_from=px(HALF)); dim_v(pz(Z_FLOOR), pz(0), px(HALF) + 44, '32', ext_from=px(HALF))
    endg()

# ---------- SVALEHALE-DETALJ ----------
def dovetail_detail(ox, oy):
    K = 5.0
    group(ox, oy)
    text(-40 * K, -30 * K, 'DETALJ – SVALEHALESKJØT (plan, 5 px/mm)', size=13, weight='bold'); text(-40 * K, -30 * K + 16, 'Skyves sammen ovenfra og ned.', size=11)
    # hunn-modul (venstre) med spor, hann-modul (høyre) med list; vist adskilt 8 mm
    gapx = 8
    # hunn: endevegg ved x=0 (lokalt), spor inn i -x
    rect(-40 * K, -20 * K, 40 * K, 40 * K, fill=C_BASE)
    f = dovetail_female_pts(0, -1, 0); poly([(x * K, y * K) for x, y in f], fill='#fff', stroke=C_DT, sw=1.6)
    rect(gapx * K, -20 * K, 40 * K, 40 * K, fill=C_BASE)
    mpts = dovetail_male_pts(gapx, -1, 0); poly([(x * K, y * K) for x, y in mpts], fill='#e8daef', stroke=C_DT, sw=1.6)
    text(-20 * K, -14 * K, 'modul A/B (hunn)', size=11, anchor='middle'); text((gapx + 20) * K, -14 * K, 'modul M (hann)', size=11, anchor='middle')
    dim_h(0, -DT_DEPTH * K, 12 * K, '6 dyp'); dim_v(-DT_BASE / 2 * K, DT_BASE / 2 * K, -22 * K, '10 hals', side='left'); dim_v(-DT_TIP / 2 * K, DT_TIP / 2 * K, -(DT_DEPTH + 10) * K, '14 topp', side='left')
    text(-20 * K, 17 * K, 'klaring 0,3 mm per side i sporet', size=10, anchor='middle', fill=C_DT)
    text((gapx + 20) * K, 17 * K, 'list 30 høy (Z 2–32), avrundet 0,5', size=10, anchor='middle', fill=C_DT)
    # snitt (side) av list + snapp-tapp
    group(-40 * K, 50 * K)
    text(0, -18 * K, 'SIDE (snitt): list i spor, snapp-tapp nederst', size=11, weight='bold')
    rect(0, -16 * K, 6 * K, 32 * K, fill='#fff', stroke='#333')               # sporet (i endeveggen)
    rect(0.3 * K, -14 * K, 5.4 * K, 30 * K, fill='#e8daef', stroke=C_DT)       # listen
    poly([(0, 14 * K), (2 * K, 14 * K), (0, 16 * K)], fill=C_DT, stroke=C_DT)  # snapp
    text(8 * K, 15 * K, 'snapp-tapp 1×2 mm: listen klikker forbi, låser mot løft', size=10, fill=C_DT)
    text(8 * K, -12 * K, 'Z 32 (gulv)', size=10); text(8 * K, 12 * K, 'Z 0', size=10)
    line(0, -16 * K, -2 * K, -16 * K, stroke='#333'); line(0, 16 * K, -2 * K, 16 * K, stroke='#333')
    endg()
    endg()

# ---------- PETG ----------
def petg(m):
    L = m['L']; rho = 1.27; slat_x, gap = slats_for(L)
    top = L * 2 * HALF * FLOOR_T; per = 2 * (L + 2 * HALF) * (Z_FLOOR - FLOOR_T) * WALL_T
    ribs = (2 * HALF) * (Z_FLOOR - FLOOR_T) * 2.4 + 2 * L * 10 * 2.4
    pockets = (4 * COIL) * POCKET_D * 2.4 if m['coil'] else 0
    lid = (L * 2 * HALF * LID_T) if m['chamber'] else 0
    wall = 2 * ((L * RAIL_B + L * RAIL_T + (len(slat_x) * SLAT + 2 * POST) * (OPEN_H - RAIL_B - RAIL_T)) * PANEL_T + L * FOOT * FOOT_T)
    roof = (2 * L * 6 + (len(slat_x) + 2) * SLAT * (ROOF_Y1 - ROOF_Y0)) * ROOF_T
    misc = (BOB_N * math.pi * 9 * BOB_LEN + math.pi * 9 * 122) if m['bobs'] else 0
    parts = [('Kar', (top + per + ribs + pockets) / 1000), ('Lokk', lid / 1000), ('Veggpaneler ×2', wall / 1000), ('Takpanel', roof / 1000), ('Bobs/stopp/lister', (misc + 2 * 2 * 10 * 120) / 1000)]
    return [(k, v, v * rho) for k, v in parts if v > 0]

# ---------- MODULARK ----------
def module_sheet(m):
    L = m['L']
    sheet_open(1700, 1250, f"DUESLUSE v3 – {m['title']}", 'Alle mål i mm · PETG, Bambu A1 · karet printes opp-ned i ett · svalehaleskjøt mot nabomodul')
    plan_module(m, 130, 130)
    section_module(m, 150, 600)
    cross_module(m, 800, 600)
    # deleliste + PETG
    group(1180, 130)
    text(0, 0, 'DELER I DENNE MODULEN', size=13, weight='bold'); y = 22
    rows = [('Kar', f'{L} × 150 × 32', 'opp-ned, skjørt'), ('Veggpanel ×2 m/ L-fot', f'{L} × 124 × 6', 'flatt på siden'), ('Takpanel', f'{L} × 122 × 6', 'flatt')]
    if m['chamber']: rows.insert(1, ('Kammerlokk m/ pakningsspor', f'{L+2} × 152 × 3', 'flatt'))
    if m['coil']: rows.append(('Sperrelister ×2', '2 × 10 × 120', 'liggende'))
    if m['bobs']: rows += [('Bobs ×5 / stoppstang', 'Ø6 × 112 / Ø6 × 122', 'liggende'), ('Svingaksel', 'Ø3 × 150 rustfri', 'kjøpes')]
    if m['ramp']: rows.append(('Rampe (valgfri)', '110 × 100 × 32', 'flatt'))
    for n, (a, b, c) in enumerate(rows, 1):
        text(0, y, str(n), size=11, weight='bold'); text(20, y, a, size=11); text(230, y, b, size=11); text(380, y, c, size=10, fill='#444'); y += 17
    y += 10; text(0, y, 'PETG-ESTIMAT', size=12, weight='bold'); y += 16; tot = 0
    for k, cm3, g in petg(m): text(0, y, k, size=10.5); text(230, y, f'{cm3:.0f} cm³', size=10.5); text(320, y, f'≈ {g:.0f} g', size=10.5); y += 15; tot += g
    text(0, y, f'Sum ≈ {tot:.0f} g', size=11, weight='bold'); y += 26
    text(0, y, 'NOTER', size=13, weight='bold'); y += 18
    notes = {
        'A': ['Spole A rett i lomme fra undersiden, tråder på tvers av løpet.', 'Kabel + kort (36×15) ut mot modul M gjennom notch Ø8 i endeveggen.', 'Hunn-svalehaler ×2 i enden mot M. Rampe valgfri ved inngangen.', 'Printes opp-ned: lomme og hulrom åpner oppover → ingen støtte.'],
        'M': ['Kammer 85 × 145 × 25 innv. under gulvet. Ingen spole → PCB kan ligge her.', 'Avstand til nærmeste vikling: ≥ 5 mm vegg + 5 mm lomme-margin i A/B', '≈ 10–15 mm til viklingens *hjørne* – lesermodulene legges i kammerets', 'ender (nær sin egen spole), PCB midt i, E1 mot -Y-siden (ut fra slaget).', 'Lokk fra undersiden med pakning; kabelhull Ø8 i begge endevegger.', 'Hann-svalehaler ×2 i begge ender.'],
        'B': ['Spole B som diamant (diagonal 141) – hjørnene under veggføttene.', 'Bobs ×5 i utgangen svinger bare innover; stoppstang på inngangssiden.', 'Hunn-svalehaler ×2 i enden mot M. Kabel ut mot M gjennom notch Ø8.'],
    }[m['key']]
    for n in notes: text(0, y, n, size=10.5); y += 15
    endg()
    sheet_close(f"duesluse_v3_modul_{m['key']}.svg")

# ---------- OVERSIKTSARK ----------
def overview_sheet():
    sheet_open(1900, 1400, 'DUESLUSE v3 – TRE MODULER MED SVALEHALESKJØT (oversikt)', 'A: rett spole (110) · M: elektronikk (90) · B: diamantspole + bobs (150) → 350 mm totalt · 150 bred · gulv 32 over brettet')
    # sammensatt plan
    group(120, 130); text(0, -34, 'PLAN – sammensatt (A | M | B), skjøter vist som stiplede linjer', size=13, weight='bold'); endg()
    x = 0
    for m in MODULES:
        plan_module(m, 120 + x * S, 130, show_dims=False, title=False, labels=False); x += m['L']
    group(120, 130)
    px = lambda x: x * S; py = lambda y: (y + HALF) * S
    for xj in (110, 200): line(px(xj), py(-HALF - 6), px(xj), py(HALF + 6), stroke=C_DT, sw=1.2, dash='6,3')
    lbl(px(110), py(-HALF - 10), 'skjøt A|M', size=9, fill=C_DT, anchor='middle'); lbl(px(200), py(-HALF - 10), 'skjøt M|B', size=9, fill=C_DT, anchor='middle')
    dim_h(px(0), px(110), py(HALF) + 22, 'A 110', ext_from=py(HALF)); dim_h(px(110), px(200), py(HALF) + 22, 'M 90', ext_from=py(HALF)); dim_h(px(200), px(350), py(HALF) + 22, 'B 150', ext_from=py(HALF))
    dim_h(px(0), px(350), py(HALF) + 42, '350', ext_from=py(HALF))
    dim_v(py(-LANE / 2), py(LANE / 2), px(350) + 46, '110 innv.', ext_from=px(350)); dim_v(py(-HALF), py(HALF), px(350) + 72, '150', ext_from=px(350))
    line(px(-44), py(24), px(-8), py(24), stroke='#111', sw=2); poly([(px(-6), py(24)), (px(-14), py(20)), (px(-14), py(28))], fill='#111'); text(px(-44), py(18), 'INN', size=11, weight='bold')
    text(px(350 + 8), py(20), 'UT', size=11, weight='bold')
    endg()
    # sammensatt lengdesnitt
    group(120, 600); text(0, -14, 'LENGDESNITT – sammensatt (Y = 0)', size=13, weight='bold'); endg()
    x = 0
    for m in MODULES:
        section_module(m, 120 + x * S, 600, title=False, dims=False); x += m['L']
    group(120, 600)
    pz = lambda z: (170 - z) * S
    for xj in (110, 200): line(px(xj), pz(Z_ROOF + ROOF_T + 6), px(xj), pz(-6), stroke=C_DT, sw=1.2, dash='6,3')
    dim_v(pz(Z_ROOF), pz(Z_FLOOR), px(350) + 44, '120', ext_from=px(350)); dim_v(pz(Z_FLOOR), pz(0), px(350) + 44, '32', ext_from=px(350))
    dim_h(px(0), px(350), pz(0) + 40, '350', ext_from=pz(0))
    endg()
    dovetail_detail(1420, 760)
    # oppsummering
    group(1330, 130)
    text(0, 0, 'SLIK HENGER DET SAMMEN', size=13, weight='bold'); y = 20
    for s in ['1. Sett modul M på brettet. Skyv A ned over hann-listene i M-enden', '   (svalehalene styrer, snapp-tappen låser mot løft). Samme med B.',
              '2. Før spolekablene fra A og B gjennom Ø8-hullene i M-veggene', '   FØR modulene skyves helt sammen. Koble til J3/J4.',
              '3. Skru veggpaneler (L-fot) og takpaneler på hver modul.', '4. Lokk under M sist, med pakning. Fest karene til brettet med', '   treskruer i føttene (≥ 15 mm fra nærmeste vikling).',
              '', 'Hvorfor tre moduler:', '• Spolene får 90 mm luft mellom seg → minimal innbyrdes kobling.',
              '• PCB ligger i en modul UTEN spole → ingen kobber under vikling.', '• Hver del ≤ 150 × 150 → små, stive print uten vridning.',
              '• Én spole i dag, to i morgen; bytt den modulen som svikter.', '', 'Total PETG ≈ ' + f"{sum(g for m in MODULES for _,_,g in petg(m)):.0f} g" + ' (~' + f"{sum(g for m in MODULES for _,_,g in petg(m))/1000*260:.0f}" + ' kr).',
              'Lengde 350 – test med pappmodell i slaget først.']:
        text(0, y, s, size=11); y += 16
    endg()
    sheet_close('duesluse_v3_oversikt.svg')

overview_sheet()
for m in MODULES: module_sheet(m)

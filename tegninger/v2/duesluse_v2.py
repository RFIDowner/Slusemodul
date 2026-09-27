#!/usr/bin/env python3
"""Duesluse v2 – to spoler (rett + diamant) og integrert sidekammer. Teknisk tegning som SVG.
X = gangretning (0 inngang, 250 utgang), Y = på tvers (0 senter, - = sidekammer), Z = opp (0 = underkant kar/lokk).
"""
import os
import math
# ---------------- GEOMETRI (mm) ----------------
L = 250; LANE = 110; FOOT = 20; HALF = LANE / 2 + FOOT          # 75
CH_W = 70; Y_OUT = -HALF - CH_W                                   # -145 (ytterkant kammer)
WALL_T = 2.4; SHELF_T = 3; FLOOR_T = 4; POCKET_D = 6; LID_T = 3
CH_IN_H = 26; Z_FLOOR = LID_T + CH_IN_H + SHELF_T                  # 32
Z_POCKET0 = Z_FLOOR - FLOOR_T - POCKET_D                          # 22
OPEN_H = 120; Z_ROOF = Z_FLOOR + OPEN_H                            # 152
ROOF_T = 6; PANEL_T = 6; FOOT_T = 4; RAIL_B = 12; RAIL_T = 10; SLAT = 8; POST = 8
COIL = 100; DIAG = COIL * math.sqrt(2)
A_X0, A_X1 = 6, 106; A_CX = 56                                    # spole A (rett)
B_CX = 176; B_D = DIAG / 2                                        # spole B (diamant) 105..247
CH_X0, CH_X1 = 30, 220                                            # kammer utvendig i X
CH_Y0, CH_Y1 = Y_OUT + WALL_T, -HALF - WALL_T                     # innvendig Y: -142.6 .. -77.4
BOB_N, BOB_PITCH, BOB_D, BOB_X, BOB_LEN = 5, 22, 6, 238, 112
Z_PIVOT = Z_ROOF - 4; STOP_X = 232; Z_STOP = Z_FLOOR + 17
PCB_L, PCB_W = 60.0, 53.1; RDR_L, RDR_W = 45, 30
WALL_Y = [(-LANE / 2 - PANEL_T, -LANE / 2), (LANE / 2, LANE / 2 + PANEL_T)]
ROOF_Y0, ROOF_Y1 = -LANE / 2 - PANEL_T, LANE / 2 + PANEL_T
n_slats = 7; gap = (L - 2 * POST - n_slats * SLAT) / (n_slats + 1)   # 22.25
slat_x = [POST + gap + i * (SLAT + gap) for i in range(n_slats)]
roof_slat_x = [0] + slat_x + [L - POST]
RAMP_L = 100
# ---------------- SVG ----------------
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
def label_bg(x, y, s, size=10, fill='#111', anchor='start', weight='normal'):
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
def leader_dims(px_edge, pz, items, x_text):
    """Små høydemål som leder-etiketter: items = [(z0,z1,label,text_y_px)]."""
    for (z0, z1, lab, ty) in items:
        line(px_edge, pz(z0), px_edge - 6, pz(z0), stroke=DIMC, sw=0.7); line(px_edge, pz(z1), px_edge - 6, pz(z1), stroke=DIMC, sw=0.7)
        line(px_edge - 6, pz(z0), px_edge - 6, pz(z1), stroke=DIMC, sw=0.9)
        line(px_edge - 6, pz((z0 + z1) / 2), x_text + 4, ty - 4, stroke=DIMC, sw=0.7)
        text(x_text, ty, lab, size=11, anchor='end', fill=DIMC)
def group(tx, ty): add(f'<g transform="translate({tx:.1f},{ty:.1f})">')
def endg(): add('</g>')
C_BASE = '#e6e6e6'; C_WALL = '#cfdcec'; C_ROOF = '#efe3cf'; C_BOX = '#d9ead3'; C_COIL = '#e07a10'; C_COIL2 = '#b5651d'
C_HID = '#777'; C_PCB = '#2e7d32'

def diamond_pts(cx, cy, d, fx, fy):
    return [(fx(cx + d), fy(cy)), (fx(cx), fy(cy + d)), (fx(cx - d), fy(cy)), (fx(cx), fy(cy - d))]

# ---------------- RISS 1: PLAN ----------------
def ppx(x): return x * S
def ppy(y): return (y - Y_OUT) * S          # Y_OUT (-145) øverst .. +75 nederst
def view_plan(ox, oy):
    group(ox, oy)
    text(0, -50, 'RISS 1 – PLAN (sett ovenfra). Tak gjennomsiktig; spoler stiplet = under gulvet; kammer stiplet = under hylla.', size=13, weight='bold')
    # Kar (hele basen) + hylle over kammer
    rect(ppx(0), ppy(Y_OUT), L * S, (HALF - Y_OUT) * S, fill=C_BASE)
    rect(ppx(0), ppy(Y_OUT), L * S, CH_W * S, fill='#e9efe6', stroke='#333')
    # Kammer innvendig (stiplet, under hylla)
    rect(ppx(CH_X0 + WALL_T), ppy(CH_Y0), (CH_X1 - CH_X0 - 2 * WALL_T) * S, (CH_Y1 - CH_Y0) * S, dash='5,3', stroke=C_HID, sw=1)
    label_bg(ppx(CH_X0 + 4), ppy(Y_OUT + 5), 'SIDEKAMMER under hylla · lokk fra undersiden · innv. 185 × 65 × 26', size=9.5, fill='#3a5a2a', weight='bold')
    # PCB: E1 mot yttervegg (-Y), J3/J4 mot løpet (+Y)
    pcb_x, pcb_y = 95, CH_Y0 + 9
    rect(ppx(pcb_x), ppy(pcb_y), PCB_L * S, PCB_W * S, stroke=C_PCB, sw=1.3, dash='6,3')
    text(ppx(pcb_x + 2), ppy(pcb_y + 5), 'E1 LTE ↑ mot yttervegg', size=8.5, fill=C_PCB)
    text(ppx(pcb_x + 2), ppy(pcb_y + 28), 'PigeonPal PCB 60×53', size=10, fill=C_PCB, weight='bold')
    text(ppx(pcb_x + 2), ppy(pcb_y + PCB_W - 2), 'J3/J4 ↓ mot løpet', size=8.5, fill=C_PCB)
    for (rx, lab) in ((CH_X0 + 8, 'Leser A'), (CH_X1 - 8 - RDR_L, 'Leser B')):
        ry = CH_Y0 + 9
        rect(ppx(rx), ppy(ry), RDR_L * S, RDR_W * S, stroke=C_PCB, sw=1.3, dash='6,3')
        text(ppx(rx + 2), ppy(ry + 12), lab + ' 125 kHz', size=9.5, fill=C_PCB); text(ppx(rx + 2), ppy(ry + 23), '(antatt 45×30×10)', size=8.5, fill=C_PCB)
    # Veggføtter + paneler
    rect(ppx(0), ppy(-HALF), L * S, FOOT * S, fill='#dadada', stroke='#555')
    rect(ppx(0), ppy(HALF - FOOT), L * S, FOOT * S, fill='#dadada', stroke='#555')
    for (y0, y1) in WALL_Y: rect(ppx(0), ppy(y0), L * S, PANEL_T * S, fill=C_WALL, stroke='#335')
    for hx in (8, 60, 125, 190, 242):
        for hy in (-68, 68): circle(ppx(hx), ppy(hy), 2.25 * S, stroke='#333')
    # Tak (full lengde, gjennomsiktig)
    for y0 in (ROOF_Y0, ROOF_Y1 - 6): rect(ppx(0), ppy(y0), L * S, 6 * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.8)
    for x0 in roof_slat_x: rect(ppx(x0), ppy(ROOF_Y0), SLAT * S, (ROOF_Y1 - ROOF_Y0) * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.6)
    label_bg(ppx(12), ppy(-46), 'TAKPANEL full lengde – spiler 8 / åpning 22', size=10, fill='#6b4f1d')
    # Spole A (rett) og B (diamant)
    rect(ppx(A_X0), ppy(-COIL / 2), COIL * S, COIL * S, stroke=C_COIL, sw=3.5, dash='9,5')
    poly(diamond_pts(B_CX, 0, B_D, ppx, ppy), stroke=C_COIL2, sw=3.5, dash='9,5')
    label_bg(ppx(A_CX), ppy(2), 'SPOLE A – rett', size=11, fill=C_COIL, anchor='middle', weight='bold')
    label_bg(ppx(A_CX), ppy(14), 'tråder på tvers av løpet', size=9, fill=C_COIL, anchor='middle')
    label_bg(ppx(B_CX), ppy(2), 'SPOLE B – diamant 45°', size=11, fill=C_COIL2, anchor='middle', weight='bold')
    label_bg(ppx(B_CX), ppy(14), 'tråder på skrå – dekker andre ringvinkler', size=9, fill=C_COIL2, anchor='middle')
    # Kabler til kammeret (gjennom skillevegg, stiplet)
    line(ppx(A_X0 + 4), ppy(-COIL / 2), ppx(A_X0 + 4), ppy(-HALF), stroke=C_COIL, sw=2, dash='3,2')
    line(ppx(A_X0 + 4), ppy(-HALF), ppx(CH_X0 + 12), ppy(CH_Y1 - 2), stroke=C_COIL, sw=2, dash='3,2')
    line(ppx(B_CX), ppy(-B_D), ppx(B_CX), ppy(-HALF), stroke=C_COIL2, sw=2, dash='3,2')
    line(ppx(B_CX), ppy(-HALF), ppx(CH_X1 - 12), ppy(CH_Y1 - 2), stroke=C_COIL2, sw=2, dash='3,2')
    label_bg(ppx(A_X0 + 8), ppy(-64), 'kabel A → hull Ø8 i skillevegg', size=8.5, fill=C_COIL)
    label_bg(ppx(B_CX + 4), ppy(-64), 'kabel B', size=8.5, fill=C_COIL2)
    rect(ppx(60), ppy(-72), 40 * S, 18 * S, stroke=C_COIL, sw=1, dash='4,3'); label_bg(ppx(62), ppy(-55), 'lomme kort 36×15', size=8.5, fill=C_COIL)
    rect(ppx(150), ppy(-72), 40 * S, 18 * S, stroke=C_COIL2, sw=1, dash='4,3'); label_bg(ppx(152), ppy(-55), 'lomme kort 36×15', size=8.5, fill=C_COIL2)
    # Bobs, aksel, stopp
    for i in range(BOB_N):
        circle(ppx(BOB_X), ppy((i - (BOB_N - 1) / 2) * BOB_PITCH), BOB_D / 2 * S, fill='#fff', stroke='#111', sw=1.4)
    line(ppx(BOB_X), ppy(ROOF_Y0), ppx(BOB_X), ppy(ROOF_Y1), stroke='#111', sw=0.8, dash='2,2')
    line(ppx(STOP_X), ppy(-LANE / 2), ppx(STOP_X), ppy(LANE / 2), stroke='#111', sw=2.5)
    text(ppx(L + 8), ppy(-52), 'bobs ×5 Ø6', size=9); text(ppx(L + 8), ppy(-42), 'deling 22', size=9)
    label_bg(ppx(STOP_X - 4), ppy(66), 'stoppstang Ø6', size=9, anchor='end')
    # Snittlinjer
    line(ppx(-6), ppy(0), ppx(L + 6), ppy(0), stroke='#111', sw=0.9, dash='12,4,3,4')
    text(ppx(-6), ppy(0) - 6, 'A', size=12, weight='bold', anchor='end'); text(ppx(L + 8), ppy(0) - 6, 'A', size=12, weight='bold')
    line(ppx(A_CX), ppy(Y_OUT - 6), ppx(A_CX), ppy(HALF + 6), stroke='#111', sw=0.9, dash='12,4,3,4')
    text(ppx(A_CX) + 6, ppy(Y_OUT) - 6, 'B', size=12, weight='bold'); text(ppx(A_CX) + 6, ppy(HALF) + 14, 'B', size=12, weight='bold')
    # Retning
    line(ppx(-44), ppy(24), ppx(-8), ppy(24), stroke='#111', sw=2); poly([(ppx(-6), ppy(24)), (ppx(-14), ppy(20)), (ppx(-14), ppy(28))], fill='#111')
    text(ppx(-44), ppy(18), 'INN', size=11, weight='bold'); text(ppx(-44), ppy(34), 'fra landingsbrett', size=9)
    text(ppx(L + 8), ppy(20), 'UT', size=11, weight='bold'); text(ppx(L + 8), ppy(32), 'til slaget', size=9)
    # Mål
    dim_h(ppx(0), ppx(L), ppy(HALF) + 40, '250', ext_from=ppy(HALF))
    dim_h(ppx(B_CX - B_D), ppx(B_CX + B_D), ppy(HALF) + 22, 'spole B diagonal 141', ext_from=ppy(HALF))
    dim_h(ppx(A_X0), ppx(A_X1), ppy(HALF) + 58, 'spole A 100', ext_from=ppy(HALF))
    dim_h(ppx(CH_X0), ppx(CH_X1), ppy(Y_OUT) - 28, 'kammer 190', ext_from=ppy(Y_OUT))
    dim_v(ppy(-LANE / 2), ppy(LANE / 2), ppx(L) + 46, '110 innv.', ext_from=ppx(L))
    dim_v(ppy(Y_OUT), ppy(HALF), ppx(L) + 74, '220', ext_from=ppx(L))
    dim_v(ppy(Y_OUT), ppy(-HALF), ppx(L) + 46, 'hylle 70', ext_from=ppx(L))
    dim_h(ppx(slat_x[0] + SLAT), ppx(slat_x[1]), ppy(HALF - FOOT) - 4, '22'); dim_h(ppx(slat_x[0]), ppx(slat_x[0] + SLAT), ppy(HALF - FOOT) - 18, '8')
    endg()

# ---------------- RISS 2: LENGDESNITT A–A ----------------
def spx(x): return x * S
def spz(z): return (170 - z) * S
def view_section(ox, oy):
    group(ox, oy)
    text(0, -14, 'RISS 2 – LENGDESNITT A–A gjennom løpets senter (Y = 0)', size=13, weight='bold')
    # bakre veggpanel
    rect(spx(0), spz(Z_FLOOR + RAIL_B), L * S, RAIL_B * S, fill=C_WALL, stroke='#88a', sw=0.8)
    rect(spx(0), spz(Z_ROOF), L * S, RAIL_T * S, fill=C_WALL, stroke='#88a', sw=0.8)
    for x0 in [0] + slat_x + [L - POST]:
        w = POST if x0 in (0, L - POST) else SLAT
        rect(spx(x0), spz(Z_ROOF - RAIL_T), w * S, (OPEN_H - RAIL_B - RAIL_T) * S, fill=C_WALL, stroke='#88a', sw=0.8)
    # Kar i snitt: gulv 4 mm, hult under (ribber), åpent mot brettet
    rect(spx(0), spz(Z_FLOOR), L * S, FLOOR_T * S, fill=C_BASE, stroke='#333')
    rect(spx(0), spz(Z_FLOOR - FLOOR_T), WALL_T * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    rect(spx(L - WALL_T), spz(Z_FLOOR - FLOOR_T), WALL_T * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    for rx in (125,):
        rect(spx(rx - 1.2), spz(Z_FLOOR - FLOOR_T), 2.4 * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    # Lommer (fra undersiden av gulvet): A rett 6..106; B diamant 105..247 (bredde i Y=0)
    for (x0, x1, col) in ((A_X0, A_X1, C_COIL), (B_CX - B_D, B_CX + B_D, C_COIL2)):
        rect(spx(x0), spz(Z_FLOOR - FLOOR_T), (x1 - x0) * S, POCKET_D * S, fill='#fff', stroke='#333')
        for xx in (x0, x1 - 2): rect(spx(xx), spz(Z_POCKET0 + 2), 2 * S, 2 * S, fill=col, stroke=col)
        # sperrelist 2 mm under lommen
        rect(spx(x0 - 3), spz(Z_POCKET0), (x1 - x0 + 6) * S, 2 * S, fill='#bbb', stroke='#333', sw=0.8)
    label_bg(spx(56), spz(Z_POCKET0 + 3) + 3, 'lomme A', size=9, fill=C_COIL, anchor='middle')
    label_bg(spx(176), spz(Z_POCKET0 + 3) + 3, 'lomme B (141 bred i Y=0)', size=9, fill=C_COIL2, anchor='middle')
    label_bg(spx(125), spz(10) + 3, 'hult under gulvet (ribber) – står rett på landingsbrettet', size=9.5, fill='#444', anchor='middle')
    label_bg(spx(30), spz(Z_FLOOR - 1.5) + 3, 'gulv 4 mm PETG', size=9.5, fill='#333')
    # Rampe (valgfri) ved inngang
    poly([(spx(-70), spz(0)), (spx(0), spz(0)), (spx(0), spz(Z_FLOOR))], fill='#f0f0f0', stroke='#333', dash='4,3')
    label_bg(spx(-36), spz(-7) + 3, 'rampe (valgfri), 100 lang', size=9, fill='#444', anchor='middle')
    # Tak
    for x0 in roof_slat_x: rect(spx(x0), spz(Z_ROOF + ROOF_T), SLAT * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    text(spx(125), spz(Z_ROOF + ROOF_T) - 6, 'takspiler 8, åpning 22 – full lengde', size=10, anchor='middle', fill='#6b4f1d')
    # Bobs, aksel, stopp
    rect(spx(BOB_X - BOB_D / 2), spz(Z_PIVOT), BOB_D * S, BOB_LEN * S, fill='#fff', stroke='#111', sw=1.4)
    circle(spx(BOB_X), spz(Z_PIVOT), 1.7 * S, fill='#111'); circle(spx(STOP_X), spz(Z_STOP), BOB_D / 2 * S, fill='#fff', stroke='#111', sw=1.4)
    label_bg(spx(BOB_X - 6), spz(Z_PIVOT + 8), 'svingaksel Ø3 rustfri', size=9, anchor='end')
    label_bg(spx(BOB_X + 7), spz(Z_STOP - 1), 'stopp Ø6', size=9)
    label_bg(spx(150), spz(110), 'bobs svinger kun innover →', size=9)
    # Duebein + ring over spole A
    lx = 56
    line(spx(lx), spz(Z_FLOOR), spx(lx + 8), spz(Z_FLOOR + 62), stroke='#7a4b1e', sw=3); line(spx(lx - 9), spz(Z_FLOOR), spx(lx + 9), spz(Z_FLOOR), stroke='#7a4b1e', sw=3)
    rect(spx(lx - 3), spz(Z_FLOOR + 15), 8 * S, 8 * S, fill='#f5c26b', stroke='#7a4b1e', sw=1.2)
    label_bg(spx(lx + 16), spz(Z_FLOOR + 24), 'chipring 5–10 mm over gulv', size=10, fill='#7a4b1e')
    label_bg(spx(lx + 16), spz(Z_FLOOR + 13), '→ 9–14 mm til vikling', size=10, fill='#7a4b1e', weight='bold')
    # Mål
    dim_v(spz(Z_ROOF), spz(Z_FLOOR), spx(L) + 44, '120 åpning', ext_from=spx(L))
    dim_v(spz(Z_FLOOR), spz(0), spx(L) + 44, '32', ext_from=spx(L))
    dim_v(spz(Z_ROOF + ROOF_T), spz(0), spx(L) + 72, '158 total', ext_from=spx(L))
    leader_dims(spx(0), spz, [(Z_FLOOR - FLOOR_T, Z_FLOOR, 'gulv 4', 196), (Z_POCKET0, Z_POCKET0 + POCKET_D, 'lomme 6', 218), (0, Z_POCKET0, 'hulrom 22', 240)], spx(-30))
    dim_h(spx(0), spx(L), spz(0) + 40, '250', ext_from=spz(0))
    endg()

# ---------------- RISS 3: TVERRSNITT B–B (gjennom spole A, X = 56) ----------------
def bpx(y): return (y - Y_OUT) * S
def bpz(z): return (170 - z) * S
def view_cross(ox, oy):
    group(ox, oy)
    text(0, -14, 'RISS 3 – TVERRSNITT B–B gjennom spole A (X = 56), sett fra inngangen', size=13, weight='bold')
    # Kammer: vegger, hylle, lokk under
    rect(bpx(Y_OUT), bpz(Z_FLOOR), CH_W * S, SHELF_T * S, fill='#e9efe6', stroke='#333')                       # hylle
    rect(bpx(Y_OUT), bpz(Z_FLOOR - SHELF_T), WALL_T * S, (Z_FLOOR - SHELF_T - LID_T) * S, fill='#e9efe6', stroke='#333')
    rect(bpx(-HALF - WALL_T), bpz(Z_FLOOR - SHELF_T), WALL_T * S, (Z_FLOOR - SHELF_T - LID_T) * S, fill='#e9efe6', stroke='#333')  # skillevegg
    rect(bpx(Y_OUT - 1), bpz(LID_T), (CH_W + 2) * S, LID_T * S, fill='#c5dcbf', stroke='#333')                    # lokk
    rect(bpx(Y_OUT + WALL_T + 2), bpz(LID_T + 1.6), (CH_W - 2 * WALL_T - 4) * S, 1.6 * S, fill='#cfc', stroke='#333', sw=0.6)  # pakning
    label_bg(bpx(Y_OUT + CH_W / 2), bpz(Z_FLOOR - SHELF_T - 5) + 3, 'SIDEKAMMER 26 innv.', size=10, fill='#3a5a2a', anchor='middle', weight='bold')
    label_bg(bpx(Y_OUT + CH_W / 2), bpz(15) + 3, 'PCB på 5 mm avstandsstykker', size=8.5, fill='#3a5a2a', anchor='middle')
    label_bg(bpx(Y_OUT + 2), bpz(-26) + 3, 'lokk 3 mm + pakning, skrus fra undersiden', size=8.5, fill='#3a5a2a')
    # PCB i snitt (liggende) + E1 mot yttervegg
    rect(bpx(CH_Y0 + 6), bpz(LID_T + 5 + 1.6), PCB_W * S, 1.6 * S, fill=C_PCB, stroke=C_PCB)
    text(bpx(CH_Y0 + 6), bpz(LID_T + 5 + 1.6) - 3, 'E1', size=8, fill=C_PCB)
    # Løp: gulv, hulrom, føtter, vegger, tak
    rect(bpx(-HALF), bpz(Z_FLOOR), 2 * HALF * S, FLOOR_T * S, fill=C_BASE, stroke='#333')
    rect(bpx(HALF - WALL_T), bpz(Z_FLOOR - FLOOR_T), WALL_T * S, (Z_FLOOR - FLOOR_T) * S, fill=C_BASE, stroke='#333')
    for rr in (-30, 30): rect(bpx(rr - 1.2), bpz(Z_FLOOR - FLOOR_T), 2.4 * S, 10 * S, fill=C_BASE, stroke='#333', sw=0.7)   # korte ribber
    # Lomme A i tverrsnitt (bredde 100), vikling 2×2 i kantene, sperrelist
    rect(bpx(-COIL / 2), bpz(Z_FLOOR - FLOOR_T), COIL * S, POCKET_D * S, fill='#fff', stroke='#333')
    for yy in (-COIL / 2, COIL / 2 - 2): rect(bpx(yy), bpz(Z_POCKET0 + 2), 2 * S, 2 * S, fill=C_COIL, stroke=C_COIL)
    rect(bpx(-COIL / 2 - 3), bpz(Z_POCKET0), (COIL + 6) * S, 2 * S, fill='#bbb', stroke='#333', sw=0.8)
    label_bg(bpx(0), bpz(Z_POCKET0 + 3) + 3, 'spole A i lomme · sperrelist 2 mm under', size=9, fill=C_COIL, anchor='middle')
    label_bg(bpx(0), bpz(8) + 3, 'hult – åpent mot landingsbrettet', size=9, fill='#444', anchor='middle')
    for y0 in (-HALF, HALF - FOOT): rect(bpx(y0), bpz(Z_FLOOR + FOOT_T), FOOT * S, FOOT_T * S, fill='#c0cfe0', stroke='#335')
    for (y0, y1) in WALL_Y: rect(bpx(y0), bpz(Z_ROOF), PANEL_T * S, OPEN_H * S, fill=C_WALL, stroke='#335')
    rect(bpx(ROOF_Y0), bpz(Z_ROOF + ROOF_T), (ROOF_Y1 - ROOF_Y0) * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    for i in range(BOB_N):
        y = (i - (BOB_N - 1) / 2) * BOB_PITCH
        rect(bpx(y - BOB_D / 2), bpz(Z_PIVOT), BOB_D * S, BOB_LEN * S, fill='#fff', stroke='#111', sw=1.0)
    line(bpx(ROOF_Y0), bpz(Z_PIVOT), bpx(ROOF_Y1), bpz(Z_PIVOT), stroke='#111', sw=1.4)
    label_bg(bpx(0), bpz(Z_ROOF - 14), 'bobs i utgangen (bak)', size=10, anchor='middle')
    # Mål
    dim_h(bpx(-LANE / 2), bpx(LANE / 2), bpz(Z_ROOF + ROOF_T) - 14, '110', ext_from=bpz(Z_ROOF + ROOF_T))
    dim_h(bpx(Y_OUT), bpx(HALF), bpz(0) + 84, '220', ext_from=bpz(0))
    dim_h(bpx(Y_OUT), bpx(-HALF), bpz(0) + 66, '70', ext_from=bpz(0))
    dim_h(bpx(-HALF), bpx(HALF), bpz(0) + 66, '150', ext_from=bpz(0))
    dim_v(bpz(Z_ROOF), bpz(Z_FLOOR), bpx(HALF) + 44, '120', ext_from=bpx(HALF))
    dim_v(bpz(Z_FLOOR), bpz(0), bpx(HALF) + 44, '32', ext_from=bpx(HALF))
    endg()

# ---------------- RISS 4: ISOMETRISK ----------------
SI = 1.15; C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
def iso(x, y, z): return ((x - y) * C30 * SI, ((x + y) * S30 - z) * SI)
def shade(hexc, f):
    h = hexc.lstrip('#'); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return '#%02x%02x%02x' % (int(r * f), int(g * f), int(b * f))
def box3d(x0, x1, y0, y1, z0, z1, fill, stroke='#333', sw=0.9):
    poly([iso(x0, y1, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x0, y1, z1)], fill=shade(fill, 0.85), stroke=stroke, sw=sw)
    poly([iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)], fill=shade(fill, 0.72), stroke=stroke, sw=sw)
    poly([iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)], fill=fill, stroke=stroke, sw=sw)
def wall3d(y0, y1, dz):
    zb = Z_FLOOR + dz
    box3d(0, L, y0, y1, zb, zb + RAIL_B, C_WALL)
    for x0 in [0] + slat_x + [L - POST]:
        w = POST if x0 in (0, L - POST) else SLAT
        box3d(x0, x0 + w, y0, y1, zb + RAIL_B, zb + OPEN_H - RAIL_T, C_WALL)
    box3d(0, L, y0, y1, zb + OPEN_H - RAIL_T, zb + OPEN_H, C_WALL)
def view_iso(ox, oy):
    group(ox, oy)
    text(0, -14, 'RISS 4 – ISOMETRISK EKSPLOSJONSRISS', size=13, weight='bold')
    group(300, 640)
    box3d(0, L, Y_OUT, HALF, 0, Z_FLOOR, C_BASE)                                   # karet
    box3d(CH_X0, CH_X1, Y_OUT, -HALF, Z_FLOOR, Z_FLOOR + 0.6, '#e9efe6')            # hyllemarkering
    rect_pts = [iso(A_X0, -COIL / 2, Z_FLOOR + 0.5), iso(A_X1, -COIL / 2, Z_FLOOR + 0.5), iso(A_X1, COIL / 2, Z_FLOOR + 0.5), iso(A_X0, COIL / 2, Z_FLOOR + 0.5)]
    poly(rect_pts, stroke=C_COIL, sw=2.5, dash='7,4')
    poly([iso(B_CX + B_D, 0, Z_FLOOR + 0.5), iso(B_CX, B_D, Z_FLOOR + 0.5), iso(B_CX - B_D, 0, Z_FLOOR + 0.5), iso(B_CX, -B_D, Z_FLOOR + 0.5)], stroke=C_COIL2, sw=2.5, dash='7,4')
    box3d(CH_X0 + 2, CH_X1 - 2, Y_OUT + 1, -HALF - 1, -40, -40 + LID_T, '#c5dcbf')  # lokk senket under kammeret
    for y0 in (-HALF, HALF - FOOT): box3d(0, L, y0, y0 + FOOT, Z_FLOOR, Z_FLOOR + FOOT_T, '#c0cfe0')
    wall3d(WALL_Y[0][0], WALL_Y[0][1], 70)
    for i in range(BOB_N):
        y = (i - (BOB_N - 1) / 2) * BOB_PITCH
        box3d(BOB_X - 3, BOB_X + 3, y - 3, y + 3, Z_PIVOT - BOB_LEN + 70, Z_PIVOT + 70, '#ffffff')
    wall3d(WALL_Y[1][0], WALL_Y[1][1], 70)
    dzr = 150
    for y0 in (ROOF_Y0, ROOF_Y1 - 6): box3d(0, L, y0, y0 + 6, Z_ROOF + dzr, Z_ROOF + dzr + ROOF_T, C_ROOF)
    for x0 in roof_slat_x: box3d(x0, x0 + SLAT, ROOF_Y0, ROOF_Y1, Z_ROOF + dzr, Z_ROOF + dzr + ROOF_T, C_ROOF)
    endg()
    y = 1010
    for s in ('Karet (250 × 220 × 32) printes opp-ned i ett: gulv og hylle på printbedet,',
              'spolelommer og kammer åpner oppover → ingen støtte. Lokket under kammeret (senket',
              'i risset) skrus fra undersiden. Veggpaneler og tak løftet. Karet er hult og åpent nedover.'):
        text(200, y, s, size=10); y += 15
    endg()

# ---------------- DELELISTE + NOTER + PETG ----------------
def petg_estimate():
    rho = 1.27  # g/cm3
    v = {}
    top = (L * (HALF - Y_OUT) - CH_W * L) * FLOOR_T + CH_W * L * SHELF_T            # gulv 4 + hylle 3
    per = 2 * (L + (HALF - Y_OUT)) * (Z_FLOOR - FLOOR_T) * WALL_T                    # ytre kar-vegger
    inner = (L * (Z_FLOOR - SHELF_T - LID_T) * WALL_T)                              # skillevegg kammer
    ribs = 3 * (2 * HALF) * (Z_FLOOR - FLOOR_T) * 2.4 + 2 * (L) * 10 * 2.4          # ribber under gulv
    pockets = (2 * (COIL + DIAG) + 40) * POCKET_D * 2.4                              # lommevegger
    v['Kar'] = (top + per + inner + ribs + pockets) / 1000
    v['Lokk'] = (CH_X1 - CH_X0) * (CH_W + 2) * LID_T / 1000
    wall = (L * RAIL_B + L * RAIL_T + (n_slats * SLAT + 2 * POST) * (OPEN_H - RAIL_B - RAIL_T)) * PANEL_T + L * FOOT * FOOT_T
    v['Veggpaneler ×2'] = 2 * wall / 1000
    roof = (2 * L * 6 + len(roof_slat_x) * SLAT * (ROOF_Y1 - ROOF_Y0)) * ROOF_T
    v['Takpanel'] = roof / 1000
    v['Bobs, stopp, sperrelister'] = (BOB_N * math.pi * 9 * BOB_LEN + math.pi * 9 * 122 + 4 * 2 * 10 * 120) / 1000
    v['Rampe (valgfri)'] = (0.5 * RAMP_L * Z_FLOOR * LANE * 0.35) / 1000            # hul rampe ~35 % fylt
    tot = 0
    rows = []
    for k, cm3 in v.items():
        g = cm3 * rho; tot += g; rows.append((k, cm3, g))
    return rows, tot

def view_notes(ox, oy):
    group(ox, oy)
    text(0, 0, 'DELELISTE (alle deler innenfor Bambu A1 256×256×256, PETG)', size=13, weight='bold')
    rows = [
        ('1', 'Kar: gulv, spolelommer, sidekammer, ribber', '250 × 220 × 32', 'opp-ned (gulv på bedet), skjørt – ikke brim'),
        ('2', 'Kammerlokk m/ pakningsspor', '192 × 72 × 3', 'flatt'),
        ('3', 'Veggpanel m/ L-fot ×2', '250 × 124 × 6 (+ fot 20 × 4)', 'flatt på siden'),
        ('4', 'Takpanel (spiler), full lengde', '250 × 122 × 6', 'flatt'),
        ('5', 'Bobs ×5 / stoppstang / sperrelister ×4', 'Ø6 × 112 / Ø6 × 122 / 2 × 10 × 120', 'liggende'),
        ('6', 'Svingaksel', 'Ø3 × 150 rustfri/messing', 'kjøpes'),
        ('7', 'Rampe ved inngang (valgfri)', '110 × 100 × 32', 'flatt'),
        ('8', 'Skruer / pakning', 'M3 heat-set ×8, treskruer 4 × 30 ×10, Ø2 silikonsnor 55 cm', 'kjøpes'),
    ]
    y = 22
    for n, name, dims, orient in rows:
        text(0, y, n, size=11, weight='bold'); text(24, y, name, size=11); text(330, y, dims, size=11); text(640, y, orient, size=10, fill='#444'); y += 17
    y += 10
    text(0, y, 'PETG-ESTIMAT (geometrisk volum × 1,27 g/cm³; slicer med 3 vegger/15 % infill gir tilsvarende siden nesten alt er tynne skall)', size=12, weight='bold'); y += 17
    rows2, tot = petg_estimate()
    for k, cm3, g in rows2:
        text(0, y, f'{k}', size=10.5); text(330, y, f'{cm3:.0f} cm³', size=10.5); text(420, y, f'≈ {g:.0f} g', size=10.5); y += 15
    text(0, y, f'Sum ≈ {tot:.0f} g (~{tot/1000*260:.0f} kr ved 260 kr/kg). Karet dominerer; gulvet på 4 mm er 60 % av det – ikke stedet å spare.', size=10.5, weight='bold'); y += 22
    text(0, y, 'NOTER', size=13, weight='bold'); y += 18
    notes = [
        'A. To spoler med ULIK orientering: A rett (tråder på tvers), B diamant. De feiler på forskjellige ringvinkler → reell redundans, ikke bare dobbelt opp.',
        '   Leses A før B = dua kom inn (retning). Firmware: dedup samme chip-ID fra begge portene innen ~10 s; backend beholder "først sett".',
        'B. Spolene ligger i lommer fra undersiden av 4 mm gulv (ring→vikling 9–14 mm). Sperrelister (2 mm) under lommene holder spolene; ingen bunnplate.',
        'C. Sidekammeret er skilt fra hulrommet under løpet med en vegg (2,4 mm) – to hull Ø8 for spolekablene. Kammeret får eget lokk under, med pakning.',
        'D. Elektronikk ≥ 5 cm fra nærmeste vikling: PCB mot ytterveggen (E1/LTE ut), lesermodulene i kammerets ender mot ytterveggen. Diamantens hjørne',
        '   (Y = −70,7) er ~10 mm fra skilleveggen – legg leser B i kammerets ytre halvdel. Lesermodulenes mål er ANTATT 45×30×10 – juster.',
        'E. Karet printes opp-ned: gulv/hylle på bedet gir glatt gulv; lommer, kammer og hulrom åpner oppover → ingen støtte. 250 × 220 på 256-bed: bruk skjørt.',
        'F. Gulvet ligger 32 mm over landingsbrettet. Dua stepper det lett; rampe (del 7) er valgfri. Innsiden i slaget: 32 mm trinn ned.',
        'G. Interferens A↔B (spolene ligger inntil hverandre): tidsdel 5V til J3/J4 i firmware (~100 ms vekselvis) hvis samtidig drift gir feillesing. Testes.',
        'H. Bobs i utgangen svinger bare innover (stoppstang på inngangssiden). Tak i full lengde: dua må GÅ over begge spolene, kan ikke hoppe ut før bobs-ene.',
        'I. Ingen metall over/rundt spolene: aksel og skruer nær spolesonene i rustfri/messing/nylon. Treskruene sitter i føttene, ≥ 15 mm fra nærmeste vikling.',
    ]
    for n in notes: text(0, y, n, size=10.5); y += 15
    endg()

# ---------------- ARK ----------------
W, H = 1900, 1760
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>'); add(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#222" stroke-width="2"/>')
text(30, 40, 'DUESLUSE v2 – TO SPOLER (rett + diamant) OG INTEGRERT SIDEKAMMER', size=22, weight='bold')
text(30, 62, 'Teknisk tegning · alle mål i mm · PETG, Bambu Lab A1 · karet printes i ett, opp-ned · spoler i lommer under 4 mm gulv · lokk under kammeret', size=12, fill='#333')
text(W - 30, 40, 'PigeonPal · sluse v2', size=12, anchor='end', fill='#333'); text(W - 30, 58, 'Skala: 2 px/mm i riss 1–3', size=11, anchor='end', fill='#555')
view_plan(130, 140)
view_section(150, 760)
view_end = view_cross
view_cross(760, 760)
view_iso(1080, 110)
view_notes(60, 1190)
add('</svg>')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'duesluse_v2.svg')
open(path, 'w', encoding='utf-8').write('\n'.join(out)); print('skrev', path)

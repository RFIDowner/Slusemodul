#!/usr/bin/env python3
"""Teknisk tegning (SVG) av duesluse med innebygd 10x10 cm 125 kHz-spole.
Mål i mm. X = gangretning (0 = inngang fra landingsbrett, 200 = utgang mot slag),
Y = på tvers (0 = senter, - = side med elektronikkboks), Z = opp (0 = underkant bunndeksel).
"""
import os
import math

# ---------------- GEOMETRI (mm) ----------------
L = 200; LANE = 110; FOOT = 20
BASE_W = LANE + 2 * FOOT; HALF = BASE_W / 2          # 150 / 75
COVER_T = 3; POCKET_D = 6; FLOOR_T = 4
PLATE_T = POCKET_D + FLOOR_T                          # 10
Z_FLOOR = COVER_T + PLATE_T                           # 13
OPEN_H = 120; Z_ROOF = Z_FLOOR + OPEN_H               # 133
ROOF_T = 6; PANEL_T = 6; FOOT_T = 4
RAIL_B = 12; RAIL_T = 10; SLAT = 8; GAP = 24; POST = 8
ROOF_L = 150
COIL = 100; DIAG = COIL * math.sqrt(2)                # 141.4
BOB_N = 5; BOB_PITCH = 22; BOB_D = 6; BOB_X = 188; BOB_LEN = 112
Z_PIVOT = Z_ROOF - 4; STOP_X = 182; Z_STOP = 30
BOX_L, BOX_W, BOX_H, LID_T = 130, 80, 42, 3
BOX_X0 = (L - BOX_L) / 2; BOX_Y0 = -HALF - BOX_W; BOX_Y1 = -HALF
PCB_L, PCB_W = 60.0, 53.1
RDR_L, RDR_W = 45, 30                                 # ANTATT lesermodul
WALL_Y = [(-LANE / 2 - PANEL_T, -LANE / 2), (LANE / 2, LANE / 2 + PANEL_T)]   # (-61,-55) og (55,61)
ROOF_Y0, ROOF_Y1 = -LANE / 2 - PANEL_T, LANE / 2 + PANEL_T                    # -61..61 (122)
slat_x = [32, 64, 96, 128, 160]
roof_slat_x = [0, 32, 64, 96, 128, 142]

# ---------------- SVG-HJELPERE ----------------
S = 2.0
out = []
def add(s): out.append(s)
def rect(x, y, w, h, fill='none', stroke='#222', sw=1.2, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' opacity="{opacity}"' if opacity is not None else ''
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
    """Tekst med hvit bakgrunn (halo) for lesbarhet oppå tegning."""
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
    # rotate(-90) om eget punkt: teksten leses nedenfra og opp
def group(tx, ty): add(f'<g transform="translate({tx:.1f},{ty:.1f})">')
def endg(): add('</g>')

C_BASE = '#e6e6e6'; C_WALL = '#cfdcec'; C_ROOF = '#efe3cf'; C_BOX = '#d9ead3'; C_COIL = '#e07a10'
C_HID = '#777'; C_PCB = '#2e7d32'

# ---------------- RISS 1: PLAN ----------------
def plan_px(x): return x * S
def plan_py(y): return (y + 155) * S
def view_plan(ox, oy):
    group(ox, oy)
    text(0, -40, 'RISS 1 – PLAN (sett ovenfra). Tak vist gjennomsiktig; spole stiplet = under gulvet.', size=13, weight='bold')
    # Elektronikkboks
    rect(plan_px(BOX_X0), plan_py(BOX_Y0), BOX_L * S, BOX_W * S, fill=C_BOX)
    rect(plan_px(BOX_X0 + 4), plan_py(BOX_Y0 + 4), (BOX_L - 8) * S, (BOX_W - 8) * S, dash='4,3', stroke=C_HID, sw=0.8)
    pcb_x, pcb_y = BOX_X0 + 6, BOX_Y0 + 9
    rect(plan_px(pcb_x), plan_py(pcb_y), PCB_L * S, PCB_W * S, stroke=C_PCB, sw=1.3, dash='6,3')
    text(plan_px(pcb_x + 2), plan_py(pcb_y - 2), 'E1 LTE-antenne: denne kanten ut ↑', size=9, fill=C_PCB)
    text(plan_px(pcb_x + 2), plan_py(pcb_y + 26), 'PigeonPal PCB 60×53', size=10, fill=C_PCB, weight='bold')
    text(plan_px(pcb_x + 2), plan_py(pcb_y + PCB_W + 6), 'J3/J4 RFID-kontakter: mot slusa ↓', size=9, fill=C_PCB)
    rx, ry = BOX_X0 + 78, BOX_Y0 + 24
    rect(plan_px(rx), plan_py(ry), RDR_L * S, RDR_W * S, stroke=C_PCB, sw=1.3, dash='6,3')
    text(plan_px(rx + 2), plan_py(ry + 12), 'Lesermodul 125 kHz', size=10, fill=C_PCB)
    text(plan_px(rx + 2), plan_py(ry + 23), '(antatt 45×30×10)', size=9, fill=C_PCB)
    circle(plan_px(100), plan_py(BOX_Y1 - 3), 6 * S, dash='3,2', stroke=C_HID)
    text(plan_px(114), plan_py(BOX_Y1 - 9), 'kabelnippel PG7 (Ø12,5)', size=9, fill=C_HID)
    for bx in (BOX_X0 + 10, BOX_X0 + BOX_L - 10):
        circle(plan_px(bx), plan_py(BOX_Y0 + BOX_W - 6), 2.2 * S, stroke=C_HID)
    # Bunnplate + veggføtter + veggpaneler
    rect(plan_px(0), plan_py(-HALF), L * S, BASE_W * S, fill=C_BASE)
    rect(plan_px(0), plan_py(-HALF), L * S, FOOT * S, fill='#dadada', stroke='#555')
    rect(plan_px(0), plan_py(HALF - FOOT), L * S, FOOT * S, fill='#dadada', stroke='#555')
    for (y0, y1) in WALL_Y:
        rect(plan_px(0), plan_py(y0), L * S, PANEL_T * S, fill=C_WALL, stroke='#335')
    # Fotskruer + monteringshull
    for (hx, hy) in ((8, -68), (8, 68), (192, -68), (192, 68), (60, -68), (140, -68), (60, 68), (140, 68)):
        circle(plan_px(hx), plan_py(hy), 2.25 * S, stroke='#333')
    # Takpanel (gjennomsiktig)
    for y0 in (ROOF_Y0, ROOF_Y1 - 6):
        rect(plan_px(0), plan_py(y0), ROOF_L * S, 6 * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.8)
    for x0 in roof_slat_x:
        rect(plan_px(x0), plan_py(ROOF_Y0), SLAT * S, (ROOF_Y1 - ROOF_Y0) * S, fill=C_ROOF, stroke='#8a6d3b', sw=0.9, opacity=0.65)
    label_bg(plan_px(12), plan_py(-46), 'TAKPANEL (spiler 8 / åpning 24) – kan printes 200 lang', size=10, fill='#6b4f1d')
    # Spole (diamant) – tegnes sist for lesbarhet
    cx, cy, d = 100, 0, DIAG / 2
    poly([(plan_px(cx + d), plan_py(cy)), (plan_px(cx), plan_py(cy + d)), (plan_px(cx - d), plan_py(cy)), (plan_px(cx), plan_py(cy - d))],
         stroke=C_COIL, sw=3.5, dash='9,5')
    label_bg(plan_px(100), plan_py(2), 'SPOLE 10×10, dreid 45°', size=11, fill=C_COIL, anchor='middle', weight='bold')
    label_bg(plan_px(100), plan_py(14), 'i lomme fra undersiden av bunnplaten', size=9, fill=C_COIL, anchor='middle')
    rect(plan_px(56), plan_py(-72), 40 * S, 18 * S, stroke=C_COIL, sw=1, dash='4,3')
    label_bg(plan_px(4), plan_py(-60), 'lomme for kort 36×15 →', size=9, fill=C_COIL)
    line(plan_px(100), plan_py(-70.7), plan_px(100), plan_py(BOX_Y1), stroke=C_COIL, sw=2.2, dash='3,2')
    label_bg(plan_px(104), plan_py(-60), '← spolekabel 8 cm til nippel', size=9, fill=C_COIL)
    # Bobs, svingaksel, stoppstang
    for i in range(BOB_N):
        y = (i - (BOB_N - 1) / 2) * BOB_PITCH
        circle(plan_px(BOB_X), plan_py(y), BOB_D / 2 * S, fill='#fff', stroke='#111', sw=1.4)
    line(plan_px(BOB_X), plan_py(ROOF_Y0), plan_px(BOB_X), plan_py(ROOF_Y1), stroke='#111', sw=0.8, dash='2,2')
    line(plan_px(STOP_X), plan_py(-LANE / 2), plan_px(STOP_X), plan_py(LANE / 2), stroke='#111', sw=2.5)
    label_bg(plan_px(178), plan_py(64), 'stoppstang Ø6', size=9, anchor='end')
    text(plan_px(L + 8), plan_py(-52), 'bobs ×5 Ø6', size=9)
    text(plan_px(L + 8), plan_py(-42), 'deling 22', size=9)
    # Snittlinje A–A
    line(plan_px(-6), plan_py(0), plan_px(L + 6), plan_py(0), stroke='#111', sw=0.9, dash='12,4,3,4')
    text(plan_px(-6), plan_py(0) - 6, 'A', size=12, weight='bold', anchor='end')
    text(plan_px(L + 8), plan_py(0) - 6, 'A', size=12, weight='bold')
    # Retning
    line(plan_px(-40), plan_py(24), plan_px(-8), plan_py(24), stroke='#111', sw=2)
    poly([(plan_px(-6), plan_py(24)), (plan_px(-14), plan_py(20)), (plan_px(-14), plan_py(28))], fill='#111')
    text(plan_px(-40), plan_py(18), 'INN', size=11, weight='bold')
    text(plan_px(-40), plan_py(34), 'fra landingsbrett', size=9)
    text(plan_px(L + 8), plan_py(20), 'UT', size=11, weight='bold')
    text(plan_px(L + 8), plan_py(32), 'til slaget', size=9)
    # Målsetting
    dim_h(plan_px(BOX_X0), plan_px(BOX_X0 + BOX_L), plan_py(BOX_Y0) - 14, 'boks 130', ext_from=plan_py(BOX_Y0))
    dim_h(plan_px(0), plan_px(ROOF_L), plan_py(HALF) + 22, 'tak 150', ext_from=plan_py(HALF))
    dim_h(plan_px(0), plan_px(L), plan_py(HALF) + 40, '200', ext_from=plan_py(HALF))
    dim_h(plan_px(100 - DIAG / 2), plan_px(100 + DIAG / 2), plan_py(HALF) + 58, 'spole-diagonal 141', ext_from=plan_py(HALF))
    dim_v(plan_py(-LANE / 2), plan_py(LANE / 2), plan_px(L) + 46, '110 innv.', ext_from=plan_px(L))
    dim_v(plan_py(-HALF), plan_py(HALF), plan_px(L) + 72, '150', ext_from=plan_px(L))
    dim_v(plan_py(BOX_Y0), plan_py(BOX_Y1), plan_px(BOX_X0 + BOX_L) + 30, 'boks 80', ext_from=plan_px(BOX_X0 + BOX_L))
    dim_h(plan_px(40), plan_px(64), plan_py(HALF - FOOT) - 4, '24')
    dim_h(plan_px(32), plan_px(40), plan_py(HALF - FOOT) - 18, '8')
    endg()

# ---------------- RISS 2: LENGDESNITT A–A ----------------
def sec_px(x): return x * S
def sec_pz(z): return (150 - z) * S
def view_section(ox, oy):
    group(ox, oy)
    text(0, -14, 'RISS 2 – LENGDESNITT A–A gjennom løpets senter (Y = 0)', size=13, weight='bold')
    rect(sec_px(0), sec_pz(Z_FLOOR + RAIL_B), L * S, RAIL_B * S, fill=C_WALL, stroke='#88a', sw=0.8)
    rect(sec_px(0), sec_pz(Z_ROOF), L * S, RAIL_T * S, fill=C_WALL, stroke='#88a', sw=0.8)
    for x0 in [0] + slat_x + [L - POST]:
        w = POST if x0 in (0, L - POST) else SLAT
        rect(sec_px(x0), sec_pz(Z_ROOF - RAIL_T), w * S, (OPEN_H - RAIL_B - RAIL_T) * S, fill=C_WALL, stroke='#88a', sw=0.8)
    rect(sec_px(0), sec_pz(COVER_T), L * S, COVER_T * S, fill='#cfcfcf', stroke='#333')
    rect(sec_px(0), sec_pz(Z_FLOOR), L * S, PLATE_T * S, fill=C_BASE, stroke='#333')
    px0, px1 = 100 - DIAG / 2, 100 + DIAG / 2
    rect(sec_px(px0), sec_pz(COVER_T + POCKET_D), (px1 - px0) * S, POCKET_D * S, fill='#fff', stroke='#333')
    for xx in (px0, px1 - 2):
        rect(sec_px(xx), sec_pz(COVER_T + 2), 2 * S, 2 * S, fill=C_COIL, stroke=C_COIL)
    label_bg(sec_px(100), sec_pz(COVER_T + 2) + 1, 'spolelomme 6 dyp · vikling 2×2 (plass til 3–4)', size=9.5, fill=C_COIL, anchor='middle')
    label_bg(sec_px(30), sec_pz(Z_FLOOR - 1.5) + 3, 'gulv 4 mm PETG over spolen', size=9.5, fill='#333')
    for x0 in roof_slat_x:
        rect(sec_px(x0), sec_pz(Z_ROOF + ROOF_T), SLAT * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    line(sec_px(0), sec_pz(Z_ROOF + ROOF_T), sec_px(ROOF_L), sec_pz(Z_ROOF + ROOF_T), stroke='#8a6d3b', sw=0.8, dash='3,2')
    text(sec_px(75), sec_pz(Z_ROOF + ROOF_T) - 6, 'takspiler 8, åpning 24', size=10, anchor='middle', fill='#6b4f1d')
    # Bobs, aksel, stoppstang
    rect(sec_px(BOB_X - BOB_D / 2), sec_pz(Z_PIVOT), BOB_D * S, BOB_LEN * S, fill='#fff', stroke='#111', sw=1.4)
    circle(sec_px(BOB_X), sec_pz(Z_PIVOT), 1.7 * S, fill='#111')
    circle(sec_px(STOP_X), sec_pz(Z_STOP), BOB_D / 2 * S, fill='#fff', stroke='#111', sw=1.4)
    label_bg(sec_px(BOB_X - 6), sec_pz(Z_PIVOT + 8), 'svingaksel Ø3 rustfri', size=9, anchor='end')
    label_bg(sec_px(BOB_X + 7), sec_pz(Z_STOP - 1), 'stoppstang Ø6', size=9)
    add(f'<path d="M {sec_px(BOB_X):.1f} {sec_pz(70):.1f} q 20 12 24 40" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="3,2"/>')
    label_bg(sec_px(118), sec_pz(100), 'bobs svinger kun innover →', size=9)
    # Duebein + ring
    lx = 100
    line(sec_px(lx), sec_pz(Z_FLOOR), sec_px(lx + 8), sec_pz(Z_FLOOR + 62), stroke='#7a4b1e', sw=3)
    line(sec_px(lx - 9), sec_pz(Z_FLOOR), sec_px(lx + 9), sec_pz(Z_FLOOR), stroke='#7a4b1e', sw=3)
    rect(sec_px(lx - 3), sec_pz(Z_FLOOR + 15), 8 * S, 8 * S, fill='#f5c26b', stroke='#7a4b1e', sw=1.2)
    label_bg(sec_px(lx + 16), sec_pz(Z_FLOOR + 24), 'chipring 5–10 mm over gulv', size=10, fill='#7a4b1e')
    label_bg(sec_px(lx + 16), sec_pz(Z_FLOOR + 13), '→ 9–14 mm fra ring til vikling', size=10, fill='#7a4b1e', weight='bold')
    # Målsetting
    dim_v(sec_pz(Z_ROOF), sec_pz(Z_FLOOR), sec_px(L) + 44, '120 åpning', ext_from=sec_px(L))
    dim_v(sec_pz(Z_FLOOR), sec_pz(0), sec_px(L) + 44, '13', ext_from=sec_px(L))
    dim_v(sec_pz(Z_ROOF + ROOF_T), sec_pz(0), sec_px(L) + 72, '139 total', ext_from=sec_px(L))
    for (z0, z1, lab, ty) in ((Z_FLOOR - FLOOR_T, Z_FLOOR, 'gulv 4', 262), (COVER_T, COVER_T + POCKET_D, 'lomme 6', 288), (0, COVER_T, 'deksel 3', 314)):
        zc = (z0 + z1) / 2
        line(sec_px(0), sec_pz(z0), sec_px(-6), sec_pz(z0), stroke=DIMC, sw=0.7); line(sec_px(0), sec_pz(z1), sec_px(-6), sec_pz(z1), stroke=DIMC, sw=0.7)
        line(sec_px(-6), sec_pz(z0), sec_px(-6), sec_pz(z1), stroke=DIMC, sw=0.9)
        line(sec_px(-6), sec_pz(zc), sec_px(-22), ty, stroke=DIMC, sw=0.7)
        text(sec_px(-26), ty + 4, lab, size=11, anchor='end', fill=DIMC)
    dim_h(sec_px(px0), sec_px(px1), sec_pz(0) + 26, 'lomme 141 (bredde i Y = 0)', ext_from=sec_pz(0))
    dim_h(sec_px(0), sec_px(L), sec_pz(0) + 48, '200', ext_from=sec_pz(0))
    endg()

# ---------------- RISS 3: ENDEOPPRISS ----------------
def end_px(y): return (y + 155) * S
def end_pz(z): return (150 - z) * S
def view_end(ox, oy):
    group(ox, oy)
    text(0, -14, 'RISS 3 – ENDEOPPRISS sett fra inngangen (landingsbrettet)', size=13, weight='bold')
    rect(end_px(BOX_Y0), end_pz(BOX_H), BOX_W * S, BOX_H * S, fill=C_BOX, stroke='#333')
    rect(end_px(BOX_Y0 - 2), end_pz(BOX_H + LID_T), (BOX_W + 4) * S, LID_T * S, fill='#c5dcbf', stroke='#333')
    text(end_px(BOX_Y0 + 6), end_pz(BOX_H / 2 + 4), 'ELEKTRONIKK', size=10, weight='bold')
    text(end_px(BOX_Y0 + 6), end_pz(BOX_H / 2 - 8), 'lokk m/ pakning + dryppkant', size=8.5)
    rect(end_px(-HALF), end_pz(COVER_T), BASE_W * S, COVER_T * S, fill='#cfcfcf', stroke='#333')
    rect(end_px(-HALF), end_pz(Z_FLOOR), BASE_W * S, PLATE_T * S, fill=C_BASE, stroke='#333')
    for yy in (-DIAG / 2, DIAG / 2 - 2):
        rect(end_px(yy), end_pz(COVER_T + 2), 2 * S, 2 * S, fill=C_COIL, stroke=C_COIL)
    line(end_px(-DIAG / 2), end_pz(COVER_T + POCKET_D), end_px(DIAG / 2), end_pz(COVER_T + POCKET_D), stroke=C_COIL, sw=1, dash='4,3')
    for y0 in (-HALF, HALF - FOOT):
        rect(end_px(y0), end_pz(Z_FLOOR + FOOT_T), FOOT * S, FOOT_T * S, fill='#c0cfe0', stroke='#335')
    for (y0, y1) in WALL_Y:
        rect(end_px(y0), end_pz(Z_ROOF), PANEL_T * S, OPEN_H * S, fill=C_WALL, stroke='#335')
    rect(end_px(ROOF_Y0), end_pz(Z_ROOF + ROOF_T), (ROOF_Y1 - ROOF_Y0) * S, ROOF_T * S, fill=C_ROOF, stroke='#8a6d3b')
    for i in range(BOB_N):
        y = (i - (BOB_N - 1) / 2) * BOB_PITCH
        rect(end_px(y - BOB_D / 2), end_pz(Z_PIVOT), BOB_D * S, BOB_LEN * S, fill='#fff', stroke='#111', sw=1.2)
    line(end_px(ROOF_Y0), end_pz(Z_PIVOT), end_px(ROOF_Y1), end_pz(Z_PIVOT), stroke='#111', sw=1.5)
    rect(end_px(-LANE / 2), end_pz(Z_STOP + BOB_D / 2), LANE * S, BOB_D * S, fill='#fff', stroke='#111', sw=1.2)
    label_bg(end_px(0), end_pz(Z_STOP - 9), 'stoppstang – dua kan ikke gå ut igjen', size=9, anchor='middle')
    label_bg(end_px(0), end_pz(Z_ROOF - 14), 'bobs ×5 i utgangen (bak)', size=10, anchor='middle')
    label_bg(end_px(0), end_pz(-4), 'spolehjørner (Y = ±70,7) ligger under veggføttene', size=9, fill=C_COIL, anchor='middle')
    dim_h(end_px(-LANE / 2), end_px(LANE / 2), end_pz(Z_ROOF + ROOF_T) - 14, '110', ext_from=end_pz(Z_ROOF + ROOF_T))
    dim_h(end_px(-HALF), end_px(HALF), end_pz(0) + 34, '150', ext_from=end_pz(0))
    dim_h(end_px(BOX_Y0), end_px(BOX_Y1), end_pz(0) + 34, '80', ext_from=end_pz(0))
    dim_v(end_pz(Z_ROOF), end_pz(Z_FLOOR), end_px(HALF) + 44, '120', ext_from=end_px(HALF))
    dim_v(end_pz(BOX_H + LID_T), end_pz(0), end_px(BOX_Y0) - 30, '45', ext_from=end_px(BOX_Y0), side='left')
    dim_h(end_px(HALF - FOOT), end_px(HALF), end_pz(Z_FLOOR + FOOT_T) - 8, 'fot 20')
    endg()

# ---------------- RISS 4: ISOMETRISK EKSPLOSJONSRISS ----------------
SI = 1.3
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
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
    text(0, -14, 'RISS 4 – ISOMETRISK EKSPLOSJONSRISS (deler løftet/trukket ut for oversikt)', size=13, weight='bold')
    group(250, 600)
    # Boks trukket 70 mm bort fra platen (eksplodert) + lokk løftet
    by0, by1 = BOX_Y0 - 70, BOX_Y1 - 70
    box3d(BOX_X0, BOX_X0 + BOX_L, by0, by1, 0, BOX_H, C_BOX)
    box3d(BOX_X0 - 2, BOX_X0 + BOX_L + 2, by0 - 2, by1 + 2, BOX_H + 28, BOX_H + 28 + LID_T, '#c5dcbf')
    u, v = iso(100, by1, BOX_H / 2); u2, v2 = iso(100, BOX_Y1, Z_FLOOR / 2)
    line(u, v, u2, v2, stroke=C_HID, sw=1, dash='4,3')
    # Bunndeksel (senket) + bunnplate
    box3d(0, L, -HALF, HALF, -34, -34 + COVER_T, '#cfcfcf')
    box3d(0, L, -HALF, HALF, COVER_T, Z_FLOOR, C_BASE)
    d = DIAG / 2
    poly([iso(100 + d, 0, Z_FLOOR + 0.5), iso(100, d, Z_FLOOR + 0.5), iso(100 - d, 0, Z_FLOOR + 0.5), iso(100, -d, Z_FLOOR + 0.5)],
         stroke=C_COIL, sw=3, dash='8,5')
    for y0 in (-HALF, HALF - FOOT):
        box3d(0, L, y0, y0 + FOOT, Z_FLOOR, Z_FLOOR + FOOT_T, '#c0cfe0')
    # Vegger løftet 70, bobs mellom dem, tak løftet 150
    wall3d(WALL_Y[0][0], WALL_Y[0][1], 70)
    for i in range(BOB_N):
        y = (i - (BOB_N - 1) / 2) * BOB_PITCH
        box3d(BOB_X - 3, BOB_X + 3, y - 3, y + 3, Z_PIVOT - BOB_LEN + 70, Z_PIVOT + 70, '#ffffff')
    wall3d(WALL_Y[1][0], WALL_Y[1][1], 70)
    dzr = 150
    for y0 in (ROOF_Y0, ROOF_Y1 - 6):
        box3d(0, ROOF_L, y0, y0 + 6, Z_ROOF + dzr, Z_ROOF + dzr + ROOF_T, C_ROOF)
    for x0 in roof_slat_x:
        box3d(x0, x0 + SLAT, ROOF_Y0, ROOF_Y1, Z_ROOF + dzr, Z_ROOF + dzr + ROOF_T, C_ROOF)
    endg()
    y = 935
    for s in ('Bunndeksel 3 mm (lukker spolelommen) · Bunnplate 10 mm: 6 mm lomme + 4 mm gulv – printes med gulvflaten NED',
              'Veggpaneler ×2 med L-fot (printes flatt) · Bobs ×5 mellom veggene · Takpanel (printes flatt, skrus i topplistene)',
              'Elektronikkboks + lokk med pakningsspor – monteres inntil bunnplaten (stiplet linje), spolekabel gjennom nippel'):
        text(170, y, s, size=10); y += 15
    endg()

# ---------------- DELELISTE + NOTER ----------------
def view_notes(ox, oy):
    group(ox, oy)
    text(0, 0, 'DELELISTE (alle deler innenfor Bambu A1 256×256×256, PETG)', size=13, weight='bold')
    rows = [
        ('1', 'Bunnplate m/ diamantlomme', '200 × 150 × 10', 'flatt, gulvflate ned (lommen opp → uten støtte)'),
        ('2', 'Bunndeksel', '196 × 146 × 3', 'flatt'),
        ('3', 'Veggpanel m/ L-fot ×2', '200 × 124 × 6 (+ fot 20 × 4)', 'flatt på siden'),
        ('4', 'Takpanel (spiler)', '150 × 122 × 6 (kan lages 200)', 'flatt'),
        ('5', 'Bobs ×5', 'Ø6 × 112', 'liggende'),
        ('6', 'Svingaksel', 'Ø3 × 150 rustfri/messing', 'kjøpes (ikke vanlig stål nær spolen)'),
        ('7', 'Stoppstang', 'Ø6 × 122', 'liggende'),
        ('8', 'Elektronikkboks', '130 × 80 × 42 (innv. 120 × 70 × 34)', 'åpning opp'),
        ('9', 'Lokk m/ pakningsspor + dryppkant', '134 × 84 × 3', 'flatt'),
        ('10', 'Skruer', 'M3 ×10 (boks) + treskruer 4 × 30 ×8 (føtter/plate)', 'kjøpes'),
    ]
    y = 22
    for n, name, dims, orient in rows:
        text(0, y, n, size=11, weight='bold'); text(24, y, name, size=11); text(270, y, dims, size=11); text(590, y, orient, size=10, fill='#444')
        y += 17
    y += 12
    text(0, y, 'NOTER', size=13, weight='bold'); y += 18
    notes = [
        'A. Spolen ligger i en diamantformet lomme fra undersiden av bunnplaten; gulv over spolen 4 mm. Ring på beinet 5–10 mm over gulv',
        '   → 9–14 mm fra ring til vikling. Diamantens tråder krysser gangbanen på skrå, så foten passerer minst to ledere uansett spor.',
        'B. Diamantens diagonal (141) er bredere enn løpet (110): hjørnene ligger under veggføttene. Derfor er bunnplaten 150 bred.',
        'C. Ingen metall over eller rundt spolen: svingaksel og skruer i spolesonen i rustfri/messing/nylon. Treskruene sitter i hjørnene og på føttene.',
        'D. Lommen har utsparing for avstemmingskortet (36×15) ved hjørnet mot boksen og en kanal for kabelen (8 cm) ut i boksens nippel.',
        'E. Boksen: lokk med spor for Ø2 silikonsnor (eller TPU-pakning), dryppkant utenpå boksveggen, kabelnippel PG7. Sprutsikker under halvtak.',
        '   PCB-en orienteres med E1 (LTE-antenne) mot ytterveggen, bort fra slusa; J3/J4 mot nippelen. Lesermodulens mål er ANTATT 45×30×10 – juster.',
        'F. Bobs svinger bare innover (mot slaget): stoppstangen ligger på inngangssiden av bobs-ene. Dua går over spolen FØR den dytter bobs-ene',
        '   → den stopper gjerne et øyeblikk på spolen = lengre lesetid. Bobs-ene hindrer også at dua flyr rett gjennom.',
        'G. Taket er spiler (åpning 24) og dekker inngang + spolesone (150). Hopper duer ut oppover før bobs-ene, print takpanelet i full lengde (200).',
        'H. Spileåpning 24 mm i vegger og tak: hodet kan ikke sette seg fast, kroppen kommer ikke gjennom. Alle deler er sett-gjennom → ikke «tunnel».',
        'I. To løp side om side: bunnplatene stilles kant i kant (150 + 150); felles takpanel lages 244 bredt i to deler.',
    ]
    for n in notes:
        text(0, y, n, size=10.5); y += 15
    endg()

# ---------------- ARK ----------------
W, H = 1800, 1600
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
add(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#222" stroke-width="2"/>')
text(30, 40, 'DUESLUSE MED INNEBYGD 125 kHz-SPOLE – én due om gangen', size=22, weight='bold')
text(30, 62, 'Teknisk tegning v1 · alle mål i mm · PETG, Bambu Lab A1 · spole 10×10 cm dreid 45° i lomme under 4 mm gulv', size=12, fill='#333')
text(W - 30, 40, 'PigeonPal · sluse v1', size=12, anchor='end', fill='#333')
text(W - 30, 58, 'Skala: 2 px/mm i riss 1–3', size=11, anchor='end', fill='#555')
view_plan(130, 150)
view_section(150, 760)
view_end(640, 760)
view_iso(1020, 110)
view_notes(60, 1140)
add('</svg>')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'duesluse_tegning.svg')
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print('skrev', path)

#!/usr/bin/env python3
"""Modul B (diamantspole) – karet, som STL klar for print (opp-ned: gulvflaten mot bedet).
Alle mål i mm. Bygges i reell orientering (Z opp, gulv ved Z=32) og roteres 180° om X til print-orientering.
"""
import os
import math, struct, numpy as np
from manifold3d import Manifold, CrossSection

# ---------- parametre ----------
L = 150.0; W = 150.0; H = 32.0          # kar utvendig
WALL = 2.4; FLOOR = 4.0                 # vegg / gulv
COIL = 100.0; CLR = 0.4                 # spole (kvadrat) + klaring per side
POCKET_D = 6.0; FRAME_T = 2.4           # lommedybde / ramme rundt spolen
RIB_T = 2.4; RIB_H = 20.0               # ribber under gulvet (stopper under lommen)
GROOVE_W = 6.4; GROOVE_D = 1.5          # styrespor for veggpanel i gulvflaten
LANE = 110.0
SCREW_D = 3.4                           # skruehull (M3 / 3,5 treskrue)
DT_BASE, DT_TIP, DT_DEPTH, DT_CLR = 10.0, 14.0, 6.0, 0.3   # svalehale hunn (mot modul M ved x=0)
DT_Y = (-48.0, 48.0); DT_Z0 = 2.0
CABLE_D = 8.0; CABLE_Z = 10.0; CABLE_Y = -66.0
DT_BOSS_X, DT_BOSS_HALF = 8.0, 12.0     # fortykning rundt hvert svalehalespor
BOARD_L, BOARD_W, BOARD_H = 40.0, 20.0, 8.0                 # utsparing for kort på spolen (36×15 + klaring)

def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

def diamond_prism(cx, cy, side, z0, z1):
    d = side / math.sqrt(2)
    cs = CrossSection([[(cx + d, cy), (cx, cy + d), (cx - d, cy), (cx, cy - d)]])
    return Manifold.extrude(cs, z1 - z0).translate([0, 0, z0])

def cyl_x(y, z, d, x0, x1):
    return Manifold.cylinder(x1 - x0, d / 2, d / 2, 48).rotate([0, 90, 0]).translate([x0, y, z])

def cyl_z(x, y, d, z0, z1):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, 48).translate([x, y, z0])

def dovetail_female(x_face, yc, into=+1):
    c = DT_CLR; xin = x_face + into * (DT_DEPTH + c)
    pts = [(x_face - into * 0.5, yc - DT_BASE / 2 - c), (xin, yc - DT_TIP / 2 - c), (xin, yc + DT_TIP / 2 + c), (x_face - into * 0.5, yc + DT_BASE / 2 + c)]
    cs = CrossSection([pts])
    return Manifold.extrude(cs, H - DT_Z0 + 1).translate([0, 0, DT_Z0])   # åpen i toppen (gulvnivå)

cx, cy = L / 2, 0.0
# ---------- kar ----------
kar = box(0, L, -W / 2, W / 2, 0, H)
kar -= box(WALL, L - WALL, -W / 2 + WALL, W / 2 - WALL, -1, H - FLOOR)          # hulrom, åpent nedover
# ramme rundt diamantlommen (henger ned fra gulvets underside)
frame = diamond_prism(cx, cy, COIL + 2 * CLR + 2 * FRAME_T, H - FLOOR - POCKET_D, H - FLOOR)
frame -= diamond_prism(cx, cy, COIL + 2 * CLR, H - FLOOR - POCKET_D - 1, H - FLOOR + 1)
kar += frame
# ribber under gulvet (Z 0..20), langs X ved Y=±62 og på tvers ved X=20/130, uten å treffe lommen
for y in (-62.0, 62.0):
    kar += box(WALL, L - WALL, y - RIB_T / 2, y + RIB_T / 2, 0, RIB_H)
for x in (20.0, L - 20.0):
    kar += box(x - RIB_T / 2, x + RIB_T / 2, -W / 2 + WALL, W / 2 - WALL, 0, RIB_H)
# gjenåpne lommen der ribbene eventuelt overlapper (sikkerhet)
kar -= diamond_prism(cx, cy, COIL + 2 * CLR, H - FLOOR - POCKET_D, H - FLOOR)
# utsparing for kortet på spolen ved hjørnet mot -Y (innenfor lommen, dypere)
kar -= box(cx - BOARD_L / 2, cx + BOARD_L / 2, -W / 2 + WALL + 1, -W / 2 + WALL + 1 + BOARD_W, H - FLOOR - BOARD_H, H - FLOOR)
# styrespor for veggpaneler i gulvflaten
for y in (-LANE / 2 - GROOVE_W, LANE / 2):
    kar -= box(-1, L + 1, y, y + GROOVE_W, H - GROOVE_D, H + 1)
# skruehull gjennom gulvet (veggfot + feste til brett)
for x in (12.0, L / 2, L - 12.0):
    for y in (-68.0, 68.0):
        kar -= cyl_z(x, y, SCREW_D, H - FLOOR - 1, H + 1)
# svalehale-hunnspor i endeveggen mot modul M (x = 0), med 8 mm fortykning rundt sporet
for yc in DT_Y:
    kar += box(0, DT_BOSS_X, yc - DT_BOSS_HALF, yc + DT_BOSS_HALF, 0, H)
for yc in DT_Y:
    kar -= dovetail_female(0.0, yc, +1)
# kabelhull i samme endevegg
kar -= cyl_x(CABLE_Y, CABLE_Z, CABLE_D, -1, WALL + 1)
# ---------- print-orientering: 180° om X → gulvflaten ned ----------
part = kar.rotate([180, 0, 0]).translate([0, 0, H])
m = part.to_mesh()
V = np.asarray(m.vert_properties)[:, :3]; T = np.asarray(m.tri_verts)
# ---------- STL (binær) ----------
def write_stl(path, V, T):
    with open(path, 'wb') as f:
        f.write(b'PigeonPal duesluse modul B kar'.ljust(80, b'\0')); f.write(struct.pack('<I', len(T)))
        for a, b, c in T:
            p0, p1, p2 = V[a], V[b], V[c]; n = np.cross(p1 - p0, p2 - p0); ln = np.linalg.norm(n); n = n / ln if ln > 0 else n
            f.write(struct.pack('<3f', *n)); f.write(struct.pack('<9f', *p0, *p1, *p2)); f.write(b'\0\0')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stl', 'modul_B', 'duesluse_modul_B_kar.stl')
write_stl(out, V, T)
mn, mx = V.min(0), V.max(0)
print(f'STL: {len(T)} trekanter, bbox {mx-mn} (min {mn}, max {mx}), volum {part.volume()/1000:.1f} cm3 ≈ {part.volume()/1000*1.27:.0f} g PETG, genus/status ok: {part.status()}')
# ---------- enkel SVG-render (isometrisk, flat shading) for visuell sjekk ----------
def render(V, T, path, W=1100, Hh=800, scale=3.2, elev=35, azim=-50, title=''):
    a, e = math.radians(azim), math.radians(elev)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(e), -math.sin(e)], [0, math.sin(e), math.cos(e)]])
    P = (V - V.mean(0)) @ R.T @ Rx.T
    light = np.array([0.3, 0.4, 0.85]); light /= np.linalg.norm(light)
    tris = []
    for a_, b_, c_ in T:
        p = P[[a_, b_, c_]]; n = np.cross(p[1] - p[0], p[2] - p[0]); ln = np.linalg.norm(n)
        if ln == 0: continue
        n /= ln
        if n[1] < 0: continue          # backface (kamera ser langs -Y etter rotasjon)
        shade = 0.45 + 0.55 * max(0.0, float(n @ light)); depth = p[:, 1].mean()
        tris.append((depth, p, shade))
    tris.sort(key=lambda t: -t[0])
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}"><rect width="100%" height="100%" fill="#fff"/>',
         f'<text x="20" y="30" font-family="Arial" font-size="18" font-weight="bold">{title}</text>']
    for _, p, sh in tris:
        col = '#%02x%02x%02x' % (int(150 * sh + 60), int(160 * sh + 60), int(190 * sh + 60))
        pts = ' '.join(f'{W/2 + p[i,0]*scale:.1f},{Hh/2 - p[i,2]*scale:.1f}' for i in range(3))
        s.append(f'<polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="0.4"/>')
    s.append('</svg>'); open(path, 'w').write('\n'.join(s))
base = out.replace('.stl', '')
render(V, T, base + '_print.svg', title='Modul B kar – print-orientering (gulvflaten ned, lomme/hulrom opp)')
Vr = np.asarray(kar.to_mesh().vert_properties)[:, :3]; Tr = np.asarray(kar.to_mesh().tri_verts)
render(Vr, Tr, base + '_reell.svg', elev=35, azim=-50, title='Modul B kar – reell orientering (gulv opp)')
render(Vr, Tr, base + '_under.svg', elev=-40, azim=-50, title='Modul B kar – sett fra undersiden')
print('render ok')

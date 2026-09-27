#!/usr/bin/env python3
"""Modul B – veggpanel med L-fot (høyre + speilvendt venstre), STL i print-orientering.
Reell orientering: X langs løpet (0 = skjøt mot M, 150 = utgang), Y utover fra løpets innside (0 = innerflate),
Z opp (0 = gulvflaten i karet). Print: innerflaten ned på bedet, foten står opp som en vegg → ingen støtte.
"""
import os
import math, struct, numpy as np
from manifold3d import Manifold

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stl', 'modul_B', '')
# ---------- parametre (matcher karet i modul_B_kar.py) ----------
L = 150.0                     # lengde
T = 6.0                       # paneltykkelse (styrespor i karet er 6,4 bredt)
GROOVE_D = 1.5                # panelet går 1,5 mm ned i styresporet
OPEN_H = 120.0                # åpningshøyde over gulv
RAIL_B, RAIL_T = 12.0, 10.0   # bunn-/topplist
POST, SLAT = 8.0, 8.0         # endestolper og spiler
N_SLATS = 5                   # → åpning ≈ 15,7 mm
FOOT_W, FOOT_T = 20.0, 4.0    # L-fot (fra innerflaten og utover)
SCREW_X = (12.0, 75.0, 138.0); SCREW_Y = 13.0; SCREW_D = 3.6   # matcher hullene i karet (Y = ±68)
PILOT_D, PILOT_DEPTH = 2.5, 10.0                                # takskruer i topplisten
AXLE_X, AXLE_Z, AXLE_D = 138.0, 116.0, 3.4                     # bobs-aksel Ø3
STOP_X, STOP_Z, STOP_D = 132.0, 17.0, 6.4                      # stoppstang Ø6

def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cyl_z(x, y, d, z0, z1):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, 40).translate([x, y, z0])
def cyl_y(x, z, d, y0, y1):
    return Manifold.cylinder(y1 - y0, d / 2, d / 2, 40).rotate([-90, 0, 0]).translate([x, y0, z])

gap = (L - 2 * POST - N_SLATS * SLAT) / (N_SLATS + 1)
slat_x = [POST + gap + i * (SLAT + gap) for i in range(N_SLATS)]

# ---------- panel ----------
p = box(0, L, 0, T, -GROOVE_D, OPEN_H)
for i in range(N_SLATS + 1):                                     # skjær ut åpningene mellom spilene
    x0 = POST + i * (SLAT + gap); x1 = x0 + gap
    p -= box(x0, x1, -1, T + 1, RAIL_B, OPEN_H - RAIL_T)
# forsterkning for stoppstangen (fyller nedre del av åpningen ved utgangen)
last_gap_x0 = slat_x[-1] + SLAT
p += box(last_gap_x0, L - POST, 0, T, RAIL_B - 0.1, 28.0)
# L-fot
p += box(0, L, 0, FOOT_W, 0, FOOT_T)
# skruehull i foten (gjennom til karet)
for x in SCREW_X:
    p -= cyl_z(x, SCREW_Y, SCREW_D, -1, FOOT_T + 1)
# forhull for takpanelet i topplisten
for x in SCREW_X:
    p -= cyl_z(x, T / 2, PILOT_D, OPEN_H - PILOT_DEPTH, OPEN_H + 1)
# bobs-aksel og stoppstang (tvers gjennom panelet)
p -= cyl_y(AXLE_X, AXLE_Z, AXLE_D, -1, T + 1)
p -= cyl_y(STOP_X, STOP_Z, STOP_D, -1, T + 1)

hoyre = p
venstre = p.mirror([1, 0, 0]).translate([L, 0, 0])               # speilvendt: akselhull havner riktig på andre side

def to_print(m):
    # innerflaten (y=0) ned på bedet: rot +90 om X → z' = y, y' = -z
    r = m.rotate([90, 0, 0])
    b = r.bounding_box(); return r.translate([-b[0], -b[1], -b[2]])

def write_stl(path, man, name):
    mesh = man.to_mesh(); V = np.asarray(mesh.vert_properties)[:, :3]; Tr = np.asarray(mesh.tri_verts)
    with open(path, 'wb') as f:
        f.write(name.encode().ljust(80, b'\0')); f.write(struct.pack('<I', len(Tr)))
        for a, b, c in Tr:
            p0, p1, p2 = V[a], V[b], V[c]; n = np.cross(p1 - p0, p2 - p0); ln = np.linalg.norm(n); n = n / ln if ln else n
            f.write(struct.pack('<3f', *n)); f.write(struct.pack('<9f', *p0, *p1, *p2)); f.write(b'\0\0')
    mn, mx = V.min(0), V.max(0)
    print(f'{path.split("/")[-1]}: {len(Tr)} trek., bbox {np.round(mx - mn, 1)}, {man.volume()/1000:.1f} cm3 ≈ {man.volume()/1000*1.27:.0f} g, status {man.status()}')
    return V, Tr

Vh, Th = write_stl(OUT + 'duesluse_modul_B_vegg_hoyre.stl', to_print(hoyre), 'PigeonPal modul B vegg hoyre')
Vv, Tv = write_stl(OUT + 'duesluse_modul_B_vegg_venstre.stl', to_print(venstre), 'PigeonPal modul B vegg venstre')
print(f'spileåpning {gap:.1f} mm')

# ---------- render for visuell sjekk (reell orientering, høyre) ----------
def render(man, path, title, elev=25, azim=-60, scale=3.0, W=1100, H=800):
    mesh = man.to_mesh(); V = np.asarray(mesh.vert_properties)[:, :3]; Tr = np.asarray(mesh.tri_verts)
    a, e = math.radians(azim), math.radians(elev)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(e), -math.sin(e)], [0, math.sin(e), math.cos(e)]])
    P = (V - V.mean(0)) @ R.T @ Rx.T
    li = np.array([0.3, 0.4, 0.85]); li /= np.linalg.norm(li)
    tris = []
    for a_, b_, c_ in Tr:
        q = P[[a_, b_, c_]]; n = np.cross(q[1] - q[0], q[2] - q[0]); ln = np.linalg.norm(n)
        if ln == 0: continue
        n /= ln
        if n[1] < 0: continue
        tris.append((q[:, 1].mean(), q, 0.45 + 0.55 * max(0.0, float(n @ li))))
    tris.sort(key=lambda t: -t[0])
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#fff"/>',
         f'<text x="20" y="30" font-family="Arial" font-size="18" font-weight="bold">{title}</text>']
    for _, q, sh in tris:
        col = '#%02x%02x%02x' % (int(150 * sh + 60), int(165 * sh + 60), int(195 * sh + 60))
        s.append(f'<polygon points="{" ".join(f"{W/2 + q[i,0]*scale:.1f},{H/2 - q[i,2]*scale:.1f}" for i in range(3))}" fill="{col}" stroke="{col}" stroke-width="0.4"/>')
    s.append('</svg>'); open(path, 'w').write('\n'.join(s))
render(hoyre, OUT + 'vegg_B_reell.svg', 'Modul B veggpanel (høyre) – reell orientering, sett fra løpet')
render(to_print(hoyre), OUT + 'vegg_B_print.svg', 'Modul B veggpanel – print-orientering (innerflate ned, fot opp)', elev=40)

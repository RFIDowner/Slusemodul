#!/usr/bin/env python3
"""Modul B – takpanel (spiler), STL. Ligger på veggpanelenes topplister og skrus i forhullene der.
X langs løpet (0 = skjøt mot M, 150 = utgang), Y på tvers (0 = senter), Z opp. Printes flatt slik det ligger.
"""
import os
import math, struct, numpy as np
from manifold3d import Manifold

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stl', 'modul_B', '')
L = 150.0; T = 6.0
LANE = 110.0; WALL_T = 6.0
Y_OUT = LANE / 2 + WALL_T                    # 61 = ytterkant vegg
BEAM_Y0 = LANE / 2                           # sidebjelke ligger rett over veggens topp (55..61)
POST, SLAT, N_SLATS = 8.0, 8.0, 5            # samme deling som veggene → spilene står over hverandre
SCREW_X = (12.0, 75.0, 138.0); SCREW_Y = LANE / 2 + WALL_T / 2; SCREW_D = 3.4; CSK_D = 6.5
LIP = 1.2; LIP_H = 3.0                       # styrekant som griper innenfor veggtoppen

def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cyl_z(x, y, d, z0, z1, d2=None):
    return Manifold.cylinder(z1 - z0, d / 2, (d2 or d) / 2, 40).translate([x, y, z0])

gap = (L - 2 * POST - N_SLATS * SLAT) / (N_SLATS + 1)
roof = Manifold()
for s in (-1, 1):                                                 # sidebjelker over veggene
    y0, y1 = (BEAM_Y0, Y_OUT) if s > 0 else (-Y_OUT, -BEAM_Y0)
    roof += box(0, L, y0, y1, 0, T)
    # styrekant under bjelken, på innsiden av veggen (holder taket sentrert)
    yl0, yl1 = (BEAM_Y0 - LIP, BEAM_Y0) if s > 0 else (-BEAM_Y0, -BEAM_Y0 + LIP)
    roof += box(0, L, yl0, yl1, -LIP_H, T)
xs = [0.0] + [POST + gap + i * (SLAT + gap) for i in range(N_SLATS)] + [L - POST]
for x in xs:                                                      # tverrspiler (endestolper + 5 spiler)
    roof += box(x, x + SLAT, -Y_OUT, Y_OUT, 0, T)
roof -= box(130, 146, -Y_OUT - 1, Y_OUT + 1, -LIP_H - 1, 0)       # styrekant kuttet ved bobs-akselen (x=138, z=116)
for x in SCREW_X:                                                 # skruehull med forsenkning
    for y in (SCREW_Y, -SCREW_Y):
        roof -= cyl_z(x, y, SCREW_D, -1, T + 1)
        roof -= cyl_z(x, y, SCREW_D, T - 2.0, T + 0.01, CSK_D)

# print: flat, toppflaten ned (styrekanten peker opp → ingen støtte)
pr = roof.rotate([180, 0, 0]); b = pr.bounding_box(); pr = pr.translate([-b[0], -b[1], -b[2]])
mesh = pr.to_mesh(); V = np.asarray(mesh.vert_properties)[:, :3]; Tr = np.asarray(mesh.tri_verts)
path = OUT + 'duesluse_modul_B_tak.stl'
with open(path, 'wb') as f:
    f.write(b'PigeonPal modul B tak'.ljust(80, b'\0')); f.write(struct.pack('<I', len(Tr)))
    for a, b_, c in Tr:
        p0, p1, p2 = V[a], V[b_], V[c]; n = np.cross(p1 - p0, p2 - p0); ln = np.linalg.norm(n); n = n / ln if ln else n
        f.write(struct.pack('<3f', *n)); f.write(struct.pack('<9f', *p0, *p1, *p2)); f.write(b'\0\0')
print(f'tak: {len(Tr)} trek., bbox {np.round(V.max(0) - V.min(0), 1)}, {pr.volume()/1000:.1f} cm3 ≈ {pr.volume()/1000*1.27:.0f} g, status {pr.status()}, spileåpning {gap:.1f}')

# render
def render(man, p, title, elev=35, azim=-55, scale=3.2, W=1100, H=800):
    m = man.to_mesh(); V = np.asarray(m.vert_properties)[:, :3]; T_ = np.asarray(m.tri_verts)
    a, e = math.radians(azim), math.radians(elev)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(e), -math.sin(e)], [0, math.sin(e), math.cos(e)]])
    P = (V - V.mean(0)) @ R.T @ Rx.T; li = np.array([0.3, 0.4, 0.85]); li /= np.linalg.norm(li); tris = []
    for a_, b_, c_ in T_:
        q = P[[a_, b_, c_]]; n = np.cross(q[1] - q[0], q[2] - q[0]); ln = np.linalg.norm(n)
        if ln == 0: continue
        n /= ln
        if n[1] < 0: continue
        tris.append((q[:, 1].mean(), q, 0.45 + 0.55 * max(0.0, float(n @ li))))
    tris.sort(key=lambda t: -t[0])
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#fff"/><text x="20" y="30" font-family="Arial" font-size="18" font-weight="bold">{title}</text>']
    for _, q, sh in tris:
        col = '#%02x%02x%02x' % (int(160 * sh + 60), int(145 * sh + 60), int(110 * sh + 60))
        s.append(f'<polygon points="{" ".join(f"{W/2 + q[i,0]*scale:.1f},{H/2 - q[i,2]*scale:.1f}" for i in range(3))}" fill="{col}" stroke="{col}" stroke-width="0.4"/>')
    s.append('</svg>'); open(p, 'w').write('\n'.join(s))
render(roof, OUT + 'tak_B.svg', 'Modul B takpanel – slik det ligger (styrekant ned mot veggene)', elev=-30)

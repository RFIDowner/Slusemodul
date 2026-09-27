#!/usr/bin/env python3
"""Modul B som STEP (ekte solider, til Fusion). Samme geometri som modul_B_kar.py / _vegg.py / _tak.py,
men bygget med CadQuery og plassert i MONTERT posisjon (ikke print-orientering):

  X langs løpet (0 = skjøt mot modul M, 150 = utgang)
  Y på tvers (0 = senter av løpet, + = høyre side sett i gangretningen)
  Z opp (0 = underkant karet / landingsbrettet, 32 = gulvflaten)

Utdata i ../step/modul_B/: én STEP per del + en samlet sammenstilling.
"""
import math, os
import cadquery as cq

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'step', 'modul_B')
os.makedirs(OUT, exist_ok=True)

# ---------- felles mål ----------
L = 150.0; W = 150.0; H = 32.0              # kar utvendig
LANE = 110.0; Z_FLOOR = H

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane('XY').box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def cyl_z(x, y, d, z0, z1):
    return cq.Workplane('XY').circle(d / 2).extrude(z1 - z0).translate((x, y, z0))

def cyl_x(y, z, d, x0, x1):
    return cq.Workplane('YZ').circle(d / 2).extrude(x1 - x0).translate((x0, y, z))

def cyl_y(x, z, d, y0, y1):
    # XZ-planets normal peker i -Y; ekstruder negativt for å gå i +Y
    return cq.Workplane('XZ').circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))

def diamond(cx, cy, side, z0, z1):
    # kvadrat dreid 45°: hjørner på aksene
    return cq.Workplane('XY').polygon(4, side * math.sqrt(2)).extrude(z1 - z0).translate((cx, cy, z0))

def prism(pts, z0, z1):
    return cq.Workplane('XY').polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))

# ======================= KAR =======================
WALL = 2.4; FLOOR = 4.0; COIL = 100.0; CLR = 0.4; POCKET_D = 6.0; FRAME_T = 2.4
RIB_T = 2.4; RIB_H = 20.0; GROOVE_W = 6.4; GROOVE_D = 1.5; SCREW_D = 3.4
DT_BASE, DT_TIP, DT_DEPTH, DT_CLR, DT_Z0 = 10.0, 14.0, 6.0, 0.3, 2.0; DT_Y = (-48.0, 48.0)
CABLE_D, CABLE_Z, CABLE_Y = 8.0, 10.0, -66.0
BOARD_L, BOARD_W, BOARD_H = 40.0, 20.0, 8.0
cx, cy = L / 2, 0.0
zp0, zp1 = H - FLOOR - POCKET_D, H - FLOOR       # lomme 22..28

kar = box(0, L, -W / 2, W / 2, 0, H)
kar = kar.cut(box(WALL, L - WALL, -W / 2 + WALL, W / 2 - WALL, -1, H - FLOOR))
frame = diamond(cx, cy, COIL + 2 * CLR + 2 * FRAME_T, zp0, zp1).cut(diamond(cx, cy, COIL + 2 * CLR, zp0 - 1, zp1 + 1))
kar = kar.union(frame)
for y in (-62.0, 62.0):
    kar = kar.union(box(WALL, L - WALL, y - RIB_T / 2, y + RIB_T / 2, 0, RIB_H))
for x in (20.0, L - 20.0):
    kar = kar.union(box(x - RIB_T / 2, x + RIB_T / 2, -W / 2 + WALL, W / 2 - WALL, 0, RIB_H))
kar = kar.cut(diamond(cx, cy, COIL + 2 * CLR, zp0, zp1))
kar = kar.cut(box(cx - BOARD_L / 2, cx + BOARD_L / 2, -W / 2 + WALL + 1, -W / 2 + WALL + 1 + BOARD_W, H - FLOOR - BOARD_H, H - FLOOR))
for y in (-LANE / 2 - GROOVE_W, LANE / 2):
    kar = kar.cut(box(-1, L + 1, y, y + GROOVE_W, H - GROOVE_D, H + 1))
for x in (12.0, L / 2, L - 12.0):
    for y in (-68.0, 68.0):
        kar = kar.cut(cyl_z(x, y, SCREW_D, H - FLOOR - 1, H + 1))
for yc in DT_Y:
    kar = kar.union(box(0, 8.0, yc - 12.0, yc + 12.0, 0, H))
for yc in DT_Y:
    c = DT_CLR; xin = DT_DEPTH + c
    pts = [(-0.5, yc - DT_BASE / 2 - c), (xin, yc - DT_TIP / 2 - c), (xin, yc + DT_TIP / 2 + c), (-0.5, yc + DT_BASE / 2 + c)]
    kar = kar.cut(prism(pts, DT_Z0, H + 1))
kar = kar.cut(cyl_x(CABLE_Y, CABLE_Z, CABLE_D, -1, WALL + 1))

# ======================= VEGG (høyre, montert) =======================
T = 6.0; OPEN_H = 120.0; RAIL_B, RAIL_T = 12.0, 10.0; POST = SLAT = 8.0; N_SLATS = 5
FOOT_W, FOOT_T = 20.0, 4.0; SCREW_X = (12.0, 75.0, 138.0)
gap = (L - 2 * POST - N_SLATS * SLAT) / (N_SLATS + 1)
slat_x = [POST + gap + i * (SLAT + gap) for i in range(N_SLATS)]

v = box(0, L, 0, T, -GROOVE_D, OPEN_H)                        # lokalt: y fra innerflaten og ut, z fra gulvflaten
for i in range(N_SLATS + 1):
    x0 = POST + i * (SLAT + gap)
    v = v.cut(box(x0, x0 + gap, -1, T + 1, RAIL_B, OPEN_H - RAIL_T))
v = v.union(box(slat_x[-1] + SLAT, L - POST, 0, T, RAIL_B - 0.1, 28.0))
v = v.union(box(0, L, 0, FOOT_W, 0, FOOT_T))
for x in SCREW_X:
    v = v.cut(cyl_z(x, 13.0, 3.6, -1, FOOT_T + 1))
    v = v.cut(cyl_z(x, T / 2, 2.5, OPEN_H - 10.0, OPEN_H + 1))
v = v.cut(cyl_y(138.0, 116.0, 3.4, -1, T + 1))                # bobs-aksel
v = v.cut(cyl_y(132.0, 17.0, 6.4, -1, T + 1))                 # stoppstang
vegg_h = v.translate((0, LANE / 2, Z_FLOOR))
vegg_v = vegg_h.mirror('XZ')                                   # speilet om Y=0 → venstre side

# ======================= TAK (montert) =======================
Y_OUT = LANE / 2 + T; LIP, LIP_H = 1.2, 3.0; Z_ROOF = Z_FLOOR + OPEN_H
t = cq.Workplane('XY')
parts = []
for s in (-1, 1):
    y0, y1 = (LANE / 2, Y_OUT) if s > 0 else (-Y_OUT, -LANE / 2)
    parts.append(box(0, L, y0, y1, 0, T))
    yl0, yl1 = (LANE / 2 - LIP, LANE / 2) if s > 0 else (-LANE / 2, -LANE / 2 + LIP)
    parts.append(box(0, L, yl0, yl1, -LIP_H, T))
for x in [0.0] + slat_x + [L - POST]:
    parts.append(box(x, x + SLAT, -Y_OUT, Y_OUT, 0, T))
t = parts[0]
for p_ in parts[1:]:
    t = t.union(p_)
t = t.cut(box(130, 146, -Y_OUT - 1, Y_OUT + 1, -LIP_H - 1, 0))  # styrekant kuttet ved bobs-akselen
for x in SCREW_X:
    for y in (LANE / 2 + T / 2, -(LANE / 2 + T / 2)):
        t = t.cut(cyl_z(x, y, 3.4, -1, T + 1))
        cone = cq.Solid.makeCone(3.4 / 2, 6.5 / 2, 2.0, cq.Vector(x, y, T - 2.0), cq.Vector(0, 0, 1))
        t = t.cut(cq.Workplane('XY').add(cone))
tak = t.translate((0, 0, Z_ROOF))

# ======================= EKSPORT =======================
deler = {'modul_B_kar': kar, 'modul_B_vegg_hoyre': vegg_h, 'modul_B_vegg_venstre': vegg_v, 'modul_B_tak': tak}
for navn, wp in deler.items():
    sol = wp.val()
    cq.exporters.export(wp, os.path.join(OUT, navn + '.step'))
    bb = sol.BoundingBox()
    print(f'{navn}.step: gyldig={sol.isValid()}, volum {sol.Volume()/1000:.1f} cm3, '
          f'bbox X {bb.xmin:.1f}..{bb.xmax:.1f}  Y {bb.ymin:.1f}..{bb.ymax:.1f}  Z {bb.zmin:.1f}..{bb.zmax:.1f}')

asm = cq.Assembly(name='modul_B')
asm.add(kar, name='kar', color=cq.Color(0.85, 0.85, 0.85))
asm.add(vegg_h, name='vegg_hoyre', color=cq.Color(0.72, 0.80, 0.90))
asm.add(vegg_v, name='vegg_venstre', color=cq.Color(0.72, 0.80, 0.90))
asm.add(tak, name='tak', color=cq.Color(0.90, 0.84, 0.72))
asm.save(os.path.join(OUT, 'modul_B_sammenstilling.step'))
print('modul_B_sammenstilling.step: 4 komponenter')

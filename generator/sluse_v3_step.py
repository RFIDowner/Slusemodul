#!/usr/bin/env python3
"""Hele duesluse v3 (modul A + M + B) som STEP, der hver modul er ÉN body
(kar + begge veggpaneler + takpanel smeltet sammen). Til utforming og videre arbeid i Fusion.
For print brukes STL-ene / de delte STEP-filene per del.

Koordinater (montert): X langs løpet (0 = inngang, 350 = utgang), Y på tvers (0 = senter),
Z opp (0 = landingsbrettet, 32 = gulvflaten).
  A: X 0–110   rett spole, hunn-svalehaler mot M
  M: X 110–200 elektronikkammer (lukket med lokk), hann-svalehaler i begge ender
  B: X 200–350 diamantspole, hunn-svalehaler mot M, hull for bobs-aksel og stoppstang
"""
import math, os
import cadquery as cq

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'step')
os.makedirs(OUT, exist_ok=True)

# ---------- felles mål ----------
W = 150.0; H = 32.0; LANE = 110.0
WALL = 2.4; FLOOR = 4.0; COIL = 100.0; CLR = 0.4; POCKET_D = 6.0; FRAME_T = 2.4
RIB_T = 2.4; RIB_H = 20.0; SCREW_D = 3.4
DT_BASE, DT_TIP, DT_DEPTH, DT_CLR, DT_Z0 = 10.0, 14.0, 6.0, 0.3, 2.0; DT_Y = (-48.0, 48.0)
CABLE_D, CABLE_Z, CABLE_Y = 8.0, 10.0, -66.0
BOARD_L, BOARD_W, BOARD_H = 40.0, 20.0, 8.0
T = 6.0; OPEN_H = 120.0; RAIL_B, RAIL_T = 12.0, 10.0; POST = SLAT = 8.0
FOOT_W, FOOT_T = 20.0, 4.0; LIP, LIP_H = 1.2, 3.0
LID_T = 3.0                                   # modul M: lokk (smeltet inn i body)

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane('XY').box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def cyl_z(x, y, d, z0, z1):
    return cq.Workplane('XY').circle(d / 2).extrude(z1 - z0).translate((x, y, z0))
def cyl_x(y, z, d, x0, x1):
    return cq.Workplane('YZ').circle(d / 2).extrude(x1 - x0).translate((x0, y, z))
def cyl_y(x, z, d, y0, y1):
    return cq.Workplane('XZ').circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))
def square(cx, cy, side, z0, z1):
    return box(cx - side / 2, cx + side / 2, cy - side / 2, cy + side / 2, z0, z1)
def diamond(cx, cy, side, z0, z1):
    return cq.Workplane('XY').polygon(4, side * math.sqrt(2)).extrude(z1 - z0).translate((cx, cy, z0))
def prism(pts, z0, z1):
    return cq.Workplane('XY').polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))

def slat_layout(L):
    n = max(2, round((L - 2 * POST + 22) / 30))
    gap = (L - 2 * POST - n * SLAT) / (n + 1)
    return n, gap, [POST + gap + i * (SLAT + gap) for i in range(n)]

def dovetail_female(x_face, into, yc):
    """Hunnspor skåret inn i endeveggen ved x_face; into = +1 (inn mot +X) eller -1."""
    c = DT_CLR; xin = x_face + into * (DT_DEPTH + c); xo = x_face - into * 0.5
    return prism([(xo, yc - DT_BASE / 2 - c), (xin, yc - DT_TIP / 2 - c), (xin, yc + DT_TIP / 2 + c), (xo, yc + DT_BASE / 2 + c)], DT_Z0, H + 1)

def dovetail_male(x_face, out, yc):
    """Hann-list som stikker ut fra endeveggen ved x_face; out = retning utover (+1/-1)."""
    xt = x_face + out * DT_DEPTH; xi = x_face - out * 0.5
    return prism([(xi, yc - DT_BASE / 2), (xt, yc - DT_TIP / 2), (xt, yc + DT_TIP / 2), (xi, yc + DT_BASE / 2)], DT_Z0, H)

# ---------- kar ----------
def kar(L, coil=None, female=(), male=(), chamber=False):
    k = box(0, L, -W / 2, W / 2, 0, H)
    if chamber:
        k = k.cut(box(WALL, L - WALL, -W / 2 + WALL, W / 2 - WALL, LID_T, H - FLOOR))   # lukket kammer (lokk innsmeltet)
    else:
        k = k.cut(box(WALL, L - WALL, -W / 2 + WALL, W / 2 - WALL, -1, H - FLOOR))      # hult, åpent mot brettet
    if coil:
        cx = L / 2; zp0, zp1 = H - FLOOR - POCKET_D, H - FLOOR
        shape = diamond if coil == 'diamond' else square
        k = k.union(shape(cx, 0, COIL + 2 * CLR + 2 * FRAME_T, zp0, zp1).cut(shape(cx, 0, COIL + 2 * CLR, zp0 - 1, zp1 + 1)))
        for y in (-62.0, 62.0):
            k = k.union(box(WALL, L - WALL, y - RIB_T / 2, y + RIB_T / 2, 0, RIB_H))
        for x in (20.0, L - 20.0):
            k = k.union(box(x - RIB_T / 2, x + RIB_T / 2, -W / 2 + WALL, W / 2 - WALL, 0, RIB_H))
        k = k.cut(shape(cx, 0, COIL + 2 * CLR, zp0, zp1))
        k = k.cut(box(cx - BOARD_L / 2, cx + BOARD_L / 2, -W / 2 + WALL + 1, -W / 2 + WALL + 1 + BOARD_W, H - FLOOR - BOARD_H, H - FLOOR))
    for x in (12.0, L / 2, L - 12.0):
        for y in (-68.0, 68.0):
            k = k.cut(cyl_z(x, y, SCREW_D, H - FLOOR - 1, H + 1))
    for (x_face, into) in female:                        # fortykning + spor
        for yc in DT_Y:
            x0, x1 = (x_face, x_face + 8.0) if into > 0 else (x_face - 8.0, x_face)
            k = k.union(box(x0, x1, yc - 12.0, yc + 12.0, 0, H))
        for yc in DT_Y:
            k = k.cut(dovetail_female(x_face, into, yc))
    for (x_face, out) in male:
        for yc in DT_Y:
            k = k.union(dovetail_male(x_face, out, yc))
    for (x_face, into) in list(female) + [(xf, -o) for (xf, o) in male]:   # kabelhull i hver skjøtevegg
        x0, x1 = (x_face - 1, x_face + WALL + 1) if into > 0 else (x_face - WALL - 1, x_face + 1)
        k = k.cut(cyl_x(CABLE_Y, CABLE_Z, CABLE_D, x0, x1))
    return k

# ---------- vegg (høyre, montert) ----------
def vegg(L, bobs=False):
    n, gap, sx = slat_layout(L)
    v = box(0, L, 0, T, -1.5, OPEN_H)
    for i in range(n + 1):
        x0 = POST + i * (SLAT + gap)
        v = v.cut(box(x0, x0 + gap, -1, T + 1, RAIL_B, OPEN_H - RAIL_T))
    screw_x = (12.0, L / 2, L - 12.0)
    if bobs:
        v = v.union(box(sx[-1] + SLAT, L - POST, 0, T, RAIL_B - 0.1, 28.0))
    v = v.union(box(0, L, 0, FOOT_W, 0, FOOT_T))
    for x in screw_x:
        v = v.cut(cyl_z(x, 13.0, 3.6, -1, FOOT_T + 1))
        v = v.cut(cyl_z(x, T / 2, 2.5, OPEN_H - 10.0, OPEN_H + 1))
    if bobs:
        v = v.cut(cyl_y(L - 12.0, 116.0, 3.4, -1, T + 1))
        v = v.cut(cyl_y(L - 18.0, 17.0, 6.4, -1, T + 1))
    return v.translate((0, LANE / 2, H))

# ---------- tak (montert) ----------
def tak(L, bobs=False):
    n, gap, sx = slat_layout(L)
    Y_OUT = LANE / 2 + T
    parts = []
    for s in (-1, 1):
        y0, y1 = (LANE / 2, Y_OUT) if s > 0 else (-Y_OUT, -LANE / 2)
        parts.append(box(0, L, y0, y1, 0, T))
        yl0, yl1 = (LANE / 2 - LIP, LANE / 2) if s > 0 else (-LANE / 2, -LANE / 2 + LIP)
        parts.append(box(0, L, yl0, yl1, -LIP_H, T))
    for x in [0.0] + sx + [L - POST]:
        parts.append(box(x, x + SLAT, -Y_OUT, Y_OUT, 0, T))
    t = parts[0]
    for p_ in parts[1:]:
        t = t.union(p_)
    if bobs:
        t = t.cut(box(L - 20, L - 4, -Y_OUT - 1, Y_OUT + 1, -LIP_H - 1, 0))
    for x in (12.0, L / 2, L - 12.0):
        for y in (LANE / 2 + T / 2, -(LANE / 2 + T / 2)):
            t = t.cut(cyl_z(x, y, 3.4, -1, T + 1))
            t = t.cut(cq.Workplane('XY').add(cq.Solid.makeCone(1.7, 3.25, 2.0, cq.Vector(x, y, T - 2.0), cq.Vector(0, 0, 1))))
    return t.translate((0, 0, H + OPEN_H))

# ---------- moduler ----------
def modul(L, coil, female, male, chamber, bobs):
    k = kar(L, coil, female, male, chamber)
    vh = vegg(L, bobs)
    vv = vh.mirror('XZ')
    return k.union(vh).union(vv).union(tak(L, bobs))

MODULER = [
    # navn, x-start, lengde, spole, hunn-skjøter, hann-skjøter, kammer, bobs
    ('A_rett_spole',    0.0, 110.0, 'square',  [(110.0, -1)], [],                      False, False),
    ('M_elektronikk', 110.0,  90.0, None,      [],            [(0.0, -1), (90.0, +1)], True,  False),
    ('B_diamant',     200.0, 150.0, 'diamond', [(0.0, +1)],   [],                      False, True),
]

bodies = []
for navn, x0, L, coil, fem, mal, ch, bobs in MODULER:
    wp = modul(L, coil, fem, mal, ch, bobs).translate((x0, 0, 0))
    sol = wp.val()
    n_sol = len(wp.solids().vals())
    bb = sol.BoundingBox()
    print(f'{navn}: solider={n_sol}, gyldig={sol.isValid()}, volum {sol.Volume()/1000:.1f} cm3, X {bb.xmin:.1f}..{bb.xmax:.1f}, Z {bb.zmin:.1f}..{bb.zmax:.1f}')
    cq.exporters.export(wp, os.path.join(OUT, f'sluse_v3_modul_{navn}.step'))
    bodies.append((navn, sol))

# én STEP med tre bodies (compound) – Fusion viser dem som Body1–3 i samme komponent
comp = cq.Compound.makeCompound([s for _, s in bodies])
cq.exporters.export(cq.Workplane('XY').add(comp), os.path.join(OUT, 'sluse_v3_komplett_3_bodies.step'))
print('sluse_v3_komplett_3_bodies.step skrevet')

# kontroll: modulene skal ikke overlappe (bortsett fra svalehalene som går inn i sporene)
for i in range(len(bodies)):
    for j in range(i + 1, len(bodies)):
        ov = bodies[i][1].intersect(bodies[j][1]).Volume()
        print(f'overlapp {bodies[i][0]} ∩ {bodies[j][0]}: {ov:.2f} mm3')

# STL av komplett modell for visuell sjekk
cq.exporters.export(cq.Workplane('XY').add(comp), '/tmp/sluse_v3_komplett.stl', tolerance=0.2, angularTolerance=0.3)

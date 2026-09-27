#!/usr/bin/env python3
"""Sluse M+A – ett kar (200 mm): elektronikkammer først (forgang), rett spole etter, gafler i utgangen.
Vegger og tak festes med klikk-tapper (ingen skruer). Lager STEP (montert) og STL (print-orientert).

Koordinater (montert): X langs løpet (0 = inngang, 200 = utgang mot slaget), Y på tvers (0 = senter),
Z opp (0 = landingsbrettet, 32 = gulvflaten).
"""
import math, os
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STEP = os.path.join(HERE, '..', 'step', 'sluse_MA')
OUT_STL = os.path.join(HERE, '..', 'stl', 'sluse_MA')
os.makedirs(OUT_STEP, exist_ok=True); os.makedirs(OUT_STL, exist_ok=True)

# ---------------- hovedmål ----------------
L, W, H = 200.0, 150.0, 32.0
WALL, FLOOR, LANE, T = 2.4, 4.0, 110.0, 6.0
Z_FL = H                                   # gulvflate
M_END = 88.0; DIV_T = 2.4                  # kammer innv. x 2.4..88, skillevegg 88..90.4
A0 = M_END + DIV_T                         # 90.4
CX = 145.0                                 # spolesenter
COIL = 100.0; CLR = 0.7; POCKET_D = 6.0; FRAME_T = 2.4
PK = COIL / 2 + CLR                        # 50.7 = lommens halvbredde
ZP0, ZP1 = Z_FL - FLOOR - POCKET_D, Z_FL - FLOOR     # 22 .. 28
LID_T = 3.0
GROOVE_W, GROOVE_D = 6.4, 1.5
OPEN_H, RAIL_B, RAIL_T, POST, SLAT = 120.0, 12.0, 10.0, 8.0, 8.0
FOOT_W, FOOT_T = 20.0, 4.0
BOB_X, AXLE_Z = 188.0, 116.0               # aksel (lokal høyde over gulv)
SILL_X, SILL_Z = 182.0, 6.0                # terskelstang (lokal høyde over gulv)
BOBS_Y = (-44.0, -22.0, 0.0, 22.0, 44.0)
BOB_D, BOB_LEN, BOB_HOLE_FROM_TOP = 6.0, 116.0, 3.0
PRONG_X = (148.0, 168.0, 188.0)            # klikk-tapper vegg→gulv (kun i A-delen)
ROOF_PRONG_X = (30.0, 100.0, 160.0)        # klikk-tapper tak→vegg

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane('XY').box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def cyl_z(x, y, d, z0, z1):
    return cq.Workplane('XY').circle(d / 2).extrude(z1 - z0).translate((x, y, z0))
def cyl_x(y, z, d, x0, x1):
    return cq.Workplane('YZ').circle(d / 2).extrude(x1 - x0).translate((x0, y, z))
def cyl_y(x, z, d, y0, y1):
    return cq.Workplane('XZ').circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))
def prism_yz(pts, x0, x1):
    """Prisme med profil i YZ-planet (liste av (y,z)), ekstrudert langs X fra x0 til x1."""
    return cq.Workplane('YZ').polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))
def prism_xz(pts, y0, y1):
    """Prisme med profil i XZ-planet (liste av (x,z)), ekstrudert langs Y fra y0 til y1."""
    return cq.Workplane('XZ').polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))

# ======================= KAR =======================
k = box(0, L, -W / 2, W / 2, 0, H)
# M: lukket kammer (lokk fra undersiden)
k = k.cut(box(WALL, M_END, -W / 2 + WALL, W / 2 - WALL, -1, Z_FL - FLOOR))
# A: hult, åpent mot brettet
k = k.cut(box(A0, L - WALL, -W / 2 + WALL, W / 2 - WALL, -1, Z_FL - FLOOR))
# kammer: kant rundt for lokket (z 3..6) + hjørneklosser med skruehull
ledge = box(WALL, M_END, -W / 2 + WALL, W / 2 - WALL, LID_T, LID_T + 3).cut(
    box(WALL + 2.5, M_END - 2.5, -W / 2 + WALL + 2.5, W / 2 - WALL - 2.5, LID_T - 1, LID_T + 4))
k = k.union(ledge)
BOSS = [(WALL + 4, -W / 2 + WALL + 4), (WALL + 4, W / 2 - WALL - 4), (M_END - 4, -W / 2 + WALL + 4), (M_END - 4, W / 2 - WALL - 4)]
for (bx, by) in BOSS:
    k = k.union(box(bx - 4, bx + 4, by - 4, by + 4, LID_T, Z_FL - FLOOR))
for (bx, by) in BOSS:
    k = k.cut(cyl_z(bx, by, 2.8, LID_T - 1, LID_T + 12))
# PG7-hull for strømkabel i kammerets sidevegg
k = k.cut(cyl_y(45.0, 15.0, 12.5, -W / 2 - 1, -W / 2 + WALL + 1))
# A: ramme rundt spolelommen (henger ned fra gulvet)
frame = box(CX - PK - FRAME_T, CX + PK + FRAME_T, -PK - FRAME_T, PK + FRAME_T, ZP0, ZP1).cut(
    box(CX - PK, CX + PK, -PK, PK, ZP0 - 1, ZP1 + 1))
k = k.union(frame)
# A: ribber på langs, utenfor spolen
for y in (-62.0, 62.0):
    k = k.union(box(A0, L - WALL, y - 1.2, y + 1.2, 0, 20.0))
# klikk-faner i rammen: to slisser gjør et 18 mm bredt fjærende felt, med nese som holder spolen
NOSE_IN, NOSE_TOP, NOSE_H, RAMP_H = 1.2, Z_FL - FLOOR - 2.0, 1.2, 1.5      # spolen (2 mm) ligger z 26..28
tabs = [('+x', CX + PK, 0.0), ('-x', CX - PK, 0.0), ('+y', CX, PK), ('-y', CX + 30.0, -PK)]
for side, a, b in tabs:
    if side in ('+x', '-x'):
        s = 1 if side == '+x' else -1
        xf = a
        for yy in (b - 9.5, b + 9.5):                                   # slisser
            k = k.cut(box(min(xf, xf + s * FRAME_T) - 0.1, max(xf, xf + s * FRAME_T) + 0.1, yy - 0.5, yy + 0.5, ZP0 - 1, ZP1 - 1))
        prof = [(xf, NOSE_TOP - NOSE_H - RAMP_H), (xf - s * NOSE_IN, NOSE_TOP - NOSE_H), (xf - s * NOSE_IN, NOSE_TOP), (xf, NOSE_TOP)]
        k = k.union(prism_xz(prof, b - 8.5, b + 8.5))
    else:
        s = 1 if side == '+y' else -1
        yf = b
        for xx in (a - 9.5, a + 9.5):
            k = k.cut(box(xx - 0.5, xx + 0.5, min(yf, yf + s * FRAME_T) - 0.1, max(yf, yf + s * FRAME_T) + 0.1, ZP0 - 1, ZP1 - 1))
        prof = [(yf, NOSE_TOP - NOSE_H - RAMP_H), (yf - s * NOSE_IN, NOSE_TOP - NOSE_H), (yf - s * NOSE_IN, NOSE_TOP), (yf, NOSE_TOP)]
        k = k.union(prism_yz(prof, a - 8.5, a + 8.5))
# gjenåpne lommen (sikkerhet) – men ikke nesene
k = k.cut(box(CX - PK + NOSE_IN, CX + PK - NOSE_IN, -PK + NOSE_IN, PK - NOSE_IN, ZP0 - 1, ZP1))
# utsparing for spolens kort (36x15) på -y-siden, nær skilleveggen
k = k.cut(box(96.0, 136.0, -73.0, -PK + 0.5, Z_FL - FLOOR - 8.0, Z_FL - FLOOR))
# kabelhull i skilleveggen, høyt (rett under gulvet)
k = k.cut(cyl_x(-68.0, 23.0, 6.0, M_END - 1, A0 + 1))
# styrespor for veggene i gulvflaten (hele lengden)
for y0 in (-LANE / 2 - GROOVE_W, LANE / 2):
    k = k.cut(box(-1, L + 1, y0, y0 + GROOVE_W, Z_FL - GROOVE_D, Z_FL + 1))
# slisser for veggenes klikk-tapper (bare i A-delen, der det er hult under)
for s in (1, -1):
    for px in PRONG_X:
        y_in, y_out = s * (LANE / 2 - 1.2), s * (LANE / 2 + 3.2)
        k = k.cut(box(px - 6.2, px + 6.2, min(y_in, y_out), max(y_in, y_out), Z_FL - FLOOR - 1, Z_FL + 1))

# ======================= LOKK (kammer) =======================
lid = box(WALL + 0.3, M_END - 0.3, -W / 2 + WALL + 0.3, W / 2 - WALL - 0.3, 0, LID_T)
# pakningsspor (Ø2 silikonsnor) mot kanten
g_out = box(WALL + 0.9, M_END - 0.9, -W / 2 + WALL + 0.9, W / 2 - WALL - 0.9, LID_T - 1.4, LID_T + 1)
g_in = box(WALL + 2.9, M_END - 2.9, -W / 2 + WALL + 2.9, W / 2 - WALL - 2.9, LID_T - 2, LID_T + 2)
lid = lid.cut(g_out.cut(g_in))
for (bx, by) in BOSS:
    lid = lid.cut(cyl_z(bx, by, 3.4, -1, LID_T + 1))
    lid = lid.cut(cq.Workplane('XY').add(cq.Solid.makeCone(3.3, 1.7, 1.6, cq.Vector(bx, by, 0), cq.Vector(0, 0, 1))))

# ======================= VEGG (høyre, lokalt → montert) =======================
n = max(2, round((L - 2 * POST + 22) / 30)); gap = (L - 2 * POST - n * SLAT) / (n + 1)
v = box(0, L, 0, T, -GROOVE_D, OPEN_H)
for i in range(n + 1):
    x0 = POST + i * (SLAT + gap)
    v = v.cut(box(x0, x0 + gap, -1, T + 1, RAIL_B, OPEN_H - RAIL_T))
v = v.union(box(0, L, 0, FOOT_W, 0, FOOT_T))
v = v.cut(cyl_y(BOB_X, AXLE_Z, 3.4, -1, T + 1))                    # aksel
v = v.cut(cyl_y(SILL_X, SILL_Z, 6.4, -1, FOOT_W + 1))              # terskelstang (gjennom panel og fot)
# spor på utsiden av topplisten for takets klikk-tapper
v = v.cut(box(-1, L + 1, T - 1.0, T + 1, OPEN_H - 9.4, OPEN_H - 6.4))
# klikk-tapper ned gjennom gulvet (lokalt: y 0..3, med mothake på +y-siden)
for px in PRONG_X:
    v = v.union(box(px - 6.0, px + 6.0, 0, 3.0, -FLOOR - 3.2, -GROOVE_D + 0.01))
    barb = [(3.0, -FLOOR - 3.2), (3.0, -FLOOR), (3.9, -FLOOR), (3.9, -FLOOR - 1.2), (3.0, -FLOOR - 3.2)]
    v = v.union(prism_yz([(3.0, -FLOOR - 3.2), (3.9, -FLOOR - 1.4), (3.9, -FLOOR), (3.0, -FLOOR)], px - 6.0, px + 6.0))
vegg_h = v.translate((0, LANE / 2, Z_FL))
vegg_v = vegg_h.mirror('XZ')

# ======================= TAK =======================
Y_OUT = LANE / 2 + T; LIP, LIP_H = 1.2, 3.0; Z_R = Z_FL + OPEN_H
parts = []
for s in (-1, 1):
    y0, y1 = (LANE / 2, Y_OUT) if s > 0 else (-Y_OUT, -LANE / 2)
    parts.append(box(0, L, y0, y1, 0, T))
    yl0, yl1 = (LANE / 2 - LIP, LANE / 2) if s > 0 else (-LANE / 2, -LANE / 2 + LIP)
    parts.append(box(0, L, yl0, yl1, -LIP_H, T))
for x in [0.0] + [POST + gap + i * (SLAT + gap) for i in range(n)] + [L - POST]:
    parts.append(box(x, x + SLAT, -Y_OUT, Y_OUT, 0, T))
t = parts[0]
for p_ in parts[1:]:
    t = t.union(p_)
t = t.cut(box(BOB_X - 8, BOB_X + 8, -Y_OUT - 1, Y_OUT + 1, -LIP_H - 1, 0))       # styrekant fri for akselen
# klikk-tapper ned på utsiden av veggens topplist
for s in (1, -1):
    for px in ROOF_PRONG_X:
        yo = s * (Y_OUT + 0.2)
        t = t.union(box(px - 6.0, px + 6.0, min(yo, yo + s * 2.4), max(yo, yo + s * 2.4), -9.0, 0.01))
        t = t.union(box(px - 6.0, px + 6.0, min(s * (Y_OUT - 1), yo + s * 2.4), max(s * (Y_OUT - 1), yo + s * 2.4), 0, T))
        # mothake inn mot veggens spor (lokal tak-z: veggspor ligger -8.0..-6.4 under takets underside)
        prof = [(yo, -8.8), (yo - s * 0.9, -7.8), (yo - s * 0.9, -6.4), (yo, -6.4)]
        t = t.union(prism_yz(prof, px - 6.0, px + 6.0))
tak = t.translate((0, 0, Z_R))

# ======================= GAFLER, AKSEL, TERSKEL =======================
bobs = []
for by in BOBS_Y:
    z_top = Z_FL + AXLE_Z + BOB_HOLE_FROM_TOP
    b = cyl_z(BOB_X, by, BOB_D, z_top - BOB_LEN, z_top).cut(cyl_x(by, Z_FL + AXLE_Z, 3.4, BOB_X - 5, BOB_X + 5).rotate((BOB_X, by, 0), (BOB_X, by, 1), 90))
    bobs.append(b)
sill = cyl_y(SILL_X, Z_FL + SILL_Z, 6.0, -Y_OUT - 2, Y_OUT + 2)
axle = cyl_y(BOB_X, Z_FL + AXLE_Z, 3.0, -Y_OUT - 3, Y_OUT + 3)
coil_ref = box(CX - 50, CX + 50, -50, 50, Z_FL - FLOOR - 2, Z_FL - FLOOR).cut(box(CX - 48, CX + 48, -48, 48, 0, 40))

# ======================= KONTROLL =======================
deler = {'kar': k, 'lokk': lid.translate((0, 0, 0)), 'vegg_hoyre': vegg_h, 'vegg_venstre': vegg_v, 'tak': tak,
         'terskelstang': sill}
for i, b in enumerate(bobs):
    deler[f'gaffel_{i+1}'] = b
for navn, wp in deler.items():
    so = wp.val(); bb = so.BoundingBox()
    print(f'{navn:13s} solider={len(wp.solids().vals())} gyldig={so.isValid()} vol={so.Volume()/1000:6.1f} cm3  '
          f'X {bb.xmin:6.1f}..{bb.xmax:6.1f} Y {bb.ymin:6.1f}..{bb.ymax:6.1f} Z {bb.zmin:6.1f}..{bb.zmax:6.1f}')
print('--- kollisjoner (mm3, skal være ~0) ---')
pairs = [('kar', 'vegg_hoyre'), ('kar', 'vegg_venstre'), ('kar', 'lokk'), ('vegg_hoyre', 'tak'), ('vegg_venstre', 'tak'),
         ('vegg_hoyre', 'terskelstang'), ('kar', 'terskelstang'), ('tak', 'gaffel_3'), ('kar', 'gaffel_3'), ('terskelstang', 'gaffel_3')]
for a, b in pairs:
    print(f'{a:13s} ∩ {b:13s}: {deler[a].val().intersect(deler[b].val()).Volume():8.2f}')
print(f'spole ∩ kar (nesene som griper spolen, forventet > 0): {coil_ref.val().intersect(k.val()).Volume():.1f}')

# ======================= EKSPORT =======================
asm = cq.Assembly(name='sluse_MA')
farge = {'kar': (0.85, 0.85, 0.85), 'lokk': (0.6, 0.8, 0.6), 'vegg_hoyre': (0.72, 0.8, 0.9), 'vegg_venstre': (0.72, 0.8, 0.9),
         'tak': (0.9, 0.84, 0.72), 'terskelstang': (0.3, 0.3, 0.3)}
for navn, wp in deler.items():
    asm.add(wp, name=navn, color=cq.Color(*farge.get(navn, (1.0, 1.0, 1.0))))
asm.add(axle, name='aksel_rustfri_ref', color=cq.Color(0.5, 0.5, 0.55))
asm.add(coil_ref, name='spole_referanse', color=cq.Color(0.9, 0.5, 0.1))
asm.save(os.path.join(OUT_STEP, 'sluse_MA_sammenstilling.step'))
for navn, wp in deler.items():
    if not navn.startswith('gaffel'):
        cq.exporters.export(wp, os.path.join(OUT_STEP, f'sluse_MA_{navn}.step'))

def to_bed(wp):
    bb = wp.val().BoundingBox(); return wp.translate((-bb.xmin, -bb.ymin, -bb.zmin))
def stl(wp, name):
    cq.exporters.export(to_bed(wp), os.path.join(OUT_STL, name), tolerance=0.02, angularTolerance=0.1)
stl(k.rotate((0, 0, 0), (1, 0, 0), 180), 'sluse_MA_kar.stl')                        # gulvflaten ned
stl(lid, 'sluse_MA_lokk.stl')                                                        # pakningssporet opp
stl(vegg_h.translate((0, -LANE / 2, -Z_FL)).rotate((0, 0, 0), (1, 0, 0), 90), 'sluse_MA_vegg_hoyre.stl')   # innerflaten ned
stl(vegg_v.translate((0, LANE / 2, -Z_FL)).rotate((0, 0, 0), (1, 0, 0), -90), 'sluse_MA_vegg_venstre.stl')
stl(tak.rotate((0, 0, 0), (1, 0, 0), 180), 'sluse_MA_tak.stl')                       # toppen ned, tappene opp
# gafler + terskel liggende på ett brett
plate = None
for i, b in enumerate(bobs + [sill]):
    bb = b.val().BoundingBox()
    lay = b.rotate((0, 0, 0), (0, 1, 0), 90) if i < len(bobs) else b.rotate((0, 0, 0), (0, 0, 1), 90)   # gafler legges ned; terskelen ligger allerede
    lay = to_bed(lay).translate((0, i * 12.0, 0))
    plate = lay if plate is None else plate.union(lay)
stl(plate, 'sluse_MA_gafler_og_terskel.stl')
print('eksport ferdig')

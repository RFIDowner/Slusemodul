#!/usr/bin/env python3
"""Duesluse v4.3 – som v4.2, men med kabelføring, kortfeste og nytt lokk:

- Lokket under el-rommet er løftet 4 mm over brettet. Det skyves inn fra inngangsenden i spor
  (kile under, skinne over, begge med 45° så de printes uten støtte) og låses med en klikk-tunge.
  Ingen skruer, ingen pakning. Dreneringsslisser og fingerhull i lokket.
- Leseren (35 × 15 × 1 mm) sitter i en holder inne i el-rommet, i hjørnet ved skilleveggen.
  Spoletrådene går gjennom en 2 mm sprekk i skilleveggen (tettes med Sika).
- Strømkabelen kommer inn under sideveggen (slisse i underkanten) og gjennom en 5 mm slisse i
  skilleveggen (Sika). PG7-hullet og det blinde Ø6-hullet er borte.
- PigeonPal-PCB henger under gulvet på tre styretapper (H1, H3, H4) og to fjærende kroker,
  komponentsiden ned, pluggkanten (J9, J3, J4) mot −y med 55 mm fri plass.
- Ribbene under leseren er fjernet. Slissene for veggtappene har runde ender.
- Gaflene har en 8-kantet nav på 21 mm langs akselen, så de holder avstanden selv.
  Stangen ligger flush med navet på én side, så gaffelen ligger flatt i printen.

Koordinater (montert): X langs løpet (0 = inngang, 200 = utgang mot slaget), Y på tvers (0 = senter),
Z opp (0 = landingsbrettet, 32 = gulvflaten).
"""
import math, os
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STEP = os.path.join(HERE, '..', 'step', 'v4.3')
OUT_STL = os.path.join(HERE, '..', 'stl', 'v4.3')
os.makedirs(OUT_STEP, exist_ok=True); os.makedirs(OUT_STL, exist_ok=True)

# ---------------- hovedmål ----------------
L, W, H = 200.0, 150.0, 32.0
WALL, FLOOR, LANE, T = 2.4, 4.0, 110.0, 6.0
Z_FL = H                                   # gulvflate
Y_IN = W / 2 - WALL                        # 72.6 = innsiden av sideveggene
M_END = 88.0; DIV_T = 2.4                  # kammer innv. x 2.4..88, skillevegg 88..90.4
A0 = M_END + DIV_T                         # 90.4
CX = 145.0                                 # spolesenter
COIL = 100.0; CLR = 0.7; POCKET_D = 6.0; FRAME_T = 2.4
PK = COIL / 2 + CLR                        # 50.7 = lommens halvbredde
ZP0, ZP1 = Z_FL - FLOOR - POCKET_D, Z_FL - FLOOR     # 22 .. 28
GROOVE_W, GROOVE_D = 6.4, 1.5
OPEN_H, RAIL_B, RAIL_T, POST, SLAT = 120.0, 12.0, 10.0, 8.0, 8.0
FOOT_W, FOOT_T = 12.0, 4.0
BOB_X, AXLE_Z = 188.0, 116.0               # aksel (lokal høyde over gulv)
BOBS_Y = (-44.0, -22.0, 0.0, 22.0, 44.0)
BOB_F, HUB_F, HUB_LEN, ROD_OFF = 6.0, 9.0, 21.0, 1.5   # 8-kant stang, 8-kant nav, navlengde, stangforskyvning
STOP_DROP, BOB_BELOW, BOB_GAP = 10.0, 2.0, 0.2
PRONG_X = (148.0, 168.0, 188.0)            # klikk-tapper vegg→gulv
# lokk
LID_Z0, LID_T, LID_CLR = 4.0, 3.0, 0.3     # lokk z 4..7, løftet 4 mm over brettet
WEDGE_W, RAIL_W = 3.0, 2.0                 # kile under lokket, skinne over
LID_W2 = Y_IN - 0.3                        # 72.3 = halv lokkbredde
LID_X1 = M_END - 0.3                       # 87.7
Z_RAIL = LID_Z0 + LID_T + LID_CLR          # 7.3 = underkant skinne
# kort (PigeonPal-PCB, 60 × 53.1 i KiCad; her 53.1 langs x og 60 langs y)
PCB_X0, PCB_Y0, PCB_L, PCB_W, PCB_T = 6.0, -18.0, 53.1, 60.0, 1.6
STANDOFF = 7.0
PCB_ZT = Z_FL - FLOOR - STANDOFF           # 21.0 = kortets bakside
PCB_ZB = PCB_ZT - PCB_T                    # 19.4 = komponentsiden
HOLES = ((72.771, 51.943), (72.771, 96.901), (124.0, 52.0))   # H4, H3, H1 i KiCad-mm
def kicad(xk, yk):
    """KiCad-koordinat → montert posisjon. Pluggkanten (KiCad x = 68.73) vender mot −y."""
    return PCB_X0 + (yk - 47.879), PCB_Y0 + (xk - 68.7345)
# leser
RD_L, RD_W, RD_T = 35.0, 15.0, 1.0
RD_Y0 = -Y_IN + 1.4                        # -71.2 = leserens ytterkant
RD_Y1 = RD_Y0 + RD_W                       # -56.2
Z_RD = Z_FL - FLOOR                        # 28 = leseren ligger mot gulvets underside
G_H, LIP = RD_T + 0.3, 1.0                 # sporhøyde og leppe

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
def oct_z(cx, cy, f, z0, z1):
    """8-kant med flatemål f, flater mot ±x og ±y, langs Z."""
    return cq.Workplane('XY').polygon(8, f / math.cos(math.pi / 8)).extrude(z1 - z0).rotate((0, 0, 0), (0, 0, 1), 22.5).translate((cx, cy, z0))
def oct_y(cx, cz, f, y0, y1):
    """8-kant med flatemål f, flater mot ±x og ±z, langs Y."""
    return cq.Workplane('XZ').polygon(8, f / math.cos(math.pi / 8)).extrude(-(y1 - y0)).rotate((0, 0, 0), (0, 1, 0), 22.5).translate((cx, y0, cz))

# ======================= KAR =======================
k = box(0, L, -W / 2, W / 2, 0, H)
k = k.cut(box(WALL, M_END, -Y_IN, Y_IN, -1, Z_FL - FLOOR))         # M: åpent nedover, lokket skyves inn
k = k.cut(box(A0, L - WALL, -Y_IN, Y_IN, -1, Z_FL - FLOOR))        # A: hult, åpent mot brettet
# lokkspor: kile under (lokket hviler på 45°-flaten) og skinne over (45° på oversiden). Ingen overheng i print.
for s in (1, -1):
    k = k.union(prism_yz([(s * Y_IN, 3.0), (s * Y_IN, 3.0 + WEDGE_W), (s * (Y_IN - WEDGE_W), 3.0)], WALL, M_END))
    k = k.union(prism_yz([(s * (Y_IN - RAIL_W), Z_RAIL), (s * Y_IN, Z_RAIL), (s * Y_IN, Z_RAIL + RAIL_W)], WALL, M_END))
# åpning i endeveggen ved inngangen: lokket skyves inn her
k = k.cut(box(-1, WALL + 0.05, -Y_IN, Y_IN, LID_Z0 - LID_CLR, LID_Z0 + LID_T + LID_CLR))
# A: ramme rundt spolelommen (henger ned fra gulvet)
frame = box(CX - PK - FRAME_T, CX + PK + FRAME_T, -PK - FRAME_T, PK + FRAME_T, ZP0, ZP1).cut(
    box(CX - PK, CX + PK, -PK, PK, ZP0 - 1, ZP1 + 1))
k = k.union(frame)
# klikk-faner i rammen: to slisser gjør et 18 mm bredt fjærende felt, med nese som holder spolen (uendret, fungerer)
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
# utsparing for spolens avstemmingskort (36x15) på -y-siden, nær skilleveggen
k = k.cut(box(96.0, 136.0, -73.0, -PK + 0.5, Z_FL - FLOOR - 8.0, Z_FL - FLOOR))
# styrespor for veggene i gulvflaten (hele lengden)
for y0 in (-LANE / 2 - GROOVE_W, LANE / 2):
    k = k.cut(box(-1, L + 1, y0, y0 + GROOVE_W, Z_FL - GROOVE_D, Z_FL + 1))
# slisser for veggenes klikk-tapper, med runde ender (rett del 12.4 mm, bredde 4.4)
for s in (1, -1):
    for px in PRONG_X:
        k = k.cut(cq.Workplane('XY').slot2D(12.4 + 4.4, 4.4).extrude(FLOOR + 2).translate((px, s * (LANE / 2 + 1.0), Z_FL - FLOOR - 1)))
# kabler gjennom skilleveggen: 2 mm sprekk for spoletrådene (ved leserens ende) og 5 mm slisse for strømkabelen
SLIT_Y = (-66.0, -64.0); PWR_Y = (-52.0, -47.0)
k = k.cut(box(M_END - 0.1, A0 + 0.1, SLIT_Y[0], SLIT_Y[1], -1, 20.0))
k = k.cut(box(M_END - 0.1, A0 + 0.1, PWR_Y[0], PWR_Y[1], -1, 18.0))
# slisse i underkanten av sideveggen (−y) for strømkabelen, rett etter skilleveggen
k = k.cut(box(92.0, 97.0, -W / 2 - 1, -Y_IN + 0.1, -1, 6.0))
# endekant mot slaget: skråflate som gaflene hviler mot (som v4.2, men stangen er forskjøvet 1.5 mm innover)
A_ABS = (BOB_X, Z_FL + AXLE_Z); C_STOP = (L, Z_FL - STOP_DROP)
_dx, _dz = C_STOP[0] - A_ABS[0], A_ABS[1] - C_STOP[1]
ROD_IN = BOB_F / 2 - ROD_OFF                                      # 1.5 = stangens innerflate (mot karet) fra akselsenter
BOB_TILT = math.atan2(_dx, _dz) + math.asin((ROD_IN + BOB_GAP) / math.hypot(_dx, _dz))
CHAMF = STOP_DROP * math.tan(BOB_TILT)
k = k.cut(prism_xz([(L, C_STOP[1]), (L - CHAMF, Z_FL), (L - CHAMF, Z_FL + 1), (L + 1, Z_FL + 1), (L + 1, C_STOP[1])], -LANE / 2 + 1, LANE / 2 - 1))

# --- leserholder i hjørnet ved skilleveggen: to skinner med spor, leseren skyves inn fra −x mot skilleveggen ---
RD_X0 = M_END - RD_L - 2.0                                        # 51
for (yv0, yv1, yg0, yg1) in ((-Y_IN, RD_Y0 + 1.2, RD_Y0 - 0.2, RD_Y0 + 1.21),          # ytre skinne, spor åpent mot +y
                             (RD_Y1 - 1.2, RD_Y1 + 1.4, RD_Y1 - 1.21, RD_Y1 + 0.2)):    # indre skinne, spor åpent mot −y
    k = k.union(box(RD_X0, M_END, yv0, yv1, Z_RD - G_H - LIP, Z_RD))
    k = k.cut(box(RD_X0 - 1, M_END - 0.5, yg0, yg1, Z_RD - G_H, Z_RD))
    k = k.union(box(RD_X0 + 1.0, RD_X0 + 2.5, yg0, yg1, Z_RD - G_H, Z_RD - G_H + 0.3))   # liten kul som holder leseren inne

# --- kortfeste: avstandsklosser med styretapper i H4, H3, H1, og to fjærende kroker ---
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk)
    k = k.union(cyl_z(hx, hy, 7.0, PCB_ZT, Z_FL - FLOOR))
    k = k.union(cyl_z(hx, hy, 3.4, PCB_ZT - 3.0, PCB_ZT))
    k = k.union(cq.Workplane('XY').add(cq.Solid.makeCone(1.2, 1.7, 0.6, cq.Vector(hx, hy, PCB_ZT - 3.6), cq.Vector(0, 0, 1))))
HOOK_T, NOSE = 1.2, 1.0
xa = PCB_X0 - 0.2 - HOOK_T                                        # krok A ved kanten mot inngangen, nese peker +x
k = k.union(box(xa, xa + HOOK_T, 20.0, 26.0, PCB_ZB - NOSE - 0.4, Z_FL - FLOOR))
k = k.union(prism_xz([(xa + HOOK_T, PCB_ZB - NOSE - 0.4), (xa + HOOK_T + 0.2 + NOSE, PCB_ZB), (xa + HOOK_T, PCB_ZB)], 20.0, 26.0))
xb = PCB_X0 + PCB_L + 0.3                                         # krok B ved kanten mot skilleveggen, nese peker −x
k = k.union(box(xb, xb + HOOK_T, 30.0, 36.0, PCB_ZB - NOSE - 0.4, Z_FL - FLOOR))
k = k.union(prism_xz([(xb, PCB_ZB - NOSE - 0.4), (xb - 0.3 - NOSE, PCB_ZB), (xb, PCB_ZB)], 30.0, 36.0))

# ======================= LOKK (skyves inn fra inngangen) =======================
lid = box(0, LID_X1, -LID_W2, LID_W2, LID_Z0, LID_Z0 + LID_T)
for s in (1, -1):                                                 # 45° kant under, hviler på kilen (0.1 klaring)
    lid = lid.cut(prism_yz([(s * (Y_IN - WEDGE_W + 0.9), LID_Z0), (s * (LID_W2 + 0.1), LID_Z0), (s * (LID_W2 + 0.1), LID_Z0 + 1.9)], -1, LID_X1 + 1))
TW = 7.0                                                          # klikk-tunge, 14 mm bred, fri i enden x=0
lid = lid.cut(box(-1, 22.0, TW, TW + 1.0, LID_Z0 - 1, LID_Z0 + LID_T + 1))
lid = lid.cut(box(-1, 22.0, -TW - 1.0, -TW, LID_Z0 - 1, LID_Z0 + LID_T + 1))
lid = lid.cut(box(-1, 22.0, -TW - 0.01, TW + 0.01, LID_Z0 - 1, LID_Z0 + 1.0))          # tungen tynnet til 2 mm
lid = lid.union(prism_xz([(2.7, LID_Z0 + 1.0), (2.7, 3.2), (3.5, 3.2), (5.3, LID_Z0 + 1.0)], -TW, TW))   # nese bak endeveggen
lid = lid.cut(cyl_z(13.0, 0.0, 7.0, LID_Z0 - 1, LID_Z0 + LID_T + 1))                    # fingerhull (og drenering)
for y in (-45.0, 0.0, 45.0):                                      # dreneringsslisser ved skilleveggen
    lid = lid.cut(box(74.0, 86.0, y - 0.75, y + 0.75, LID_Z0 - 1, LID_Z0 + LID_T + 1))

# ======================= HETTE: vegger + tak i ett (som v4.2) =======================
n = max(2, round((L - 2 * POST + 22) / 30)); gap = (L - 2 * POST - n * SLAT) / (n + 1)
v = box(0, L, 0, T, -GROOVE_D, OPEN_H)                           # lokalt: y fra innerflaten og ut, z fra gulvflaten
for i in range(n + 1):
    x0 = POST + i * (SLAT + gap)
    v = v.cut(box(x0, x0 + gap, -1, T + 1, RAIL_B, OPEN_H - RAIL_T))
v = v.union(box(0, L, 0, FOOT_W, 0, FOOT_T))                     # fot
v = v.union(prism_yz([(T, FOOT_T), (FOOT_W, FOOT_T), (T, FOOT_T + FOOT_W - T)], 0, L))   # 45° skråkant over foten
v = v.cut(cyl_y(BOB_X, AXLE_Z, 3.4, -1, T + 1))                    # aksel
for px in PRONG_X:                                                # klikk-tapper ned gjennom gulvet
    v = v.union(box(px - 6.0, px + 6.0, 0, 3.0, -FLOOR - 3.2, -GROOVE_D + 0.01))
    v = v.union(prism_yz([(3.0, -FLOOR - 3.2), (3.9, -FLOOR - 1.4), (3.9, -FLOOR), (3.0, -FLOOR)], px - 6.0, px + 6.0))
vegg_h = v.translate((0, LANE / 2, Z_FL))
vegg_v = vegg_h.mirror('XZ')
Y_OUT = LANE / 2 + T; Z_R = Z_FL + OPEN_H
tak = box(0, L, LANE / 2, Y_OUT, 0, T).union(box(0, L, -Y_OUT, -LANE / 2, 0, T))
for x in [0.0] + [POST + gap + i * (SLAT + gap) for i in range(n)] + [L - POST]:
    tak = tak.union(box(x, x + SLAT, -Y_OUT, Y_OUT, 0, T))
tak = tak.translate((0, 0, Z_R))
hette = vegg_h.union(vegg_v).union(tak)

# ======================= GAFLER (8-kant med nav) OG AKSEL =======================
BOB_LEN = (A_ABS[1] - (C_STOP[1] - BOB_BELOW) - ROD_IN * math.sin(BOB_TILT)) / math.cos(BOB_TILT)
def gaffel_lokal():
    """Akselen i origo langs Y, stangen ned langs −Z. Stangen er forskjøvet ROD_OFF mot +x (utover),
    så stangens +x-flate ligger flush med navets +x-flate: gaffelen ligger flatt på den siden."""
    rod = oct_z(ROD_OFF, 0, BOB_F, -BOB_LEN, 0)
    hub = oct_y(0, 0, HUB_F, -HUB_LEN / 2, HUB_LEN / 2)
    return rod.union(hub).cut(cyl_y(0, 0, 3.4, -HUB_LEN, HUB_LEN))
bobs = [gaffel_lokal().rotate((0, 0, 0), (0, 1, 0), -math.degrees(BOB_TILT)).translate((BOB_X, by, Z_FL + AXLE_Z)) for by in BOBS_Y]
axle = cyl_y(BOB_X, Z_FL + AXLE_Z, 3.0, -Y_OUT - 3, Y_OUT + 3)
coil_ref = box(CX - 50, CX + 50, -50, 50, Z_FL - FLOOR - 2, Z_FL - FLOOR).cut(box(CX - 48, CX + 48, -48, 48, 0, 40))
pcb_ref = box(PCB_X0, PCB_X0 + PCB_L, PCB_Y0, PCB_Y0 + PCB_W, PCB_ZB, PCB_ZT)
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk); pcb_ref = pcb_ref.cut(cyl_z(hx, hy, 3.7, PCB_ZB - 1, PCB_ZT + 1))
reader_ref = box(M_END - 0.3 - RD_L, M_END - 0.3, RD_Y0, RD_Y1, Z_RD - 0.15 - RD_T, Z_RD - 0.15)

# ======================= KONTROLL =======================
deler = {'kar': k, 'lokk': lid, 'hette': hette}
for i, b in enumerate(bobs):
    deler[f'gaffel_{i+1}'] = b
for navn, wp in deler.items():
    so = wp.val(); bb = so.BoundingBox()
    print(f'{navn:13s} solider={len(wp.solids().vals())} gyldig={so.isValid()} vol={so.Volume()/1000:6.1f} cm3  '
          f'X {bb.xmin:6.1f}..{bb.xmax:6.1f} Y {bb.ymin:6.1f}..{bb.ymax:6.1f} Z {bb.zmin:6.1f}..{bb.zmax:6.1f}')
print(f'gaffel: stang {BOB_F} mm 8-kant, nav {HUB_F} mm × {HUB_LEN} mm, lengde aksel→ende {BOB_LEN:.1f} mm, skrå {math.degrees(BOB_TILT):.2f}°')
print('--- kollisjoner (mm3, skal være ~0) ---')
ref = {'pcb_ref': pcb_ref, 'reader_ref': reader_ref}
alle = {**deler, **ref}
for a, b in [('kar', 'hette'), ('kar', 'lokk'), ('kar', 'pcb_ref'), ('kar', 'reader_ref'), ('lokk', 'pcb_ref'), ('lokk', 'reader_ref'),
             ('hette', 'gaffel_1'), ('hette', 'gaffel_3'), ('hette', 'gaffel_5'), ('kar', 'gaffel_1'), ('kar', 'gaffel_3'), ('kar', 'gaffel_5'),
             ('gaffel_1', 'gaffel_2'), ('gaffel_2', 'gaffel_3')]:
    print(f'{a:13s} ∩ {b:13s}: {alle[a].val().intersect(alle[b].val()).Volume():8.2f}')
print(f'gaffel–kar minste avstand: {bobs[2].val().distance(k.val()):.2f} mm, nav–nav avstand: {bobs[0].val().distance(bobs[1].val()):.2f} mm')

# ======================= EKSPORT =======================
asm = cq.Assembly(name='sluse_v4_3')
farge = {'kar': (0.85, 0.85, 0.85), 'lokk': (0.6, 0.8, 0.6), 'hette': (0.72, 0.8, 0.9)}
for navn, wp in deler.items():
    asm.add(wp, name=navn, color=cq.Color(*farge.get(navn, (0.85, 0.65, 0.4))))
asm.add(axle, name='aksel_rustfri_ref', color=cq.Color(0.5, 0.5, 0.55))
asm.add(coil_ref, name='spole_referanse', color=cq.Color(0.9, 0.5, 0.1))
asm.add(pcb_ref, name='pcb_referanse', color=cq.Color(0.1, 0.5, 0.2))
asm.add(reader_ref, name='leser_referanse', color=cq.Color(0.2, 0.3, 0.8))
asm.save(os.path.join(OUT_STEP, 'sluse_v4.3_sammenstilling.step'))
for navn in ('kar', 'lokk', 'hette'):
    cq.exporters.export(deler[navn], os.path.join(OUT_STEP, f'sluse_v4.3_{navn}.step'))
cq.exporters.export(bobs[2], os.path.join(OUT_STEP, 'sluse_v4.3_gaffel.step'))

def to_bed(wp):
    bb = wp.val().BoundingBox(); return wp.translate((-bb.xmin, -bb.ymin, -bb.zmin))
def stl(wp, name):
    cq.exporters.export(wp, os.path.join(OUT_STL, name), tolerance=0.02, angularTolerance=0.1)
kar_p = to_bed(k.rotate((0, 0, 0), (1, 0, 0), 180))                      # gulvflaten ned
hette_p = to_bed(hette.rotate((0, 0, 0), (1, 0, 0), 180))                # taket ned, veggene opp
lokk_p = to_bed(lid.rotate((0, 0, 0), (1, 0, 0), 180))                   # oversiden ned, tungen og nesen opp
# gafler: ligger på den flate siden (+x-flaten ned), annenhver snudd så navene ikke ligger ved siden av hverandre
PITCH = 15.0
g = None
for i in range(len(bobs)):
    lay = gaffel_lokal().rotate((0, 0, 0), (0, 1, 0), 90)                # +x-flaten ned, stangen langs −x
    if i % 2: lay = lay.rotate((0, 0, 0), (0, 0, 1), 180)
    lay = to_bed(lay).translate((0, i * PITCH, 0))
    g = lay if g is None else g.union(lay)
gafler_p = to_bed(g)
print(f'gafler i printen: {len(gafler_p.solids().vals())} legemer (skal være 5)')
stl(kar_p, 'sluse_v4.3_kar.stl'); stl(hette_p, 'sluse_v4.3_hette.stl'); stl(lokk_p, 'sluse_v4.3_lokk.stl'); stl(gafler_p, 'sluse_v4.3_gafler.stl')
def bb(wp): b_ = wp.val().BoundingBox(); return b_.xlen, b_.ylen, b_.zlen
kx, ky, _ = bb(kar_p); hx, hy, hz = bb(hette_p)
p1 = [kar_p.val(), gafler_p.translate((0, ky + 8, 0)).val()]
lokk_rot = to_bed(lokk_p.rotate((0, 0, 0), (0, 0, 1), 90))
p2 = [hette_p.val(), lokk_rot.translate((0, hy + 8, 0)).val()]
for navn, parts in (('print1_kar_og_gafler', p1), ('print2_hette_og_lokk', p2)):
    comp = cq.Compound.makeCompound(parts); b_ = comp.BoundingBox()
    print(f'{navn}: {b_.xlen:.1f} x {b_.ylen:.1f} x {b_.zlen:.1f} mm  (A1-bed 256 x 256 x 256)')
    cq.exporters.export(cq.Workplane('XY').add(comp), os.path.join(OUT_STL, f'sluse_v4.3_{navn}.stl'), tolerance=0.02, angularTolerance=0.1)
print('eksport ferdig')

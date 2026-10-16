#!/usr/bin/env python3
"""Duesluse v6 – Stigs ett-stykks sluse («nyeste antenne løsning») med forgang, el-rom under gulvet og spole i lomme.

Ett stykke, printet stående (gulvet er 32 mm over brettet, veggene 165 mm over gulvet):
- Gulvplate 212 × 128 mm. Forgang x 0..88 med el-rom under, skillevegg 88..90.4, kar 90.4..212 med
  spolelommen under gulvet (v5-prinsippet: 6 mm dyp, fire fjærende felt med klikk-nese). Gulvet er flatt hele veien.
- Fire ribber over forgangen (x 0, 21, 42, 63), hver en 4 mm vegg med spiss døråpning innvendig og flat topp.
  En toppramme (bjelke langs hver langside, bundet av ribbe 1 og portalene) binder dem. 17 mm lysåpning mellom ribbene.
  Hvert mellomrom i veggene, mellom ribber og mellom spiler, har spiss topp med samme 38° som døråpningen.
- Portalvegg ved x 88..92.4 og utgangsportal ved 167.6..172, samme spisse døråpning: rette sider til 113 mm,
  topp i 158, vegghøyde 165. Buen er to rette linjer med 38° fra vannrett, så den printes uten støtte.
- Karets sidevegger x 94..166 har to spiler à 10 mm (17 mm åpning), bunnbånd 12 mm, toppbånd 12 mm.
- De siste 40 mm av gulvet (172..212) har ingen vegger. Spolen ligger under 107..209.
- Lokket (skuffen) skyves inn fra −y-siden, kortsiden først, 4 mm over brettet, mellom fire kiler og fire stoppere
  på endeveggen og skilleveggen. Tunge i kanten ved åpningen med nese som klikker opp bak veggkanten. Hakk på
  undersiden for negl/kniv. Ingen fingerhull. Lokket printes flatt ved siden av karet i samme print.
- Kortfeste som v5. Leserholder som v5, men 1,5 mm bredere og 0,2 mm høyere spor. Kabelslisser i skilleveggen.
- Støtte i printen: under hele gulvet (el-rom og spolelomme), trekkes ut nedenfra. Ingen andre steder.
- Ingen gafler i denne versjonen (venter).

Koordinater (montert): X langs løpet (0 = inngang, 212 = enden mot slaget), Y på tvers (0 = senter),
Z opp (0 = landingsbrettet, 32 = gulvflaten).
"""
import math, os
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STEP = os.path.join(HERE, '..', 'step', 'v6')
OUT_STL = os.path.join(HERE, '..', 'stl', 'v6')
os.makedirs(OUT_STEP, exist_ok=True); os.makedirs(OUT_STL, exist_ok=True)

# ---------------- hovedmål ----------------
L, W, H = 212.0, 128.0, 32.0               # gulvplate, plintens høyde
WALL, FLOOR = 2.4, 4.0                     # plintvegg, gulvtykkelse
T_SIDE, LANE = 6.0, 116.0                  # sidevegger over gulvet, løpets bredde
Z_FL = H
Y_IN = W / 2 - WALL                        # 61.6 = innsiden av plintveggene
M_END = 88.0; DIV_T = 2.4; A0 = M_END + DIV_T            # el-rom 2.4..88, skillevegg 88..90.4
WALL_H, ARCH_SIDE, ARCH_TOP = 165.0, 113.0, 158.0         # vegghøyde, rette sider, buetopp (over gulvet)
ARCH_HALF = LANE / 2                                       # 58 = døråpningens halvbredde
RIB_T, RIB_X = 4.0, (0.0, 21.0, 42.0, 63.0)               # ribber over forgangen, 17 mm lysåpning
PORTAL_X = ((88.0, 92.4), (167.6, 172.0))                  # portalvegger (inn i karet, ut mot slaget)
RIDGE_W, RIDGE_H = 16.0, 7.0                              # mønebjelke
STRINGER_H, BAND_B, BAND_T = 12.0, 12.0, 12.0             # hjørnebjelke, bunnbånd, toppbånd
SLAT, N_SLAT = 10.0, 2                                     # spiler i karets sidevegger
# spole
CX = 158.0
COIL = 100.0; CLR = 0.7; POCKET_D = 6.0; FRAME_T = 2.4
PK = COIL / 2 + CLR                        # 50.7
ZP0, ZP1 = Z_FL - FLOOR - POCKET_D, Z_FL - FLOOR     # 22 .. 28
# lokk
LID_Z0, LID_T, LID_CLR = 4.0, 3.0, 0.3
WEDGE_W, RAIL_W = 3.0, 2.0
LID_X0, LID_X1 = WALL + 0.3, M_END - 0.3   # 2.7 .. 87.7
LID_W2 = Y_IN - 0.3                        # 61.3
Z_RAIL = LID_Z0 + LID_T + LID_CLR          # 7.3
GUIDE_Y = ((-59.0, -44.0), (44.0, 59.0))   # kiler og stoppere, korte segmenter
TONGUE_X = (35.0, 55.0); TONGUE_LEN, TONGUE_T, SL = 20.0, 2.0, 0.6
NOSE_H = 2.0                               # nese oppå tungen, z 6..8, klikker bak veggkanten (7.3)
# LED
LED_X, LED_Z, LED_D = 20.0, 20.0, 5.2
# kort (PigeonPal-PCB, 60 × 53.1 i KiCad; 53.1 langs x og 60 langs y), som v5
PCB_X0, PCB_Y0, PCB_L, PCB_W, PCB_T = 6.0, -18.0, 53.1, 60.0, 1.6
STANDOFF = 7.0
PCB_ZT = Z_FL - FLOOR - STANDOFF           # 21.0
PCB_ZB = PCB_ZT - PCB_T                    # 19.4
HOLES = ((72.771, 51.943), (72.771, 96.901), (124.0, 52.0))
def kicad(xk, yk):
    return PCB_X0 + (yk - 47.879), PCB_Y0 + (xk - 68.7345)
# leser (holder 1.5 mm bredere og 0.2 mm høyere enn v4.3/v5)
RD_L, RD_W, RD_T = 35.0, 15.0, 1.0
RD_Y0 = -Y_IN + 1.4; RD_Y1 = RD_Y0 + RD_W
Z_RD = Z_FL - FLOOR
G_H, LIP, RD_EXTRA = RD_T + 0.5, 1.0, 1.5

def box(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return cq.Workplane('XY').box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def cyl_z(x, y, d, z0, z1):
    return cq.Workplane('XY').circle(d / 2).extrude(z1 - z0).translate((x, y, z0))
def cyl_y(x, z, d, y0, y1):
    return cq.Workplane('XZ').circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))
def prism_yz(pts, x0, x1):
    return cq.Workplane('YZ').polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))
def prism_xz(pts, y0, y1):
    return cq.Workplane('XZ').polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))

# ======================= KAR (ett stykke) =======================
k = box(0, L, -W / 2, W / 2, 0, H)
k = k.cut(box(WALL, M_END, -Y_IN, Y_IN, -1, Z_FL - FLOOR))                 # el-rom, åpent nedover
k = k.cut(box(A0, L - WALL, -Y_IN, Y_IN, -1, Z_FL - FLOOR))                # under karet, åpent nedover
# lokkåpning i −y-plintveggen: åpen under z 7.3 langs el-rommet
k = k.cut(box(WALL, M_END, -W / 2 - 1, -Y_IN + 0.05, -1, Z_RAIL))
# lokkføring på endeveggen (x = 2.4) og skilleveggen (x = 88): kile under (45°) og stopper over (45°), 4 korte segmenter
for y0, y1 in GUIDE_Y:
    for xf, s in ((WALL, 1), (M_END, -1)):                               # s: retning inn i rommet
        k = k.union(prism_xz([(xf, 3.0), (xf, 3.0 + WEDGE_W), (xf + s * WEDGE_W, 3.0)], y0, y1))
        k = k.union(prism_xz([(xf + s * RAIL_W, Z_RAIL), (xf, Z_RAIL), (xf, Z_RAIL + RAIL_W)], y0, y1))
# spolelomme med ramme og fire klikk-neser (som v5)
frame = box(CX - PK - FRAME_T, CX + PK + FRAME_T, -PK - FRAME_T, PK + FRAME_T, ZP0, ZP1).cut(
    box(CX - PK, CX + PK, -PK, PK, ZP0 - 1, ZP1 + 1))
k = k.union(frame)
NOSE_IN, NOSE_TOP, NOSE_HH, RAMP_H = 1.2, Z_FL - FLOOR - 2.0, 1.2, 1.5
tabs = [('+x', CX + PK, 0.0), ('-x', CX - PK, 0.0), ('+y', CX, PK), ('-y', CX + 30.0, -PK)]
for side, a, b in tabs:
    if side in ('+x', '-x'):
        s = 1 if side == '+x' else -1
        xf = a
        for yy in (b - 9.5, b + 9.5):
            k = k.cut(box(min(xf, xf + s * FRAME_T) - 0.1, max(xf, xf + s * FRAME_T) + 0.1, yy - 0.5, yy + 0.5, ZP0 - 1, ZP1 - 1))
        prof = [(xf, NOSE_TOP - NOSE_HH - RAMP_H), (xf - s * NOSE_IN, NOSE_TOP - NOSE_HH), (xf - s * NOSE_IN, NOSE_TOP), (xf, NOSE_TOP)]
        k = k.union(prism_xz(prof, b - 8.5, b + 8.5))
    else:
        s = 1 if side == '+y' else -1
        yf = b
        for xx in (a - 9.5, a + 9.5):
            k = k.cut(box(xx - 0.5, xx + 0.5, min(yf, yf + s * FRAME_T) - 0.1, max(yf, yf + s * FRAME_T) + 0.1, ZP0 - 1, ZP1 - 1))
        prof = [(yf, NOSE_TOP - NOSE_HH - RAMP_H), (yf - s * NOSE_IN, NOSE_TOP - NOSE_HH), (yf - s * NOSE_IN, NOSE_TOP), (yf, NOSE_TOP)]
        k = k.union(prism_yz(prof, a - 8.5, a + 8.5))
k = k.cut(box(CX - PK + NOSE_IN, CX + PK - NOSE_IN, -PK + NOSE_IN, PK - NOSE_IN, ZP0 - 1, ZP1))
# utsparing for spolens avstemmingskort på −y-siden, nær skilleveggen
k = k.cut(box(CX - 49.0, CX - 9.0, -Y_IN - 1, -PK + 0.5, Z_FL - FLOOR - 8.0, Z_FL - FLOOR))
# kabler gjennom skilleveggen: 2 mm sprekk for spoletrådene (ved leserens ende) og 5 mm slisse for strømkabelen (Sika)
SLIT_Y = (RD_Y0 + 5.0, RD_Y0 + 7.0); PWR_Y = (-42.0, -37.0)
k = k.cut(box(M_END - 0.1, A0 + 0.1, SLIT_Y[0], SLIT_Y[1], -1, 20.0))
k = k.cut(box(M_END - 0.1, A0 + 0.1, PWR_Y[0], PWR_Y[1], -1, 18.0))
k = k.cut(box(92.0, 97.0, -W / 2 - 1, -Y_IN + 0.1, -1, 6.0))              # strømkabel under −y-veggen
# leserholder i hjørnet ved skilleveggen (−y), 1.5 mm bredere spor enn v5
RD_X0 = M_END - RD_L - 2.0
for (yv0, yv1, yg0, yg1) in ((-Y_IN, RD_Y0 + 1.2, RD_Y0 - 0.2 - RD_EXTRA / 2, RD_Y0 + 1.21),
                             (RD_Y1 - 1.2, RD_Y1 + 1.4 + RD_EXTRA / 2, RD_Y1 - 1.21, RD_Y1 + 0.2 + RD_EXTRA / 2)):
    k = k.union(box(RD_X0, M_END, yv0, yv1, Z_RD - G_H - LIP, Z_RD))
    k = k.cut(box(RD_X0 - 1, M_END - 0.5, yg0, yg1, Z_RD - G_H, Z_RD))
    k = k.union(box(RD_X0 + 1.0, RD_X0 + 2.5, yg0, yg1, Z_RD - G_H, Z_RD - G_H + 0.3))
# kortfeste (som v5)
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk)
    k = k.union(cyl_z(hx, hy, 7.0, PCB_ZT, Z_FL - FLOOR))
    k = k.union(cyl_z(hx, hy, 3.4, PCB_ZT - 3.0, PCB_ZT))
    k = k.union(cq.Workplane('XY').add(cq.Solid.makeCone(1.2, 1.7, 0.6, cq.Vector(hx, hy, PCB_ZT - 3.6), cq.Vector(0, 0, 1))))
HK_T, HK_NOSE = 1.2, 1.0
xa = PCB_X0 - 0.2 - HK_T
k = k.union(box(xa, xa + HK_T, 20.0, 26.0, PCB_ZB - HK_NOSE - 0.4, Z_FL - FLOOR))
k = k.union(prism_xz([(xa + HK_T, PCB_ZB - HK_NOSE - 0.4), (xa + HK_T + 0.2 + HK_NOSE, PCB_ZB), (xa + HK_T, PCB_ZB)], 20.0, 26.0))
xb = PCB_X0 + PCB_L + 0.3
k = k.union(box(xb, xb + HK_T, 30.0, 36.0, PCB_ZB - HK_NOSE - 0.4, Z_FL - FLOOR))
k = k.union(prism_xz([(xb, PCB_ZB - HK_NOSE - 0.4), (xb - 0.3 - HK_NOSE, PCB_ZB), (xb, PCB_ZB)], 30.0, 36.0))

# --- vegger over gulvet ---
DOOR = [(-ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_FL + ARCH_SIDE), (0.0, Z_FL + ARCH_TOP), (-ARCH_HALF, Z_FL + ARCH_SIDE)]
ARCH_DEG = math.degrees(math.atan2(ARCH_TOP - ARCH_SIDE, ARCH_HALF))
def portal(x0, x1):
    """Vegg tvers over løpet med spiss døråpning."""
    return box(x0, x1, -W / 2, W / 2, Z_FL, Z_FL + WALL_H).cut(prism_yz(DOOR, x0 - 1, x1 + 1))
for x0 in RIB_X:
    k = k.union(portal(x0, x0 + RIB_T))
for x0, x1 in PORTAL_X:
    k = k.union(portal(x0, x1))
# toppramme: bjelke langs hver langside over forgangen (karets toppbånd forlenget til inngangen). Ingen mønebjelke.
for s in (1, -1):
    k = k.union(box(0, PORTAL_X[0][1], s * (LANE / 2), s * (W / 2), Z_FL + WALL_H - STRINGER_H, Z_FL + WALL_H))
# karets sidevegger med spiler
KX0, KX1 = PORTAL_X[0][1], PORTAL_X[1][0]                                  # 92.4 .. 167.6
gap = (KX1 - KX0 - N_SLAT * SLAT) / (N_SLAT + 1)
Z_GAP_TOP = Z_FL + WALL_H - BAND_T                                         # 185 = underkant toppbånd
for s in (1, -1):
    wll = box(KX0, KX1, s * (LANE / 2), s * (W / 2), Z_FL, Z_FL + WALL_H)
    for i in range(N_SLAT + 1):
        g0 = KX0 + i * (SLAT + gap)
        wll = wll.cut(box(g0, g0 + gap, s * (LANE / 2 - 1), s * (W / 2 + 1), Z_FL + BAND_B, Z_GAP_TOP))
    k = k.union(wll)
# spiss topp i hvert mellomrom i veggene, samme vinkel som døråpningen: de to øvre hjørnene fylles med 38°
TAN = (ARCH_TOP - ARCH_SIDE) / ARCH_HALF
def spiss(x0, x1):
    xm, rise = (x0 + x1) / 2, (x1 - x0) / 2 * TAN
    for s in (1, -1):
        k_add = prism_xz([(x0 - 0.01, Z_GAP_TOP - rise), (x0 - 0.01, Z_GAP_TOP + 0.01), (xm, Z_GAP_TOP + 0.01)], s * (LANE / 2), s * (W / 2))
        k_add = k_add.union(prism_xz([(x1 + 0.01, Z_GAP_TOP - rise), (x1 + 0.01, Z_GAP_TOP + 0.01), (xm, Z_GAP_TOP + 0.01)], s * (LANE / 2), s * (W / 2)))
        yield k_add
GAPS = [(RIB_X[i] + RIB_T, RIB_X[i + 1]) for i in range(len(RIB_X) - 1)] + [(RIB_X[-1] + RIB_T, PORTAL_X[0][0])]
GAPS += [(KX0 + i * (SLAT + gap), KX0 + i * (SLAT + gap) + gap) for i in range(N_SLAT + 1)]
for x0, x1 in GAPS:
    for g in spiss(x0, x1):
        k = k.union(g)

# ======================= LOKK (skuffen, skyves inn fra −y) =======================
lid = box(LID_X0, LID_X1, -LID_W2, LID_W2, LID_Z0, LID_Z0 + LID_T)
# 45° kanter under langs x-kantene, hviler på kilene (0.1 klaring)
lid = lid.cut(prism_xz([(WALL + WEDGE_W - 0.9, LID_Z0), (LID_X0 - 0.1, LID_Z0), (LID_X0 - 0.1, LID_Z0 + 1.9)], -LID_W2 - 1, LID_W2 + 1))
lid = lid.cut(prism_xz([(M_END - WEDGE_W + 0.9, LID_Z0), (LID_X1 + 0.1, LID_Z0), (LID_X1 + 0.1, LID_Z0 + 1.9)], -LID_W2 - 1, LID_W2 + 1))
# tunge ved −y-kanten: to slisser langs y, rot innerst, tynnet ovenfra til 2 mm, nese oppå ytterst
tx0, tx1 = TONGUE_X
ty_root = -LID_W2 + TONGUE_LEN
for xx in (tx0, tx1):
    lid = lid.cut(box(xx - SL / 2, xx + SL / 2, -LID_W2 - 1, ty_root, LID_Z0 - 1, LID_Z0 + LID_T + 1))
lid = lid.cut(box(tx0, tx1, -LID_W2 - 1, ty_root + 0.01, LID_Z0 + TONGUE_T, LID_Z0 + LID_T + 1))
ZT = LID_Z0 + TONGUE_T                                                      # 6
lid = lid.union(prism_yz([(-LID_W2, ZT - 0.01), (-LID_W2, ZT + NOSE_H), (-LID_W2 + 1.5, ZT + NOSE_H), (-LID_W2 + 3.0, ZT - 0.01)], tx0 + 1.5, tx1 - 1.5))
# hakk på undersiden av tungen ytterst: negl eller kniv drar tungen ned
lid = lid.cut(box(tx0 + 6.0, tx1 - 6.0, -LID_W2 - 1, -LID_W2 + 1.5, LID_Z0 - 1, LID_Z0 + 1.2))
# dreneringsslisser ved skilleveggen
for y in (-40.0, 0.0, 40.0):
    lid = lid.cut(box(74.0, 86.0, y - 0.75, y + 0.75, LID_Z0 - 1, LID_Z0 + LID_T + 1))

# ======================= REFERANSER =======================
coil_ref = box(CX - 50, CX + 50, -50, 50, Z_FL - FLOOR - 2, Z_FL - FLOOR).cut(box(CX - 48, CX + 48, -48, 48, 0, 40))
pcb_ref = box(PCB_X0, PCB_X0 + PCB_L, PCB_Y0, PCB_Y0 + PCB_W, PCB_ZB, PCB_ZT)
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk); pcb_ref = pcb_ref.cut(cyl_z(hx, hy, 3.7, PCB_ZB - 1, PCB_ZT + 1))
reader_ref = box(M_END - 0.3 - RD_L, M_END - 0.3, RD_Y0, RD_Y1, Z_RD - 0.15 - RD_T, Z_RD - 0.15)

# ======================= KONTROLL =======================
deler = {'kar': k, 'lokk': lid}
for navn, wp in deler.items():
    so = wp.val(); bb = so.BoundingBox()
    print(f'{navn:6s} solider={len(wp.solids().vals())} gyldig={so.isValid()} vol={so.Volume()/1000:6.1f} cm3  '
          f'X {bb.xmin:6.1f}..{bb.xmax:6.1f} Y {bb.ymin:6.1f}..{bb.ymax:6.1f} Z {bb.zmin:6.1f}..{bb.zmax:6.1f}')
print(f'bue: rette sider til {ARCH_SIDE:.0f} mm, topp {ARCH_TOP:.0f} mm, vinkel {ARCH_DEG:.1f}° fra vannrett (overheng {90-ARCH_DEG:.1f}° fra loddrett)')
print(f'ribber: {len(RIB_X)} à {RIB_T} mm, lysåpning {RIB_X[1]-RIB_X[0]-RIB_T:.0f} mm; spiler i karet: {N_SLAT} à {SLAT} mm, lysåpning {gap:.1f} mm')
def strain(t, d, l): return 1.5 * t * d / l ** 2 * 100
print(f'tøyning lokktunge {strain(TONGUE_T, ZT + NOSE_H - Z_RAIL + 0.3, TONGUE_LEN):.2f} % (grense 2 %)')
print('--- kollisjoner (mm3, skal være ~0) ---')
alle = {**deler, 'pcb_ref': pcb_ref, 'reader_ref': reader_ref, 'coil_ref': coil_ref}
for a, b in [('kar', 'lokk'), ('kar', 'pcb_ref'), ('kar', 'reader_ref'), ('kar', 'coil_ref'), ('lokk', 'pcb_ref'), ('lokk', 'reader_ref')]:
    print(f'{a:6s} ∩ {b:10s}: {alle[a].val().intersect(alle[b].val()).Volume():8.2f}')

# ======================= EKSPORT =======================
asm = cq.Assembly(name='sluse_v6')
asm.add(k, name='kar', color=cq.Color(0.85, 0.85, 0.85))
asm.add(lid, name='lokk', color=cq.Color(0.6, 0.8, 0.6))
asm.add(coil_ref, name='spole_referanse', color=cq.Color(0.9, 0.5, 0.1))
asm.add(pcb_ref, name='pcb_referanse', color=cq.Color(0.1, 0.5, 0.2))
asm.add(reader_ref, name='leser_referanse', color=cq.Color(0.2, 0.3, 0.8))
asm.save(os.path.join(OUT_STEP, 'sluse_v6_sammenstilling.step'))
cq.exporters.export(k, os.path.join(OUT_STEP, 'sluse_v6_kar.step'))
cq.exporters.export(lid, os.path.join(OUT_STEP, 'sluse_v6_lokk.step'))

def to_bed(wp):
    bb = wp.val().BoundingBox(); return wp.translate((-bb.xmin, -bb.ymin, -bb.zmin))
def stl(wp, name):
    cq.exporters.export(wp, os.path.join(OUT_STL, name), tolerance=0.02, angularTolerance=0.1)
kar_p = to_bed(k)                                                           # stående, som montert
lokk_p = to_bed(lid)                                                        # flatt, undersiden ned, nesen opp
stl(kar_p, 'sluse_v6_kar.stl'); stl(lokk_p, 'sluse_v6_lokk.stl')
kb = kar_p.val().BoundingBox()
lokk_rot = to_bed(lokk_p.rotate((0, 0, 0), (0, 0, 1), 90))                  # kortsiden langs y, så printen blir 222 mm bred
comp = cq.Compound.makeCompound([kar_p.val(), lokk_rot.translate((0, kb.ylen + 8, 0)).val()])
b_ = comp.BoundingBox()
print(f'print (kar + lokk): {b_.xlen:.1f} x {b_.ylen:.1f} x {b_.zlen:.1f} mm  (A1-bed 256 x 256 x 256)')
cq.exporters.export(cq.Workplane('XY').add(comp), os.path.join(OUT_STL, 'sluse_v6_print_kar_og_lokk.stl'), tolerance=0.02, angularTolerance=0.1)
print('eksport ferdig')

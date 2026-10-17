#!/usr/bin/env python3
"""Duesluse v7.3 – som v7.2, men med én avstiver per side i stedet for kryss (Stig 17. okt: kryssene gjør modellen rotete).
Avstiveren som beholdes er den som er festet i foten av første stolpe (ved inngangen) og går på 45° opp mot slaget,
inn i toppramma ved siste takstol. Den andre (fra foten av siste stolpe) er tatt bort.

v7.2 – som v7.1, med fanggafler ved utgangen (Stigs forslag 17. okt):
- Siste takstol har rett gavl: døra er et rektangel 116 × 113, over den en overligger og en rett gavlplate 4 mm.
  Overliggeren stikker 4 mm ut mot slaget og er stopperen for gaflene (de kan bare svinge inn i slaget).
- Toppramma er forlenget forbi siste takstol som to ører. Mellom ørene ligger en tverrstang 6 × 8 mm
  (fasede hjørner, 3 mm flate) i flukt med toppen av hetta. Hetta printes på hodet, så stangen ligger på plata.
- Fem gafler (8-kant 6 mm, som v4.3) med nav på tverrstangen. Navet har nøkkelhull: en slisse like bred som stangen
  er tynn (6,3 mm). Gaffelen skyves på når den peker vannrett inn i slaget, og er låst så snart den henger.
  Navene fyller bredden mellom ørene, så gaflene holder avstanden selv. Printes flatt, fem i ett print.
- Plinten, skuffen og splintene er som v7.1.

Resten som v7 – v6 delt i to: plint og hette. Stolpene går rett ned i hull i plinten.

- Plint (bunnen): gulvplate 212 × 128 mm, 32 mm høy, el-rom under forgangen, skillevegg, spolelomme under karet,
  skuff fra −y-siden. Som v6, men med en kloss innenfor langsideveggen under hver stolpe
  (8 hull, 10,4 × 3,9 mm, 22 mm dype, 0,2 mm klaring, 0,5 mm skrå i kanten, 3 mm hull i bunnen).
  Printes med gulvet ned. Ingen støtte.
- Hette: fire like takstoler (ribber) med spiss døråpning, bein 10 × 5 mm helt til topps, gavl 4 mm, jevnt fordelt fra
  x 1.6 til 172, bundet av en toppramme 5 × 10 langs hver langside og én avstiver 4 × 4 mm på 45° per side
  (fra foten av første stolpe, gjennom mellomstolpene, inn i toppramma ved siste). Tappen er 10 × 3,5 mm og
  fortsetter 22 mm ned i hullet. Hetta er 126 mm bred, plinten 128, så plintkanten stikker 1 mm utenfor. Printes med
  toppramma ned, med brim. Ingen støtte.
- Feste: 4,2 mm vannrett hull gjennom plintvegg, kloss og stolpe ved første og siste takstol, begge sider.
  Printet splint (4 mm, to tunger med 0,4 mm mothake, printes flatt) eller M4 med mutter.
- Leseren er flyttet 8 mm inn fra −y-veggen (klossene ligger der den sto). Spolens −y-nese og vinduet for
  avstemmingskortet har byttet plass (nese ved x 128, vindu 176..208).
- Skuffen som v6.

Koordinater (montert): X langs løpet (0 = inngang, 212 = enden mot slaget), Y på tvers (0 = senter),
Z opp (0 = landingsbrettet, 32 = gulvflaten).
"""
import math, os
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STEP = os.path.join(HERE, '..', 'step', 'v7.3')
OUT_STL = os.path.join(HERE, '..', 'stl', 'v7.3')
os.makedirs(OUT_STEP, exist_ok=True); os.makedirs(OUT_STL, exist_ok=True)

# ---------------- hovedmål ----------------
L, W, H = 212.0, 128.0, 32.0               # gulvplate, plintens høyde
WALL, FLOOR = 2.4, 4.0                     # plintvegg, gulvtykkelse
LANE = 116.0                               # døråpningens bredde
Z_FL = H
Y_IN = W / 2 - WALL                        # 63.6 = innsiden av plintveggene
M_END = 88.0; DIV_T = 2.4; A0 = M_END + DIV_T            # el-rom 2.4..88, skillevegg 88..90.4
WALL_H, ARCH_SIDE, ARCH_TOP = 165.0, 113.0, 158.0         # vegghøyde, rette sider, buetopp (over gulvet)
ARCH_HALF = LANE / 2                                       # 58 = døråpningens halvbredde
LEG_W = 5.0; HETTE_HALF = ARCH_HALF + LEG_W                # beina er 5 mm brede, y 58..63; plintkanten stikker 1 mm utenfor
STRINGER_H = 10.0                                          # toppramme langs langsidene, 5 bred (som beinet) × 10 høy
# stolper / tapper / hull
N_POST, POST_T, GABLE_T = 4, 10.0, 4.0                     # takstoler, beinas tykkelse langs løpet, gavlens tykkelse
X_FIRST, X_LAST_END = 1.6, 172.0                           # første stolpe starter 1.6 (gods rundt hullet), siste slutter 172
POST_C = [X_FIRST + POST_T / 2 + i * (X_LAST_END - POST_T / 2 - X_FIRST - POST_T / 2) / (N_POST - 1) for i in range(N_POST)]
TEN_W, TEN_D = 3.5, 22.0
TEN_Y0, TEN_Y1 = ARCH_HALF + (LEG_W - TEN_W) / 2, ARCH_HALF + (LEG_W + TEN_W) / 2   # tapp y 58.75..62.25, 22 mm ned (z 10..32)
CLR, CHAMF = 0.2, 0.5
BOSS_Y0, BOSS_X = TEN_Y0 - CLR - 1.5, POST_T / 2 + CLR + 1.5        # kloss fra y 57.05 til veggen, 13.4 mm lang
BOSS_Z0_FORGANG = 8.5                                              # over skuffen og tungenesen (nese til z 8)
DRAIN_D = 3.0
PIN_D, PIN_Z, PIN_POSTS = 4.2, Z_FL - TEN_D / 2, (0, N_POST - 1)   # festehull ved første og siste takstol
BRACE, BRACE_Y = 4.0, (ARCH_HALF, ARCH_HALF + 4.0)                 # én avstiver 4 × 4 i veggplanet per side, 45°, y 58..62
BRACE_DIRS = (1,)                                                  # v7.2 hadde (1, -1) = kryss; 1 = fra foten av første stolpe opp mot slaget
# gafler ved utgangen (siste takstol): tverrstang i ører på toppramma, rett gavl med overligger som stopper
BAR_W, BAR_H, BAR_CH = 6.0, 8.0, 1.5                               # tverrstang 6 (x) × 8 (z), fas 1,5 → 3 mm flate mot plata
BAR_X = 178.5                                                      # stangens senter; hetta slutter ved X_LAST_END = 172
EAR_X1 = BAR_X + BAR_W / 2 + 4.0                                   # ørene (toppramma forlenget) slutter 4 mm etter stangen: 185.5
Z_BAR_TOP = Z_FL + WALL_H                                          # stangens overside i flukt med toppen av hetta (197)
Z_LINTEL0, LINTEL_T, LINTEL_X1 = Z_FL + ARCH_SIDE, 3.0, 173.0      # overligger fra z 145, 3 mm høy, stikker ut til x 173 (+4 mm)
N_BOB, BOB_PITCH, HUB_LEN = 5, 22.5, 22.0                          # fem gafler, 22,5 mm c/c, nav 22 mm (0,5 mm luft)
BOB_F = 6.0                                                        # gaffelstang 8-kant, 6 mm flate-til-flate
HUB_R = 6.5                                                        # navets halvbredde (flate), 13 mm nav
HUB_APEX = 8.5                                                     # navets spiss mot slaget (45° tak over hullet)
HUB_CH = 1.5                                                       # fas på navets to hjørner mot gavlen (føttene i printen)
BORE_CLR, SLOT_CLR = 0.3, 0.3                                      # klaring stang–hull og stang–slisse
BOB_TIP_Z = Z_FL + 3.0                                             # gaffelen slutter 3 mm over gulvet
# spole
CX = 158.0
COIL = 100.0; CLR_COIL = 0.7; POCKET_D = 6.0; FRAME_T = 2.4
PK = COIL / 2 + CLR_COIL                   # 50.7
ZP0, ZP1 = Z_FL - FLOOR - POCKET_D, Z_FL - FLOOR     # 22 .. 28
# lokk
LID_Z0, LID_T, LID_CLR = 4.0, 3.0, 0.3
WEDGE_W, RAIL_W = 3.0, 2.0
LID_X0, LID_X1 = WALL + 0.3, M_END - 0.3   # 2.7 .. 87.7
LID_W2 = Y_IN - 0.3                        # 63.3
Z_RAIL = LID_Z0 + LID_T + LID_CLR          # 7.3
GUIDE_Y = ((-59.0, -44.0), (44.0, 59.0))   # kiler og stoppere, korte segmenter
TONGUE_X = (35.0, 55.0); TONGUE_LEN, TONGUE_T, SL = 20.0, 2.0, 0.6
NOSE_H = 2.0
# kort (PigeonPal-PCB, 60 × 53.1 i KiCad; 53.1 langs x og 60 langs y), som v5
PCB_X0, PCB_Y0, PCB_L, PCB_W, PCB_T = 6.0, -18.0, 53.1, 60.0, 1.6
STANDOFF = 7.0
PCB_ZT = Z_FL - FLOOR - STANDOFF           # 21.0
PCB_ZB = PCB_ZT - PCB_T                    # 19.4
HOLES = ((72.771, 51.943), (72.771, 96.901), (124.0, 52.0))
def kicad(xk, yk):
    return PCB_X0 + (yk - 47.879), PCB_Y0 + (xk - 68.7345)
# leser: flyttet inn fra veggen så klossene får plass (v6: inntil veggen)
RD_L, RD_W, RD_T = 35.0, 15.0, 1.0
RD_Y0 = -52.0; RD_Y1 = RD_Y0 + RD_W        # −52 .. −37
Z_RD = Z_FL - FLOOR
G_H, LIP, RD_EXTRA = RD_T + 0.5, 1.0, 1.5

def box(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return cq.Workplane('XY').box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def cyl_z(x, y, d, z0, z1):
    return cq.Workplane('XY').circle(d / 2).extrude(z1 - z0).translate((x, y, z0))
def cyl_y(x, z, d, y0, y1):
    y0, y1 = sorted((y0, y1))
    return cq.Workplane('XZ').circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))
def prism_yz(pts, x0, x1):
    return cq.Workplane('YZ').polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))
def prism_xz(pts, y0, y1):
    return cq.Workplane('XZ').polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))
def prism_xy(pts, z0, z1):
    return cq.Workplane('XY').polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))

# ======================= PLINT =======================
p = box(0, L, -W / 2, W / 2, 0, H)
p = p.cut(box(WALL, M_END, -Y_IN, Y_IN, -1, Z_FL - FLOOR))                 # el-rom, åpent nedover
p = p.cut(box(A0, L - WALL, -Y_IN, Y_IN, -1, Z_FL - FLOOR))                # under karet, åpent nedover
# klosser under stolpene, innenfor langsideveggene
for c in POST_C:
    z0 = BOSS_Z0_FORGANG if c < A0 else 0.0
    for s in (1, -1):
        p = p.union(box(max(c - BOSS_X, 0.0), c + BOSS_X, s * BOSS_Y0, s * (W / 2 - 0.01), z0, Z_FL - FLOOR + 0.01))
# lokkåpning i −y-plintveggen: åpen under z 7.3 langs el-rommet
p = p.cut(box(WALL, M_END, -W / 2 - 1, -Y_IN + 0.05, -1, Z_RAIL))
# lokkføring på endeveggen (x = 2.4) og skilleveggen (x = 88): kile under (45°) og stopper over (45°)
for y0, y1 in GUIDE_Y:
    for xf, s in ((WALL, 1), (M_END, -1)):
        p = p.union(prism_xz([(xf, 3.0), (xf, 3.0 + WEDGE_W), (xf + s * WEDGE_W, 3.0)], y0, y1))
        p = p.union(prism_xz([(xf + s * RAIL_W, Z_RAIL), (xf, Z_RAIL), (xf, Z_RAIL + RAIL_W)], y0, y1))
# spolelomme med ramme og fire klikk-neser (som v6; −y-nesen flyttet til x 128)
frame = box(CX - PK - FRAME_T, CX + PK + FRAME_T, -PK - FRAME_T, PK + FRAME_T, ZP0, ZP1).cut(
    box(CX - PK, CX + PK, -PK, PK, ZP0 - 1, ZP1 + 1))
p = p.union(frame)
NOSE_IN, NOSE_TOP, NOSE_HH, RAMP_H = 1.2, Z_FL - FLOOR - 2.0, 1.2, 1.5
tabs = [('+x', CX + PK, 0.0), ('-x', CX - PK, 0.0), ('+y', CX, PK), ('-y', CX - 30.0, -PK)]
for side, a, b in tabs:
    if side in ('+x', '-x'):
        s = 1 if side == '+x' else -1
        xf = a
        for yy in (b - 9.5, b + 9.5):
            p = p.cut(box(min(xf, xf + s * FRAME_T) - 0.1, max(xf, xf + s * FRAME_T) + 0.1, yy - 0.5, yy + 0.5, ZP0 - 1, ZP1 - 1))
        prof = [(xf, NOSE_TOP - NOSE_HH - RAMP_H), (xf - s * NOSE_IN, NOSE_TOP - NOSE_HH), (xf - s * NOSE_IN, NOSE_TOP), (xf, NOSE_TOP)]
        p = p.union(prism_xz(prof, b - 8.5, b + 8.5))
    else:
        s = 1 if side == '+y' else -1
        yf = b
        for xx in (a - 9.5, a + 9.5):
            p = p.cut(box(xx - 0.5, xx + 0.5, min(yf, yf + s * FRAME_T) - 0.1, max(yf, yf + s * FRAME_T) + 0.1, ZP0 - 1, ZP1 - 1))
        prof = [(yf, NOSE_TOP - NOSE_HH - RAMP_H), (yf - s * NOSE_IN, NOSE_TOP - NOSE_HH), (yf - s * NOSE_IN, NOSE_TOP), (yf, NOSE_TOP)]
        p = p.union(prism_yz(prof, a - 8.5, a + 8.5))
p = p.cut(box(CX - PK + NOSE_IN, CX + PK - NOSE_IN, -PK + NOSE_IN, PK - NOSE_IN, ZP0 - 1, ZP1))
# vindu for spolens avstemmingskort på −y-siden, mot slaget (mellom siste kloss og endeveggen), innvendig: ytterveggen er hel
WIN_X = (176.0, 208.0)
p = p.cut(box(WIN_X[0], WIN_X[1], -Y_IN, -PK + 0.5, Z_FL - FLOOR - 8.0, Z_FL - FLOOR))
# kabler gjennom skilleveggen: 2 mm sprekk for spoletrådene (ved leseren) og 5 mm slisse for strømkabelen (Sika)
SLIT_Y = (RD_Y0 + 5.0, RD_Y0 + 7.0); PWR_Y = (-30.0, -25.0)
p = p.cut(box(M_END - 0.1, A0 + 0.1, SLIT_Y[0], SLIT_Y[1], -1, 20.0))
p = p.cut(box(M_END - 0.1, A0 + 0.1, PWR_Y[0], PWR_Y[1], -1, 18.0))
p = p.cut(box(92.0, 97.0, -W / 2 - 1, -Y_IN + 0.1, -1, 6.0))              # strømkabel under −y-veggen
# leserholder ved skilleveggen (−y), to frittstående skinner med spor
RD_X0 = M_END - RD_L - 2.0
for (yv0, yv1, yg0, yg1) in ((RD_Y0 - 2.2, RD_Y0 + 1.2, RD_Y0 - 0.2 - RD_EXTRA / 2, RD_Y0 + 1.21),
                             (RD_Y1 - 1.2, RD_Y1 + 1.4 + RD_EXTRA / 2, RD_Y1 - 1.21, RD_Y1 + 0.2 + RD_EXTRA / 2)):
    p = p.union(box(RD_X0, M_END, yv0, yv1, Z_RD - G_H - LIP, Z_RD))
    p = p.cut(box(RD_X0 - 1, M_END - 0.5, yg0, yg1, Z_RD - G_H, Z_RD))
    p = p.union(box(RD_X0 + 1.0, RD_X0 + 2.5, yg0, yg1, Z_RD - G_H, Z_RD - G_H + 0.3))
# kortfeste (som v6)
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk)
    p = p.union(cyl_z(hx, hy, 7.0, PCB_ZT, Z_FL - FLOOR))
    p = p.union(cyl_z(hx, hy, 3.4, PCB_ZT - 3.0, PCB_ZT))
    p = p.union(cq.Workplane('XY').add(cq.Solid.makeCone(1.2, 1.7, 0.6, cq.Vector(hx, hy, PCB_ZT - 3.6), cq.Vector(0, 0, 1))))
HK_T, HK_NOSE = 1.2, 1.0
xa = PCB_X0 - 0.2 - HK_T
p = p.union(box(xa, xa + HK_T, 20.0, 26.0, PCB_ZB - HK_NOSE - 0.4, Z_FL - FLOOR))
p = p.union(prism_xz([(xa + HK_T, PCB_ZB - HK_NOSE - 0.4), (xa + HK_T + 0.2 + HK_NOSE, PCB_ZB), (xa + HK_T, PCB_ZB)], 20.0, 26.0))
xb = PCB_X0 + PCB_L + 0.3
p = p.union(box(xb, xb + HK_T, 30.0, 36.0, PCB_ZB - HK_NOSE - 0.4, Z_FL - FLOOR))
p = p.union(prism_xz([(xb, PCB_ZB - HK_NOSE - 0.4), (xb - 0.3 - HK_NOSE, PCB_ZB), (xb, PCB_ZB)], 30.0, 36.0))
# stolpehull: 10.4 × 6.4, fra gulvflaten 22 mm ned, 0.5 mm skrå i kanten, 3 mm hull videre ned gjennom klossen
Z_HOLE0 = Z_FL - TEN_D                                                     # 10
for c in POST_C:
    for s in (1, -1):
        yc = s * (TEN_Y0 + TEN_Y1) / 2
        p = p.cut(box(c - POST_T / 2 - CLR, c + POST_T / 2 + CLR, s * (TEN_Y0 - CLR), s * (TEN_Y1 + CLR), Z_HOLE0, Z_FL + 1))
        flare = (cq.Workplane('XY').workplane(offset=Z_FL - CHAMF).center(c, yc).rect(POST_T + 2 * CLR, TEN_Y1 - TEN_Y0 + 2 * CLR)
                 .workplane(offset=CHAMF + 0.01).rect(POST_T + 2 * CLR + 2 * CHAMF, TEN_Y1 - TEN_Y0 + 2 * CLR + 2 * CHAMF).loft())
        p = p.cut(flare)
        p = p.cut(cyl_z(c, yc, DRAIN_D, -1, Z_HOLE0 + 1))
# festehull, vannrett gjennom vegg og kloss
for i in PIN_POSTS:
    for s in (1, -1):
        p = p.cut(cyl_y(POST_C[i], PIN_Z, PIN_D, s * (W / 2 + 1), s * (BOSS_Y0 - 1)))

# festeører: to på hver kortside, ved hjørnene, flate mot brettet. Skruehull 10 mm fra plintkanten.
# Flens 6 mm over brettet, over den en kile på 45° tilbake til veggen, så øret printes uten støtte med gulvet ned.
# Ø4 hull for treskrue 3,5 mm, senk 90° (Ø8) i toppen av flensen, Ø8 boring opp gjennom kilen for skrutrekkeren.
EAR_OUT, EAR_W, EAR_T, EAR_HOLE_X = 17.0, 16.0, 6.0, 10.0
EAR_D, EAR_HEAD_D = 4.0, 8.0
EAR_Y = (W / 2 - EAR_W / 2, -(W / 2 - EAR_W / 2))                          # ørene flukter med langsidene
for xw, s in ((0.0, -1), (L, 1)):
    for yc in EAR_Y:
        prof = [(xw, 0.0), (xw + s * EAR_OUT, 0.0), (xw + s * EAR_OUT, EAR_T), (xw, EAR_T + EAR_OUT)]
        p = p.union(prism_xz(prof, yc - EAR_W / 2, yc + EAR_W / 2))
        hx = xw + s * EAR_HOLE_X
        p = p.cut(cyl_z(hx, yc, EAR_D, -1, EAR_T))
        p = p.cut(cq.Workplane('XY').add(cq.Solid.makeCone(EAR_D / 2, EAR_HEAD_D / 2, (EAR_HEAD_D - EAR_D) / 2,
                                                             cq.Vector(hx, yc, EAR_T - (EAR_HEAD_D - EAR_D) / 2), cq.Vector(0, 0, 1))))
        p = p.cut(cyl_z(hx, yc, EAR_HEAD_D, EAR_T, EAR_T + EAR_OUT + 1))

# ======================= HETTE =======================
DOOR = [(-ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_FL + ARCH_SIDE), (0.0, Z_FL + ARCH_TOP), (-ARCH_HALF, Z_FL + ARCH_SIDE)]
ARCH_DEG = math.degrees(math.atan2(ARCH_TOP - ARCH_SIDE, ARCH_HALF))
DOOR_RECT = [(-ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_FL - 1), (ARCH_HALF, Z_LINTEL0), (-ARCH_HALF, Z_LINTEL0)]
def rib(c, straight=False):
    """Takstol: bein 10 mm tykke helt opp til toppen, gavlen over døråpningen 4 mm tykk.
    Spiss døråpning, eller (siste takstol) rektangulær dør 116 × 113 med rett gavl og en overligger som stikker
    4 mm ut mot slaget: gaflene hviler mot den. Overliggeren har 45° skrå oppover på begge sider (printes på hodet)."""
    r = box(c - POST_T / 2, c + POST_T / 2, -HETTE_HALF, HETTE_HALF, Z_FL, Z_FL + WALL_H)
    for sx in (1, -1):                                                      # tynn gavlen mellom beina (|y| < 58)
        r = r.cut(box(c + sx * GABLE_T / 2, c + sx * (POST_T / 2 + 1), -ARCH_HALF, ARCH_HALF, Z_FL + ARCH_SIDE, Z_FL + WALL_H + 1))
    if not straight:
        return r.cut(prism_yz(DOOR, c - POST_T, c + POST_T))
    r = r.cut(prism_yz(DOOR_RECT, c - POST_T, c + POST_T))
    x0, x1, g0, g1 = c - POST_T / 2, LINTEL_X1, c - GABLE_T / 2, c + GABLE_T / 2
    z0, z1 = Z_LINTEL0, Z_LINTEL0 + LINTEL_T
    lintel = prism_xz([(x0, z0), (x1, z0), (x1, z1), (g1, z1 + (x1 - g1)), (g0, z1 + (g0 - x0)), (x0, z1)], -ARCH_HALF, ARCH_HALF)
    return r.union(lintel)
h = None
for i, c in enumerate(POST_C):
    r = rib(c, straight=(i == N_POST - 1))
    h = r if h is None else h.union(r)
for s in (1, -1):                                                           # toppramme langs hver langside, forlenget som ører forbi siste takstol
    h = h.union(box(X_FIRST, EAR_X1, s * ARCH_HALF, s * HETTE_HALF, Z_FL + WALL_H - STRINGER_H, Z_FL + WALL_H))
# tverrstang for gaflene: 6 × 8 med fasede hjørner, overside i flukt med toppen, mellom ørene (ligger på plata i printen)
bx0, bx1, bz0, bz1 = BAR_X - BAR_W / 2, BAR_X + BAR_W / 2, Z_BAR_TOP - BAR_H, Z_BAR_TOP
BAR_PROF = [(bx0 + BAR_CH, bz0), (bx1 - BAR_CH, bz0), (bx1, bz0 + BAR_CH), (bx1, bz1 - BAR_CH), (bx1 - BAR_CH, bz1),
            (bx0 + BAR_CH, bz1), (bx0, bz1 - BAR_CH), (bx0, bz0 + BAR_CH)]
h = h.union(prism_xz(BAR_PROF, -HETTE_HALF, HETTE_HALF))
# én avstiver per side på 45°: fra foten av første stolpe (inngangen), gjennom mellomstolpene, inn i toppramma ved siste takstol
tlen = (Z_FL + WALL_H - 5.0) - (Z_FL - 3.0)
A = (POST_C[0], Z_FL - 3.0)
n = (BRACE / 2 / math.sqrt(2), BRACE / 2 / math.sqrt(2))
for s in (1, -1):
    for d in BRACE_DIRS:                                                    # d = retning langs x
        a = (POST_C[0] if d == 1 else POST_C[-1], Z_FL - 3.0); b = (a[0] + d * tlen, a[1] + tlen)
        nn = (-d * n[0], n[1])
        bar = prism_xz([(a[0] + nn[0], a[1] + nn[1]), (b[0] + nn[0], b[1] + nn[1]), (b[0] - nn[0], b[1] - nn[1]), (a[0] - nn[0], a[1] - nn[1])],
                       s * BRACE_Y[0], s * BRACE_Y[1])
        h = h.union(bar.intersect(box(X_FIRST, X_LAST_END, -HETTE_HALF, HETTE_HALF, Z_FL, Z_FL + WALL_H)))
BRACE_DEG = 45.0

for c in POST_C:                                                            # tapper: de innerste 6 mm av beinet, 22 mm ned, skrå tupp
    for s in (1, -1):
        t = box(c - POST_T / 2, c + POST_T / 2, s * TEN_Y0, s * TEN_Y1, Z_HOLE0, Z_FL + 0.01).edges('<Z').chamfer(CHAMF)
        h = h.union(t)
for i in PIN_POSTS:                                                         # festehull gjennom stolpen
    for s in (1, -1):
        h = h.cut(cyl_y(POST_C[i], PIN_Z, PIN_D, s * (HETTE_HALF + 1), s * (BOSS_Y0 - 1)))

# ======================= SPLINT =======================
# 4 mm pinne med hode, slisset på langs: to tunger med 0.4 mm mothake som klikker bak klossen (9.5 mm inne).
# Modellert montert på −y-siden ved x = 0, z = 0 (akse langs +y, hodet utenfor veggen), flyttes/speiles til hullene.
PIN_LEN, HEAD_D, HEAD_T, SLOT, BARB = 14.0, 8.0, 2.0, 1.4, 0.3
Y_WALL = -W / 2                                                             # −66
def splint():
    s = cyl_y(0, 0, HEAD_D, Y_WALL - HEAD_T, Y_WALL).union(cyl_y(0, 0, PIN_D - CLR, Y_WALL, Y_WALL + PIN_LEN))
    tip = Y_WALL + PIN_LEN
    s = s.cut(prism_yz([(tip - 1.2, 2.0), (tip + 0.1, 0.8), (tip + 0.1, 3.0), (tip - 1.2, 3.0)], -3, 3))      # skrå tupp
    s = s.cut(prism_yz([(tip - 1.2, -2.0), (tip + 0.1, -0.8), (tip + 0.1, -3.0), (tip - 1.2, -3.0)], -3, 3))
    yb = -BOSS_Y0                                                           # klossens innside, 9.5 mm innenfor veggen
    for sx in (1, -1):
        bb = [(sx * 1.95, yb + 0.1), (sx * (2.0 + BARB), yb + 0.5), (sx * (2.0 + BARB), yb + 1.3), (sx * 1.95, yb + 2.6)]
        s = s.union(prism_xy(bb, -1.3, 1.3))
    s = s.cut(box(-SLOT / 2, SLOT / 2, Y_WALL - HEAD_T + 0.5, tip + 1, -5, 5))                   # slisse, rot i hodet
    s = s.cut(box(-5, 5, Y_WALL - HEAD_T - 1, tip + 1, -5, -1.5))                                # flate for printen
    return s
spl = splint()
splints = []
for i in PIN_POSTS:
    for s in (1, -1):
        base = spl if s == -1 else spl.mirror('XZ')
        splints.append(base.translate((POST_C[i], 0, PIN_Z)))

# ======================= GAFLER (nøkkelhull-nav på tverrstangen) =======================
# Lokalt: navets senter i origo, stangen (tverrstangen) langs y, gaffelstangen ned langs −z, slissen mot −x (gavlen),
# spissen mot +x (slaget). Hullet er en 8-kant med 45° tak (ingen flate over hullet i printen), inskrevet radius =
# tverrstangens hjørneradius + klaring, så stangen kan rotere fritt. Slissen er 6,3 mm bred: tverrstangen (6 mm tynn, 8 høy)
# går bare gjennom når gaffelen peker vannrett inn i slaget. Hengende er den låst. Printes liggende på −x-siden:
# navets to føtter ved slissen og gaffelstangens flate ligger på plata, taket over hullet er 45°.
BAR_CORNER_R = max(math.hypot(BAR_W / 2 - BAR_CH, BAR_H / 2), math.hypot(BAR_W / 2, BAR_H / 2 - BAR_CH))   # 4.27
BORE_A = BAR_CORNER_R + BORE_CLR                                           # inskrevet radius i hullet: 4.57
_k = BORE_A * math.tan(math.radians(22.5))                                 # halve flaten i 8-kanten: 1.89
BORE_PROF = [(-BORE_A, -_k), (-_k, -BORE_A), (_k, -BORE_A), (BORE_A * math.sqrt(2), 0.0), (_k, BORE_A), (-_k, BORE_A), (-BORE_A, _k)]
HUB_PROF = [(-HUB_R, -(HUB_R - HUB_CH)), (-(HUB_R - HUB_CH), -HUB_R), (HUB_APEX - HUB_R, -HUB_R), (HUB_APEX, 0.0),
            (HUB_APEX - HUB_R, HUB_R), (-(HUB_R - HUB_CH), HUB_R), (-HUB_R, HUB_R - HUB_CH)]
SLOT_HW = (BAR_W + SLOT_CLR) / 2                                           # 3.15
Z_HUB = Z_BAR_TOP - BORE_A + 0.05                                          # navet henger med hullets overflate på stangens overside (0,05 luft i modellen)
ROD_X = -(HUB_R - BOB_F / 2)                                               # gaffelstangens senter: flaten i flukt med navets føtter
ROD_LEN = Z_HUB - BOB_TIP_Z                                                # fra navsenter til tupp
def gaffel_lokal():
    hub = prism_xz(HUB_PROF, -HUB_LEN / 2, HUB_LEN / 2)
    hub = hub.cut(prism_xz(BORE_PROF, -HUB_LEN / 2 - 1, HUB_LEN / 2 + 1))
    hub = hub.cut(box(-HUB_R - 1, -3.0, -HUB_LEN / 2 - 1, HUB_LEN / 2 + 1, -SLOT_HW, SLOT_HW))        # slissen mot −x
    rod = cq.Workplane('XY').polygon(8, BOB_F / math.cos(math.radians(22.5))).extrude(ROD_LEN - (HUB_R - HUB_CH))
    rod = rod.rotate((0, 0, 0), (0, 0, 1), 22.5).translate((ROD_X, 0, -ROD_LEN))                     # flater mot ±x, ±y
    rod = rod.edges('<Z').chamfer(1.0)
    return hub.union(rod)
gaffel = gaffel_lokal()
_rb = gaffel.val().BoundingBox()
assert abs((_rb.ymax - _rb.ymin) - HUB_LEN) < 0.01, 'navlengde'
# rotasjonsretning om y: finn fortegnet som fører tuppen mot +x (inn i slaget)
_probe = box(-0.5, 0.5, -0.5, 0.5, -10.5, -9.5).rotate((0, 0, 0), (0, 1, 0), 10).val().Center().x
ROT_SIGN = 1.0 if _probe > 0 else -1.0
# hvilevinkel: gaffelen lener seg mot overliggerens ytre overkant (LINTEL_X1, Z_LINTEL0 + LINTEL_T) av egen tyngde
_dz = (Z_LINTEL0 + LINTEL_T) - Z_HUB
def _f(phi): return -HUB_R * math.cos(phi) - _dz * math.sin(phi) - (LINTEL_X1 - BAR_X)
lo, hi = 0.0, math.radians(10)
for _ in range(60):
    mid = (lo + hi) / 2
    if _f(lo) * _f(mid) <= 0: hi = mid
    else: lo = mid
LEAN = (lo + hi) / 2                                                       # rad
LEAN_DEG = math.degrees(LEAN)
BOBS_Y = [(-(N_BOB - 1) / 2 + i) * BOB_PITCH for i in range(N_BOB)]
bobs = [gaffel.rotate((0, 0, 0), (0, 1, 0), ROT_SIGN * (LEAN_DEG + 0.02)).translate((BAR_X, y, Z_HUB)) for y in BOBS_Y]

# ======================= LOKK (skuffen, skyves inn fra −y) =======================
lid = box(LID_X0, LID_X1, -LID_W2, LID_W2, LID_Z0, LID_Z0 + LID_T)
lid = lid.cut(prism_xz([(WALL + WEDGE_W - 0.9, LID_Z0), (LID_X0 - 0.1, LID_Z0), (LID_X0 - 0.1, LID_Z0 + 1.9)], -LID_W2 - 1, LID_W2 + 1))
lid = lid.cut(prism_xz([(M_END - WEDGE_W + 0.9, LID_Z0), (LID_X1 + 0.1, LID_Z0), (LID_X1 + 0.1, LID_Z0 + 1.9)], -LID_W2 - 1, LID_W2 + 1))
tx0, tx1 = TONGUE_X
ty_root = -LID_W2 + TONGUE_LEN
for xx in (tx0, tx1):
    lid = lid.cut(box(xx - SL / 2, xx + SL / 2, -LID_W2 - 1, ty_root, LID_Z0 - 1, LID_Z0 + LID_T + 1))
lid = lid.cut(box(tx0, tx1, -LID_W2 - 1, ty_root + 0.01, LID_Z0 + TONGUE_T, LID_Z0 + LID_T + 1))
ZT = LID_Z0 + TONGUE_T
lid = lid.union(prism_yz([(-LID_W2, ZT - 0.01), (-LID_W2, ZT + NOSE_H), (-LID_W2 + 1.5, ZT + NOSE_H), (-LID_W2 + 3.0, ZT - 0.01)], tx0 + 1.5, tx1 - 1.5))
lid = lid.cut(box(tx0 + 6.0, tx1 - 6.0, -LID_W2 - 1, -LID_W2 + 1.5, LID_Z0 - 1, LID_Z0 + 1.2))
for y in (-40.0, 0.0, 40.0):
    lid = lid.cut(box(74.0, 86.0, y - 0.75, y + 0.75, LID_Z0 - 1, LID_Z0 + LID_T + 1))

# ======================= REFERANSER =======================
coil_ref = box(CX - 50, CX + 50, -50, 50, Z_FL - FLOOR - 2, Z_FL - FLOOR).cut(box(CX - 48, CX + 48, -48, 48, 0, 40))
pcb_ref = box(PCB_X0, PCB_X0 + PCB_L, PCB_Y0, PCB_Y0 + PCB_W, PCB_ZB, PCB_ZT)
for xk, yk in HOLES:
    hx, hy = kicad(xk, yk); pcb_ref = pcb_ref.cut(cyl_z(hx, hy, 3.7, PCB_ZB - 1, PCB_ZT + 1))
reader_ref = box(M_END - 0.3 - RD_L, M_END - 0.3, RD_Y0, RD_Y1, Z_RD - 0.15 - RD_T, Z_RD - 0.15)

# ======================= KONTROLL =======================
deler = {'plint': p, 'hette': h, 'lokk': lid, 'splint': splints[0], 'gaffel': bobs[N_BOB // 2]}
for navn, wp in deler.items():
    so = wp.val(); bb = so.BoundingBox()
    print(f'{navn:6s} solider={len(wp.solids().vals())} gyldig={so.isValid()} vol={so.Volume()/1000:6.1f} cm3  '
          f'X {bb.xmin:6.1f}..{bb.xmax:6.1f} Y {bb.ymin:6.1f}..{bb.ymax:6.1f} Z {bb.zmin:6.1f}..{bb.zmax:6.1f}')
print(f'bue: rette sider til {ARCH_SIDE:.0f} mm, topp {ARCH_TOP:.0f} mm, vinkel {ARCH_DEG:.1f} grader fra vannrett; '
      f'siste takstol: rett gavl, dor {LANE:.0f} x {ARCH_SIDE:.0f}, overligger {LINTEL_T:.0f} mm hoy til x {LINTEL_X1:.0f}')
print(f'tverrstang: {BAR_W:.0f} x {BAR_H:.0f} mm, fas {BAR_CH}, flate {BAR_W - 2 * BAR_CH:.0f} mm mot plata, senter x {BAR_X}, z {Z_BAR_TOP - BAR_H / 2:.0f}; '
      f'orer til x {EAR_X1}; hjorneradius {BAR_CORNER_R:.2f}')
print(f'gaffel: {N_BOB} stk, {BOB_PITCH} mm c/c, nav {HUB_LEN} x {2 * HUB_R:.0f} mm (spiss {HUB_APEX}), hull inskrevet r {BORE_A:.2f} '
      f'(klaring {BORE_CLR}), slisse {2 * SLOT_HW:.1f} mm, stang 8-kant {BOB_F:.0f} mm, navsenter til tupp {ROD_LEN:.1f} mm, '
      f'tupp {BOB_TIP_Z - Z_FL:.0f} mm over gulvet, hviler {LEAN_DEG:.2f} grader inn i slaget mot overliggeren')
_hub_sweep = math.hypot(HUB_R, HUB_R - HUB_CH)
print(f'nav mot gavl: {BAR_X - HUB_R - (POST_C[-1] + GABLE_T / 2):.1f} mm i ro, {BAR_X - _hub_sweep - (POST_C[-1] + GABLE_T / 2):.1f} mm naar gaffelen svinger; '
      f'ytterste nav til oret: {ARCH_HALF - (BOBS_Y[-1] + HUB_LEN / 2):.2f} mm')
print(f'takstoler: {N_POST} a {POST_T} mm ved x = ' + ', '.join(f'{c:.1f}' for c in POST_C) +
      f'; lysapning {POST_C[1]-POST_C[0]-POST_T:.1f} mm; bein {POST_T:.0f} x {LEG_W:.0f} mm, gavl {GABLE_T:.0f} mm, tapp {POST_T:.0f} x {TEN_W} x {TEN_D:.0f} mm, klaring {CLR} mm')
print(f'avstiver: {len(BRACE_DIRS)} per side, {BRACE:.0f} x {BRACE:.0f} mm, {BRACE_DEG:.0f} grader fra foten av foerste stolpe (x {A[0]:.1f}, z {A[1]:.0f}), '
      f'krysser stolpene ved z = ' + ', '.join(f'{A[1] + (c - A[0]):.0f}' for c in POST_C[1:]) + f', inn i toppramma ved x {A[0] + tlen:.1f}')
def strain(t, d, l): return 1.5 * t * d / l ** 2 * 100
print(f'toyning lokktunge {strain(TONGUE_T, ZT + NOSE_H - Z_RAIL + 0.3, TONGUE_LEN):.2f} %, '
      f'splinttunge {strain((PIN_D - CLR - SLOT) / 2, BARB, W / 2 - BOSS_Y0 + HEAD_T - 0.5):.2f} % (grense 1 %)')
print('--- kollisjoner (mm3, skal vaere ~0) ---')
alle = {**deler, 'pcb_ref': pcb_ref, 'reader_ref': reader_ref, 'coil_ref': coil_ref}
for a, b in [('plint', 'hette'), ('plint', 'lokk'), ('plint', 'pcb_ref'), ('plint', 'reader_ref'), ('plint', 'coil_ref'),
             ('hette', 'lokk'), ('lokk', 'pcb_ref'), ('lokk', 'reader_ref'), ('splint', 'plint'), ('splint', 'hette'),
             ('gaffel', 'hette'), ('gaffel', 'plint'), ('gaffel', 'coil_ref')]:
    print(f'{a:6s} x {b:10s}: {alle[a].val().intersect(alle[b].val()).Volume():8.2f}')
for i in range(N_BOB):
    v = bobs[i].val().intersect(h.val()).Volume()
    vv = bobs[i].val().intersect(bobs[i + 1].val()).Volume() if i + 1 < N_BOB else 0.0
    print(f'gaffel {i+1} x hette: {v:6.2f}   gaffel {i+1} x gaffel {i+2 if i + 1 < N_BOB else "-"}: {vv:6.2f}')
print(f'gaffel-overligger minste avstand: {bobs[2].val().distance(h.val()):.2f} mm, nav-nav: {bobs[0].val().distance(bobs[1].val()):.2f} mm, '
      f'gaffel-gulv: {bobs[2].val().distance(p.val()):.2f} mm')

# ======================= EKSPORT =======================
asm = cq.Assembly(name='sluse_v7.3')
asm.add(p, name='plint', color=cq.Color(0.85, 0.85, 0.85))
asm.add(h, name='hette', color=cq.Color(0.75, 0.78, 0.9))
asm.add(lid, name='lokk', color=cq.Color(0.6, 0.8, 0.6))
for i, sp in enumerate(splints):
    asm.add(sp, name=f'splint_{i+1}', color=cq.Color(0.9, 0.6, 0.2))
for i, b in enumerate(bobs):
    asm.add(b, name=f'gaffel_{i+1}', color=cq.Color(0.85, 0.65, 0.4))
asm.add(coil_ref, name='spole_referanse', color=cq.Color(0.9, 0.5, 0.1))
asm.add(pcb_ref, name='pcb_referanse', color=cq.Color(0.1, 0.5, 0.2))
asm.add(reader_ref, name='leser_referanse', color=cq.Color(0.2, 0.3, 0.8))
asm.save(os.path.join(OUT_STEP, 'sluse_v7.3_sammenstilling.step'))
for navn, wp in deler.items():
    cq.exporters.export(wp, os.path.join(OUT_STEP, f'sluse_v7.3_{navn}.step'))

def to_bed(wp):
    bb = wp.val().BoundingBox(); return wp.translate((-bb.xmin, -bb.ymin, -bb.zmin))
def stl(wp, name):
    cq.exporters.export(wp, os.path.join(OUT_STL, name), tolerance=0.02, angularTolerance=0.1)
flip = lambda wp: wp.rotate((0, 0, 0), (1, 0, 0), 180)
plint_p = to_bed(flip(p))                                                   # gulvet ned
hette_p = to_bed(flip(h))                                                   # toppramma ned
lokk_p = to_bed(lid)                                                        # flatt, undersiden ned
splint_p = to_bed(splints[0].rotate((0, 0, 0), (0, 0, 1), 90))              # flatt, flaten ned, slissen staaende
stl(plint_p, 'sluse_v7.3_plint.stl'); stl(hette_p, 'sluse_v7.3_hette.stl'); stl(lokk_p, 'sluse_v7.3_lokk.stl'); stl(splint_p, 'sluse_v7.3_splint.stl')
# print 1: plint + lokk + 4 splinter
pb = plint_p.val().BoundingBox()
lokk_rot = to_bed(lokk_p.rotate((0, 0, 0), (0, 0, 1), 90)).translate((0, pb.ylen + 8, 0))
lb = lokk_rot.val().BoundingBox()
items = [plint_p.val(), lokk_rot.val()]
for i in range(4):
    items.append(splint_p.translate((lb.xmax + 8 + i * 12, pb.ylen + 8, 0)).val())
comp = cq.Compound.makeCompound(items)
b_ = comp.BoundingBox()
print(f'print 1 (plint + lokk + 4 splinter): {b_.xlen:.1f} x {b_.ylen:.1f} x {b_.zlen:.1f} mm  (A1-bed 256 x 256 x 256)')
cq.exporters.export(cq.Workplane('XY').add(comp), os.path.join(OUT_STL, 'sluse_v7.3_print1_plint_lokk_splinter.stl'), tolerance=0.02, angularTolerance=0.1)
hb = hette_p.val().BoundingBox()
print(f'print 2 (hette, toppramma ned): {hb.xlen:.1f} x {hb.ylen:.1f} x {hb.zlen:.1f} mm')
# print 3: fem gafler liggende paa -x-siden (navets fotter og stangens flate ned, taket over hullet opp)
gaffel_flat = None
for ang in (90, -90):
    g = gaffel.rotate((0, 0, 0), (0, 1, 0), ang)
    gb = g.val().BoundingBox()
    if abs(gb.zmin + HUB_R) < 0.01:                                         # fottene nederst, ikke spissen
        gaffel_flat = to_bed(g); break
assert gaffel_flat is not None, 'fant ikke printorientering for gaffelen'
stl(gaffel_flat, 'sluse_v7.3_gaffel.stl')
gfb = gaffel_flat.val().BoundingBox()
items3 = [gaffel_flat.translate((0, i * (gfb.ylen + 5.0), 0)).val() for i in range(N_BOB)]
comp3 = cq.Compound.makeCompound(items3)
b3 = comp3.BoundingBox()
print(f'print 3 ({N_BOB} gafler, flatt): {b3.xlen:.1f} x {b3.ylen:.1f} x {b3.zlen:.1f} mm, {len(comp3.Solids())} legemer')
cq.exporters.export(cq.Workplane('XY').add(comp3), os.path.join(OUT_STL, 'sluse_v7.3_print3_gafler.stl'), tolerance=0.02, angularTolerance=0.1)
print('eksport ferdig')

#!/usr/bin/env python3
"""
Magnetic field of a single square air-core loop (10 x 10 cm, z = 0 plane,
centred at origin, 1 A) computed with the closed-form Biot-Savart field of a
finite straight wire segment. Pure Python, no numpy.

Purpose: compare how a leg-ring (horizontal-axis) LF RFID transponder couples
to the coil when it passes 0.5-1 cm above the coil vs 5-10 cm above it.
"""
import math

MU0 = 4e-7 * math.pi
I = 1.0
SIDE = 0.10           # m
HALF = SIDE / 2.0

# ---------------------------------------------------------------- vector helpers
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def mul(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))

# ------------------------------------------------- closed-form finite segment field
def b_segment(P, a, b, cur=I):
    """B at point P from straight segment a->b carrying current cur (SI)."""
    L = sub(b, a)
    Lhat = mul(L, 1.0 / norm(L))
    ra = sub(P, a)
    rb = sub(P, b)
    d = sub(ra, mul(Lhat, dot(ra, Lhat)))   # perpendicular vector from wire to P
    dn = norm(d)
    if dn < 1e-9:
        return (0.0, 0.0, 0.0)              # on the wire line: field undefined/zero
    dhat = mul(d, 1.0 / dn)
    fac = MU0 * cur / (4.0 * math.pi * dn) * (dot(ra, Lhat) / norm(ra) - dot(rb, Lhat) / norm(rb))
    return mul(cross(Lhat, dhat), fac)

# Square loop corners, counter-clockwise seen from +z -> Bz positive on axis
CORNERS = [(-HALF, -HALF, 0.0), (HALF, -HALF, 0.0), (HALF, HALF, 0.0), (-HALF, HALF, 0.0)]

def b_loop(P):
    B = (0.0, 0.0, 0.0)
    for k in range(4):
        B = add(B, b_segment(P, CORNERS[k], CORNERS[(k + 1) % 4]))
    return B

# ------------------------------------------ discretised Biot-Savart (for verification)
def b_loop_discrete(P, n=200):
    B = (0.0, 0.0, 0.0)
    for k in range(4):
        a = CORNERS[k]; b = CORNERS[(k + 1) % 4]
        dl = mul(sub(b, a), 1.0 / n)
        for i in range(n):
            mid = add(a, mul(dl, i + 0.5))
            r = sub(P, mid)
            rn = norm(r)
            B = add(B, mul(cross(dl, r), MU0 * I / (4.0 * math.pi * rn ** 3)))
    return B

def uT(x): return x * 1e6

# ------------------------------------------------------------------ sanity checks
print("=" * 78)
print("SANITY CHECKS")
print("=" * 78)
Bc = b_loop((0, 0, 0))
Bc_theory = 2 * math.sqrt(2) * MU0 * I / (math.pi * SIDE)
print(f"Centre field closed-form : Bz = {uT(Bc[2]):.4f} uT")
print(f"Centre field theory      : Bz = {uT(Bc_theory):.4f} uT   (2*sqrt(2)*mu0*I/(pi*a))")
P = (0.03, 0.01, 0.04)
B1 = b_loop(P); B2 = b_loop_discrete(P, 200)
print(f"Off-axis point {P}: closed-form {tuple(round(uT(c),4) for c in B1)} uT, "
      f"discretised(200/side) {tuple(round(uT(c),4) for c in B2)} uT")
print()

# ------------------------------------------------------------------ (1) axis
print("=" * 78)
print("(1) FIELD ON AXIS (x=y=0), 10x10 cm square loop, 1 A   [uT]")
print("=" * 78)
print(f"{'z [cm]':>7} {'|B|':>9} {'Bz':>9} {'Bh':>9} {'Bz/Bz(0)':>9}")
axis_z = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
axis_bz = {}
for zc in axis_z:
    B = b_loop((0.0, 0.0, zc / 100.0))
    Bh = math.hypot(B[0], B[1])
    axis_bz[zc] = B[2]
    print(f"{zc:>7.1f} {uT(norm(B)):>9.3f} {uT(B[2]):>9.3f} {uT(Bh):>9.4f} {B[2]/Bc[2]:>9.3f}")
B_THR = abs(axis_bz[9])
print(f"\nCalibrated threshold: B_threshold = |Bz(0,0,9 cm)| = {uT(B_THR):.3f} uT "
      f"(bench: co-planar ring reads at ~9 cm on axis)")
print()

# ------------------------------------------------------ (2)/(3) walking paths
heights = [0.5, 1, 2, 3, 5, 7, 8, 10]
xs = [round(-9 + 0.5 * i, 1) for i in range(37)]   # -9 .. +9 cm
DX = 0.5   # cm step

def path_table(yoff_cm, label):
    print("=" * 78)
    print(f"{label}: walking path along x, y = {yoff_cm} cm   [uT]")
    print("=" * 78)
    results = {}
    for zc in heights:
        rows = []
        for xc in xs:
            B = b_loop((xc / 100.0, yoff_cm / 100.0, zc / 100.0))
            Bh = math.hypot(B[0], B[1])
            rows.append((xc, B[0], B[1], B[2], Bh, norm(B)))
        results[zc] = rows
    # Compact per-height listing (every 1 cm to keep it readable)
    for zc in heights:
        print(f"\n-- z = {zc} cm --")
        print(f"{'x[cm]':>6} {'|B|':>8} {'Bz':>8} {'Bx':>8} {'By':>8} {'Bh':>8}")
        for (xc, bx, by, bz, bh, bm) in results[zc]:
            if abs(xc * 2 - round(xc * 2)) < 1e-9 and abs(xc - round(xc)) < 1e-9:
                print(f"{xc:>6.1f} {uT(bm):>8.3f} {uT(bz):>8.3f} {uT(bx):>8.3f} {uT(by):>8.3f} {uT(bh):>8.3f}")
    return results

def summarise(results, label):
    print()
    print("=" * 78)
    print(f"TAG-COUPLING SUMMARY  ({label})")
    print("Cases: (a) tag axis vertical -> |Bz|; (b) axis along x (walking dir) -> |Bx|;")
    print("       (c) axis along y (across passage) -> |By|; (d) horizontal, random azimuth:")
    print("       best-case Bh, azimuth-average (2/pi)*Bh.")
    print(f"Threshold = {uT(B_THR):.3f} uT. 'Readable length' = path length where component >= threshold")
    print("(path is 18 cm long, -9..+9 cm; coil conductors at x = +/-5 cm).")
    print("=" * 78)
    hdr = (f"{'z':>4} | {'case':>7} | {'max[uT]':>8} {'at x[cm]':>9} {'margin':>7} {'read len[cm]':>12}")
    print(hdr)
    print("-" * len(hdr))
    summary = {}
    for zc in heights:
        rows = results[zc]
        cases = {
            'a |Bz|': [abs(r[3]) for r in rows],
            'b |Bx|': [abs(r[1]) for r in rows],
            'c |By|': [abs(r[2]) for r in rows],
            'd Bh':   [r[4] for r in rows],
            'd avg':  [2.0 / math.pi * r[4] for r in rows],
        }
        summary[zc] = {}
        for name, vals in cases.items():
            mx = max(vals)
            ix = [i for i, v in enumerate(vals) if abs(v - mx) < 1e-15]
            xpos = ",".join(f"{rows[i][0]:+.1f}" for i in ix)
            readable = sum(DX for v in vals if v >= B_THR)
            margin = mx / B_THR
            summary[zc][name] = (mx, xpos, margin, readable)
            print(f"{zc:>4} | {name:>7} | {uT(mx):>8.3f} {xpos:>9} {margin:>7.2f} {readable:>12.1f}")
        print("-" * len(hdr))
    return summary

res_c = path_table(0.0, "(2) CENTRED PATH")
sum_c = summarise(res_c, "centred path, y = 0")
res_o = path_table(2.5, "(3) OFFSET PATH")
sum_o = summarise(res_o, "offset path, y = 2.5 cm")

# ------------------------------------------------------------- comparison block
print()
print("=" * 78)
print("HEIGHT COMPARISON FOR A HORIZONTAL-AXIS TAG (leg ring), centred path")
print("=" * 78)
print(f"{'z[cm]':>6} {'max|Bx|':>9} {'max|By|':>9} {'maxBh':>8} {'margin Bh':>10} {'read len Bh':>12} {'read len avg':>13} {'|Bz| axis':>10} {'margin Bz':>10}")
for zc in heights:
    a = sum_c[zc]
    bz_axis = abs(b_loop((0, 0, zc / 100.0))[2])
    print(f"{zc:>6} {uT(a['b |Bx|'][0]):>9.3f} {uT(a['c |By|'][0]):>9.3f} {uT(a['d Bh'][0]):>8.3f} "
          f"{a['d Bh'][2]:>10.2f} {a['d Bh'][3]:>12.1f} {a['d avg'][3]:>13.1f} {uT(bz_axis):>10.3f} {bz_axis/B_THR:>10.2f}")

print()
print("Ratio of horizontal-tag margin, low vs raised coil (centred path, best-case Bh):")
for lo in (0.5, 1):
    for hi in (5, 7, 8, 10):
        print(f"  z={lo} cm vs z={hi} cm : {sum_c[lo]['d Bh'][2] / sum_c[hi]['d Bh'][2]:.1f}x")

# Field-direction picture: angle of B from vertical along path at a few heights
print()
print("Field tilt from vertical along the centred path (deg), 0 = purely vertical:")
print(f"{'x[cm]':>6}" + "".join(f"{'z='+str(z):>8}" for z in heights))
for xc in [0, 2, 3, 4, 4.5, 5, 5.5, 6, 7, 9]:
    line = f"{xc:>6.1f}"
    for zc in heights:
        B = b_loop((xc / 100.0, 0.0, zc / 100.0))
        ang = math.degrees(math.atan2(math.hypot(B[0], B[1]), abs(B[2])))
        line += f"{ang:>8.1f}"
    print(line)
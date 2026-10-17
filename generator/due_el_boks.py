#!/usr/bin/env python3
"""Tar duefiguren ut av Stigs el-boks i «nyeste antenne løsning» (stl/v5/nyeste antenne løsning i stl.stl) og lagrer den
som egen fil, uendret: samme omriss, samme tykkelse (0,4 mm relieff på boksens framside).

Figuren er en lukket strek (237 punkter) på framsida av el-boksen (x −91,0), hevet 0,4 mm til x −91,4,
ca. 28 × 30 mm, sammen med teksten PIGEONPAL. Bare fuglen tas med.

- step/v5/due_el_boks.step: fuglen der den står i Stigs modell (x −91,4..−91,0, y −25..3, z 90..120).
- stl/v5/due_el_boks.stl: fuglen flatt på plata, relieffsida opp, 29,6 × 28,3 × 0,4 mm, hjørnet i origo.
- tegninger/v5/due_el_boks.png
"""
import os
import numpy as np
import trimesh
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'stl', 'v5', 'nyeste antenne løsning i stl.stl')
OUT_STEP = os.path.join(HERE, '..', 'step', 'v5'); OUT_STL = os.path.join(HERE, '..', 'stl', 'v5'); OUT_PNG = os.path.join(HERE, '..', 'tegninger', 'v5')
X_BASE, X_TOP = -91.0, -91.4                                      # boksens framside og relieffets topp (relieffet stikker ut i −x)

m = trimesh.load(SRC, force='mesh')
boks = sorted(m.split(only_watertight=False), key=lambda q: -q.volume)[1]       # el-boksen er den minste av de to kroppene
nx, fx = boks.face_normals[:, 0], boks.triangles_center[:, 0]
topp = np.where((nx < -0.9) & (np.abs(fx - X_TOP) < 0.15))[0]                     # relieffets toppflater
grupper = trimesh.Trimesh(boks.vertices, boks.faces[topp], process=False).split(only_watertight=False)
fugl = [g for g in grupper if g.bounds[1, 1] < 8.0]                                 # bokstavene ligger ved y 12..18, fuglen ved y −25..3
assert len(fugl) == 1, len(fugl)
fugl = fugl[0]
loops = fugl.outline().discrete
assert len(loops) == 1 and np.allclose(loops[0][0], loops[0][-1]), [len(l) for l in loops]
pts = loops[0][:-1]                                                                  # lukket omriss, siste punkt = første
print(f'omriss: {len(pts)} punkter, y {pts[:, 1].min():.1f}..{pts[:, 1].max():.1f}, z {pts[:, 2].min():.1f}..{pts[:, 2].max():.1f}, '
      f'areal {fugl.area:.1f} mm2, tykkelse {abs(X_TOP - X_BASE):.1f} mm')

wire = cq.Wire.makePolygon([cq.Vector(X_BASE, y, z) for _, y, z in pts], close=True)
due = cq.Solid.extrudeLinear(cq.Face.makeFromWires(wire), cq.Vector(X_TOP - X_BASE, 0, 0))
assert due.isValid()
print(f'due: gyldig, volum {due.Volume():.2f} mm3, boks ' + ' '.join(f'{a}: {getattr(due.BoundingBox(), a + "min"):.1f}..{getattr(due.BoundingBox(), a + "max"):.1f}' for a in 'xyz'))

for d in (OUT_STEP, OUT_STL, OUT_PNG): os.makedirs(d, exist_ok=True)
cq.exporters.export(cq.Workplane('XY').add(due), os.path.join(OUT_STEP, 'due_el_boks.step'))
# flatt paa plata: framsida (x −91,4) opp, boksens flate ned paa z 0. Rotasjon om y: −x → +z
flat = due.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90).translate((0, 0, 0))
bb = flat.BoundingBox(); flat = flat.translate((-bb.xmin, -bb.ymin, -bb.zmin))
bb = flat.BoundingBox()
cq.exporters.export(cq.Workplane('XY').add(flat), os.path.join(OUT_STL, 'due_el_boks.stl'), tolerance=0.01, angularTolerance=0.1)
print(f'stl flatt: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm')

fig, ax = plt.subplots(figsize=(7, 7), dpi=110)
ax.add_collection(PolyCollection(fugl.triangles[:, :, 1:3], facecolors='tab:orange', edgecolors='none'))
ax.plot(np.r_[pts[:, 1], pts[0, 1]], np.r_[pts[:, 2], pts[0, 2]], 'k-', lw=0.4)
ax.set_xlim(-30, 10); ax.set_ylim(85, 125); ax.set_aspect('equal'); ax.set_xlabel('y'); ax.set_ylabel('z')
ax.set_title('Duefiguren fra el-boksen, sett forfra (−x), 0,4 mm relieff', loc='left', fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(OUT_PNG, 'due_el_boks.png'), facecolor='white')
print('eksport ferdig')

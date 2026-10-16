#!/usr/bin/env python3
"""Lager PNG-bilder av v5-delene fra STEP-filene (cadquery → trimesh → matplotlib). Skrives til tegninger/v5/."""
import os, sys
import numpy as np
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, '..', 'step', 'v5')
OUT = os.path.join(HERE, '..', 'tegninger', 'v5')
os.makedirs(OUT, exist_ok=True)

def mesh_of(shape, tol=0.15):
    verts, tris = shape.tessellate(tol, 0.3)
    v = np.array([(p.x, p.y, p.z) for p in verts]); f = np.array(tris)
    return trimesh.Trimesh(v, f, process=False)

def load(name):
    return cq.importers.importStep(os.path.join(STEP, f'sluse_v5_{name}.step')).val()

parts = {n: mesh_of(load(n)) for n in ('kar', 'lokk', 'hette', 'gaffel')}
COL = {'kar': (0.82, 0.82, 0.80), 'lokk': (0.62, 0.80, 0.60), 'hette': (0.66, 0.75, 0.88), 'gaffel': (0.80, 0.62, 0.38)}
BOBS_Y = (-44.0, -22.0, 0.0, 22.0, 44.0)
LIGHT = np.array([0.4, -0.5, 0.75]); LIGHT /= np.linalg.norm(LIGHT)

def draw(ax, mesh, color, alpha=1.0):
    tri = mesh.vertices[mesh.faces]
    n = mesh.face_normals
    shade = 0.45 + 0.55 * np.clip(n @ LIGHT, 0, 1)
    cols = np.clip(np.array(color)[None, :] * shade[:, None], 0, 1)
    pc = Poly3DCollection(tri, facecolors=cols, edgecolors='none', alpha=alpha)
    ax.add_collection3d(pc)

def view(fname, title, items, elev, azim, lim=None, clip=None):
    fig = plt.figure(figsize=(13, 9), dpi=110)
    ax = fig.add_subplot(111, projection='3d')
    allv = []
    for name, mesh, tf in items:
        m = mesh.copy()
        if tf is not None: m.apply_transform(tf)
        if clip is not None:
            keep = np.all(clip(m.vertices[m.faces]), axis=1)
            m.update_faces(keep)
        draw(ax, m, COL[name]); allv.append(m.vertices)
    V = np.vstack(allv) if lim is None else np.array(lim)
    c = (V.min(0) + V.max(0)) / 2; r = (V.max(0) - V.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title(title, loc='left', fontsize=13, fontweight='bold')
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), facecolor='white'); plt.close(fig)
    print('skrev', fname)

def T(dx=0, dy=0, dz=0): m = np.eye(4); m[:3, 3] = (dx, dy, dz); return m
def flipx(): return trimesh.transformations.rotation_matrix(np.pi, (1, 0, 0))

gafler = [('gaffel', parts['gaffel'], T(0, y, 0)) for y in BOBS_Y]
# 1 montert
view('sluse_v5_montert.png', 'Duesluse v5 – montert', [('kar', parts['kar'], None), ('lokk', parts['lokk'], None), ('hette', parts['hette'], None)] + gafler, 28, -58)
# 2 inngangsenden: kroker, åpen endevegg, lokket
view('sluse_v5_inngang.png', 'Inngangsenden: L-krokene på utsiden av endeveggen, lokket i den åpne spalten', [('kar', parts['kar'], None), ('lokk', parts['lokk'], None), ('hette', parts['hette'], None)], 14, -150,
     lim=[(-30, -80, -5), (60, 80, 85)])
# 3 slagenden: flik med vindu og trykknapp
view('sluse_v5_slag_trykknapp.png', 'Slagenden: fliken med vindu og karets trykknapp (fjærbjelke i endeveggen)', [('kar', parts['kar'], None), ('hette', parts['hette'], None)], 12, 28,
     lim=[(150, -80, -5), (240, 80, 85)])
# 4 karet nedenfra med lokket inne
view('sluse_v5_kar_med_lokk.png', 'Karet sett nedenfra med skuffen inne: tunge med nese, fingerhull, 4 kiler/stoppere', [('kar', parts['kar'], flipx()), ('lokk', parts['lokk'], flipx())], 32, -120)
# 5 el-rommet uten lokk
view('sluse_v5_kammer.png', 'El-rommet nedenfra uten lokk: kloss for nesen, kiler, stoppere, kortfeste, leserholder', [('kar', parts['kar'], flipx())], 40, -115,
     lim=[(-5, -80, -35), (115, 80, 5)])
# 6 lokket
view('sluse_v5_lokk.png', 'Skuffen ovenfra: tungen bakerst med nese, fingerhull i tungen, dreneringsslisser', [('lokk', parts['lokk'], None)], 40, -110)
# 7 taket ovenfra
view('sluse_v5_tak.png', 'Taket ovenfra: ramme, flygende due, fjærlinjer', [('hette', parts['hette'], None)], 90, -90)
# 8 print 2: hette opp-ned
view('sluse_v5_print2.png', 'Print 2: hetta med taket ned, kroker og fliker øverst', [('hette', parts['hette'], flipx())], 22, -60)

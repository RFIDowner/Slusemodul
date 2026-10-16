#!/usr/bin/env python3
"""Lager PNG-bilder av v6 fra STEP-filene (cadquery → trimesh → matplotlib). Skrives til tegninger/v6/."""
import os
import numpy as np
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, '..', 'step', 'v6')
OUT = os.path.join(HERE, '..', 'tegninger', 'v6')
os.makedirs(OUT, exist_ok=True)

def mesh_of(shape, tol=0.15):
    verts, tris = shape.tessellate(tol, 0.3)
    m = trimesh.Trimesh(np.array([(p.x, p.y, p.z) for p in verts]), np.array(tris), process=False)
    return m.subdivide_to_size(max_edge=12.0)        # små trekanter gir riktig dybdesortering i matplotlib
def load(name):
    return cq.importers.importStep(os.path.join(STEP, f'sluse_v6_{name}.step')).val()

parts = {n: mesh_of(load(n)) for n in ('kar', 'lokk')}
COL = {'kar': (0.82, 0.82, 0.80), 'lokk': (0.62, 0.80, 0.60)}
LIGHT = np.array([0.4, -0.5, 0.75]); LIGHT /= np.linalg.norm(LIGHT)

def draw(ax, mesh, color):
    tri = mesh.vertices[mesh.faces]
    shade = 0.45 + 0.55 * np.clip(mesh.face_normals @ LIGHT, 0, 1)
    ax.add_collection3d(Poly3DCollection(tri, facecolors=np.clip(np.array(color)[None, :] * shade[:, None], 0, 1), edgecolors='none'))

def view(fname, title, items, elev, azim, lim=None, clip=None):
    fig = plt.figure(figsize=(13, 9), dpi=110)
    ax = fig.add_subplot(111, projection='3d')
    allv = []
    for name, mesh, tf in items:
        m = mesh.copy()
        if tf is not None: m.apply_transform(tf)
        if clip is not None:
            m.update_faces(np.all(clip(m.vertices[m.faces]), axis=1))
        draw(ax, m, COL[name]); allv.append(m.vertices)
    V = np.vstack(allv) if lim is None else np.array(lim)
    c = (V.min(0) + V.max(0)) / 2; r = (V.max(0) - V.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title(title, loc='left', fontsize=13, fontweight='bold')
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), facecolor='white'); plt.close(fig)
    print('skrev', fname)

def flipx(): return trimesh.transformations.rotation_matrix(np.pi, (1, 0, 0))
K, Lk = parts['kar'], parts['lokk']
view('sluse_v6_montert.png', 'Duesluse v6 – ett stykke, sett fra inngangen', [('kar', K, None), ('lokk', Lk, None)], 24, -125)
view('sluse_v6_fra_slaget.png', 'v6 sett fra slaget: utgangsportal og 40 mm gulv uten vegger', [('kar', K, None), ('lokk', Lk, None)], 24, 40)
view('sluse_v6_side.png', 'v6 fra −y: lokkåpningen under el-rommet, ribber og spiler med spiss topp', [('kar', K, None), ('lokk', Lk, None)], 6, -90)
view('sluse_v6_snitt.png', 'v6 snitt langs midten (y < 0 fjernet): el-rom, skillevegg, spolelomme, buer', [('kar', K, None), ('lokk', Lk, None)], 14, -70,
     clip=lambda v: v[:, :, 1] > 0)
view('sluse_v6_kar_med_lokk.png', 'v6 nedenfra med skuffen inne', [('kar', K, flipx()), ('lokk', Lk, flipx())], 35, -115)
view('sluse_v6_kammer.png', 'El-rommet nedenfra uten lokk: kiler, stoppere, kortfeste, leserholder', [('kar', K, flipx())], 40, -115,
     lim=[(-5, -70, -35), (100, 70, 5)])
view('sluse_v6_lokk.png', 'Skuffen ovenfra: tunge med nese ved −y-kanten, hakk under, dreneringsslisser', [('lokk', Lk, None)], 40, -110)

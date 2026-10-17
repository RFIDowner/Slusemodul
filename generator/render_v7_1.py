#!/usr/bin/env python3
"""Lager PNG-bilder av v7.1 fra STEP-filene (cadquery -> trimesh -> matplotlib). Skrives til tegninger/v7.1/."""
import os
import numpy as np
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, '..', 'step', 'v7.1')
OUT = os.path.join(HERE, '..', 'tegninger', 'v7.1')
os.makedirs(OUT, exist_ok=True)

def mesh_of(shape, tol=0.15, max_edge=12.0):
    verts, tris = shape.tessellate(tol, 0.3)
    m = trimesh.Trimesh(np.array([(p.x, p.y, p.z) for p in verts]), np.array(tris), process=False)
    return m.subdivide_to_size(max_edge=max_edge)
def load(name):
    return cq.importers.importStep(os.path.join(STEP, f'sluse_v7.1_{name}.step')).val()

parts = {n: mesh_of(load(n)) for n in ('plint', 'hette', 'lokk')}
parts['splint'] = mesh_of(load('splint'), tol=0.05, max_edge=2.0)
COL = {'plint': (0.82, 0.82, 0.80), 'hette': (0.72, 0.76, 0.88), 'lokk': (0.62, 0.80, 0.60), 'splint': (0.9, 0.6, 0.2)}
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

T = trimesh.transformations
def flipx(): return T.rotation_matrix(np.pi, (1, 0, 0))
def move(dx=0, dy=0, dz=0): return T.translation_matrix((dx, dy, dz))
P, Hh, Lk, Sp = parts['plint'], parts['hette'], parts['lokk'], parts['splint']
# de fire splintene: STEP-fila er splinten ved x 6.6 paa +y-siden
mirror_y = np.diag([1.0, -1.0, 1.0, 1.0])
def splint_at(x, side):
    m = Sp.copy()
    if side < 0:
        m.apply_transform(mirror_y); m.invert()
    m.apply_transform(move(dx=x - 6.6))
    return m
SPL = [splint_at(6.6, 1), splint_at(6.6, -1), splint_at(167.0, 1), splint_at(167.0, -1)]
def spl_items(tf=None, out=0.0):
    return [('splint', s, (tf if tf is not None else np.eye(4)) @ (move(dy=(out if i % 2 == 0 else -out)))) for i, s in enumerate(SPL)]

base = [('plint', P, None), ('hette', Hh, None), ('lokk', Lk, None)] + spl_items()
view('sluse_v7.1_montert.png', 'Duesluse v7.1 - plint og hette, sett fra inngangen', base, 24, -125)
view('sluse_v7.1_fra_slaget.png', 'v7.1 sett fra slaget: utgangsportal og 40 mm gulv uten vegger', base, 24, 40)
view('sluse_v7.1_side.png', 'v7.1 fra -y: fire takstoler, kryss, splinthoder ved forste og siste, skuffeapningen under', base, 6, -90)
view('sluse_v7.1_delt.png', 'v7.1 delt: hetta loftet 60 mm, splintene trukket ut', 
     [('plint', P, None), ('lokk', Lk, None), ('hette', Hh, move(dz=60))] + spl_items(out=25), 22, -120)
view('sluse_v7.1_snitt_stolpe.png', 'v7.1 snitt gjennom stolperekka pa +y (y > 61 fjernet): tapper i hullene, klosser, splint',
     [('plint', P, None), ('hette', Hh, None), ('lokk', Lk, None)] + spl_items(), 12, 95, clip=lambda v: v[:, :, 1] < 61.2)
view('sluse_v7.1_snitt_midt.png', 'v7.1 snitt langs midten (y < 0 fjernet): el-rom, skillevegg, spolelomme, takstoler med 6 mm gavl',
     [('plint', P, None), ('hette', Hh, None), ('lokk', Lk, None)], 14, -70, clip=lambda v: v[:, :, 1] > 0)
view('sluse_v7.1_plint.png', 'Plinten ovenfra: 8 stolpehull, 4 festehull i veggen', [('plint', P, None), ('lokk', Lk, None)], 40, -120)
view('sluse_v7.1_kammer.png', 'Plinten nedenfra uten skuff: el-rom, klosser, leserholder, spolelomme', [('plint', P, flipx())], 40, -115)
view('sluse_v7.1_oere.png', 'Festeore ved inngangen (-y): flens 6 mm, senket skruehull 10 mm fra kanten, kile 45 grader',
     [('plint', P, None)], 28, -135, lim=[(-20, -66, 0), (25, -20, 30)], clip=lambda v: (v[:, :, 0] < 30) & (v[:, :, 1] < -20))
view('sluse_v7.1_hette_print.png', 'Hetta slik den printes: toppramma ned, tappene opp', [('hette', Hh, flipx() @ move(dz=-197))], 20, -125)
view('sluse_v7.1_splint.png', 'Splinten: hode, slisse, to tunger med mothake, flate under', [('splint', Sp, None)], 30, -60)

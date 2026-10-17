#!/usr/bin/env python3
"""Lager PNG-bilder av v7.3 fra STEP-filene (cadquery -> trimesh -> matplotlib). Skrives til tegninger/v7.3/."""
import os
import numpy as np
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, '..', 'step', 'v7.3')
OUT = os.path.join(HERE, '..', 'tegninger', 'v7.3')
os.makedirs(OUT, exist_ok=True)

def mesh_of(shape, tol=0.15, max_edge=12.0):
    verts, tris = shape.tessellate(tol, 0.3)
    m = trimesh.Trimesh(np.array([(p.x, p.y, p.z) for p in verts]), np.array(tris), process=False)
    return m.subdivide_to_size(max_edge=max_edge)
def load(name):
    return cq.importers.importStep(os.path.join(STEP, f'sluse_v7.3_{name}.step')).val()

parts = {n: mesh_of(load(n)) for n in ('plint', 'hette', 'lokk')}
parts['splint'] = mesh_of(load('splint'), tol=0.05, max_edge=2.0)
parts['gaffel'] = mesh_of(load('gaffel'), tol=0.05, max_edge=3.0)
COL = {'plint': (0.82, 0.82, 0.80), 'hette': (0.72, 0.76, 0.88), 'lokk': (0.62, 0.80, 0.60), 'splint': (0.9, 0.6, 0.2),
       'gaffel': (0.85, 0.62, 0.35)}
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
P, Hh, Lk, Sp, G = parts['plint'], parts['hette'], parts['lokk'], parts['splint'], parts['gaffel']
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
# de fem gaflene: STEP-fila er den midterste (y 0), de andre er forskjøvet 22,5 mm
BOBS_Y = [-45.0, -22.5, 0.0, 22.5, 45.0]
def bob_items(tf=None):
    return [('gaffel', G, (tf if tf is not None else np.eye(4)) @ move(dy=y)) for y in BOBS_Y]
# gaffel svingt om tverrstangen (x 178.5, z 192.4): 60 grader inn i slaget (dyttet av en due), og 90 grader loftet 12 mm (kneppes paa)
PIV = (178.5, 0.0, 192.4)
def swing(deg, lift=0.0):
    best = None
    for s in (1, -1):
        tf = move(*PIV) @ T.rotation_matrix(np.radians(s * deg), (0, 1, 0)) @ move(*[-v for v in PIV])
        m = G.copy(); m.apply_transform(tf)
        if best is None or m.vertices[:, 0].max() > best[1]:
            best = (tf, m.vertices[:, 0].max())
    return move(dz=lift) @ best[0]

base = [('plint', P, None), ('hette', Hh, None), ('lokk', Lk, None)] + spl_items() + bob_items()
view('sluse_v7.3_montert.png', 'Duesluse v7.3 - plint, hette og fem gafler ved utgangen, sett fra inngangen', base, 24, -125)
view('sluse_v7.3_fra_slaget.png', 'v7.3 sett fra slaget: rett gavl, tverrstang i orene, fem gafler som bare svinger inn', base, 24, 40)
view('sluse_v7.3_side.png', 'v7.3 fra -y: en avstiver per side, fra foten av forste stolpe opp mot slaget', base, 6, -90)
view('sluse_v7.3_delt.png', 'v7.3 delt: hetta loftet 60 mm, splintene trukket ut, gaflene folger hetta',
     [('plint', P, None), ('lokk', Lk, None), ('hette', Hh, move(dz=60))] + spl_items(out=25) + bob_items(move(dz=60)), 22, -120)
view('sluse_v7.3_snitt_midt.png', 'v7.3 snitt langs midten (y < 0 fjernet): siste takstol med rett gavl og overligger, gaffel mot overliggeren',
     [('plint', P, None), ('hette', Hh, None), ('lokk', Lk, None)] + [('gaffel', G, move(dy=y)) for y in BOBS_Y if y >= 0], 14, -70,
     clip=lambda v: v[:, :, 1] > 0)
view('sluse_v7.3_gaffel_stopp.png', 'Gaffelen i ro, snitt midt i navet: hviler mot overliggeren, nokkelhullet paa tverrstangen, slissen mot gavlen',
     [('hette', Hh, None), ('gaffel', G, None)], 0, -90, lim=[(150, -10, 130), (200, 10, 205)],
     clip=lambda v: (v[:, :, 1] < 0.5) & (v[:, :, 1] > -30))
view('sluse_v7.3_gaffel_svingt.png', 'Due paa vei inn: gaffelen svinger 60 grader inn i slaget. Mot inngangen stopper den i overliggeren',
     [('plint', P, None), ('hette', Hh, None), ('gaffel', G, swing(60))] + [('gaffel', G, move(dy=y)) for y in BOBS_Y if y > 0], 8, -75,
     lim=[(120, -70, 20), (300, 70, 205)], clip=lambda v: v[:, :, 1] > -1)
view('sluse_v7.3_gaffel_paa.png', 'Kneppe paa: gaffelen holdes vannrett inn i slaget, slissen peker ned, og senkes over tverrstangen',
     [('hette', Hh, None), ('gaffel', G, swing(90, lift=12))] + [('gaffel', G, move(dy=y)) for y in BOBS_Y if y > 0], 8, -75,
     lim=[(120, -70, 20), (300, 70, 215)], clip=lambda v: v[:, :, 1] > -1)
view('sluse_v7.3_gaffel.png', 'Gaffelen: nav 22 x 13 mm med nokkelhull (8-kant hull, 45 graders tak, slisse 6,3), 8-kant stang 6 mm',
     [('gaffel', G, None)], 25, -50, lim=[(165, -15, 160), (195, 15, 205)])
G3 = trimesh.load(os.path.join(HERE, '..', 'stl', 'v7.3', 'sluse_v7.3_print3_gafler.stl'), force='mesh').subdivide_to_size(max_edge=3.0)
view('sluse_v7.3_gaffel_print.png', 'Print 3: fem gafler liggende paa fottene ved slissen og stangens flate, taket over hullet opp',
     [('gaffel', G3, None)], 30, -60)
view('sluse_v7.3_plint.png', 'Plinten ovenfra: 8 stolpehull, 4 festehull i veggen (som v7.1)', [('plint', P, None), ('lokk', Lk, None)], 40, -120)
view('sluse_v7.3_hette_print.png', 'Hetta slik den printes: toppramma, orene og tverrstangen ned paa plata, tappene opp',
     [('hette', Hh, flipx() @ move(dz=-197))], 20, -125)
view('sluse_v7.3_hette_print_stang.png', 'Hetta i printen, enden mot slaget: tverrstangen paa plata mellom orene, overliggeren over',
     [('hette', Hh, flipx() @ move(dz=-197))], 18, -40, lim=[(150, -70, 0), (200, 70, 70)], clip=lambda v: v[:, :, 0] > 140)

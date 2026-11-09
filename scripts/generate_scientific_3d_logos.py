#!/usr/bin/env python3
"""
HyperSettle Scientific Differential Geometry 3D Logo Engine
Generates 10 unique mathematical surface logos inspired by:
1. Matplotlib / Mathematica 3D scientific coordinate plots (rainbow jet colormap + 3D grid cage)
2. Curve Finance (Michael Egorov's Boy's surface topological wireframe minimal brand lockup)
3. Blender 3D physical raytraced meshes
"""

import os
import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, 'branding', 'scientific-differential-geometry-10')
SCIENTIFIC_DIR = os.path.join(OUT_DIR, 'scientific-plots')
BRAND_DIR = os.path.join(OUT_DIR, 'brand-lockups')
DATA_DIR = os.path.join(OUT_DIR, 'mesh-data')

os.makedirs(SCIENTIFIC_DIR, exist_ok=True)
os.makedirs(BRAND_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# 10 Mathematically rigorous differential geometry surfaces
def generate_surfaces():
    surfaces = []

    # 1. Boy's Surface (Curve Finance Archetype - Apery immersion of Projective Plane)
    u = np.linspace(0, np.pi, 60)
    v = np.linspace(0, np.pi, 60)
    U, V = np.meshgrid(u, v)
    den = 2.0 - np.sqrt(2.0) * np.sin(3*U) * np.sin(2*V)
    den = np.where(np.abs(den) < 1e-4, 1e-4, den)
    x1 = (np.sqrt(2.0) * np.cos(V)**2 * np.cos(2*U) + np.cos(U) * np.sin(2*V)) / den
    y1 = (np.sqrt(2.0) * np.cos(V)**2 * np.sin(2*U) - np.sin(U) * np.sin(2*V)) / den
    z1 = (3.0 * np.cos(V)**2) / den
    surfaces.append({
        'id': '01_boys_surface',
        'title': "Boy's Surface",
        'subtitle': "Curve Finance Topological Archetype (Immersion of Real Projective Plane)",
        'equations': "Apery Parametrization: RP² immersion with order-3 cyclic symmetry",
        'X': x1, 'Y': y1, 'Z': z1,
        'elev': 28, 'azim': 125
    })

    # 2. Figure-8 Klein Bottle (User Reference 1 - Topological Non-Orientable Manifold)
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)
    r = 2.0 + np.cos(U/2.0) * np.sin(V) - np.sin(U/2.0) * np.sin(2*V)
    x2 = r * np.cos(U)
    y2 = r * np.sin(U)
    z2 = np.sin(U/2.0) * np.sin(V) + np.cos(U/2.0) * np.sin(2*V)
    surfaces.append({
        'id': '02_figure8_klein_bottle',
        'title': "Figure-8 Klein Bottle",
        'subtitle': "Non-Orientable 2-Manifold Immersion (User Reference Matplotlib Model)",
        'equations': "r(u,v) = 2 + cos(u/2)sin(v) - sin(u/2)sin(2v)",
        'X': x2, 'Y': y2, 'Z': z2,
        'elev': 32, 'azim': -60
    })

    # 3. 33rd Tree Singularity Funnel (Black Hole Event Horizon + Accretion Curvature)
    r_val = np.linspace(0.2, 3.2, 60)
    theta = np.linspace(0, 2*np.pi, 60)
    R, TH = np.meshgrid(r_val, theta)
    twist = TH + 1.2 / (R + 0.25)
    x3 = R * np.cos(twist)
    y3 = R * np.sin(twist)
    z3 = -1.4 * np.log(R + 0.15) * (1.0 + 0.18 * np.cos(3*TH))
    surfaces.append({
        'id': '03_singularity_funnel',
        'title': "33rd Tree Singularity Funnel",
        'subtitle': "Kerr Metric Ergosphere & Spacetime Curvature Gradient",
        'equations': "z(r,θ) = -1.4·ln(r + 0.15)·(1 + 0.18·cos(3θ)) with frame-dragging twist",
        'X': x3, 'Y': y3, 'Z': z3,
        'elev': 35, 'azim': -45
    })

    # 4. Dupin Cyclide (Conformal Inversion of Ring Torus)
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)
    a, b = 1.5, 1.1
    c = np.sqrt(a**2 - b**2)
    mu = 1.3
    d = a - c * np.cos(U) * np.cos(V)
    d = np.where(np.abs(d) < 1e-4, 1e-4, d)
    x4 = (mu * (c - a * np.cos(U) * np.cos(V)) + b**2 * np.cos(U)) / d
    y4 = (b * np.sin(U) * (a - mu * np.cos(V))) / d
    z4 = (b * np.sin(V) * (c * np.cos(U) - mu)) / d
    surfaces.append({
        'id': '04_dupin_cyclide',
        'title': "Dupin Cyclide",
        'subtitle': "Conformal Inversion Manifold of Principal Curvature Lines",
        'equations': "Dupin (1822): Envelope of a family of spheres tangent to three fixed spheres",
        'X': x4, 'Y': y4, 'Z': z4,
        'elev': 25, 'azim': 55
    })

    # 5. Enneper Minimal Surface (Weierstrass-Enneper Representation)
    u = np.linspace(-1.7, 1.7, 60)
    v = np.linspace(-1.7, 1.7, 60)
    U, V = np.meshgrid(u, v)
    x5 = U - (U**3)/3.0 + U * (V**2)
    y5 = V - (V**3)/3.0 + V * (U**2)
    z5 = U**2 - V**2
    surfaces.append({
        'id': '05_enneper_surface',
        'title': "Enneper Minimal Surface",
        'subtitle': "Classical Zero-Mean Curvature (H=0) Self-Intersecting Sheet",
        'equations': "x = u - u³/3 + uv²,  y = v - v³/3 + vu²,  z = u² - v²",
        'X': x5, 'Y': y5, 'Z': z5,
        'elev': 30, 'azim': 45
    })

    # 6. Clifford Torus (Stereographic Projection from 4D S³ to R³)
    u = np.linspace(0, 2*np.pi, 60)
    v = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)
    x1_4d = np.cos(U) / np.sqrt(2.0)
    x2_4d = np.sin(U) / np.sqrt(2.0)
    x3_4d = np.cos(V) / np.sqrt(2.0)
    x4_4d = np.sin(V) / np.sqrt(2.0)
    p_den = 1.0 - 0.75 * x4_4d
    x6 = x1_4d / p_den
    y6 = x2_4d / p_den
    z6 = x3_4d / p_den
    surfaces.append({
        'id': '06_clifford_torus',
        'title': "Clifford Torus Projection",
        'subtitle': "Flat Torus in 4-Space S³ Stereographically Projected into R³",
        'equations': "S¹ × S¹ ⊂ S³ ⊂ R⁴ stereographic projection onto R³",
        'X': x6, 'Y': y6, 'Z': z6,
        'elev': 30, 'azim': 120
    })

    # 7. Breather Soliton Surface (Sine-Gordon Nonlinear Wave Packet)
    u = np.linspace(-12, 12, 60)
    v = np.linspace(-26, 26, 60)
    U, V = np.meshgrid(u, v)
    aa = 0.45
    w = np.sqrt(1.0 - aa**2)
    denom = aa * ((w * np.cosh(aa * U))**2 + (aa * np.sin(w * V))**2)
    denom = np.where(np.abs(denom) < 1e-4, 1e-4, denom)
    x7 = -U + (2.0 * (1.0 - aa**2) * np.cosh(aa * U) * np.sinh(aa * U)) / denom
    y7 = (2.0 * w * np.cosh(aa * U) * (-w * np.cos(V) * np.cos(w * V) - np.sin(V) * np.sin(w * V))) / denom
    z7 = (2.0 * w * np.cosh(aa * U) * (-w * np.sin(V) * np.cos(w * V) + np.cos(V) * np.sin(w * V))) / denom
    surfaces.append({
        'id': '07_breather_soliton',
        'title': "Breather Soliton Manifold",
        'subtitle': "Exact Analytical Solution to Sine-Gordon Nonlinear Wave Equation",
        'equations': "Breather pseudospherical surface modeling localized topological energy solitons",
        'X': x7, 'Y': y7, 'Z': z7,
        'elev': 25, 'azim': 135
    })

    # 8. Dini's Surface (Twisted Pseudosphere with Constant Negative Curvature K = -1)
    u = np.linspace(0.08, 2.0, 60)
    v = np.linspace(0, 4*np.pi, 60)
    U, V = np.meshgrid(u, v)
    a_dini = 1.0
    b_dini = 0.22
    x8 = a_dini * np.sin(U) * np.cos(V)
    y8 = a_dini * np.sin(U) * np.sin(V)
    z8 = a_dini * (np.cos(U) + np.log(np.tan(U/2.0))) + b_dini * V
    surfaces.append({
        'id': '08_dini_pseudosphere',
        'title': "Dini's Pseudosphere Spiral",
        'subtitle': "Surface of Constant Negative Curvature (K = -1) Twisted into a Helix",
        'equations': "Pseudosphere transformation with helical pitch b=0.22",
        'X': x8, 'Y': y8, 'Z': z8,
        'elev': 20, 'azim': 70
    })

    # 9. Kuen Pseudospherical Surface (Cusp Singularities & Dual Horns)
    u = np.linspace(-4.0, 4.0, 60)
    v = np.linspace(0.08, np.pi - 0.08, 60)
    U, V = np.meshgrid(u, v)
    k_den = 1.0 + (U**2) * (np.sin(V)**2)
    k_den = np.where(np.abs(k_den) < 1e-4, 1e-4, k_den)
    x9 = (2.0 * (np.cos(U) + U * np.sin(U)) * np.sin(V)) / k_den
    y9 = (2.0 * (np.sin(U) - U * np.cos(U)) * np.sin(V)) / k_den
    z9 = np.log(np.tan(V/2.0)) + (2.0 * np.cos(V)) / k_den
    surfaces.append({
        'id': '09_kuen_surface',
        'title': "Kuen Pseudosphere",
        'subtitle': "Constant Negative Curvature Manifold with Dual Horn Singularities",
        'equations': "Alfred Kuen (1884): Pseudospherical surface with asymptotic lines",
        'X': x9, 'Y': y9, 'Z': z9,
        'elev': 20, 'azim': 110
    })

    # 10. Cross-Cap Projective Plane (Self-Intersecting Line Segment Singularity)
    u = np.linspace(0, np.pi, 60)
    v = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)
    x10 = 0.5 * np.sin(2*U) * (np.sin(V)**2)
    y10 = 0.5 * np.sin(U) * np.cos(2*V)
    z10 = 0.5 * np.cos(U) * np.sin(2*V)
    surfaces.append({
        'id': '10_cross_cap',
        'title': "Cross-Cap Projective Plane",
        'subtitle': "Non-Orientable Manifold with Pinch-Point Whitney Singularities",
        'equations': "Classic immersion of the real projective plane with a line of self-intersection",
        'X': x10, 'Y': y10, 'Z': z10,
        'elev': 25, 'azim': 65
    })

    return surfaces

def render_scientific_plots(surfaces):
    print("Generating 10 Scientific Differential Geometry 3D Plots (Matplotlib)...")
    for s in surfaces:
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.add_subplot(projection='3d')
        
        # Color mapping: Jet / Turbo spectrum as requested in User Reference 1
        X, Y, Z = s['X'], s['Y'], s['Z']
        
        # Surface plot with wireframe edges and rainbow jet colormap
        surf = ax.plot_surface(
            X, Y, Z,
            cmap=cm.jet,
            rstride=1,
            cstride=1,
            edgecolor=(0.05, 0.05, 0.05, 0.35),
            linewidth=0.35,
            antialiased=True,
            shade=True,
            alpha=0.96
        )
        
        ax.view_init(elev=s['elev'], azim=s['azim'])
        
        # Authentic scientific styling: gray grid cage, subtle panes
        ax.set_facecolor('#ffffff')
        fig.patch.set_facecolor('#ffffff')
        
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        ax.xaxis.pane.set_edgecolor('#d1d5db')
        ax.yaxis.pane.set_edgecolor('#d1d5db')
        ax.zaxis.pane.set_edgecolor('#d1d5db')
        
        ax.grid(True, linestyle='-', color='#e5e7eb', linewidth=0.6)
        
        ax.tick_params(colors='#6b7280', labelsize=8)
        ax.set_title(f"{s['title']}\n[ HyperSettle Scientific Differential Geometry Engine ]", 
                     fontsize=11, fontweight='bold', color='#111827', pad=12, fontfamily='monospace')
        
        out_path = os.path.join(SCIENTIFIC_DIR, f"{s['id']}_scientific_plot.png")
        plt.savefig(out_path, bbox_inches='tight', dpi=300, facecolor='#ffffff')
        plt.close(fig)
        print(f"  ✓ Saved scientific plot: {out_path}")

def render_brand_lockups(surfaces):
    print("Generating 10 Curve Finance-Style Minimal Brand Lockups (300 DPI)...")
    for s in surfaces:
        fig = plt.figure(figsize=(10, 4.5), dpi=300)
        
        # Left 3D wireframe icon
        ax = fig.add_axes([0.02, 0.05, 0.42, 0.9], projection='3d')
        X, Y, Z = s['X'], s['Y'], s['Z']
        
        # Pure technical wireframe without axis box, exact Curve style
        ax.plot_wireframe(
            X, Y, Z,
            rstride=2,
            cstride=2,
            color='#0d1b2a', # Deep space navy (Curve brand tone)
            linewidth=0.65,
            antialiased=True
        )
        
        ax.view_init(elev=s['elev'], azim=s['azim'])
        ax.set_axis_off()
        ax.set_facecolor('#ffffff')
        fig.patch.set_facecolor('#ffffff')
        
        # Right typography block matching Curve Finance + Obel Mono aesthetic
        fig.text(0.48, 0.64, "HyperSettle", fontsize=28, fontweight='bold', 
                 color='#0d1b2a', fontfamily='sans-serif')
        fig.text(0.48, 0.52, f"PARAMETRIC MANIFOLD #{s['id'][:2]} // {s['title'].upper()}", 
                 fontsize=10, fontweight='bold', color='#0284c7', fontfamily='monospace')
        fig.text(0.48, 0.42, s['subtitle'], fontsize=9, color='#4b5563', fontfamily='sans-serif')
        fig.text(0.48, 0.32, f"FORMULATION: {s['equations']}", 
                 fontsize=8, color='#6b7280', fontfamily='monospace')
        fig.text(0.48, 0.22, "SETTLEMENT: HYPERLIQUID DEX BUILDER FEES → SOLANA SPL USDC", 
                 fontsize=8, fontweight='bold', color='#059669', fontfamily='monospace')
        
        out_path = os.path.join(BRAND_DIR, f"{s['id']}_curve_brand_lockup.png")
        plt.savefig(out_path, bbox_inches='tight', dpi=300, facecolor='#ffffff')
        plt.close(fig)
        print(f"  ✓ Saved brand lockup: {out_path}")

def export_mesh_data_json(surfaces):
    """Save 3D vertex and quad index data for WebGL Three.js interactive inspector"""
    import json
    mesh_catalogue = []
    for s in surfaces:
        X, Y, Z = s['X'], s['Y'], s['Z']
        # Resample to 30x30 for lightweight client-side rendering
        step = 2
        xs = X[::step, ::step].tolist()
        ys = Y[::step, ::step].tolist()
        zs = Z[::step, ::step].tolist()
        mesh_catalogue.append({
            'id': s['id'],
            'title': s['title'],
            'subtitle': s['subtitle'],
            'equations': s['equations'],
            'elev': s['elev'],
            'azim': s['azim'],
            'rows': len(xs),
            'cols': len(xs[0]),
            'x': xs,
            'y': ys,
            'z': zs
        })
    json_path = os.path.join(DATA_DIR, 'surfaces.json')
    with open(json_path, 'w') as f:
        json.dump(mesh_catalogue, f, indent=2)
    print(f"  ✓ Exported surface JSON catalogue for interactive 3D: {json_path}")

if __name__ == '__main__':
    surfaces = generate_surfaces()
    render_scientific_plots(surfaces)
    render_brand_lockups(surfaces)
    export_mesh_data_json(surfaces)
    print("\nAll 10 Scientific Differential Geometry models rendered successfully!")

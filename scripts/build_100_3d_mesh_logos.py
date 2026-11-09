#!/usr/bin/env python3
"""
HyperSettle - 100 3D Parametric Mesh Grid Logos
Inspired by:
1. The 3D Rainbow/Jet Mesh Differential Geometry Plot (User Uploaded Image 1)
2. The Curve Finance Boy's Surface / Wireframe Immersion Logo (User Uploaded Image 2)
3. The 33rd Tree Labs Singularity Exponential Plunge (#06)

Generates 100 mathematically authentic 3D parametric quad-mesh vector SVGs:
- Real 3D rotation, perspective projection, depth sorting (Painter's algorithm)
- Shaded quadrilateral facets with authentic wireframe grid lines
- 3D bounding coordinate box / floor grid options (Matplotlib style) and clean floating wireframe options (Curve.fi style)
- Colormaps: Rainbow/Jet, Hyperliquid Mint-Cyan-Solana, Curve.fi Navy Wireframe, Monochromatic HUD
"""

import os
import math

BASE_DIR = "/Users/ianmora/Desktop/Projects/HyperSettle"
OUTPUT_DIR = os.path.join(BASE_DIR, "branding", "mesh-3d-100")
SHOWCASE_HTML = os.path.join(BASE_DIR, "branding", "showcase_3d_mesh_100.html")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# COLORMAP ENGINE
# -----------------------------------------------------------------------------
PALETTES = {
    "rainbow_jet": [
        (0.00, (0, 20, 240)),     # Blue
        (0.20, (0, 220, 255)),    # Cyan
        (0.40, (20, 240, 60)),    # Green
        (0.65, (255, 235, 0)),    # Yellow
        (0.85, (255, 110, 0)),    # Orange
        (1.00, (240, 20, 0))      # Red
    ],
    "hyperliquid_spectral": [
        (0.00, (15, 57, 51)),     # Deep Teal
        (0.25, (152, 252, 228)),  # Hyperliquid Mint
        (0.50, (0, 229, 255)),    # Electric Cyan
        (0.75, (153, 69, 255)),   # Solana Violet
        (1.00, (255, 0, 122))     # Neon Magenta
    ],
    "curve_navy_wire": [
        (0.00, (10, 17, 40)),
        (1.00, (15, 30, 70))
    ],
    "monochrome_hud": [
        (0.00, (40, 40, 40)),
        (1.00, (255, 255, 255))
    ],
    "aurora_neon": [
        (0.00, (16, 185, 129)),   # Emerald
        (0.35, (0, 245, 212)),    # Mint
        (0.70, (0, 112, 243)),    # Blue
        (1.00, (123, 44, 191))    # Purple
    ],
    "magma_heat": [
        (0.00, (10, 5, 20)),
        (0.30, (140, 20, 80)),
        (0.60, (230, 60, 20)),
        (0.85, (255, 180, 0)),
        (1.00, (255, 255, 220))
    ]
}

def get_color(t, palette_name="rainbow_jet"):
    stops = PALETTES.get(palette_name, PALETTES["rainbow_jet"])
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i+1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            r = int(c0[0] + f * (c1[0] - c0[0]))
            g = int(c0[1] + f * (c1[1] - c0[1]))
            b = int(c0[2] + f * (c1[2] - c0[2]))
            return r, g, b
    c = stops[-1][1]
    return c[0], c[1], c[2]

# -----------------------------------------------------------------------------
# 3D ROTATION & PROJECTION ENGINE
# -----------------------------------------------------------------------------
def rotate_point(p, rx_deg, ry_deg, rz_deg):
    x, y, z = p
    # Convert to radians
    rad_x, rad_y, rad_z = math.radians(rx_deg), math.radians(ry_deg), math.radians(rz_deg)
    
    # X rotation
    cos_x, sin_x = math.cos(rad_x), math.sin(rad_x)
    y1 = y * cos_x - z * sin_x
    z1 = y * sin_x + z * cos_x
    x1 = x
    
    # Y rotation
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    x2 = x1 * cos_y + z1 * sin_y
    z2 = -x1 * sin_y + z1 * cos_y
    y2 = y1
    
    # Z rotation
    cos_z, sin_z = math.cos(rad_z), math.sin(rad_z)
    x3 = x2 * cos_z - y2 * sin_z
    y3 = x2 * sin_z + y2 * cos_z
    z3 = z2
    
    return x3, y3, z3

def project_point(p3, width=512, height=512, zoom=140, fov=4.5):
    x, y, z = p3
    dist = fov
    factor = zoom * (dist / (dist + z))
    px = width / 2 + x * factor
    py = height / 2 - y * factor
    return px, py, z

# -----------------------------------------------------------------------------
# 25 PARAMETRIC SURFACE EQUATIONS
# -----------------------------------------------------------------------------
def surf_boys_surface(u, v):
    # Curve.fi signature shape: Boy's surface in Apery's parametrization
    # u in [0, pi], v in [0, pi]
    cu, su = math.cos(u), math.sin(u)
    cv, sv = math.cos(v), math.sin(v)
    c2u, s2u = math.cos(2*u), math.sin(2*u)
    c2v, s2v = math.cos(2*v), math.sin(2*v)
    s3u = math.sin(3*u)
    den = 2.0 - math.sqrt(2.0) * s3u * s2v
    if abs(den) < 1e-4: den = 1e-4
    x = (math.sqrt(2.0) * cv * cv * c2u + cu * s2v) / den
    y = (math.sqrt(2.0) * cv * cv * s2u - su * s2v) / den
    z = (3.0 * cv * cv) / den - 1.2
    return x * 1.1, y * 1.1, z * 1.1

def surf_klein_bottle_figure8(u, v):
    # u in [0, 2*pi], v in [0, 2*pi]
    r = 2.0
    cu, su = math.cos(u), math.sin(u)
    cu2, su2 = math.cos(u/2), math.sin(u/2)
    sv, s2v = math.sin(v), math.sin(2*v)
    x = (r + cu2 * sv - su2 * s2v) * cu
    y = (r + cu2 * sv - su2 * s2v) * su
    z = su2 * sv + cu2 * s2v
    return x * 0.55, y * 0.55, z * 0.8

def surf_33rd_singularity_funnel(u, v):
    # The 33rd Tree Exponential Plunge (#06) in full 3D!
    # u in [0, 2*pi], v in [-1, 1]
    norm = min(1.0, abs(v))
    r = 0.08 + 1.65 * ((math.exp(3.8 * norm) - 1.0) / (math.exp(3.8) - 1.0))
    x = r * math.cos(u)
    y = r * math.sin(u)
    z = v * 1.5
    return x, y, z

def surf_dupin_cyclide(u, v):
    # Ring / Horn cyclide inversion
    # u in [0, 2*pi], v in [0, 2*pi]
    a, b, c, d = 1.8, 1.4, 1.1, 0.9
    cu, cv = math.cos(u), math.cos(v)
    su, sv = math.sin(u), math.sin(v)
    den = a - c * cu * cv
    if abs(den) < 1e-4: den = 1e-4
    x = (d * (c - a * cu * cv) + b * b * cu) / den
    y = (b * su * (a - d * cv)) / den
    z = (b * sv * (c * cu - d)) / den
    return x * 0.8, y * 0.8, z * 0.8

def surf_enneper(u, v):
    # u in [-1.6, 1.6], v in [-1.6, 1.6]
    x = u - (u**3)/3 + u * (v**2)
    y = v - (v**3)/3 + v * (u**2)
    z = (u**2) - (v**2)
    return x * 0.5, y * 0.5, z * 0.5

def surf_cross_cap(u, v):
    # Real projective plane immersion
    # u in [0, pi], v in [0, 2*pi]
    x = math.sin(u) * math.sin(2*v)
    y = math.sin(2*u) * (math.cos(v)**2)
    z = math.cos(2*u) * (math.cos(v)**2)
    return x * 1.5, y * 1.5, z * 1.5

def surf_clifford_torus(u, v):
    # Stereographic projection of flat 4D torus
    # u in [0, 2*pi], v in [0, 2*pi]
    den = math.sqrt(2.0) - math.sin(u - v)
    if abs(den) < 1e-4: den = 1e-4
    x = math.cos(u + v) / den
    y = math.sin(u + v) / den
    z = math.cos(u - v) / den
    return x * 0.9, y * 0.9, z * 0.9

def surf_catenoid(u, v):
    # Minimal surface
    # u in [0, 2*pi], v in [-1.5, 1.5]
    c = 0.7
    x = c * math.cosh(v / c) * math.cos(u)
    y = c * math.cosh(v / c) * math.sin(u)
    z = v
    return x * 0.8, y * 0.8, z * 0.8

def surf_helicoid(u, v):
    # u in [-1.6, 1.6], v in [-2.5, 2.5]
    x = u * math.cos(v)
    y = u * math.sin(v)
    z = 0.5 * v
    return x * 0.9, y * 0.9, z * 0.8

def surf_kuen_surface(u, v):
    # Pseudospherical immersion
    # u in [-3, 3], v in [0.05, pi - 0.05]
    su, cu = math.sin(u), math.cos(u)
    sv, cv = math.sin(v), math.cos(v)
    den = 1.0 + (u**2) * (sv**2)
    if abs(den) < 1e-4: den = 1e-4
    x = 2.0 * (cu + u * su) * sv / den
    y = 2.0 * (su - u * cu) * sv / den
    z = math.log(max(1e-4, math.tan(v/2.0))) + 2.0 * cv / den
    return x * 0.65, y * 0.65, z * 0.45

def surf_dini_surface(u, v):
    # Twisted pseudosphere
    # u in [0, 4*pi], v in [0.1, 2.0]
    a, b = 1.0, 0.2
    cu, su = math.cos(u), math.sin(u)
    sv, cv = math.sin(v), math.cos(v)
    x = a * cu * sv
    y = a * su * sv
    z = a * (cv + math.log(max(1e-4, math.tan(v/2.0)))) + b * u - 1.5
    return x * 1.1, y * 1.1, z * 0.4

def surf_trefoil_tube(u, v):
    # Trefoil knot (p=2, q=3) with tube frame
    # u in [0, 2*pi] (around knot), v in [0, 2*pi] (around tube)
    r_tube = 0.38
    # Curve center
    x0 = math.sin(u) + 2.0 * math.sin(2*u)
    y0 = math.cos(u) - 2.0 * math.cos(2*u)
    z0 = -math.sin(3*u)
    # Approx tangent
    tx = math.cos(u) + 4.0 * math.cos(2*u)
    ty = -math.sin(u) + 4.0 * math.sin(2*u)
    tz = -3.0 * math.cos(3*u)
    t_len = math.sqrt(tx*tx + ty*ty + tz*tz) + 1e-6
    tx, ty, tz = tx/t_len, ty/t_len, tz/t_len
    # Normal and binormal
    nx, ny, nz = -ty, tx, 0
    n_len = math.sqrt(nx*nx + ny*ny) + 1e-6
    nx, ny = nx/n_len, ny/n_len
    bx = ty*nz - tz*ny
    by = tz*nx - tx*nz
    bz = tx*ny - ty*nx
    x = x0 + r_tube * (math.cos(v) * nx + math.sin(v) * bx)
    y = y0 + r_tube * (math.cos(v) * ny + math.sin(v) * by)
    z = z0 + r_tube * (math.cos(v) * nz + math.sin(v) * bz)
    return x * 0.5, y * 0.5, z * 0.55

def surf_mobius_strip(u, v):
    # u in [0, 2*pi], v in [-0.5, 0.5]
    cu, su = math.cos(u), math.sin(u)
    cu2, su2 = math.cos(u/2.0), math.sin(u/2.0)
    x = (1.5 + v * cu2) * cu
    y = (1.5 + v * cu2) * su
    z = v * su2
    return x * 0.9, y * 0.9, z * 1.4

def surf_gabriels_horn(u, v):
    # u in [0, 2*pi], v in [0.25, 2.5]
    r = 0.6 / v
    x = r * math.cos(u)
    y = r * math.sin(u)
    z = v - 1.3
    return x * 1.5, y * 1.5, z * 1.0

def surf_steiner_roman(u, v):
    # u in [0, pi], v in [0, pi]
    r = 1.6
    x = 0.5 * r * math.sin(2*u) * (math.sin(v)**2)
    y = 0.5 * r * math.sin(u) * math.sin(2*v)
    z = 0.5 * r * math.cos(u) * math.sin(2*v)
    return x * 1.4, y * 1.4, z * 1.4

def surf_calabi_yau_slice(u, v):
    # 2D cross-section manifold of Calabi-Yau 3-fold
    # u in [0, 2*pi], v in [0, 2*pi]
    n = 5.0
    r = 1.0 + 0.35 * math.cos(n * u) * math.sin(n * v)
    x = r * math.cos(u) * math.sin(v)
    y = r * math.sin(u) * math.sin(v)
    z = 0.45 * math.sin(n * u) * math.cos(n * v)
    return x * 1.4, y * 1.4, z * 1.6

def surf_breather_soliton(u, v):
    # u in [-12, 12], v in [0, 2*pi]
    b = 0.4
    r = 1.0 - b*b
    w = math.sqrt(r)
    cosh_bu = math.cosh(b * u * 0.3)
    sinh_bu = math.sinh(b * u * 0.3)
    cos_wv = math.cos(w * v)
    sin_wv = math.sin(w * v)
    den = b * ((w * cosh_bu)**2 + (b * sin_wv)**2) + 1e-4
    x = -2.0 * w * cosh_bu * (-w * cos_wv * cos_wv + sin_wv * sin_wv) / den
    y = 2.0 * w * cosh_bu * (-w * sin_wv * cos_wv - cos_wv * sin_wv) / den
    z = u * 0.25
    return x * 0.7, y * 0.7, z * 0.7

def surf_hyperbolic_paraboloid(u, v):
    # Saddle surface
    # u in [-1.5, 1.5], v in [-1.5, 1.5]
    x = u
    y = v
    z = (u**2 - v**2) * 0.5
    return x * 0.9, y * 0.9, z * 0.9

def surf_monkey_saddle(u, v):
    # u in [-1.4, 1.4], v in [-1.4, 1.4]
    x = u
    y = v
    z = (u**3 - 3.0 * u * (v**2)) * 0.35
    return x * 0.9, y * 0.9, z * 0.7

def surf_apple_toroid(u, v):
    # u in [0, 2*pi], v in [-pi, pi]
    cu, su = math.cos(u), math.sin(u)
    cv, sv = math.cos(v), math.sin(v)
    r = 4.0 - 2.0 * cv
    x = cu * (r + math.cos(v/2.0))
    y = su * (r + math.cos(v/2.0))
    z = 2.5 * sv + 2.0 * math.sin(v/2.0)
    return x * 0.24, y * 0.24, z * 0.25

def surf_bour_surface(u, v):
    # u in [0, 2*pi], v in [0.1, 1.3]
    r = v
    cu, su = math.cos(u), math.sin(u)
    c2u, s2u = math.cos(2*u), math.sin(2*u)
    c3u2 = math.cos(1.5 * u)
    x = r * cu - 0.5 * (r**2) * c2u
    y = -r * su - 0.5 * (r**2) * s2u
    z = (4.0/3.0) * (r**1.5) * c3u2
    return x * 0.9, y * 0.9, z * 0.9

def surf_schwarz_p_surface(u, v):
    # Triply periodic minimal surface patch
    # u in [-pi, pi], v in [-pi, pi]
    x = u
    y = v
    z = math.sin(u) * math.cos(v) * 1.2
    return x * 0.45, y * 0.45, z * 0.65

def surf_plucker_conoid(u, v):
    # u in [-1.5, 1.5], v in [0, 2*pi]
    n = 2
    x = u * math.cos(v)
    y = u * math.sin(v)
    z = 0.8 * math.sin(n * v)
    return x * 0.9, y * 0.9, z * 1.0

def surf_torus_knot_3_5(u, v):
    # Knot tube (p=3, q=5)
    r_tube = 0.25
    p, q = 3, 5
    r0 = 1.6 + 0.6 * math.cos(q * u)
    x0 = r0 * math.cos(p * u)
    y0 = r0 * math.sin(p * u)
    z0 = -0.7 * math.sin(q * u)
    # Tube
    x = x0 + r_tube * math.cos(v) * math.cos(p * u)
    y = y0 + r_tube * math.cos(v) * math.sin(p * u)
    z = z0 + r_tube * math.sin(v)
    return x * 0.55, y * 0.55, z * 0.7

def surf_wormhole_bridge(u, v):
    # Two gravitational funnels connected by throat
    # u in [0, 2*pi], v in [-1.8, 1.8]
    r = 0.35 + 0.5 * (v**2)
    x = r * math.cos(u)
    y = r * math.sin(u)
    z = v
    return x * 0.8, y * 0.8, z * 0.8

# Registry of 25 core mathematical surface generators
SURFACE_FUNCS = [
    ("boys_surface", "Boy's Surface (Curve.fi)", surf_boys_surface, 0, math.pi, 0, math.pi),
    ("klein_bottle_fig8", "Klein Bottle (Figure-8)", surf_klein_bottle_figure8, 0, 2*math.pi, 0, 2*math.pi),
    ("33rd_singularity_funnel", "33rd Tree Exponential Funnel", surf_33rd_singularity_funnel, 0, 2*math.pi, -1.0, 1.0),
    ("dupin_cyclide", "Dupin Cyclide Inversion", surf_dupin_cyclide, 0, 2*math.pi, 0, 2*math.pi),
    ("enneper_surface", "Enneper Minimal Surface", surf_enneper, -1.5, 1.5, -1.5, 1.5),
    ("cross_cap", "Cross-Cap (RP^2 Immersion)", surf_cross_cap, 0, math.pi, 0, 2*math.pi),
    ("clifford_torus", "Clifford 4D Torus Projection", surf_clifford_torus, 0, 2*math.pi, 0, 2*math.pi),
    ("catenoid_surface", "Catenoid Minimal Surface", surf_catenoid, 0, 2*math.pi, -1.4, 1.4),
    ("helicoid_surface", "Helicoid Ruled Surface", surf_helicoid, -1.4, 1.4, -2.4, 2.4),
    ("kuen_pseudosphere", "Kuen Pseudosphere", surf_kuen_surface, -2.8, 2.8, 0.1, math.pi - 0.1),
    ("dini_twisted_surface", "Dini's Twisted Pseudosphere", surf_dini_surface, 0, 4*math.pi, 0.15, 2.0),
    ("trefoil_tube", "Trefoil Knot Mesh Tube", surf_trefoil_tube, 0, 2*math.pi, 0, 2*math.pi),
    ("mobius_strip", "Möbius Strip 3D Ribbon", surf_mobius_strip, 0, 2*math.pi, -0.6, 0.6),
    ("gabriels_horn", "Gabriel's Horn (Trumpet)", surf_gabriels_horn, 0, 2*math.pi, 0.25, 2.4),
    ("steiner_roman", "Steiner's Roman Surface", surf_steiner_roman, 0, math.pi, 0, math.pi),
    ("calabi_yau_slice", "Calabi-Yau 3-Fold Manifold", surf_calabi_yau_slice, 0, 2*math.pi, 0, 2*math.pi),
    ("breather_soliton", "Breather Soliton Surface", surf_breather_soliton, -8.0, 8.0, 0, 2*math.pi),
    ("hyperbolic_paraboloid", "Hyperbolic Paraboloid Saddle", surf_hyperbolic_paraboloid, -1.4, 1.4, -1.4, 1.4),
    ("monkey_saddle", "Monkey Saddle Manifold", surf_monkey_saddle, -1.3, 1.3, -1.3, 1.3),
    ("apple_toroid", "Apple Toroidal Pinch", surf_apple_toroid, 0, 2*math.pi, -math.pi, math.pi),
    ("bour_minimal", "Bour's Minimal Surface", surf_bour_surface, 0, 2*math.pi, 0.1, 1.3),
    ("schwarz_p_minimal", "Schwarz P Minimal Surface", surf_schwarz_p_surface, -math.pi, math.pi, -math.pi, math.pi),
    ("plucker_conoid", "Plücker's Conoid", surf_plucker_conoid, -1.4, 1.4, 0, 2*math.pi),
    ("torus_knot_3_5", "Torus Knot (3,5) Tube", surf_torus_knot_3_5, 0, 2*math.pi, 0, 2*math.pi),
    ("wormhole_bridge", "Wormhole Einstein-Rosen Bridge", surf_wormhole_bridge, 0, 2*math.pi, -1.6, 1.6)
]

# -----------------------------------------------------------------------------
# 3D RENDERING PIPELINE FOR A SINGLE LOGO
# -----------------------------------------------------------------------------
def render_3d_mesh_logo(index, func_tuple, rx, ry, rz, palette_name, show_grid_box=True, is_dark=True, wire_only=False):
    key, title, func, u_min, u_max, v_min, v_max = func_tuple
    
    # Mesh resolution
    NU, NV = 26, 26
    
    # Compute 3D points
    grid_3d = []
    z_min_val, z_max_val = 999.0, -999.0
    
    for i in range(NU + 1):
        u = u_min + (i / NU) * (u_max - u_min)
        row = []
        for j in range(NV + 1):
            v = v_min + (j / NV) * (v_max - v_min)
            try:
                p = func(u, v)
            except Exception:
                p = (0.0, 0.0, 0.0)
            p_rot = rotate_point(p, rx, ry, rz)
            row.append(p_rot)
            if p_rot[2] < z_min_val: z_min_val = p_rot[2]
            if p_rot[2] > z_max_val: z_max_val = p_rot[2]
        grid_3d.append(row)
        
    z_range = max(1e-4, z_max_val - z_min_val)

    # Build quadrilaterals with Painter's depth sorting
    quads = []
    light_vec = [0.35, 0.65, 0.68]
    l_mag = math.sqrt(sum(x*x for x in light_vec))
    lx, ly, lz = [x/l_mag for x in light_vec]

    for i in range(NU):
        for j in range(NV):
            p0 = grid_3d[i][j]
            p1 = grid_3d[i+1][j]
            p2 = grid_3d[i+1][j+1]
            p3 = grid_3d[i][j+1]
            
            # Average depth
            avg_z = (p0[2] + p1[2] + p2[2] + p3[2]) / 4.0
            
            # Surface normal
            ax, ay, az = p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]
            bx, by, bz = p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]
            nx = ay * bz - az * by
            ny = az * bx - ax * bz
            nz = ax * by - ay * bx
            n_mag = math.sqrt(nx*nx + ny*ny + nz*nz) + 1e-6
            nx, ny, nz = nx/n_mag, ny/n_mag, nz/n_mag
            
            # Shading intensity (ambient + diffuse)
            dot = max(0.0, abs(nx * lx + ny * ly + nz * lz))
            shade = 0.25 + 0.75 * dot
            
            # Projected 2D screen points
            s0 = project_point(p0)
            s1 = project_point(p1)
            s2 = project_point(p2)
            s3 = project_point(p3)
            
            # Normalized height/depth for color
            t_col = (avg_z - z_min_val) / z_range
            
            quads.append({
                "depth": avg_z,
                "pts": [(s0[0], s0[1]), (s1[0], s1[1]), (s2[0], s2[1]), (s3[0], s3[1])],
                "t": t_col,
                "shade": shade
            })

    # Sort quads from back to front (Painter's Algorithm)
    quads.sort(key=lambda q: q["depth"])

    # Theme colors
    bg_color = "#040706" if is_dark else "#F8FAFC"
    border_color = "#162822" if is_dark else "#E2E8F0"
    box_grid_color = "#1F3830" if is_dark else "#CBD5E1"
    box_axis_color = "#2D5246" if is_dark else "#94A3B8"
    
    svg_elements = []
    
    # -------------------------------------------------------------------------
    # Optional 3D Bounding Coordinate Box / Floor & Wall Grid (Image 1 Style)
    # -------------------------------------------------------------------------
    if show_grid_box:
        # Create back walls & floor box in 3D
        box_pts = []
        b_min, b_max = -1.8, 1.8
        # Floor grid lines
        for step in range(7):
            val = b_min + step * (b_max - b_min) / 6.0
            p_a = project_point(rotate_point((b_min, val, b_min), rx, ry, rz))
            p_b = project_point(rotate_point((b_max, val, b_min), rx, ry, rz))
            svg_elements.append(f'<line x1="{p_a[0]:.1f}" y1="{p_a[1]:.1f}" x2="{p_b[0]:.1f}" y2="{p_b[1]:.1f}" stroke="{box_grid_color}" stroke-width="0.8" opacity="0.6"/>')
            p_c = project_point(rotate_point((val, b_min, b_min), rx, ry, rz))
            p_d = project_point(rotate_point((val, b_max, b_min), rx, ry, rz))
            svg_elements.append(f'<line x1="{p_c[0]:.1f}" y1="{p_c[1]:.1f}" x2="{p_d[0]:.1f}" y2="{p_d[1]:.1f}" stroke="{box_grid_color}" stroke-width="0.8" opacity="0.6"/>')
            
        # Back wall grid lines
        for step in range(7):
            val = b_min + step * (b_max - b_min) / 6.0
            p_a = project_point(rotate_point((b_min, b_max, val), rx, ry, rz))
            p_b = project_point(rotate_point((b_max, b_max, val), rx, ry, rz))
            svg_elements.append(f'<line x1="{p_a[0]:.1f}" y1="{p_a[1]:.1f}" x2="{p_b[0]:.1f}" y2="{p_b[1]:.1f}" stroke="{box_grid_color}" stroke-width="0.8" opacity="0.4"/>')
            
        # Box frame bounding axes
        axes = [
            ((-1.8, -1.8, -1.8), (1.8, -1.8, -1.8)),
            ((1.8, -1.8, -1.8), (1.8, 1.8, -1.8)),
            ((-1.8, 1.8, -1.8), (1.8, 1.8, -1.8)),
            ((-1.8, -1.8, -1.8), (-1.8, 1.8, -1.8)),
            ((-1.8, 1.8, -1.8), (-1.8, 1.8, 1.8)),
            ((1.8, 1.8, -1.8), (1.8, 1.8, 1.8)),
        ]
        for a0, a1 in axes:
            pa = project_point(rotate_point(a0, rx, ry, rz))
            pb = project_point(rotate_point(a1, rx, ry, rz))
            svg_elements.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{box_axis_color}" stroke-width="1.2" opacity="0.8"/>')

    # -------------------------------------------------------------------------
    # Render 3D Surface Quadrilateral Facets & Wireframe Grid
    # -------------------------------------------------------------------------
    for q in quads:
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in q["pts"])
        r, g, b = get_color(q["t"], palette_name)
        
        # Apply diffuse/ambient lighting
        s = q["shade"]
        rf, gf, bf = int(r * s), int(g * s), int(b * s)
        
        if wire_only:
            # Curve.fi pure wireframe style (no fill or subtle translucent fill)
            fill_str = "none" if is_dark else "rgba(10, 17, 40, 0.02)"
            stroke_str = "#98FCE4" if is_dark else "#0A1128"
            sw = "0.9"
            op = "0.85"
        else:
            # Matplotlib / Shaded 3D grid style
            fill_str = f"rgb({rf},{gf},{bf})"
            # Dark or contrasting wireframe mesh lines on the surface
            stroke_str = "rgba(0,0,0,0.4)" if palette_name == "rainbow_jet" else "rgba(255,255,255,0.3)"
            sw = "0.75"
            op = "0.96"

        svg_elements.append(f'<polygon points="{pts_str}" fill="{fill_str}" stroke="{stroke_str}" stroke-width="{sw}" opacity="{op}"/>')

    body = "\n    ".join(svg_elements)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <!-- Background Frame -->
    <rect width="512" height="512" rx="32" fill="{bg_color}"/>
    <rect width="512" height="512" rx="32" fill="none" stroke="{border_color}" stroke-width="1.5"/>
    
    <!-- 3D Parametric Mesh Grid Surface -->
    {body}
</svg>'''
    
    fname = f"mesh_{index:03d}_{key}_{palette_name}.svg"
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(svg)
        
    return {
        "id": index,
        "filename": fname,
        "title": f"#{index:03d} • {title}",
        "surface": title,
        "palette": palette_name,
        "svg": svg
    }

# -----------------------------------------------------------------------------
# MAIN GENERATOR: 100 DISTINCT LOGOS
# -----------------------------------------------------------------------------
def build_all_100_mesh_logos():
    print("Generating 100 3D Parametric Mesh Grid Logos...")
    logos = []
    
    # We will produce 100 variations across the 25 mathematical surfaces:
    # 4 distinct variants per surface = 100 total logos!
    # Variant 1: Matplotlib Rainbow/Jet 3D Plot with Box Grid (Image 1 Style)
    # Variant 2: Curve.fi Dark Navy Minimalist Wireframe (Image 2 Style)
    # Variant 3: Hyperliquid Spectral (Mint -> Cyan -> Solana Violet) on Obsidian Void
    # Variant 4: Isometric HUD Telemetry with Neon Lines
    
    idx = 1
    for surf_tuple in SURFACE_FUNCS:
        key, title = surf_tuple[0], surf_tuple[1]
        
        # Variant 1: Matplotlib Rainbow Plot with Grid Box (Image 1)
        v1 = render_3d_mesh_logo(
            index=idx,
            func_tuple=surf_tuple,
            rx=-32, ry=42, rz=12,
            palette_name="rainbow_jet",
            show_grid_box=True,
            is_dark=False,
            wire_only=False
        )
        v1["category"] = "Rainbow Differential Plot"
        logos.append(v1)
        idx += 1
        
        # Variant 2: Curve.fi Signature Wireframe Mesh (Image 2)
        v2 = render_3d_mesh_logo(
            index=idx,
            func_tuple=surf_tuple,
            rx=-24, ry=38, rz=5,
            palette_name="curve_navy_wire",
            show_grid_box=False,
            is_dark=False,
            wire_only=True
        )
        v2["category"] = "Curve.fi Minimal Wireframe"
        logos.append(v2)
        idx += 1
        
        # Variant 3: Hyperliquid Spectral on Dark Obsidian
        v3 = render_3d_mesh_logo(
            index=idx,
            func_tuple=surf_tuple,
            rx=-38, ry=55, rz=-15,
            palette_name="hyperliquid_spectral",
            show_grid_box=True,
            is_dark=True,
            wire_only=False
        )
        v3["category"] = "Hyperliquid Spectral Mesh"
        logos.append(v3)
        idx += 1
        
        # Variant 4: Neon Cyber HUD Wireframe
        v4 = render_3d_mesh_logo(
            index=idx,
            func_tuple=surf_tuple,
            rx=-15, ry=-45, rz=20,
            palette_name="aurora_neon",
            show_grid_box=True,
            is_dark=True,
            wire_only=True
        )
        v4["category"] = "Cyber HUD Wireframe"
        logos.append(v4)
        idx += 1

    print(f"Generated {len(logos)} distinct 3D mesh logos in {OUTPUT_DIR}")
    return logos

# -----------------------------------------------------------------------------
# DEDICATED SHOWCASE HTML (showcase_3d_mesh_100.html)
# -----------------------------------------------------------------------------
def build_mesh_showcase(logos):
    categories = ["All 100 Logos", "Rainbow Differential Plot", "Curve.fi Minimal Wireframe", "Hyperliquid Spectral Mesh", "Cyber HUD Wireframe"]
    
    cat_buttons = []
    for cat in categories:
        val = "all" if cat == "All 100 Logos" else cat
        active_cls = "active" if val == "all" else ""
        cat_buttons.append(f'<button class="filter-btn {active_cls}" onclick="filterMesh(\'{val}\', this)">{cat}</button>')
    cat_nav = "\n".join(cat_buttons)
    
    cards_html = []
    for l in logos:
        ta_id = f"copy_{l['filename'].replace('.', '_')}"
        cards_html.append(f'''
        <div class="mesh-card" data-category="{l['category']}">
            <div class="mesh-preview">
                {l['svg']}
            </div>
            <div class="mesh-meta">
                <div class="mesh-title">{l['title']}</div>
                <div class="mesh-badge">{l['category']}</div>
                <div class="mesh-actions">
                    <a href="mesh-3d-100/{l['filename']}" download class="btn btn-primary">Download SVG</a>
                    <button class="btn btn-secondary" onclick="copySvgCode('{ta_id}')">Copy SVG</button>
                    <textarea id="{ta_id}" style="display:none;">{l['svg']}</textarea>
                </div>
            </div>
        </div>''')
    cards_grid = "\n".join(cards_html)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperSettle • 100 3D Parametric Mesh Grid Logos</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #030605;
            --surface: #091210;
            --surface-border: #162622;
            --mint: #98FCE4;
            --cyan: #00E5FF;
            --solana: #9945FF;
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --font-mono: 'JetBrains Mono', 'Space Mono', monospace;
            --font-sans: 'Space Grotesk', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text-primary);
            font-family: var(--font-mono);
            padding: 48px 24px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1440px; margin: 0 auto; }}
        
        header {{
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 36px;
            margin-bottom: 36px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(152, 252, 228, 0.1);
            color: var(--mint);
            border: 1px solid rgba(152, 252, 228, 0.3);
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 16px;
        }}
        h1 {{
            font-family: var(--font-sans);
            font-size: 46px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #FFFFFF 40%, var(--mint) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            color: var(--text-secondary);
            font-size: 16px;
            max-width: 900px;
        }}
        
        /* Filter Bar */
        .filter-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 36px;
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 20px;
        }}
        .filter-btn {{
            background: var(--surface);
            color: var(--text-secondary);
            border: 1px solid var(--surface-border);
            padding: 8px 18px;
            border-radius: 999px;
            font-size: 13px;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--mint);
            color: #030605;
            border-color: var(--mint);
            font-weight: 700;
        }}
        
        /* Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
        }}
        .mesh-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 16px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }}
        .mesh-card:hover {{
            transform: translateY(-4px);
            border-color: var(--cyan);
            box-shadow: 0 12px 30px -5px rgba(0, 229, 255, 0.15);
        }}
        .mesh-preview {{
            aspect-ratio: 1 / 1;
            background: #000000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px;
        }}
        .mesh-meta {{
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex-grow: 1;
        }}
        .mesh-title {{
            font-size: 13px;
            font-weight: 700;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .mesh-badge {{
            font-size: 10.5px;
            color: var(--mint);
            background: rgba(152, 252, 228, 0.08);
            display: inline-block;
            align-self: flex-start;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .mesh-actions {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 6px;
        }}
        
        .btn {{
            padding: 8px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 11px;
            font-family: var(--font-mono);
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: none;
            transition: opacity 0.15s;
        }}
        .btn-primary {{
            background: var(--mint);
            color: #030605;
        }}
        .btn-primary:hover {{ opacity: 0.9; }}
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.08);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.16);
        }}
        
        /* Toast */
        #toast {{
            position: fixed;
            bottom: 32px;
            right: 32px;
            background: var(--mint);
            color: #030605;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            opacity: 0;
            transform: translateY(16px);
            transition: opacity 0.2s, transform 0.2s;
            pointer-events: none;
            z-index: 9999;
        }}
        #toast.show {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">CURVE FINANCE × HYPERLIQUID 3D DIFFERENTIAL GEOMETRY SUITE</span>
            <h1>100 3D Parametric Mesh Grid Logos</h1>
            <p class="subtitle">100 mathematically authentic 3D wireframe mesh surfaces—featuring the exact Boy's Surface used by Curve Finance, the 33rd Tree Exponential Funnel in 3D, and Matplotlib-style rainbow differential geometry plots with 3D coordinate bounding grids.</p>
        </header>

        <div class="filter-bar">
            {cat_nav}
        </div>

        <div class="grid" id="meshGrid">
            {cards_grid}
        </div>
    </div>

    <div id="toast">SVG Vector Code Copied!</div>

    <script>
        function filterMesh(category, btn) {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const cards = document.querySelectorAll('.mesh-card');
            cards.forEach(card => {{
                if (category === 'all' || card.getAttribute('data-category') === category) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function copySvgCode(id) {{
            const code = document.getElementById(id).value;
            navigator.clipboard.writeText(code).then(() => {{
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            }});
        }}
    </script>
</body>
</html>'''

    with open(SHOWCASE_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated 3D mesh showcase at {SHOWCASE_HTML}")

if __name__ == "__main__":
    logos = build_all_100_mesh_logos()
    build_mesh_showcase(logos)
    print("All 100 3D Parametric Mesh Grid logos and showcase generated successfully!")

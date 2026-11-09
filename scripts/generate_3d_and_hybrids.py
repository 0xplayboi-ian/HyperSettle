#!/usr/bin/env python3
"""
HyperSettle - Advanced 3D & Hybrid Brand Generator
1. 10 Redesigned 33rd Labs Black Hole Concepts: Same exact exponential plunge / tensor arbor, but 10 completely distinct 3D / volumetric / fluid rendering styles.
2. 25 Unique Hybrid Logos: Merging the 33rd Tree blackhole / singularity concept with Hyperliquid's fluid droplet & iridescent multi-color gradient aesthetic.
3. Dedicated Interactive HTML Showcase: showcase_3d_and_hybrids.html (Preserving all previous showcases untouched).
"""

import os
import math

BASE_DIR = "/Users/ianmora/Desktop/Projects/HyperSettle"
BH10_DIR = os.path.join(BASE_DIR, "branding", "blackhole-10")
HYBRID25_DIR = os.path.join(BASE_DIR, "branding", "hybrid-25")
SHOWCASE_HTML = os.path.join(BASE_DIR, "branding", "showcase_3d_and_hybrids.html")

os.makedirs(BH10_DIR, exist_ok=True)
os.makedirs(HYBRID25_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# Mathematical Formula for 33rd Tree Exponential Plunge (#06)
# -------------------------------------------------------------------------
CX, CY_THROAT = 256, 256
Y_TOP = 80
Y_BOTTOM = 432
H_TOP = CY_THROAT - Y_TOP
H_BOT = Y_BOTTOM - CY_THROAT

def r_exp(y):
    dist = abs(y - CY_THROAT)
    h = H_TOP if y < CY_THROAT else H_BOT
    norm = min(1.0, dist / h)
    return 3.0 + 172.0 * ((math.exp(3.8 * norm) - 1.0) / (math.exp(3.8) - 1.0))

# Sample points for meridians
def get_meridian_pts(frac, side, steps=60):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        y = Y_TOP + t * (Y_BOTTOM - Y_TOP)
        r = r_exp(y) * frac
        x = CX + side * r
        pts.append((x, y))
    return pts

def pts_to_d(pts):
    return f"M {pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(f"L {p[0]:.1f} {p[1]:.1f}" for p in pts[1:])

# Standard color tokens
MINT = "#98FCE4"
CYAN = "#00E5FF"
SOLANA = "#9945FF"
TEAL_DEEP = "#072723"
MAGENTA = "#FF007A"
BLUE = "#0070F3"
LIME = "#10B981"
GOLD = "#FFD600"

# =========================================================================
# PART 1: 10 REDESIGNED 33RD LABS BLACK HOLE CONCEPTS
# =========================================================================
def generate_10_blackhole_concepts():
    concepts = []

    # ---------------------------------------------------------------------
    # 01. 3D Volumetric Fluid Shading (Hyperliquid Style)
    # ---------------------------------------------------------------------
    svg_01 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh01_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#0E2420" stop-opacity="0.9"/>
            <stop offset="60%" stop-color="#050B09"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="fluidFunnelL" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="40%" stop-color="#00E5FF"/>
            <stop offset="80%" stop-color="#0D4B41"/>
            <stop offset="100%" stop-color="#000000"/>
        </linearGradient>
        <linearGradient id="fluidFunnelR" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#00E5FF"/>
            <stop offset="45%" stop-color="#9945FF"/>
            <stop offset="85%" stop-color="#2D114D"/>
            <stop offset="100%" stop-color="#000000"/>
        </linearGradient>
        <linearGradient id="specularGlow" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9"/>
            <stop offset="40%" stop-color="#98FCE4" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#00E5FF" stop-opacity="0.0"/>
        </linearGradient>
        <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh01_bg)"/>
    
    <!-- Outer 3D Volumetric Fluid Funnel -->
    <!-- Left Surface Mesh -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="url(#fluidFunnelL)" opacity="0.95"/>
    <!-- Right Surface Mesh -->
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="url(#fluidFunnelR)" opacity="0.9"/>
    
    <!-- Inner Volumetric Shadow Cavity (Creating 3D Depth) -->
    <path d="{pts_to_d(get_meridian_pts(0.48, -1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="#000000" opacity="0.85"/>
    <path d="{pts_to_d(get_meridian_pts(0.48, 1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="#000000" opacity="0.75"/>
    
    <!-- Top & Bottom Elliptical Rims -->
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="175" ry="38" fill="#072723" stroke="#98FCE4" stroke-width="3" filter="url(#softGlow)"/>
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="175" ry="38" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.8"/>
    <ellipse cx="{CX}" cy="{Y_BOTTOM}" rx="175" ry="38" fill="#130826" stroke="#9945FF" stroke-width="3"/>
    
    <!-- Specular Ridge Lines (3D Lighting from Upper-Left) -->
    <path d="{pts_to_d(get_meridian_pts(0.85, -1))}" fill="none" stroke="url(#specularGlow)" stroke-width="3.5" stroke-linecap="round"/>
    <path d="{pts_to_d(get_meridian_pts(0.68, 1))}" fill="none" stroke="#9945FF" stroke-width="2.5" opacity="0.8" stroke-linecap="round"/>
    
    <!-- The Ultra-Narrow Singularity Throat (3.0px) -->
    <line x1="{CX}" y1="230" x2="{CX}" y2="282" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="5" ry="3" fill="#FFFFFF" filter="url(#softGlow)"/>
    
    <!-- Horizontal Floating Energy Ribbons -->
    <ellipse cx="{CX}" cy="140" rx="90" ry="20" fill="none" stroke="#98FCE4" stroke-width="2" stroke-dasharray="4 6" opacity="0.7"/>
    <ellipse cx="{CX}" cy="370" rx="100" ry="22" fill="none" stroke="#00E5FF" stroke-width="2" stroke-dasharray="6 8" opacity="0.7"/>
</svg>'''
    concepts.append(("bh_01_3d_volumetric_fluid.svg", svg_01, "01 • 3D Volumetric Fluid Shading", "Hyperliquid-inspired smooth volumetric gradient lighting with deep ambient cavity."))

    # ---------------------------------------------------------------------
    # 02. Refractive Chromatic Glass / Prismatic Dispersion
    # ---------------------------------------------------------------------
    svg_02 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh02_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#180B22"/>
            <stop offset="60%" stop-color="#08030C"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="prismRed" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FF0055" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#FF5500" stop-opacity="0.2"/>
        </linearGradient>
        <linearGradient id="prismCyan" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#00F5D4" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#0070F3" stop-opacity="0.2"/>
        </linearGradient>
        <linearGradient id="prismViolet" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#9945FF" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#FF007A" stop-opacity="0.2"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh02_bg)"/>
    
    <!-- Chromatic Aberration Dispersion Offset Layers -->
    <!-- Red Dispersion Layer -->
    <g transform="translate(-4, 0)">
        <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="url(#prismRed)" stroke-width="4.5" stroke-linecap="round"/>
        <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="url(#prismRed)" stroke-width="4.5" stroke-linecap="round"/>
        <ellipse cx="{CX}" cy="{Y_TOP}" rx="175" ry="38" fill="none" stroke="#FF0055" stroke-width="2" opacity="0.6"/>
    </g>
    <!-- Cyan Dispersion Layer -->
    <g transform="translate(4, 0)">
        <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="url(#prismCyan)" stroke-width="4.5" stroke-linecap="round"/>
        <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="url(#prismCyan)" stroke-width="4.5" stroke-linecap="round"/>
        <ellipse cx="{CX}" cy="{Y_TOP}" rx="175" ry="38" fill="none" stroke="#00F5D4" stroke-width="2" opacity="0.6"/>
    </g>
    <!-- White Master Glass Core Layer -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Internal Refractive Ribbons -->
    <path d="{pts_to_d(get_meridian_pts(0.65, -1))}" fill="none" stroke="url(#prismViolet)" stroke-width="3" opacity="0.85"/>
    <path d="{pts_to_d(get_meridian_pts(0.65, 1))}" fill="none" stroke="url(#prismCyan)" stroke-width="3" opacity="0.85"/>
    <path d="{pts_to_d(get_meridian_pts(0.35, -1))}" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.6"/>
    <path d="{pts_to_d(get_meridian_pts(0.35, 1))}" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.6"/>
    
    <!-- Caustic Rings -->
    <ellipse cx="{CX}" cy="130" rx="100" ry="22" fill="none" stroke="#98FCE4" stroke-width="2" opacity="0.8"/>
    <ellipse cx="{CX}" cy="180" rx="42" ry="9" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.9"/>
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="12" ry="3" fill="#FFFFFF"/>
    <ellipse cx="{CX}" cy="330" rx="42" ry="9" fill="none" stroke="#FF007A" stroke-width="2" opacity="0.8"/>
    <ellipse cx="{CX}" cy="380" rx="100" ry="22" fill="none" stroke="#9945FF" stroke-width="2" opacity="0.8"/>
</svg>'''
    concepts.append(("bh_02_chromatic_glass_dispersion.svg", svg_02, "02 • Chromatic Glass Dispersion", "Optical glass refractive edges with prismatic RGB dispersion and caustic rings."))

    # ---------------------------------------------------------------------
    # 03. Gargantua Relativistic Accretion Disk (Interstellar Physics)
    # ---------------------------------------------------------------------
    svg_03 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh03_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#141E1C"/>
            <stop offset="60%" stop-color="#060A09"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="accretionGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="30%" stop-color="#00E5FF"/>
            <stop offset="70%" stop-color="#FF8A00"/>
            <stop offset="100%" stop-color="#FF0055"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh03_bg)"/>
    
    <!-- 1. Gravitationally Lensed Back Halo (The back of the disk arched over top & bottom) -->
    <path d="M 70 {CY_THROAT} C 70 60 442 60 442 {CY_THROAT}" fill="none" stroke="url(#accretionGrad)" stroke-width="16" stroke-linecap="round" opacity="0.85"/>
    <path d="M 90 {CY_THROAT} C 90 450 422 450 422 {CY_THROAT}" fill="none" stroke="url(#accretionGrad)" stroke-width="14" stroke-linecap="round" opacity="0.75"/>
    
    <!-- 2. The 33rd Tree Exponential Singular Funnel (Void Silhouette) -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="#000000"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="#000000"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="#98FCE4" stroke-width="3"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="#00E5FF" stroke-width="3"/>
    
    <!-- 3. Foreground Equatorial Accretion Disk (Cutting horizontally across the front) -->
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="220" ry="24" fill="none" stroke="url(#accretionGrad)" stroke-width="18" stroke-linecap="round"/>
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="220" ry="24" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.9"/>
    
    <!-- 4. Pure Black Singularity Sphere at Throat -->
    <circle cx="{CX}" cy="{CY_THROAT}" r="22" fill="#000000" stroke="#FFFFFF" stroke-width="2"/>
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="6" ry="2" fill="#98FCE4"/>
</svg>'''
    concepts.append(("bh_03_gargantua_relativistic_disk.svg", svg_03, "03 • Gargantua Relativistic Accretion", "True gravitational lensing where the equatorial accretion ring loops over and under the black hole."))

    # ---------------------------------------------------------------------
    # 04. 3D Isometric Topological Gravity-Well Mesh
    # ---------------------------------------------------------------------
    svg_04 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh04_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#041F1A"/>
            <stop offset="60%" stop-color="#020C0A"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh04_bg)"/>
    
    <!-- 12 Isometric Curved Meridians -->
    <g stroke="#98FCE4" stroke-linecap="round">'''
    meridians = [1.0, 0.85, 0.70, 0.55, 0.40, 0.25, 0.12]
    for m in meridians:
        sw = 2.4 if m == 1.0 else 1.2
        op = 0.9 if m == 1.0 else 0.45
        svg_04 += f'''
        <path d="{pts_to_d(get_meridian_pts(m, -1))}" fill="none" stroke-width="{sw}" opacity="{op}"/>
        <path d="{pts_to_d(get_meridian_pts(m, 1))}" fill="none" stroke-width="{sw}" opacity="{op}"/>'''
    
    # Latitude Rings descending into the well
    rings = [80, 100, 130, 170, 210, 235, 256, 277, 302, 342, 382, 412, 432]
    for y in rings:
        r = r_exp(y)
        ry = max(1.5, r * 0.24)
        sw = 2.0 if y in [80, 432, 256] else 1.0
        op = 0.9 if y in [80, 432, 256] else 0.5
        svg_04 += f'''
        <ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="#00E5FF" stroke-width="{sw}" opacity="{op}"/>'''
        # Add grid intersection dots
        svg_04 += f'''
        <circle cx="{CX - r:.1f}" cy="{y}" r="2.5" fill="#FFFFFF"/>
        <circle cx="{CX + r:.1f}" cy="{y}" r="2.5" fill="#FFFFFF"/>'''

    svg_04 += f'''
    </g>
    <!-- Central Metric Axis -->
    <line x1="{CX}" y1="50" x2="{CX}" y2="462" stroke="#FFFFFF" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8"/>
    <circle cx="{CX}" cy="{CY_THROAT}" r="4" fill="#FFFFFF"/>
</svg>'''
    concepts.append(("bh_04_isometric_gravity_mesh.svg", svg_04, "04 • Isometric Gravity-Well Mesh", "Full 3D topological coordinate grid representing spacetime curvature into the singularity."))

    # ---------------------------------------------------------------------
    # 05. Cybernetic Particle Kinetic Vortex
    # ---------------------------------------------------------------------
    svg_05 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh05_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#120A24"/>
            <stop offset="60%" stop-color="#06030C"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="particleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh05_bg)"/>
    
    <!-- Base Vector Envelope -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="#374151" stroke-width="1.2" stroke-dasharray="3 3"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="#374151" stroke-width="1.2" stroke-dasharray="3 3"/>
    
    <!-- Swarming Kinetic Acceleration Streams -->'''
    # Generate particles along the curve
    for i in range(70):
        t = i / 69
        y = Y_TOP + t * (Y_BOTTOM - Y_TOP)
        r = r_exp(y)
        side = -1 if i % 2 == 0 else 1
        x = CX + side * r
        rad = 1.5 + (1.0 - abs(t - 0.5) * 2) * 3.5
        col = MINT if t < 0.35 else (CYAN if t < 0.65 else SOLANA)
        svg_05 += f'''
        <circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{col}" opacity="{0.6 + rad*0.08}"/>'''
        if i % 3 == 0:
            # Orbital ring stream
            ry = max(1.5, r * 0.22)
            svg_05 += f'''
            <ellipse cx="{CX}" cy="{y:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="{col}" stroke-width="0.8" stroke-dasharray="{3+i%5} {4+i%4}" opacity="0.5"/>'''

    svg_05 += f'''
    <!-- Singularity Photon Sphere Core -->
    <circle cx="{CX}" cy="{CY_THROAT}" r="12" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
    <circle cx="{CX}" cy="{CY_THROAT}" r="5" fill="#98FCE4"/>
</svg>'''
    concepts.append(("bh_05_cybernetic_particle_vortex.svg", svg_05, "05 • Cybernetic Particle Kinetic Vortex", "Quantized photon nodes and relativistic matter packets accelerating into the event horizon."))

    # ---------------------------------------------------------------------
    # 06. Liquid Chrome & Obsidian Monolith
    # ---------------------------------------------------------------------
    svg_06 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh06_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#1E1E24"/>
            <stop offset="70%" stop-color="#08080A"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="chromeLeft" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FFFFFF"/>
            <stop offset="25%" stop-color="#E2E8F0"/>
            <stop offset="60%" stop-color="#475569"/>
            <stop offset="85%" stop-color="#0F172A"/>
            <stop offset="100%" stop-color="#000000"/>
        </linearGradient>
        <linearGradient id="chromeRight" x1="100%" y1="0%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="#FFFFFF"/>
            <stop offset="25%" stop-color="#E2E8F0"/>
            <stop offset="60%" stop-color="#475569"/>
            <stop offset="85%" stop-color="#0F172A"/>
            <stop offset="100%" stop-color="#000000"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh06_bg)"/>
    
    <!-- Heavy Solid Metallic Body -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="url(#chromeLeft)"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))} L {CX} {Y_BOTTOM} L {CX} {Y_TOP} Z" fill="url(#chromeRight)"/>
    
    <!-- Mirror Highlights Along Rim -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    
    <!-- Top & Bottom Heavy Chrome Flanges -->
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="175" ry="38" fill="#1E293B" stroke="#FFFFFF" stroke-width="3"/>
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="145" ry="30" fill="#000000"/>
    <ellipse cx="{CX}" cy="{Y_BOTTOM}" rx="175" ry="38" fill="#1E293B" stroke="#FFFFFF" stroke-width="3"/>
    <ellipse cx="{CX}" cy="{Y_BOTTOM}" rx="145" ry="30" fill="#000000"/>
    
    <!-- Vertical Polished Ingot Spine -->
    <line x1="{CX}" y1="{Y_TOP}" x2="{CX}" y2="{Y_BOTTOM}" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.6"/>
    <rect x="{CX-4}" y="{CY_THROAT-15}" width="8" height="30" rx="3" fill="#FFFFFF"/>
</svg>'''
    concepts.append(("bh_06_liquid_chrome_monolith.svg", svg_06, "06 • Liquid Chrome &amp; Obsidian Monolith", "Heavy metallic mercury finish with high specular reflection and brushed platinum flanges."))

    # ---------------------------------------------------------------------
    # 07. Neon Ribbon Strip (Möbius Flow)
    # ---------------------------------------------------------------------
    svg_07 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh07_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#14061A"/>
            <stop offset="60%" stop-color="#07020A"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="mobiusGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="25%" stop-color="#00E5FF"/>
            <stop offset="60%" stop-color="#9945FF"/>
            <stop offset="100%" stop-color="#FF007A"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh07_bg)"/>
    
    <!-- Continuous 3D Flowing Möbius Ribbon following the Exponential Contour -->
    <!-- Front Upper Ribbon -->
    <path d="M 82 {Y_TOP} C 120 160 220 220 {CX} {CY_THROAT} C 290 290 390 350 430 {Y_BOTTOM}" 
          fill="none" stroke="url(#mobiusGrad)" stroke-width="26" stroke-linecap="round"/>
    <!-- Rear Counter Ribbon (Twisting Behind) -->
    <path d="M 430 {Y_TOP} C 390 160 290 220 {CX} {CY_THROAT} C 220 290 120 350 82 {Y_BOTTOM}" 
          fill="none" stroke="url(#mobiusGrad)" stroke-width="16" stroke-linecap="round" opacity="0.6"/>
          
    <!-- Core Shimmer Wire -->
    <path d="M 82 {Y_TOP} C 120 160 220 220 {CX} {CY_THROAT} C 290 290 390 350 430 {Y_BOTTOM}" 
          fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
          
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="174" ry="36" fill="none" stroke="#98FCE4" stroke-width="2" opacity="0.8"/>
    <ellipse cx="{CX}" cy="{Y_BOTTOM}" rx="174" ry="36" fill="none" stroke="#FF007A" stroke-width="2" opacity="0.8"/>
    <circle cx="{CX}" cy="{CY_THROAT}" r="14" fill="#FFFFFF"/>
</svg>'''
    concepts.append(("bh_07_mobius_continuous_ribbon.svg", svg_07, "07 • Neon Ribbon Strip (Möbius Flow)", "Continuous 3D twisting ribbon wrapping 180 degrees through the central singularity throat."))

    # ---------------------------------------------------------------------
    # 08. Stepped Topographical Elevation Contour
    # ---------------------------------------------------------------------
    svg_08 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh08_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#0A1815"/>
            <stop offset="60%" stop-color="#030807"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh08_bg)"/>
    
    <!-- Terraced Elevation Contour Slices -->'''
    step_ys = [80, 110, 150, 200, 240, 256, 272, 312, 362, 402, 432]
    colors_step = ["#164E44", "#115E59", "#0F766E", "#0D9488", "#14B8A6", "#98FCE4", "#14B8A6", "#0D9488", "#0F766E", "#115E59", "#164E44"]
    for idx, y in enumerate(step_ys):
        r = r_exp(y)
        ry = max(2.0, r * 0.25)
        c = colors_step[idx]
        svg_08 += f'''
        <ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="2.5"/>
        <line x1="{CX-r:.1f}" y1="{y}" x2="{CX+r:.1f}" y2="{y}" stroke="{c}" stroke-width="0.8" opacity="0.3"/>'''

    svg_08 += f'''
    <line x1="{CX}" y1="60" x2="{CX}" y2="452" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="4 4"/>
    <circle cx="{CX}" cy="{CY_THROAT}" r="5" fill="#FFFFFF"/>
</svg>'''
    concepts.append(("bh_08_stepped_topographical_contour.svg", svg_08, "08 • Stepped Topographical Contour", "Terraced architectural elevation planes descending step-by-step into the singularity well."))

    # ---------------------------------------------------------------------
    # 09. Relativistic Plasma Jet Funnel
    # ---------------------------------------------------------------------
    svg_09 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh09_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#1C1808"/>
            <stop offset="60%" stop-color="#0C0A03"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="plasmaBeam" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#FFE600"/>
            <stop offset="25%" stop-color="#FF5500"/>
            <stop offset="50%" stop-color="#FFFFFF"/>
            <stop offset="75%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#98FCE4"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh09_bg)"/>
    
    <!-- Blazing Vertical Relativistic Plasma Jet -->
    <line x1="{CX}" y1="20" x2="{CX}" y2="492" stroke="url(#plasmaBeam)" stroke-width="8" stroke-linecap="round"/>
    <line x1="{CX}" y1="20" x2="{CX}" y2="492" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Magnetic Meridian Flux Lines -->
    <path d="{pts_to_d(get_meridian_pts(1.0, -1))}" fill="none" stroke="#FFE600" stroke-width="3" stroke-linecap="round"/>
    <path d="{pts_to_d(get_meridian_pts(1.0, 1))}" fill="none" stroke="#FFE600" stroke-width="3" stroke-linecap="round"/>
    <path d="{pts_to_d(get_meridian_pts(0.65, -1))}" fill="none" stroke="#FF5500" stroke-width="2.2" opacity="0.8"/>
    <path d="{pts_to_d(get_meridian_pts(0.65, 1))}" fill="none" stroke="#FF5500" stroke-width="2.2" opacity="0.8"/>
    <path d="{pts_to_d(get_meridian_pts(0.35, -1))}" fill="none" stroke="#00E5FF" stroke-width="1.8" opacity="0.7"/>
    <path d="{pts_to_d(get_meridian_pts(0.35, 1))}" fill="none" stroke="#00E5FF" stroke-width="1.8" opacity="0.7"/>
    
    <!-- Toroidal Magnetic Confinement Rings -->
    <ellipse cx="{CX}" cy="{Y_TOP}" rx="174" ry="38" fill="none" stroke="#FFE600" stroke-width="2.5"/>
    <ellipse cx="{CX}" cy="180" rx="42" ry="9" fill="none" stroke="#FF5500" stroke-width="2"/>
    <ellipse cx="{CX}" cy="{CY_THROAT}" rx="16" ry="5" fill="#FFFFFF" stroke="#FFE600" stroke-width="3"/>
    <ellipse cx="{CX}" cy="330" rx="42" ry="9" fill="none" stroke="#00E5FF" stroke-width="2"/>
    <ellipse cx="{CX}" cy="{Y_BOTTOM}" rx="174" ry="38" fill="none" stroke="#98FCE4" stroke-width="2.5"/>
</svg>'''
    concepts.append(("bh_09_relativistic_plasma_jets.svg", svg_09, "09 • Relativistic Plasma Jets", "High-energy relativistic plasma beam erupting through the singularity axis with magnetic confinement."))

    # ---------------------------------------------------------------------
    # 10. Holographic Quantum Lattice
    # ---------------------------------------------------------------------
    svg_10 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="bh10_bg" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#02141C"/>
            <stop offset="60%" stop-color="#01080C"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#bh10_bg)"/>
    
    <!-- Fine Multi-Layered Laser Interference Curves -->'''
    fractions = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    for idx, fr in enumerate(fractions):
        col = MINT if idx % 2 == 0 else CYAN
        svg_10 += f'''
        <path d="{pts_to_d(get_meridian_pts(fr, -1))}" fill="none" stroke="{col}" stroke-width="1.2" opacity="{0.9 - idx*0.06}"/>
        <path d="{pts_to_d(get_meridian_pts(fr, 1))}" fill="none" stroke="{col}" stroke-width="1.2" opacity="{0.9 - idx*0.06}"/>'''
        
    for y in [80, 120, 160, 200, 230, 256, 282, 312, 352, 392, 432]:
        r = r_exp(y)
        ry = max(1.5, r * 0.22)
        svg_10 += f'''
        <ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="#FFFFFF" stroke-width="0.8" opacity="0.6"/>'''

    svg_10 += f'''
    <!-- Reticle Datum Crosshairs -->
    <line x1="80" y1="{CY_THROAT}" x2="432" y2="{CY_THROAT}" stroke="#00E5FF" stroke-width="1.5" stroke-dasharray="4 6"/>
    <line x1="{CX}" y1="50" x2="{CX}" y2="462" stroke="#00E5FF" stroke-width="1.5" stroke-dasharray="4 6"/>
    <circle cx="{CX}" cy="{CY_THROAT}" r="6" fill="#98FCE4"/>
</svg>'''
    concepts.append(("bh_10_holographic_quantum_lattice.svg", svg_10, "10 • Holographic Quantum Lattice", "High-density laser interference curves creating a 3D hologram projection effect."))

    for fname, svg_str, title, desc in concepts:
        fpath = os.path.join(BH10_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_str)

    print(f"Generated {len(concepts)} 3D blackhole concepts in {BH10_DIR}")
    return concepts

# =========================================================================
# PART 2: 25 UNIQUE HYBRID LOGOS (33RD TREE BLACKHOLE + HYPERLIQUID)
# =========================================================================
def generate_25_hybrids():
    hybrids = []
    
    # Helper to generate unique designs
    def add_hybrid(num, key, name, desc, inner_svg):
        gid1 = f"hyb_grad_{num}_a"
        gid2 = f"hyb_grad_{num}_b"
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <radialGradient id="hyb_bg_{num}" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#081816"/>
            <stop offset="60%" stop-color="#020807"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="{gid1}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="45%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
        <linearGradient id="{gid2}" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#FF007A"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#98FCE4"/>
        </linearGradient>
    </defs>
    <rect width="512" height="512" rx="36" fill="url(#hyb_bg_{num})"/>
    <rect width="512" height="512" rx="36" fill="none" stroke="#162E29" stroke-width="1.5"/>
    
    <!-- Hybrid Vector Mark -->
    {inner_svg}
</svg>'''
        fname = f"hybrid_{num:02d}_{key}.svg"
        fpath = os.path.join(HYBRID25_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg)
        hybrids.append((fname, svg, f"Hybrid {num:02d} • {name}", desc))

    # 01. Fluid Teardrop with Singularity Core
    h01 = f'''<g transform="translate(256, 256)">
        <path d="M 0 -170 C 80 -60 140 30 140 110 C 140 185 80 230 0 230 C -80 230 -140 185 -140 110 C -140 30 -80 -60 0 -170 Z" 
              fill="url(#hyb_grad_1_a)"/>
        <!-- Internal Gravitational Black Hole Void -->
        <path d="M 0 -70 C 35 -20 60 20 60 65 C 60 100 35 125 0 125 C -35 125 -60 100 -60 65 C -60 20 -35 -20 0 -70 Z" 
              fill="#000000"/>
        <!-- Exponential Plunge Wire inside Droplet -->
        <path d="M -50 -10 C -10 30 -2 55 0 65 C 2 55 10 30 50 -10" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
        <circle cx="0" cy="65" r="5" fill="#98FCE4"/>
        <!-- Specular Bubble Reflection -->
        <ellipse cx="-45" cy="50" rx="18" ry="36" transform="rotate(-25 -45 50)" fill="#FFFFFF" opacity="0.35"/>
    </g>'''
    add_hybrid(1, "droplet_singularity_core", "Droplet Singularity Core", "Hyperliquid fluid teardrop harboring an internal 3D black hole gravity well.", h01)

    # 02. Vortex Liquid Funnel
    h02 = f'''<g transform="translate(256, 256)">
        <!-- 3 Swirling Fluid Arms -->
        <path d="M 0 0 C 60 -120 160 -140 200 -80 C 240 -20 180 80 120 110 C 60 140 10 90 0 0 Z" fill="url(#hyb_grad_2_a)" opacity="0.9"/>
        <path d="M 0 0 C -120 -60 -140 60 -80 120 C -20 180 80 160 110 80 C 140 0 90 -40 0 0 Z" fill="url(#hyb_grad_2_b)" opacity="0.85"/>
        <path d="M 0 0 C 60 120 -60 160 -120 100 C -180 40 -120 -60 -40 -100 C 40 -140 80 -60 0 0 Z" fill="url(#hyb_grad_2_a)" opacity="0.8"/>
        <!-- Deep Black Hole Center Drain -->
        <circle cx="0" cy="0" r="32" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="0" r="10" fill="#98FCE4"/>
    </g>'''
    add_hybrid(2, "vortex_liquid_funnel", "Vortex Liquid Funnel", "Multi-armed iridescent fluid cyclone coiling into an event horizon drain.", h02)

    # 03. Möbius Liquid Plunge
    h03 = f'''<g transform="translate(256, 256)">
        <!-- Fluid Figure-8 looping through singularity -->
        <path d="M -90 -80 C -150 -80 -150 80 -90 80 C -30 80 30 -80 90 -80 C 150 -80 150 80 90 80 C 30 80 -30 -80 -90 -80 Z" 
              fill="none" stroke="url(#hyb_grad_3_a)" stroke-width="34" stroke-linecap="round"/>
        <!-- Shading Highlight -->
        <path d="M -90 -80 C -150 -80 -150 80 -90 80 C -30 80 30 -80 90 -80 C 150 -80 150 80 90 80" 
              fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
        <circle cx="0" cy="0" r="18" fill="#000000" stroke="#98FCE4" stroke-width="3"/>
    </g>'''
    add_hybrid(3, "mobius_liquid_plunge", "Möbius Liquid Plunge", "Infinite continuous fluid ribbon plunging through its own central singularity.", h03)

    # 04. Dual Fluid Torus Gravity
    h04 = f'''<g transform="translate(256, 256)">
        <ellipse cx="0" cy="0" rx="160" ry="60" fill="none" stroke="url(#hyb_grad_4_a)" stroke-width="24" transform="rotate(-25)"/>
        <ellipse cx="0" cy="0" rx="160" ry="60" fill="none" stroke="url(#hyb_grad_4_b)" stroke-width="24" transform="rotate(35)"/>
        <!-- Central Gravity Well -->
        <circle cx="0" cy="0" r="42" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <ellipse cx="0" cy="0" rx="14" ry="5" fill="#98FCE4"/>
    </g>'''
    add_hybrid(4, "dual_fluid_torus_gravity", "Dual Fluid Torus Gravity", "Two intersecting fluid tori orbiting an ultra-dense singularity core.", h04)

    # 05. Exponential Crown Splash
    h05 = f'''<g transform="translate(256, 256)">
        <!-- Fluid Splash Crown -->
        <path d="M -140 100 C -120 -40 -80 -120 -60 -100 C -40 -80 -30 20 0 0 C 30 20 40 -80 60 -100 C 80 -120 120 -40 140 100 C 100 150 -100 150 -140 100 Z" 
              fill="url(#hyb_grad_5_a)"/>
        <!-- Center Singularity Throat Plunge -->
        <path d="M -30 0 Q -2 40 0 50 Q 2 40 30 0 Z" fill="#000000"/>
        <circle cx="0" cy="50" r="8" fill="#FFFFFF"/>
        <circle cx="-60" cy="-115" r="10" fill="#98FCE4"/>
        <circle cx="60" cy="-115" r="10" fill="#9945FF"/>
    </g>'''
    add_hybrid(5, "exponential_crown_splash", "Exponential Crown Splash", "Liquid impact crown splash plunging into a central black hole throat.", h05)

    # 06. Hyperliquid 'H' Singularity
    h06 = f'''<g transform="translate(256, 256)">
        <!-- Left Pillar -->
        <path d="M -90 -140 C -90 -40 -30 -10 -20 0 C -30 10 -90 40 -90 140" fill="none" stroke="url(#hyb_grad_6_a)" stroke-width="28" stroke-linecap="round"/>
        <!-- Right Pillar -->
        <path d="M 90 -140 C 90 -40 30 -10 20 0 C 30 10 90 40 90 140" fill="none" stroke="url(#hyb_grad_6_b)" stroke-width="28" stroke-linecap="round"/>
        <!-- Central Gravity Bridge -->
        <line x1="-30" y1="0" x2="30" y2="0" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="14" fill="#000000" stroke="#98FCE4" stroke-width="3"/>
    </g>'''
    add_hybrid(6, "hyper_h_singularity", "Hyperliquid 'H' Singularity", "The classic 'H' monogram reimagined as fluid pillars curved by a central black hole.", h06)

    # 07. Iridescent Accretion Spiral
    h07 = f'''<g transform="translate(256, 256)">
        <path d="M 0 0 C 40 -30 80 -20 90 20 C 100 80 40 120 -20 120 C -100 120 -150 40 -130 -40 C -110 -130 -10 -170 80 -150 C 180 -130 220 0 180 100" 
              fill="none" stroke="url(#hyb_grad_7_a)" stroke-width="22" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="28" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="0" r="10" fill="#98FCE4"/>
    </g>'''
    add_hybrid(7, "iridescent_accretion_spiral", "Iridescent Accretion Spiral", "Spiral fluid filament coiling dynamically into an event horizon core.", h07)

    # 08. Gravitational Fluid Bubble
    h08 = f'''<g transform="translate(256, 256)">
        <circle cx="0" cy="0" r="140" fill="url(#hyb_grad_8_a)" opacity="0.9"/>
        <!-- Hollow Inner Curved Wormhole -->
        <ellipse cx="0" cy="0" rx="60" ry="100" fill="#000000"/>
        <line x1="0" y1="-140" x2="0" y2="140" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="6 6"/>
        <ellipse cx="-40" cy="-40" rx="30" ry="60" transform="rotate(-30 -40 -40)" fill="#FFFFFF" opacity="0.3"/>
    </g>'''
    add_hybrid(8, "gravitational_fluid_bubble", "Gravitational Fluid Bubble", "Volumetric liquid sphere with an internal wormhole cavity.", h08)

    # 09. Tsunami Gravity Crest
    h09 = f'''<g transform="translate(256, 256)">
        <path d="M -160 120 C -120 -60 -40 -160 60 -150 C 140 -140 180 -60 140 0 C 100 60 20 60 0 20 C -10 0 10 -20 30 -10" 
              fill="none" stroke="url(#hyb_grad_9_a)" stroke-width="28" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="22" fill="#000000" stroke="#98FCE4" stroke-width="3"/>
        <circle cx="0" cy="0" r="8" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(9, "tsunami_gravity_crest", "Tsunami Gravity Crest", "Fluid ocean tidal wave curling inward into an exponential singularity sink.", h09)

    # 10. Infinity Liquid Vortex
    h10 = f'''<g transform="translate(256, 256)">
        <ellipse cx="-75" cy="0" rx="80" ry="60" fill="none" stroke="url(#hyb_grad_10_a)" stroke-width="24"/>
        <ellipse cx="75" cy="0" rx="80" ry="60" fill="none" stroke="url(#hyb_grad_10_b)" stroke-width="24"/>
        <circle cx="-75" cy="0" r="20" fill="#000000" stroke="#98FCE4" stroke-width="2.5"/>
        <circle cx="75" cy="0" r="20" fill="#000000" stroke="#FF007A" stroke-width="2.5"/>
    </g>'''
    add_hybrid(10, "infinity_liquid_vortex", "Infinity Liquid Vortex", "Dual-vortex infinity loop connecting two opposing black hole funnels.", h10)

    # 11. Prismatic Liquid Jewel
    h11 = f'''<g transform="translate(256, 256)">
        <!-- Faceted Outer Droplet -->
        <polygon points="0,-160 120,-30 100,120 0,160 -100,120 -120,-30" fill="url(#hyb_grad_11_a)" opacity="0.9"/>
        <!-- Smooth Interior Singularity Well -->
        <circle cx="0" cy="10" r="50" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="10" r="15" fill="#98FCE4"/>
    </g>'''
    add_hybrid(11, "prismatic_liquid_jewel", "Prismatic Liquid Jewel", "Faceted crystalline droplet harboring a central black hole void.", h11)

    # 12. Magnetic Fluid Loops
    h12 = f'''<g transform="translate(256, 256)">
        <path d="M 0 120 C -120 60 -150 -80 -80 -130 C -20 -170 0 -80 0 0" fill="none" stroke="url(#hyb_grad_12_a)" stroke-width="18" stroke-linecap="round"/>
        <path d="M 0 120 C 120 60 150 -80 80 -130 C 20 -170 0 -80 0 0" fill="none" stroke="url(#hyb_grad_12_b)" stroke-width="18" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="22" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="0" r="8" fill="#98FCE4"/>
    </g>'''
    add_hybrid(12, "magnetic_fluid_loops", "Magnetic Fluid Loops", "Curved ferrofluid loops arching symmetrically out of a central throat.", h12)

    # 13. Hyper S Fluid Plunge
    h13 = f'''<g transform="translate(256, 256)">
        <path d="M 80 -130 C -50 -130 -80 -40 0 0 C 80 40 50 130 -80 130" fill="none" stroke="url(#hyb_grad_13_a)" stroke-width="32" stroke-linecap="round"/>
        <path d="M 80 -130 C -50 -130 -80 -40 0 0 C 80 40 50 130 -80 130" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
        <!-- Singularity Pinched at inflection point -->
        <circle cx="0" cy="0" r="16" fill="#000000" stroke="#98FCE4" stroke-width="3"/>
    </g>'''
    add_hybrid(13, "hyper_s_fluid_plunge", "Hyper 'S' Fluid Plunge", "Fluid 'S' monogram with its inflection point anchored by a singularity core.", h13)

    # 14. Nested Chromatic Funnels
    h14 = f'''<g transform="translate(256, 256)">
        <ellipse cx="0" cy="-60" rx="140" ry="40" fill="none" stroke="url(#hyb_grad_14_a)" stroke-width="18"/>
        <ellipse cx="0" cy="0" rx="90" ry="26" fill="none" stroke="url(#hyb_grad_14_b)" stroke-width="14"/>
        <ellipse cx="0" cy="60" rx="40" ry="12" fill="none" stroke="#98FCE4" stroke-width="10"/>
        <circle cx="0" cy="110" r="12" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(14, "nested_chromatic_funnels", "Nested Chromatic Funnels", "Concentric iridescent fluid tiers descending into a focal singularity.", h14)

    # 15. Orbiting Liquid Beads
    h15 = f'''<g transform="translate(256, 256)">
        <circle cx="0" cy="0" r="60" fill="#000000" stroke="url(#hyb_grad_15_a)" stroke-width="8"/>
        <ellipse cx="0" cy="0" rx="150" ry="50" fill="none" stroke="#374151" stroke-width="2" stroke-dasharray="4 6"/>
        <!-- Orbiting beads -->
        <circle cx="-130" cy="-25" r="16" fill="url(#hyb_grad_15_a)"/>
        <circle cx="140" cy="18" r="22" fill="url(#hyb_grad_15_b)"/>
        <circle cx="0" cy="0" r="16" fill="#98FCE4"/>
    </g>'''
    add_hybrid(15, "orbiting_liquid_beads", "Orbiting Liquid Beads", "Central black hole with fluid satellites caught in relativistic orbit.", h15)

    # 16. Double Helix Liquid Vortex
    h16 = f'''<g transform="translate(256, 256)">
        <path d="M -80 -140 Q 20 -70 -20 0 Q -60 70 80 140" fill="none" stroke="url(#hyb_grad_16_a)" stroke-width="20" stroke-linecap="round"/>
        <path d="M 80 -140 Q -20 -70 20 0 Q 60 70 -80 140" fill="none" stroke="url(#hyb_grad_16_b)" stroke-width="20" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="18" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="0" r="6" fill="#98FCE4"/>
    </g>'''
    add_hybrid(16, "double_helix_liquid_vortex", "Double Helix Liquid Vortex", "Dual fluid strands twisting into an ultra-narrow central singularity node.", h16)

    # 17. Aurora Fluid Curtain
    h17 = f'''<g transform="translate(256, 256)">
        <path d="M -140 -100 Q -60 0 -100 100 Q 0 40 100 100 Q 60 0 140 -100 Z" fill="url(#hyb_grad_17_a)" opacity="0.85"/>
        <ellipse cx="0" cy="20" rx="35" ry="50" fill="#000000" stroke="#FFFFFF" stroke-width="2"/>
        <circle cx="0" cy="20" r="8" fill="#98FCE4"/>
    </g>'''
    add_hybrid(17, "aurora_fluid_curtain", "Aurora Fluid Curtain", "Waving sheet of northern-lights fluid funneling into an event horizon aperture.", h17)

    # 18. Toroidal Fluid Whirlpool
    h18 = f'''<g transform="translate(256, 256)">
        <path d="M -120 0 C -120 -80 -60 -120 0 -120 C 60 -120 120 -80 120 0 C 120 80 60 120 0 120 C -60 120 -120 80 -120 0 Z" 
              fill="none" stroke="url(#hyb_grad_18_a)" stroke-width="32"/>
        <circle cx="0" cy="0" r="30" fill="#000000" stroke="#00E5FF" stroke-width="3"/>
        <circle cx="0" cy="0" r="10" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(18, "toroidal_fluid_whirlpool", "Toroidal Fluid Whirlpool", "Thick fluid donut pulling liquid inward through its center eye.", h18)

    # 19. Liquid Mercury Lens
    h19 = f'''<g transform="translate(256, 256)">
        <ellipse cx="0" cy="0" rx="140" ry="110" fill="url(#hyb_grad_19_a)"/>
        <!-- Gravitational Core -->
        <ellipse cx="0" cy="0" rx="70" ry="55" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <ellipse cx="-45" cy="-35" rx="20" ry="12" transform="rotate(-20 -45 -35)" fill="#FFFFFF" opacity="0.6"/>
        <circle cx="0" cy="0" r="10" fill="#98FCE4"/>
    </g>'''
    add_hybrid(19, "liquid_mercury_lens", "Liquid Mercury Lens", "Curved metallic liquid lens reflecting light around a black hole silhouette.", h19)

    # 20. Ocean Cyclone Eye
    h20 = f'''<g transform="translate(256, 256)">
        <path d="M 0 -140 C 90 -140 140 -80 140 0 C 140 60 90 90 40 60 C -10 30 10 -20 0 0" 
              fill="none" stroke="url(#hyb_grad_20_a)" stroke-width="26" stroke-linecap="round"/>
        <path d="M 0 140 C -90 140 -140 80 -140 0 C -140 -60 -90 -90 -40 -60 C 10 -30 -10 20 0 0" 
              fill="none" stroke="url(#hyb_grad_20_b)" stroke-width="26" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="18" fill="#000000" stroke="#FFFFFF" stroke-width="2.5"/>
    </g>'''
    add_hybrid(20, "ocean_cyclone_eye", "Ocean Cyclone Eye", "Atmospheric fluid cyclone spiraling into a central calm eye of singularity.", h20)

    # 21. Plasma Ring Singularity
    h21 = f'''<g transform="translate(256, 256)">
        <ellipse cx="0" cy="-60" rx="120" ry="30" fill="none" stroke="url(#hyb_grad_21_a)" stroke-width="22"/>
        <!-- Downward Funnel Filaments -->
        <path d="M -120 -60 Q -20 60 0 110" fill="none" stroke="url(#hyb_grad_21_b)" stroke-width="14" stroke-linecap="round"/>
        <path d="M 120 -60 Q 20 60 0 110" fill="none" stroke="url(#hyb_grad_21_b)" stroke-width="14" stroke-linecap="round"/>
        <circle cx="0" cy="110" r="14" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(21, "plasma_ring_singularity", "Plasma Ring Singularity", "Upper floating fluid ring connecting to a needle-thin singularity tip.", h21)

    # 22. Tri-Blade Fluid Spiral
    h22 = f'''<g transform="translate(256, 256)">
        <path d="M 0 0 C 40 -80 120 -110 140 -50 C 160 10 90 50 0 0 Z" fill="url(#hyb_grad_22_a)" opacity="0.9"/>
        <path d="M 0 0 C -80 -40 -110 40 -50 120 C 10 160 50 90 0 0 Z" fill="url(#hyb_grad_22_b)" opacity="0.85" transform="rotate(120)"/>
        <path d="M 0 0 C -40 80 40 120 120 50 C 160 -10 90 -60 0 0 Z" fill="url(#hyb_grad_22_a)" opacity="0.8" transform="rotate(240)"/>
        <circle cx="0" cy="0" r="22" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
    </g>'''
    add_hybrid(22, "tri_blade_fluid_spiral", "Tri-Blade Fluid Spiral", "Three aerodynamic fluid foils meeting at a central gravitational vortex.", h22)

    # 23. Modernist Fluid Hourglass
    h23 = f'''<g transform="translate(256, 256)">
        <path d="M -100 -130 L 100 -130 C 50 -40 15 -10 0 0 C -15 10 -50 40 -100 130 L 100 130 C 50 40 15 10 0 0 C -15 -10 -50 -40 -100 -130 Z" 
              fill="url(#hyb_grad_23_a)" opacity="0.85"/>
        <line x1="0" y1="-130" x2="0" y2="130" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="4 4"/>
        <circle cx="0" cy="0" r="8" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(23, "modernist_fluid_hourglass", "Modernist Fluid Hourglass", "Fluid hourglass chambers connected through an exponential 3.0px neck.", h23)

    # 24. Solar Fluid Prominence
    h24 = f'''<g transform="translate(256, 256)">
        <circle cx="0" cy="0" r="110" fill="#000000" stroke="#374151" stroke-width="2"/>
        <!-- Giant arching fluid prominence -->
        <path d="M -80 75 C -140 -80 0 -170 80 -75" fill="none" stroke="url(#hyb_grad_24_a)" stroke-width="26" stroke-linecap="round"/>
        <circle cx="0" cy="0" r="28" fill="#98FCE4" opacity="0.4"/>
        <circle cx="0" cy="0" r="12" fill="#FFFFFF"/>
    </g>'''
    add_hybrid(24, "solar_fluid_prominence", "Solar Fluid Prominence", "Giant fluid arc looping over a deep black hole event horizon disk.", h24)

    # 25. Singularity Lotus Bloom
    h25 = f'''<g transform="translate(256, 256)">
        <!-- 4 Fluid Petals -->
        <path d="M 0 0 C -50 -60 -100 -60 -110 0 C -100 60 -50 60 0 0 Z" fill="url(#hyb_grad_25_a)" opacity="0.85"/>
        <path d="M 0 0 C 50 -60 100 -60 110 0 C 100 60 50 60 0 0 Z" fill="url(#hyb_grad_25_a)" opacity="0.85"/>
        <path d="M 0 0 C -60 -50 -60 -100 0 -110 C 60 -100 60 -50 0 0 Z" fill="url(#hyb_grad_25_b)" opacity="0.85"/>
        <path d="M 0 0 C -60 50 -60 100 0 110 C 60 100 60 50 0 0 Z" fill="url(#hyb_grad_25_b)" opacity="0.85"/>
        <!-- Central Gravity Stamen -->
        <circle cx="0" cy="0" r="24" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
        <circle cx="0" cy="0" r="8" fill="#98FCE4"/>
    </g>'''
    add_hybrid(25, "singularity_lotus_bloom", "Singularity Lotus Bloom", "Organic fluid petals radiating outward from a dense gravitational core.", h25)

    print(f"Generated {len(hybrids)} hybrid logos in {HYBRID25_DIR}")
    return hybrids

# =========================================================================
# PART 3: BUILD DEDICATED SHOWCASE HTML (showcase_3d_and_hybrids.html)
# =========================================================================
def build_showcase(bh_list, hyb_list):
    def render_items(items, folder):
        html_items = []
        for fname, svg_code, title, desc in items:
            ta_id = f"copy_{fname.replace('.', '_')}"
            html_items.append(f'''
            <div class="logo-card">
                <div class="logo-preview">
                    {svg_code}
                </div>
                <div class="logo-meta">
                    <div class="logo-title">{title}</div>
                    <div class="logo-desc">{desc}</div>
                    <div class="logo-actions">
                        <a href="{folder}/{fname}" download class="btn btn-primary">Download SVG</a>
                        <button class="btn btn-secondary" onclick="copySvgCode('{ta_id}')">Copy SVG Code</button>
                        <textarea id="{ta_id}" style="display:none;">{svg_code}</textarea>
                    </div>
                </div>
            </div>''')
        return "\n".join(html_items)

    bh_html = render_items(bh_list, "blackhole-10")
    hyb_html = render_items(hyb_list, "hybrid-25")

    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperSettle • 10 3D Black Holes &amp; 25 Hybrid Logos</title>
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
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        header {{
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 36px;
            margin-bottom: 40px;
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
            font-size: 44px;
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
            max-width: 860px;
        }}
        
        /* Navigation Tabs */
        .tab-bar {{
            display: flex;
            gap: 12px;
            margin-bottom: 36px;
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 16px;
        }}
        .tab-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-family: var(--font-mono);
            font-size: 14px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active, .tab-btn:hover {{
            color: #030605;
            background: var(--mint);
        }}
        
        /* Section Header */
        .section-header {{
            margin-bottom: 28px;
        }}
        .section-title {{
            font-size: 26px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        .section-desc {{
            color: var(--text-secondary);
            font-size: 13px;
            margin-top: 4px;
        }}
        
        /* Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 28px;
            margin-bottom: 64px;
        }}
        .logo-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
        }}
        .logo-card:hover {{
            border-color: var(--cyan);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px -5px rgba(0, 229, 255, 0.15);
        }}
        .logo-preview {{
            background: #000000;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            aspect-ratio: 1 / 1;
        }}
        .logo-meta {{
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex-grow: 1;
        }}
        .logo-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--mint);
        }}
        .logo-desc {{
            font-size: 12.5px;
            color: var(--text-secondary);
            flex-grow: 1;
        }}
        .logo-actions {{
            display: flex;
            gap: 10px;
            margin-top: 12px;
        }}
        
        .btn {{
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 12px;
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
            <span class="badge">33RD LABS 3D REDESIGNS + HYPERLIQUID HYBRID MARKS</span>
            <h1>3D Black Holes &amp; Hybrid Logo Suite</h1>
            <p class="subtitle">10 architectural redesigns of the 33rd Labs black hole concept rendered with 3D volumetric shading and physics, alongside 25 unique logos merging the 33rd Tree singularity with Hyperliquid's fluid multi-color aesthetic.</p>
        </header>

        <div class="tab-bar">
            <button class="tab-btn active" onclick="switchTab('bh', this)">10 3D Black Hole Redesigns</button>
            <button class="tab-btn" onclick="switchTab('hyb', this)">25 Hyperliquid Hybrid Logos</button>
        </div>

        <!-- Tab 1: 10 3D Black Hole Concepts -->
        <div id="tab-bh">
            <div class="section-header">
                <h2 class="section-title">10 Redesigned 33rd Labs Black Hole Concepts</h2>
                <p class="section-desc">The same exact mathematical exponential plunge / tensor arbor, rendered across 10 distinct physics and 3D visual paradigms.</p>
            </div>
            <div class="cards-grid">
                {bh_html}
            </div>
        </div>

        <!-- Tab 2: 25 Hybrid Logos -->
        <div id="tab-hyb" style="display:none;">
            <div class="section-header">
                <h2 class="section-title">25 Unique 33rd Tree × Hyperliquid Hybrid Logos</h2>
                <p class="section-desc">Merging the 33rd Tree blackhole singularity throat with Hyperliquid's organic fluid droplet, iridescent gradients, and specular sheen.</p>
            </div>
            <div class="cards-grid">
                {hyb_html}
            </div>
        </div>
    </div>

    <div id="toast">SVG Vector Code Copied!</div>

    <script>
        function switchTab(tabName, btn) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (tabName === 'bh') {{
                document.getElementById('tab-bh').style.display = 'block';
                document.getElementById('tab-hyb').style.display = 'none';
            }} else {{
                document.getElementById('tab-bh').style.display = 'none';
                document.getElementById('tab-hyb').style.display = 'block';
            }}
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
        f.write(content)
    print(f"Generated dedicated showcase at {SHOWCASE_HTML}")

if __name__ == "__main__":
    bh = generate_10_blackhole_concepts()
    hyb = generate_25_hybrids()
    build_showcase(bh, hyb)
    print("All 35 new advanced designs and showcase generated successfully!")

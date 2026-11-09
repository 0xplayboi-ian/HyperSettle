#!/usr/bin/env python3
"""
HyperSettle Brand & Logo Suite Generator
- Generates 6 Brand Card Drafts using the 33rd Trees Tensor Arbor logo + Obel Mono typography
- Generates 100 distinct Multi-Color Logos similar to the Hyperliquid fluid/gradient aesthetic
- Generates an interactive gallery HTML showcase
"""

import os
import math
import json

BASE_DIR = "/Users/ianmora/Desktop/Projects/HyperSettle"
BRAND_CARDS_DIR = os.path.join(BASE_DIR, "branding", "brand-cards")
LOGOS_DIR = os.path.join(BASE_DIR, "branding", "logos-100")
SHOWCASE_PATH = os.path.join(BASE_DIR, "branding", "index.html")

os.makedirs(BRAND_CARDS_DIR, exist_ok=True)
os.makedirs(LOGOS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 33RD TREES TENSOR ARBOR #06 MATHEMATICAL CURVATURE & ELEMENTS
# -----------------------------------------------------------------------------
CX = 120
Y_TOP = 38
Y_THROAT = 135
Y_BOTTOM = 205

def r_exp(y):
    dist = abs(y - Y_THROAT)
    h = (Y_THROAT - Y_TOP) if y < Y_THROAT else (Y_BOTTOM - Y_THROAT)
    norm = dist / h
    return 1.5 + 85.5 * ((math.exp(3.8 * norm) - 1.0) / (math.exp(3.8) - 1.0))

RING_YS = [38, 44, 55, 75, 105, 126, 135, 144, 165, 185, 205]
MERIDIAN_FRACTIONS = [1.0, 0.75, 0.48, 0.22]

def make_curve_pts(factor, side, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        y = Y_TOP + t * (Y_BOTTOM - Y_TOP)
        r = r_exp(y) * factor
        x = CX + side * r
        pts.append((x, y))
    return pts

def path_from_pts(pts):
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for p in pts[1:]:
        d += f" L {p[0]:.1f} {p[1]:.1f}"
    return d

def render_33rd_mark(stroke_color="#FFFFFF", fill_throat="#FFFFFF", accent_color=None):
    elems = []
    # 4 Tensor Meridians (Left & Right)
    for frac in MERIDIAN_FRACTIONS:
        sw = "2.8" if frac == 1.0 else ("2.0" if frac > 0.6 else "1.5")
        op = "1.0" if frac == 1.0 else ("0.85" if frac > 0.6 else "0.7")
        col = stroke_color
        if accent_color and frac == 1.0:
            col = accent_color
        pts_l = make_curve_pts(frac, -1)
        pts_r = make_curve_pts(frac, 1)
        elems.append(f'<path d="{path_from_pts(pts_l)}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
        elems.append(f'<path d="{path_from_pts(pts_r)}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
        
    # Central Singularity Axis
    axis_col = accent_color if accent_color else stroke_color
    elems.append(f'<line x1="{CX}" y1="28" x2="{CX}" y2="212" stroke="{axis_col}" stroke-width="1.8" stroke-dasharray="3 3" opacity="0.75"/>')

    # Exponentially Clustered Rings
    for y in RING_YS:
        r = r_exp(y)
        ry = max(1.0, r * 0.22)
        if y == Y_THROAT:
            throat_col = accent_color if accent_color else fill_throat
            elems.append(f'<ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="{throat_col}" stroke="{stroke_color}" stroke-width="2.5"/>')
        else:
            ring_sw = "1.8" if (y == Y_TOP or y == Y_BOTTOM) else "1.5"
            ring_op = "0.9" if (y == Y_TOP or y == Y_BOTTOM) else "0.75"
            elems.append(f'<ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="{stroke_color}" stroke-width="{ring_sw}" opacity="{ring_op}"/>')
            
    # Datum Coordinate Points
    elems.append(f'<circle cx="{CX}" cy="26" r="4.5" fill="{axis_col}"/>')
    elems.append(f'<circle cx="33.0" cy="38" r="3.2" fill="{stroke_color}"/>')
    elems.append(f'<circle cx="207.0" cy="38" r="3.2" fill="{stroke_color}"/>')
    return "\n            ".join(elems)

FONT_STACK = "'Obel Mono', 'Obelisk Mono', 'Space Mono', 'JetBrains Mono', monospace"

# -----------------------------------------------------------------------------
# GENERATE 6 BRAND CARD DRAFTS (33RD TREES AESTHETIC)
# -----------------------------------------------------------------------------
def build_brand_cards():
    cards = []
    
    # 1. Classic Monochrome Horizontal (740x190)
    svg_01 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 190" width="100%" height="100%">
    <rect width="740" height="190" rx="20" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    <g transform="translate(24, 15) scale(0.68)">
        {render_33rd_mark("#FFFFFF", "#FFFFFF")}
    </g>
    <g transform="translate(210, 74)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="24" fill="#FFFFFF" letter-spacing="2.5">HYPERSETTLE</tspan>
            <tspan font-weight="600" font-size="14" fill="#FFFFFF" opacity="0.8" letter-spacing="1.8"> • REVENUE ENGINE</tspan>
        </text>
        <line x1="0" y1="22" x2="495" y2="22" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.35"/>
        <text x="0" y="46" font-family="{FONT_STACK}" font-weight="600" font-size="12" fill="#FFFFFF" opacity="0.75" letter-spacing="2.2">HYPERCORE ATTRIBUTION // SOLANA SQUADS SETTLEMENT</text>
    </g>
</svg>'''
    cards.append(("01_33rd_monochrome_horizontal.svg", svg_01, "01 • Classic Monochrome Horizontal", "Pure obsidian black with crisp white precision vector geometry and Obel Mono telemetry."))

    # 2. Hyperliquid Mint & Solana Purple Dual Glow (740x190)
    svg_02 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 190" width="100%" height="100%">
    <defs>
        <linearGradient id="hlMintSol" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
        <radialGradient id="cardGlow" cx="15%" cy="50%" r="55%">
            <stop offset="0%" stop-color="#98FCE4" stop-opacity="0.12"/>
            <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
        </radialGradient>
    </defs>
    <rect width="740" height="190" rx="20" fill="#080C0B" stroke="#163832" stroke-width="1.5"/>
    <rect width="740" height="190" rx="20" fill="url(#cardGlow)"/>
    <g transform="translate(24, 15) scale(0.68)">
        {render_33rd_mark("#E0FFF8", "#98FCE4", accent_color="#98FCE4")}
    </g>
    <g transform="translate(210, 74)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="24" fill="#98FCE4" letter-spacing="2.5">HYPERSETTLE</tspan>
            <tspan font-weight="600" font-size="14" fill="#E0FFF8" opacity="0.85" letter-spacing="1.8"> • FINOPS PROTOCOL</tspan>
        </text>
        <line x1="0" y1="22" x2="495" y2="22" stroke="url(#hlMintSol)" stroke-width="1.6" stroke-opacity="0.8"/>
        <text x="0" y="46" font-family="{FONT_STACK}" font-weight="600" font-size="12" fill="#E0FFF8" opacity="0.75" letter-spacing="2.2">L1 BUILDER CODE REVENUE // DETERMINISTIC MICRO-USD SPLIT</text>
    </g>
</svg>'''
    cards.append(("02_33rd_hyperliquid_mint_horizontal.svg", svg_02, "02 • Hyperliquid Mint & Solana Telemetry", "Deep dark teal obsidian background with Hyperliquid electric mint (#98FCE4) and Solana spectrum rule."))

    # 3. Stacked Tactical HUD Card (520x420)
    svg_03 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" width="100%" height="100%">
    <defs>
        <pattern id="hudGrid" width="20" height="20" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="20" y2="0" stroke="#FFFFFF" stroke-width="0.5" stroke-opacity="0.05"/>
            <line x1="0" y1="0" x2="0" y2="20" stroke="#FFFFFF" stroke-width="0.5" stroke-opacity="0.05"/>
        </pattern>
    </defs>
    <rect width="520" height="420" rx="24" fill="#040608" stroke="#1F2937" stroke-width="1.5"/>
    <rect width="520" height="420" fill="url(#hudGrid)" rx="24"/>
    
    <!-- Top HUD telemetry bar -->
    <text x="32" y="42" font-family="{FONT_STACK}" font-size="10" fill="#98FCE4" letter-spacing="2">SYS_ID: HYPE_SETTLE // CORE_V04</text>
    <text x="488" y="42" text-anchor="end" font-family="{FONT_STACK}" font-size="10" fill="#6B7280" letter-spacing="1.5">PRECISION: 10^-6 USD</text>
    <line x1="32" y1="52" x2="488" y2="52" stroke="#374151" stroke-width="1"/>
    
    <!-- Centered Mark -->
    <g transform="translate(196, 68) scale(0.53)">
        {render_33rd_mark("#FFFFFF", "#98FCE4", accent_color="#98FCE4")}
    </g>
    
    <!-- Main Center Titles -->
    <text x="260" y="225" text-anchor="middle" font-family="{FONT_STACK}" font-weight="800" font-size="28" fill="#FFFFFF" letter-spacing="3.5">HYPERSETTLE</text>
    <text x="260" y="252" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="13" fill="#98FCE4" letter-spacing="2.5">DECENTRALIZED BUILDER SETTLEMENTS</text>
    
    <line x1="60" y1="272" x2="460" y2="272" stroke="#374151" stroke-width="1" stroke-dasharray="4 4"/>
    
    <!-- Coordinate Telemetry Block -->
    <g transform="translate(60, 298)">
        <text x="0" y="0" font-family="{FONT_STACK}" font-size="11" fill="#9CA3AF" letter-spacing="1">INGESTION : HYPERCORE FILL STREAM</text>
        <text x="0" y="20" font-family="{FONT_STACK}" font-size="11" fill="#9CA3AF" letter-spacing="1">SETTLEMENT: SQUADS MULTISIG // SOLANA</text>
        <text x="0" y="40" font-family="{FONT_STACK}" font-size="11" fill="#9CA3AF" letter-spacing="1">CUSTODY   : ZERO-CUSTODY // AUDITABLE</text>
        
        <rect x="300" y="-12" width="100" height="56" rx="6" fill="#0E1A18" stroke="#163832"/>
        <text x="350" y="10" text-anchor="middle" font-family="{FONT_STACK}" font-size="9" fill="#98FCE4" letter-spacing="1">STATUS</text>
        <text x="350" y="28" text-anchor="middle" font-family="{FONT_STACK}" font-weight="700" font-size="13" fill="#10B981" letter-spacing="1">VERIFIED</text>
    </g>
    
    <!-- Corner Reticles -->
    <path d="M 20 30 L 20 20 L 30 20" fill="none" stroke="#98FCE4" stroke-width="1.8"/>
    <path d="M 500 30 L 500 20 L 490 20" fill="none" stroke="#98FCE4" stroke-width="1.8"/>
    <path d="M 20 390 L 20 400 L 30 400" fill="none" stroke="#98FCE4" stroke-width="1.8"/>
    <path d="M 500 390 L 500 400 L 490 400" fill="none" stroke="#98FCE4" stroke-width="1.8"/>
</svg>'''
    cards.append(("03_33rd_stacked_hud_card.svg", svg_03, "03 • Stacked Tactical HUD Brand Card", "Full square-ratio technical HUD card with coordinate reticles, telemetry grid, and verification badge."))

    # 4. Circular Token Seal / PFP (512x512)
    svg_04 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        <path id="topTextArc" d="M 56,256 A 200,200 0 1,1 456,256" fill="none"/>
        <path id="botTextArc" d="M 456,256 A 200,200 0 0,1 56,256" fill="none"/>
        <radialGradient id="tokenGlow" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stop-color="#142F2A"/>
            <stop offset="70%" stop-color="#050A09"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
    </defs>
    <circle cx="256" cy="256" r="250" fill="url(#tokenGlow)" stroke="#1F473E" stroke-width="2.5"/>
    <circle cx="256" cy="256" r="226" fill="none" stroke="#98FCE4" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
    <circle cx="256" cy="256" r="176" fill="none" stroke="#374151" stroke-width="1"/>
    
    <!-- Curved Circular Typography -->
    <text font-family="{FONT_STACK}" font-weight="800" font-size="14" fill="#98FCE4" letter-spacing="3.8">
        <textPath href="#topTextArc" startOffset="50%" text-anchor="middle">HYPERSETTLE • REVENUE ENGINE</textPath>
    </text>
    <text font-family="{FONT_STACK}" font-weight="700" font-size="12" fill="#9CA3AF" letter-spacing="3.2">
        <textPath href="#botTextArc" startOffset="50%" text-anchor="middle">HYPERCORE L1 // SOLANA SQUADS</textPath>
    </text>
    
    <!-- Center Mark -->
    <g transform="translate(196, 172) scale(0.5)">
        {render_33rd_mark("#FFFFFF", "#98FCE4", accent_color="#98FCE4")}
    </g>
</svg>'''
    cards.append(("04_33rd_token_round_badge.svg", svg_04, "04 • Circular Token / PFP Badge", "360-degree round token emblem with circular typography following outer orbit curves."))

    # 5. Inverted Minimalist Editorial (740x190)
    svg_05 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 190" width="100%" height="100%">
    <rect width="740" height="190" rx="20" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
    <g transform="translate(24, 15) scale(0.68)">
        {render_33rd_mark("#0F172A", "#0F172A", accent_color="#0F172A")}
    </g>
    <g transform="translate(210, 74)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="24" fill="#0F172A" letter-spacing="2.5">HYPERSETTLE</tspan>
            <tspan font-weight="600" font-size="14" fill="#475569" letter-spacing="1.8"> • PROTOCOL REVENUE</tspan>
        </text>
        <line x1="0" y1="22" x2="495" y2="22" stroke="#0F172A" stroke-width="1.4" stroke-opacity="0.3"/>
        <text x="0" y="46" font-family="{FONT_STACK}" font-weight="600" font-size="12" fill="#64748B" letter-spacing="2.2">RECONCILIATION // SPLIT CALCULATIONS // CSV EXPORT</text>
    </g>
</svg>'''
    cards.append(("05_33rd_inverted_light_card.svg", svg_05, "05 • Inverted Crisp Editorial Light", "Paper white high-contrast editorial variant with deep obsidian ink typography and geometry."))

    # 6. Hero Social / Pitch Deck Banner (1200x630)
    svg_06 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
    <defs>
        <radialGradient id="heroBg" cx="30%" cy="50%" r="70%">
            <stop offset="0%" stop-color="#0B1A17"/>
            <stop offset="50%" stop-color="#040807"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="glowLine" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
    </defs>
    <rect width="1200" height="630" fill="url(#heroBg)"/>
    
    <!-- Background telemetry grid lines -->
    <line x1="80" y1="80" x2="1120" y2="80" stroke="#1F3D37" stroke-width="1"/>
    <line x1="80" y1="550" x2="1120" y2="550" stroke="#1F3D37" stroke-width="1"/>
    <line x1="80" y1="80" x2="80" y2="550" stroke="#1F3D37" stroke-width="1"/>
    <line x1="1120" y1="80" x2="1120" y2="550" stroke="#1F3D37" stroke-width="1"/>
    
    <!-- Scaled Mark Left -->
    <g transform="translate(130, 160) scale(1.4)">
        {render_33rd_mark("#FFFFFF", "#98FCE4", accent_color="#98FCE4")}
    </g>
    
    <!-- Main Typography Right -->
    <g transform="translate(540, 260)">
        <text x="0" y="0" font-family="{FONT_STACK}" font-size="14" fill="#98FCE4" letter-spacing="4">COLOSSEUM ETERNAL // PAYMENTS &amp; TOOLING</text>
        <text x="0" y="55" font-family="{FONT_STACK}" font-weight="800" font-size="52" fill="#FFFFFF" letter-spacing="4">HYPERSETTLE</text>
        <line x1="0" y1="85" x2="580" y2="85" stroke="url(#glowLine)" stroke-width="3"/>
        <text x="0" y="125" font-family="{FONT_STACK}" font-weight="600" font-size="18" fill="#E0FFF8" opacity="0.9" letter-spacing="2">HYPERLIQUID BUILDER REVENUE ATTRIBUTION</text>
        <text x="0" y="155" font-family="{FONT_STACK}" font-weight="500" font-size="16" fill="#9CA3AF" letter-spacing="1.8">NON-CUSTODIAL SOLANA USDC SQUADS SETTLEMENTS</text>
        
        <rect x="0" y="195" width="220" height="42" rx="8" fill="#133830" stroke="#98FCE4" stroke-width="1.5"/>
        <text x="110" y="222" text-anchor="middle" font-family="{FONT_STACK}" font-weight="700" font-size="13" fill="#98FCE4" letter-spacing="2.2">PRECISION 10^-6 USD</text>
    </g>
</svg>'''
    cards.append(("06_33rd_banner_social.svg", svg_06, "06 • Pitch Deck & Social Hero Banner (1200x630)", "Widescreen high-resolution showcase banner for GitHub preview, pitch presentation, and social cards."))

    for fname, svg_content, title, desc in cards:
        path = os.path.join(BRAND_CARDS_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
    print(f"Generated {len(cards)} brand cards in {BRAND_CARDS_DIR}")
    return cards

# -----------------------------------------------------------------------------
# GENERATE 100 MULTI-COLOR LOGOS SIMILAR TO HYPERLIQUID'S FLUID GRADIENTS
# -----------------------------------------------------------------------------
PALETTES = [
    # 0: Hyperliquid Primary (Electric Mint to Deep Teal to Cyan)
    ["#98FCE4", "#00E5FF", "#00B4D8", "#072723"],
    # 1: Solana Spectrum (Solana Violet to Electric Turquoise)
    ["#9945FF", "#7928CA", "#00DFD8", "#14F195"],
    # 2: Iridescent Rainbow Flow (Prismatic Hologram)
    ["#FF007A", "#7928CA", "#0070F3", "#00F5A0"],
    # 3: Aurora Borealis (Neon Lime, Emerald, Cyan)
    ["#10B981", "#059669", "#00F5D4", "#7B2CBF"],
    # 4: Cosmic Twilight (Deep Magenta, Violet, Neon Blue)
    ["#FF0055", "#C800FF", "#0038FF", "#00FFF0"],
    # 5: Solar Flare & Liquid Gold (Electric Amber, Flame, Bright Coral)
    ["#FFE600", "#FF6B00", "#FF007A", "#98FCE4"],
    # 6: Liquid Nitrogen (Ice Blue, Bright Cyan, Ultra-White)
    ["#E0F2FE", "#38BDF8", "#0284C7", "#98FCE4"],
    # 7: HyperCore Matrix (Cyber Emerald, Mint, Pure White)
    ["#FFFFFF", "#98FCE4", "#10B981", "#042F2E"]
]

def make_gradient(gid, colors, gtype="linear", angle=45):
    rad = math.radians(angle)
    x1 = f"{50 - 50 * math.cos(rad):.1f}%"
    y1 = f"{50 - 50 * math.sin(rad):.1f}%"
    x2 = f"{50 + 50 * math.cos(rad):.1f}%"
    y2 = f"{50 + 50 * math.sin(rad):.1f}%"
    
    n = len(colors)
    stops = []
    for i, c in enumerate(colors):
        pct = int(i * 100 / (n - 1))
        stops.append(f'<stop offset="{pct}%" stop-color="{c}"/>')
    stops_str = "\n            ".join(stops)
    
    if gtype == "radial":
        return f'''<radialGradient id="{gid}" cx="50%" cy="50%" r="55%">
            {stops_str}
        </radialGradient>'''
    else:
        return f'''<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">
            {stops_str}
        </linearGradient>'''

def build_100_logos():
    logos = []
    
    # 10 Archetypes, 10 variations each
    for idx in range(1, 101):
        archetype_id = (idx - 1) // 10  # 0..9
        variant_num = ((idx - 1) % 10) + 1
        pal = PALETTES[idx % len(PALETTES)]
        gid1 = f"grad_{idx}_a"
        gid2 = f"grad_{idx}_b"
        
        grad1 = make_gradient(gid1, pal, "linear", angle=(idx * 37) % 360)
        grad2 = make_gradient(gid2, list(reversed(pal)), "linear", angle=((idx * 53) + 90) % 360)
        
        cx, cy = 256, 256
        elements = []
        name = ""
        category = ""
        
        # -------------------------------------------------------------
        # Archetype 0: Fluid Liquid Droplets & Tear Loops (Hyperliquid style)
        # -------------------------------------------------------------
        if archetype_id == 0:
            category = "Fluid Liquid Droplet"
            name = f"Hydro Drop Alpha #{variant_num:02d}"
            # Fluid teardrop / water drop geometry with intersecting waves
            scale = 0.85 + (variant_num * 0.02)
            rot = (variant_num - 1) * 36
            elements.append(f'''
            <g transform="translate({cx},{cy}) rotate({rot}) scale({scale}) translate(-{cx},-{cy})">
                <!-- Outer Liquid Body -->
                <path d="M 256 70 C 330 170 380 240 380 320 C 380 395 325 442 256 442 C 187 442 132 395 132 320 C 132 240 182 170 256 70 Z" 
                      fill="url(#{gid1})" opacity="0.95"/>
                <!-- Inner Curved Specular Reflection -->
                <path d="M 256 110 C 300 180 340 240 340 310 C 340 365 305 402 256 402 C 235 402 215 393 200 378 C 220 378 250 360 260 320 C 275 260 256 180 256 110 Z" 
                      fill="url(#{gid2})" opacity="0.85"/>
                <!-- Specular Highlight Drop -->
                <circle cx="215" cy="235" r="24" fill="#FFFFFF" opacity="0.4"/>
                <ellipse cx="280" cy="340" rx="45" ry="25" transform="rotate(-30 280 340)" fill="url(#{gid2})" opacity="0.75"/>
            </g>''')

        # -------------------------------------------------------------
        # Archetype 1: Vortex & Hydro-Spirals
        # -------------------------------------------------------------
        elif archetype_id == 1:
            category = "Vortex & Hydro-Spiral"
            name = f"Vortex Swirl #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy})">')
            blades = 3 + (variant_num % 4)
            for b in range(blades):
                rot = b * (360 / blades) + (variant_num * 12)
                sw = 12 + variant_num
                elements.append(f'''
                <path d="M 0 0 C 40 -60 120 -100 170 -60 C 210 -20 200 60 150 110 C 100 160 20 170 -40 140" 
                      fill="none" stroke="url(#{gid1})" stroke-width="{sw}" stroke-linecap="round" 
                      transform="rotate({rot})" opacity="0.85"/>
                <circle cx="90" cy="-40" r="16" fill="url(#{gid2})" transform="rotate({rot})"/>
                ''')
            elements.append(f'<circle cx="0" cy="0" r="28" fill="url(#{gid2})"/>')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 2: Nested Orbital Tori & Hyper-Rings
        # -------------------------------------------------------------
        elif archetype_id == 2:
            category = "Orbital Tori & Hyper-Rings"
            name = f"Orbital Core #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy})">')
            rings = 3 + (variant_num % 3)
            for r in range(rings):
                rx = 160 - r * 28
                ry = 65 + r * 14
                tilt = r * 45 + (variant_num * 15)
                elements.append(f'''
                <ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="none" stroke="url(#{gid1 if r%2==0 else gid2})" 
                         stroke-width="{14 - r*2}" stroke-linecap="round" transform="rotate({tilt})" opacity="{0.9 - r*0.1}"/>
                <circle cx="{rx}" cy="0" r="{10 - r}" fill="#FFFFFF" transform="rotate({tilt})"/>
                ''')
            elements.append(f'<circle cx="0" cy="0" r="38" fill="url(#{gid1})"/>')
            elements.append(f'<circle cx="0" cy="0" r="18" fill="#FFFFFF" opacity="0.8"/>')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 3: Möbius Bands & Continuous Liquid Loops
        # -------------------------------------------------------------
        elif archetype_id == 3:
            category = "Möbius Liquid Loop"
            name = f"Infinity Ribbon #{variant_num:02d}"
            scale = 0.9 + (variant_num * 0.02)
            rot = (variant_num - 1) * 20
            elements.append(f'''
            <g transform="translate({cx},{cy}) rotate({rot}) scale({scale}) translate(-{cx},-{cy})">
                <!-- Left Loop -->
                <path d="M 160 256 C 160 180 80 180 80 256 C 80 332 160 332 256 256 C 352 180 432 180 432 256 C 432 332 352 332 256 256" 
                      fill="none" stroke="url(#{gid1})" stroke-width="{26 + variant_num}" stroke-linecap="round" stroke-linejoin="round"/>
                <!-- Shimmer Overlay Loop -->
                <path d="M 160 256 C 160 190 95 190 95 256 C 95 322 160 322 256 256" 
                      fill="none" stroke="url(#{gid2})" stroke-width="12" stroke-linecap="round" opacity="0.9"/>
                <circle cx="80" cy="256" r="14" fill="#FFFFFF"/>
                <circle cx="432" cy="256" r="14" fill="#98FCE4"/>
            </g>''')

        # -------------------------------------------------------------
        # Archetype 4: Dual-Helix Settlement Waves (Cross-Chain Bridge)
        # -------------------------------------------------------------
        elif archetype_id == 4:
            category = "Cross-Chain Wave Helix"
            name = f"Helix Bridge #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy}) rotate({(variant_num-1)*18})">')
            for h in range(7):
                y_pos = -130 + h * 42
                amp = 80 + variant_num * 4
                x1 = math.sin(h * 0.8) * amp
                x2 = -x1
                elements.append(f'<line x1="{x1}" y1="{y_pos}" x2="{x2}" y2="{y_pos}" stroke="#374151" stroke-width="2.5" stroke-dasharray="3 3"/>')
                elements.append(f'<circle cx="{x1}" cy="{y_pos}" r="12" fill="url(#{gid1})"/>')
                elements.append(f'<circle cx="{x2}" cy="{y_pos}" r="12" fill="url(#{gid2})"/>')
            # Connecting Splines
            elements.append(f'''
            <path d="M -80 -130 Q -10 -40 -80 40 T -80 130" fill="none" stroke="url(#{gid1})" stroke-width="16" stroke-linecap="round" opacity="0.85"/>
            <path d="M 80 -130 Q 10 -40 80 40 T 80 130" fill="none" stroke="url(#{gid2})" stroke-width="16" stroke-linecap="round" opacity="0.85"/>
            ''')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 5: Prismatic Hyper-Crystals & Refracted Nodes
        # -------------------------------------------------------------
        elif archetype_id == 5:
            category = "Prismatic Hyper-Crystal"
            name = f"Prism Node #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy}) rotate({(variant_num-1)*15})">')
            pts = 5 + (variant_num % 4)
            r_out = 160
            r_in = 75
            path_d = ""
            for p in range(pts * 2):
                ang = p * math.pi / pts
                r = r_out if p % 2 == 0 else r_in
                px = r * math.cos(ang)
                py = r * math.sin(ang)
                path_d += f"{'M' if p == 0 else 'L'} {px:.1f} {py:.1f} "
            path_d += "Z"
            elements.append(f'<path d="{path_d}" fill="url(#{gid1})" opacity="0.85"/>')
            elements.append(f'<circle cx="0" cy="0" r="50" fill="url(#{gid2})"/>')
            elements.append(f'<circle cx="0" cy="0" r="22" fill="#FFFFFF"/>')
            for p in range(pts):
                ang = p * 2 * math.pi / pts
                px = r_out * math.cos(ang)
                py = r_out * math.sin(ang)
                elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="#FFFFFF"/>')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 6: Kinetic Ring Accelerators & Data Tracks
        # -------------------------------------------------------------
        elif archetype_id == 6:
            category = "Kinetic Ring Accelerator"
            name = f"Particle Track #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy})">')
            tracks = 4
            for t in range(tracks):
                r = 50 + t * 35
                sw = 10 + t * 2
                da = f"{20 + t*15} {15 + t*8}"
                rot = (t * 45) + (variant_num * 18)
                elements.append(f'''
                <circle cx="0" cy="0" r="{r}" fill="none" stroke="url(#{gid1 if t%2==0 else gid2})" 
                        stroke-width="{sw}" stroke-dasharray="{da}" transform="rotate({rot})" opacity="0.9"/>
                ''')
            elements.append(f'<circle cx="0" cy="0" r="30" fill="url(#{gid1})"/>')
            elements.append(f'<circle cx="0" cy="0" r="14" fill="#FFFFFF"/>')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 7: Event Horizon Lenses & Gravity Curvatures
        # -------------------------------------------------------------
        elif archetype_id == 7:
            category = "Event Horizon Gravitational Lens"
            name = f"Curvature Horizon #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy}) rotate({(variant_num-1)*24})">')
            # Arching gravitational arcs
            for a in range(5):
                r = 60 + a * 25
                sw = 8 + a * 2
                op = 1.0 - a * 0.15
                elements.append(f'''
                <path d="M -{r*1.4:.1f} 0 A {r*1.4:.1f} {r:.1f} 0 0 1 {r*1.4:.1f} 0" 
                      fill="none" stroke="url(#{gid1})" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>
                <path d="M -{r*1.4:.1f} 0 A {r*1.4:.1f} {r:.1f} 0 0 0 {r*1.4:.1f} 0" 
                      fill="none" stroke="url(#{gid2})" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>
                ''')
            elements.append(f'<circle cx="0" cy="0" r="38" fill="#020617" stroke="url(#{gid1})" stroke-width="4"/>')
            elements.append(f'<circle cx="0" cy="0" r="18" fill="url(#{gid2})"/>')
            elements.append('</g>')

        # -------------------------------------------------------------
        # Archetype 8: 'H' & 'S' Liquid Monograms (HyperSettle)
        # -------------------------------------------------------------
        elif archetype_id == 8:
            category = "Fluid Monogram Glyph"
            name = f"HyperSettle Glyph #{variant_num:02d}"
            # Fluid stylized 'H' and 'S' dynamic ribbon intertwine
            elements.append(f'''
            <g transform="translate({cx},{cy}) rotate({(variant_num-1)*10})">
                <!-- S-Wave Backbone -->
                <path d="M 80 -120 C -40 -120 -80 -40 0 0 C 80 40 40 120 -80 120" 
                      fill="none" stroke="url(#{gid1})" stroke-width="32" stroke-linecap="round"/>
                <!-- Intersecting H-Pillar Left -->
                <path d="M -90 -140 L -90 140" 
                      fill="none" stroke="url(#{gid2})" stroke-width="22" stroke-linecap="round" opacity="0.85"/>
                <!-- Intersecting H-Pillar Right -->
                <path d="M 90 -140 L 90 140" 
                      fill="none" stroke="url(#{gid2})" stroke-width="22" stroke-linecap="round" opacity="0.85"/>
                <!-- Accent Glowing Dots -->
                <circle cx="80" cy="-120" r="16" fill="#FFFFFF"/>
                <circle cx="-80" cy="120" r="16" fill="#98FCE4"/>
            </g>''')

        # -------------------------------------------------------------
        # Archetype 9: Harmonic Resonance & Standing Wave Nodes
        # -------------------------------------------------------------
        elif archetype_id == 9:
            category = "Harmonic Standing Wave"
            name = f"Harmonic Pulse #{variant_num:02d}"
            elements.append(f'<g transform="translate({cx},{cy})">')
            waves = 6
            for w in range(waves):
                r = 30 + w * 24
                sw = 6 + (w % 3) * 3
                rot = w * 18 + (variant_num * 12)
                elements.append(f'''
                <ellipse cx="0" cy="0" rx="{r*1.2:.1f}" ry="{r*0.8:.1f}" fill="none" 
                         stroke="url(#{gid1 if w%2==0 else gid2})" stroke-width="{sw}" 
                         transform="rotate({rot})" opacity="{0.95 - w*0.1}"/>
                ''')
            elements.append(f'<circle cx="0" cy="0" r="22" fill="#FFFFFF"/>')
            elements.append(f'<circle cx="0" cy="0" r="12" fill="url(#{gid1})"/>')
            elements.append('</g>')

        inner_body = "\n        ".join(elements)
        
        svg_code = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
    <defs>
        {grad1}
        {grad2}
        <radialGradient id="bgGlow_{idx}" cx="50%" cy="50%" r="65%">
            <stop offset="0%" stop-color="#0E1E1C" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#040608" stop-opacity="1.0"/>
        </radialGradient>
    </defs>
    <!-- Background Frame -->
    <rect width="512" height="512" rx="36" fill="url(#bgGlow_{idx})"/>
    <rect width="512" height="512" rx="36" fill="none" stroke="#1F2E2B" stroke-width="1.5"/>
    
    <!-- Vector Mark -->
    {inner_body}
</svg>'''
        
        fname = f"logo_{idx:03d}_{name.lower().replace(' ', '_').replace('#', '')}.svg"
        fpath = os.path.join(LOGOS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_code)
            
        logos.append({
            "id": idx,
            "filename": fname,
            "name": name,
            "category": category,
            "palette": pal,
            "svg": svg_code
        })
        
    print(f"Generated {len(logos)} multi-color logos in {LOGOS_DIR}")
    return logos

# -----------------------------------------------------------------------------
# BUILD INTERACTIVE HTML SHOWCASE
# -----------------------------------------------------------------------------
def build_html_showcase(cards, logos):
    categories = sorted(list(set(l["category"] for l in logos)))
    
    cards_html = []
    for fname, svg_code, title, desc in cards:
        cards_html.append(f'''
        <div class="card-item">
            <div class="card-preview">
                {svg_code}
            </div>
            <div class="card-meta">
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
                <div class="card-actions">
                    <a href="brand-cards/{fname}" download class="btn">Download SVG</a>
                    <button class="btn btn-secondary" onclick="copySvg(this, 'card-{fname}')">Copy SVG Code</button>
                    <textarea id="card-{fname}" style="display:none;">{svg_code}</textarea>
                </div>
            </div>
        </div>''')
    cards_section = "\n".join(cards_html)
    
    logos_json = json.dumps([{
        "id": l["id"],
        "name": l["name"],
        "category": l["category"],
        "filename": l["filename"]
    } for l in logos])

    logos_html = []
    for l in logos:
        logos_html.append(f'''
        <div class="logo-item" data-category="{l['category']}" data-id="{l['id']}">
            <div class="logo-preview">
                {l['svg']}
            </div>
            <div class="logo-info">
                <span class="logo-num">#{l['id']:03d}</span>
                <span class="logo-name">{l['name']}</span>
            </div>
            <div class="logo-actions">
                <a href="logos-100/{l['filename']}" download class="btn btn-sm">Download</a>
                <button class="btn btn-sm btn-secondary" onclick="copySvg(this, 'logo-{l['id']}')">Copy SVG</button>
                <textarea id="logo-{l['id']}" style="display:none;">{l['svg']}</textarea>
            </div>
        </div>''')
    logos_section = "\n".join(logos_html)

    cat_buttons = ['<button class="filter-btn active" onclick="filterLogos(\'all\', this)">All 100 Logos</button>']
    for cat in categories:
        cat_buttons.append(f'<button class="filter-btn" onclick="filterLogos(\'{cat}\', this)">{cat}</button>')
    cat_buttons_html = "\n".join(cat_buttons)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperSettle • Brand Cards &amp; 100 Multi-Color Logo Suite</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #030706;
            --surface: #0A1210;
            --surface-border: #162B26;
            --mint: #98FCE4;
            --solana: #9945FF;
            --cyan: #00E5FF;
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
            padding: 40px 24px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        /* Header */
        header {{
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 32px;
            margin-bottom: 48px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(152, 252, 228, 0.1);
            color: var(--mint);
            border: 1px solid rgba(152, 252, 228, 0.3);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 16px;
        }}
        h1 {{
            font-family: var(--font-sans);
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #FFFFFF 40%, var(--mint) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            color: var(--text-secondary);
            font-size: 16px;
            max-width: 780px;
        }}
        
        /* Section styling */
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 24px;
            padding-top: 24px;
            border-top: 1px solid var(--surface-border);
        }}
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .section-desc {{
            color: var(--text-secondary);
            font-size: 13px;
            margin-top: 4px;
        }}
        
        /* Brand Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
            gap: 28px;
            margin-bottom: 64px;
        }}
        .card-item {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 16px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card-item:hover {{
            border-color: var(--mint);
            transform: translateY(-2px);
        }}
        .card-preview {{
            background: #000000;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 200px;
        }}
        .card-meta {{
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex-grow: 1;
        }}
        .card-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--mint);
        }}
        .card-desc {{
            font-size: 12px;
            color: var(--text-secondary);
            flex-grow: 1;
        }}
        .card-actions {{
            display: flex;
            gap: 10px;
            margin-top: 12px;
        }}
        
        /* Button styling */
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            font-family: var(--font-mono);
            text-decoration: none;
            cursor: pointer;
            background: var(--mint);
            color: #030706;
            border: none;
            transition: opacity 0.15s;
        }}
        .btn:hover {{ opacity: 0.9; }}
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.15);
        }}
        .btn-sm {{
            padding: 6px 10px;
            font-size: 11px;
        }}
        
        /* 100 Logos Filter Bar */
        .filter-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 28px;
        }}
        .filter-btn {{
            background: var(--surface);
            color: var(--text-secondary);
            border: 1px solid var(--surface-border);
            padding: 7px 14px;
            border-radius: 999px;
            font-size: 12px;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: all 0.15s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--mint);
            color: #030706;
            border-color: var(--mint);
            font-weight: 700;
        }}
        
        /* 100 Logos Grid */
        .logos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 20px;
        }}
        .logo-item {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }}
        .logo-item:hover {{
            transform: translateY(-4px);
            border-color: var(--cyan);
            box-shadow: 0 10px 25px -5px rgba(0, 229, 255, 0.15);
        }}
        .logo-preview {{
            aspect-ratio: 1 / 1;
            background: #000000;
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }}
        .logo-info {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
        }}
        .logo-num {{
            font-size: 11px;
            color: var(--mint);
            font-weight: 700;
        }}
        .logo-name {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .logo-actions {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}
        
        /* Toast notification */
        #toast {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--mint);
            color: #030706;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            opacity: 0;
            transform: translateY(20px);
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
            <span class="badge">COLOSSEUM ETERNAL // PAYMENTS &amp; DEV TOOLS</span>
            <h1>HyperSettle Brand Suite</h1>
            <p class="subtitle">Brand card drafts featuring the 33rd Trees Tensor Arbor mathematical geometry and Obel Mono typography, paired with 100 multi-color fluid vector marks inspired by Hyperliquid.</p>
        </header>

        <!-- Section 1: 33rd Trees Brand Cards -->
        <div class="section-header">
            <div>
                <h2 class="section-title">Brand Card Drafts (33rd Trees Aesthetic)</h2>
                <p class="section-desc">Testing Mark #06 Exponential Plunge geometry with Obel Mono precision telemetry, dark obsidian palettes, and Hyperliquid/Solana accents.</p>
            </div>
        </div>
        <div class="cards-grid">
            {cards_section}
        </div>

        <!-- Section 2: 100 Multi-Color Logos -->
        <div class="section-header">
            <div>
                <h2 class="section-title">100 Multi-Color Fluid Logos (Hyperliquid Aesthetic)</h2>
                <p class="section-desc">Procedural iridescent gradients (Mint, Cyan, Solana Violet, Electric Blue, Neon Coral) across 10 distinct architectural archetypes.</p>
            </div>
        </div>

        <div class="filter-bar">
            {cat_buttons_html}
        </div>

        <div class="logos-grid" id="logosGrid">
            {logos_section}
        </div>
    </div>

    <div id="toast">SVG Code Copied to Clipboard!</div>

    <script>
        function filterLogos(category, btn) {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const items = document.querySelectorAll('.logo-item');
            items.forEach(item => {{
                if (category === 'all' || item.getAttribute('data-category') === category) {{
                    item.style.display = 'flex';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}

        function copySvg(btn, textareaId) {{
            const ta = document.getElementById(textareaId);
            navigator.clipboard.writeText(ta.value).then(() => {{
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            }});
        }}
    </script>
</body>
</html>'''

    with open(SHOWCASE_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated interactive showcase at {SHOWCASE_PATH}")

if __name__ == "__main__":
    cards = build_brand_cards()
    logos = build_100_logos()
    build_html_showcase(cards, logos)
    print("All branding assets successfully created!")

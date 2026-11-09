#!/usr/bin/env python3
"""
HyperSettle - Master Brand Card Generator
Adopts the 33rd Trees Tensor Arbor mathematical geometry and Obel Mono typography system.
Generates:
- Complete vector lockup asset inventory (Horizontal, Stacked, Icon, Token, Inverted, HUD, Banner)
- 12 distinct Token Chassis variations
- Interactive Brand Card Showcase HTML
- Comprehensive Brand Card Documentation (BRAND_CARD_SYSTEM.md)
"""

import os
import math

PROJECT_DIR = "/Users/ianmora/Desktop/Projects/HyperSettle/branding/brand-cards"
TOKEN_DIR = os.path.join(PROJECT_DIR, "token-versions")
SHOWCASE_HTML_PATH = os.path.join(PROJECT_DIR, "brand_cards_showcase.html")
DOCS_MD_PATH = os.path.join(PROJECT_DIR, "BRAND_CARD_SYSTEM.md")

os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(TOKEN_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# Exact Exponential Plunge Mathematical Radial Function (33rd Trees Arbor)
# -------------------------------------------------------------------------
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

def render_mark_elements(stroke_color="#FFFFFF", fill_throat="#FFFFFF", accent_color=None, stroke_mult=1.0):
    elems = []
    for frac in MERIDIAN_FRACTIONS:
        base_sw = 2.8 if frac == 1.0 else (2.0 if frac > 0.6 else 1.5)
        sw = f"{base_sw * stroke_mult:.2f}"
        op = "1.0" if frac == 1.0 else ("0.85" if frac > 0.6 else "0.7")
        col = stroke_color
        if accent_color and frac == 1.0:
            col = accent_color
        pts_l = make_curve_pts(frac, -1)
        pts_r = make_curve_pts(frac, 1)
        elems.append(f'<path d="{path_from_pts(pts_l)}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
        elems.append(f'<path d="{path_from_pts(pts_r)}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
        
    axis_col = accent_color if accent_color else stroke_color
    elems.append(f'<line x1="{CX}" y1="28" x2="{CX}" y2="212" stroke="{axis_col}" stroke-width="{1.8*stroke_mult:.2f}" stroke-dasharray="3 3" opacity="0.75"/>')

    for y in RING_YS:
        r = r_exp(y)
        ry = max(1.0, r * 0.22)
        if y == Y_THROAT:
            throat_col = accent_color if accent_color else fill_throat
            elems.append(f'<ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="{throat_col}" stroke="{stroke_color}" stroke-width="{2.5*stroke_mult:.2f}"/>')
        else:
            ring_sw = (1.8 if (y == Y_TOP or y == Y_BOTTOM) else 1.5) * stroke_mult
            ring_op = "0.9" if (y == Y_TOP or y == Y_BOTTOM) else "0.75"
            elems.append(f'<ellipse cx="{CX}" cy="{y}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="{stroke_color}" stroke-width="{ring_sw:.2f}" opacity="{ring_op}"/>')
            
    elems.append(f'<circle cx="{CX}" cy="26" r="{4.5*stroke_mult:.2f}" fill="{axis_col}"/>')
    elems.append(f'<circle cx="33.0" cy="38" r="{3.2*stroke_mult:.2f}" fill="{stroke_color}"/>')
    elems.append(f'<circle cx="207.0" cy="38" r="{3.2*stroke_mult:.2f}" fill="{stroke_color}"/>')
    return "\n        ".join(elems)

FONT_STACK = "'Obel Mono', 'Obelisk Mono', 'Space Mono', 'JetBrains Mono', monospace"

# Typography texts
NAME = "HYPERSETTLE"
LINE1_FULL = "HYPERSETTLE • REVENUE ENGINE"
LINE2_FULL = "HYPERCORE ATTRIBUTION // SOLANA SQUADS SETTLEMENT"
LINE_METRO = "PRECISION: 10^-6 USD • NON-CUSTODIAL • SQUADS BATCH EXPORT"

# -------------------------------------------------------------------------
# 1. CORE VECTOR LOCKUPS
# -------------------------------------------------------------------------
def generate_core_lockups():
    lockups = []

    # 1. Horizontal Monochrome Lockup (740 x 190)
    svg_h = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 190" width="100%" height="100%">
    <rect width="740" height="190" rx="20" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    <g transform="translate(24, 15) scale(0.68)">
        {render_mark_elements("#FFFFFF", "#FFFFFF")}
    </g>
    <g transform="translate(210, 74)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="24" fill="#FFFFFF" letter-spacing="2.5">{NAME}</tspan>
            <tspan font-weight="600" font-size="14" fill="#FFFFFF" opacity="0.8" letter-spacing="1.8"> • REVENUE ENGINE</tspan>
        </text>
        <line x1="0" y1="22" x2="495" y2="22" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.35"/>
        <text x="0" y="46" font-family="{FONT_STACK}" font-weight="600" font-size="12" fill="#FFFFFF" opacity="0.75" letter-spacing="2.2">{LINE2_FULL}</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-01-horizontal.svg", svg_h, "Primary Horizontal Lockup", "740 × 190 standard header & press lockup."))

    # 2. Stacked Centered Lockup (420 x 480)
    svg_s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 480" width="100%" height="100%">
    <rect width="420" height="480" rx="24" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    <g transform="translate(115, 35) scale(0.79)">
        {render_mark_elements("#FFFFFF", "#FFFFFF")}
    </g>
    <g transform="translate(210, 265)">
        <text x="0" y="0" text-anchor="middle" font-family="{FONT_STACK}" font-weight="800" font-size="28" fill="#FFFFFF" letter-spacing="3.5">{NAME}</text>
        <text x="0" y="28" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="13" fill="#FFFFFF" opacity="0.85" letter-spacing="2.4">REVENUE RECONCILIATION ENGINE</text>
        <line x1="-160" y1="48" x2="160" y2="48" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.35"/>
        <text x="0" y="74" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="11" fill="#FFFFFF" opacity="0.7" letter-spacing="2.0">HYPERCORE L1 // SOLANA SQUADS</text>
        <text x="0" y="98" text-anchor="middle" font-family="{FONT_STACK}" font-weight="400" font-size="9.5" fill="#FFFFFF" opacity="0.5" letter-spacing="1.5">{LINE_METRO}</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-02-stacked.svg", svg_s, "Vertical Stacked Lockup", "420 × 480 centered mobile splash & poster lockup."))

    # 3. Square Standalone Icon (256 x 256)
    svg_icon = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="100%" height="100%">
    <rect width="256" height="256" rx="28" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    <g transform="translate(20, 16) scale(0.9)">
        {render_mark_elements("#FFFFFF", "#FFFFFF", stroke_mult=1.1)}
    </g>
</svg>'''
    lockups.append(("hypersettle-03-icon.svg", svg_icon, "Square App Icon", "256 × 256 standalone profile & audit mark."))

    # 4. Inverted Black-on-White Icon (256 x 256)
    svg_icon_inv = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="100%" height="100%">
    <rect width="256" height="256" rx="28" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <g transform="translate(20, 16) scale(0.9)">
        {render_mark_elements("#000000", "#000000", stroke_mult=1.1)}
    </g>
</svg>'''
    lockups.append(("hypersettle-04-icon-inverted.svg", svg_icon_inv, "Inverted Editorial Icon", "256 × 256 black-on-white stationery & print mark."))

    # 5. Circular Medallion Token (360 x 360)
    svg_token = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="100%" height="100%">
    <rect width="360" height="360" fill="#000000" />
    <circle cx="180" cy="180" r="165" fill="#000000" stroke="#FFFFFF" stroke-width="2.5"/>
    <circle cx="180" cy="180" r="158" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="3 4" opacity="0.75"/>
    <circle cx="180" cy="180" r="148" fill="none" stroke="#FFFFFF" stroke-width="0.8" opacity="0.4"/>
    
    <!-- Cardinal Ticks -->
    <g stroke="#FFFFFF" stroke-width="1.5" opacity="0.9">
        <line x1="180" y1="15" x2="180" y2="30"/>
        <line x1="180" y1="330" x2="180" y2="345"/>
        <line x1="15" y1="180" x2="30" y2="180"/>
        <line x1="330" y1="180" x2="345" y2="180"/>
    </g>
    
    <g transform="translate(72, 60) scale(0.9)">
        {render_mark_elements("#FFFFFF", "#FFFFFF", stroke_mult=1.05)}
    </g>
</svg>'''
    lockups.append(("hypersettle-05-token.svg", svg_token, "Circular Medallion Token", "360 × 360 cryptocurrency token & hardware seal."))

    # 6. Horizontal Lockup with Token (780 x 220)
    svg_th = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 220" width="100%" height="100%">
    <rect width="780" height="220" rx="24" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    
    <!-- Token Left -->
    <g transform="translate(30, 20)">
        <circle cx="90" cy="90" r="82" fill="#000000" stroke="#FFFFFF" stroke-width="2"/>
        <circle cx="90" cy="90" r="76" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 4" opacity="0.7"/>
        <g transform="translate(30, 24) scale(0.5)">
            {render_mark_elements("#FFFFFF", "#FFFFFF")}
        </g>
    </g>
    
    <!-- Wordmark Right -->
    <g transform="translate(240, 88)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="28" fill="#FFFFFF" letter-spacing="3.0">{NAME}</tspan>
            <tspan font-weight="600" font-size="14" fill="#FFFFFF" opacity="0.8" letter-spacing="1.8"> • FINOPS ENGINE</tspan>
        </text>
        <line x1="0" y1="26" x2="500" y2="26" stroke="#FFFFFF" stroke-width="1.4" stroke-opacity="0.35"/>
        <text x="0" y="52" font-family="{FONT_STACK}" font-weight="600" font-size="12.5" fill="#FFFFFF" opacity="0.8" letter-spacing="2.2">{LINE2_FULL}</text>
        <text x="0" y="76" font-family="{FONT_STACK}" font-weight="400" font-size="10" fill="#FFFFFF" opacity="0.5" letter-spacing="1.6">{LINE_METRO}</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-06-token-horizontal.svg", svg_th, "Token Horizontal Lockup", "780 × 220 executive lockup pairing circular medallion with Obel Mono."))

    # 7. Stacked Token Lockup (440 x 520)
    svg_ts = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 520" width="100%" height="100%">
    <rect width="440" height="520" rx="28" fill="#000000" stroke="#222222" stroke-width="1.5"/>
    
    <!-- Token Center -->
    <g transform="translate(130, 40)">
        <circle cx="90" cy="90" r="82" fill="#000000" stroke="#FFFFFF" stroke-width="2"/>
        <circle cx="90" cy="90" r="76" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 4" opacity="0.7"/>
        <g transform="translate(30, 24) scale(0.5)">
            {render_mark_elements("#FFFFFF", "#FFFFFF")}
        </g>
    </g>
    
    <!-- Typography Stacked Below -->
    <g transform="translate(220, 290)">
        <text x="0" y="0" text-anchor="middle" font-family="{FONT_STACK}" font-weight="800" font-size="32" fill="#FFFFFF" letter-spacing="4">{NAME}</text>
        <text x="0" y="32" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="13" fill="#FFFFFF" opacity="0.85" letter-spacing="2.5">REVENUE RECONCILIATION ENGINE</text>
        <line x1="-170" y1="56" x2="170" y2="56" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.35"/>
        <text x="0" y="84" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="11.5" fill="#FFFFFF" opacity="0.75" letter-spacing="2.2">HYPERCORE L1 // SOLANA SQUADS</text>
        <text x="0" y="110" text-anchor="middle" font-family="{FONT_STACK}" font-weight="400" font-size="9.5" fill="#FFFFFF" opacity="0.5" letter-spacing="1.5">{LINE_METRO}</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-07-token-stacked.svg", svg_ts, "Token Stacked Lockup", "440 × 520 vertical lockup with central coin and structured metadata."))

    # 8. Hyperliquid Mint Edition Horizontal (740 x 190)
    svg_mint_h = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 190" width="100%" height="100%">
    <defs>
        <linearGradient id="hlMintSol" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
    </defs>
    <rect width="740" height="190" rx="20" fill="#040807" stroke="#163832" stroke-width="1.5"/>
    <g transform="translate(24, 15) scale(0.68)">
        {render_mark_elements("#E0FFF8", "#98FCE4", accent_color="#98FCE4")}
    </g>
    <g transform="translate(210, 74)">
        <text x="0" y="0" font-family="{FONT_STACK}">
            <tspan font-weight="800" font-size="24" fill="#98FCE4" letter-spacing="2.5">{NAME}</tspan>
            <tspan font-weight="600" font-size="14" fill="#E0FFF8" opacity="0.85" letter-spacing="1.8"> • FINOPS PROTOCOL</tspan>
        </text>
        <line x1="0" y1="22" x2="495" y2="22" stroke="url(#hlMintSol)" stroke-width="1.6" stroke-opacity="0.85"/>
        <text x="0" y="46" font-family="{FONT_STACK}" font-weight="600" font-size="12" fill="#E0FFF8" opacity="0.8" letter-spacing="2.2">L1 BUILDER CODE REVENUE // DETERMINISTIC MICRO-USD SPLIT</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-08-mint-edition-horizontal.svg", svg_mint_h, "Hyperliquid Mint Edition", "740 × 190 electric mint (#98FCE4) with Solana cross-chain gradient."))

    # 9. Tactical Sci-Fi HUD Card (520 x 420)
    svg_hud = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" width="100%" height="100%">
    <defs>
        <pattern id="hudGrid" width="20" height="20" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="20" y2="0" stroke="#FFFFFF" stroke-width="0.5" stroke-opacity="0.04"/>
            <line x1="0" y1="0" x2="0" y2="20" stroke="#FFFFFF" stroke-width="0.5" stroke-opacity="0.04"/>
        </pattern>
    </defs>
    <rect width="520" height="420" rx="24" fill="#040608" stroke="#1F2937" stroke-width="1.5"/>
    <rect width="520" height="420" fill="url(#hudGrid)" rx="24"/>
    
    <!-- Top HUD telemetry bar -->
    <text x="32" y="40" font-family="{FONT_STACK}" font-size="10" fill="#98FCE4" letter-spacing="2">SYS_ID: HYPE_SETTLE // CORE_V04</text>
    <text x="488" y="40" text-anchor="end" font-family="{FONT_STACK}" font-size="10" fill="#6B7280" letter-spacing="1.5">PRECISION: 10^-6 USD</text>
    <line x1="32" y1="50" x2="488" y2="50" stroke="#374151" stroke-width="1"/>
    
    <!-- Centered Mark -->
    <g transform="translate(196, 65) scale(0.53)">
        {render_mark_elements("#FFFFFF", "#98FCE4", accent_color="#98FCE4")}
    </g>
    
    <!-- Main Center Titles -->
    <text x="260" y="222" text-anchor="middle" font-family="{FONT_STACK}" font-weight="800" font-size="28" fill="#FFFFFF" letter-spacing="3.5">{NAME}</text>
    <text x="260" y="248" text-anchor="middle" font-family="{FONT_STACK}" font-weight="600" font-size="13" fill="#98FCE4" letter-spacing="2.5">DECENTRALIZED BUILDER SETTLEMENTS</text>
    
    <line x1="60" y1="268" x2="460" y2="268" stroke="#374151" stroke-width="1" stroke-dasharray="4 4"/>
    
    <!-- Coordinate Telemetry Block -->
    <g transform="translate(60, 294)">
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
    lockups.append(("hypersettle-09-tactical-hud.svg", svg_hud, "Tactical Sci-Fi HUD Brand Card", "520 × 420 telemetry grid card with corner reticles and status readout."))

    # 10. Pitch Deck / Social Hero Banner (1200 x 630)
    svg_banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
    <defs>
        <radialGradient id="bannerBg" cx="30%" cy="50%" r="70%">
            <stop offset="0%" stop-color="#0B1A17"/>
            <stop offset="50%" stop-color="#040807"/>
            <stop offset="100%" stop-color="#000000"/>
        </radialGradient>
        <linearGradient id="glowRule" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#98FCE4"/>
            <stop offset="50%" stop-color="#00E5FF"/>
            <stop offset="100%" stop-color="#9945FF"/>
        </linearGradient>
    </defs>
    <rect width="1200" height="630" fill="url(#bannerBg)"/>
    
    <!-- Outer framing grid -->
    <line x1="80" y1="80" x2="1120" y2="80" stroke="#1F3D37" stroke-width="1"/>
    <line x1="80" y1="550" x2="1120" y2="550" stroke="#1F3D37" stroke-width="1"/>
    <line x1="80" y1="80" x2="80" y2="550" stroke="#1F3D37" stroke-width="1"/>
    <line x1="1120" y1="80" x2="1120" y2="550" stroke="#1F3D37" stroke-width="1"/>
    
    <!-- Scaled Mark Left -->
    <g transform="translate(130, 160) scale(1.4)">
        {render_mark_elements("#FFFFFF", "#98FCE4", accent_color="#98FCE4")}
    </g>
    
    <!-- Typography Right -->
    <g transform="translate(540, 260)">
        <text x="0" y="0" font-family="{FONT_STACK}" font-size="14" fill="#98FCE4" letter-spacing="4">COLOSSEUM ETERNAL // PAYMENTS &amp; DEV TOOLS</text>
        <text x="0" y="55" font-family="{FONT_STACK}" font-weight="800" font-size="52" fill="#FFFFFF" letter-spacing="4">{NAME}</text>
        <line x1="0" y1="85" x2="580" y2="85" stroke="url(#glowRule)" stroke-width="3"/>
        <text x="0" y="125" font-family="{FONT_STACK}" font-weight="600" font-size="18" fill="#E0FFF8" opacity="0.9" letter-spacing="2">HYPERLIQUID BUILDER REVENUE ATTRIBUTION</text>
        <text x="0" y="155" font-family="{FONT_STACK}" font-weight="500" font-size="16" fill="#9CA3AF" letter-spacing="1.8">NON-CUSTODIAL SOLANA USDC SQUADS SETTLEMENTS</text>
        
        <rect x="0" y="195" width="220" height="42" rx="8" fill="#133830" stroke="#98FCE4" stroke-width="1.5"/>
        <text x="110" y="222" text-anchor="middle" font-family="{FONT_STACK}" font-weight="700" font-size="13" fill="#98FCE4" letter-spacing="2.2">PRECISION 10^-6 USD</text>
    </g>
</svg>'''
    lockups.append(("hypersettle-10-social-banner.svg", svg_banner, "Social & Pitch Deck Hero Banner", "1200 × 630 high-impact presentation slide & GitHub preview."))

    for fname, svg_str, title, desc in lockups:
        fpath = os.path.join(PROJECT_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_str)

    print(f"Generated {len(lockups)} core brand cards in {PROJECT_DIR}")
    return lockups

# -------------------------------------------------------------------------
# 2. GENERATE THE 12 TOKEN CHASSIS VARIATIONS
# -------------------------------------------------------------------------
def generate_12_tokens():
    tokens = []
    
    # Template chassis generator with central 33rd arbor mark
    def make_token_chassis(num, key, title, desc, extra_svg):
        vb = "0 0 480 340"
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="100%" height="100%">
    <rect width="480" height="340" fill="#000000" />
    
    <!-- Central Coin Perimeter (cx=240, cy=170, r=142) -->
    <circle cx="240" cy="170" r="142" fill="#000000" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="240" cy="170" r="136" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 5" opacity="0.75"/>
    
    <!-- Central Mark (scale 0.72) -->
    <g transform="translate(153, 94) scale(0.72)">
        {render_mark_elements("#FFFFFF", "#FFFFFF")}
    </g>
    
    <!-- Outer Horizontal Typography (Unclipped, Overhanging Circle) -->
    <text x="240" y="32" font-family="{FONT_STACK}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="3.8">{LINE1_FULL}</text>
    <text x="240" y="318" font-family="{FONT_STACK}" font-size="8.5" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="3.2">{LINE2_FULL}</text>
    
    <!-- Architectural Chassis Elements -->
    {extra_svg}
</svg>'''
        fname = f"hypersettle-token-{num:02d}-{key}.svg"
        fpath = os.path.join(TOKEN_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg)
        tokens.append((fname, svg, f"Token {num:02d} • {title}", desc))

    # 01. Extended Horizon
    extra_01 = '''
    <g stroke="#FFFFFF" stroke-width="1.5" opacity="0.85">
        <line x1="240" y1="20" x2="240" y2="34"/>
        <line x1="240" y1="306" x2="240" y2="320"/>
        <line x1="90" y1="170" x2="104" y2="170"/>
        <line x1="376" y1="170" x2="390" y2="170"/>
    </g>'''
    make_token_chassis(1, "extended-horizon", "Extended Horizon", "Pure unclipped original with cardinal metrology markers.", extra_01)

    # 02. Laser Datum Axis
    extra_02 = '''
    <line x1="20" y1="170" x2="460" y2="170" stroke="#FFFFFF" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.5"/>
    <circle cx="20" cy="170" r="2.5" fill="#FFFFFF"/>
    <circle cx="460" cy="170" r="2.5" fill="#FFFFFF"/>'''
    make_token_chassis(2, "laser-datum-axis", "Laser Datum Axis", "Horizontal laser alignment plane passing through the singularity throat.", extra_02)

    # 03. Terminal Brackets
    extra_03 = '''
    <g stroke="#FFFFFF" stroke-width="1.8" fill="none">
        <path d="M 40 22 L 28 22 L 28 42"/>
        <path d="M 440 22 L 452 22 L 452 42"/>
        <path d="M 40 326 L 28 326 L 28 306"/>
        <path d="M 440 326 L 452 326 L 452 306"/>
    </g>'''
    make_token_chassis(3, "terminal-brackets", "Terminal Brackets", "Corner HUD brackets framing the typography and central coin.", extra_03)

    # 04. Notched Perimeter
    extra_04 = '''
    <g stroke="#FFFFFF" stroke-width="2" opacity="0.8">
        <line x1="240" y1="12" x2="240" y2="28"/>
        <line x1="240" y1="312" x2="240" y2="328"/>
        <circle cx="98" cy="170" r="3" fill="#FFFFFF"/>
        <circle cx="382" cy="170" r="3" fill="#FFFFFF"/>
    </g>'''
    make_token_chassis(4, "notched-perimeter", "Notched Perimeter", "Hardware perimeter keying notches along cardinal axes.", extra_04)

    # 05. Square Polar Exterior
    extra_05 = '''
    <rect x="70" y="20" width="340" height="300" fill="none" stroke="#FFFFFF" stroke-width="1.0" opacity="0.35"/>
    <line x1="240" y1="20" x2="240" y2="320" stroke="#FFFFFF" stroke-width="0.8" stroke-dasharray="4 4" opacity="0.3"/>'''
    make_token_chassis(5, "square-polar-exterior", "Square Polar Exterior", "Concentric square bounding chassis with polar division guides.", extra_05)

    # 06. Orbital Concentric
    extra_06 = '''
    <circle cx="240" cy="170" r="156" fill="none" stroke="#FFFFFF" stroke-width="0.6" stroke-dasharray="2 4" opacity="0.4"/>
    <circle cx="240" cy="170" r="164" fill="none" stroke="#FFFFFF" stroke-width="1.0" opacity="0.6"/>'''
    make_token_chassis(6, "orbital-concentric", "Orbital Concentric", "Dual nested planetary orbits creating a technical celestial seal.", extra_06)

    # 07. Sci-Fi Chassis
    extra_07 = '''
    <path d="M 60 40 L 420 40 L 450 70 L 450 270 L 420 300 L 60 300 L 30 270 L 30 70 Z" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.4"/>'''
    make_token_chassis(7, "sci-fi-chassis", "Sci-Fi Chassis", "Chamfered octagonal flight-computer perimeter frame.", extra_07)

    # 08. Laboratory Telemetry
    extra_08 = '''
    <text x="36" y="174" font-family="{FONT_STACK}" font-size="8" fill="#FFFFFF" opacity="0.6" letter-spacing="1.5">HYPERCORE</text>
    <text x="444" y="174" text-anchor="end" font-family="{FONT_STACK}" font-size="8" fill="#FFFFFF" opacity="0.6" letter-spacing="1.5">10^-6 USD</text>'''
    make_token_chassis(8, "laboratory-telemetry", "Laboratory Telemetry", "Subtle side telemetric coordinate readouts flanking the central coin.", extra_08)

    # 09. Minimalist Pure
    extra_09 = '''
    <!-- Pure minimal baseline without additional ornamentation -->'''
    make_token_chassis(9, "minimalist-pure", "Minimalist Pure", "Stripped to absolute essentials: pure circle, arbor, and typography.", extra_09)

    # 10. Cartesian Reticle
    extra_10 = '''
    <circle cx="240" cy="170" r="6" fill="none" stroke="#FFFFFF" stroke-width="1"/>
    <line x1="220" y1="170" x2="260" y2="170" stroke="#FFFFFF" stroke-width="0.8"/>
    <line x1="240" y1="150" x2="240" y2="190" stroke="#FFFFFF" stroke-width="0.8"/>'''
    make_token_chassis(10, "cartesian-reticle", "Cartesian Reticle", "Precision targeting crosshairs superimposed over singularity throat.", extra_10)

    # 11. Pill Horizon Capsule
    extra_11 = '''
    <rect x="50" y="15" width="380" height="310" rx="40" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.45"/>'''
    make_token_chassis(11, "pill-horizon-capsule", "Pill Horizon Capsule", "Curved capsule perimeter housing matching contemporary hardware keyfobs.", extra_11)

    # 12. Cryptographic Metadata
    extra_12 = '''
    <text x="240" y="52" font-family="{FONT_STACK}" font-size="7" fill="#FFFFFF" opacity="0.45" text-anchor="middle" letter-spacing="2">0x4859504552534554544C45</text>
    <text x="240" y="298" font-family="{FONT_STACK}" font-size="7" fill="#FFFFFF" opacity="0.45" text-anchor="middle" letter-spacing="2">SQUADS_MULTISIG_V4 // ZERO_CUSTODY</text>'''
    make_token_chassis(12, "cryptographic-metadata", "Cryptographic Metadata", "Microscopic hexadecimal and contract telemetry tags top and bottom.", extra_12)

    print(f"Generated 12 token chassis variations in {TOKEN_DIR}")
    return tokens

# -------------------------------------------------------------------------
# 3. BUILD INTERACTIVE SHOWCASE HTML FOR BRAND CARDS
# -------------------------------------------------------------------------
def build_brand_cards_html(core_lockups, token_versions):
    def render_gallery_items(items, download_subdir=""):
        cards_html = []
        for fname, svg_code, title, desc in items:
            href_path = f"{download_subdir}{fname}" if download_subdir else fname
            ta_id = f"copy-{fname.replace('.', '_')}"
            cards_html.append(f'''
            <div class="brand-card-item">
                <div class="card-canvas">
                    {svg_code}
                </div>
                <div class="card-details">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                    <div class="card-buttons">
                        <a href="{href_path}" download class="btn-primary">Download SVG</a>
                        <button class="btn-secondary" onclick="copySvgCode('{ta_id}')">Copy SVG Code</button>
                        <textarea id="{ta_id}" style="display:none;">{svg_code}</textarea>
                    </div>
                </div>
            </div>''')
        return "\n".join(cards_html)

    core_html = render_gallery_items(core_lockups, "")
    tokens_html = render_gallery_items(token_versions, "token-versions/")

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperSettle • Brand Card System &amp; Design Architecture</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #000000;
            --surface: #0A0A0C;
            --surface-border: #1E1E24;
            --mint: #98FCE4;
            --solana: #9945FF;
            --text-primary: #FFFFFF;
            --text-muted: #8E8E93;
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
        .container {{ max-width: 1380px; margin: 0 auto; }}
        
        header {{
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 36px;
            margin-bottom: 48px;
        }}
        .badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
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
        }}
        .subtitle {{
            color: var(--text-muted);
            font-size: 16px;
            max-width: 840px;
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
            color: var(--text-muted);
            font-family: var(--font-mono);
            font-size: 14px;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active, .tab-btn:hover {{
            color: #000000;
            background: #FFFFFF;
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
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 4px;
        }}
        
        /* Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 32px;
            margin-bottom: 64px;
        }}
        .brand-card-item {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s, transform 0.2s;
        }}
        .brand-card-item:hover {{
            border-color: #FFFFFF;
            transform: translateY(-2px);
        }}
        .card-canvas {{
            background: #000000;
            padding: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 240px;
            border-bottom: 1px solid var(--surface-border);
        }}
        .card-details {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex-grow: 1;
        }}
        .card-title {{
            font-size: 16px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        .card-desc {{
            font-size: 13px;
            color: var(--text-muted);
            flex-grow: 1;
        }}
        .card-buttons {{
            display: flex;
            gap: 12px;
            margin-top: 14px;
        }}
        
        /* Buttons */
        .btn-primary {{
            padding: 10px 18px;
            background: #FFFFFF;
            color: #000000;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            font-size: 12px;
            border: none;
            cursor: pointer;
            transition: opacity 0.15s;
        }}
        .btn-primary:hover {{ opacity: 0.9; }}
        .btn-secondary {{
            padding: 10px 18px;
            background: rgba(255, 255, 255, 0.08);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            font-weight: 700;
            font-size: 12px;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.16);
        }}
        
        /* Toast */
        #toast {{
            position: fixed;
            bottom: 32px;
            right: 32px;
            background: #FFFFFF;
            color: #000000;
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
            <span class="badge">33RD TREES SPECIFICATION // OBEL MONO TYPOGRAPHY</span>
            <h1>HyperSettle Brand Card System</h1>
            <p class="subtitle">Complete vector identity suite adopting the 33rd Trees Tensor Arbor mathematical geometry, high-contrast monospace typography, and precision financial telemetry for Colosseum Eternal.</p>
        </header>

        <div class="tab-bar">
            <button class="tab-btn active" onclick="switchTab('core', this)">Core Lockup Suite (10 Cards)</button>
            <button class="tab-btn" onclick="switchTab('tokens', this)">12 Architectural Token Chassis</button>
        </div>

        <!-- Tab 1: Core Lockup Suite -->
        <div id="tab-core">
            <div class="section-header">
                <h2 class="section-title">Core Vector Lockup Suite</h2>
                <p class="section-desc">Primary horizontal lockups, centered splash locks, square app icons, inverted stationery, and pitch deck hero banners.</p>
            </div>
            <div class="cards-grid">
                {core_html}
            </div>
        </div>

        <!-- Tab 2: 12 Token Chassis -->
        <div id="tab-tokens" style="display:none;">
            <div class="section-header">
                <h2 class="section-title">12 Architectural Token Chassis</h2>
                <p class="section-desc">Straight horizontal Obel Mono typography overhanging circular medallion perimeters with zero edge-clipping across 12 distinct engineering frames.</p>
            </div>
            <div class="cards-grid">
                {tokens_html}
            </div>
        </div>
    </div>

    <div id="toast">SVG Vector Code Copied!</div>

    <script>
        function switchTab(tabName, btn) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (tabName === 'core') {{
                document.getElementById('tab-core').style.display = 'block';
                document.getElementById('tab-tokens').style.display = 'none';
            }} else {{
                document.getElementById('tab-core').style.display = 'none';
                document.getElementById('tab-tokens').style.display = 'block';
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

    with open(SHOWCASE_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated brand cards showcase at {SHOWCASE_HTML_PATH}")

# -------------------------------------------------------------------------
# 4. BUILD BRAND_CARD_SYSTEM.MD SPECIFICATION DOCUMENT
# -------------------------------------------------------------------------
def build_brand_docs():
    doc = f'''# HyperSettle Brand Card Identity System

> **Brand**: HyperSettle  
> **Geometry**: 33rd Trees Tensor Arbor #06 (Singularity Curvature)  
> **Typography**: Obel Mono (Fixed-Width Technical Grotesque)  
> **Aesthetic Standard**: High-Contrast Vector Metrology (`#000000` & `#FFFFFF`) with Hyperliquid Mint (`#98FCE4`) & Solana Spectral Accents  

---

## 1. Executive Summary & Brand Thesis

HyperSettle bridges two distinct cryptographic ecosystems:
1. **HyperCore L1**: The high-throughput matching engine where $65M+ in builder fee volume is generated.
2. **Solana**: The standard treasury, multisig (Squads), and settlement layer for crypto teams.

To communicate trust, mathematical precision, and zero-custodial safety, HyperSettle adopts the **33rd Trees Tensor Arbor #06** identity system:
* **The Mathematical Curvature**: An exponential gravitational divergence function modeling the unyielding cryptographic anchor (the singularity throat) branching into an unbounded canopy of distributed trading revenue.
* **The Monospace Metrology**: All characters conform to strict tabular monospace cells (`Obel Mono`), reflecting deterministic integer micro-USD precision ($10^{{-6}}$ USD) where rounding errors are strictly forbidden.

---

## 2. Typographic Standard: Obel Mono

* **Primary Typeface**: `Obel Mono` (System Fallbacks: `Space Mono`, `JetBrains Mono`, `monospace`)
* **Kerning & Tracking Principles**:
  * **Primary Wordmark**: `HYPERSETTLE` (Weight: 800 / Extra Bold, Tracking: `+0.25em` to `+0.35em`).
  * **Secondary Technical Tagline**: `HYPERCORE ATTRIBUTION // SOLANA SQUADS SETTLEMENT` (Weight: 600 / Semi-Bold, Tracking: `+0.22em`).
  * **Micro Metrology Readout**: `PRECISION: 10^-6 USD • NON-CUSTODIAL • SQUADS BATCH EXPORT` (Weight: 400, Tracking: `+0.15em`).

---

## 3. Core Vector Lockup Asset Inventory

All vector assets are stored as clean SVGs in `branding/brand-cards/`:

| File Name | Dimensions | Primary Role |
| :--- | :--- | :--- |
| **`hypersettle-01-horizontal.svg`** | 740 × 190 | Primary horizontal lockup for documentation, web headers, and navigation bars. |
| **`hypersettle-02-stacked.svg`** | 420 × 480 | Vertical centered lockup for mobile splash screens, poster prints, and pitch cards. |
| **`hypersettle-03-icon.svg`** | 256 × 256 | High-contrast black square standalone icon for avatars, app icons, and badges. |
| **`hypersettle-04-icon-inverted.svg`** | 256 × 256 | Crisp paper-white inverted icon for printed contracts, PDFs, and invoices. |
| **`hypersettle-05-token.svg`** | 360 × 360 | Circular medallion token with perimeter ticks for cryptocurrency icons and hardware seals. |
| **`hypersettle-06-token-horizontal.svg`** | 780 × 220 | Horizontal lockup pairing the circular medallion token with Obel Mono typography. |
| **`hypersettle-07-token-stacked.svg`** | 440 × 520 | Vertical lockup with central coin and structured telemetry metadata. |
| **`hypersettle-08-mint-edition-horizontal.svg`** | 740 × 190 | Hyperliquid electric mint (`#98FCE4`) with cross-chain Solana spectral gradient. |
| **`hypersettle-09-tactical-hud.svg`** | 520 × 420 | Military-grade HUD telemetry grid card with corner reticles and verified status readout. |
| **`hypersettle-10-social-banner.svg`** | 1200 × 630 | Widescreen presentation slide and GitHub OpenGraph preview card. |

---

## 4. The 12 Architectural Token Chassis

Stored in `branding/brand-cards/token-versions/`:

1. **`hypersettle-token-01-extended-horizon.svg`**: Unclipped original with cardinal metrology markers.
2. **`hypersettle-token-02-laser-datum-axis.svg`**: Horizontal laser alignment plane passing through singularity throat.
3. **`hypersettle-token-03-terminal-brackets.svg`**: Corner HUD brackets framing the typography and central coin.
4. **`hypersettle-token-04-notched-perimeter.svg`**: Hardware perimeter keying notches along cardinal axes.
5. **`hypersettle-token-05-square-polar-exterior.svg`**: Concentric square bounding chassis with polar division guides.
6. **`hypersettle-token-06-orbital-concentric.svg`**: Dual nested planetary orbits creating a technical celestial seal.
7. **`hypersettle-token-07-sci-fi-chassis.svg`**: Chamfered octagonal flight-computer perimeter frame.
8. **`hypersettle-token-08-laboratory-telemetry.svg`**: Subtle side telemetric coordinate readouts flanking the coin.
9. **`hypersettle-token-09-minimalist-pure.svg`**: Stripped to absolute essentials: pure circle, arbor, and typography.
10. **`hypersettle-token-10-cartesian-reticle.svg`**: Precision targeting crosshairs superimposed over singularity throat.
11. **`hypersettle-token-11-pill-horizon-capsule.svg`**: Curved capsule perimeter housing matching contemporary hardware keyfobs.
12. **`hypersettle-token-12-cryptographic-metadata.svg`**: Microscopic hexadecimal and contract telemetry tags top and bottom.

---

## 5. Color Palette Tokens

| Token Name | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Singularity Void** | `#000000` | Primary canvas & absolute negative space. |
| **High-Voltage White** | `#FFFFFF` | Primary vector paths, Obel Mono wordmark & singularity core. |
| **Hyperliquid Mint** | `#98FCE4` | Primary brand accent for status indicators, active fees, and highlights. |
| **HyperCore Teal** | `#0F3933` | Background depth, card borders, and HUD reticle accents. |
| **Solana Violet** | `#9945FF` | Settlement execution indicator & Squads multisig bridge tags. |
| **Telemetry Grey** | `#9CA3AF` | Metrology text, coordinate labels, and micro-USD precision markers. |
'''
    with open(DOCS_MD_PATH, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Generated brand docs at {DOCS_MD_PATH}")

if __name__ == "__main__":
    core = generate_core_lockups()
    tokens = generate_12_tokens()
    build_brand_cards_html(core, tokens)
    build_brand_docs()
    print("HyperSettle Brand Card system successfully generated!")

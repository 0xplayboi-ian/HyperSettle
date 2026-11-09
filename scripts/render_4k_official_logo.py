#!/usr/bin/env python3
"""
HyperSettle 4K Ultra-Resolution Logo Engine (4096 x 4096 & 3840 x 2160)
Generates high-resolution 4K JPGs, 4K Transparent PNGs, and Vector SVGs
for the official Goursat Hypersurface Wave (#34) 3D mathematical mark.
Uses 2x Supersample Anti-Aliasing (8192x8192 -> 4096x4096 LANCZOS).
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = '/Users/ianmora/Desktop/Projects/HyperSettle'
OUT_DIR = os.path.join(BASE_DIR, 'branding', 'official-logo')
OUT_4K_DIR = os.path.join(OUT_DIR, '4k-resolution')
os.makedirs(OUT_4K_DIR, exist_ok=True)

# 4K Canvas Parameters
DIM_4K = 4096
DIM_SSAA = 8192  # 2x supersampling for ultra-crisp antialiasing

# Three.js Perspective Camera matching 3d_parametric_studio.html
cam_x, cam_y, cam_z = 3.5, 2.5, 4.5
dist = math.sqrt(cam_x**2 + cam_y**2 + cam_z**2)
fwd = np.array([-cam_x/dist, -cam_y/dist, -cam_z/dist])
right = np.array([-fwd[2], 0, fwd[0]])
right /= np.linalg.norm(right)
up = np.cross(right, fwd)

fov_deg = 40.0
half_h = math.tan(math.radians(fov_deg / 2))
half_w = half_h  # Square canvas

def project_point(x, y, z, canvas_dim=DIM_SSAA):
    dx, dy, dz = x - cam_x, y - cam_y, z - cam_z
    depth = dx * fwd[0] + dy * fwd[1] + dz * fwd[2]
    cam_r = dx * right[0] + dy * right[1] + dz * right[2]
    cam_u = dx * up[0] + dy * up[1] + dz * up[2]
    
    ndc_x = cam_r / (depth * half_w)
    ndc_y = cam_u / (depth * half_h)
    
    # Scale factor so the mark fills ~75% of the square canvas cleanly
    scale = 1.34
    sx = (ndc_x * scale + 1.0) * 0.5 * canvas_dim
    sy = (1.0 - ndc_y * scale) * 0.5 * canvas_dim
    return sx, sy

def compute_grid(res, canvas_dim=DIM_SSAA):
    u_vals = np.linspace(0, 1, res + 1)
    v_vals = np.linspace(0, 1, res + 1)
    grid = []
    for i in range(res + 1):
        row = []
        for j in range(res + 1):
            u = u_vals[i] * 2 * math.pi
            v = (v_vals[j] - 0.5) * 2.2
            x = math.sin(u) * math.cosh(v) * 0.65
            y = math.sin(2 * u) * 0.7
            z = math.cos(u) * math.sinh(v) * 0.65
            row.append(project_point(x, y, z, canvas_dim))
        grid.append(row)
    return grid

def render_4k_wireframe(res, line_width_ssaa, bg_color, stroke_color, is_transparent=False):
    """Render at 8192x8192 with 2x SSAA, then downsample to 4096x4096 with Lanczos"""
    grid = compute_grid(res, DIM_SSAA)
    
    if is_transparent:
        img_ssaa = Image.new('RGBA', (DIM_SSAA, DIM_SSAA), (0, 0, 0, 0))
    else:
        img_ssaa = Image.new('RGB', (DIM_SSAA, DIM_SSAA), bg_color)
    
    draw = ImageDraw.Draw(img_ssaa)
    
    # Draw quad perimeters + diagonal triangulation matching Three.js WireframeGeometry
    for i in range(res):
        for j in range(res):
            p0 = grid[i][j]
            p1 = grid[i+1][j]
            p2 = grid[i+1][j+1]
            p3 = grid[i][j+1]
            
            draw.line([p0, p1], fill=stroke_color, width=line_width_ssaa)
            draw.line([p1, p2], fill=stroke_color, width=line_width_ssaa)
            draw.line([p2, p3], fill=stroke_color, width=line_width_ssaa)
            draw.line([p3, p0], fill=stroke_color, width=line_width_ssaa)
            draw.line([p0, p2], fill=stroke_color, width=line_width_ssaa)
            
    # Downsample to 4096 x 4096 with Lanczos antialiasing
    img_4k = img_ssaa.resize((DIM_4K, DIM_4K), Image.Resampling.LANCZOS)
    return img_4k

# Colors
COLOR_NAVY = (13, 27, 42)           # #0D1B2A Curve Deep Navy
COLOR_WHITE = (255, 255, 255)       # Pure White
COLOR_MINT = (0, 245, 212)          # #00F5D4 Hyperliquid Mint
COLOR_CYAN = (0, 229, 255)          # #00E5FF Electric Cyan
BG_WHITE = (255, 255, 255)
BG_OBSIDIAN = (3, 7, 6)             # #030706 Obsidian Void

print("Generating 4K Ultra-Resolution Suite (4096 x 4096)...")

# --- 1. 4K Ultra-Res JPGs ---
# A. Curve Pure White background, Navy wireframe (Fine Mesh, res=36)
img_white_fine = render_4k_wireframe(36, 7, BG_WHITE, COLOR_NAVY, False)
p_white_fine = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-curve-white.jpg')
img_white_fine.save(p_white_fine, quality=98)
img_white_fine.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-light.jpg'), quality=98)
print(f"  ✓ Saved 4K JPG: {p_white_fine}")

# B. Obsidian Dark background, Pure White wireframe (Fine Mesh, res=36)
img_dark_white = render_4k_wireframe(36, 7, BG_OBSIDIAN, COLOR_WHITE, False)
p_dark_white = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-obsidian-dark.jpg')
img_dark_white.save(p_dark_white, quality=98)
img_dark_white.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-dark.jpg'), quality=98)
print(f"  ✓ Saved 4K JPG: {p_dark_white}")

# C. Obsidian Dark background, Hyperliquid Mint wireframe (Fine Mesh, res=36)
img_dark_mint = render_4k_wireframe(36, 7, BG_OBSIDIAN, COLOR_MINT, False)
p_dark_mint = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-hyperliquid-mint.jpg')
img_dark_mint.save(p_dark_mint, quality=98)
img_dark_mint.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-mint.jpg'), quality=98)
print(f"  ✓ Saved 4K JPG: {p_dark_mint}")

# D. Obsidian Dark background, Electric Cyan wireframe
img_dark_cyan = render_4k_wireframe(36, 7, BG_OBSIDIAN, COLOR_CYAN, False)
p_dark_cyan = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-electric-cyan.jpg')
img_dark_cyan.save(p_dark_cyan, quality=98)
img_dark_cyan.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-cyan.jpg'), quality=98)
print(f"  ✓ Saved 4K JPG: {p_dark_cyan}")

# E. Bold / Coarse Quad Mesh on Pure White (res=18, line_width=10)
img_bold_white = render_4k_wireframe(18, 10, BG_WHITE, COLOR_NAVY, False)
p_bold_white = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-bold-quads-light.jpg')
img_bold_white.save(p_bold_white, quality=98)
img_bold_white.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-bold-light.jpg'), quality=98)
img_bold_white.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-light.png'))
print(f"  ✓ Saved 4K Bold JPG & PNG: {p_bold_white}")

# F. Bold / Coarse Quad Mesh on Obsidian Dark
img_bold_dark = render_4k_wireframe(18, 10, BG_OBSIDIAN, COLOR_MINT, False)
p_bold_dark = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-bold-quads-dark.jpg')
img_bold_dark.save(p_bold_dark, quality=98)
img_bold_dark.save(os.path.join(OUT_DIR, 'hypersettle-mark-4k-bold-dark.jpg'), quality=98)
print(f"  ✓ Saved 4K Bold Dark JPG: {p_bold_dark}")


# --- 2. 4K Ultra-Res Transparent PNGs (32-Bit Alpha) ---
print("Generating 4K Transparent PNGs (4096 x 4096)...")

# A. Transparent Navy
img_trans_navy = render_4k_wireframe(36, 7, None, (13, 27, 42, 255), True)
p_trans_navy = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-transparent-navy.png')
img_trans_navy.save(p_trans_navy)
img_trans_navy.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-navy.png'))
print(f"  ✓ Saved 4K Transparent PNG: {p_trans_navy}")

# B. Transparent White
img_trans_white = render_4k_wireframe(36, 7, None, (255, 255, 255, 255), True)
p_trans_white = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-transparent-white.png')
img_trans_white.save(p_trans_white)
img_trans_white.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-white.png'))
print(f"  ✓ Saved 4K Transparent PNG: {p_trans_white}")

# C. Transparent Mint (#00F5D4)
img_trans_mint = render_4k_wireframe(36, 7, None, (0, 245, 212, 255), True)
p_trans_mint = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-transparent-mint.png')
img_trans_mint.save(p_trans_mint)
img_trans_mint.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-mint.png'))
print(f"  ✓ Saved 4K Transparent PNG: {p_trans_mint}")

# D. Transparent Cyan (#00E5FF)
img_trans_cyan = render_4k_wireframe(36, 7, None, (0, 229, 255, 255), True)
p_trans_cyan = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-transparent-cyan.png')
img_trans_cyan.save(p_trans_cyan)
img_trans_cyan.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-cyan.png'))
print(f"  ✓ Saved 4K Transparent PNG: {p_trans_cyan}")

# E. Bold Transparent Navy
img_bold_trans_navy = render_4k_wireframe(18, 10, None, (13, 27, 42, 255), True)
p_bold_trans_navy = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-bold-transparent-navy.png')
img_bold_trans_navy.save(p_bold_trans_navy)
img_bold_trans_navy.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-transparent-navy.png'))
print(f"  ✓ Saved 4K Bold Transparent PNG: {p_bold_trans_navy}")

# F. Bold Transparent Mint
img_bold_trans_mint = render_4k_wireframe(18, 10, None, (0, 245, 212, 255), True)
p_bold_trans_mint = os.path.join(OUT_4K_DIR, 'hypersettle-4k-mark-bold-transparent-mint.png')
img_bold_trans_mint.save(p_bold_trans_mint)
img_bold_trans_mint.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-transparent-mint.png'))
print(f"  ✓ Saved 4K Bold Transparent PNG: {p_bold_trans_mint}")


# --- 3. 4K UHD 16:9 Presentation & Social Banner (3840 x 2160) ---
print("Generating 4K UHD 16:9 Presentation Banner (3840 x 2160)...")
bw, bh = 3840, 2160
banner = Image.new('RGB', (bw, bh), (4, 8, 7))
b_draw = ImageDraw.Draw(banner)

# Technical coordinate grid
for x in range(0, bw, 80):
    b_draw.line([(x, 0), (x, bh)], fill=(12, 24, 21), width=1)
for y in range(0, bh, 80):
    b_draw.line([(0, y), (bw, y)], fill=(12, 24, 21), width=1)

# Outer architectural border
b_draw.rectangle([(40, 40), (bw - 41, bh - 41)], outline=(22, 38, 34), width=3)
corner_len = 80
b_draw.line([(40, 40), (40 + corner_len, 40)], fill=(0, 245, 212), width=6)
b_draw.line([(40, 40), (40, 40 + corner_len)], fill=(0, 245, 212), width=6)
b_draw.line([(bw - 41, 40), (bw - 41 - corner_len, 40)], fill=(0, 245, 212), width=6)
b_draw.line([(bw - 41, 40), (bw - 41, 40 + corner_len)], fill=(0, 245, 212), width=6)
b_draw.line([(40, bh - 41), (40 + corner_len, bh - 41)], fill=(0, 245, 212), width=6)
b_draw.line([(40, bh - 41), (40, bh - 41 - corner_len)], fill=(0, 245, 212), width=6)
b_draw.line([(bw - 41, bh - 41), (bw - 41 - corner_len, bh - 41)], fill=(0, 245, 212), width=6)
b_draw.line([(bw - 41, bh - 41), (bw - 41, bh - 41 - corner_len)], fill=(0, 245, 212), width=6)

# Paste 4K Mint Mark on right side (height 1750)
mark_h = 1750
mark_w = 1750
resized_mark = img_trans_mint.resize((mark_w, mark_h), Image.Resampling.LANCZOS)
banner.paste(resized_mark, (bw - mark_w - 180, (bh - mark_h) // 2), resized_mark)

# Typography
f_helv_hero = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 170, index=1)
f_helv_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 68, index=0)
f_menlo_badge = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 48, index=1)
f_menlo_meta = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 38, index=0)

tx = 180
# Badge
b_draw.rounded_rectangle([tx, 260, tx + 940, 345], radius=16, fill=(0, 43, 36))
b_draw.text((tx + 36, 280), "COLOSSEUM ETERNAL SPRINT // 2026", fill=(0, 245, 212), font=f_menlo_badge)

# Title
b_draw.text((tx, 420), "HyperSettle", fill=(255, 255, 255), font=f_helv_hero)

# Tagline
b_draw.text((tx, 660), "Non-Custodial Revenue Reconciliation\n& Solana Settlement Engine", fill=(226, 232, 240), font=f_helv_sub)

# Description
b_draw.text((tx, 900), "Ingesting L1 HyperCore builder fees with ~0.2s finality.\nEnforcing deterministic integer micro-USD splits ($10⁻⁶).\nExporting Squads V4 multisig batch payouts in SPL USDC.", fill=(148, 163, 184), font=f_menlo_meta)

# Technical Specs Box
specs = [
    ("FINALITY", "~0.2s HyperBFT"),
    ("PRECISION", "10⁻⁶ Micro-USD"),
    ("SETTLEMENT", "Squads V4 Multisig"),
    ("GEOMETRY", "Goursat Manifold #34")
]
sp_x = tx
for label, val in specs:
    b_draw.rounded_rectangle([sp_x, 1420, sp_x + 360, 1580], radius=16, fill=(10, 18, 16), outline=(22, 38, 34))
    b_draw.text((sp_x + 28, 1450), label, fill=(100, 116, 139), font=f_menlo_meta)
    b_draw.text((sp_x + 28, 1505), val, fill=(0, 245, 212), font=f_menlo_badge)
    sp_x += 390

p_banner = os.path.join(OUT_4K_DIR, 'hypersettle-4k-social-banner-3840x2160.jpg')
banner.save(p_banner, quality=98)
print(f"  ✓ Saved 4K UHD Banner: {p_banner}")


# --- 4. Infinite-Resolution Vector SVG ---
print("Generating Infinite-Resolution Lossless Vector SVG...")
svg_grid = compute_grid(36, 4096)
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4096 4096" width="100%" height="100%">
  <defs>
    <style>
      .wire-edge {{ stroke: #0D1B2A; stroke-width: 3.5; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    </style>
  </defs>
  <rect width="4096" height="4096" fill="#FFFFFF"/>
'''

# Draw lines in SVG
for i in range(36):
    for j in range(36):
        p0 = svg_grid[i][j]
        p1 = svg_grid[i+1][j]
        p2 = svg_grid[i+1][j+1]
        p3 = svg_grid[i][j+1]
        
        svg_content += f'  <line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" class="wire-edge"/>\n'
        svg_content += f'  <line x1="{p1[0]:.2f}" y1="{p1[1]:.2f}" x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" class="wire-edge"/>\n'
        svg_content += f'  <line x1="{p2[0]:.2f}" y1="{p2[1]:.2f}" x2="{p3[0]:.2f}" y2="{p3[1]:.2f}" class="wire-edge"/>\n'
        svg_content += f'  <line x1="{p3[0]:.2f}" y1="{p3[1]:.2f}" x2="{p0[0]:.2f}" y2="{p0[1]:.2f}" class="wire-edge"/>\n'
        svg_content += f'  <line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" class="wire-edge"/>\n'

svg_content += '</svg>'
p_svg = os.path.join(OUT_4K_DIR, 'hypersettle-mark-vector-lossless.svg')
with open(p_svg, 'w') as f:
    f.write(svg_content)
with open(os.path.join(OUT_DIR, 'hypersettle-mark-vector.svg'), 'w') as f:
    f.write(svg_content)
print(f"  ✓ Saved Lossless Vector SVG: {p_svg}")

print("\nAll 4K Ultra-Resolution assets generated successfully!")

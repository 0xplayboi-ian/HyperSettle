#!/usr/bin/env python3
"""
HyperSettle Official Logo Processor & Brand Asset Generator
Processes the user-selected mathematical 3D differential geometry logo mark:
- Crops to geometric bounding box with square and optical balancing
- Extracts transparent alpha channel (matte removal)
- Produces Curve Navy, Hyperliquid Mint, Electric Cyan, Pure White, and Dark Mode assets
- Generates official horizontal and vertical brand lockups with typography
- Creates social banner (1200x630) and square avatar (800x800)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC_PATH = '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222138914_a557b919.jpg'
BASE_DIR = '/Users/ianmora/Desktop/Projects/HyperSettle'
OUT_DIR = os.path.join(BASE_DIR, 'branding', 'official-logo')
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load source image
img = Image.open(SRC_PATH).convert('RGB')
arr = np.array(img).astype(np.float32)

# Save original copy
img.save(os.path.join(OUT_DIR, 'hypersettle-logo-original.jpg'), quality=95)

# 2. Compute background & foreground mask
# Background is pure white ~255
# Invert brightness: 255 - grayscale gives line density
gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]
density = 255.0 - gray

# Bounding box of significant lines (> 5 threshold)
y_indices, x_indices = np.where(density > 8)
ymin, ymax = y_indices.min(), y_indices.max()
xmin, xmax = x_indices.min(), x_indices.max()

print(f"Detected logo bounding box: X=[{xmin}, {xmax}] (w={xmax-xmin}), Y=[{ymin}, {ymax}] (h={ymax-ymin})")

# Add 4% padding around mark
pad_x = int((xmax - xmin) * 0.04)
pad_y = int((ymax - ymin) * 0.04)
crop_box = (max(0, xmin - pad_x), max(0, ymin - pad_y), min(img.width, xmax + pad_x), min(img.height, ymax + pad_y))
cropped = img.crop(crop_box)
cropped.save(os.path.join(OUT_DIR, 'hypersettle-mark-tight.png'))

# 3. Create high-precision Transparent Alpha version
# For each pixel, alpha = (255 - gray) / 255 * scale
crop_arr = np.array(cropped).astype(np.float32)
crop_gray = 0.299 * crop_arr[:,:,0] + 0.587 * crop_arr[:,:,1] + 0.114 * crop_arr[:,:,2]
alpha_channel = np.clip((255.0 - crop_gray) * 1.6, 0, 255).astype(np.uint8)

# Color variants on transparent background
# A. Original Curve Deep Navy (#0D1B2A / #1E293B)
h, w = cropped.height, cropped.width
navy_rgba = np.zeros((h, w, 4), dtype=np.uint8)
navy_rgba[:, :, 0] = 13  # R
navy_rgba[:, :, 1] = 27  # G
navy_rgba[:, :, 2] = 42  # B
navy_rgba[:, :, 3] = alpha_channel
img_navy_trans = Image.fromarray(navy_rgba, 'RGBA')
img_navy_trans.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-navy.png'))

# B. Pure White Transparent (for dark backgrounds)
white_rgba = np.zeros((h, w, 4), dtype=np.uint8)
white_rgba[:, :, 0] = 255
white_rgba[:, :, 1] = 255
white_rgba[:, :, 2] = 255
white_rgba[:, :, 3] = alpha_channel
img_white_trans = Image.fromarray(white_rgba, 'RGBA')
img_white_trans.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-white.png'))

# C. Hyperliquid Mint Transparent (#00F5D4)
mint_rgba = np.zeros((h, w, 4), dtype=np.uint8)
mint_rgba[:, :, 0] = 0
mint_rgba[:, :, 1] = 245
mint_rgba[:, :, 2] = 212
mint_rgba[:, :, 3] = alpha_channel
img_mint_trans = Image.fromarray(mint_rgba, 'RGBA')
img_mint_trans.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-mint.png'))

# D. Electric Cyan Transparent (#00E5FF)
cyan_rgba = np.zeros((h, w, 4), dtype=np.uint8)
cyan_rgba[:, :, 0] = 0
cyan_rgba[:, :, 1] = 229
cyan_rgba[:, :, 2] = 255
cyan_rgba[:, :, 3] = alpha_channel
img_cyan_trans = Image.fromarray(cyan_rgba, 'RGBA')
img_cyan_trans.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-cyan.png'))

# 4. Square Icons (800x800)
def make_square_avatar(mark_trans, bg_color, out_filename):
    avatar = Image.new('RGBA', (800, 800), bg_color)
    # Fit mark inside 540x540
    aspect = mark_trans.width / mark_trans.height
    if aspect > 1:
        nw = 540
        nh = int(540 / aspect)
    else:
        nh = 540
        nw = int(540 * aspect)
    resized = mark_trans.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (800 - nw) // 2
    y = (800 - nh) // 2
    avatar.paste(resized, (x, y), resized)
    avatar.save(os.path.join(OUT_DIR, out_filename))

# Light mode square avatar
make_square_avatar(img_navy_trans, (255, 255, 255, 255), 'hypersettle-avatar-light-800x800.png')
# Dark mode obsidian square avatar
make_square_avatar(img_mint_trans, (3, 7, 6, 255), 'hypersettle-avatar-dark-800x800.png')
# Deep navy square avatar
make_square_avatar(img_cyan_trans, (10, 17, 40, 255), 'hypersettle-avatar-navy-800x800.png')

# 5. Favicon suite
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
img_navy_trans.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, 'favicon-32x32.png'))
img_mint_trans.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, 'favicon-mint-32x32.png'))
img_navy_trans.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, 'apple-touch-icon.png'))

print("✓ Base marks, transparent variants, and avatars generated successfully!")


# --- 6. Brand Lockups with Typography ---
font_helvetica_bold = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72, index=1)
font_helvetica_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28, index=0)
font_menlo_bold = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 22, index=1)
font_menlo_reg = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16, index=0)

def generate_horizontal_lockup(mark_img, bg_color, text_color, sub_color, badge_bg, badge_text, out_path):
    w, h = 1400, 480
    canvas = Image.new('RGBA', (w, h), bg_color)
    draw = ImageDraw.Draw(canvas)

    aspect = mark_img.width / mark_img.height
    mark_h = 340
    mark_w = int(mark_h * aspect)
    mark_resized = mark_img.resize((mark_w, mark_h), Image.Resampling.LANCZOS)
    
    mark_x = 70
    mark_y = (h - mark_h) // 2
    canvas.paste(mark_resized, (mark_x, mark_y), mark_resized)

    tx = mark_x + mark_w + 60
    
    badge_str = "COLOSSEUM ETERNAL // HYPERLIQUID DEX → SOLANA"
    badge_bbox = draw.textbbox((0, 0), badge_str, font=font_menlo_bold)
    bw = badge_bbox[2] - badge_bbox[0] + 20
    bh = badge_bbox[3] - badge_bbox[1] + 12
    draw.rounded_rectangle([tx, 90, tx + bw, 90 + bh], radius=6, fill=badge_bg)
    draw.text((tx + 10, 96), badge_str, fill=badge_text, font=font_menlo_bold)

    draw.text((tx, 140), "HyperSettle", fill=text_color, font=font_helvetica_bold)
    draw.text((tx, 240), "Non-Custodial Revenue Reconciliation & Solana Settlement", fill=sub_color, font=font_helvetica_med)

    meta = "DIFFERENTIAL GEOMETRY ARBOR #01 • SQUADS V4 MULTISIG COMPATIBLE • SPL USDC"
    draw.text((tx, 290), meta, fill=sub_color, font=font_menlo_reg)

    canvas.save(out_path, quality=95)
    print(f"✓ Saved horizontal lockup: {out_path}")

# Light mode horizontal lockup
generate_horizontal_lockup(
    img_navy_trans,
    (255, 255, 255, 255),
    (13, 27, 42, 255),
    (100, 116, 139, 255),
    (241, 245, 249, 255),
    (2, 132, 199, 255),
    os.path.join(OUT_DIR, 'hypersettle-lockup-horizontal-light.png')
)

# Dark mode horizontal lockup
generate_horizontal_lockup(
    img_mint_trans,
    (3, 7, 6, 255),
    (255, 255, 255, 255),
    (148, 163, 184, 255),
    (0, 43, 36, 255),
    (0, 245, 212, 255),
    os.path.join(OUT_DIR, 'hypersettle-lockup-horizontal-dark.png')
)

# --- 7. GitHub & Social Card Banner (1200 x 630) ---
def generate_social_card():
    w, h = 1200, 630
    card = Image.new('RGBA', (w, h), (4, 8, 7, 255))
    draw = ImageDraw.Draw(card)

    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(12, 24, 21, 255), width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(12, 24, 21, 255), width=1)

    draw.rectangle([(16, 16), (w - 17, h - 17)], outline=(22, 38, 34, 255), width=2)
    corner_len = 24
    draw.line([(16, 16), (16 + corner_len, 16)], fill=(0, 245, 212, 255), width=3)
    draw.line([(16, 16), (16, 16 + corner_len)], fill=(0, 245, 212, 255), width=3)
    draw.line([(w - 17, 16), (w - 17 - corner_len, 16)], fill=(0, 245, 212, 255), width=3)
    draw.line([(w - 17, 16), (w - 17, 16 + corner_len)], fill=(0, 245, 212, 255), width=3)

    aspect = img_mint_trans.width / img_mint_trans.height
    mark_h = 440
    mark_w = int(mark_h * aspect)
    mark_resized = img_mint_trans.resize((mark_w, mark_h), Image.Resampling.LANCZOS)
    card.paste(mark_resized, (w - mark_w - 70, (h - mark_h) // 2), mark_resized)

    lx = 64
    draw.rounded_rectangle([lx, 70, lx + 360, 102], radius=6, fill=(0, 43, 36, 255))
    draw.text((lx + 14, 78), "COLOSSEUM ETERNAL SPRINT", fill=(0, 245, 212, 255), font=font_menlo_bold)

    draw.text((lx, 130), "HyperSettle", fill=(255, 255, 255, 255), font=font_helvetica_bold)
    draw.text((lx, 230), "Non-Custodial Revenue Engine\nfor Hyperliquid Builders", fill=(226, 232, 240, 255), font=font_helvetica_med)

    draw.text((lx, 330), "Settling L1 DEX fees to Solana contributors & treasury.", fill=(148, 163, 184, 255), font=font_menlo_reg)
    draw.text((lx, 360), "100% Non-Custodial • Squads V4 Batch Export • Zero Key Risk", fill=(56, 189, 248, 255), font=font_menlo_reg)

    pills = [("SPEED", "~0.2s Finality"), ("PRECISION", "10⁻⁶ USDC"), ("SOLANA", "SPL Pay")]
    px = lx
    for label, val in pills:
        draw.rounded_rectangle([px, 440, px + 150, 500], radius=8, fill=(10, 18, 16, 255), outline=(22, 38, 34, 255))
        draw.text((px + 12, 450), label, fill=(100, 116, 139, 255), font=font_menlo_reg)
        draw.text((px + 12, 472), val, fill=(0, 245, 212, 255), font=font_menlo_bold)
        px += 166

    out_card = os.path.join(OUT_DIR, 'hypersettle-social-card-1200x630.png')
    card.save(out_card, quality=95)
    print(f"✓ Saved social card: {out_card}")

generate_social_card()

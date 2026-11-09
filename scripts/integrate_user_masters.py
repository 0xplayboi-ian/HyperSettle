#!/usr/bin/env python3
"""
HyperSettle Master Logo Integrator
Ingests the 5 user-curated master exports from the 3D Parametric Studio:
1. Fine Wireframe Transparent Navy (PNG)
2. Fine Wireframe Dark Solid (JPG)
3. Fine Wireframe Light Solid (JPG)
4. Fine Wireframe Transparent White (PNG)
5. Bold / Coarse Geometric Wireframe (JPG)
Produces the complete final production suite across all formats, badges, lockups, and social cards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

USER_UPLOADS = {
    'trans_navy': '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516739_99f28d7c.png',
    'dark_solid': '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516768_dc0792c1.jpg',
    'light_solid': '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516783_899fac65.jpg',
    'trans_white': '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516747_7752edb9.png',
    'bold_wire': '/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516795_24ae3984.jpg'
}

BASE_DIR = '/Users/ianmora/Desktop/Projects/HyperSettle'
OUT_DIR = os.path.join(BASE_DIR, 'branding', 'official-logo')
MASTERS_DIR = os.path.join(OUT_DIR, 'user-masters')
os.makedirs(MASTERS_DIR, exist_ok=True)

# 1. Archive the 5 user masters
shutil.copy(USER_UPLOADS['trans_navy'], os.path.join(MASTERS_DIR, '01_master_trans_navy.png'))
shutil.copy(USER_UPLOADS['dark_solid'], os.path.join(MASTERS_DIR, '02_master_dark_solid.jpg'))
shutil.copy(USER_UPLOADS['light_solid'], os.path.join(MASTERS_DIR, '03_master_light_solid.jpg'))
shutil.copy(USER_UPLOADS['trans_white'], os.path.join(MASTERS_DIR, '04_master_trans_white.png'))
shutil.copy(USER_UPLOADS['bold_wire'], os.path.join(MASTERS_DIR, '05_master_bold_wire.jpg'))
print("✓ Preserved all 5 user masters in branding/official-logo/user-masters/")

# 2. Tight bounding box crop on the transparent navy master
im_trans_navy = Image.open(USER_UPLOADS['trans_navy'])
arr_navy = np.array(im_trans_navy)
alpha_navy = arr_navy[:, :, 3]

y_idxs, x_idxs = np.where(alpha_navy > 10)
ymin, ymax = y_idxs.min(), y_idxs.max()
xmin, xmax = x_idxs.min(), x_idxs.max()
print(f"Master tight crop: X=[{xmin}, {xmax}] (w={xmax-xmin}), Y=[{ymin}, {ymax}] (h={ymax-ymin})")

pad_x = int((xmax - xmin) * 0.04)
pad_y = int((ymax - ymin) * 0.04)
crop_box = (max(0, xmin - pad_x), max(0, ymin - pad_y), min(im_trans_navy.width, xmax + pad_x), min(im_trans_navy.height, ymax + pad_y))

mark_navy = im_trans_navy.crop(crop_box)
mark_navy.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-navy.png'))

im_trans_white = Image.open(USER_UPLOADS['trans_white'])
mark_white = im_trans_white.crop(crop_box)
mark_white.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-white.png'))

# 3. Create Mint & Cyan Tinted versions using exact alpha mask
w, h = mark_navy.width, mark_navy.height
alpha_cropped = np.array(mark_navy)[:, :, 3]

# Hyperliquid Mint (#00F5D4)
mint_rgba = np.zeros((h, w, 4), dtype=np.uint8)
mint_rgba[:, :, 0] = 0
mint_rgba[:, :, 1] = 245
mint_rgba[:, :, 2] = 212
mint_rgba[:, :, 3] = alpha_cropped
mark_mint = Image.fromarray(mint_rgba, 'RGBA')
mark_mint.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-mint.png'))

# Electric Cyan (#00E5FF)
cyan_rgba = np.zeros((h, w, 4), dtype=np.uint8)
cyan_rgba[:, :, 0] = 0
cyan_rgba[:, :, 1] = 229
cyan_rgba[:, :, 2] = 255
cyan_rgba[:, :, 3] = alpha_cropped
mark_cyan = Image.fromarray(cyan_rgba, 'RGBA')
mark_cyan.save(os.path.join(OUT_DIR, 'hypersettle-mark-transparent-cyan.png'))

# 4. Process the Bold / Coarse Wireframe Master (Image 5)
im_bold = Image.open(USER_UPLOADS['bold_wire']).convert('RGB')
arr_bold = np.array(im_bold).astype(np.float32)
gray_bold = 0.299 * arr_bold[:,:,0] + 0.587 * arr_bold[:,:,1] + 0.114 * arr_bold[:,:,2]
density_bold = 255.0 - gray_bold
by_idxs, bx_idxs = np.where(density_bold > 8)
bymin, bymax = by_idxs.min(), by_idxs.max()
bxmin, bxmax = bx_idxs.min(), bx_idxs.max()

b_crop_box = (max(0, bxmin - pad_x), max(0, bymin - pad_y), min(im_bold.width, bxmax + pad_x), min(im_bold.height, bymax + pad_y))
cropped_bold = im_bold.crop(b_crop_box)
cropped_bold.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-light.png'))

# Create transparent bold version
bold_arr = np.array(cropped_bold).astype(np.float32)
bold_gray = 0.299 * bold_arr[:,:,0] + 0.587 * bold_arr[:,:,1] + 0.114 * bold_arr[:,:,2]
bold_alpha = np.clip((255.0 - bold_gray) * 1.5, 0, 255).astype(np.uint8)

bold_navy_rgba = np.zeros((cropped_bold.height, cropped_bold.width, 4), dtype=np.uint8)
bold_navy_rgba[:, :, 0] = 13
bold_navy_rgba[:, :, 1] = 27
bold_navy_rgba[:, :, 2] = 42
bold_navy_rgba[:, :, 3] = bold_alpha
mark_bold_navy = Image.fromarray(bold_navy_rgba, 'RGBA')
mark_bold_navy.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-transparent-navy.png'))

bold_mint_rgba = np.zeros((cropped_bold.height, cropped_bold.width, 4), dtype=np.uint8)
bold_mint_rgba[:, :, 0] = 0
bold_mint_rgba[:, :, 1] = 245
bold_mint_rgba[:, :, 2] = 212
bold_mint_rgba[:, :, 3] = bold_alpha
mark_bold_mint = Image.fromarray(bold_mint_rgba, 'RGBA')
mark_bold_mint.save(os.path.join(OUT_DIR, 'hypersettle-mark-bold-transparent-mint.png'))

# 5. Generate Square 800x800 Avatars
def make_square_avatar(mark_img, bg_color, out_filename):
    avatar = Image.new('RGBA', (800, 800), bg_color)
    aspect = mark_img.width / mark_img.height
    if aspect > 1:
        nw = 560
        nh = int(560 / aspect)
    else:
        nh = 560
        nw = int(560 * aspect)
    resized = mark_img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (800 - nw) // 2
    y = (800 - nh) // 2
    avatar.paste(resized, (x, y), resized)
    avatar.save(os.path.join(OUT_DIR, out_filename))

make_square_avatar(mark_navy, (255, 255, 255, 255), 'hypersettle-avatar-light-800x800.png')
make_square_avatar(mark_white, (3, 7, 6, 255), 'hypersettle-avatar-dark-white-800x800.png')
make_square_avatar(mark_mint, (3, 7, 6, 255), 'hypersettle-avatar-dark-800x800.png')
make_square_avatar(mark_bold_navy, (255, 255, 255, 255), 'hypersettle-avatar-bold-light-800x800.png')
make_square_avatar(mark_bold_mint, (3, 7, 6, 255), 'hypersettle-avatar-bold-dark-800x800.png')

# 6. Generate Horizontal Typography Lockups (1400 x 480)
font_helvetica_bold = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72, index=1)
font_helvetica_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28, index=0)
font_menlo_bold = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 22, index=1)
font_menlo_reg = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16, index=0)

def generate_lockup(mark_img, bg_color, text_color, sub_color, badge_bg, badge_text, out_path):
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
generate_lockup(
    mark_navy,
    (255, 255, 255, 255),
    (13, 27, 42, 255),
    (100, 116, 139, 255),
    (241, 245, 249, 255),
    (2, 132, 199, 255),
    os.path.join(OUT_DIR, 'hypersettle-lockup-horizontal-light.png')
)

# Dark mode horizontal lockup with Mint
generate_lockup(
    mark_mint,
    (3, 7, 6, 255),
    (255, 255, 255, 255),
    (148, 163, 184, 255),
    (0, 43, 36, 255),
    (0, 245, 212, 255),
    os.path.join(OUT_DIR, 'hypersettle-lockup-horizontal-dark.png')
)

# Dark mode horizontal lockup with White wireframe
generate_lockup(
    mark_white,
    (3, 7, 6, 255),
    (255, 255, 255, 255),
    (148, 163, 184, 255),
    (20, 30, 28, 255),
    (255, 255, 255, 255),
    os.path.join(OUT_DIR, 'hypersettle-lockup-horizontal-dark-white.png')
)

# 7. Generate Social Banner (1200 x 630)
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

    aspect = mark_mint.width / mark_mint.height
    mark_h = 450
    mark_w = int(mark_h * aspect)
    mark_resized = mark_mint.resize((mark_w, mark_h), Image.Resampling.LANCZOS)
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
print("✓ Master integration and asset generation completed successfully!")

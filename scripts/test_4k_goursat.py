#!/usr/bin/env python3
"""
Test 4K Goursat Surface Projector
Renders Goursat Hypersurface Wave (#34) at 4096x4096 using exact Three.js perspective camera
"""

import math
import numpy as np
from PIL import Image, ImageDraw

WIDTH = 4096
HEIGHT = 4096

# Three.js Perspective Camera
cam_x, cam_y, cam_z = 3.5, 2.5, 4.5
dist = math.sqrt(cam_x**2 + cam_y**2 + cam_z**2)
fwd = np.array([-cam_x/dist, -cam_y/dist, -cam_z/dist])
right = np.array([-fwd[2], 0, fwd[0]])
right = right / np.linalg.norm(right)
up = np.cross(right, fwd)

fov_deg = 40.0
half_h = math.tan(math.radians(fov_deg / 2))
half_w = half_h * (WIDTH / HEIGHT) # 1.0 for square

def project_point(x, y, z):
    # Vector from camera
    dx = x - cam_x
    dy = y - cam_y
    dz = z - cam_z
    
    depth = dx * fwd[0] + dy * fwd[1] + dz * fwd[2]
    cam_r = dx * right[0] + dy * right[1] + dz * right[2]
    cam_u = dx * up[0] + dy * up[1] + dz * up[2]
    
    ndc_x = cam_r / (depth * half_w)
    ndc_y = cam_u / (depth * half_h)
    
    # Screen coordinates in [0, WIDTH] and [0, HEIGHT]
    # We apply optical centering and scale so it fills 75% of canvas
    scale = 1.35
    sx = (ndc_x * scale + 1.0) * 0.5 * WIDTH
    sy = (1.0 - ndc_y * scale) * 0.5 * HEIGHT
    return sx, sy

def generate_mesh_lines(res_u, res_v):
    # Goursat surface
    u_vals = np.linspace(0, 1, res_u)
    v_vals = np.linspace(0, 1, res_v)
    
    grid = []
    for i in range(res_u):
        row = []
        for j in range(res_v):
            u = u_vals[i] * 2 * math.pi
            v = (v_vals[j] - 0.5) * 2.2
            # Shape 34 Three.js target.set(x, y, z):
            # target.set(Math.sin(u)*Math.cosh(v)*0.65, Math.sin(2*u)*0.7, Math.cos(u)*Math.sinh(v)*0.65);
            # Three.js: X is right, Y is up, Z is forward
            x = math.sin(u) * math.cosh(v) * 0.65
            y = math.sin(2*u) * 0.7
            z = math.cos(u) * math.sinh(v) * 0.65
            sx, sy = project_point(x, y, z)
            row.append((sx, sy))
        grid.append(row)
    return grid

# Test with res=36 (fine mesh)
grid = generate_mesh_lines(36, 36)

# Render on 4096 x 4096 canvas
img = Image.new('RGB', (WIDTH, HEIGHT), '#FFFFFF')
draw = ImageDraw.Draw(img)

# Line width 4.5px at 4096 resolution = perfectly crisp fine line
stroke_color = (13, 27, 42) # #0D1B2A Curve Navy

# U-lines
for i in range(len(grid)):
    for j in range(len(grid[i]) - 1):
        draw.line([grid[i][j], grid[i][j+1]], fill=stroke_color, width=4)

# V-lines
for j in range(len(grid[0])):
    for i in range(len(grid) - 1):
        draw.line([grid[i][j], grid[i+1][j]], fill=stroke_color, width=4)

# Connect periodic U loop (u goes 0 to 2pi)
for j in range(len(grid[0])):
    draw.line([grid[-1][j], grid[0][j]], fill=stroke_color, width=4)

img.save('/tmp/test_4k_goursat.jpg', quality=95)
print("✓ Saved /tmp/test_4k_goursat.jpg at 4096x4096!")

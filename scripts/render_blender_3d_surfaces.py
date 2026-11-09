#!/usr/bin/env python3
"""
HyperSettle Blender 3D Wireframe Render Pipeline
Renders 10 mathematical differential geometry surfaces using Blender's Cycles/Eevee engine.
"""

import os
import sys
import json
import math

try:
    import bpy
except ImportError:
    print("This script must be executed via Blender headless: blender -b -P scripts/render_blender_3d_surfaces.py")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'branding', 'scientific-differential-geometry-10', 'mesh-data', 'surfaces.json')
OUT_DIR = os.path.join(BASE_DIR, 'branding', 'scientific-differential-geometry-10', 'blender-renders')
os.makedirs(OUT_DIR, exist_ok=True)

with open(JSON_PATH, 'r') as f:
    surfaces = json.load(f)

for s in surfaces:
    sid = s['id']
    title = s['title']
    rows = s['rows']
    cols = s['cols']
    xs = s['x']
    ys = s['y']
    zs = s['z']

    # Reset scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True

    # Camera setup
    cam_data = bpy.data.cameras.new('Camera')
    cam = bpy.data.objects.new('Camera', cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    # Compute bounding box and center
    all_x = [val for row in xs for val in row if math.isfinite(val)]
    all_y = [val for row in ys for val in row if math.isfinite(val)]
    all_z = [val for row in zs for val in row if math.isfinite(val)]
    
    cx = (max(all_x) + min(all_x)) / 2.0
    cy = (max(all_y) + min(all_y)) / 2.0
    cz = (max(all_z) + min(all_z)) / 2.0
    span = max(max(all_x) - min(all_x), max(all_y) - min(all_y), max(all_z) - min(all_z), 0.1)

    # Position camera
    dist = span * 2.2
    elev_rad = math.radians(s.get('elev', 28))
    azim_rad = math.radians(s.get('azim', 60))
    cam.location = (
        cx + dist * math.cos(elev_rad) * math.sin(azim_rad),
        cy - dist * math.cos(elev_rad) * math.cos(azim_rad),
        cz + dist * math.sin(elev_rad)
    )
    # Track towards center
    track = cam.constraints.new(type='TRACK_TO')
    
    # Target empty
    target_data = bpy.data.objects.new('Target', None)
    target_data.location = (cx, cy, cz)
    scene.collection.objects.link(target_data)
    track.target = target_data
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Lighting: 3-point studio lighting
    # Key light
    key_light = bpy.data.lights.new('KeyLight', type='SUN')
    key_light.energy = 3.5
    key_light.color = (0.9, 0.98, 1.0)
    key_obj = bpy.data.objects.new('KeyLight', key_light)
    key_obj.location = (cx + dist, cy - dist, cz + dist * 1.5)
    scene.collection.objects.link(key_obj)

    # Fill light (Hyperliquid Mint tint)
    fill_light = bpy.data.lights.new('FillLight', type='SUN')
    fill_light.energy = 1.8
    fill_light.color = (0.2, 0.95, 0.8) # #00f5d4
    fill_obj = bpy.data.objects.new('FillLight', fill_light)
    fill_obj.location = (cx - dist, cy - dist * 0.5, cz - dist * 0.5)
    scene.collection.objects.link(fill_obj)

    # Rim light
    rim_light = bpy.data.lights.new('RimLight', type='SUN')
    rim_light.energy = 2.0
    rim_light.color = (1.0, 0.85, 0.3)
    rim_obj = bpy.data.objects.new('RimLight', rim_light)
    rim_obj.location = (cx, cy + dist, cz + dist)
    scene.collection.objects.link(rim_obj)

    # Create 3D Mesh
    vertices = []
    faces = []
    vert_map = {}
    idx = 0
    for r in range(rows):
        for c in range(cols):
            x, y, z = xs[r][c], ys[r][c], zs[r][c]
            if math.isfinite(x) and math.isfinite(y) and math.isfinite(z):
                vertices.append((x, y, z))
                vert_map[(r, c)] = idx
                idx += 1
            else:
                vert_map[(r, c)] = None

    for r in range(rows - 1):
        for c in range(cols - 1):
            i0 = vert_map.get((r, c))
            i1 = vert_map.get((r + 1, c))
            i2 = vert_map.get((r + 1, c + 1))
            i3 = vert_map.get((r, c + 1))
            if i0 is not None and i1 is not None and i2 is not None and i3 is not None:
                faces.append((i0, i1, i2, i3))

    mesh_data = bpy.data.meshes.new(f'Mesh_{sid}')
    mesh_data.from_pydata(vertices, [], faces)
    mesh_data.update()

    mesh_obj = bpy.data.objects.new(f'Obj_{sid}', mesh_data)
    scene.collection.objects.link(mesh_obj)

    # Add Wireframe Modifier
    wire_mod = mesh_obj.modifiers.new('Wireframe', 'WIREFRAME')
    wire_mod.thickness = span * 0.008
    wire_mod.use_replace = True

    # Shader material: Iridescent metallic dark navy with mint Fresnel
    mat = bpy.data.materials.new(name=f"Mat_{sid}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.1, 0.18, 1.0) # Deep Navy
        bsdf.inputs['Metallic'].default_value = 0.85
        bsdf.inputs['Roughness'].default_value = 0.15
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = (0.0, 0.8, 0.7, 1.0)
            bsdf.inputs['Emission Strength'].default_value = 0.15
    mesh_obj.data.materials.append(mat)

    # Render filepath
    out_file = os.path.join(OUT_DIR, f"{sid}_blender_render.png")
    scene.render.filepath = out_file
    
    print(f"Rendering Blender 3D: {sid}...")
    bpy.ops.render.render(write_still=True)
    print(f"  ✓ Saved Blender render: {out_file}")

print("\nAll 10 Blender 3D surfaces rendered successfully!")

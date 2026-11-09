#!/usr/bin/env python3
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

# Parse JS functions from 3d_parametric_studio.html
with open('/Users/ianmora/Desktop/Projects/HyperSettle/branding/3d_parametric_studio.html') as f:
    html = f.read()

# Let's extract each surface definition
surface_matches = re.findall(r'id:\s*\"(\d+)\",\s*name:\s*\"([^\"]+)\".*?func:\s*\((.*?)\)\s*=>\s*\{(.*?)\n\s*\}', html, re.DOTALL)
print(f"Extracted {len(surface_matches)} surface definitions.")

user_im = Image.open('/Users/ianmora/.gemini/antigravity/brain/f190b5d1-3ec9-4e13-996d-a81cf918bec3/.user_uploaded/media_1794222516795_24ae3984.jpg').convert('L').resize((100, 100))
user_arr = 255.0 - np.array(user_im)
user_mask = user_arr > 15

best_shapes = []

for sid, name, args, code in surface_matches:
    # Convert JS code to python code
    py_code = code.replace('Math.', 'np.').replace('target.set', 'return_vec')
    # Let's evaluate u, v
    u_vals = np.linspace(0, 1, 24)
    v_vals = np.linspace(0, 1, 24)
    U, V = np.meshgrid(u_vals, v_vals)
    
    # We will test manually for known iconic shapes
    # Let's print out what shapes exist around 01-10, 19, 38, 43, 47
    pass

print("Inspection script ready.")

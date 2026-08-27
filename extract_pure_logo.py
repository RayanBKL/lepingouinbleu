import numpy as np
from PIL import Image

# Load original
img_rgb = Image.open('305307073_531871505411363_5769649798829963485_n.jpg').convert('RGBA')
img_gray = img_rgb.convert('L')
arr_gray = np.array(img_gray)
h, w = arr_gray.shape

# Threshold for pure dark silhouette
low = 60.0
high = 95.0
alpha = np.clip((high - arr_gray) / (high - low), 0.0, 1.0)

# Limit to logo area
y_indices, x_indices = np.indices((h, w))
mask_box = (y_indices >= 280) & (y_indices <= 1750) & (x_indices >= 300) & (x_indices <= 1750)
alpha[~mask_box] = 0.0

# Notice the penguin's belly is at X <= 1040.
# The coordinates text starts at X >= 1100 to 1750, Y: 980 to 1250.
# Let's inspect:
coords_box = (y_indices >= 980) & (y_indices <= 1260) & (x_indices >= 1100) & (x_indices <= 1750)
alpha[coords_box] = 0.0

# Clean up noise specks outside penguin & sextant
import collections
binary = (alpha > 0.35).astype(np.uint8)
visited = np.zeros((h, w), dtype=bool)

for y in range(h):
    for x in range(w):
        if binary[y, x] and not visited[y, x]:
            q = collections.deque([(y, x)])
            visited[y, x] = True
            count = 0
            pixels = []
            while q:
                cy, cx = q.popleft()
                pixels.append((cy, cx))
                count += 1
                for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        if binary[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            q.append((ny, nx))
            
            # Remove any stray speckle < 80 pixels
            if count < 80:
                for py, px in pixels:
                    alpha[py, px] = 0.0

# Crop to tight bounding box of penguin + sextant
active = (alpha > 0.05)
rows = np.any(active, axis=1)
cols = np.any(active, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

pad = 15
rmin = max(0, rmin - pad)
rmax = min(h, rmax + pad)
cmin = max(0, cmin - pad)
cmax = min(w, cmax + pad)

cropped_alpha = alpha[rmin:rmax, cmin:cmax]
ch, cw = cropped_alpha.shape

# 1. Solid Brand Blue (#18385C)
blue_r, blue_g, blue_b = 24, 56, 92
out_arr_blue = np.zeros((ch, cw, 4), dtype=np.uint8)
out_arr_blue[:, :, 0] = blue_r
out_arr_blue[:, :, 1] = blue_g
out_arr_blue[:, :, 2] = blue_b
out_arr_blue[:, :, 3] = (cropped_alpha * 255).astype(np.uint8)

img_blue = Image.fromarray(out_arr_blue, mode='RGBA')
img_blue.save('assets/images/logo_pingouin_clean.png')
print(f"Saved assets/images/logo_pingouin_clean.png ({cw}x{ch})")

# 2. Solid White (#FFFFFF)
out_arr_white = np.zeros((ch, cw, 4), dtype=np.uint8)
out_arr_white[:, :, 0] = 255
out_arr_white[:, :, 1] = 255
out_arr_white[:, :, 2] = 255
out_arr_white[:, :, 3] = (cropped_alpha * 255).astype(np.uint8)

img_white = Image.fromarray(out_arr_white, mode='RGBA')
img_white.save('assets/images/logo_pingouin_clean_white.png')
print(f"Saved assets/images/logo_pingouin_clean_white.png ({cw}x{ch})")

# 3. Create SVG wrappers
import base64
with open('assets/images/logo_pingouin_clean.png', 'rb') as f:
    b64_blue = base64.b64encode(f.read()).decode('utf-8')

svg_blue = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_blue}" width="{cw}" height="{ch}" />
</svg>
'''
with open('assets/images/logo_pingouin.svg', 'w', encoding='utf-8') as f:
    f.write(svg_blue)

with open('assets/images/logo_pingouin_clean_white.png', 'rb') as f:
    b64_white = base64.b64encode(f.read()).decode('utf-8')

svg_white = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_white}" width="{cw}" height="{ch}" />
</svg>
'''
with open('assets/images/logo_pingouin_white.svg', 'w', encoding='utf-8') as f:
    f.write(svg_white)

print("Generated refined logo_pingouin.svg with untouched penguin belly & sextant!")

import numpy as np
from PIL import Image
import collections
import base64

# Load the generated image
img = Image.open('assets/images/logo_pingouin_clean.png')
arr = np.array(img)
alpha = arr[:, :, 3]

# Binarize
binary = (alpha > 50).astype(np.uint8)
h, w = binary.shape
visited = np.zeros((h, w), dtype=bool)

components = []

for y in range(h):
    for x in range(w):
        if binary[y, x] and not visited[y, x]:
            q = collections.deque([(y, x)])
            visited[y, x] = True
            pixels = []
            while q:
                cy, cx = q.popleft()
                pixels.append((cy, cx))
                for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        if binary[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            q.append((ny, nx))
            components.append(pixels)

components.sort(key=lambda p: len(p), reverse=True)

# Keep ONLY the 2 major elements: Component 0 (Penguin + Tray) and Component 1 (Sextant)
clean_alpha = np.zeros((h, w), dtype=np.uint8)
for comp in components[:2]:
    for py, px in comp:
        clean_alpha[py, px] = alpha[py, px]

# Crop to exact bounding box
active = (clean_alpha > 0)
rows = np.any(active, axis=1)
cols = np.any(active, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

pad = 10
rmin = max(0, rmin - pad)
rmax = min(h, rmax + pad)
cmin = max(0, cmin - pad)
cmax = min(w, cmax + pad)

cropped_clean = clean_alpha[rmin:rmax, cmin:cmax]
ch, cw = cropped_clean.shape

# 1. Blue Logo
blue_arr = np.zeros((ch, cw, 4), dtype=np.uint8)
blue_arr[:, :, 0] = 24
blue_arr[:, :, 1] = 56
blue_arr[:, :, 2] = 92
blue_arr[:, :, 3] = cropped_clean

blue_img = Image.fromarray(blue_arr, mode='RGBA')
blue_img.save('assets/images/logo_pingouin_clean.png')

# 2. White Logo
white_arr = np.zeros((ch, cw, 4), dtype=np.uint8)
white_arr[:, :, 0] = 255
white_arr[:, :, 1] = 255
white_arr[:, :, 2] = 255
white_arr[:, :, 3] = cropped_clean

white_img = Image.fromarray(white_arr, mode='RGBA')
white_img.save('assets/images/logo_pingouin_clean_white.png')

# 3. SVG Embeds
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

print(f"Pristine logo (ONLY Penguin + Sextant) generated successfully ({cw}x{ch})!")

import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

# Load grayscale
img = Image.open('305307073_531871505411363_5769649798829963485_n.jpg').convert('L')
arr = np.array(img)

# Slight blur to reduce wood grain noise inside silhouette
blurred = img.filter(ImageFilter.GaussianBlur(radius=2.0))
barr = np.array(blurred)

# Binary threshold
thresh = 76
mask = (barr < thresh)

# Crop to tight bounding box of mask (filter out border noise)
rows = np.any(mask, axis=1)
cols = np.any(mask, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

margin = 30
rmin = max(0, rmin - margin)
rmax = min(arr.shape[0], rmax + margin)
cmin = max(0, cmin - margin)
cmax = min(arr.shape[1], cmax + margin)

cropped_barr = barr[rmin:rmax, cmin:cmax]
h, w = cropped_barr.shape

# Use matplotlib to extract contour paths at threshold
fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
contours = ax.contour(cropped_barr, levels=[thresh], colors='black')
plt.close(fig)

svg_paths = []
# In modern matplotlib, paths can be obtained from allsegs
for level_segs in contours.allsegs:
    for seg in level_segs:
        if len(seg) < 15:  # Skip tiny noise specks
            continue
        x_span = seg[:, 0].max() - seg[:, 0].min()
        y_span = seg[:, 1].max() - seg[:, 1].min()
        if x_span < 5 and y_span < 5:
            continue
        d_str = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in seg) + " Z"
        svg_paths.append(d_str)

print(f"Extracted {len(svg_paths)} vector paths. ViewBox: 0 0 {w} {h}")

# Generate clean SVG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="currentColor" fill-rule="evenodd">
  <g class="pingouin-official-silhouette">
'''

for p in svg_paths:
    svg_content += f'    <path d="{p}" />\n'

svg_content += '''  </g>
</svg>
'''

with open('assets/images/logo_pingouin.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Saved assets/images/logo_pingouin.svg successfully!")

import numpy as np
from PIL import Image, ImageFilter, ImageOps

# 1. Create a transparent PNG cutout of the exact logo
img_rgb = Image.open('305307073_531871505411363_5769649798829963485_n.jpg').convert('RGBA')
img_gray = img_rgb.convert('L')
arr_gray = np.array(img_gray)

# The wood background is light (around 120-160), the logo is dark (around 30-70)
# Let's create an alpha mask where dark pixels are solid #18385C (brand blue)
# and light wood background is 100% transparent.

# Threshold with smooth anti-aliased transition
# dark threshold = 65 (fully opaque), light threshold = 95 (fully transparent)
low = 65.0
high = 98.0

# Calculate alpha: 1.0 at <= low, 0.0 at >= high
alpha = np.clip((high - arr_gray) / (high - low), 0.0, 1.0)

# Remove stray noise specks outside the logo area:
# Bounding box of logo:
# y from ~300 to ~1700, x from ~300 to ~1750
h, w = arr_gray.shape
y_indices, x_indices = np.indices((h, w))

# Clean up outer borders
mask_box = (y_indices >= 280) & (y_indices <= 1750) & (x_indices >= 300) & (x_indices <= 1750)
alpha[~mask_box] = 0.0

# Crop to tight bounding box
active_pixels = (alpha > 0.05)
rows = np.any(active_pixels, axis=1)
cols = np.any(active_pixels, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

pad = 20
rmin = max(0, rmin - pad)
rmax = min(h, rmax + pad)
cmin = max(0, cmin - pad)
cmax = min(w, cmax + pad)

cropped_alpha = alpha[rmin:rmax, cmin:cmax]
ch, cw = cropped_alpha.shape

# Create solid Brand Blue image (#18385C)
blue_r, blue_g, blue_b = 24, 56, 92  # #18385C
out_arr = np.zeros((ch, cw, 4), dtype=np.uint8)
out_arr[:, :, 0] = blue_r
out_arr[:, :, 1] = blue_g
out_arr[:, :, 2] = blue_b
out_arr[:, :, 3] = (cropped_alpha * 255).astype(np.uint8)

out_img = Image.fromarray(out_arr, mode='RGBA')
out_img.save('assets/images/logo_pingouin_transparent.png')
print(f"Saved assets/images/logo_pingouin_transparent.png (Size: {cw}x{ch})")

# Also create White version for dark backgrounds / footer
white_arr = np.zeros((ch, cw, 4), dtype=np.uint8)
white_arr[:, :, 0] = 255
white_arr[:, :, 1] = 255
white_arr[:, :, 2] = 255
white_arr[:, :, 3] = (cropped_alpha * 255).astype(np.uint8)

white_img = Image.fromarray(white_arr, mode='RGBA')
white_img.save('assets/images/logo_pingouin_white.png')
print("Saved assets/images/logo_pingouin_white.png")

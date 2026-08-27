import numpy as np
from PIL import Image
import collections

# Load the generated alpha
img = Image.open('assets/images/logo_pingouin_transparent.png')
arr = np.array(img)
alpha = arr[:, :, 3]

# BFS to find connected components on alpha > 40
binary = (alpha > 40).astype(np.uint8)
h, w = binary.shape
visited = np.zeros((h, w), dtype=bool)

# Using 4-connectivity
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
            
            # Keep if size > 60 pixels (letters, numbers, penguin, sextant are > 60 pixels)
            if count < 55:
                for py, px in pixels:
                    alpha[py, px] = 0

arr[:, :, 3] = alpha

# Save clean blue logo
clean_blue = Image.fromarray(arr, mode='RGBA')
clean_blue.save('assets/images/logo_pingouin_clean.png')
print("Saved assets/images/logo_pingouin_clean.png")

# Save clean white logo
white_arr = arr.copy()
white_arr[:, :, 0] = 255
white_arr[:, :, 1] = 255
white_arr[:, :, 2] = 255
clean_white = Image.fromarray(white_arr, mode='RGBA')
clean_white.save('assets/images/logo_pingouin_clean_white.png')
print("Saved assets/images/logo_pingouin_clean_white.png")

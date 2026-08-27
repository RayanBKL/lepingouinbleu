import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

# Load image
img = Image.open('305307073_531871505411363_5769649798829963485_n.jpg').convert('L')
arr = np.array(img)

# The penguin silhouette is clearly dark (values < 80)
# Background wood has grain, so let's apply smooth thresholding
# Let's inspect where the logo elements are:
# Bounding box of dark region:
mask = (arr < 75)

# Save mask as test image
mask_img = Image.fromarray((mask * 255).astype(np.uint8))
mask_img.save('test_mask.png')
print("Saved test_mask.png")

import base64
from PIL import Image

# Read the clean transparent PNG and embed in SVG for crisp scaling, or output base64 data-uri SVG
with open('assets/images/logo_pingouin_clean.png', 'rb') as f:
    png_data = f.read()

b64_str = base64.b64encode(png_data).decode('utf-8')

img = Image.open('assets/images/logo_pingouin_clean.png')
w, h = img.size

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_str}" width="{w}" height="{h}" />
</svg>
'''

with open('assets/images/logo_pingouin.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Generated assets/images/logo_pingouin.svg with exact 1:1 fidelity ({w}x{h})")

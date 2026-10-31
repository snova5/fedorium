#!/usr/bin/env python3
"""Generates the Fedorium boot splash image: logo + "fedorium" in Comfortaa.
Usage: make-splash.py output.png"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1] if len(sys.argv) > 1 else "fedorium-watermark.png"

def find_font():
    for pat in ("Comfortaa:bold", "Comfortaa"):
        try:
            p = subprocess.run(["fc-match", "-f", "%{file}", pat], capture_output=True, text=True).stdout
            if "omfortaa" in p:
                return p
        except FileNotFoundError:
            pass
    print("WARNING: Comfortaa font not found (sudo dnf install aajohan-comfortaa-fonts); using a fallback font.")
    for p in ("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            ImageFont.truetype(p, 10); return p
        except OSError:
            pass
    return None

SS = 3                       # supersampling for smooth edges
W, H = 560, 440
LOGO = 270                   # logo height (px)
img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# --- logo (same coordinates as fedorium-logo.svg, viewBox 20 20 360 360) ---
s = LOGO * SS / 360
ox = (W * SS - 360 * s) / 2 - 20 * s
oy = 0 - 20 * s
def P(x, y, dy=0): return (ox + x * s, oy + (y + dy) * s)
def quad(a, c, b, n=24):
    return [((1-t)**2*a[0] + 2*(1-t)*t*c[0] + t*t*b[0], (1-t)**2*a[1] + 2*(1-t)*t*c[1] + t*t*b[1])
            for t in (i / n for i in range(n + 1))]

hexp = [P(*p) for p in [(200,34),(344,117),(344,283),(200,366),(56,283),(56,117)]]
d.line(hexp + [hexp[0], hexp[1]], fill="#8EC9F0", width=int(16 * s), joint="curve")
crown = [(140,226),(152,142)] + quad((152,142),(155,128),(169,131)) + [(190,139),(200,151),(210,139),(231,131)] \
        + quad((231,131),(245,128),(248,142)) + [(260,226)]
d.polygon([P(x, y, 10) for x, y in crown], fill="#3C6EB4")
d.polygon([P(x, y, 10) for x, y in [(144.5,192),(255.5,192),(259.3,220),(140.7,220)]], fill="#8EC9F0")
for br in ([(184,197),(170,206),(184,215)], [(216,197),(230,206),(216,215)]):
    d.line([P(x, y, 10) for x, y in br], fill="#294172", width=int(6 * s), joint="curve")
x0, y0 = P(88, 234, 10); x1, y1 = P(312, 258, 10)
d.rounded_rectangle([x0, y0, x1, y1], radius=12 * s, fill="#3C6EB4")

# --- the word "fedorium" ---
fp = find_font()
font = ImageFont.truetype(fp, 84 * SS) if fp else ImageFont.load_default()
text = "fedorium"
bb = d.textbbox((0, 0), text, font=font)
tx = (W * SS - (bb[2] - bb[0])) / 2 - bb[0]
ty = (LOGO + 40) * SS - bb[1]
d.text((tx, ty), text, font=font, fill="#FFFFFF")

img.resize((W, H), Image.LANCZOS).save(out)
print(f"Boot splash generated: {out} (font: {fp})")

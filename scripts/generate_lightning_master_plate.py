"""Generate a 4K technical architectural master plate for Lightning Conductor."""

from __future__ import annotations
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W = 3840
H = 2160

img = Image.new("RGBA", (W, H), (14, 20, 30, 255))
draw = ImageDraw.Draw(img)

# 1. Subtle Engineering Grid
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=(24, 34, 50, 140), width=1)
for y in range(0, H, 80):
    draw.line([(0, y), (W, y)], fill=(24, 34, 50, 140), width=1)

# 2. Soil Ground Cross-section
ground_y = 1580
# Subterranean strata
draw.rectangle([0, ground_y, W, H], fill=(42, 30, 24, 255))
# Soil gradient & layers
for gy, col in [(1700, (36, 24, 18, 255)), (1840, (28, 18, 14, 255)), (1980, (22, 14, 10, 255))]:
    draw.line([(0, gy), (W, gy)], fill=col, width=4)
# Surface grass/ground line
draw.line([(0, ground_y), (W, ground_y)], fill=(75, 58, 42, 255), width=8)

# 3. Building Structure (Architectural cutaway)
bx1, bx2 = 1000, 2800
by_roof = 760
peak_x = 1800
peak_y = 480

# Main wall
draw.rectangle([bx1, by_roof, bx2, ground_y], fill=(32, 46, 64, 255), outline=(55, 80, 110, 255), width=6)
# Interior structural rooms & concrete
for wy in range(by_roof + 100, ground_y - 120, 180):
    for wx in range(bx1 + 120, bx2 - 120, 260):
        draw.rectangle([wx, wy, wx + 180, wy + 120], fill=(22, 32, 46, 255), outline=(42, 60, 84, 255), width=3)
        # Window mullions
        draw.line([(wx + 90, wy), (wx + 90, wy + 120)], fill=(30, 44, 62, 255), width=2)
        draw.line([(wx, wy + 60), (wx + 180, wy + 60)], fill=(30, 44, 62, 255), width=2)

# Pitched Slate Roof
roof_pts = [(bx1 - 50, by_roof), (peak_x, peak_y), (bx2 + 50, by_roof)]
draw.polygon(roof_pts, fill=(45, 62, 85, 255), outline=(75, 105, 140, 255))
# Slate tile lines
for t_y in range(peak_y + 40, by_roof, 50):
    prog = (t_y - peak_y) / float(by_roof - peak_y)
    lx = int((1 - prog) * peak_x + prog * (bx1 - 50))
    rx = int((1 - prog) * peak_x + prog * (bx2 + 50))
    draw.line([(lx, t_y), (rx, t_y)], fill=(38, 52, 72, 200), width=2)

# 4. Air Terminal (Pointed Copper Franklin Rod)
rod_tip = (peak_x, peak_y - 220)
rod_base = (peak_x, peak_y)
# Mounting bracket
draw.rectangle([peak_x - 22, peak_y - 15, peak_x + 22, peak_y + 15], fill=(90, 105, 120, 255), outline=(130, 150, 170, 255), width=3)
# Heavy Copper Rod
draw.line([rod_tip, rod_base], fill=(230, 126, 34, 255), width=18)
draw.line([(rod_tip[0] - 3, rod_tip[1]), (rod_base[0] - 3, rod_base[1])], fill=(255, 185, 100, 255), width=5)
# Sharp tip
draw.polygon([(rod_tip[0], rod_tip[1] - 30), (rod_tip[0] - 14, rod_tip[1]), (rod_tip[0] + 14, rod_tip[1])], fill=(255, 190, 110, 255))

# 5. Heavy Braided Copper Down-Conductor Path
corner_x, corner_y = bx1 - 40, by_roof + 20
ground_entry_x, ground_entry_y = bx1 - 40, ground_y
pit_bottom_x, pit_bottom_y = bx1 - 40, 1940

# Roof run
draw.line([rod_base, (corner_x, corner_y)], fill=(230, 126, 34, 255), width=14)
draw.line([(rod_base[0], rod_base[1] - 2), (corner_x, corner_y - 2)], fill=(255, 185, 100, 255), width=4)
# Down exterior wall
draw.line([(corner_x, corner_y), (ground_entry_x, ground_entry_y)], fill=(230, 126, 34, 255), width=14)
draw.line([(corner_x - 2, corner_y), (ground_entry_x - 2, ground_entry_y)], fill=(255, 185, 100, 255), width=4)

# Wall standoff clips
for cy in range(corner_y + 120, ground_entry_y, 160):
    draw.rectangle([corner_x - 22, cy - 8, corner_x + 22, cy + 8], fill=(160, 175, 190, 255))

# 6. Underground Earth Pit & Electrode
# Bentonite backfill pit (conductive earth bed)
draw.rectangle([ground_entry_x - 90, ground_entry_y + 60, ground_entry_x + 90, pit_bottom_y + 60], fill=(58, 42, 32, 255), outline=(95, 70, 52, 255), width=4)
# Copper Earthing Electrode Rod
draw.line([(ground_entry_x, ground_entry_y), (pit_bottom_x, pit_bottom_y)], fill=(230, 126, 34, 255), width=18)
draw.line([(ground_entry_x - 3, ground_entry_y), (pit_bottom_x - 3, pit_bottom_y)], fill=(255, 185, 100, 255), width=5)
# Ground plate & radial dissipation spikes
draw.rectangle([pit_bottom_x - 60, pit_bottom_y - 12, pit_bottom_x + 60, pit_bottom_y + 12], fill=(230, 126, 34, 255))
for spike_dx, spike_dy in [(-100, 40), (-50, 70), (50, 70), (100, 40)]:
    draw.line([(pit_bottom_x, pit_bottom_y), (pit_bottom_x + spike_dx, pit_bottom_y + spike_dy)], fill=(230, 126, 34, 255), width=8)

# 7. Callout Labels (Audited Plate Typography)
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 44)
font_sm = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 32)

# Air Terminal label
draw.text((peak_x + 60, peak_y - 180), "COPPER AIR TERMINAL (FRANKLIN ROD)", font=font, fill=(255, 200, 120, 255))
draw.text((peak_x + 60, peak_y - 130), "Preferential strike attachment point", font=font_sm, fill=(160, 180, 205, 255))

# Down-Conductor label
draw.text((corner_x - 680, (corner_y + ground_entry_y) // 2 - 40), "BARE COPPER DOWN-CONDUCTOR", font=font, fill=(255, 200, 120, 255))
draw.text((corner_x - 680, (corner_y + ground_entry_y) // 2 + 10), "Low-impedance exterior path", font=font_sm, fill=(160, 180, 205, 255))

# Earth Pit label
draw.text((pit_bottom_x + 120, pit_bottom_y - 40), "EARTHING ELECTRODE & BENTONITE BED", font=font, fill=(100, 230, 150, 255))
draw.text((pit_bottom_x + 120, pit_bottom_y + 10), "Safe surge dissipation into 0V ground grid", font=font_sm, fill=(160, 180, 205, 255))

out_path = Path("projects/lightning-conductor-remotion/public/assets/lightning-master-plate.png")
img.save(str(out_path), "PNG")
print("Saved 4K Master Plate:", out_path, "Size:", out_path.stat().st_size)

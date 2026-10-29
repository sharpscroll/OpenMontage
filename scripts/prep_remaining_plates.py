from PIL import Image, ImageDraw, ImageFilter
import os
import numpy as np

masters_dir = r"E:\Data\YT\Video Data\Shorts Bank Videos\Shorts Working Temp\Q18_Safety_Switch_No_Overload\G2_Artwork\Masters"
user_dir = r"C:\Users\Hp\.gemini\antigravity\brain\3b239e0d-cf08-4230-b1b3-e372d8f5148c\.user_uploaded"

TARGET_W, TARGET_H = 1080, 1920

# 1. Build Plate 4: Clean Smudge-Free Comparison Plate
# Base canvas: Warm cream paper (#FAF9F4) with soft watercolor blue wash vignette
canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (250, 249, 244, 255))

# Soft blue watercolor wash in the background
wash = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(wash)
# Draw soft blue elliptical washes behind objects
draw.ellipse([80, 80, 480, 520], fill=(225, 238, 246, 160))
draw.ellipse([550, 1200, 1020, 1780], fill=(225, 238, 246, 160))
draw.ellipse([150, 700, 930, 1250], fill=(245, 248, 252, 100))
wash = wash.filter(ImageFilter.GaussianBlur(radius=65))
canvas.alpha_composite(wash)

# Load RCD (Top Left) from user's RCD plate
rcd_source = Image.open(os.path.join(user_dir, "media_1793101906011_25a096fd.jpg")).convert("RGBA")
# Crop RCD object
rcd_w, rcd_h = rcd_source.size
rcd_crop = rcd_source.crop((int(rcd_w * 0.15), int(rcd_h * 0.18), int(rcd_w * 0.85), int(rcd_h * 0.82)))
# Resize RCD for upper-left placement
rcd_scale = 0.55
rcd_resized = rcd_crop.resize((int(rcd_crop.width * rcd_scale), int(rcd_crop.height * rcd_scale)), Image.Resampling.LANCZOS)

# Create soft drop shadow and mask for RCD
rcd_mask = Image.new("L", rcd_resized.size, 255)
# Feather edges softly so it blends seamlessly into cream canvas
feather_draw = ImageDraw.Draw(rcd_mask)
feather_w, feather_h = rcd_resized.size
for i in range(15):
    alpha = int(255 * (i / 15.0))
    feather_draw.rectangle([i, i, feather_w - i, feather_h - i], outline=alpha)

# Paste RCD at top-left: x=100, y=140
canvas.paste(rcd_resized, (100, 140))

# Load Toaster (Bottom Right) from user's toaster plate
toaster_source = Image.open(os.path.join(user_dir, "media_1793101906011_ad01ca35.jpg")).convert("RGBA")
t_w, t_h = toaster_source.size
# Crop toaster and counter surface
toaster_crop = toaster_source.crop((int(t_w * 0.10), int(t_h * 0.30), int(t_w * 0.95), int(t_h * 0.85)))
t_scale = 0.65
toaster_resized = toaster_crop.resize((int(toaster_crop.width * t_scale), int(toaster_crop.height * t_scale)), Image.Resampling.LANCZOS)

# Paste Toaster at bottom-right: x=460, y=1180
canvas.paste(toaster_resized, (480, 1180))

# Save pristine Plate 4
p4_out = os.path.join(masters_dir, "plate4_comparison_clean_1080x1920.png")
canvas.convert("RGB").save(p4_out, quality=95)
print("Saved clean comparison plate:", p4_out)

# 2. Build Plate 3: RCD Normal ON Position
# Load Plate 2 (RCD Tripped), and flip the blue lever toggle UP
rcd_plate2 = Image.open(os.path.join(masters_dir, "plate2_rcd_tripped_1080x1920.png")).convert("RGBA")
# The toggle handle on plate2 is around center.
# Let's inspect toggle coordinates on 1080x1920
print("Plate 2 size:", rcd_plate2.size)

# Let's save a clean Plate 3
# In DIN-rail RCCB, normal monitoring is with the lever flipped UP.
# We create plate 3:
p3_out = os.path.join(masters_dir, "plate3_rcd_on_1080x1920.png")
# We copy plate 2 and adjust the lever area to show the UP position
p3_img = rcd_plate2.copy()
# Draw the blue lever in the UP position (raised 70px)
# Let's measure where the toggle is located
arr = np.array(p3_img)
# Blue lever has distinctive high blue and low red
blue_mask = (arr[:, :, 2] > 110) & (arr[:, :, 0] < 70) & (arr[:, :, 1] < 100)
y_indices, x_indices = np.where(blue_mask)
if len(y_indices) > 0:
    min_y, max_y = y_indices.min(), y_indices.max()
    min_x, max_x = x_indices.min(), x_indices.max()
    print(f"Blue toggle detected at X: {min_x}..{max_x}, Y: {min_y}..{max_y}")
    
    # Crop the blue toggle
    toggle_crop = p3_img.crop((min_x - 10, min_y - 10, max_x + 10, max_y + 10))
    # Fill the old tripped slot with the grey recess color
    recess_fill = Image.new("RGBA", toggle_crop.size, (215, 218, 220, 255))
    p3_img.paste(recess_fill, (min_x - 10, min_y - 10))
    
    # Paste toggle shifted UP by ~95 pixels
    shift_up = 95
    p3_img.paste(toggle_crop, (min_x - 10, min_y - 10 - shift_up))

p3_img.convert("RGB").save(p3_out, quality=95)
print("Saved RCD ON plate:", p3_out)

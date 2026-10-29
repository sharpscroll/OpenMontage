from PIL import Image, ImageFilter, ImageOps
import os

user_dir = r"C:\Users\Hp\.gemini\antigravity\brain\3b239e0d-cf08-4230-b1b3-e372d8f5148c\.user_uploaded"
masters_dir = r"E:\Data\YT\Video Data\Shorts Bank Videos\Shorts Working Temp\Q18_Safety_Switch_No_Overload\G2_Artwork\Masters"
os.makedirs(masters_dir, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def fit_to_canvas(img_path, out_path, bg_color=(254, 253, 249)):
    im = Image.open(img_path).convert("RGBA")
    # Scale to 1080x1920 preserving aspect ratio or fill canvas
    w, h = im.size
    scale = max(TARGET_W / w, TARGET_H / h)
    new_w, new_h = int(w * scale), int(h * scale)
    im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Crop to exact center 1080x1920
    left = (new_w - TARGET_W) // 2
    top = (new_h - TARGET_H) // 2
    im_cropped = im_resized.crop((left, top, left + TARGET_W, top + TARGET_H))
    
    im_cropped.convert("RGB").save(out_path, quality=95)
    print(f"Saved: {out_path} ({TARGET_W}x{TARGET_H})")

# 1. Scene 1: Character Making Toast
p1_in = os.path.join(user_dir, "media_1793103929167_bdc372dc.jpg")
p1_out = os.path.join(masters_dir, "plate1_character_toast_1080x1920.png")
fit_to_canvas(p1_in, p1_out)

# 2. Scene 2: RCD Switch Tripped
p2_in = os.path.join(user_dir, "media_1793101906011_25a096fd.jpg")
p2_out = os.path.join(masters_dir, "plate2_rcd_tripped_1080x1920.png")
fit_to_canvas(p2_in, p2_out)

# 3. Scene 5: Fault Cutaway
p5_in = os.path.join(user_dir, "media_1793101906020_bd87f967.jpg")
p5_out = os.path.join(masters_dir, "plate5_fault_cutaway_1080x1920.png")
fit_to_canvas(p5_in, p5_out)

print("Done basic plates conversion.")

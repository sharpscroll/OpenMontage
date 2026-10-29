from PIL import Image
import glob
import os

dir_path = r"C:\Users\Hp\.gemini\antigravity\brain\3b239e0d-cf08-4230-b1b3-e372d8f5148c\.user_uploaded"
for f in glob.glob(os.path.join(dir_path, "*.jpg")) + glob.glob(os.path.join(dir_path, "*.png")):
    im = Image.open(f)
    print(os.path.basename(f), im.size, im.mode)

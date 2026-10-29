from PIL import Image
import glob
import os

dir_path = r"E:\Data\YT\Video Data\Shorts Bank Videos\Shorts Working Temp\Q18_Safety_Switch_No_Overload\G1_Illustrated_v02"
for f in glob.glob(os.path.join(dir_path, "*.png")):
    im = Image.open(f)
    print(os.path.basename(f), im.size, im.mode)

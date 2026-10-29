import glob
import os
import re

dir_path = r"E:\Data\YT\Video Data\Shorts Bank Videos\Shorts Working Temp\Q18_Safety_Switch_No_Overload\G1_Illustrated_v03\Compositions"
for f in sorted(glob.glob(os.path.join(dir_path, "*.svg"))):
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()
    texts = re.findall(r'<text[^>]*>(.*?)</text>', content)
    print(os.path.basename(f), "-->", texts)

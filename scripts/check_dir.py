import os

dir_path = "E:/Data/YT/Video Data"
entries = os.listdir(dir_path)
for e in entries:
    full = os.path.join(dir_path, e)
    print(repr(e), os.path.exists(full))

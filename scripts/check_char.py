from PIL import Image
import os

path = r"E:\Data\YT\Video Data\00_Channel_Assets\Character Masters\CM_Character_Seated_Desk_2K.png"
if os.path.exists(path):
    im = Image.open(path)
    print("Character Seated:", im.size, im.mode)

path2 = r"E:\Data\YT\Video Data\00_Channel_Assets\Character Masters\CM_Character_Master_2K.jpg"
if os.path.exists(path2):
    im2 = Image.open(path2)
    print("Character Master:", im2.size, im2.mode)

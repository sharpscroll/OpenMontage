from PIL import Image
import numpy as np

im = Image.open(r"E:\Data\YT\Video Data\00_Channel_Assets\Character Masters\CM_Character_Master_2K.jpg")
print("Size:", im.size)
# Sample colors or check if there is any text in the image
# Let's crop a thumbnail or check basic stats
arr = np.array(im)
print("Mean RGB:", arr.mean(axis=(0,1)))

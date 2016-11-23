import cv2
import numpy as np
import os

img_path = '/Users/gzhou/TL_documents/python/fisheye/fish-me.jpg'
#print(filedir+'fish-me.jpg')

print os.path.exists(img_path)

img = cv2.imread(filedir+'fish-me.jpg', CV_LOAD_IMAGE_COLOR)
print(img.shape)

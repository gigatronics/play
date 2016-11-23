
import cv2
import glob
import os
import numpy as np

cwd = os.getcwd()
img_path = cwd+'/video-conf/161024-stereo3/le-pano/'
print(os.path.exists(img_path))


img_list = []

for filename in glob.glob(img_path+'*.png'):
    img = cv2.imread(filename)
    img_list.append(img)

    #print(img.shape)
    height, width = img.shape[:-1]

    img2 = np.zeros((height, width, 3), np.uint8)
    #print(img2.shape)

    for i in range(height):          # height = 240
        for j in range(2, width):       # width = 960
            if j < width/2:         # y = 0 .. 479 < 480
                img2[i, j+width/2] = img[i, j]
            else:                   # y = 480
                img2[i, j-width/2+2] = img[i, j]

    filename_new = os.path.basename(filename)[:-4]+'-shft.png'
    cv2.imwrite(img_path+filename_new, img2)

fish2pano2eye-batch.py
import glob
import os
import cv2
from fish2pano_cv2_rgb import fish2pano_lut

img_path = '/Users/gzhou/TL_documents/python/video-conf/161025-stereo-align/test2/'

#os.path.exists(img_path)

img_list = []
for filename in glob.glob(img_path+'*.png'):
    img = cv2.imread(filename)
    img_list.append(img)

    #img =
    img_pano = fish2pano_lut(img)
    filename_new = os.path.basename(filename)[:-4]+'-pano.png'
    cv2.imwrite(img_path+filename_new, img_pano)

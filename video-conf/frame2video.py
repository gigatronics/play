

import cv2
import glob
import os


cwd = os.getcwd()
#img_path = cwd+'/video-conf/161025-stereo-align/le-pano/'
img_path = cwd +'/data/161031-wkend/pumpkin/c2-PHOTO-timelapse/'


print(os.path.exists(img_path))
img_list = []

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(img_path+'pumpkin-carving-fps12-hd.avi', fourcc, 12, (1280, 720))       #4608x2592

for filename in glob.glob(img_path+'*.JPG'):
    cv2.imread(filename)
    img = cv2.imread(filename)
    img_mid = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_CUBIC)
    img_list.append(img_mid)

    #rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    out.write(img_mid)

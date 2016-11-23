import cv2
import numpy as np
import math
from fish2pano_cv2_rgb import fish2pano
import time
import os


# # test run time
# frame = cv2.imread(os.getcwd()+'/fisheye/fish-me.jpg')
# start = time.time()
# pano = fish2pano(frame)# end = time.time()# print(end-start)    # 1.5s to unwarp 612x612 image

cap = cv2.VideoCapture(1)
#width = cap.get(CV_CAP_PROP_FRAME_WIDTH)
#height = cap.get(CV_CAP_PROP_FRAME_HEIGHT)
#fps = cap.get(CV_CAP_PROP_FPS)
#print(fps)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(os.getcwd()+'/fisheye/output.avi', fourcc, 30, (240, 960), isColor = 1)
#print(type(out), out.dtype)

count =0

while(cap.isOpened()):
    ret, frame = cap.read()    #print(type(frame), frame.dtype)

    start = time.time()

    pano = fish2pano(frame) #.astype('u8')
    #print(type(pano), pano.dtype)
#    out.write(pano)

    cv2.imwrite(os.getcwd()+'/fisheye/frame-%s.png' % count, pano)
    count +=1

    end = time.time()
    print(end-start)
    #cv2.waitKey(1000)

cap.release()
out.release()
cv2.destroyAllWindows

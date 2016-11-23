import cv2
import numpy as np
import math
from fish2pano_cv2_rgb import fish2pano
import time
import os
import subprocess as sp
import sys

cap = cv2.VideoCapture(0)

count =0

while(cap.isOpened()):
    ret, frame = cap.read()    #print(type(frame), frame.dtype)
    start = time.time()
    pano = fish2pano(frame) #.astype('u8')

    cv2.imwrite('frame.png', pano)# % count, pano)
    sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1/5 -i frame.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)

    end = time.time()
    print(end-start)
    #cv2.waitKey(1000)

#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

cap.release()
out.release()
cv2.destroyAllWindows

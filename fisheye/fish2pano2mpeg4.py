# which device to call: ffmpeg -f avfoundation -list_devices true -i "" (mac)
# set up server: ffserver -d -f /etc/ffserver-gina.conf

import cv2
import numpy as np
import math
from fish2pano_cv2_rgb import fish2pano
import time
import os
import subprocess as sp
import sys

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()    #print(type(frame), frame.dtype)
#    print(frame.shape[0], frame.shape[1])
    start = time.time()
    pano = fish2pano(frame) #.astype('u8')
    #pano= cv2.logPolar(frame, (frame.shape[0]/2, frame.shape[1]/2), 100, cv2.WARP_FILL_OUTLIERS)      # [0]: height; [1]: width
    cv2.write('frame.png', pano)# % count, pano)
    sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1/2 -i frame.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)
    #sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1/5 -i frame.png -f mpegts udp://localhost:1234', shell=True)

    # to simply display
    #cv2.imshow('preview', pano)

    end = time.time()
    print(end-start)
    #cv2.waitKey(1000)

#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

cap.release()
out.release()
cv2.destroyAllWindows

import cv2
import numpy as np
import math
from fish2pano_cv2_rgb import fish2pano
import time
import os
import subprocess as sp
import sys

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
directory = '/Users/gzhou/TL_documents/python/fisheye/'
out = cv2.VideoWriter(directory+'output.avi', fourcc, 1, (960, 480))
#out0 = cv2.VideoWriter(directory+'output0.avi', fourcc, 1, (960, 240))
#out1 = cv2.VideoWriter(directory+'output1.avi', fourcc, 1, (960, 240))

cap0 = cv2.VideoCapture(0)
cap0.set(3, 640)
cap0.set(4, 480)    # this give 160x120 images

cap1 = cv2.VideoCapture(1)
cap1.set(3, 640)
cap1.set(4, 480)    # this give 160x120 images

while(cap0.isOpened() & cap1.isOpened()):
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if (ret0==True & ret1==True):
        start = time.time()

        pano0 = fish2pano(frame0) #.astype('u8')
        pano1 = fish2pano(frame1) #.astype('u8')

        stack = np.vstack((pano0, pano1))
        out.write(stack)
        #out0.write(pano0)
        #out1.write(pano1)

        #cv2.imwrite('frame1.png', pano0)# % count, pano)
    #    cv2.imwrite()
        # sp.call('/usr/local')
    #    sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1/5 -i frame.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)
        #pipe.proc.stdout.write(frame.tostring() )

#        cv2.imshow('frame',frame)
        end = time.time()
        print(end-start)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
        #cv2.waitKey(1000)

#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)
cap0.release()
out0.release()

cap1.release()
out1.release()

out.release()
cv2.destroyAllWindows

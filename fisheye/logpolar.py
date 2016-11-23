# which device to call: ffmpeg -f avfoundation -list_devices true -i "" (mac)
# set up server: ffserver -d -f /etc/ffserver-gina.conf or ~/ffserver-rtp.conf

# todo: add options as args

import cv2
import numpy as np
import math
import time
import os
import subprocess as sp
import sys

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()    #print(type(frame), frame.dtype)
#    print(frame.shape[0], frame.shape[1])
    start = time.time()
    #pano = fish2pano(frame) #.astype('u8')q

    # resize 16:9 to 4:3 images... eg. 640x480 to 960x480
    h, w = (frame.shape[0], frame.shape[1]*3/2)
    frame_resize = cv2.resize(frame, (w, h))#, interpolation=cv2.CV_INTER_CUBIC)

    # pad image... e.g. 960x960
    if (w !=h):
        #img_sq = np.ndarray(shape = (width, width, 3))
        diff = int((w-h)/2)
        # pad
        frame_pad = cv2.copyMakeBorder(frame_resize, diff, diff, 0, 0, cv2.BORDER_CONSTANT)
        # crop
#        img_sq = img[0:h, diff:(diff+h)] # crop only the middle
        h, w = frame_pad.shape[: 2]
        #print ('image is now squared of size ', (w, h) )
    else:
        frame_pad = frame_resize
        h, w = frame_pad.shape[: 2]

    # fisheye to rectlinear
    #frame_polar= cv2.logPolar(frame, (frame_resize.shape[0]/2, frame_resize.shape[1]/2), 80, cv2.WARP_FILL_OUTLIERS)      # [0]: height; [1]: width
    frame_polar = cv2.linearPolar(frame_pad, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)
    h, w = frame_polar.shape[:2]
    #print(h, w)

    # rotate 90
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_polar, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

    # option 1: play back
    #cv2.imwrite('frame_pano.png', frame_pano)
    cv2.imshow('cam1', frame_pano)# % count, pano)

    # option 2: send as mjpeg
    #sp.call('/usr/local/bin/ffmpeg -f image2 -s 1820x480 -i frame_pano.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)


    # option 3: send down pipe (preferred)
    # convert bgr24 to yuv420p
    #print(frame_pano.dtype)
#    frame_yuv = cv2.cvtColor(frame_pano, cv2.COLOR_BGR2YUV_I420)
    #cv2.imshow('', frame_yuv)
#    sys.stdout.write( frame_pano.tostring() )

    # option 4: send as


    # option 5: send through sockCet

    #sp.call('/usr/local/bin/ffmpeg -f rawvideo -pix_fmt bgr24 -s 1820x480 -i sys.stdout.write(frame_pano.tostring)  -f mpegts udp://localhost:8090/cam2.ffm', shell=True)
    #frame_pano.format

    end = time.time()
    #print(end-start)   #cv2.waitKey(q1000)

#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

cap.release()
cv2.destroyAllWindows

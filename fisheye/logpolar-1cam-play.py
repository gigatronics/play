# which device to call: ffmpeg -f avfoundation -list_devices true -i "" (mac)
# set up server: ffserver -d -f /etc/ffserver-gina.conf or ~/ffserver-rtp.conf

# this function adds sliding bar features

import cv2
import numpy as np
import math
import time
import os
import subprocess as sp
import sys

#cap1 = cv2.VideoCapture(2)
#cap2 = cv2.VideoCapture(3)

def unwarp(frame, angle):
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

    # rotate 0 or 120 or 240
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)  # center,  angle, scale
    frame_align = cv2.warpAffine(frame_pad, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # fisheye to rectlinear
    #frame_polar= cv2.logPolar(frame, (frame_resize.shape[0]/2, frame_resize.shape[1]/2), 80, cv2.WARP_FILL_OUTLIERS)      # [0]: height; [1]: width
    frame_polar = cv2.linearPolar(frame_align, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)
    h, w = frame_polar.shape[:2]
    #print(h, w)

    # rotate 90
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_polar, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

    return frame_pano
    #cv2.imshow('preview', frame_pano)# % count, pano)
    #    cv2.imshow('cam1', frame_pnao1)


if __name__ == '__main__':

#    frame_out = np.
    cap0 = cv2.VideoCapture()

    while(cap0.isOpened()):
        ret, frame0 = cap0.read()    #print(type(frame), frame.dtype)
        print(frame0.shape[:2])

        frame_pano0 = unwarp(frame0, 0)       # centre, bandwidth in degrees
    #    frame_pano1 = unwarp(frame1, 120)
    #    frame_out = np.vstack((frame_pano0, frame_pano1))

        #cv2.imwrite('frame_pano.png', frame_pano)

        cv2.imshow('preview', frame_pano0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #frame_pano.format

        #print(end-start)   #cv2.waitKey(q1000)

    #sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

    cap.release()
    cv2.destroyAllWindows

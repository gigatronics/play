# which device to call: ffmpeg -f avfoundation -list_devices true -i "" (mac)
# set up server: ffserver -d -f /etc/ffserver-gina.conf

'''
todo:
- add options as args
- make a new one to work with two cameras...
- then dev into a manual calibration

'''

import cv2
import numpy as np
import math
import time
import os
import subprocess as sp
import sys


x = 320
y = 240        # h/2
r = 240
xmax = 640
ymax = 480
rmax = 480


def preproc(frame): # this function is only for action cam with 16:9 sensor captured as 4:3

    #resize 16:9 to 4:3 images... eg. 640x480 to 960x480
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
        print ('image is now squared of size ', (w, h) )
    else:
        frame_pad = frame_resize
        h, w = frame_pad.shape[: 2]
    return frame_pad


def postproc(frame):
    # rotate 90
    h, w = frame.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

    # option 1: play back
#    cv2.imwrite('frame_pano.png', frame_pano)
    cv2.imshow('cam1', cv2.pyrDown(frame_pano))# % count, pano)
    return frame_pano

def update(_):
    # fisheye to rectlinear
    polar = cv2.linearPolar(frame_pano, (x, y), r, cv2.WARP_FILL_OUTLIERS)
    frame_pano = postproc(polar)

    cv2.putText(frame_pano, ('params (x, y, r) = '+ str(x) + ', ' + str(y) + ', ' + str(r)), (10, 100), font, 1, (0, 255, 0), 2)
    cv2.imshow(win, frame_pano)
    cv2.waitKey()


if __name__ == '__name__':
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.imread('./fisheye/frame_00_test.png')

    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        ret, frame = cap.read()    #print(type(frame), frame.dtype)
        print(frame.shape[:2])
        # preprocess
        frame_pad = preproc(frame)

        #  create trackbar
        win = 'output'
        cv2.createTrackbar('x', win, int(opts.get('--x', x)), xmax, update)
        cv2.createTrackbar('y', win, int(opts.get('--y', y)), ymax, update)
        cv2.createTrackbar('r', win, int(opts.get('--r', r)), rmax, update)

        if cv2.waitKey() & 0xFF == ord('q'):
            break
#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

#cap.release()
cv2.destroyAllWindows

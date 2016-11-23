# which device to call: ffmpeg -f avfoundation -list_devices true -i "" (mac)
# set up server: ffserver -d -f /etc/ffserver-gina.conf

'''

This is adapted from fisheye/logpolar-slide-2cam.py

todo:
- then dev into a manual calibration

'''

import cv2
import numpy as np
import math
import time
import os
import subprocess as sp
import sys

x0, y0, r0 = (480, 480, 400)
x1, y1, r1 = (480, 480, 400)
a = 0             # angle between two cam, rotate color-wise

xmax = 640
ymax = 480
rmax = 480
amax = 120


def preproc(frame, a): # this function is only for action cam with 16:9 sensor captured as 4:3
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

    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), a, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_pad, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    return frame_rot


def postproc(frame, flip):
    # rotate 90
    h, w = frame.shape[:2]

    if flip == 1:
        rot_mat = cv2.getRotationMatrix2D((w/2, h/2), 90, 1.0)  # center,  angle, scale
    else:
        rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

#   cv2.imwrite('frame_pano.png', frame_pano)
    cv2.imshow('cam1', cv2.pyrDown(frame_pano)) # % count, pano)
    return frame_pano

def update(_):
    # fisheye to rectlinear
    polar0 = cv2.linearPolar(frame_pano0, (x0, y0), r0, cv2.WARP_FILL_OUTLIERS)
    frame_pano0 = postproc(polar0, 0)

    polar1 = cv2.linearPolar(frame_pano1, (x1, y1), r1, cv2.WARP_FILL_OUTLIERS)
    frame_pano1 = postproc(polar1, 0)           # flip == 1

    frame_vstack = np.concatenate((frame_pano0, frame_pano1), axis = 0)

    cv2.putText(frame_vstack, ('params (x, y, r) = '+ str(x) + ', ' + str(y) + ', ' + str(r)), (10, 100), font, 1, (0, 255, 0), 2)
    cv2.imshow(win, frame_vstack)
    #cv2.waitKey()

if __name__ == '__name__':
    font = cv2.FONT_HERSHEY_SIMPLEX
#    frame = cv2.imread('./fisheye/frame_00_test.png')

    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)

    while(cap0.isOpened()):
        ret, frame0 = cap0.read()    #print(type(frame), frame.dtype)
        ret, frame1 = cap1.read()    #print(type(frame), frame.dtype)
        print(frame.shape[:2])
        # preprocess
        frame_pad0 = preproc(frame0)
        frame_pad1 = preproc(frame1)

        #  create trackbar
        win = 'output'
        cv2.createTrackbar('x0', win, int(opts.get('--x0', x0)), xmax, update)
        cv2.createTrackbar('y0', win, int(opts.get('--y0', y0)), ymax, update)
        cv2.createTrackbar('r0', win, int(opts.get('--r0', r0)), rmax, update)
        cv2.createTrackbar('x1', win, int(opts.get('--x1', x1)), xmax, update)
        cv2.createTrackbar('y1', win, int(opts.get('--y1', y1)), ymax, update)
        cv2.createTrackbar('r1', win, int(opts.get('--r1', r1)), rmax, update)
        cv2.createTrackbar('a', win, int(opts.get('--a', a)), amax, update)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

#cap.release()
cv2.destroyAllWindows

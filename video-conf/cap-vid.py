

import numpy as np
import cv2
import math
from fish2pano_cv2_rgb import fish2pano


cap = cv2.VideoCapture(0)           # either 0 or 1 between facecam and action cam

#cap.set(CV_CAP_PROP_FPS, 2)

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()         # frame is numpy.ndarray
    print(frame.shape)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width = gray.shape

    # downsize image; skip frames
    gray_sm = cv2.resize(gray, (int(width/2), int(height/2)), interpolation = cv2.INTER_CUBIC)
    height, width = gray_sm.shape

    # square image
    edge = int((width-height)/2)
    gray_sq = gray_sm[edge:(edge+height), edge:(edge+height)] # crop only the middle
    half = height/2


    # unwarp frame
    #    imDest = Image.new("RGB", (4 * length, length) )
    #imDest = np.ndarray.shape(half, 4*half)
    imDest = np.ndarray(shape = (half, 4*half))
    # imBilinear = Image.new("RGB", (4 * length, height) )

    # backwards
    for i in range(0, int(4*half)):
        # for i in range(imDest.height/2, imDest.height):
        for j in range(0, int(half)):

            radius = float(half - j)
            # theta = 2.0 * math.pi * float(4.0 * length - j) / float(4.0 * length)
            theta = 2.0 * math.pi * float(i) / float(4.0 * half )
            # theta = 2.0 * math.pi * float(-j) / float(4.0 * length)

            # x', y' in the coordinates where o' = (half, -half)
            fTrueX = radius * math.cos(theta)
            fTrueY = radius * math.sin(theta)

            # xy in the coordinate where o = (0, 0)
            x = int( (round(fTrueX)) + half )
            y = int( (round(fTrueY)) ) - half


            # check bounds
            if x >= 0 and x < 2*half and y >= 0 and y < 2*half:
                imDest[half-j-1, i] = gray_sq[x, y]
            #    print(x, j, i, j)

    # wait 1s
    cv2.waitKey(1000);

    # display unwarped frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capturec
cap.release()
cv2.destroyAllWindows()

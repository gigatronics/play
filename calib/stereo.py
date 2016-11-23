# work in progress

import numpy as np
import cv2
#from matplotlib import pyplot as plt
import os

path = os.getcwd()+'/data/161025-2cam/test/'
print(os.path.exists(path))
imgL = cv2.imread((path+'le-001-pano.png'), 1)
imgR = cv2.imread((path+'re-001-pano.png'), 1)
#cv2.imshow('preview', imgL)
#cv2.waitKey(1000)

w, h = imgL.shape[: 2]

# temp values
cameraMatrix1 = [[ 244.79656725,    0.        ,  241.08056764],
       [   0.        ,  321.37010648,  316.39901554],
       [   0.        ,    0.        ,    1.        ]]
cameraMatrix2 = cameraMatrix1
distCoeffs1 = [-0.08473431, -0.0009205 , -0.01775865, -0.04750078,  0.01130868]
distCoeffs2 = distCoeffs1

retval,cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpointsL, imgpointsL, imgpointsR, (320,240))


# Params from camera calibration
camMats = [cameraMatrix1, cameraMatrix2]
distCoeffs = [distCoeffs1, distCoeffs2]

camSources = [0,1]
for src in camSources:
    distCoeffs[src][0][4] = 0.0 # use only the first 2 values in distCoeffs

# The rectification process
newCams = [0,0]
roi = [0,0]
for src in camSources:
    newCams[src], roi[src] = cv2.getOptimalNewCameraMatrix(cameraMatrix = camMats[src], distCoeffs = distCoeffs[src], imageSize = (w,h), alpha = 0)


#rectFrames = [0,0]
#for src in camSources:
#    rectFrames[src] = cv2.undistort(frames[src], camMats[src], distCoeffs[src])


#cv2.StereoCalibrate(objectPoints, imagePoints1, imagePoints2, pointCounts)
#cv2.STEREO_FISH_EYE_PRESET,
#
# SADWindowSize=15
# stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)#, SADWindowSize=15)
# disparity = stereo.compute(imgL,imgR)
# cv2.imshow('gray', disparity)
# #plt.show()

#  stereo calibration 

import numpy as np
import cv2
import glob
import os

import matplotlib


# termination criteria
term_crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1)

m = 5
n = 5

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) for (6x7, 3)
objp = np.zeros((m*n, 3), np.float32)
objp[:, : 2] = np.mgrid[0:m, 0:n].T.reshape(-1,2)
centres = np.zeros((m*n, 2), np.float32)


# Arrays to store object points and image points from all the images.
objpoints_c0 =[] #[np.dtype('f16')] # 3d point in real world space
imgpoints_c0 =[]#  [np.dtype('f16')] # 2d points in image plane.
objpoints_c1 =[] #[np.dtype('f16')] # 3d point in real world space
imgpoints_c1 =[]#  [np.dtype('f16')] # 2d points in image plane.

cameraMatrix1 = np.zeros((3, 3), np.float32)
cameraMatrix2 = np.zeros((3, 3), np.float32)


cwd = os.getcwd()

img_path = cwd+'/data/161025-2cam/test/'
images = glob.glob(img_path+'le*.png')

f = open(cwd+"/data/161025-2cam/test/cam1-cam2-calib.txt", "w")

for fname in images:
    print(fname)
    img = cv2.imread(fname)

    ret, centres = cv2.findCirclesGrid(img, (m,n))   #, blobDetector)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print('found')
        #print(objp, centres)
        objpoints_c0.append(objp)
        imgpoints_c0.append(centres)

        # this is to increase the corner accuracy...
        #corners2 = cv2.cornerSubPix(gray,centres,(20, 20),(-1,-1), criteria)
        #imgpoints.append(corners2)

        # Draw and display the corners
#        img2= cv2.drawChessboardCorners(img, (m, n), centres, ret)

        #cv2.imwrite(fname[:-4]+'-pts.png', img2)
        #cv2.waitKey(1000)
    else:
        print('Not found')

img_path = cwd+'/data/161025-2cam/test/'
images = glob.glob(img_path+'re*.png')


#ret, cameraMatrix0, distCoeffs0, rvecs, tvecs = cv2.calibrateCamera(objpoints_c0, imgpoints_c0, (640, 480), None, None)
cameraMatrix0_int= cv2.initCameraMatrix2D(objpoints_c0, imgpoints_c0, (640, 480), 1.33)

scale0, cameraMatrix0, distCoeffs0, r0, t0= cv2.calibrateCamera(objpoints_c0, imgpoints_c0, (640, 480), cameraMatrix0_int, None, None)
#print (scale0, cameramatrix0, distCoeffs0, r0, t0)


for fname in images:
    print(fname)
    img = cv2.imread(fname)

    ret, centres = cv2.findCirclesGrid(img, (m,n), term_crit)   #, blobDetector)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print('found')
        #print(objp, centres)
        objpoints_c1.append(objp)
        imgpoints_c1.append(centres)

        # this is to increase the corner accuracy...
        #corners2 = cv2.cornerSubPix(gray,centres,(20, 20),(-1,-1), criteria)
        #imgpoints.append(corners2)

        # Draw and display the corners
#        img2= cv2.drawChessboardCorners(img, (m, n), centres, ret)

        #cv2.imwrite(fname[:-4]+'-pts.png', img2)
        #cv2.waitKey(1000)
    else:
        print('Not found')


cameraMatrix1_int = cv2.initCameraMatrix2D(objpoints_c1, imgpoints_c1, (640, 480), 1.33)
#print(cameraMatrix1)

scale1, cameraMatrix1, distCoeffs1, r1, t1= cv2.calibrateCamera(objpoints_c1, imgpoints_c1, (640, 480), cameraMatrix0_int, None, None)
#print (scale, cameramatrix1, distCoeffs1, r1, t1)


# stereo calibration, note that the two objpoints are the same!
CV_CALIB_FIX_INTRINSIC =0x00100


imgpoints_c0_world = -np.transpose(r0)*t0          # camera 0 position in the world view
imgpoints_c1_world = -np.transpose(r1)*t1


# Finding elemnetary matrix and fundamental matrix
k, cameraMatrix0, distCoeffs0, cameraMatrix1, distCoeffs1, R, T, E, F = cv2.stereoCalibrate(objpoints_c0, imgpoints_c0, imgpoints_c1, cameraMatrix0, distCoeffs0, cameraMatrix1, distCoeffs1, (640, 480), None, None) #, flags=CV_CALIB_FIX_INTRINSIC)
#R = cv2.stereoCalibrate(objpoints_c0, imgpoints_c0, imgpoints_c1, cameraMatrix0, distCoeffs0, cameraMatrix1, distCoeffs1, (640, 480), term_crit, flags=CV_CALIB_FIX_INTRINSIC)
#print(F)

# alternative way to find fundamental matrix > but doesn't run
#F2 = cv2.findFundamentalMat(imgpoints_c0, imgpoints_c1)
#print(F2)

# with R and T, we can calculate roection matrix, P1 and P2
R0, R1, P0, P1, Q, roi0, roi1= cv2.stereoRectify(cameraMatrix0, distCoeffs0, cameraMatrix1, distCoeffs1, (640, 480), R, T)
print(P0, P1)

# alternative can estimate recitifcation homogaphy H without calibration (assume linear lens)  > doesn't run
#ans = cv2.stereoRectifyUncalibrated(imgpoints_c0, imgpoints_c1, F, (640, 480))
#print(ans)

# having P, can calculate objectpoints in the world
points4D = cv2.triangulatePoints(P0, P1, np.transpose(imgpoints_c0), np.transpose(imgpoints_c1))
print(points4D)


# next: calculat disparity from calibrated stereo image


# reprojectImageTo3D





#print gray.shape[: : -1], objpoints, imgpoints
#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[: 2], None, None)
#print(imgpoints.dtype)

#ret, mtx, dist, rvecs, tvecs = cv2.fisheye.calibrate(objpoints, imgpoints, img.shape[: 2], None, None)
#print(mtx, dist, rvecs, tvecs)
f.write("scaling, camera matrix, distortion, rotation, translation for cam0 and cam1: \n %s" % [scale0, cameraMatrix0, distCoeffs0, r0, t0, scale1, cameraMatrix1, distCoeffs1, r1, t1])

f.close()
cv2.destroyAllWindows()

# # print unwarpped images
# for fname in images:
#     print('correcting..')
#     img = cv2.imread(fname)
#     h,  w = img.shape[:2]
#     newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
#     print(newcameramtx)
#
#     # undistort
#     dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
#     print(dst)
#
#     # crop the image
#     #x,y,w,h = roi
#     #dst = dst[y:y+h, x:x+w]
#     cv2.imshow('corrected', dst)
#     cv2.waitKey(5000)
# #    cv2.imwrite('corrected.png',dst)

# cv2.destroyAllWindows()

# cv2.fisheye.calibrate() > doesnt' have python binding

import numpy as np
import cv2
import glob
import os

cwd = os.getcwd()
print(cwd)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1)

M = 5
N = 5

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) this is a 7x6 array
objp = np.zeros((M*N,3), np.float32)
objp[:,:2] = np.mgrid[0:M,0:N].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

f = open(cwd+"/calib/c0-cam-para-fisheye.txt", "w")

images = glob.glob(cwd+'/calib/161025-2cam/c0-intrinsic/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    #cv2.waitKey(500)


    # Find the chess board corners
    #ret, corners = cv2.findChessboardCorners(gray, (4,4), None)
    ret, centres = cv2.findCirclesGrid(img, (M,N), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print('found')
        objpoints.append(objp)
        imgpoints.append(centres)

        print(objpoints)

        # this is to increase the corner accuracy...
        #corners2 = cv2.cornerSubPix(gray,corners,(20, 20),(-1,-1), criteria)
        #imgpoints.append(corners2)

        # Draw and display the corners
        #img = cv2.drawChessboardCorners(img, (7,6), corners,ret)
        img = cv2.drawChessboardCorners(img, (M,N), centres, ret)
        cv2.imshow('img',img)
        cv2.waitKey(1000)

cv2.destroyAllWindows()

#print gray.shape[: : -1], objpoints, imgpoints
#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[: : -1], None, None)
#print(mtx, dist)

#k0 = cv2.fisheye.CALIB_USE_INTRINSIC_GUESS
#d0 =

ret, k1, d1, rvecs, tvecs = cv2.fisheye.calibrate(objpoints, imgpoints, img.shape[: : -1], None, None)     # <--------
print (k1, d1, rvecs, tvecs)


f.write("camera para, distortion, translation, rotation: \n %s" % [mtx, dist, tvecs, rvecs])
f.close()


#
# for fname in images:
#     print('correcting..')
#     img = cv2.imread(fname)
#     h,  w = img.shape[:2]
#     newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
#     print(newcameramtx)
#
#     # undistort
#     #dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
#     dst = cv2.fisheye.undistortImage(img, k1, d1, newcameramtx, None, None)
#     print(dst)
#
#     # crop the image
#     #x,y,w,h = roi
#     #dst = dst[y:y+h, x:x+w]
#     cv2.imshow('corrected', dst)
#     cv2.waitKey(5000)
# #    cv2.imwrite('corrected.png',dst)
#
# cv2.destroyAllWindows()

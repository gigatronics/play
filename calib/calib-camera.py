import numpy as np
import cv2
import glob
import os


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1)

m = 5
n = 5

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) for (6x7, 3)
objp = np.zeros((m*n, 3), np.float32)
objp[:, : 2] = np.mgrid[0:m, 0:n].T.reshape(-1,2)
centres = np.zeros((m*n, 2), np.float32)


# Arrays to store object points and image points from all the images.
objpoints =[] #[np.dtype('f16')] # 3d point in real world space
imgpoints =[]#  [np.dtype('f16')] # 2d points in image plane.

img_path = os.getcwd()+'/data/161025-2cam/c0-intrinsic/'
images = glob.glob(img_path+'*.png')
cwd = os.getcwd()

f = open(cwd+"/calib/c0-cam-para.txt", "w")


for fname in images:
    print(fname)
    img = cv2.imread(fname)

    # # setup blob detector:
    # params = cv2.SimpleBlobDetector_Params()
    # #params.minThresh = 10;
    # #params.maxThresh = 200;
    # params.filterByArea = True
    # params.minArea = 200
    # #params.filterByCirularity = True
    # params.minCircularity = 0.5
    # params.filterByConvexity = True
    # params.minConvexity = 0.5
    # blobDetector = cv2.SimpleBlobDetector_create(params)

    ret, centres = cv2.findCirclesGrid(img, (m,n))   #, blobDetector)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print('found')
        #print(objp, centres)
        objpoints.append(objp)
        imgpoints.append(centres)

        # this is to increase the corner accuracy...
        #corners2 = cv2.cornerSubPix(gray,centres,(20, 20),(-1,-1), criteria)
        #imgpoints.append(corners2)

        # Draw and display the corners
        img2= cv2.drawChessboardCorners(img, (m, n), centres, ret)


        #cv2.imwrite(fname[:-4]+'-pts.png', img2)
        #cv2.waitKey(1000)
    else:
        print('Not found')

#print gray.shape[: : -1], objpoints, imgpoints
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[: 2], None, None)
#print(imgpoints.dtype)

#ret, mtx, dist, rvecs, tvecs = cv2.fisheye.calibrate(objpoints, imgpoints, img.shape[: 2], None, None)
print(mtx, dist, rvecs, tvecs)
f.write("camera para, distortion, translation, rotation: \n %s" % [mtx, dist, tvecs, rvecs])

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

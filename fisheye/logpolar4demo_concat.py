import cv2
import os
import numpy as np
import glob



#files = glob.glob(os.getcwd()+'/data/161112-urbania-demo/*.png')
filesR = glob.glob(os.getcwd()+'/data/161112-urbania-demo/domeRpng/*.png')
filesL = glob.glob(os.getcwd()+'/data/161112-urbania-demo/domeLpng/*.png')
#filesR = glob.glob(os.getcwd()+'/data/161112-urbania-demo/testR/*.png')
#filesL = glob.glob(os.getcwd()+'/data/161112-urbania-demo/testL/*.png')
bkgnd = os.getcwd()+'/data/161112-urbania-demo/bkgnd_640.png'
PAD = 180

#file2 = os.getcwd()+'/fisheye/fish-me-small.png'
fourcc=cv2.VideoWriter_fourcc(* 'MJPG')
#out = cv2.VideoWriter('output-cv-pad-rvs-pad180-sidebyside.avi', fourcc, 24, (4000, 1000+2*PAD))
out = cv2.VideoWriter('output-cv-pad-rvs-pad180-sidebyside.avi', fourcc, 24, (4000*2, 1000+PAD))

def unwarp(fn):
    frame = cv2.imread(fn, 1)

    h, w = frame.shape[:2]
    frame_polar = cv2.linearPolar(frame, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)

    h, w = frame_polar.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_polar, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)
    frame_pad = cv2.copyMakeBorder(frame_pano, 0, PAD, 0, 0, cv2.BORDER_CONSTANT)
    #print(frame_pad.shape)

#    cv2.imwrite((fn[:-4]+'-pano.png'), frame_pano)
#
    return frame_pad


frameOut = np.zeros((1000+PAD, 4000*2, 3))
#frame_bkgnd = cv2.imread(bkgnd)
#print(frame_bkgnd.shape)

for i in range(len(filesR)):
    fnR = filesR[i]
    print(fnR)
    frame_pano_R = unwarp(fnR)
    #print(frame_pano_R.shape)

    fnL = filesL[i]
    print(fnL)
    frame_pano_L = unwarp(fnL)

    frameOut = np.concatenate((frame_pano_L, frame_pano_R), axis=1) # PATCHED IN REVERSE
    out.write(frameOut)

out.release()
cv2.destroyAllWindows
#    cv2.imshow('pre', frame_pano)
#    cv2.waitKey(0)

# frame.shape(), frame)

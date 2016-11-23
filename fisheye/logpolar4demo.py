import cv2
import os
import numpy as np
import glob

files = glob.glob(os.getcwd()+'/data/161112-urbania-demo/*.png')
#file2 = os.getcwd()+'/fisheye/fish-me-small.png'

fourcc=cv2.VideoWriter_fourcc(* 'MJPG')
out = cv2.VideoWriter('outputR.avi', fourcc, 24, (4000, 1000))

for fn in files:
    print(fn)
    frame = cv2.imread(fn, 1)

    h, w = frame.shape[:2]
    frame_polar = cv2.linearPolar(frame, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)

    h, w = frame_polar.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_polar, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

#    cv2.imwrite((fn[:-4]+'-pano.png'), frame_pano)
    out.write(frame_pano)

out.release()
cv2.destroyAllWindows
#    cv2.imshow('pre', frame_pano)
#    cv2.waitKey(0)

# frame.shape(), frame)

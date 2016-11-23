import cv2
import os
import numpy as np
import glob

filesR = glob.glob(os.getcwd()+'/data/161112-urbania-demo/domeRpng/*.png')
filesL = glob.glob(os.getcwd()+'/data/161112-urbania-demo/domeLpng/*.png')

filesR = os.getcwd()+'/data/161112-urbania-demo/domeRpng/output_0001.png'
filesL = os.getcwd()+'/data/161112-urbania-demo/domeLpng/output_0001.png'
#file2 = os.getcwd()+'/fisheye/fish-me-small.png'

fourcc=cv2.VideoWriter_fourcc(* 'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 24, (4000, 2000))

#for fn in filesR:
#    print(fn)

#for i in len(filesR):
frameR = cv2.imread(filesR, 1)
frameL = cv2.imread(filesL, 1)
#print(frameL.shape())
frameOut = np.hstack((frameR, frameL))
#print(frameOut.shape())

cv2.imshow('pre', frameOut)
cv2.waitKey(0)
#    cv2.imwrite((fn[:-4]+'-pano.png'), frame_pano)
#out.write(frameO)

out.release()
cv2.destroyAllWindows
#    cv2.imshow('pre', frame_pano)
#    cv2.waitKey(0)

# frame.shape(), frame)

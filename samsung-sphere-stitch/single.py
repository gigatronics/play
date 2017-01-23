# samsung gear 360 video processing

import cv2
import numpy as np

# ingest video
#cap = cv2.VideoCapture('/Users/geewiz/Documents/python/Desktop/2017-01-18-lachine/rob/')
#while(cap.isOpen()):
#    ret, frame = cap.read()

frame = cv2.imread('/Users/geewiz/Desktop/2017-01-18-lachine/larry/100.png')

# get half image
print(frame.shape)
height, width = frame.shape[:2]
top = frame[0:height, 0:width/2]
bot = frame[0:height, width/2:width]

#### for top half
# unwarp
small = cv2.pyrDown(top)
small2 = cv2.pyrDown(small)
h, w = small.shape[:2]
unwarp = cv2.linearPolar(small, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)
# rotate
rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)
rotate = cv2.warpAffine(unwarp, rot_mat, (w, h), flags=cv2.INTER_LINEAR)
#resize
pano_top = cv2.resize(rotate, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

#### for bot half
small = cv2.pyrDown(bot)
small2 = cv2.pyrDown(small)
h, w = small.shape[:2]
# unwarp
unwarp = cv2.linearPolar(small, (w/2, h/2), h/2, cv2.WARP_FILL_OUTLIERS)
# rotate
rot_mat = cv2.getRotationMatrix2D((w/2, h/2), 90, 1.0)
rotate = cv2.warpAffine(unwarp, rot_mat, (w, h), flags=cv2.INTER_LINEAR)
#resize
pano = cv2.resize(rotate, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)
#shift image
pano1 = pano[0:h/2, w:w*2]
pano2 = pano[0:h/2, 0:w]
pano_bot = np.hstack((pano1, pano2))

#### stitch two images
pano = np.vstack((pano_top, pano_bot))



# parameters are linear polar parameters.. x, y, and r for both top and bot...
# define cost function = sum of key points distances...
# ... first find key points from top, then bot
# ...
# adjust x, y, r for top, to min cost function
# the stitched image would be a monoscopic



# another idea is to extract the scene info and stitch based on depth? how?


cv2.imwrite('top.png', pano_top)
cv2.imwrite('bot.png', pano_bot)

cv2.imshow('pano', pano)
cv2.waitKey(0)

# repeat

# save to video

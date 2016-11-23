import cv2
import numpy as np
import math
import time
from lut import lut
import os

def fish2pano(img):

    # import image
    # path = '/Users/gzhou/TL_documents/data/160823-3cam/'
    # filename = 't2c1.jpg'

    #img = cv2.imread(filename)

    height, width = img.shape[: 2]
    # # image resizing
    # if height > 512:
    #     img = cv2.resize(img, (int(width/4), int(height/4)), interpolation = cv2.INTER_CUBIC)
    #     print ('image is too big, resized to ', img.shape[: 2])
    # elif  width != height:

    if width !=height:
        #img_sq = np.ndarray(shape = (width, width, 3))
        diff = int((width-height)/2)
        img_sq = img[0:height, diff:(diff+height)] # crop only the middle
        print ('image is now squared of size ', img_sq.shape[: 2])
    else:
        img_sq = img
        print('image size is ', img_sq.shape[: 2])


    #cv2.imshow("small", img)

    # new array:
    radius = img_sq.shape[1]/2
    #print(radius)
    imDest = np.ndarray(shape = (int(radius), int(4*radius), 3), dtype= 'uint8')
    #print (radius)

    dict = lut(radius)

    for j in range(int(radius)):
        for i in range(int(4*radius)):

            ## replace the folloiwng four lines with a lookup talbe.
            R = radius - j
            theta = - 2.0 * math.pi * i / (4.0 * radius)

            x = int( (R * math.cos(theta)) + radius )
            y = radius - int( R * math.sin(theta) )

            # check bounds
            if x >= 0 and x < 2*radius and y >= 0 and y < 2*radius:
                #print(x, y, i, j)
                imDest[radius-j-1, i]  = img_sq[x, y]


    #cv2.imwrite('/Users/gzhou/TL_documents/python/fisheye/test.png', imDest)
    #imDest_u8 = cv.CvtColor(imDest, imDest_u8, 'u8')
    return imDest
    print('saved')


def fish2pano_lut(img):


    height, width = img.shape[: 2]

    if width !=height:
        diff = int((width-height)/2)
        img_sq = img[0:height, diff:(diff+height)] # crop only the middle


        #length = min(width, height)
        #diff = int(abs((width-height)/2))
        #img_sq = img[0:length, diff:(diff+length)] # crop only the middle


        print ('image is now squared of size ', img_sq.shape[: 2])
    else:
        img_sq = img
        print('image size is ', img_sq.shape[: 2])

    # new array:
    radius = img_sq.shape[1]/2
    #print(radius)
    imDest = np.ndarray(shape = (int(radius), int(4*radius), 3), dtype= 'uint8')
    #print (radius)

    dict = lut(radius)

    for j in range(int(radius)):
        for i in range(int(4*radius)):

            x, y = dict[(i,j)]

            # check bounds
            if x >= 0 and x < 2*radius and y >= 0 and y < 2*radius:
                #print(x, y, i, j)
                imDest[radius-j-1, i]  = img_sq[x, y]

    #cv2.imwrite('/Users/gzhou/TL_documents/python/fisheye/test.png', imDest)
    #imDest_u8 = cv.CvtColor(imDest, imDest_u8, 'u8')
    return imDest
    print('saved')



# a function to figure out how to run multiple streams - NON FUNCTIONAL
def fish2pano_lut_multi_ps(img):


    height, width = img.shape[: 2]

    if width !=height:
        diff = int((width-height)/2)
        img_sq = img[0:height, diff:(diff+height)] # crop only the middle


        #length = min(width, height)
        #diff = int(abs((width-height)/2))
        #img_sq = img[0:length, diff:(diff+length)] # crop only the middle


        print ('image is now squared of size ', img_sq.shape[: 2])
    else:
        img_sq = img
        print('image size is ', img_sq.shape[: 2])

    # new array:
    radius = img_sq.shape[1]/2
    #print(radius)
    imDest = np.ndarray(shape = (int(radius), int(4*radius), 3), dtype= 'uint8')
    #print (radius)


    dict = lut(radius)

    for j in range(int(radius)):
        for i in range(int(4*radius)):

            x, y = dict[(i,j)]

            # check bounds
            if x >= 0 and x < 2*radius and y >= 0 and y < 2*radius:
                #print(x, y, i, j)
                imDest[radius-j-1, i]  = img_sq[x, y]

    #cv2.imwrite('/Users/gzhou/TL_documents/python/fisheye/test.png', imDest)
    #imDest_u8 = cv.CvtColor(imDest, imDest_u8, 'u8')
    return imDest
    print('saved')


if __name__ == "__main__":
    img = np.zeros((2448, 2448, 3))
    #img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_path = '/Users/gzhou/TL_documents/python/fisheye/fish-me-small.png'
    #print os.path.exists(img_path)
    img = cv2.imread(img_path)

    #print(type(img))

    start = time.time()
    img_pano = fish2pano(img)
    end = time.time()
    print('baseline: ', end-start)
    cv2.imwrite("fish-me-pano-base.png", img_pano)

    start = time.time()
    img_pano2 = fish2pano_lut(img)
    end = time.time()
    print('with lut: ', end-start)
    cv2.imwrite("fish-me-pano-lut.png", img_pano2)

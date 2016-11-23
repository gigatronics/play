import numpy as np
import cv2
import math

def fish2pano(img):

    # import image
    # path = '/Users/gzhou/TL_documents/data/160823-3cam/'
    # filename = 't2c1.jpg'

    #img = cv2.imread(filename)

    height, width = img.shape[: 2]

    # image resizing
    if height > 512:
        img = cv2.resize(img, (int(width/4), int(height/4)), interpolation = cv2.INTER_CUBIC)
        print ('image is too big, resized to ', img.shape[: 2])
    elif  width != height:
        diff = int((width-height)/2)
        img = img[diff:(diff+height), diff:(diff+height)] # crop only the middle
        print ("image is now square! ")
    else:
        print("image size is ", img.shape [: 2])

    cv2.imshow("small", img)

    # new array:
    radius = img.shape[1]/2
    print(radius)
    imDest = np.ndarray(shape = (radius, 4*radius, 3))
    #print (radius)

    for j in range(radius):
        for i in range(4*radius):

            R = radius - j
            theta = - 2.0 * math.pi * i / (4.0 * radius)

            x = int( (R * math.cos(theta)) + radius )
            y = radius - int( R * math.sin(theta) )

            # check bounds
            if x >= 0 and x < 2*radius and y >= 0 and y < 2*radius:
                #print(x, y, i, j)
                imDest[radius-j-1, i]  = img[x, y]

    #cv2.imwrite('/Users/gzhou/TL_documents/python/fisheye/test.png', imDest)
    return imDest
    print('saved')

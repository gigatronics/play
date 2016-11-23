
## needs debugging

import numpy as np
import glob
import cv2

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape)/2)
  rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
  return result


if __name__ == "__main__":

    img_path = '/Users/gzhou/TL_documents/python/video-conf/161024-stereo/test/'

    img_list = []
    for filename in glob.glob(img_path+'*.png'):
        img = cv2.imread(filename)
        imgr = rotateImage(img, 90)
        img_list.append(img)
        cv2.imsave(filename+'r.png', imgr)

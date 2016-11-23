import cv2
import os
import numpy as np

def map_2cam2eye(frame0, frame1, angle):   # angle = stitch position


    #print(img.shape)
    height, width = frame0.shape[:-1]
    shift = angle * width / 360
    #print(width, shift)

    re = np.zeros((height, width, 3), np.uint8)
    le = np.zeros((height, width, 3), np.uint8)

    for h in range(height):
        #
        # re[h, range(0, width/2), :] = frame0[h, range(0, width/2), :].copy()
        # re[h, range(width/2, width), :] = frame1[h, range(0, width/2), :].copy()
        # le[h, range (0, width/2), :] = frame1[h, range(0, width/2), :].copy()
        # le[h, range (width/2, width), :] = frame0[h, range(0, width/2) :].copy()
        re1 = frame0[h, range(shift, width/2+shift), :]
        re2 = frame1[h, range(0, shift)]
        re3 = frame1[h, range(width/2+shift, width), :]

        le1 = frame1[h, range(shift, width/2+shift), :]
        le2 = frame0[h, range(0, shift)]
        le3 = frame0[h, range(width/2+shift, width), :]

        re[h, :]= np.concatenate((re2, re1, re3))
        le[h, :] = np.concatenate((le2, le1, le3))

#        np.append(re, re)
    #
    return re, le

if __name__ == "__main__":

#
# cwd = os.getcwd()
# img_path = cwd+'/video-conf/161024-stereo3/le-pano/'
# print(os.path.exists(img_path))
#img_list = []
#for filename in glob.glob(img_path+'*.png'):


    img_path = os.getcwd()+'/video-conf/161025-stereo-align/test/'
    #print(os.path.exists(img_path))
    frame0 = cv2.imread(img_path+'c0-001-pano.png')
    frame1 = cv2.imread(img_path+'c1-001-pano.png')

    re, le = map_2cam2eye(frame0, frame1, 90)
    cv2.imwrite(img_path+'re.png', re)
    cv2.imwrite(img_path+'le.png', le)

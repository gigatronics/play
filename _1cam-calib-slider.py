'''


'''

import cv2
import ids
import numpy as py
import matplotlib.pyplot as plt
import sys, getopt


# help(ids) and print(ids.camera_list()) to find out which ones are connected
#print(ids.camera_list())

def preproc(frame): # this function is only for action cam with 16:9 sensor captured as 4:3

    #resize 16:9 to 4:3 images... eg. 640x480 to 960x480
    #h, w = (frame.shape[0], frame.shape[1]*3/2)

    # this is CP cam

    h, w = frame.shape[:2]
    #frame_resize = cv2.resize(frame, (w, h))
    diff = (w-h)/2
    frame_resize = frame[0:h, diff:(diff+h)]     # x, y, w, h ... y:y+h, x:x+w
    return frame_resize
    #
    # # pad image... e.g.1296x1296
    # if (w !=h):
    #     #img_sq = np.ndarray(shape = (width, width, 3))
    #     diff = int((w-h)/2)
    #     # pad
    #     #frame_pad = cv2.copyMakeBorder(frame, diff, diff, 0, 0, cv2.BORDER_CONSTANT) # top, bot, left, right
    #     # crop
    # #        img_sq = img[0:h, diff:(diff+h)] # crop only the middle
    #     h, w = frame_pad.shape[: 2]
    #     #print ('image is now squared of size ', (w, h) )
    # else:
    #     frame_pad = frame
    #     h, w = frame_pad.shape[: 2]
    return frame_resize

#
# def warp(frame):
# #    ret, frame = cam.read()
#     polar = cv2.linearPolar(frame, (x, y), r, cv2.WARP_FILL_OUTLIERS)
#     return polar

def postproc(frame):
    # rotate 90
    h, w = frame.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame, rot_mat, (w, h), flags=cv2.INTER_LINEAR)

    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)

    # option 1: play back
#    cv2.imwrite('frame_pano.png', frame_pano)
    return frame_pano



if __name__ == '__main__':

    xmax, ymax, rmax = (1944,1944,1944)
    x, y, r = (xmax/2, ymax/2, rmax/2)
    x, y, r = (635, 510, 555)   # cam1
    x, y, r = (650, 510, 555)   # cam2
    x, y, r = (655, 500, 555)   # cam2
    x, y, r = (512, 512, 512)   # rst

    opts, args = getopt.getopt(sys.argv[1:], '', ['x', 'y', 'r'])
    opts = dict()

    cam = ids.Camera(1)
    cam.color_mode = ids.ids_core.COLOR_RGB8
    cam.exposure = 100
    cam.auto_exposure = False #True
    cam.continuous_capture = True
    #
    # cam1 = ids.Camera(3)i
    # cam1.color_mode = ids.ids_core.COLOR_RGB8
    # cam1.exposure = 5
    # cam1.auto_exposure = True
    # cam1.continuous_capture = True
    #
    # cam2 = ids.Camera(2)
    # cam2.color_mode = ids.ids_core.COLOR_RGB8
    # cam2.exposure = 5
    # cam2.auto_exposure = True
    # cam2.continuous_capture = True

    font = cv2.FONT_HERSHEY_SIMPLEX
    def update(_):
        x = cv2.getTrackbarPos('x', win)
        y = cv2.getTrackbarPos('y', win)
        r = cv2.getTrackbarPos('r', win)

        # fisheye to rectlinear
        frame_polar = cv2.linearPolar(frame_pad, (x, y), r, cv2.WARP_FILL_OUTLIERS)
        frame_pano = postproc(frame_polar)

        cv2.putText(frame_pano, ('params (x, y, r) = '+ str(x) + ', ' + str(y) + ', ' + str(r)), (10, 100), font, 1, (0, 255, 0), 2)
        cv2.imshow(win, frame_pano)
    #    cv2.waitKey()

    while(1):
        img0, meta = cam.next()
        # img1, meta = cam1.next()
        # img2, meta = cam2.next()
        small = cv2.pyrDown(img0)

#        polar = warp(small)
#        pano = postproc(polar)

        frame_pad = preproc(small)

#        cv2.imshow('cam1', cv2.pyrDown(img1))

        # plt.subplot(221), plt.imshow(img0),plt.title('img0')
        # plt.subplot(222), plt.imshow(img1),plt.title('img1')
        # plt.subplot(223), plt.imshow(img2),plt.title('img2')
        # plt.show()

        #  create trackbar
        win = 'output'
        cv2.createTrackbar('x', win, int(opts.get('--x', x)), xmax, update)
        cv2.createTrackbar('y', win, int(opts.get('--y', y)), ymax, update)
        cv2.createTrackbar('r', win, int(opts.get('--r', r)), rmax, update)
        update(None)


        #cv2.waitKey(0)
        if cv2.waitKey() & 0xFF==ord('q'):
            break

    #bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #cv2.imwrite('test.jpg', bgr_img)

    cv2.destroyAllWindows

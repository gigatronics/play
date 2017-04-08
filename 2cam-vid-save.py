'''
play a video from the cam using manually set parameters

todo:
x- get live view
x- fix color
x- save the video > can't control the exposure...- save at HQ?!
- show/save 2 cams?!
- toggle beween low res and high res


status:
works as is.. videos are right sized, padded.. color is corrected.. frames drops.. need to slow down the frame 4x in ffmpeg

'''

import cv2
import ids
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt
import os


# help(ids) and print(ids.camera_list()) to find out which ones are connected
#print(ids.camera_list())



def preproc(frame, a): # this function is only for action cam with 16:9 sensor captured as 4:3

    h, w = frame.shape[:2]
    #frame_resize = cv2.resize(frame, (w, h))
    diff = (w-h)/2
    frame_resize = frame[0:h, diff:(diff+h)]     # x, y, w, h ... y:y+h, x:x+w

    rot_mat = cv2.getRotationMatrix2D((h/2, h/2), a, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame_resize, rot_mat, (h, h), flags=cv2.INTER_LINEAR)

    return frame_rot


def postproc(frame):
    # rotate 90
    h, w = frame.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((w/2, h/2), -90, 1.0)  # center,  angle, scale
    frame_rot = cv2.warpAffine(frame, rot_mat, (w, h), flags=cv2.INTER_LINEAR)
    # resize to pano view
    frame_pano = cv2.resize(frame_rot, (w*2, h/2))#, interpolation=cv2.CV_INTER_CUBIC)
    return frame_pano


if __name__ == '__main__':

    PAD = 600
    vid_size = (1024*4, 1024*2 + PAD*2)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('./temp/test2.avi', fourcc, 48, vid_size) #(w, h)

    x, y, r = (1024, 1024, 1024)
    a = -120

#    print(x, y, r)

    opts, args = getopt.getopt(sys.argv[1:], '', ['x', 'y', 'r'])
    opts = dict()

    cam = ids.Camera(1)
    cam.color_mode = ids.ids_core.COLOR_RGB8
    cam.exposure = 40
    cam.auto_exposure = True
    cam.continuous_capture = True

    cam1 = ids.Camera(2)
    cam1.color_mode = ids.ids_core.COLOR_RGB8
    cam1.exposure = 50
    cam1.auto_exposure = True
    cam1.continuous_capture = True
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
    win = 'output'
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

    frame_vstack = []
    while(1):
        img0, meta = cam.next()
        img1, meta = cam1.next()

        frame_resize0 = preproc(img0, 0)
        frame_resize1 = preproc(img1, a)
#        cv2.imshow('cam1', cv2.pyrDown(img1))

        # fisheye to rectlinear
        frame_polar0 = cv2.linearPolar(frame_resize0, (x, y), r, cv2.WARP_FILL_OUTLIERS)
        frame_pano0 = postproc(frame_polar0)

        frame_polar1 = cv2.linearPolar(frame_resize1, (x, y), r, cv2.WARP_FILL_OUTLIERS)
        frame_pano1 = postproc(frame_polar1)

        frame_pad0 = cv2.copyMakeBorder(frame_pano0, 0, PAD, 0, 0, cv2.BORDER_CONSTANT) # top, bot, left, right
        frame_pad1 = cv2.copyMakeBorder(frame_pano1, 0, PAD, 0, 0, cv2.BORDER_CONSTANT) # top, bot, left, right

        frame_vstack = np.concatenate((frame_pad0, frame_pad1), axis = 0)
        h, w = frame_vstack.shape[:2]

        frame_color = cv2.cvtColor(frame_vstack, cv2.COLOR_RGB2BGR)
        print(frame_color.shape[:2], vid_size)

#        small0 = cv2.pyrDown(img_bgr0)
#        small1 = cv2.pyrDown(img_bgr1)

        cv2.putText(frame_color, ('img info: '+ str(w) + 'x' + str(h)), (10, 100), font, 1, (0, 255, 0), 2)

        # cv2.imshow(win, frame_color)
        # cv2.waitKey(0)
        out.write(frame_color)


        # #  create trackbar
        # cv2.createTrackbar('x', win, int(opts.get('--x', x)), xmax, update)
        # cv2.createTrackbar('y', win, int(opts.get('--y', y)), ymax, update)
        # cv2.createTrackbar('r', win, int(opts.get('--r', r)), rmax, update)


#    print('Press SPACE to save the image\n')
#    while(1):
#        ch = 0xFF & cv2.waitKey(1)
#        if ch==ord(' '):
#              bgr_img = cv2.cvtColor(frame_pano, cv2.COLOR_RGB2BGR)
#              cv2.imwrite('test.png', bgr_img)
#              print(('png saved in '+ os.getcwd()))

#        if ch ==27:
#            break

    cv2.destroyAllWindows

    #cv2.imwrite('test.jpg', bgr_img)

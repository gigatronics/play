# run ffmpeg -f avfoundation -list_devices true -i video

import numpy as np
import cv2

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
directory = '/Users/gzhou/TL_documents/python/video-conf/'
out0 = cv2.VideoWriter(directory+'output0-fisheye.avi', fourcc, 30, (640, 480))
out1 = cv2.VideoWriter(directory+'output1-fisheye.avi', fourcc, 30, (640, 480))
out2 = cv2.VideoWriter(directory+'output2-fisheye.avi', fourcc, 30, (640, 480))


cap0 = cv2.VideoCapture(0)
cap0.set(3, 640)
cap0.set(4, 480)    # this give 160x120 images

cap1 = cv2.VideoCapture(3)
cap1.set(3, 640)
cap1.set(4, 480)    # this give 160x120 images

cap2 = cv2.VideoCapture(2)
cap2.set(3, 640)
cap2.set(4, 480)    # this give 160x120 images

#while(cap.get(1)<5):
while(cap0.isOpened() and cap1.isOpened() and cap2.isOpened):
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if (ret0==True and ret1 ==True and ret2 == True):
#        frame0 = cv2.flip(frame0,0)          # write the flipped frame
        print("write")
        out0.write(frame0)
        out1.write(frame1)
        out2.write(frame2)

    #    stack = np.vstack((pano0, pano1))

#        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


# Release everything if job is finished
cap0.release()
cap1.release()
cap2.release()

out0.release()
out1.release()
out2.release()

cv2.destroyAllWindows()

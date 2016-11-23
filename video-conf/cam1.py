import numpy as np
import cv2

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
directory = '/Users/gzhou/TL_documents/python/video-conf/'
out1 = cv2.VideoWriter(directory+'output1.avi', fourcc, 1.0, (640, 480))
#
cap1 = cv2.VideoCapture(1)
cap1.set(3, 640)
cap1.set(4, 480)    # this give 160x120 images


while(cap1.isOpened()):
    ret1, frame1 = cap1.read()
    assert ret1

    if ret1==True:
        frame1 = cv2.flip(frame1,0)
        out1.write(frame1)

        #cv2.imshow(frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished

cap1.release()
out1.release()
cv2.destroyAllWindows()

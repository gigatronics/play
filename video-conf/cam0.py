import numpy as np
import cv2

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(c1, c2, c3, c4)
#fourcc = cv2.CV_FOURCC(*'MJPG')

#w = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
#h = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
#size(int(w), int(h))
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
directory = '/Users/gzhou/TL_documents/python/video-conf/'
out0 = cv2.VideoWriter(directory+'output0.avi', fourcc, 1.0, (640, 480))

# while cap.get(1)<20:
#     flag, img = cap.read()
#     if cap.get(1)==1:
#         cv2.imwrite('output2.avi', img)
#
cap0 = cv2.VideoCapture(0)
cap0.set(3, 640)
cap0.set(4, 480)    # this give 160x120 images


#while(cap.get(1)<5):
while(cap0.isOpened()):
    ret0, frame0 = cap0.read()
    assert ret0

    if ret0==True:
        #frame0 = cv2.flip(frame0,0)          # write the flipped frame
        out0.write(frame0)
        #print(frame0.shape)
        #cv2.imshow(frame0)

#        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


# Release everything if job is finished
cap0.release()
out0.release()

cv2.destroyAllWindows()

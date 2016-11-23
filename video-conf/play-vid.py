# this piece of code reads the file and tracks the difference in the video
#
# the bascis steps involves the following:
## fetch frames:
## reduce res to 16x16 macroblocks
## calculuate error for each block by taking RMS
## prioritize high error frames


import numpy as np
import cv2
import time

#cap = cv2.VideoCapture(0)           # either 0 or 1 between facecam and action cam
cap = cv2.VideoCapture('handwaving.avi')        # to playback a video
fgbg = cv2.createBackgroundSubtractorMOG2()

#w = cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH)
#h = cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')    # MJPG OR XVID
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))       #fps = 20Hz
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))       #fps = 20Hz

fgmasks = []
i = 0

while(1):

    ret, frame = cap.read()
    out.write(frame)

    fgmask = fgbg.apply(frame)

    #print(fgmask.shape)
    #fgmasks.append(fgmask)

    cv2.imshow('frame',fgmask)
    #cv2.imwrite(('frame'+str(i)+'.jpg'), fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    i += 1
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break
# else:
#     break



cap.release()
out.release()
cv2.destroyAllWindows()



#
#
# #------------------------
#
# #
# # # play video
# # while(True):
# #     # Capture frame-by-frame
# #     ret, frame = cap.read()
# #
# #     # Our operations on the frame come here
# #     #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #
# #
# #     # Display the resulting frame
# #     cv2.imshow('frame', gray)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
# #
# # # figure out number of frames in the Video
# # #l = cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)
# #
#
# # fetch frames:
# list_of_frames = []
#
# for i in range(20):
#     ret, frame = cap.read()
#
#     # trim image into sqaure
#     res = cv2.resize(frame, (480, 480), interpolation = cv2.INTER_CUBIC)
#
#     # append frames
#     list_of_frames.append(res)
#     time.sleep(1)
#
# cap.release()
#
# # reduce res to 16x16 macroblocks
#
# list_of_frames_sm = []
# for (i, frame, ) in enumerate(list_of_frames):
#     frame1 = cv2.pyrDown(frame)
#     list_of_frames_sm.append(frame1)
#
#
# # calculuate error for each block by taking RMS
#
# list_of_error = []
# prev_frame = frame1
#
# for (i, frame1, ) in enumerate(list_of_frames_sm, start = 1):
#     error = frame1 - prev_frame
#     prev_frame = frame1
#     list_of_error.append(error)
#
#
# # prioritize high error frames
#
# for (i, error, ) in enumerate(list_of_error):
#     cv2.imshow('frame {}'.format(i), error)             # frame title "frame #"
#
# #waitKey causes pending tasks to process.
# #imshow is a pending task.
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#
# #
# ##
# #
# # # When everything done, release the capture
# # cap.release()
# # cv2.destroyAllWindows()

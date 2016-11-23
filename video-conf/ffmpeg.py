import subprocess as sp
import numpy as np
import os
import urllib
import platform
import cv2
# files = os.listdir()

#args = '/usr/bin/ffmpeg', '-i', files[0], files[0][:-4].replace(' ', '_') + '.mp3'
#os.execl('usr/bin/ffmpeg', *args)

cam2 = "http://localhost:8090/cam2.mjpeg"
stream=urllib.urlopen(cam2)
bytes = ''

while True:
    # to read mjpeg frame -
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    # we now have frame stored in frame.

    cv2.imshow('cam2',frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



#sp.call(['/usr/bin/ffmpeg', '-i \', 'output.avi', '-t', '5'])
#sp.call(['/usr/local/bin/ffmpeg -i ./video-conf/output1.avi -t 5'], shell=True)

# command = [FFMPEG_BIN,
#             '-ss', '00:00:00',
#             '-i', 'handwaving-RAW.mp4',
#             '-ss', 1        # skip 1 sec of movie... so starts at 00:00:01
#             '-f', 'image2pipe',
#             '-pix_fmt', 'rgb24',
#             '-vcodec', 'rawvideo', '-']
# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
#
#
# # read frames of a video
# raw_image = pipe.stdout.read(640*480*3)
# image = numpy.fromstring(raw_image, dtype ='uint8')
# image = image.reshape((480, 640, 3))
# pipe.stout.flush

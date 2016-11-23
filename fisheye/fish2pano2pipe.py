import cv2
import numpy as np
import math
from fish2pano_cv2_rgb import fish2pano
import time
import os
import subprocess as sp
import sys

#
# command = [FFMPEG_BIN,
#         '-y', # (optional) overwrite output file if it exists
#         '-f', 'rawvideo',
#         '-vcodec','rawvideo',
#         '-s', '480x480', # size of one frame
#         '-pix_fmt', 'rgb24',
#         '-r', '1', # frames per second
#         '-i', '-', # The imput comes from a pipe
#         '-an', # Tells FFMPEG not to expect any audio
#         '-vcodec', 'mpeg',
#         'output.mp4' ]
#
# pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)

#command = '/usr/local/bin/ffmpeg -pix_fmt bgr24 -s 240x960 -r 1 -i - -vcodec mjpeg http://localhost:8090/cam2.ffm'

#ffplay -f rawvideo -pix_fmt bgr24

# # test run time
# frame = cv2.imread(os.getcwd()+'/fisheye/fish-me.jpg')
# start = time.time()
# pano = fish2pano(frame)# end = time.time()# print(end-start)    # 1.5s to unwarp 612x612 image

cap = cv2.VideoCapture(0)
#width = cap.get(CV_CAP_PROP_FRAME_WIDTH)
#height = cap.get(CV_CAP_PROP_FRAME_HEIGHT)
#fps = cap.get(CV_CAP_PROP_FPS)
#print(fps)
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(os.getcwd()+'/fisheye/output.avi', fourcc, 1, (240, 960), isColor = 1)
#print(type(out), out.dtype)

count =0

#pano = Image.new("RGB", (240, 960), (i, 1, 1))
#p = sp.Popen('/usr/local/bin/ffmpeg -f image2pipe -r 1/2 -s 240x960 -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True, stdin=PIPE)
#sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i frame.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)

# cmdline = ['vlc', '--demux', 'h264', '-'] #pick a media player
# cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
#player = subprocess.Popen(cmdlin, stdin=sp.PIPE)

while(cap.isOpened()):       #-f image2pipe
    command = '/usr/local/bin/ffmpeg -f image2 -i - c-s 240x960 -pix_fmt bgr24 -r 1 -c:v mjpeg  http://localhost:8090/cam2.ffm'
    player = sp.Popen(command, stdin=sp.PIPE, bufsize=10**8, shell=True)

    ret, frame = cap.read()    #print(type(frame), frame.dtype)

    start = time.time()

    pano = fish2pano(frame) #.astype('u8')

#    print(pano.shape, pano.dtype)       # (240, 960, 3)
#    out.write(pano)

#    ret, jpeg = cv2.imencode('.jpg', pano)
#    pano = jpeg.tobytes()
#    sp.call('/usr/local/bin/ffmpeg -f image2 -r 1 -i pano.jpg http://localhost:8090/cam2.ffm', shell=True)

#    cv2.imwrite(os.getcwd()+'/fisheye/frame.png' % count, pano)
#    count +=1

#   p.stdout.write(frame.tostring())
#    cv2.imwrite('frame.png', pano)
#    sp.call('/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i frame.png -vcodec mjpeg http://localhost:8090/cam2.ffm', shell=True)


    data = sock.recv(1024)
    player.stdin.write(pano.tostring())
    #pipe.stdin.write(pano.tostring())
    #pipe.communicate(pano.tostring())


    end = time.time()
    print(end-start)
    #cv2.waitKey(1000)

#sp.call(['/usr/local/bin/ffmpeg -f image2 -s 240x960 -r 1 -i image2pipe -vcodec mpeg4 -y mvoei.mpeg'], shell=True)

cap.release()
out.release()
cv2.destroyAllWindows

import time
from multiprocessing import Pool

import cv2
from fish2pano_cv2_rgb import fish2pano_lut
from datetime import datetime as dt
import time
import os

def process_frame(frame_id, frame_data):
    # this function simulates the processing of the frame.
    # I used a longer sleep thinking that it takes longer
    # and therefore the reason of parallel processing.

    frame_pano = fish2pano_lut(frame)
    print("... got frame {}".format(frame_id))
    return frame_pano

    #char = frame_data[frame_id]
    #count = frame_data.count(char)
    #return frame_id, char, count

def process_result(res):
    # this function simulates the function that would receive
    # the result from analyzing the frame, and do what is
    # appropriate, like printing, making a dict, saving to file, etc.
    # this function is called back when the result is ready.
    frame_id, frame_pano = res
    print('processing {}'.format(frame_id))
    return frame_pano
    #print("in frame {}".format(frame_id), \
    #    ", character '{}' appears {} times.".format(chr(char), count))

if __name__ == '__main__':
    cam1 = cv2.VideoCapture(0)
    frame_num = 0
    i = 0

    from multiprocessing import Pool

    while(cam1.isOpened()):
        ret, frame = cam1.read()
        i = i+1

        pool = Pool(4)      # start 4 workers

        results =[ pool.apply_async(os.getpid, ()) for i in range(4)]
        print[(res.get(timeout=1) for res in results)]

        #t0 = dt.now()
        start = time.time()
        #for i in range(20):   # I limited this loop to simulate 20 frames
                              # but it could be a continuous stream,
                              # that when finishes should execute the
                              # close() and join() methods to finish
                              # gathering all the results.

        # The following lines simulate the video streaming and
        # your selecting the frames that you need to analyze and
        # send to the function process_frame.
        frame_id = i
        frame_data = frame # 'a bunch of binary data representing your frame'
        end = time.time()
        print(end - start)
        pool.apply_async(process_frame(frame_id, frame_data), callback=process_result) #func, #args, # return value


        #print(dt.now() - t0)
pool.close()
pool.join()



import cv2
import time
import multiprocessing
from fish2pano_cv2_rgb import fish2pano_lut



class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue                    # the queue and item
        self.result_queue = result_queue
        #other initialization stuff

    def run(self):
        while True:
            frame_num, frame = self.task_queue.get()               # consumer go gets the tasks and does it

            #Do computations on image, 1-2sec
            frame_pano = fish2pano_lut(frame)

            # put the results in queue
            self.result_queue.put(frame_pano)
        return

pool = multiprocessing.Pool()

for (frame_pano, frame) in pool.imap(fish2pano_lut(frame), frame)
    cv2.imshow('preview', frame_pano)

# Tasks queue with size 1 - only want one image queued for processing.
# Queue size should therefore match number of processes !!!!!


tasks = multiprocessing.Queue(1)
results = multiprocessing.Queue(20)
consumer = Consumer(tasks, results)
consumer.start()


#Creating window and starting video capturer from camera
# take input frames, and store the into a buffer
# in a parallel process, fetch videos every x second...  package and send over down the pipe.

cam1 = cv2.VideoCapture(0)
frame_num = 0

while(cam1.isOpened()):
    ret, frame = cam1.read()
    #frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)      # resize prev image

# the process loop:
    frame_num += 1

    start = time.time()

    # put captured frame in task queue, if empty
    try:
        tasks.put((frame_num, frame))
    except:
        pass

    # get results if ready
    try:
        frame_out = results.get()
    except:
        pass

    end = time.time()
    print(end-start)
    print('current frame# is ', frame_num)


processor.terminate()










# other Functions


def bufferSelection(itemUrl, fp):
        print('Fetching ' + itemUrl + '...');

        video_file_size_start = 0;
        video_file_size_buffer = 1048576 * cacheSize;  # end in CacheSize in  MB
        video_file_size_end = 0;
        block_size = 1024;

        r = REQ.get(itemUrl, auth=HTTPDigestAuth('tivo', mak), verify=False, stream=True);
        if r.status_code == REQ.codes.ok:
                print('HTTP Request sent, awaiting response... 200 OK');
                if r.headers['tivo-estimated-length'] != None:
                        video_file_size_end = (int(r.headers['tivo-estimated-length'])/1024)/1024;
                print('Downloading {} MB...'.format(video_file_size_end));
        else:
                print('HTTP Request sent, awaiting response... ' + str(r.status_code));
                print(r.raise_for_status());
                return;
        with open(fp+'.tivo', 'wb') as fd:
                pbar = ProgressBar(widgets=['Downloading: ', SimpleProgress(), ' MB'], maxval=video_file_size_end).start();
                subProcessChild = None;
                for chunk in r.iter_content(block_size):
                        if not chunk:
                                fd.close();
                                break;
                        video_file_size_start += len(chunk);
                        if video_file_size_start == video_file_size_buffer:
                                child = subprocess.Popen('tivodecode -m ' + mak + ' \"' + fp + '.tivo\" | vlc --file-caching=2048 -');
                                subProcessChild = child.poll();
                        fd.write(chunk);
                        pbar.update((video_file_size_start/1024)/1024);
                        if subProcessChild is not None:
                                fd.close();
                                os.remove(fp);
                                break;
                pbar.finish();
        print('Download complete. Running decode: \"tivodecode -m ' + mak + ' \"' + fp + '.tivo\" | vlc -vvv --file-caching=2048 -');
        child = subprocess.Popen('tivodecode -m ' + mak + ' \"' + fp + '.tivo\" | vlc -vvv --file-caching=2048 -', shell=True);
        return;

def fetchSelection(url, fp):
        playerCommand = 'curl --anyauth --globaloff --user tivo:' + mak + ' --insecure --url \"' + url + '\" | ';
        playerCommand += 'tivodecode -m ' + mak + ' --out ' + fp + '.mpg - | ';
        playerCommand += 'vlc --file-caching=2048 -';
        print('Fetching ' + url + '...');
        subprocess.Popen(playerCommand, stdout=sub.PIPE);


def resumeDownload(url, fp):
        video_file_size_start = chacheSize;
        block_size = 1024;
        video_file_size_current = 0;

        with open(fp, "a") as fd:
                for chunk in r.iter_content(block_size):
                        video_file_size_current += len(chunk);
                        if video_file_size_current >= video_file_size_start:
                                fd.write(chunk);
                fd.close();
        return;

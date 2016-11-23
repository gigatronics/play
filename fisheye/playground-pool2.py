import time
import random
random.seed(1250)
from multiprocessing import Pool, Manager
from collections import deque


def display_stream(stream, pool, queue, buff, buffered=False):
    delay = 24
    popped_frames = 0
    for i, frame in enumerate(stream):
        buff.append([chr(frame), ''])
        time.sleep(1/24 * random.random()) # suppose a 24 fps video
        if i % 6 == 0:                     # suppose one out of 6 frames
            pool.apply_async(process_frame, (i, frame, queue))
        ii, caption = (None, '') if queue.empty() else queue.get()
        if buffered:
            if ii is not None:
                buff[ii - popped_frames][1] = caption
            if i > delay:
                print(buff.popleft())
                popped_frames += 1
        else:
            lag = '' if ii is None else i - ii
            print(chr(frame), caption, lag)

    else:
        pool.close()
        pool.join()
        if buffered:
            try:
                while True:
                    print(buff.popleft())
            except IndexError:
                pass


def process_frame(i, frame, queue):
    time.sleep(0.4 * random.random())      # suppose ~0.2s to process
    caption = chr(frame).upper()           # mocking the result...
    queue.put((i, caption))

if __name__ == '__main__':

    p = Pool()
    q = Manager().Queue()
    d = deque()

    stream = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

    display_stream(stream, p, q, b)

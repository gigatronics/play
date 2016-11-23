import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        sefl.video.release()

    def get_frame(self):
        ret, image = self.video.read()

        # openCV defaults to capture raw.. to work with MotionJPEG, encode it to JPEG to be displayed in video stream
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

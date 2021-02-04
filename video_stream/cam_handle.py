import cv2, imutils
from imutils.video import FPS
import datetime as dt

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, jpeg = cv2.imencode('.jpg', gray)
        # self.fps = dt.time() - self.fps
        return (jpeg.tobytes(), self.fps)
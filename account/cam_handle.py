import cv2, imutils
# from imutils.video import FPS
import datetime as dt
import face_recognition

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        self.ret, self.frame = self.video.read()
        self.frame = cv2.flip(self.frame,1)
        self.frame = imutils.resize(self.frame, width=600)
        self.face_detect()
        # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        # self.fps = dt.time() - self.fps
        return jpeg.tobytes()

    def face_detect(self):
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # print(f'coords: {self.detections[1][0]}|{self.detections[1][1]}|{self.detections[1][2]}|{self.detections[1][3]}')
        # print(f'Confidence: {self.detections[1][4]}')
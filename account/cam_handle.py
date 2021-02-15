import cv2, imutils
# from imutils.video import FPS
import datetime as dt
import face_recognition
import pickle



class VideoCamera(object):
    # show = False
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.loaded_encodings = None
    def __del__(self):
        self.video.release()
    def get_frame(self):
        self.ret, self.frame = self.video.read()
        self.frame = cv2.flip(self.frame,1)
        # self.frame = imutils.resize(self.frame, width=600)
        self.face_detect()
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def face_detect(self):
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        names = []
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)
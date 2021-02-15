import cv2, imutils
# from imutils.video import FPS
import datetime as dt
import face_recognition
import pandas as pd
ENCODINGS_FILE = 'W:\\backup\\prog\\django\\diploma_proj\\media\\encodings\\encodings.pkl'

def handle_encods():
    df = pd.read_pickle(ENCODINGS_FILE)
    res_names = []
    result = []
    for encod in df.encodings:
        result.append(encod)
    for name in df.names:
        res_names.append(name)
    # print(names)
    # print(result)
    return result, res_names

class VideoCamera(object):
    # encodings, names = pd.read_pickle(ENCODINGS_FILE)
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.encodings, self.names = handle_encods()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        self.ret, self.frame = self.video.read()
        self.frame = cv2.flip(self.frame, 1)
        self.frame = imutils.resize(self.frame, width=600)
        self.face_detect()
        # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        # self.fps = dt.time() - self.fps
        return jpeg.tobytes()

    def face_detect(self):
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        boxes = face_recognition.face_locations(rgb_small_frame)
        encods = face_recognition.face_encodings(small_frame, boxes)
        names = []
        for encoding in encods:
            matches = face_recognition.compare_faces(self.encodings, encoding)
            name = 'Unknown'
            if True in matches:
                matchedIds = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIds:
                    name = self.names[i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key = counts.get)
            names.append(name)
        for ((top, right, bottom, left), name) in zip(boxes, names):
        # for (top, right, bottom, left) in boxes:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(self.frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

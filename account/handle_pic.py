import face_recognition as fr
import pickle
import cv2
import os

# os.walk()

def handle_picture(image = None, worker = None):
    # if image:
    loaded_image = cv2.imread(worker.face_pic)
    loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2RGB)
    boxes = fr.face_locations(loaded_image, model='cnn')
    encodings = fr.face_encodings(loaded_image, boxes)
    # worker.face_embeding = encodings
    return encodings

    # elif worker:

# ~5-10 encodings of each person
# loop through all encodings while handling 1 frame
# check if there any matches (True, False)
# If there any, then get the name of encoding and show it => login
# otherwise "login failure"
# for enc in encodings:



class PictureHandler(object):
    pass
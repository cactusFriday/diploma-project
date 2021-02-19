import face_recognition as fr
import cv2
import os
import pandas as pd
from .config import *
from .models import WorkerBiometric


# os.walk()

def sync_encods():
    encodings_list = []
    names_list = []
    worker_bio = WorkerBiometric.objects.all()
    for elem in worker_bio:
        path = str(elem.face_pic)
        name = elem.person.user.first_name
        path = os.path.join(MEDIA_DIR, path)
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print('executing encodings for: ', name)
        boxes = fr.face_locations(img, model='hog')
        encoding = fr.face_encodings(img, boxes)
        if encoding:
            encodings_list.append(encoding[0])
            names_list.append(name)
        print(encodings_list[-1])
        print(names_list[-1])
    data = pd.DataFrame({'encodings': encodings_list, 'names': names_list})
    data.to_pickle(ENCODING_FILE)

def handle_picture(face_pic, username):
    face_pic = os.path.join(IMGS_BASE_DIR, face_pic)
    print('IMAGE_PATH: ', face_pic)
    print('USERNAME: ', username)
    img = cv2.imread(face_pic)
    boxes = fr.face_locations(img, model='hog')
    encoding = fr.face_encodings(img, boxes)
    df = pd.DataFrame({
        'encodings': encoding,
		'names': username
    })
    if os.path.isfile(ENCODING_FILE):
        loaded_df = pd.read_pickle(ENCODING_FILE)
        concat_df = pd.concat([loaded_df, df])
        concat_df.to_pickle(ENCODING_FILE)
    else:
        df.to_pickle(ENCODING_FILE)
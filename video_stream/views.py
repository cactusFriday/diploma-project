from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone
from django.views.decorators import gzip
import cv2
import numpy as np
# import dlib
import face_detection
# from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace
# from face_detection.retinaface import RetinaNetResNet50
from .cam_handle import VideoCamera

def gen(camera):
    while True:
        frame = camera.get_frame()
        # img = np.ndarray(frame)
        # inference_imshape =(480, 640) # Input to the CNN
        # input_imshape = (1080, 1920) # Input for original video source
        # detector = RetinaNetResNet50()
        # boxes, landmarks, scores = detector.detect(image=img)
        # print("Number of faces detected: {}".format(len(dets)))
        # for i, d in enumerate(dets):
        #     print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
        #         i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

        # print(fps)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def cam_capture(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")

def index(request):
    return render(request, 'streaming/index.html')

from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone
from django.views.decorators import gzip
import cv2

from .cam_handle import VideoCamera

def gen(camera):
    while True:
        frame, fps = camera.get_frame()
        # print(fps)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def cam_capture(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")

def index(request):
    return render(request, 'streaming/index.html')

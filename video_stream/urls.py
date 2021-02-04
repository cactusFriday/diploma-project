from django.urls import path
from . import views

app_name = 'video_stream'
urlpatterns = [
    path('', views.index, name= 'index'),
    path('cam_capture', views.cam_capture, name = 'cam_capture'),
]
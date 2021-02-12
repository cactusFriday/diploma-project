from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    # path('', views.index, name= 'index'),
    path('login/', views.user_login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('register_biometric/', views.register_biometric, name = 'register_biometric'),
    # path('login/')
    # path('cam_capture', views.cam_capture, name = 'cam_capture'),
]
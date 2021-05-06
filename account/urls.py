from django.urls import path
from django.conf.urls import url
from django.views.generic import RedirectView
from . import views
# RedirectView.as_view()

app_name = 'account'
urlpatterns = [
    # path('', views.index, name= 'index'),
    path('', RedirectView.as_view(url='login/', permanent=True)),
    path('login/', views.user_login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('register_biometric/', views.register_biometric, name = 'register_biometric'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.UserLogout.as_view(), name = 'logout_page'),
    # path('login/')
    # path('cam_capture', views.cam_capture, name = 'cam_capture'),
]
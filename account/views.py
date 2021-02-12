from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from .forms import LoginForm, UserRegistrationForm
import cv2
import sys
import datetime as dt
from .cam_handle import VideoCamera
from .models import WorkerBiometric

# from sys.path.insert(0, '../video_stream/cam_handle.py') import video_stream.cam_handle
# import video_stream.cam_handle as streaming

def user_login(request):
    print('login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate() checks user data and return user-object if succeed
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    # login() activates user session
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create new user but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save user
            new_user.save()
            string_a = 'register yout biometric'
            string_p = 'Now you can '
            context = {'user_form': user_form, 'string_a': string_a, 'string_p': string_p}
            return render(request, 'account/register.html', context)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

def register_biometric(request):
    if request.method == 'POST':
        cam = VideoCamera()
        img = cam.get_frame()
        cam.__del__()
        # cv2.imwrite('W:/backup/prog/django/imgs/image.jpg', img)
        # print('We are here')
        content = ContentFile(img)
        worker = WorkerBiometric()
        worker.date_stored = dt.datetime.now()
        worker.name = 'First_pic'
        worker.face_pic.save('face.jpg', content)
        worker.save()
        # worker.save()
        msg = 'bio saved'
        context = {"msg": msg}
        return render(request, 'account/register_done.html', {})
    else:
        context = {}
    # print('soooooooo?')
    return render(request, 'account/registrate_biometric.html', context)
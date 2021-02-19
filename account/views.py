from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, WorkerBioEditForm
from .models import WorkerBiometric, Profile
from .cam_handle import VideoCamera
from .handle_pic import handle_picture, sync_encods

import cv2
import time
import sys
import os
import pandas as pd
import datetime as dt
import threading
import face_recognition as fr
from .config import *

# def face_authorise():
#     cam = VideoCamera()
#     while True:
#         # get frames and recognise
#         # if match => return True

# loads all images in image folder, get set(encoding, name) for each image and creates dataframe
# pickle dataframe to encodings.pkl


def save_face_image(request):
    cam = VideoCamera()
    img = cam.get_frame()
    cam.__del__()
    sync_encods()
    user = request.user.profile
    content = ContentFile(img)
    date = dt.datetime.now()
    worker = WorkerBiometric.objects.create(date_stored = date)
    # worker.save(commit=False)
    name = str(request.user.username) + str(worker.pk) + '.jpg'
    # save image(content) with name
    worker.face_pic.save(name, content)
    worker.person = user
    worker.name = str(request.user.username) + str(worker.pk)
    worker.save()
    handle_picture(name, request.user.first_name)
    sync_encods()
    # profile = Profile.objects.get(user = user)
    # print('USER FROM REQUEST: ', request.user, 'USER FROM PROFILE', profile)

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
            username = user_form['username'].value()
            # Set choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save user
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            string_a = 'register yout biometric'
            string_p = 'Now you can '
            context = {'user_form': user_form, 'string_a': string_a, 'string_p': string_p}
            # immediatly login after registration
            user = authenticate(username=username, password=user_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            return render(request, 'account/register.html', context)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

# async def get_register_done(request):
    # msg = 'bio saved'
    # context = {"msg": msg}
    # print('we are about to render HTML')
    # return render(request, 'account/register_done.html', {})
@login_required
def register_biometric(request):
    context = {}
    if request.method == 'POST':
        # create a thread for handling function in parallel flow
        t = threading.Thread(target=save_face_image, args=[request])
        # t.setDaemon(True)
        t.start()
        print('**********************RENDERED**********************')
        return render(request, 'account/register_done.html', {})
    else:
        context = {'msg': 'this is GET'}
    return render(request, 'account/registrate_biometric.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES, )
        worker_form = WorkerBioEditForm(instance=request.user.profile, data = request.POST)
        if user_form.is_valid() and profile_form.is_valid() and worker_form.is_valid():
            user_form.save()
            profile_form.save()
            worker_form.save()
        # TODO: !!!!!!!REDIRECT TO HOME PAGE FOR LOGGED IN USERS (CREATE THIS PAGE)!!!!!!!
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        worker_form = WorkerBioEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'worker_form': worker_form,
        }
    return render(request, 'account/edit.html', context)

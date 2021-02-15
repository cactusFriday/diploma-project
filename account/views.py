from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import WorkerBiometric, Profile
from .cam_handle import VideoCamera

import cv2
import time
import sys
import os
# import pickle
import pandas as pd
import datetime as dt
import asyncio
import face_recognition as fr
from asgiref.sync import sync_to_async
from .config import ENCODINGS_BASE_DIR, ENCODING_FILE, IMGS_BASE_DIR

# def face_authorise():
#     cam = VideoCamera()
#     while True:
#         # get frames and recognise
#         # if match => return True

# @sync_to_async
def handle_picture(face_pic, username):
    face_pic = os.path.join(IMGS_BASE_DIR, face_pic)
    print('IMAGE_PATH: ', face_pic)
    print('USERNAME: ', username)
    # time.sleep(2)
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

@sync_to_async
def save_face_image(request):
    cam = VideoCamera()
    img = cam.get_frame()
    cam.__del__()
    user = request.user.profile
    # print('********************************************')
    # print('USER PROFILE VAR', user)
    # print('********************************************')
    # cv2.imwrite('W:/backup/prog/django/imgs/image.jpg', img)
    # print('We are here')
    content = ContentFile(img)
    date = dt.datetime.now()
    worker = WorkerBiometric.objects.create(date_stored = date)
    # worker.save(commit=False)
    name = str(request.user.username) + str(worker.pk) + '.jpg'
    worker.face_pic.save(name, content)
    worker.person = user
    worker.name = str(request.user.username) + str(worker.pk)
    worker.save()
    # await asyncio.gather(*[handle_picture(worker.face_pic, name)])
    handle_picture(name, request.user.first_name)
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

async def register_biometric(request):
    if request.method == 'POST':
        print('start saving')
        # await save_face_image()
        await asyncio.gather(*[save_face_image(request)])
        msg = 'bio saved'
        context = {"msg": msg}
        print('we are about to render HTML')
        return render(request, 'account/register_done.html', {})
    else:
        context = {}
    # print('soooooooo?')
    return render(request, 'account/registrate_biometric.html', context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        # TODO: !!!!!!!REDIRECT TO HOME PAGE FOR LOGGED IN USERS (CREATE THIS PAGE)!!!!!!!
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/edit.html', context)

# TODO: deal with handling pics from DB and implement face_recognition NN
# TODO: find out what make server stuck (probably async/await functions. Learn how to stop this processes)
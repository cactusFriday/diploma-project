from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, WorkerBioEditForm
from .models import WorkerBiometric, Profile, Transaction
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
from .blockchain.block import Block

# def face_authorise():
#     cam = VideoCamera()
#     while True:
#         # get frames and recognise
#         # if match => return True

# loads all images in image folder, get set(encoding, name) for each image and creates dataframe
# pickle dataframe to encodings.pkl
def create_trans(user):
    temp_trans = Transaction()
    temp_trans.user = user.profile
    temp_trans.date = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    temp_trans.data = f'Entry for user {user.username}'
    # temp_trans.save(commit = False)
    return temp_trans

def check_trans(user):
    '''
    check if transaction from one unique user is more than 5
    '''
    temp_trans = Transaction.objects.all()
    temp = []
    result_s = '['
    for t in temp_trans:
        if t.user.user.username == user.username:
            temp.append(t)
            result_s += t.strformat()
    if len(temp) >= 2:
        print("Create Block")
        d = {
            'index': 1,
            'timestamp': time.strftime('%Y-%m-%d %H:%M'),
            'hash': '',
            'prev_hash': '',
            'nonce': 0,
            'data': str(result_s + ']').strip(),
        }
        block = Block(d)
        block.update_self_hash()
        while not block.is_valid():
            block.nonce += 1
        block.self_save()

        for tr in temp:
            tr.delete()
        # delete all gathered transactions
        del block

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
                    transaction = create_trans(user)
                    transaction.save()
                    check_trans(user)
                    # !!! Create a transaction with (date, data, person)
                    return redirect('workspace:index')
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


@login_required(login_url='account:login')
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


@login_required(login_url='account:login')
def edit(request):
    context = {}
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES, )
        worker_form = WorkerBioEditForm(instance=request.user.profile, data = request.POST)
        if user_form.is_valid() and profile_form.is_valid() and worker_form.is_valid():
            user_form.save()
            profile_form.save()
            worker_form.save()
            print(user_form.data)
            print(user_form)
            render(request, 'workspace/index.html', context)
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

class UserLogout(LogoutView):
    next_page = reverse_lazy('account:login')
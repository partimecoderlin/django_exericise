from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import RoomForm
from . import models

# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except Exception:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User or password does not exists')

    context = {}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q')
    if q is None:
        q = ''
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q)
        | Q(description__icontains=q))
    topics = models.Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = models.Room.objects.get(id=int(pk))
    context = {'room': room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # form=RoomForm(request.post)
    context = {'form': form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    # ???room????????????id???pk?????????
    room = models.Room.objects.get(id=int(pk))
    # ????????????????????????form???????????????
    form = RoomForm(instance=room)
    # ????????????post???????????????view

    if request.user != room.host:
        return HttpResponse('You are note allowed here')

    if request.method == 'POST':
        # ???room???????????????????????????????????????post?????????????????????
        form = RoomForm(request.POST, instance=room)
        # ??????form??????????????????
        if form.is_valid():
            # ??????????????????????????????????????????
            form.save()
            return redirect('home')
    # ??????????????????form??????????????????render
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = models.Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse('You are note allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import RoomForm
from . import models

# Create your views here.


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


def updateRoom(request, pk):
    # 在room表中取得id为pk的数据
    room = models.Room.objects.get(id=int(pk))
    # 用上面的数据生成form供用户输入
    form = RoomForm(instance=room)
    # 当客户端post数据到这个view
    if request.method == 'POST':
        # 用room查找到数据表中的数据，并用post数据更新数据表
        form = RoomForm(request.POST, instance=room)
        # 如果form的数据合法？
        if form.is_valid():
            # 保存数据和重新引导用户会主页
            form.save()
            return redirect('home')
    # 供用户输入的form作为参数传给render
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = models.Room.objects.get(id=int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

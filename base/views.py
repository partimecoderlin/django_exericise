from django.shortcuts import render,redirect
from .forms import RoomForm
from . import models

# Create your views here.


def home(request):
    rooms = models.Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = models.Room.objects.get(id=int(pk))
    context = {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # form=RoomForm(request.post)
    context = {'form': form}

    return render(request, 'base/room_form.html', context)

def updateRoom(request,pk):
    room=models.Room.objects.get(id=int(pk))
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)
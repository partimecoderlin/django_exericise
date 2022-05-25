from django.shortcuts import render

# Create your views here.

dummy_room_data = [
    {
        'id': 1,
        'name': 'python web dev'
    },
    {
        'id': 2,
        'name': 'nodejs web dev'
    },
    {
        'id': 3,
        'name': 'javascripts web dev'
    },
]


def home(request):
    context = {'rooms': dummy_room_data}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = None
    for i in dummy_room_data:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)

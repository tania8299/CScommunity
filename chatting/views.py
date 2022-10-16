from tkinter.messagebox import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message, Room 
# Create your views here.

def front(request):
    return render(request, 'core.html')
@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
   room = Room.objects.get(slug=slug)
   messages = Message.objects.filter(room=room)[0:25]
   return render(request, 'room.html', {'room': room, 'messages': messages})



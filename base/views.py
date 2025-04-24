from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from .forms import RoomForm
# Create your views here.


def login_view(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login')  # redirect back to the login page
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          return redirect('home')
        else: 
          messages.error(request, 'User OR Password does not exist')
    return render(request, 'base/login_form.html')



def home(request): 
  q = request.GET.get('q') or ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q) 
    ).order_by('-last_updated', '-created_at')
  topics = Topic.objects.all()
  room_count = rooms.count()
  context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
  return render(request, 'base/home.html', context)



def room(request, pk): 
  room = Room.objects.get(id=pk)
  context={'room':room}
  return render(request, 'base/room.html', context)



def create_room(request): 
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/room-form.html', context)



def update_room(request, pk): 
  room = Room.objects.get(id = pk)
  form = RoomForm(instance=room)
  
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  context={'form': form}
  return render(request, 'base/room-form.html', context)



def delete_room(request, pk):
  room = Room.objects.get(id = pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': room})
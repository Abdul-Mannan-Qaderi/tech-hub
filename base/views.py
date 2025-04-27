from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm
# Create your views here.


def login_view(request):   
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == 'POST':
      username = request.POST.get('username').lower()
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
  context = {'page':page}
  return render(request, 'base/login_register.html', context)

def register_view(request):
  form = UserCreationForm
  
  if request.method=='POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else: 
      messages.error(request, 'Something went wrong with Signing up!')   
  context = {'form':form}
  return render(request, 'base/login_register.html', context)

def logout_view(request):
  logout(request)
  return redirect('login')

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
  room_messages = room.message_set.all().order_by('-created_at')
  
  if request.method == 'POST':
    message = Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    return redirect('room', pk=room.id)
  context={'room':room, 'room_messages':room_messages}
  return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def create_room(request): 
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/room-form.html', context)

@login_required(login_url='/login')
def update_room(request, pk): 
  room = Room.objects.get(id = pk)
  form = RoomForm(instance=room)
  
  if request.user != room.host:
    return HttpResponse('You can only edit your own posts')
  
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  context={'form': form}
  return render(request, 'base/room-form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
  room = Room.objects.get(id = pk)
  
  if request.user != room.host:
    return HttpResponse('You can only delete your own posts')
  
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': room})
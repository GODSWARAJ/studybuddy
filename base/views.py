from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username = username, password = password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')    
    return render(request, 'base/login_register.html', {'page':page})

def logoutpage(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error during register')
    return render(request, 'base/login_register.html', {'form' : form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
    Q(topic__name__icontains = q) |
    Q(name__icontains = q) |
    Q(description__icontains = q)
    )
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    topics = Topic.objects.all()[:5]
    return render(request, 'base/home.html', {'rooms': rooms, 'topics':topics, 'rooms_count':rooms_count, 'room_messages':room_messages}) 

def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}    
    return render(request, 'base/room.html', context)

@login_required(login_url = 'login') 
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    return render(request, 'base/room_form.html', {'form' : form, 'topics':topics})

@login_required(login_url = 'login') 
def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if request.user != room.host:
        HttpResponse('You are not allow to update')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('name')
        room.save()
        return redirect('home')
    return render(request, 'base/room_form.html', {'form':form, 'topics':topics, 'room':room})

@login_required(login_url = 'login') 
def deleteroom(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        HttpResponse('You are not allow to delete')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url = 'login') 
def deletemessage(request, pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('You are not allow to delete')
    if request.method == 'POST':    
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

def userprofile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':messages, 'topics' : topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login') 
def updateuser(request):
    form = UserForm(instance = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance = request.user)
        form.save()
        return redirect('userprofile', pk = request.user.id)
        
    return render(request, 'base/update-user.html', {'form' : form})

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html', {'topics':topics})

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html', {'topics':topics})

def activitypage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})
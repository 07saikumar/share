from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Room, Message
from .forms import RoomForm, PublicMessageForm, RoomMessageForm
from django.http import JsonResponse
from django.db.models import F, Count
from django.utils.html import urlize
from django.utils.safestring import mark_safe
from .templatetags.custom_filters import urlize_newtab

def landing_page(request):
    return render(request, 'content/landing_page.html')

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            # Delete duplicate room names
            Room.objects.filter(room_name=room_name).delete()
            room = form.save(commit=False)
            room.expiry_time = timedelta(seconds=int(form.cleaned_data['expiry_time']))
            room.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomForm()
    return render(request, 'content/create_room.html', {'form': form})




def public_section(request):
    if request.method == 'POST':
        form = PublicMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.expiry_time = timedelta(seconds=int(form.cleaned_data['expiry_time']))
            message.save()
            return redirect('public_section')
    else:
        form = PublicMessageForm()
    messages = Message.objects.filter(room__isnull=True, creation_time__gte=timezone.now() - F('expiry_time'))
    return render(request, 'content/public_section.html', {'form': form, 'messages': messages})



def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if room.is_expired():
        return redirect('landing_page')
    if request.method == 'POST':
        form = RoomMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.expiry_time = timedelta(seconds=int(form.cleaned_data['expiry_time']))
            message.save()
    else:
        form = RoomMessageForm()
    messages = room.messages.filter(creation_time__gte=timezone.now() - F('expiry_time'))
    return render(request, 'content/room_detail.html', {'room': room, 'messages': messages, 'form': form})


def access_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        password = request.POST.get('password')
        room = get_object_or_404(Room, id=room_id, password=password)
        if room.is_expired():
            return redirect('landing_page')
        return redirect('room_detail', room_id=room.id)
    else:
        now = timezone.now()
        rooms = Room.objects.filter(creation_time__gte=now - F('expiry_time')).values('room_name', 'id')
        return render(request, 'content/access_room.html', {'rooms': rooms})

#fetching

def fetch_public_messages(request):
    messages = Message.objects.filter(room__isnull=True, creation_time__gte=timezone.now() - F('expiry_time'))
    messages_data = [
        {
            'content': urlize_newtab(message.content),
            'image': message.image.url if message.image else ''
        }
        for message in messages
    ]
    return JsonResponse({'messages': messages_data})

def fetch_messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.filter(creation_time__gte=timezone.now() - F('expiry_time'))
    messages_data = [
        {
            'content': urlize_newtab(message.content),
            'image': message.image.url if message.image else ''
        }
        for message in messages
    ]
    return JsonResponse({'messages': messages_data})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Hotel, Room
from .forms import RegisterForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking
from .models import Room

# Create your views here.

template_name = 'booking/register.html', 'booking/hotel_list.html', 
'booking/room_list.html', 
'payments/payment_process.html', 'Booking/booking_form.html', 'registration/login.html' 
paginate_by = 10

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel_list')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'booking/hotel_list.html', {'hotels': hotels})

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.room_set.filter(is_available=True)
    return render(request, 'booking/room_list.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.amount = booking.total_price()
            booking.save()
            room.is_available = False
            room.save()
            return redirect('hotel_list')
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'room': room, 'form': form})


def payment_process(request, booking_id):
    return render(request, 'payments/payment_process.html', {'booking_id': booking_id})



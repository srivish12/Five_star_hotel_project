from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Hotel, Room

# Create your views here.

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'booking/hotel_list.html', {'hotels': hotels})

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.room_set.filter(is_available=True)
    return render(request, 'booking/room_list.html', {'hotel': hotel, 'rooms': rooms})

def payment_process(request, booking_id):
    return render(request, 'payments/payment_process.html', {'booking_id': booking_id})

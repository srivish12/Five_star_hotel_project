from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Hotel, Room, Booking
from .forms import RegisterForm, BookingForm
from django.utils.dateparse import parse_date
 


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('hotel_list')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'booking/hotel_list.html', {'hotels': hotels})


def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'booking/room_list.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def admin_book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)

        if not check_in_date or not check_out_date:
            messages.error(request, "Please provide valid check-in and check-out dates.")
            return redirect('room_list', hotel_id=room.hotel.id)

        if check_in_date >= check_out_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('room_list', hotel_id=room.hotel.id)

        
        overlap_exists = Booking.objects.filter(
            room=room,
            is_active=True,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        ).exists()

        if overlap_exists:
            messages.error(request, "Sorry, this room is already booked for the selected dates.")
            return redirect('room_list', hotel_id=room.hotel.id)

       
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user 
            booking.room = room
            booking.amount = booking.total_price()
            booking.save()
            room.is_available = False
            room.save()

            return redirect('payment_process', booking_id=booking.id)
        
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {'room': room, 'form': form})


@user_passes_test(lambda u: u.is_staff)
def admin_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.is_active = False
    booking.room.is_canceled = True
    booking.room.is_available = True
    booking.room.save()
    booking.save()
    messages.success(request, "Booking has been cancelled by admin.")
    return redirect('booking/room_list', hotel_id=booking.room.hotel.id)

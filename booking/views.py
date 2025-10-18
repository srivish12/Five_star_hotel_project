from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Hotel, Room, Booking
from .forms import RegisterForm, BookingForm


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
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if not room.is_available:
        messages.error(request, "Sorry, this room is already booked.")
        return redirect('room_list', hotel_id=room.hotel.id)

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
            messages.success(request, 'Room booked successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'room': room, 'form': form})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if booking.is_active:
        booking.is_active = False
        booking.save()

        booking.room.is_available = True
        booking.room.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "This booking is already cancelled.")
    return redirect('room_list', hotel_id=booking.room.hotel.id)


@user_passes_test(lambda u: u.is_staff)
def admin_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.is_active = False
    booking.room.is_available = True
    booking.room.save()
    booking.save()
    messages.success(request, "Booking has been cancelled by admin.")
    return redirect('hotel_list')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

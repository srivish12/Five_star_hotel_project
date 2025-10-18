from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Booking
from django.utils.dateparse import parse_date


# Create your views here.

@login_required
@login_required
def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        # parse dates (expects YYYY-MM-DD)
        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)

        if not check_in_date or not check_out_date:
            messages.error(request, "Please provide valid check-in and check-out dates.")
        elif check_in_date >= check_out_date:
            messages.error(request, "Check-out date must be after check-in date.")
        else:
            # Prevent overlapping bookings
            if Booking.objects.filter(room=room, is_active=True, check_in__lt=check_out_date, check_out__gt=check_in_date).exists():
                messages.error(request, "Room is already booked for the selected dates.")
            else:
                Booking.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in_date,
                    check_out=check_out_date
                )
                # mark room unavailable while booked
                room.is_available = False
                room.save()
                messages.success(request, f"Room {room.number} reserved successfully!")
                return redirect("my_bookings")

    return render(request, "reservations/reserve_room.html", {"room": room})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, is_active=True)

    if request.method == "POST":
        booking.is_active = False
        booking.room.is_available = True
        booking.room.save()
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("my_bookings")

    return render(request, "reservations/cancel_booking.html", {"booking": booking})

@login_required
def amend_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, is_active=True)

    if request.method == "POST":
        new_check_in = request.POST.get("check_in")
        new_check_out = request.POST.get("check_out")

        # parse and validate new dates
        new_check_in_date = parse_date(new_check_in)
        new_check_out_date = parse_date(new_check_out)

        if not new_check_in_date or not new_check_out_date:
            messages.error(request, "Please provide valid check-in and check-out dates.")
        elif new_check_in_date >= new_check_out_date:
            messages.error(request, "Check-out date must be after check-in date.")
        else:
            # Prevent overlaps with other bookings (exclude current booking)
            if Booking.objects.filter(room=booking.room, is_active=True, check_in__lt=new_check_out_date, check_out__gt=new_check_in_date).exclude(id=booking.id).exists():
                messages.error(request, "Room is not available for these new dates.")
            else:
                booking.check_in = new_check_in_date
                booking.check_out = new_check_out_date
                booking.save()
                messages.success(request, "Booking updated successfully.")
                return redirect("my_bookings")

    return render(request, "reservations/amend_booking.html", {"booking": booking})
    #return render(request, "reservations/amend_booking.html", {"booking": booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "reservations/my_bookings.html", {"bookings": bookings})

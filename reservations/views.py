from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Booking
from django.utils.dateparse import parse_date
from booking.models import Booking


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, user=request.user, is_active=True
        )

    if request.method == 'POST':
        booking.is_active = False
        booking.save()

        if not Booking.objects.filter(
            room=booking.room,
            is_active=True
        ).exists():
            booking.room.is_available = True
            booking.room.save()
        
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')

    return render(
        request, 'reservations/cancel_booking.html', {'booking': booking}
        )


@login_required
def amend_booking(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, user=request.user, is_active=True
        )

    if request.method == 'POST':
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)

        if not check_in_date or not check_out_date:
            messages.error(
                request, "Please provide valid check-in and check-out dates."
               )
        elif check_in_date >= check_out_date:
            messages.error(
                request, "Check-out date must be after check-in date."
                )
        else:
            if Booking.objects.filter(
                room=booking.room,
                is_active=True,
                check_in__lt=check_out_date,
                check_out__gt=check_in_date
            ).exclude(id=booking.id).exists():
                messages.error(
                    request, "Room is already booked for the selected dates."
                    )
            else:
                booking.check_in = check_in_date
                booking.check_out = check_out_date
                booking.save()
                messages.success(request, 'Booking amended successfully.')
                return redirect('my_bookings')

    return render(
        request, 'reservations/amend_booking.html', {'booking': booking}
        )


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user, is_active=True)
        .select_related('room').order_by('-check_in')
        )
    return render(
        request, 'reservations/my_bookings.html', {'bookings': bookings}
    )
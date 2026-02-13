from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booking.models import Booking, Room
from .models import Payment
from .forms import PaymentForm
import uuid


@login_required
def payment_process(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    payment = getattr(booking, 'payment', None)
    if payment and payment.status == 'completed':
        messages.info(request, "Payment already completed for this booking.")
        return redirect('payment_success', booking_id=booking.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.user = request.user
            payment.amount = booking.amount
            payment.notes = request.POST.get('notes')
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
            booking.notes = payment.notes
            booking.payment_id = payment.transaction_id

            if payment.method in ['card', 'paypal', 'mobile']:
                payment.status = 'completed'
                booking.payment_status = 'completed'

            elif payment.method in ['cash', 'other']:
                payment.status = 'pending'
                booking.payment_status = 'pending'
            else:
                payment.status = 'pending'

            payment.save()
            booking.save()
            messages.success(
                request, "Room is reserved for the selected dates."
                )
            return redirect('payment_success', booking_id=booking.id)
    else:
        form = PaymentForm(initial={'amount': booking.amount})

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'booking': booking,
        'room': booking.room,
    })


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(
        request, 'payments/payment_success.html', {'booking': booking}
        )


@login_required
def payment_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    messages.warning(request, "Payment was cancelled.")
    return render(
        request, 'payments/payment_cancel.html', {'booking': booking}
    )

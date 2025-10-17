from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booking.models import Booking
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
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"

           
            if payment.method in ['card', 'cash', 'paypal', 'mobile']:
                payment.status = 'completed'
                booking.payment_status = 'Completed'
            else:
                payment.status = 'pending'

            payment.save()
            booking.save()
            messages.success(request, "Payment processed successfully!")
            return redirect('payment_success', booking_id=booking.id)
    else:
        form = PaymentForm(initial={'amount': booking.amount})

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'booking': booking
    })


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'payments/payment_success.html', {'booking': booking})


@login_required
def payment_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    messages.warning(request, "Payment was cancelled.")
    return render(request, 'payments/payment_cancel.html', {'booking': booking})


@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
    return render(request, 'payments/payment_history.html', {'payments': payments})


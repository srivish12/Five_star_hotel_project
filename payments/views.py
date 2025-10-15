from django.shortcuts import render
from django.http import HttpResponse

def payment_process(request, booking_id):
    return HttpResponse(f"Process payment for booking {booking_id}")


def payment_success(request, booking_id):
    return HttpResponse(f"Payment successful for booking {booking_id}")


def payment_cancel(request, booking_id):
    return HttpResponse(f"Cancel payment for booking {booking_id}")


def payment_history(request):
    return HttpResponse("Payment history page")
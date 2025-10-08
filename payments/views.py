from django.shortcuts import render
from django.http import HttpResponse

def payment_process(request, booking_id):
    return HttpResponse(f"Process payment for booking {booking_id}")
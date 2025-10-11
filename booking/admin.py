from django.contrib import admin
from .models import  Room, Hotel, Booking, payment_process

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(payment_process)
# Register your models here.

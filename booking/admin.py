from django.contrib import admin
from .models import  Room, Hotel, Booking
#from payments.models import Payment

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
#admin.site.register(Payment)


# Register your models here.

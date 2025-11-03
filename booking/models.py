from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('family', 'Family'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
                              related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return ( 
            f"{self.hotel.name} - "
            f"Room {self.room_number}  ({self.room_type})"
         )


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, default='Pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        status = "Active" if self.is_active else "Cancelled"
        return f"Booking by {self.user.username} for {self.room} ({status})"

    def total_price(self):
        days = (self.check_out - self.check_in).days
        return Decimal(days) * self.room.price_per_night

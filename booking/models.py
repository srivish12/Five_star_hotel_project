from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here.
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
        ('Family', 'Family'),
    ]
    hotel = models. ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number =models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room{self.room_number} ({self.room_type}) "
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)  #True if canelled
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')  #Pending, Completed, Failed
    payment_id = models.CharField(max_length=100, blank=True, null=True)  #ID from payment gateway

    def total_price(self):
            days = (self.check_out - self.check_in).days
            return days * self.room.price_per_night
    
    def cancelle(self):
            self.is_cancelled = True
            self.room.is_available = True
            self.room.save()
            self.save()



    def __str__(self):
            return f"Booking by {self.user.username} for {self.room} from {self.check_in} to {self.check_out}"

from django.db import models
from django.conf import settings
from booking.models import Booking
from django.utils import timezone


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('mobile', 'Mobile Money'),
        ('other', 'Other'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment'
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default='pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"{self.booking.user.username} - "
            f"{self.get_method_display()} - {self.status}"
            )

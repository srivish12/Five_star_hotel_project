# payments/admin.py
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'method', 'amount', 'status', 'payment_date')
    list_filter = ('method', 'status')
    search_fields = ('booking__id', 'transaction_id', 'user__username')

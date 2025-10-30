from django.urls import path
from . import views

urlpatterns = [
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('amend/<int:booking_id>/', views.amend_booking, name='amend_booking'), 
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]

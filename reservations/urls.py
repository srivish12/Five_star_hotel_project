from django.urls import path
from . import views

urlpatterns = [
    path("reserve/<int:room_id>/", views.reserve_room, name="reserve_room"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("amend/<int:booking_id>/", views.amend_booking, name="amend_booking"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
]

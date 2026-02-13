from django.urls import path, include
from . import views
from booking import views as booking_views


urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.room_list, name='room_list'),
    path('room/<int:room_id>/', views.admin_book_room, name='admin_book_room'),
    path(
        'admin/cancel/<int:booking_id>/',
        views.admin_cancel_booking, name='admin_cancel_booking'
        ),
    path('register/', booking_views.register, name='register'),
    path('reservations/', include('reservations.urls')),
    path('payments/', include('payments.urls')),
]

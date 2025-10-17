from django.urls import path, include
from . import views

urlpatterns = [
       
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.room_list, name='room_list'),
    path('room/<int:room_id>/book/', views.book_room, name='book_room'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin/cancel/<int:booking_id>/', views.admin_cancel_booking, name='admin_cancel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    
    path('register/', views.register, name='register'),
    path('payment/<int:booking_id>/', views.payment_process, name='payment_process'),
    path('accounts/', include('django.contrib.auth.urls')),  # LOGIN/LOGOUT
]
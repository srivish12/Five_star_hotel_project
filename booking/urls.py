from django.urls import path, include
from . import views

urlpatterns = [
   
    
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.room_list, name='room_list'),
    path('room/<int:room_id>/book/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.payment_process, name='payment_process'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # LOGIN/LOGOUT
]
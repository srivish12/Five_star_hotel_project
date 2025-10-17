from django.urls import path
from . import views

urlpatterns = [
    path('<int:booking_id>/', views.payment_process, name='payment_process'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel/<int:booking_id>/', views.payment_cancel, name='payment_cancel'),
    #path('history/', views.payment_history, name='payment_history'),
]

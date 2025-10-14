from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking
from django.utils import timezone

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }



def accurate_booking(self):
        accurate_data = super().accurate()
        check_in = accurate_data.get('check_in')
        check_out = accurate_data.get('check_out')

        if check_in and check_out:
            if check_in < timezone.now().date():
                self.add_error('check_in', 'Check-in date cannot be in the past.')
            if check_out <= check_in:
                self.add_error('check_out', 'Check-out date must be after check-in date.')
        return accurate_data
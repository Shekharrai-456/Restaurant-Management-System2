from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['quantity', 'ticket_type']  # No input fields needed; booking is auto-filled from view

from django import forms
from .models import Payment

class DummyPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']

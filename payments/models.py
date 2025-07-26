

# Create your models here.
from django.db import models
from bookings.models import Booking

PAYMENT_METHODS = [
    ('dummy', 'Dummy'),
    ('esewa', 'eSewa'),
    ('khalti', 'Khalti'),
]

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='dummy')
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.ticket_id} - {'Success' if self.success else 'Failed'}"

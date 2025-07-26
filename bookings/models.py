

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
import uuid

User = get_user_model()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_paid = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.ticket_id}"

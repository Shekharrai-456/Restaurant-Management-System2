

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']  # one review per user per event

    def __str__(self):
        return f"{self.user.username} review on {self.event.title}"


# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORY_CHOICES = [
    ('music', 'Music'),
    ('tech', 'Tech'),
    ('conference', 'Conference'),
    ('art', 'Art'),
    ('sports', 'Sports'),
]

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

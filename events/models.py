from django.db import models
from django.contrib.auth import get_user_model
from datetime import time


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
    
    date = models.DateField()  # Split date
    time = models.TimeField()  # Split time
    
    location = models.CharField(max_length=200)  # Renamed from venue
    
    price_normal = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00,
        help_text="Normal ticket price"
    )
    price_vip = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00,
        help_text="VIP ticket price"
    )
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    dark_mode_enabled = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=True)

    def __str__(self):
        return self.username

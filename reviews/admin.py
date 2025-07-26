

# Register your models here.
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'reviewed_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('rating', 'reviewed_at')

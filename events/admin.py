
# Register your models here.
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'venue', 'organizer', 'is_approved')
    list_filter = ('category', 'is_approved', 'date')
    search_fields = ('title', 'description', 'venue')
    list_editable = ('is_approved',)

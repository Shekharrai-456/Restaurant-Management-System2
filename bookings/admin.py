

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_id', 'is_paid', 'booked_at')
    list_filter = ('is_paid', 'booked_at')
    search_fields = ('user__username', 'event__title', 'ticket_id')




# Register your models here.
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'method', 'success', 'timestamp')
    list_filter = ('method', 'success')
    search_fields = ('booking__ticket_id',)

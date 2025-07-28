

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'dark_mode_enabled')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'dark_mode_enabled')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'dark_mode_enabled')}),
    )


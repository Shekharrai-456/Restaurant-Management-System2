from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('events/', views.api_event_list, name='api_event_list'),
    path('bookings/user/<int:user_id>/', views.api_user_bookings, name='api_user_bookings'),
    path('bookings/create/', views.api_create_booking, name='api_create_booking'),
    path('auth/register/', views.api_register_user, name='api_register'),
    path('auth/login/', views.api_login_user, name='api_login'),
]

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('download/<int:booking_id>/', views.download_ticket, name='download_ticket'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('process/', views.process_payment, name='process_payment'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    # Payment flow
    path('payment/<int:booking_id>/', views.payment_choice, name='payment_choice'),
    path('payment/dummy/<int:booking_id>/', views.dummy_payment, name='dummy_payment'),
]

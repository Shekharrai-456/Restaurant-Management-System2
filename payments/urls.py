from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('choice/<int:booking_id>/', views.payment_choice, name='payment_choice'),
    path('dummy/<int:booking_id>/', views.dummy_payment, name='dummy_payment'),
    path('ticket/<int:booking_id>/', views.generate_ticket_pdf, name='generate_ticket_pdf'),
    path('process/', views.process_payment, name='process_payment'),  # <-- this
]

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('approval/', views.event_approval, name='event_approval'),
    path('approve/<int:pk>/', views.approve_event, name='approve_event'),
]

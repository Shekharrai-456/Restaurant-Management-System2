from django.urls import path
from reviews.views import submit_review
from . import views


urlpatterns = [
    # path('submit/<int:event_id>/', views.submit_review, name='submit_review'),
    
    path('<int:event_id>/', submit_review, name='submit_review'),
]

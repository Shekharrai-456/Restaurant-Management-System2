from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from events.models import Event
from bookings.models import Booking

@login_required
def submit_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user booked the event
    user_has_booking = Booking.objects.filter(event=event, user=request.user).exists()
    if not user_has_booking:
        messages.error(request, "You must book or attend the event to leave a review.")
        return redirect('events:event_detail', pk=event_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('events:event_detail', pk=event_id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'event': event,
    })

@login_required
def review_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    # Prevent duplicate reviews
    if Review.objects.filter(user=request.user, event=event).exists():
        return redirect('events:event_detail', pk=event_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            return redirect('events:event_detail', pk=event_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {'form': form, 'event': event})

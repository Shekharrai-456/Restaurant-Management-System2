from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm
from reviews.models import Review
from reviews.forms import ReviewForm
from bookings.models import Booking

def event_list(request):
    events = Event.objects.filter(is_approved=True).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_approved=True)
    user = request.user

    # Check if the user has booked the event
    has_booking = Booking.objects.filter(event=event, user=user).exists()

    # Handle review form submission
    if request.method == 'POST' and has_booking:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.event = event
            review.save()
            messages.success(request, 'Your review has been submitted for admin approval.')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = ReviewForm()

    # Get latest 5 reviews
    reviews = Review.objects.filter(event=event).order_by('-reviewed_at')[:5]

    context = {
        'event': event,
        'form': form if has_booking else None,
        'reviews': reviews,
        'has_booking': has_booking,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def event_approval(request):
    events = Event.objects.filter(is_approved=False)
    return render(request, 'events/event_approval.html', {'events': events})

@staff_member_required
def approve_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.is_approved = True
    event.save()
    return redirect('events:event_approval')

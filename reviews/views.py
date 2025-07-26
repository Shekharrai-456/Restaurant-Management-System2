
# Create your views here.
# reviews/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from events.models import Event
from django.contrib.auth.decorators import login_required

@login_required
def submit_review(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            return redirect('events:event_detail', pk=event_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form, 'event': event})

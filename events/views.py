
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def event_list(request):
    events = Event.objects.filter(is_approved=True).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_approved=True)
    return render(request, 'events/event_detail.html', {'event': event})

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

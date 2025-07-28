from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # pip install xhtml2pdf

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, is_approved=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            return redirect('bookings:payment_choice', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'event': event})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, is_paid=True)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def payment_choice(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, is_paid=False)
    return render(request, 'bookings/payment_choice.html', {'booking': booking})

@login_required
def dummy_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, is_paid=False)
    booking.is_paid = True
    booking.save()
    return redirect('bookings:booking_success', booking_id=booking.id)

@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.all().order_by('-booked_at')
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

# Your new booking_detail view
@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, is_paid=True)
    template_path = 'payments/ticket_pdf_template.html'
    context = {'booking': booking}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors generating your ticket')
    return response

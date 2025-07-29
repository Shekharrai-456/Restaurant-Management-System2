from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # pip install xhtml2pdf
from django import forms
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event

            # Fetch ticket type and quantity from the form
            ticket_type = request.POST.get('ticket_type')
            quantity = int(request.POST.get('quantity', 1))

            if ticket_type == 'vip':
                price_per_ticket = event.price_vip
            else:
                price_per_ticket = event.price_normal

            total_price = price_per_ticket * quantity

            booking.ticket_type = ticket_type
            booking.quantity = quantity
            booking.price = total_price
            booking.save()

            # ✅ Redirect to payment choice with booking id
            return redirect('payments:payment_choice', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/book_event.html', {'form': form, 'event': event})

# @login_required
# def book_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         ticket_type = request.POST.get('ticket_type')
#         quantity_str = request.POST.get('quantity')

#         # Validate ticket_type
#         if ticket_type not in ('normal', 'vip'):
#             form.add_error(None, "Please select a valid ticket type.")

#         # Validate quantity
#         try:
#             quantity = int(quantity_str)
#             if quantity < 1:
#                 form.add_error(None, "Quantity must be at least 1.")
#         except (TypeError, ValueError):
#             form.add_error(None, "Please enter a valid quantity.")

#         # Proceed only if form is valid and no custom errors added
#         if form.is_valid() and not form.errors:
#             booking = form.save(commit=False)
#             booking.event = event
#             booking.user = request.user
#             booking.ticket_type = ticket_type
#             booking.quantity = quantity

#             # Set price based on ticket_type
#             if ticket_type == 'normal':
#                 booking.price = event.price_normal
#             elif ticket_type == 'vip':
#                 booking.price = event.price_vip

#             booking.total_price = booking.price * quantity
#             booking.save()

#             # Redirect to payment choice page after successful booking
#             return redirect('payments:payment_choice', booking_id=booking.id)
#     else:
#         form = BookingForm()

#     return render(request, 'bookings/book_event.html', {
#         'form': form,
#         'event': event
#     })


# def book_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.event = event
#             booking.user = request.user
#             booking.ticket_type = request.POST.get('ticket_type')
#             booking.quantity = int(request.POST.get('quantity'))
            

#             # Calculate price
#             if booking.ticket_type == 'normal':
#                 booking.price = event.price_normal
#             elif booking.ticket_type == 'vip':
#                 booking.price = event.price_vip

#             booking.total_price = booking.price * booking.quantity
#             booking.save()

#             # Redirect to payment choice page
#             return redirect('payments:payment_choice', booking_id=booking.id)

#     else:
#         form = BookingForm()

#     return render(request, 'bookings/book_event.html', {
#         'form': form,
#         'event': event
#     })

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
    booking = get_object_or_404(Booking, pk=pk)
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

@login_required
def process_payment(request):
    # Placeholder logic for actual payment processing (e.g., integrating with Stripe, etc.)
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        # Simulate payment success
        booking.is_paid = True
        booking.save()

        return redirect('bookings:booking_success', booking_id=booking.id)

    return redirect('core:home')  # Fallback or error handling

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this booking.")
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('bookings:my_bookings')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/edit_booking.html', {'form': form, 'booking': booking})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this booking.")
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
        return redirect('bookings:my_bookings')
    
    return render(request, 'bookings/delete_booking_confirm.html', {'booking': booking})
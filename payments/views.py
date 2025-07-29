from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Booking
from .models import Payment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def payment_choice(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'payments/payment_choice.html', {'booking': booking})

@login_required
def dummy_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        Payment.objects.create(booking=booking, method='dummy', success=True)
        booking.is_paid = True
        booking.save()
        return redirect('bookings:booking_success', booking_id=booking.id)
    return render(request, 'bookings/payment_dummy.html', {'booking': booking})

@login_required
def generate_ticket_pdf(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    template_path = 'payments/ticket_pdf_template.html'
    context = {'booking': booking}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.ticket_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response

@login_required
def process_payment(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        payment_method = request.POST.get('payment_method')
        booking = get_object_or_404(Booking, pk=booking_id, user=request.user, is_paid=False)

        # Here, you would implement actual payment gateway logic.
        # For now, we simulate successful payment:
        Payment.objects.create(booking=booking, method=payment_method, success=True)
        booking.is_paid = True
        booking.save()

        return redirect('bookings:booking_success', booking_id=booking.id)
    else:
        return redirect('core:dashboard')  # or any fallback page


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
# Create your views here.

def homepage(request):
    return render(request, 'core/homepage.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def dashboard(request):
    return render(request, 'core/homepage.html')


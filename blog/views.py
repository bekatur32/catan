from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
from django.utils.translation import get_language

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email with language-aware subject
            send_mail(
                subject=f'Contact Form: {subject} [{get_language().upper()}]',
                message=f'Name: {name}\nEmail: {email}\nMessage: {message}\nLanguage: {get_language()}',
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, _('Thank you! Your message has been sent.'))
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})

def blog(request):
    return render(request,'index.html')

def about(request):
    return render(request,'blog/about.html')

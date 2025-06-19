from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Enter your name')}),
        required=True
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'placeholder': _('example@domain.com')}),
        required=True
    )
    subject = forms.CharField(
        label=_('Subject'),
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': _('Enter subject')}),
        required=True
    )
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={'placeholder': _('Enter your message'), 'rows': 5}),
        required=True
    )

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha', '').lower()
        expected_captcha = 'abc123'  # Replace with dynamic CAPTCHA logic or reCAPTCHA
        if captcha != expected_captcha:
            raise forms.ValidationError(_('Invalid CAPTCHA. Please try again.'))
        return captcha
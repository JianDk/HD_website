from django import forms
from django.utils.safestring import mark_safe

class contactForm(forms.Form):
    senderName = forms.CharField(label='Your name', max_length=20, required=True)
    senderEmail = forms.EmailField(label= 'Your email')
    senderPhone = forms.CharField(label = 'Phone', required=False, max_length=20)
    senderMessage = forms.CharField(label = 'Message', widget=forms.Textarea)
    ccSender = forms.BooleanField(label = 'cc myself', required=False)

class newsLetterForm(forms.Form):
    signUpEmail = forms.EmailField(label='Newsletter email signup')
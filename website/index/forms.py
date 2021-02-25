from django import forms
from django.utils.safestring import mark_safe

class contactForm(forms.Form):
    senderName = forms.CharField(label='Your name', max_length=50)
    senderEmail = forms.EmailField(label= 'Your email')
    senderPhone = forms.CharField(label = 'Phone', max_length=20, required=False)
    senderMessage = forms.CharField(label = 'Message', widget=forms.Textarea)
    ccSender = forms.BooleanField(label = 'cc myself', required=False)

class newsLetterForm(forms.Form):
    signUpEmail = forms.EmailField(label='Newsletter email signup')
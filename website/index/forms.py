from django import forms
from django.utils.safestring import mark_safe

class contactForm(forms.Form):
    yourName = forms.CharField(label='Your name', max_length=50)
    sender = forms.EmailField(label= 'Your email')
    phone = forms.CharField(label = 'Phone', max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)
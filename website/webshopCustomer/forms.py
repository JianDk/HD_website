from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def phoneNumberValidation(value):
    print('here is the value')
    print(value)
    if len(value) <= 7:
        print('we are here')
        raise ValidationError(_("The phone number must be 8 digits"))
    return value

class customerLocalDeliveryForm(forms.Form):

    customerName = forms.CharField(label = 'Name', max_length=50, required=True)
    customerEmail = forms.EmailField(label = 'Email', max_length=50, required=True)
    
    customerMobile = forms.CharField(label = 'Mobile', max_length = 20,
    required = True) 

    comments = forms.CharField(label = 'Comments', max_length = 300, widget=forms.Textarea, required = False)
    deliveryTime = forms.ChoiceField(choices = (), required=True)

    def __init__(self, *args, **kwargs):
        self.deliveryTimeList = kwargs.pop('deliveryTimeList')
        super().__init__(*args, **kwargs)
        self.fields['deliveryTime'].choices = self.deliveryTimeList

class customerPickupForm(forms.Form):
    customerName = forms.CharField(label = 'Name', max_length=50, required=True)
    comments = forms.CharField(label = 'Comments', max_length = 300, widget=forms.Textarea, required = False)
    pickupTime = forms.ChoiceField(choices = (), required=True)

    def __init__(self, *args, **kwargs):
        self.pickupTimeList = kwargs.pop('pickupTimeList')
        super().__init__(*args, **kwargs)
        self.fields['pickupTime'].choices = self.pickupTimeList
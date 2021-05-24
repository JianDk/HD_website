from django import forms
from django.core.validators import RegexValidator

class customerLocalDeliveryForm(forms.Form):
    customerName = forms.CharField(label = 'Name', max_length=20, required=True)
    customerEmail = forms.EmailField(label = 'Email', max_length=50, required=True)
    customerMobile = forms.CharField(label = 'Mobile', max_length = 10, 
    required=True, validators = [RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')])
    deliveryTime = forms.ChoiceField(choices = (), required=True)

    def __init__(self, *args, **kwargs):
        self.deliveryTimeList = kwargs.pop('deliveryTimeList')
        super().__init__(*args, **kwargs)
        self.fields['deliveryTime'].choices = self.deliveryTimeList


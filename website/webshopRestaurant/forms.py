from django import forms
from webshopRestaurant.models import Restaurant

class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__' 

class DeliveryPossible(forms.Form):
    address = forms.CharField(max_length = 200, required=True)
    
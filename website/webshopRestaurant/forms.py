from django import forms
from webshopRestaurant.models import Restaurant

class RestaurantAdminForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = '__all__' 
        
    
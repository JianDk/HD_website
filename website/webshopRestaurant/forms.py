from django import forms
from webshopRestaurant.models import Restaurant

weekdays = (
        ('Mon', 'Monday',),
        ('Tue', 'Tuesday',),
        ('Wed', 'Wednesday',),
        ('Thu', 'Thursday',),
        ('Fri', 'Friday',),
        ('Sat', 'Saturday',),
        ('Sun', 'Sunday',),
    )

class RestaurantAdminForm(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields = '__all__' 
        
    
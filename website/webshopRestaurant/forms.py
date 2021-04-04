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

    delivery_weekdays = forms.MultipleChoiceField(choices=weekdays, help_text="Select multiple days. All the selected days is possible for delivery")
    pickup_weekdays = forms.MultipleChoiceField(choices=weekdays, help_text="Select multiple days. All selected days will be available for pickup")
    
    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def clean_pickup_weekdays(self):
        pickup_weekdays = self.cleaned_data['pickup_weekdays']
        pickup_weekdays = ','.join(pickup_weekdays)
        print('here is the pickup weekdays returned')
        print(pickup_weekdays)
        return pickup_weekdays
        
    def clean_delivery_weekdays(self):
        delivery_weekdays = self.cleaned_data['delivery_weekdays']
        delivery_weekdays = ','.join(delivery_weekdays)
        print('here is the weekdays returned')
        print(delivery_weekdays)
        return delivery_weekdays 
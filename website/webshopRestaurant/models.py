from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 20)
    email = models.EmailField()
    latitude = models.DecimalField(max_digits=15, decimal_places=5)
    longitude = models.DecimalField(max_digits=15, decimal_places=5)

    is_active = models.BooleanField(default=True, help_text='If on it is possible to order takeaway both for delivery and pickup')
    has_delivery = models.BooleanField(default=True, help_text='If on, it is possible to order delivery. If not on, it is only possible to order pickup')
    
    delivery_radius = models.IntegerField(help_text="Delivery radius in km")
    
    deliverey_timeStart = models.TimeField()
    deliverey_timeEnd = models.TimeField()

    has_pickup = models.BooleanField(default=True, help_text = 'If on it is possible to pickup from this restauant')
    pickup_timeStart = models.TimeField()
    pickup_timeEnd = models.TimeField()
    

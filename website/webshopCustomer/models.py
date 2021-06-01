from django.db import models

# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=30, blank = False)
    lastname = models.CharField(max_length=30, blank = False)
    delivery = models.BooleanField(default=False)
    pickup = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    session_id = models.CharField(max_length = 100)
    deliveryAddressStreet = models.CharField(max_length = 100, blank = True)
    deliveryAddressHouseNumber = models.CharField(max_length = 20, blank = True)
    deliveryAddressPostCode = models.IntegerField(blank = True)
    comments = models.TextField(max_length = 300, blank = True)

    class Meta:
        db_table = 'customer'
        ordering = ['lastname']

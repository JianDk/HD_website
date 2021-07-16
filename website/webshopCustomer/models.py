from django.db import models

# Create your models here.
class Orders(models.Model):
    fullName = models.CharField(max_length=30, blank = False)
    email = models.EmailField(max_length=100, blank = True)
    mobile = models.CharField(max_length = 30, blank = True)
    deliveryAddress = models.CharField(max_length = 100, blank = True)
    latitude = models.CharField(max_length = 50)
    longitude = models.CharField(max_length = 50)
    deliveryTime = models.CharField(max_length = 20, blank = False)
    delivery = models.BooleanField(default=False)
    pickup = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    session_id = models.CharField(max_length = 100)
    comments = models.TextField(max_length = 300, blank = True)
    orderCreationDateTime = models.DateTimeField(auto_now_add=True, blank = True)

    class Meta:
        db_table = 'orders'
        ordering = ['fullName']

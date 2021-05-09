from django.db import models
from webshopCatalog.models import Product, Category

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50) 
    address = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 20)
    email = models.EmailField()
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)

    is_active = models.BooleanField(default=True, help_text='If active it is possible to order takeaway both for delivery and pickup')
    has_delivery = models.BooleanField(default=True, help_text='If active it is possible to order delivery. If not on, it is only possible to order pickup')
    delivery_fee = models.PositiveSmallIntegerField(default = 60, help_text = "delivery cost in dkk")
    minimum_order_total_for_delivery = models.PositiveSmallIntegerField(default  = 400, help_text= "How much kr should customer order before local delivery will be offered")
    delivery_radius = models.IntegerField(help_text="Delivery radius in km")
    delivery_preparationtime = models.PositiveSmallIntegerField(default = 60, help_text="Time it takes to prepare the order. The client cannot pickup on a time earlier than the defined minutes")
    
    delivery_monday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Monday")
    delivery_monday_timestart = models.TimeField()
    delivery_monday_timeend = models.TimeField()

    delivery_tuesday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Tuesday")
    delivery_tuesday_timestart = models.TimeField()
    delivery_tuesday_timeend = models.TimeField()

    delivery_wednesday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Wednesday")
    delivery_wednesday_timestart = models.TimeField()
    delivery_wednesday_timeend = models.TimeField()

    delivery_thursday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Thursday")
    delivery_thursday_timestart = models.TimeField()
    delivery_thursday_timeend = models.TimeField()

    delivery_friday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Friday")
    delivery_friday_timestart = models.TimeField()
    delivery_friday_timeend = models.TimeField()

    delivery_saturday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Saturday")
    delivery_saturday_timestart = models.TimeField()
    delivery_saturday_timeend = models.TimeField()

    delivery_sunday_active = models.BooleanField(default=True, help_text="If active, delivery can be performed on Sunday")
    delivery_sunday_timestart = models.TimeField()
    delivery_sunday_timeend = models.TimeField()

    pickup_preparationtime = models.SmallIntegerField(default = 30, help_text="The time needed to prepare pickup order. Client cannot pickup before this time. Defined in minutes.")
    pickup_monday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Monday")
    pickup_monday_timestart = models.TimeField()
    pickup_monday_timeend = models.TimeField()

    pickup_tuesday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Tuesday")
    pickup_tuesday_timestart = models.TimeField()
    pickup_tuesday_timeend = models.TimeField()

    pickup_wednesday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Wednesday")
    pickup_wednesday_timestart = models.TimeField()
    pickup_wednesday_timeend = models.TimeField()

    pickup_thursday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Thursday")
    pickup_thursday_timestart = models.TimeField()
    pickup_thursday_timeend = models.TimeField()

    pickup_friday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Friday")
    pickup_friday_timestart = models.TimeField()
    pickup_friday_timeend = models.TimeField()

    pickup_saturday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Saturday")
    pickup_saturday_timestart = models.TimeField()
    pickup_saturday_timeend = models.TimeField()

    pickup_sunday_active = models.BooleanField(default=True, help_text="If active, pickup is possible on Sunday")
    pickup_sunday_timestart = models.TimeField()
    pickup_sunday_timeend = models.TimeField()

    bagFee = models.PositiveSmallIntegerField(default = 4, help_text = "pose afgift in dkk")

    #Define many to many relationships to Products and Category. One restaurant can have many products from 
    #Product table and Category from category table
    products = models.ManyToManyField(Product)
    category = models.ManyToManyField(Category)

    class Meta:
        db_table = "restaurant"
        ordering = ['-name']

    def __str__(self):
        return self.name    

from django.db import models
from django.db.models.deletion import CASCADE
from webshopCatalog.models import Product
from webshopRestaurant.models import Restaurant

#Create your models here.

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)

    class Meta:
        db_table = 'cartItems'
        ordering = ['date_added']
    
    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name 

    def price(self):
        return self.product.price
    
    def add_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()
        
    def __str__(self):
        return self.cart_id
    


    
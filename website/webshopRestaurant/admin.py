from django.contrib import admin
from webshopRestaurant.forms import RestaurantAdminForm
from webshopRestaurant.models import Restaurant

# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantAdminForm
    filter_horizontal = ('products','category',)

admin.site.register(Restaurant, RestaurantAdmin)
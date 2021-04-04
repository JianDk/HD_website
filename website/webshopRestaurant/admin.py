from django.contrib import admin
from .forms import RestaurantAdminForm
from .models import Restaurant

# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantAdminForm

admin.site.register(Restaurant, RestaurantAdmin)
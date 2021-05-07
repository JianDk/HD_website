from django.shortcuts import render
from django.views import View
from website.Modules.restaurantUtils import RestaurantUtils

# Create your views here.
session_id_key = 'hd2900TakeAwayCartId'
restaurantName = "Hidden Dimsum 2900"

class TakeawayCheckout(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)
        self.deliveryStatus = self.hd2900RestaurantObject.isDeliveryOpenToday()

    def get(self, request, *args, **kwargs):
        #Check if restaurant has delivery today
        if self.deliveryStatus:
            context = {}
            return render(request, template_name = 'takeawayWebshop/webshopCheckout.html', context = context)
        
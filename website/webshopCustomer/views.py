from django.shortcuts import render, redirect
from django.views import View
from webshopCart.models import CartItem
from website.Modules.restaurantUtils import RestaurantUtils
import website.Modules.takeawayWebshopUtils as webshopUtils

# Create your views here.
session_id_key = 'hd2900TakeAwayCartId'
restaurantName = "Hidden Dimsum 2900"

class TakeawayCheckout(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)
        self.deliveryStatus = self.hd2900RestaurantObject.isDeliveryOpenToday()

    def get(self, request, *args, **kwargs):
        #Check if session is still valid
        sessionValid = webshopUtils.checkSessionIdValidity(request = request, session_id_key = session_id_key, validPeriodInDays= 7)
        if sessionValid is False: #the session has expired and the user needs to start over
            return redirect('/hd2900_takeaway_webshop')

        #Get all active products offered by the restaurant
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()

        #Check if the shopping cart items are still offered by the restaurant
        sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
        sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
        
        #Check delivery status
        
        return render(request, template_name = 'takeawayWebshop/webshopCheckout.html', context = context)
        #For address verification
            #return render(request, template_name = 'takeawayWebshop/webshopAddressTest.html', context = context)
        
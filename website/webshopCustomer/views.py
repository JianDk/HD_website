from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
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
        sessionValid = webshopUtils.checkSessionIdValidity(request = request, session_id_key = session_id_key,  validPeriodInDays = self.hd2900RestaurantObject.restaurantModelData.session_valid_time)
        if sessionValid is False: #the session has expired and the user needs to start over
            return redirect('/hd2900_takeaway_webshop')

        #Get all active products offered by the restaurant
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()

        #Check if the shopping cart items are still offered by the restaurant
        sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
        sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)

        #Check if total in sessionItems are above the limit for local delivery
        totalPrice = webshopUtils.get_BasketTotalPrice(request.session[session_id_key])
        if totalPrice < self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery:
            deliveryPossible = False
            totalPriceDeliveryMessage = "Minimum order for takeaway delivery : " + str(self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery) + ' kr'
        else:
            deliveryPossible = True
            totalPriceDeliveryMessage = ''

        #Check delivery status
        context = {'title' : 'Hidden Dimsum takeaway checkout',
        'checkoutProducts' : sessionItems,
        'totalPrice' : totalPrice,
        'deliveryActive' : self.deliveryStatus, #This is the restaurant delivery status for today 
        'deliveryPossible' : deliveryPossible,  #Relates to the total amount of order by the customer
        'totalPriceDeliveryMessage' : totalPriceDeliveryMessage}
        
        return render(request, template_name = 'takeawayWebshop/webshopCheckout.html', context = context)
        #For address verification
            #return render(request, template_name = 'takeawayWebshop/webshopAddressTest.html', context = context)

class totalPriceDeliveryPossible(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)
        self.deliveryStatus = self.hd2900RestaurantObject.isDeliveryOpenToday()

    def get(self, request, *args, **kwargs):
        context = dict()

        #Check if session is valid
        sessionValid = webshopUtils.checkSessionIdValidity(request = request, session_id_key = session_id_key, validPeriodInDays = self.hd2900RestaurantObject.restaurantModelData.session_valid_time)
        
        if sessionValid is False:
            context["pageRefresh"] = True
            return JsonResponse(context, status = 200)
        
        #Check if all items still are available. This is to assure that the products are not sold out
        #Get all active products offered by the restaurant
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()
        sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
        number_of_products_ordered_beforeCheck = len(sessionItems)
        sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
        if not sessionItems:
            context["pageRefresh"] = True
            return JsonResponse(context, status = 200)

        number_of_products_ordered_afterCheck = len(sessionItems)
        if number_of_products_ordered_beforeCheck != number_of_products_ordered_afterCheck:
            context["pageRefresh"] = True
            return JsonResponse(context, status = 200)

        #Get the total price
        context['totalPrice'] = webshopUtils.get_BasketTotalPrice(request.session[session_id_key])

        #If both restaurant offers delivery today and the total price is above the limit, the signal for delivery button is sent back
        if self.hd2900RestaurantObject.restaurantModelData.has_delivery and context['totalPrice'] >= self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery:
            context['deliveryPossible'] = True
        else:
            context['deliveryPossible'] = False
            context['minimum_totalPrice_for_delivery'] = self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery
        return JsonResponse(context, status = 200)
    

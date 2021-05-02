from webshopRestaurant.models import Restaurant
from django.shortcuts import render
from django.http import JsonResponse
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse
from website.Modules.geoLocation import GeoLocationUtils 
from website.Modules.restaurantUtils import RestaurantUtils
import website.Modules.takeawayWebshopUtils as webshopUtils
from django.conf import settings
from webshopCart.models import CartItem
import json

session_id_key = 'hd2900TakeAwayCartId'
restaurantName = "Hidden Dimsum 2900"
# Create your views here.
class hd2900_webshop_Main(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)

    def get(self, request, *args, **kwargs):
        #Check if visitor has a cookie
        sessionValid = webshopUtils.checkSessionIdValidity(request=request,session_id_key=session_id_key, validPeriodInDays=7)
        
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()
        if sessionValid:
            sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
            #Assure that the products in the session cart is still valid otherwise they should be removed. This
            #validation is made to assure that the products in the cart is still offered by the restaurant
            sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
            #Merge sessionItems with all active products and add the quantity 
            productToDisplay = self.hd2900RestaurantObject.generateProductsForView(allActiveProducts = allActiveProducts, sessionItems = sessionItems)

        else:
            productToDisplay = self.hd2900RestaurantObject.generateProductsForView(allActiveProducts = allActiveProducts, sessionItems = [])

        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)
    
        context = {
            'addressField' : addressFieldForm,
            'products' : productToDisplay,
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('<h1>hello world</h1>')

class ChangeItemQuantity(View):
    def get(self, request, *args, **kwargs):
        #First check if a session already exists
        sessionValid = webshopUtils.checkSessionIdValidity(request=request,session_id_key=session_id_key, validPeriodInDays=7)
        restaurant = Restaurant.objects.get(name = restaurantName)
        print(sessionValid)

        if sessionValid is False: #The user has not a session and it is first time that the user puts a product in basket. A new session will be assigned to the user
            #Assign a new session id
            request.session[session_id_key] = webshopUtils.createNewSessionId()
            #Extract what the user has clicked
            productToChange = webshopUtils.productToChange(request)
             
            #Check if the product exists in the first place. 
            success, updatedQuantity = webshopUtils.addRemoveProductInBasket(productToChange = productToChange, 
            session_id = request.session[session_id_key], 
            restaurant = restaurant)

            #If success evaluates to False, then user hitted a subtract button while sessionValid is False. In this case do nothing
            if success is False:
                #Do nothing since the product does not exists in the data base
                context = {"update_field" : False}
                return JsonResponse(context, status = 200)
            
            if success:
                context = {"update_field" : True, 
                "product_to_update_slug" : productToChange[0].slug, 
                "updatedQuantity" : updatedQuantity, 
                "sessionIdKey" : session_id_key,
                "sessionId" : request.session[session_id_key]}
                return JsonResponse(context, status = 200)

        if sessionValid:
            #Extract which product element the suer has selected
            productToChange = webshopUtils.productToChange(request)

            #Update the product in the backend 
            success, updatedQuantity = webshopUtils.addRemoveProductInBasket(productToChange = productToChange, 
            session_id = request.session[session_id_key], 
            restaurant = restaurant)

            context = {"update_field": True,
            "product_to_update_slug" : productToChange[0].slug,
            "updatedQuantity" : updatedQuantity,
            "sessionIdKey" : session_id_key,
            "sessionId" : request.session[session_id_key]}
            return JsonResponse(context, status = 200)

class AddressCheckForDeliverability(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = "Hidden Dimsum 2900")
        
    def post(self, request, *args, **kwargs):
        deliveryAddress = request.body
        deliveryAddress = json.loads(deliveryAddress)['deliveryAddress']
        #If address is empty Google geocode service will not be called
        if not deliveryAddress:
            return JsonResponse({"message" : False}, staus = 200)
                
        location = GeoLocationUtils(settings.GOOGLE_GEOCODING_API_KEY)
        location.addressToGeoCoordinates(address = deliveryAddress)

        #Calculate distance to customer address
        distance_km = location.distanceBetweenCoordinates(coordinate1=(self.hd2900RestaurantObject.restaurantModelData.longitude,
        self.hd2900RestaurantObject.restaurantModelData.latitude),
        coordinate2=(location.geoDict['longitude'], location.geoDict['latitude']))
            
        if distance_km <= self.hd2900RestaurantObject.restaurantModelData.delivery_radius:
            offerDelivery = True
        else:
            offerDelivery = False
        
        return JsonResponse({"message" : offerDelivery}, status = 200)
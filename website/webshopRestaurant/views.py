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
        #Inform visitor the delivery status today
        deliveryStatus = self.hd2900RestaurantObject.isDeliveryOpenToday()

        if deliveryStatus:
            takeawayStatusMsg = "We offer local delivery today"
        else:
            takeawayStatusMsg = "Order online and pickup at Hidden Dimsum 2900. Local delivery not available today"

        #Check if visitor has a cookie
        sessionValid = webshopUtils.checkSessionIdValidity(request=request,session_id_key=session_id_key, validPeriodInDays = self.hd2900RestaurantObject.restaurantModelData.session_valid_time)
        
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()
        if sessionValid:
            sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
            #Assure that the products in the session cart is still valid otherwise they should be removed. This
            #validation is made to assure that the products in the cart is still offered by the restaurant
            sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
            #Merge sessionItems with all active products and add the quantity 
            productToDisplay = self.hd2900RestaurantObject.generateProductsForView(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
            totalItemsInBasket = webshopUtils.get_totalBasketItemQuantity(request.session[session_id_key])
        else:
            productToDisplay = self.hd2900RestaurantObject.generateProductsForView(allActiveProducts = allActiveProducts, sessionItems = [])
            totalItemsInBasket = 0

        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET) #<-------------------REMOVE THIS
        print('here is delivery end time!!!!!!!!!')
        print(self.hd2900RestaurantObject.get_deliveryOpenTime().strftime('%H:%M'))
        
    
        context = {
            'title' : restaurantName + ' online takeaway',
            'takeawayStatusToday' : takeawayStatusMsg,
            'deliveryStatus' : deliveryStatus,
            'deliveryStartTime' : self.hd2900RestaurantObject.get_deliveryOpenTime().strftime('%H:%M'),
            'deliveryEndTime' : self.hd2900RestaurantObject.get_deliveryEndtime().strftime('%H:%M'),
            'addressField' : addressFieldForm,
            'products' : productToDisplay,
            'totalItemsInBasket' : totalItemsInBasket,
            'deliveryRadius' : self.hd2900RestaurantObject.restaurantModelData.delivery_radius,
            'deliveryFee' : self.hd2900RestaurantObject.restaurantModelData.delivery_fee,
            'minimumOrderForDelivery' : self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery,
        }
        return render(request, template_name="takeawayWebshop/takeawayProducts.html", context = context)

class ChangeItemQuantity(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)

    def get(self, request, *args, **kwargs):
        #First check if a session already exists
        sessionValid = webshopUtils.checkSessionIdValidity(request=request,session_id_key=session_id_key, validPeriodInDays = self.hd2900RestaurantObject.restaurantModelData.session_valid_time)

        if sessionValid is False: #The user has not a session and it is first time that the user puts a product in basket. A new session will be assigned to the user
            #Assign a new session id
            request.session[session_id_key] = webshopUtils.createNewSessionId()
            #Extract what the user has clicked
            productToChange = webshopUtils.productToChange(request)
             
            #Check if the product exists in the first place. 
            success, updatedQuantity = webshopUtils.addRemoveProductInBasket(productToChange = productToChange, 
            session_id = request.session[session_id_key], 
            restaurant = self.hd2900RestaurantObject.restaurantModelData)

            #If success evaluates to False, then user hitted a subtract button while sessionValid is False. In this case do nothing
            if success is False:
                #Do nothing since the product does not exists in the data base
                context = {"update_field" : False,
                "totalItemsInBasket" : 0}
                return JsonResponse(context, status = 200)
            
            if success:
                totalItemsInCart = webshopUtils.get_totalBasketItemQuantity(session_id = request.session[session_id_key])
                context = {"update_field" : True, 
                "product_to_update_slug" : productToChange[0].slug, 
                "updatedQuantity" : updatedQuantity, 
                "sessionIdKey" : session_id_key,
                "sessionId" : request.session[session_id_key],
                "totalItemsInBasket" : totalItemsInCart}
                return JsonResponse(context, status = 200)

        if sessionValid:
            #Extract which product element the suer has selected
            productToChange = webshopUtils.productToChange(request)

            #Update the product in the backend 
            success, updatedQuantity = webshopUtils.addRemoveProductInBasket(productToChange = productToChange, 
            session_id = request.session[session_id_key], 
            restaurant = self.hd2900RestaurantObject.restaurantModelData)

            totalItemsInCart = webshopUtils.get_totalBasketItemQuantity(session_id=request.session[session_id_key])

            context = {"update_field": True,
            "product_to_update_slug" : productToChange[0].slug,
            "updatedQuantity" : updatedQuantity,
            "sessionIdKey" : session_id_key,
            "sessionId" : request.session[session_id_key],
            "totalItemsInBasket" : totalItemsInCart}
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
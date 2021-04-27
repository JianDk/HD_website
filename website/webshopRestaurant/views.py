from django.shortcuts import render
from django.http import JsonResponse
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse
from website.Modules.geoLocation import GeoLocationUtils 
from website.Modules.restaurantUtils import RestaurantUtils
import website.Modules.sessionUtils as sessionUtils
from django.conf import settings
from webshopCart.models import CartItem
from webshopCatalog.models import Product
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
        sessionValid = sessionUtils.checkSessionIdValidity(request=request,session_id_key=session_id_key, validPeriodInDays=7)
        
        if sessionValid:
            print('session is valid and extract the ordered items')
            sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
            #Make sure that the ordered products are all still valid and the restaurant still has them
            allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()
            #Assure that the products in the session cart is still valid otherwise they should be removed. This
            #validation is made to assure that the products in the cart is still offered by the restaurant
            sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)
            #Merge sessionItems with all active products and add the quantity 
            self.hd2900RestaurantObject.generateProductsForView(allActiveProducts = allActiveProducts, sessionItems = sessionItems)

        else:
            print('session do not exist')
            #Get a list of products to be displayed for restaurant Hidden Dimsum 2900
        
        products = self.hd2900RestaurantObject.get_all_products()

        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)
    
        context = {
            'addressField' : addressFieldForm,
            'products' : products,
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('<h1>hello world</h1>')

class ChangeItemQuantity(View):

    def get(self, request, *args, **kwargs):
        print('called here at get')
        print(request.GET.get('itemToChange'))
        print('\n')
        print(request.session)
        sessionUtils.checkSessionIdValidity(request = request, session_id_key=session_id_key, validPeriodInDays=7)
        #First check if a cart id exists and if it exists check if it is valid
        if session_id_key in request.session:
            print('cart id exists and is this value')
            print(request.session[session_id_key])
        else:
            #In which case a new session id is assigned
            request.session[session_id_key] = sessionUtils.createNewSessionId()
            print('here is the item to change')
            print(request.GET.get("itemToChange"))
            print(type(request.GET.get("itemToChange")))
            
            #Detect if it is add og subtract button that has been pressed
            if 'btn_add_' in request.GET.get("itemToChange"):                
                #The item to add is saved to the cart model
                itemSlug = request.GET.get('itemToChange').replace('btn_add_','')
                product = Product.objects.filter(slug=itemSlug)[0]
                restaurant = RestaurantUtils(restaurantName = restaurantName)
                cart = CartItem.objects.create(cart_id = request.session[session_id_key], 
                product = product,
                quantity = 1,
                restaurant = restaurant.restaurantModelData)
                cart.save()

            if 'btn_subtract_' in request.GET.get("itemToChange"):
                #Get all the products
                pass

        return JsonResponse({"message" : "item received by server", "sessionid": request.session['hd2900TakeAwayCartId']}, status = 200)

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
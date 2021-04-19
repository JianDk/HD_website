from django.shortcuts import render
from django.http import JsonResponse
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse
from website.Modules.geoLocation import GeoLocationUtils 
from website.Modules.restaurantUtils import RestaurantUtils
from django.conf import settings
from webshopRestaurant.models import Restaurant
import json

# Create your views here.
class hd2900_webshop_Main(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = "Hidden Dimsum 2900")


    def get(self, request, *args, **kwargs):
        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)

        #Get a list of products to be displayed for restaurant Hidden Dimsum 2900
        products = self.hd2900RestaurantObject.get_all_products()
        print(products[0].image_path)
        context = {
            'addressField' : addressFieldForm,
            'products' : products
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('<h1>hello world</h1>')

class AddItemToBasket(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({"message" : "item received by server"}, status = 200)

    def get(self, request, *args, **kwargs):
        print('called here at get')
        print(request.GET.get('itemToAdd'))
        print('\n')
        print(request.session)

        #First check if a cart id exists
        if 'hd2900TakeAwayCartId' in request.session:
            print('cart id exists and is this value')
            print(request.session['hd2900TakeAwayCartId'])
        else:
            print('cart id cannot be found')
        
        request.session['hd2900TakeAwayCartId'] = '12345678910'
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
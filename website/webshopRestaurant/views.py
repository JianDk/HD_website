from django.shortcuts import render
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse
from website.Modules.geoLocation import GeoLocationUtils 
from website.Modules.restaurantUtils import RestaurantUtils
from django.conf import settings
from webshopRestaurant.models import Restaurant

# Create your views here.
class hd2900_webshop_Main(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = "Hidden Dimsum 2900")


    def get(self, request, *args, **kwargs):
        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)
        context = {
            'addressField' : addressFieldForm,
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        print('push button clicked triggered from post')
        # AddressInputForm = DeliveryPossible(request.POST)
        # if AddressInputForm.is_valid():
        #     address = AddressInputForm.cleaned_data['address']
        #     location = GeoLocationUtils(settings.GOOGLE_GEOCODING_API_KEY)
        #     location.addressToGeoCoordinates(address = address)

        #     #Calculate distance to customer address
        #     distance_km = location.distanceBetweenCoordinates(coordinate1=(self.hd2900RestaurantObject.restaurantModelData.longitude,
        #     self.hd2900RestaurantObject.restaurantModelData.latitude),
        #     coordinate2=(location.geoDict['longitude'], location.geoDict['latitude']))
            
        #     if distance_km <= self.hd2900RestaurantObject.restaurantModelData.delivery_radius:
        #         print('Delivery possible')
        #         offerDelivery = True
        #     else:
        #         print('Delivery not possible')
        #         offerDelivery = False
            

        #     print('here is the distance from HD 2900 to customer ', str(distance_km), ' km')

        return HttpResponse('<h1>hello world</h1>')
        
class AddressCheckForDeliverability(View):
    def post(self, request, *args, **kwargs):
        print('ajax called here')
        return HttpResponse("<h1>This is the respose from DeliveryPossible</h1>")
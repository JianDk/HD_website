from django.shortcuts import render
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse
from website.Modules.geoLocation import GeoLocationUtils 
from django.conf import settings

# Create your views here.
class hd2900_webshop_Main(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        
        pass

    def get(self, request, *args, **kwargs):
        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)
        context = {
            'addressField' : addressFieldForm,
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        print('post has been called')
        form = DeliveryPossible(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = GeoLocationUtils(settings.GOOGLE_GEOCODING_API_KEY)
            location.addressToGeoCoordinates(address = address)
            print(location.geoDict)
        return HttpResponse('<h1>hello world</h1>')


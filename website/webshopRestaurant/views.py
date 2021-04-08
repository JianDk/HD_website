from django.shortcuts import render
from webshopRestaurant.forms import DeliveryPossible
# Create your views here.
from django.views import View
from django.http import HttpResponse

# Create your views here.
class hd2900_Main(View):
    def get(self, request, *args, **kwargs):
        #form for checking if customer address is within delivery range
        addressFieldForm = DeliveryPossible(request.GET)
        context = {
            'addressField' : addressFieldForm,
        }
        return render(request, template_name="takeawayWebshop/base.html", context = context)
    
    def post(self, request, *args, **kwargs):
        form = DeliveryPossible(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            print(address)
        return HttpResponse('<h1>hello world</h1>')


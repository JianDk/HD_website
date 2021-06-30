from types import CodeType
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from webshopCart.models import CartItem
from .forms import customerLocalDeliveryForm
from website.Modules.restaurantUtils import RestaurantUtils
import website.Modules.takeawayWebshopUtils as webshopUtils
from website.Modules.geoLocation import GeoLocationTools
from django.http import HttpResponse
from website.Modules.paymentModule import NETS


# Create your views here.
session_id_key = 'hd2900TakeAwayCartId'
restaurantName = "Hidden Dimsum 2900"
platform = 'test' #The platform for NETS payment

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
        
        #Check if delivery is still possible at this given date and time
        deliveryPossible = self.hd2900RestaurantObject.isDeliveryPossible()
        
        #Get all active products offered by the restaurant
        allActiveProducts = self.hd2900RestaurantObject.get_all_active_products()

        #Check if the shopping cart items are still offered by the restaurant
        sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
        sessionItems = self.hd2900RestaurantObject.validateSessionOrderedProducts(allActiveProducts = allActiveProducts, sessionItems = sessionItems)

        #Check if total in sessionItems are above the limit for local delivery
        totalPrice = webshopUtils.get_BasketTotalPrice(request.session[session_id_key])

        if totalPrice < self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery:
            deliveryButtonActive = False
            totalPriceDeliveryMessage = "Minimum order for takeaway delivery : " + str(self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery) + ' kr'
        else:
            deliveryButtonActive = True
            totalPriceDeliveryMessage = ''

        #Check delivery status
        context = {'title' : 'Hidden Dimsum takeaway checkout',
        'checkoutProducts' : sessionItems,
        'totalPrice' : totalPrice,
        'deliveryPossible' : deliveryPossible,  #Relates to if it at all is possible to order delivery for today at the given time
        'deliveryButtonActive' : deliveryButtonActive, #checks if the total price is above the minimum limit for delivery
        'totalPriceDeliveryMessage' : totalPriceDeliveryMessage}
        return render(request, template_name = 'takeawayWebshop/webshopCheckout.html', context = context)

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
        deliveryPossible = self.hd2900RestaurantObject.isDeliveryPossible()
        if deliveryPossible and context['totalPrice'] >= self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery:
            context['deliveryButtonActive'] = True
        else:
            context['deliveryButtonActive'] = False
            context['minimum_totalPrice_for_delivery'] = self.hd2900RestaurantObject.restaurantModelData.minimum_order_total_for_delivery
        return JsonResponse(context, status = 200)
    
class DeliveryForm(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)

    def get (self, request, *args, **kwargs):
        #Display the total cost together with delivery fee and bag fee
        sessionItems = CartItem.objects.filter(cart_id = request.session[session_id_key])
        
        #Decide if delivery is still possible
        deliveryPossible = self.hd2900RestaurantObject.isDeliveryPossible()
        
        #deliveryPossible = True #<-----------------------------------------------DELETE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if deliveryPossible is False:
            #Redirect the user to pickup
            context = dict()
            context['message'] = "Sorry takeaway delivery is closed for today."
            return render(request, template_name = "takeawayWebshop/takeawayClosed.html", context = context)
        
        #Generate time list for receiving delivery package
        deliveryTimeList = self.hd2900RestaurantObject.get_deliveryTimeList()

        #Get the payment id from NETS
        #Calculate the grand total the total price in basket + delivery fee 0 bag fee
        totalPrice = webshopUtils.get_BasketTotalPrice(request.session[session_id_key]) + self.hd2900RestaurantObject.restaurantModelData.delivery_fee + self.hd2900RestaurantObject.restaurantModelData.bagFee
        payment = NETS()
        paymentId = payment.get_paymentId(platform = platform,
            reference = 'here comes order id', 
            name = 'Hidden Dimsum 2900 Takeaway',
            paymentReference ='Hidden Dimsum 2900 takeaway paymrent ref',
            unitPrice = int(totalPrice) *100)

        context = dict()
        #Get the total price and add on top of it the bag fee and delivery cost
        context['title'] = 'Local delivery checkout'
        context['orderProducts'] = sessionItems
        context['deliveryCost'] = self.hd2900RestaurantObject.restaurantModelData.delivery_fee
        context['bagFee'] = self.hd2900RestaurantObject.restaurantModelData.bagFee
        context['grandTotal'] = webshopUtils.get_BasketTotalPrice(request.session[session_id_key]) + context['deliveryCost'] + context['bagFee']
        checkoutLocalDeliveryForm = customerLocalDeliveryForm(deliveryTimeList = deliveryTimeList, auto_id = True)
        context['customerDeliveryForm'] = checkoutLocalDeliveryForm
        context['paymentId'] = paymentId.json()['paymentId']

        return render(request, template_name = "takeawayWebshop/checkoutLocalDelivery.html", context = context)
        

class localDeliveryCheckoutAddressCheck(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)

    def get(self, request, *args, **kwargs):
        x = request.GET.get('x')
        y = request.GET.get('y')
        x = float(x)
        y = float(y)
        restaurant_latitude = self.hd2900RestaurantObject.restaurantModelData.latitude
        restaurant_longitude = self.hd2900RestaurantObject.restaurantModelData.longitude
        geoTools = GeoLocationTools()
        distance_km = geoTools.distanceBetweenCoordinates(coordinate1=(restaurant_longitude,restaurant_latitude), 
        coordinate2=(x,y))
        context = dict()
        if distance_km <= self.hd2900RestaurantObject.restaurantModelData.delivery_radius:
            context['distance_within_delivery_range'] = True
        else:
            context['distance_within_delivery_range'] = False
        return JsonResponse(context, status = 200)

class Payment(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)
    
    def post(self, request, *args, **kwargs):
        #Check if session is still valid 
        sessionValid = webshopUtils.checkSessionIdValidity(request = request, session_id_key = session_id_key, validPeriodInDays = self.hd2900RestaurantObject.restaurantModelData.session_valid_time)
        
        #In this case the session has expired and the user will be redirected
        if sessionValid is False:
            return redirect('hd2900_takeaway_webshop')
        
        #Write the customer info into the data base
        webshopUtils.create_or_update_Order(session_id_key=session_id_key, request=request, deliveryType='delivery')

        #Calculate the total price followed by creation of paymentID from NETS
        totalPrice = webshopUtils.get_BasketTotalPrice(request.session[session_id_key]) + self.hd2900RestaurantObject.restaurantModelData.delivery_fee + self.hd2900RestaurantObject.restaurantModelData.bagFee

        #Create an order reference and link that to NETS reference
        reference = webshopUtils.get_order_reference(request = request, session_id_key=session_id_key)

        #Get the payment id from NETS 
        payment = NETS()
        paymentId = payment.get_paymentId(platform = platform,
        reference = reference, 
        name = 'Hidden Dimsum 2900 Takeaway',
        paymentReference ='Hidden Dimsum 2900 takeaway paymrent ref',
        unitPrice = int(totalPrice) *100)

        if paymentId.status_code == 201:
            paymentId = paymentId.json()['paymentId']

        #Put the checkout key and the payment id into the page that javascript is going to read from during payment
        checkoutKey = payment.getCheckoutKey(platform = platform)

        context = dict()
        context['paymentId'] = paymentId
        context['checkoutKey'] = checkoutKey

        return render(request, template_name="takeawayWebshop/webshopPayment.html", context = context)

class PaymentComplete(View):
    def __init__(self):
        #Get model webshopRestaurant data for hd2900 restaurant for location id for this restaurant
        self.hd2900RestaurantObject = RestaurantUtils(restaurantName = restaurantName)
    
    def get(self, request, *args, **kwargs):
        #Get all user information and the ordered products and display it to the user
        session_id = request.session[session_id_key]
        order = webshopUtils.get_order(session_id_key = session_id_key, request = request)
        context = dict()
        context['order'] = order
        print(dir(order))

        return render(request, template_name = "takeawayWebshop/webshopPaymentComplete.html", context = context)




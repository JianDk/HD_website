from webshopCatalog.models import Product
import datetime
from random import choice
from string import ascii_uppercase
from webshopCart.models import CartItem
from webshopCustomer.models import Orders


#Product related 
def productToChange(request):
    '''
    Extract which product needs to be added or subtracted from the basket
    '''
    itemSlug = request.GET.get('itemToChange')
    if 'btn_add_' in itemSlug:
        itemSlug = itemSlug.replace('btn_add_','')
        #Get the product that is related to itemSlug
        product = Product.objects.filter(slug = itemSlug)[0]
        return (product, 'add')
    
    if 'btn_subtract_' in itemSlug:
        itemSlug = itemSlug.replace('btn_subtract_','')
        #Get the product that is related to itemSlug
        product = Product.objects.filter(slug = itemSlug)[0]
        return (product, 'subtract')

def addRemoveProductInBasket(productToChange, session_id, restaurant):
    '''
    Given the productToChange tuple and the session_id string, a query will be made to the data base to check if 
    the product and the session already exists. If it already exists the data base entry will be updated, otherwise the
    entry will be created or deleted
    '''
    #check if the cartItem exists in the first place
    cartItem = CartItem.objects.filter(cart_id = session_id, product = productToChange[0], restaurant = restaurant)

    if productToChange[1] == 'subtract':
        if not cartItem:
            success = False
            updatedQuantity = None
            return success, updatedQuantity
        
        if cartItem:
            cartItem = cartItem[0]
            #get the current quantity for this specific cartItem
            if cartItem.quantity - 1 < 1:
                cartItem = cartItem.delete()
                
                updatedQuantity = 0
            else:
                cartItem.quantity = cartItem.quantity - 1
                cartItem.save()
                updatedQuantity = cartItem.quantity
            success = True
            return success, updatedQuantity
    
    if productToChange[1] == 'add':
        if not cartItem:
            #then the cart item will be created
            cartitem = CartItem.objects.create(cart_id = session_id,
            product = productToChange[0], 
            quantity = 1,
            restaurant = restaurant)
            cartitem.save()

            success = True
            updatedQuantity = 1
            return success, updatedQuantity

        if cartItem:
            #Update the product quantity for cartItem
            cartItem[0].quantity += 1
            cartItem[0].save()
            updatedQuantity = cartItem[0].quantity
            success = True
            return success, updatedQuantity

def get_totalBasketItemQuantity(session_id):
    '''
    Given the session_id string, a query will be made to the data base. All sessions belonging to this id will be obtained
    and the total item counted up and returned
    '''
    cartItems = CartItem.objects.filter(cart_id = session_id)
    if not cartItems:
        totalQuantity = 0
        return totalQuantity 
    else:
        totalQuantity = 0
        for item in cartItems:
            totalQuantity += item.quantity
        return totalQuantity

def get_BasketTotalPrice(session_id):
    '''
    Given the session_id string a query will be made to the data base. All ordered products related to this session will be
    extracted and a total price calculated and returned
    '''
    cartItems = CartItem.objects.filter(cart_id = session_id)
    totalPrice =0
    if not cartItems:
        return totalPrice
    else:
        for item in cartItems:
            totalPrice += (item.quantity * item.product.price)
        return totalPrice

def createNewSessionId():
    '''
    Generates a session id which is a random string of 50 characters. The first 20 characters in the string is the 
    date and time and the subsequent 30 characters are random generated
    '''
    firstPart = datetime.datetime.now().strftime(format = "%d%m%Y%H%M%S%f")
    #append further 30 upper case characters to make the session id unique
    lastPart = ''.join(choice(ascii_uppercase) for i in range(30))
    session_id = firstPart + lastPart

    return session_id

def create_or_update_Order(session_id_key, request, deliveryType):
        '''
        Given the session_id_key, the corresponding session id will be read from the request.session. If the session exists 
        in data base already, the existing order will be updated with the new information posted by the user. Otherwise a 
        new order will be created. The deliveryType can either be "delivery" or "pickup" and is used to register the order with
        the right information
        '''

        #log the form information into the session
        customerName = request.POST['customerName']
        customerEmail = request.POST['customerEmail']
        customerMobile = request.POST['customerMobile']
        customerComment = request.POST['comments']
        deliveryTime = request.POST['deliveryTime']
        customerAddress = request.POST['addressField']

        #First get the sessionId from the request
        sessionId = get_sessionId(request = request, session_id_key = session_id_key)

        #Check if that sessionId already exists
        orders = Orders.objects.filter(session_id = sessionId)

        if not orders:
            if deliveryType == 'delivery':
                newOrder = Orders(fullName = customerName,
                email = customerEmail,
                mobile = customerMobile,
                session_id = sessionId,
                deliveryAddress = customerAddress,
                comments = customerComment,
                deliveryTime = deliveryTime,
                delivery = True,
                pickup = False)
                newOrder.save()
            
            if deliveryType == 'pickup':
                newOrder = Orders(fullName = customerName,
                email = customerEmail,
                mobile = customerMobile,
                session_id = sessionId,
                deliveryAddress = customerAddress,
                comments = customerComment,
                deliveryTime = deliveryTime,
                delivery = False,
                pickup = True)
                newOrder.save()
        else:
            existingOrder = orders[0]
            existingOrder.fullName = customerName
            existingOrder.email = customerEmail
            existingOrder.mobile = customerMobile
            existingOrder.session_id = sessionId
            existingOrder.deliveryAddress = customerAddress
            existingOrder.comments = customerComment
            existingOrder.deliveryTime = deliveryTime

            if deliveryType == 'delivery':
                existingOrder.delivery = True
                existingOrder.pickup = False
            
            if deliveryType == 'pickup':
                existingOrder.delivery = False
                existingOrder.pickup = True
            existingOrder.save()
    
def get_order(session_id_key, request):
    '''
    Given the request and session_id_key the order will be retrieved from the data base and returned. This method is 
    intend to be used at the payment confirmation page, confirming all logged information to the customer
    '''
    sessionId = get_sessionId(request = request, session_id_key=session_id_key)
    order = Orders.objects.filter(session_id = sessionId)
    order = order[0]
    return order

def get_order_reference(request, session_id_key):
    '''
    The session id will be retried from the request.session and if the Order is created in the data base the order id will be returned
    '''
    sessionId = get_sessionId(request = request, session_id_key=session_id_key)
    orders = Orders.objects.filter(session_id = sessionId)

    #If for some reasons the order has not been created
    if not orders:
        return False
    
    if orders[0].delivery is True:
        return 'delivery_' + str(orders[0].id)
    
    if orders[0].delivery is False:
        return 'pickup_' + str(orders[0].id)

def get_sessionId(request, session_id_key):
    '''
    Given the request and session_id_key and the request, the session id is retrieved
    '''
    return request.session[session_id_key]


def checkSessionIdValidity(request, session_id_key, validPeriodInDays):
    '''
    Check if session has already assigned an id. If session id exists a check will be made to see if it is more than 
    validPeriodInDays old.  
    '''
    if session_id_key in request.session:
        #Do a check in the data base to see if we can find it
        sessionData = CartItem.objects.filter(cart_id = request.session[session_id_key])
        if not sessionData:
            return False
        
        #check all entries for the cart id. If all date added is below validPeriodInDays, the test has passed
        now = datetime.datetime.now()
        for item in sessionData:
            timeDelta = now - item.date_added
            timeDelta = timeDelta.seconds
            if (timeDelta / (60 * 60 * 24)) <= validPeriodInDays:
                return True
        return False
    else:
        return False
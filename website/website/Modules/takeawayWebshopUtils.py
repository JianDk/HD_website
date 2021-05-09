from webshopCatalog.models import Product
import datetime
from random import choice
from string import ascii_uppercase
from webshopCart.models import CartItem

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
            #get the current quantity for this specific cartItem
            if cartItem[0].quantity - 1 <= 0:
                cartItem[0].delete()
                updatedQuantity = 0
            else:
                cartItem[0].quantity = cartItem[0].quantity - 1
                cartItem[0].save()
                updatedQuantity = cartItem[0].quantity
            success = True
            return success, updatedQuantity
    
    if productToChange[1] == 'add':
        if not cartItem:
            #then the cart item will be created
            CartItem.objects.create(cart_id = session_id,
            product = productToChange[0], 
            quantity = 1,
            restaurant = restaurant)

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
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
    if productToChange[1] == 'subtract':
        #check if the cartItem exists in the first place
        cartItem = CartItem.objects.filter(cart_id = session_id, product = productToChange[0], restaurant = restaurant)
        
        if not cartItem:
            success = False
            updatedQuantity = None
            return success, updatedQuantity
        
        if cartItem:
            print('cartitems exists. Update cart items quantity')
    
    if productToChange[1] == 'add':
        

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
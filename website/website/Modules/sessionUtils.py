import datetime
from random import choice
from string import ascii_uppercase
from webshopCart.models import CartItem

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


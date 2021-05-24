from webshopRestaurant.models import Restaurant
import datetime

class RestaurantUtils:
    def __init__(self, restaurantName):
        self.restaurantModelData = Restaurant.objects.get(name=restaurantName)
        #once the restaurant is found we will change the restaurant latitude and longitude data format to float
        self.restaurantModelData.latitude = float(self.restaurantModelData.latitude)
        self.restaurantModelData.longitude = float(self.restaurantModelData.longitude)

    def get_all_products(self):
        products = self.restaurantModelData.products.all()
        return products
    
    def get_all_active_products(self):
        '''
            Filter all the products belonging to the restaurant and only return the active products
        '''
        products = self.get_all_products()
        products = list(products)
        activeproducts = list()
        for item in products:
            if item.is_active:
                activeproducts.append(item)
        return activeproducts
    
    def validateSessionOrderedProducts(self, allActiveProducts, sessionItems):
        '''
        given the products ordered in a given cart and the current restaurant products which is obtained from
        get_all_active_products, this method removes any products in the session cart which is not in the return 
        from get_all_active_products
        '''
        if not allActiveProducts or not sessionItems:
            return None
            
        #Obtain a list of product id in currentRestaurantProducts
        allActiveProductIds = [item.id for item in allActiveProducts]
        productIdsToRemove = list()
        
        for item in sessionItems:
            if item.product_id not in allActiveProductIds:
                productIdsToRemove.append(item.product_id)
        productIdsToRemove = list(set(productIdsToRemove))
        
        for productId in productIdsToRemove:
            sessionItems.filter(product_id = productId).delete()

        return sessionItems
    
    def generateProductsForView(self, allActiveProducts, sessionItems):
        '''
        After sessionItems has been validated and any products in sessionItems no longer active has been removed from
        validateSessionOrderedProducts, a list of products to be presented to the viewer is generated
        '''
        productListToDisplay = list()
        #Get a list of unique product_id in sessionItems
        productIdInSessionItems = [item.product_id for item in sessionItems]
        if sessionItems:
            for product in allActiveProducts:
                productDict = dict()
                productDict['product'] = product
                
                if product.id in productIdInSessionItems:
                    productDict['quantity'] = sessionItems.filter(product_id = product.id)[0].quantity
                else:
                    productDict['quantity'] = 0
                
                productListToDisplay.append(productDict)
        else:
            for product in allActiveProducts:
                productDict = dict()
                productDict['product'] = product
                productDict['quantity'] = 0
                productListToDisplay.append(productDict)
                        
        return productListToDisplay

    def isDeliveryOpenToday(self):
        '''
        Checks if the restaurant actually offers delivery today. Returns either True or False 
        as delivery possible or not possible, respectively
        '''
        self.today_weekday_string = self._convert_isoweekday_to_weekday(datetime.datetime.today().isoweekday())
        return self.restaurantModelData.__dict__['delivery_' + self.today_weekday_string + '_active']
    
    def isDeliveryPossible(self):
        '''
        Takes the date, time and the lead time to produce a delivery order into account. Then the method returns either 
        true or false on if delivery can be offered for today. This method is the main method used to check if delivery is
        possible.
        '''
        deliveryPossible = self.isDeliveryOpenToday()
        
        if deliveryPossible is False: #In this case the restaurant does not offere delivery for today
            return deliveryPossible
        
        #Get the end time of today's delivery
        deliveryEndTime = self.get_deliveryEndtime()
        deliveryEndTime = deliveryEndTime.strftime('%H:%M:%S')       

        #Get delivery end time with date and form it as a date time object to allow comparison
        today = datetime.date.today().strftime('%d-%m-%Y')

        deliveryEndTime = datetime.datetime.strptime(today + ' ' + deliveryEndTime, '%d-%m-%Y %H:%M:%S')

        pickUpPreparationTime = self.restaurantModelData.pickup_preparationtime
        deliveryPreparationTime = self.restaurantModelData.delivery_preparationtime

        #Get current time and add on top of that the pickup preparation time (time it takes to cook food) and delivery time (time it takes to deliver)
        currentTime = datetime.datetime.now()
        estimatedDeliveryTime = currentTime + datetime.timedelta(minutes=pickUpPreparationTime + deliveryPreparationTime)

        if estimatedDeliveryTime <= deliveryEndTime:
            deliveryPossible = True
        else:
            deliveryPossible = False

        return deliveryPossible

    def get_deliveryEndtime(self):
        '''
        Get today's delivery end time and returns it as a string in format HH:MM:SS
        '''
        weekday = self._convert_isoweekday_to_weekday(isoweekday = datetime.datetime.today().isoweekday())
        return self.restaurantModelData.__dict__['delivery_' + weekday + '_timeend']    

    def get_deliveryTimeList(self):
        '''
        Given the current time and a time resolution of 15 min this script creates a list of the fastest 
        takeaway delivery time which is the time point from now + preparation time + delivery time and the time
        point where the restaurant closes
        '''
        #Generate time list for receiving delivery package
        deliveryEndTime = self.get_deliveryEndtime()
        deliveryEndTime = deliveryEndTime.strftime('%H:%M:%S')    
        today = datetime.date.today().strftime('%d-%m-%Y')
        deliveryEndTime = datetime.datetime.strptime(today + ' ' + deliveryEndTime, '%d-%m-%Y %H:%M:%S')
        deliveryStartTime = datetime.datetime.now() + datetime.timedelta(minutes=self.restaurantModelData.pickup_preparationtime + self.restaurantModelData.delivery_preparationtime)
        
        #Round up delivery start time to the closest 15 min
        deliveryStartTime = self.roundTimeUp(currentTime=deliveryStartTime, timeresolution=15)
        deliveryTimeList = list()
        deliveryTimeList.append( (deliveryStartTime.strftime('%H:%M'), deliveryStartTime.strftime('%H:%M')) )

        while deliveryStartTime < deliveryEndTime:
            deliveryStartTime = deliveryStartTime + datetime.timedelta(minutes = 15)
            deliveryTimeList.append( (deliveryStartTime.strftime('%H:%M'), deliveryStartTime.strftime('%H:%M')) )
        
        return deliveryTimeList
    
    def roundTimeUp(self, currentTime, timeresolution):
        '''
        Given the currentTime which is a datetime object and the timeresolution which is an integer, this method rounds up the 
        time to the nearest time resolution. Say that the time right now is 18:05 and the timeresolution is 15, the rounded
        up time will be 18:15. the rounded time returned is in the format of a date time object
        '''
        return currentTime + (datetime.datetime.min - currentTime) % datetime.timedelta(minutes = timeresolution)

    def _convert_isoweekday_to_weekday(self, isoweekday):
        if isoweekday == 1:
            return 'monday'
        if isoweekday == 2:
            return 'tuesday'
        if isoweekday == 3:
            return 'wednesday'
        if isoweekday == 4:
            return 'thursday'
        if isoweekday == 5:
            return 'friday'
        if isoweekday == 6:
            return 'saturday'
        if isoweekday == 7:
            return 'sunday'


    

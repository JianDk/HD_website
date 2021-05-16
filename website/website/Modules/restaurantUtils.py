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


    

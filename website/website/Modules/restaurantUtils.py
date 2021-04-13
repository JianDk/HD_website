from webshopRestaurant.models import Restaurant
import datetime

class RestaurantUtils:
    def __init__(self, restaurantName):
        self.restaurantModelData = Restaurant.objects.get(name=restaurantName)
        #once the restaurant is found we will change the restaurant latitude and longitude data format to float
        self.restaurantModelData.latitude = float(self.restaurantModelData.latitude)
        self.restaurantModelData.longitude = float(self.restaurantModelData.longitude)
    
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


    

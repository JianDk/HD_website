from django.test import TestCase

# Create your tests here.
import datetime
from datetime import timedelta
from website.Modules.restaurantUtils import RestaurantUtils
restaurant = RestaurantUtils(restaurantName = "Hidden Dimsum 2900")

now = datetime.datetime.now()
rounded = now + (datetime.datetime.min - now) % datetime.timedelta(minutes = 15)
print(now)
print(rounded)


def rounded_to_the_last_30th_minute_epoch():
    now = datetime.now()
    rounded = now - (now - datetime.min) % timedelta(minutes=30)
    return rounded
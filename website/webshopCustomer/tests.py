from django.test import TestCase
from website.Modules.restaurantUtils import RestaurantUtils
# Create your tests here.
import datetime
from datetime import timedelta
restaurant = RestaurantUtils(restaurantName = "Hidden Dimsum 2900")

now = datetime.datetime.now()
rounded = now + (datetime.datetime.min - now) % datetime.timedelta(minutes = 15)
print(now)
print(rounded)


def rounded_to_the_last_30th_minute_epoch():
    now = datetime.now()
    rounded = now - (now - datetime.min) % timedelta(minutes=30)
    return rounded
"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from index import views
from index.views import indexPage, hdnytorv
from webshopRestaurant.views import hd2900_webshop_Main, AddressCheckForDeliverability, ChangeItemQuantity
from webshopCustomer.views import TakeawayCheckout, totalPriceDeliveryPossible, DeliveryForm, localDeliveryCheckoutAddressCheck, Payment
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexPage.as_view(), name = 'index'),
    path('hdnytorv', hdnytorv.as_view(), name='hdnytorv'),
    path('hd2900', views.hd2900.as_view(), name='hd2900'),
    path('hd2900_takeaway_webshop', hd2900_webshop_Main.as_view()),
    path('check-address-for-deliverable', AddressCheckForDeliverability.as_view()),
    path('changeItemQuantityInBasket', ChangeItemQuantity.as_view()),
    path('isPriceAboveDeliveryLimit', totalPriceDeliveryPossible.as_view()),
    path('hdbynight', views.hdbynight.as_view(), name='hdbynight'),
    path('takeawayCheckout', TakeawayCheckout.as_view()),
    path('deliveryFormCheckout', DeliveryForm.as_view()),
    path('local_delivery_checkout_is_address_deliverable', localDeliveryCheckoutAddressCheck.as_view()),
    path('localDeliveryPayment', Payment.as_view()),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from webshopRestaurant.views import hd2900_webshop_Main, AddressCheckForDeliverability

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexPage.as_view(), name = 'index'),
    path('hdnytorv', hdnytorv.as_view(), name='hdnytorv'),
    path('hd2900', views.hd2900.as_view(), name='hd2900'),
    path('hd2900_takeaway_webshop', hd2900_webshop_Main.as_view()),
    path('check-address-for-deliverable', AddressCheckForDeliverability.as_view()),
    path('hdbynight', views.hdbynight.as_view(), name='hdbynight'),
]

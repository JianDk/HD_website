from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class hd2900_Main(View):
    def get(self, request, *args, **kwargs):
        print('worked here is it is called')
        return HttpResponse('<html><h1>hello world from webshop</h1></html>')

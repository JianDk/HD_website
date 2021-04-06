from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse

# Create your views here.
class hd2900_Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="takeawayWebshop/hd2900_webshop_index.html")


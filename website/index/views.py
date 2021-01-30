from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def hdnytorv(request):
    return render(request, template_name='hdnytorv.html')

def hd2900(request):
    return render(request, template_name = 'hd2900.html')

    

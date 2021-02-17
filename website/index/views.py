from django.shortcuts import render
from .forms import contactForm

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def hdnytorv(request):
    return render(request, template_name='hdnytorv.html')

def hd2900(request):
    print('request starts here')
    print(request)
    print('request ends here')
    form = contactForm()
    context = {"form" : form,
    "emailStatus" : "hello world"}
    return render(request, template_name = 'hd2900.html', context = context)

    

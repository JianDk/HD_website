from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def hdnytorv(request):
    print('here')
    return render(request, template_name='hdnytorv.html')
    

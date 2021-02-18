from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import contactForm

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def hdnytorv(request):
    return render(request, template_name='hdnytorv.html')

def hd2900(request):

    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Message sent')
            return redirect('/hd2900#contactField')
    else:      
        form = contactForm()
        context = {"form" : form}
        return render(request, template_name = 'hd2900.html', context = context)

    

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
            #Take the form content and send it via en email 
            senderName = form.cleaned_data['senderName']
            senderEmail = form.cleaned_data['senderEmail']
            senderPhone = form.cleaned_data['senderPhone']
            senderMessage = form.cleaned_data['senderMessage']
            ccSender = form.cleaned_data['ccSender']
            print('here is sender name')
            print(senderName)
            print('sender email')
            print(senderEmail)
            print('sender phone')
            print(senderPhone)
            print('senderMessage')
            print(senderMessage)
            print('is cc sender true')
            print(ccSender)

            messages.success(request, 'Message sent')
            return redirect('/hd2900#contactField')
    else:      
        form = contactForm()
        return render(request, template_name = 'hd2900.html', context = {"form" : form})

    

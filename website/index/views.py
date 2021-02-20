from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import contactForm
from website.Modules.emailMessage import sendEmail 

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
            
            emailObject = sendEmail(form = form, 
            sourceFrom = 'Web message from Hidden Dimsum 2900', 
            emailTo = 'kontakt@dimsum.dk')
            
            #if email was sent successful
            if emailObject.status[0]:
                messages.success(request, 'Message sent')
                return redirect('/hd2900#contactContainer')
            else:
                messages.warning(request, 'Something wrong. Contact kontakt@dimsum.dk')
                return redirect('/hd2900#contactContainer')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('/hd2900#contactContainer')
    else:      
        form = contactForm()
        return render(request, template_name = 'hd2900.html', context = {"form" : form})

    

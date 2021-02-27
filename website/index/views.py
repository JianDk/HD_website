from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import contactForm
from .forms import newsLetterForm
from website.Modules.emailMessage import sendEmail 
from website.Modules.registerEmailSubscription import registerEmail

# Create your views here.
def index(request):
    emailSignupForm = newsLetterForm(request.POST)
    if request.method == 'POST':
        if emailSignupForm.is_valid():
            emailToRegister = emailSignupForm.cleaned_data['signUpEmail']
            #Insert the email to sqlite3 data base
            regEmailObj = registerEmail()
            if regEmailObj.conn != False: #successfully connected to register email sql database
                regEmailObj.insertEmailToDatabase(emailToRegister,'www.dimsum.dk')
                messages.success(request, 'Email registered', extra_tags='emailSubscription')
            else:
                messages.warning(request, 'Something wrong, email not registered!', extra_tags='emailSubscription')
            return redirect('/#newsLetterSubmitButton')
    
    if request.method == 'GET':
        #Links in the cover section on the top part of the page
        links = list()
        links.append(('LOCATIONS', '#anchor_locations'))
        links.append(('ABOUT US', '#anchor-aboutUs'))
        links.append(('CONTACT', '#anchor-mainContact'))

        context = {'links' : links,
        'imagePath' : 'static/media/cover.jpg',
        'coverTitle1' : 'We are dimsum!',
        'coverTitle2' : 'at',
        'coverTitle3' : 'HIDDEN DIMSUM',
        'emailSignUpForm' : emailSignupForm,
        'shopTitle' : 'Hidden Dimsum',
        'addressStreet' : 'Nytorv 19',
        'addressPostcodeCity' : '1450 København K',
        'addressPhone' : '+45-33 12 88 28',
        'addressEmail' : 'kontakt@dimsum.dk',
        'addressCVR' : 'CVR: 38908901'}
        return render(request, template_name='index.html', context = context)

def hdnytorv(request):
    #cover link name and url address
    links = list()
    links.append(('Link1', 'http://www.google.com'))
    links.append(('Link2', '#'))
    links.append(('Link3', '#'))

    context = {'imagePath' : 'static/media/coverNytorv1.jpg',
    'links' : links,
    'menuImgPath' : 'static/media/hdNytorvMenu.png'}

    return render(request, template_name='hdnytorv.html', context = context)

def hd2900(request):

    if request.method == 'POST':
        form = contactForm(request.POST)
        newsletterForm = newsLetterForm(request.POST)
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
                messages.success(request, 'Message sent', extra_tags='contactSubmitStatus')
                return redirect('/hd2900#contactForm')
            else:
                messages.warning(request, 'Something wrong. Contact kontakt@dimsum.dk', extra_tags='contactSubmitStatus')
                return redirect('/hd2900#contactForm')
        elif newsletterForm.is_valid():
            emailToRegister = newsletterForm.cleaned_data['signUpEmail']
            #Insert the email to sqlite3 data base
            regEmailObj = registerEmail()
            if regEmailObj.conn != False: #successfully connected to register email sql database
                regEmailObj.insertEmailToDatabase(emailToRegister,'HiddenDimsum2900')
                messages.success(request,'Email registered', extra_tags='emailSubscription')
            else:
                messages.warning(request, 'Something wrong, email not registered!', extra_tags='emailSubscription')

            return redirect('/hd2900#newsLetterSubmitButton')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('/hd2900#contactForm')
    else:      
        form = contactForm(request.POST)
        emailSignUpForm = newsLetterForm(request.POST)
        context = {'form' : form,
        'emailSignUpForm' : emailSignUpForm,
        'menuImgPath' : 'static/media/hd2900Menu.png',
        'dayRange1' : 'Everyday',
        'timeRange1': '16:00 - 20:30',
        'dayRange2' : 'Takeaway order: 40388884',
        'shopTitle' : 'Hidden Dimsum 2900',
        'addressStreet' : 'Strandvejen 163, 2900 Hellerup',
        'addressPhone' : '+45-40 38 88 84',
        'addressEmail' : 'kontakt@dimsum.dk',
        'addressCVR' : 'CVR: 38908901',
        'instagramLink' : 'https://www.instagram.com/hiddendimsum2900/?hl=da',
        'youtubeLink' : 'https://www.youtube.com/channel/UC-ryuXvGrMK2WQHBDui2lxw',
        'facebookLink' : 'https://www.facebook.com/hiddendimsum/'
        }

        return render(request, template_name = 'hd2900.html', context = context)

    

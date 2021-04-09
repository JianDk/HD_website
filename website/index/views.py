from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.conf import settings
from .forms import contactForm
from .forms import newsLetterForm

from website.Modules.emailMessage import sendEmail 
from website.Modules.registerEmailSubscription import registerEmail
from website.Modules.recaptchaValidate import Validate


# Create your views here.
class ContextBuilder:
    def __init__(self):
        self.context = {
        'backgroundImageAlt' : None,
        'imagePath' : None,
        'navbarLogoPath' : None,
        'navbarLogoAlt' : None,
        'links' : None,
        'menuImgPath' : None,
        'aboutUsImagePath' : None,
        'aboutUsImageAlt' : None,
        'aboutUsText' : None,
        'dayRange1' : None,
        'timeRange1' : None,
        'form' : None,
        'emailSignUpForm' : None,
        'shopTitle' : None,
        'addressStreet' : None,
        'addressPhone' : None,
        'addressEmail' : 'kontakt@dimsum.dk',
        'addressCVR' : 'CVR: 38908901',
        'instagramLink' : None,
        'youtubeLink' : None,
        'facebookLink' : None}

    def Set_headerCoverImageLinks(self, linksList):
        '''
        Accepts a list of tuples containing ('Link_title', 'url')
        '''
        self.links = list()
        for linkTuple in linksList:
            self.links.append(linkTuple)

    def Set_context(self, **kwargs):
        '''
        The kwargs points to the dictionary keys in context, and the values are inserted
        '''
        for key in kwargs.keys():
            self.context[key] = kwargs[key]

    def importTextFile(self, filePath):
        with open(filePath,'r',encoding='utf-8') as fid:
            self.textString = fid.read()

class indexPage(View):
    def __init__(self, *args, **kwargs):
        self.ContextObject = ContextBuilder()
        self.ContextObject.importTextFile(str(settings.BASE_DIR) + '/static/mainAboutUs.txt')
        self.ContextObject.Set_headerCoverImageLinks(linksList = [
            ('LOCATIONS', '#anchor_locations'),
            ('ABOUT US', '#anchor-aboutUs'),
            ('CONTACT', '#anchor-mainContact')
            ]
        )

        self.emailSignupForm = newsLetterForm()

        self.ContextObject.Set_context(
        backgroundImageAlt = "A steamer of dimsum at Hidden Dimsum",
        navbarLogoPath = 'static/media/hiddendimsum_maincoverLogo.png',
        navbarLogoAlt = 'Hidden Dimsum',
        links = self.ContextObject.links,
        imagePath = 'static/media/cover.jpg', 
        aboutUsImagePath = 'static/media/aboutus2900.jpg',
        aboutUsImageAlt = 'Owner of Hidden Dimsum the siblings Wang and Mai',
        aboutUsText = self.ContextObject.textString,
        coverTitle1 = 'WE ARE DIMSUM!', 
        coverTitle2 = 'AT',
        coverTitle3 = 'HIDDEN DIMSUM', 
        instagramLink = 'https://www.instagram.com/hiddendimsum/?hl=da',
        youtubeLink = 'https://www.youtube.com/channel/UC-ryuXvGrMK2WQHBDui2lxw',
        facebookLink = 'https://www.facebook.com/hiddendimsum/',
        emailSignUpForm = self.emailSignupForm,
        shopTitle = 'Hidden Dimsum', 
        addressStreet = 'Nytorv 19', 
        addressPostcodeCity = '1450 København K',
        addressPhone = '+45-33 12 88 28')

        self.context = self.ContextObject.context

    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html', context = self.context)
    
    def post(self, request, *args, **kwargs):
        emailForm = newsLetterForm(request.POST)

        if emailForm.is_valid():
            signUpEmail = emailForm.cleaned_data['signUpEmail']
            #Insert the email to sqlite3 data base
            regEmailObj = registerEmail()
            if regEmailObj.conn != False: #successfully connected to register email sql database
                regEmailObj.insertEmailToDatabase(signUpEmail,'HiddenDimsum Nytorv')
                messages.success(request, 'Email registered', extra_tags='emailSubscription')
            else:
                messages.warning(request, 'Something wrong, email not registered!', extra_tags='emailSubscription')
            return redirect('/#newsLetterSubmitButton')
        else:
            return redirect('/')

class hdnytorv(View):
    def __init__(self, *args, **kwargs):
        self.ContextObject = ContextBuilder()
        self.ContextObject.Set_headerCoverImageLinks(linksList = [
            ('MENU', '/hdnytorv#menuHeader',),
            ('ABOUT US', '/hdnytorv#aboutUsLogo',),
            ('CONTACT', '/hdnytorv#contactForm',),
            ('BOOK TABLE', 'https://book.easytablebooking.com/book/?id=bb7ae&lang=da',)
        ])
    
    def get(self, request, *args, **kwargs):
        #get the contact form fields and news letter form fields
        self.ContextObject.importTextFile(str(settings.BASE_DIR) + '/static/aboutUsNytorv.txt')
        self.ContextObject.Set_context(imagePath ='static/media/coverNytorv.jpg',
            navbarLogoPath = 'static/media/hiddendimsum_maincoverLogo.png',
            links = self.ContextObject.links,
            menuImgPath = 'static/media/hdNytorvMenu.jpg',
            aboutUsImagePath = 'static/media/aboutus2900.jpg',
            aboutUsText = self.ContextObject.textString,
            dayRange1 = 'Closed due to COVID-19 restrictions',
            timeRange1 = 'Subscribe to our newsletter and get informed when we reopen!',
            form = contactForm(),
            emailSignUpForm = newsLetterForm(),
            shopTitle = 'Hidden Dimsum',
            addressStreet = 'Nytorv 19, 1450 København K',
            addressPhone = '+45-33 12 88 28',
            instagramLink = 'https://www.instagram.com/hiddendimsum2900/?hl=da',
            youtubeLink = 'https://www.youtube.com/channel/UC-ryuXvGrMK2WQHBDui2lxw',
            facebookLink = 'https://www.facebook.com/hiddendimsum/')
        
        self.context = self.ContextObject.context
        
        return render(request, template_name='hdnytorv.html', context = self.context)
    
    def post(self, request, *args, **kwargs):
        form = contactForm(request.POST)
        newsletterForm = newsLetterForm(request.POST)

        if form.is_valid():
            #check recaptcha 
            validate = Validate(request = request)

            if validate.result['success'] is False:
                messages.warning(request, 'Validation failed. Try again.', extra_tags='contactSubmitStatus')
                return redirect('/hdnytorv#contactForm')

            emailObject = sendEmail(form = form, 
            sourceFrom = 'Web message from Hidden Dimsum Nytorv', 
            emailTo = 'kontakt@dimsum.dk')
            messages.success(request, 'Message sent', extra_tags='contactSubmitStatus')
            return redirect('/hdnytorv#contactForm')
        
        elif newsletterForm.is_valid():
            emailToRegister = newsletterForm.cleaned_data['signUpEmail']
            #Insert the email to sqlite3 data base
            regEmailObj = registerEmail()
            if regEmailObj.conn != False: #successfully connected to register email sql database
                regEmailObj.insertEmailToDatabase(emailToRegister,'HiddenDimsum_Nytorv')
                messages.success(request,'Email registered', extra_tags='emailSubscription')
            else:
                messages.warning(request, 'Something wrong, email not registered!', extra_tags='emailSubscription')
            return redirect('/hdnytorv#newsLetterSubmitButton')

class hdbynight(View):
    def __init__(self, *args, **kwargs):
        #cover link name and url address
        self.ContextObject = ContextBuilder()
        self.ContextObject.Set_headerCoverImageLinks(linksList = [
            ('MENU', '/hdbynight#menuHeader'),
            ('ABOUT US', '/hdbynight#aboutUsLogo'),
            ('CONTACT', '/hdbynight#contactForm')])
    
    def get(self, request, *args, **kwargs):
        self.ContextObject.importTextFile(str(settings.BASE_DIR) + '/static/aboutUs2900.txt')
        self.ContextObject.Set_context(
            imagePath = 'static/media/coverByNight2.jpg',
            navbarLogoPath = 'static/media/hiddendimsum_maincoverLogo.png',
            links = self.ContextObject.links,
            menuImgPath = 'static/media/hdNytorvMenu.jpg',
            aboutUsImagePath = 'static/media/aboutus2900.jpg',
            aboutUsText = self.ContextObject.textString,
            dayRange1 = 'Closed due to COVID-19 restrictions',
            timeRange1 = 'Subscribe to our newsletter and get informed when we reopen!',
            form = contactForm(),
            emailSignUpForm = newsLetterForm(),
            shopTitle = 'Hidden Dimsum',
            addressStreet = 'Nytorv 19, 1450 København K',
            addressPhone = '+45-33 12 88 28',
            instagramLink = 'https://www.instagram.com/hiddendimsum2900/?hl=da',
            youtubeLink = 'https://www.youtube.com/channel/UC-ryuXvGrMK2WQHBDui2lxw',
            facebookLink = 'https://www.facebook.com/hiddendimsum/')

        #get the contact form fields and news letter form fields
        return render(request, template_name='hdbynight.html', context = self.ContextObject.context)

    def post(self, request, *args, **kwargs):
        form = contactForm(request.POST)
        newsletterForm = newsLetterForm(request.POST)
        if form.is_valid():
            #check recaptcha 
            validate = Validate(request = request)

            if validate.result['success'] is False:
                messages.warning(request, 'Validation failed. Try again.', extra_tags='contactSubmitStatus')
                return redirect('/hdnytorv#contactForm')

            #Take the form content and send it via en email                 
            emailObject = sendEmail(form = form,
            sourceFrom = 'Web message from Hidden Dimsum by Night', 
            emailTo = 'kontakt@dimsum.dk')
            messages.success(request, 'Message sent', extra_tags='contactSubmitStatus')
            return redirect('/hdbynight#contactForm')
        
        elif newsletterForm.is_valid():
            emailToRegister = newsletterForm.cleaned_data['signUpEmail']
            #Insert the email to sqlite3 data base
            regEmailObj = registerEmail()
            if regEmailObj.conn != False: #successfully connected to register email sql database
                regEmailObj.insertEmailToDatabase(emailToRegister,'HiddenDimsum_byNight')
                messages.success(request,'Email registered', extra_tags='emailSubscription')
            else:
                messages.warning(request, 'Something wrong, email not registered!', extra_tags='emailSubscription')

            return redirect('/hdbynight#newsLetterSubmitButton')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('/hdbynight#contactForm')

class hd2900(View):
    def __init__(self, *args, **kwargs):
        #cover link name and url address
        self.ContextObject = ContextBuilder()
        self.ContextObject.importTextFile(str(settings.BASE_DIR) + '/static/aboutUs2900.txt')
        
    def get(self, request, *args, **kwargs):
        #import about us text

        form = contactForm(request.POST)
        context = {'navbarLogoAlt' : "Hidden Dimsum 2900",
        'form' : contactForm(),
        'emailSignUpForm' : newsLetterForm(),
        'menuImgPath' : 'static/media/hd2900Menu.jpg',
        'menuAltText' : 'Hidden Dimsum 2900 menu',
        'contactSubMessage' : 'NOT for takeaway ordering, we check messages once daily',
        'aboutUsImagePath' : 'static/media/aboutus2900.jpg',
        'aboutUsImageAlt' : 'Owner of Hidden Dimsum 2900 Hellerup Mak and Mai',
        'aboutUsText' : self.ContextObject.textString,
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


    def post(self, request, *args, **kwargs):
        form = contactForm(request.POST)
        newsletterForm = newsLetterForm(request.POST)
        if form.is_valid():
            #check recaptcha 
            validate = Validate(request = request)

            if validate.result['success'] is False:
                messages.warning(request, 'Validation failed. Try again.', extra_tags='contactSubmitStatus')
                return redirect('/hd2900#contactForm')

            #Take the form content and send it via en email 
            emailObject = sendEmail(form = form, 
            sourceFrom = 'Web message from Hidden Dimsum 2900', 
            emailTo = 'kontakt@dimsum.dk')
            messages.success(request, 'Message sent', extra_tags='contactSubmitStatus')
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

        

    

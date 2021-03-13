import urllib
import json

class Validate:
    def __init__(self, request):
        #Import recaptcha secret key
        with open('static/emailCred.txt','r') as fileId:
            cred = json.load(fileId)

        #validate recaptha
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': cred['recaptchaSecretKey'],
            'response': request.POST.get('g-recaptcha-response')
            }
            
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        self.result = json.loads(response.read().decode())
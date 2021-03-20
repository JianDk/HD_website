import urllib.request
import json

class Validate:
    def __init__(self, request):
        #Import recaptcha secret key
        with open('/etc/config.json','r') as fileId:
            cred = json.load(fileId)

        #validate recaptha
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': cred['GOOGLE_RECAPTCHA_SECRET_KEY'],
            'response': request.POST.get('g-recaptcha-response')
            }
            
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        self.result = json.loads(response.read().decode())
        print('here is the result')
        print(self.result)
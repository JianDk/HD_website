from django.test import TestCase
import requests     
import json

class NETS:
    def __init__(self):
        #Import the secret key
        with open('/etc/config.json','r') as fileId:
            secretKeys = json.load(fileId)
        
        self.secretKeys = secretKeys['NETS']

    def create_order(self, **kwargs):
        data = dict()
        data['order'] = dict()
        data['order']['items'] = list()

        #Create item
        item = dict()
        item['reference'] = kwargs['reference']
        item['name'] = kwargs['name']
        item['unit'] = 'pcs'
        item['unitPrice'] = kwargs['unitPrice']
        item['taxRate'] = 0
        item['grossTotalAmount'] = kwargs['unitPrice']
        item['taxAmount'] = 0
        item['grossTotalAmount'] = kwargs['unitPrice']
        item['netTotalAmount'] = kwargs['unitPrice']

        data['order']['items'].append(item)
        data['order']['amount'] = kwargs['unitPrice']
        data['order']['currency'] = 'DKK'
        data['order']['reference'] = kwargs['paymentReference']

        data['checkout'] = dict()
        data['checkout']['charge'] = True
        data['checkout']['publicDevice'] = False
        data['checkout']['integrationType'] = 'EmbeddedCheckout'
        data['checkout']['url'] = 'http://127.0.0.1:8000/deliveryFormCheckout' #<-------------SHOULD BE CHANGED
        data['checkout']['termsUrl'] = 'http://127.0.0.1:8000/deliveryFormCheckout' #<------------SHOULD BE CHANGED
        data['checkout']['merchantHandlesConsumerData'] = True

        self.json_formatted_str = json.dumps(data, indent=4)
        return self.json_formatted_str

    def get_paymentId(self, platform, reference, name, unitPrice, paymentReference):
    
        if platform == 'test':
            secretKey = self.secretKeys['test']['secretKey']
            url = "https://test.api.dibspayment.eu/v1/payments/"

        if platform == 'production':
            secretKey = self.secretKeys['production']['secretKey']
            url = 'api.dibspayment.eu/v1/payments/'
        
        #Insert secretKey in header
        headers = {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : secretKey}

        #Data for post body
        data = self.create_order(reference = reference, name = name, quantity = 1, unitPrice = unitPrice, paymentReference = paymentReference )
        
        #Do the actual post
        print(url)
        print(headers)
        print(data)


        resp = self._requestPost(url = url, headers = headers, data = data)
        print('here is the response from post')
        print(resp.status_code)
    
    def _requestPost(self, url, data, headers):
        with requests.Session() as session:
            resp = session.post(url = url, headers = headers, data = data)

        return resp
 

payment = NETS()
payment.get_paymentId(platform = 'test', 
name = 'Hidden Dimsum 2900', 
unitPrice=10000, 
paymentReference='testRef', 
reference='product reference')
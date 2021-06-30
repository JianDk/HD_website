from django.test import TestCase
import requests     
import json

class NETS:
    def __init__(self):
        '''
        Upon initiation the secret key is loaded
        '''
        #Import the secret key
        with open('/etc/config.json','r') as fileId:
            secretKeys = json.load(fileId)
        
        self.secretKeys = secretKeys['NETS']

    def create_order(self, **kwargs):
        ''''
        create_order takes in the following kwargs:
        reference : a string containing payment reference. E.g. order id.
        name: a string containing the product name
        unitPrice : integer. Total price to charge. Note the last two digits are interpreted as decimal after comma. E.g. 100.50 should be written as 10050
        paymentReference: a string containing the reference of the payment

        MUST BE IMPLEMENTED FURTHER 
        url and terms url
        '''
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
        data['checkout']['url'] = 'http://127.0.0.1:8000/localDeliveryPayment' #<-------------SHOULD BE CHANGED
        data['checkout']['termsUrl'] = 'http://127.0.0.1:8000/localDeliveryPayment' #<------------SHOULD BE CHANGED
        data['checkout']['merchantHandlesConsumerData'] = True

        self.json_formatted_str = json.dumps(data, indent=4)
        return self.json_formatted_str

    def get_paymentId(self, platform, reference, name, unitPrice, paymentReference):
    
        if platform == 'test':
            secretKey = self.secretKeys['test']['secretKey']
            url = "https://test.api.dibspayment.eu/v1/payments/"

        if platform == 'production':
            secretKey = self.secretKeys['production']['secretKey']
            url = 'https://api.dibspayment.eu/v1/payments/'
        
        #Insert secretKey in header
        headers = {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : secretKey}

        #Data for post body
        data = self.create_order(reference = reference, name = name, quantity = 1, unitPrice = unitPrice, paymentReference = paymentReference )
        
        #Do the actual post
        resp = self._requestPost(url = url, headers = headers, data = data)
        return resp
    
    def getCheckoutKey(self, platform):
        return self.secretKeys[platform]['checkoutKey']

    def _requestPost(self, url, data, headers):
        with requests.Session() as session:
            resp = session.post(url = url, headers = headers, data = data)
        return resp
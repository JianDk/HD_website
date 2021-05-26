from django.test import TestCase
import requests
testPaymentIdUrl = "https://test.api.dibspayment.eu/v1/payments/"
test_secretyKey = "c8210f169b344cf58e3508f50fe02494"

def create_order(**kwargs):
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
    


    print(item)

create_order(reference = "reference no", 
name = "product name", 
quantity = 1,
unitPrice = 10000)
#with requests.Session() as session:
 #   resp = session.post(url = testPaymentIdUrl)
#print(resp.status_code)
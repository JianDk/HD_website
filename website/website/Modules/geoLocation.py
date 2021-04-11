import requests
class GeoLocationUtils:
    def __init__(self,api_key):
        self.googleGeoCoding_apikey = api_key
        self._geocodeDict()

    def _geocodeDict(self):
        '''
            Used by addressToGeoCoordinates for returning a dictionary with predefined keys
        '''
        self.geoDict = dict()
        self.geoDict['httpRequestStatusCode'] = None
        self.geoDict['geocode_status'] = None
        self.geoDict['latitude'] = None
        self.geoDict['longitude'] = None
        self.geoDict['streetName'] = None
        self.geoDict['houseNumber'] = None
        self.geoDict['postCode'] = None
        self.geoDict['city'] = None
        self.geoDict['country'] = None
        self.geoDict['address'] = None

    def addressToGeoCoordinates(self, address):
        '''
        Given the google geocoding api key and the address, the method performs a request to Google's API and returns
        the corresponding latitude and longitude data in a tuple.
        '''
        url = f'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
        'address': address,
        'sensor': 'false',
        'region': 'dk',
        'key' : self.googleGeoCoding_apikey}

        #post address to Google's geocoding to receive the address
        with requests.Session() as session:
            req = session.get(url, params=params)

        if req.status_code != 200:
            self.geoDict['httpRequestStatusCode'] = req.status_code
        else:
            data = req.json()
            self.geoDict['httpRequestStatusCode'] = 200
            self.geoDict['geocode_status'] = data['status']
            self.geoDict['laitude'] = data['results'][0]['geometry']['location']['lat']
            self.geoDict['longitude'] = data['results'][0]['geometry']['location']['lng'] 
            self.geoDict['formatted_address'] = data['results'][0]['formatted_address']
            
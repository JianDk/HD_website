import requests
import math

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
            self.geoDict['latitude'] = data['results'][0]['geometry']['location']['lat']
            self.geoDict['longitude'] = data['results'][0]['geometry']['location']['lng'] 
            self.geoDict['formatted_address'] = data['results'][0]['formatted_address']
    
    def distanceBetweenCoordinates(self, coordinate1, coordinate2):
        '''
        Given the coordinate1 and coordinate2 each in a tuple consisting of (latitude, longitude)
        the method calculates the distance between the two points

        Reference for distance calculation
        https://community.esri.com/t5/coordinate-reference-systems/distance-on-a-sphere-the-haversine-formula/ba-p/902128
        '''
        # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
        lon1, lat1 = coordinate1
        lon2, lat2 = coordinate2

        R = 6371000  # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        meters = R * c  # output distance in meters
        km = meters / 1000.0  # output distance in kilometers

        return km

#The above class should be changed to the one below as the above one was using Google's API service
class GeoLocationTools:
    def distanceBetweenCoordinates(self, coordinate1, coordinate2):
        '''
        Given the coordinate1 and coordinate2 each in a tuple consisting of (longitude, latitude)
        the method calculates the distance between the two points

        Reference for distance calculation
        https://community.esri.com/t5/coordinate-reference-systems/distance-on-a-sphere-the-haversine-formula/ba-p/902128
        '''
        # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
        lon1, lat1 = coordinate1
        lon2, lat2 = coordinate2

        R = 6371000  # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        meters = R * c  # output distance in meters
        km = meters / 1000.0  # output distance in kilometers

        return km
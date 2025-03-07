import requests
import pprint 
from geopy import geocoders
from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim 

import CONSTANTS

def get_lat_long(location_name): #get coordinates from name
    geolocator = Nominatim(user_agent="geopy_example",timeout=10)
    location = geolocator.geocode(location_name)

    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return None

location_name = input("Enter a location name: ")
result = get_lat_long(location_name)

if result:
    latitude, longitude = result
    
else:
    print(f"Could not find coordinates for {location_name}") 

def make_url(): #make url using coordinates

#convert to string
    lat = str(latitude)
    long = str(longitude)

    url = 'https://api.tomorrow.io/v4/weather/forecast?location='+lat+','+long+'&apikey='+CONSTANTS.TOMORROWWEATHER_API_KEY
    return url

def get_posts():
    # Define the API endpoint URL
    url = make_url()
    #url = 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey='+CONSTANTS.OPENWEATHER_API_KEY
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)
        posts = response.json()
        print(type(posts))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(posts)
            #return print(soup.prettify())
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
  
    # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


output = get_posts()


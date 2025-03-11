import requests
import pprint 
from geopy import geocoders
from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim 
import pandas
import json

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
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)
        posts = response.json()
        # print(type(posts))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(posts)
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
  
    # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


output = get_posts()
# Access the current temperature (first entry in the minutely timeline)
current_data = output['timelines']['minutely'][0]
current_temp = current_data['values']['temperature']

print(f"Current temperature: {current_temp}°C")

def get_weather_description(code):
    weather_codes = {
        1000: "Clear, Sunny",
        1100: "Mostly Clear",
        1101: "Partly Cloudy",
        1102: "Mostly Cloudy",
        1001: "Cloudy",
        4000: "Drizzle",
        4001: "Rain",
        # Add more codes as needed
    }
    return weather_codes.get(code, f"Unknown ({code})")

def print_weather_data(data):
    # Get current weather
    current_data = data['timelines']['minutely'][0]
    current_values = current_data['values']
    
    print("===== CURRENT WEATHER =====")
    print(f"Temperature: {current_values['temperature']}°C")
    print(f"Humidity: {current_values['humidity']}%")
    print(f"Wind Speed: {current_values['windSpeed']} km/h")
    print(f"Weather: {get_weather_description(current_values['weatherCode'])}")
    
    # Get hourly forecast
    print("\n===== 4-HOUR FORECAST =====")
    hourly_data = data['timelines']['hourly'][:5]  # First 5 entries
    
    for i, hour_data in enumerate(hourly_data):
        if i == 0:  # Skip current hour
            continue
            
        time = hour_data['time']
        values = hour_data['values']
        
        print(f"\nTime: {time}")
        print(f"Temperature: {values['temperature']}°C")
        print(f"Humidity: {values['humidity']}%")
        print(f"Weather: {get_weather_description(values['weatherCode'])}")

# Use the function
print_weather_data(output)



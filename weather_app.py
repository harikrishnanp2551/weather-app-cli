import requests
import pprint 

import CONSTANTS

def make_url():
    lat = input('Enter the latitude:\n')
    long = input('Enter the longitude:\n')

    url = 'https://api.tomorrow.io/v4/weather/forecast?location='+lat+','+long+'&apikey='+CONSTANTS.OPENWEATHER_API_KEY
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

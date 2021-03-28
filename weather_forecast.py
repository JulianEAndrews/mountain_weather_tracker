import requests
from datetime import datetime
import pandas as pd
import api

#To-do List

#In Progress, ongoing: Update user input functionality to prevent errors or crashes.
#In Progress: Build classes to house functions to call each different website.

#Compare data from multiple websites and create one output file with cross-referenced data points
#Expand csv functionality
#Make compatible with rasppi (query at 'x' time, update frequency, etc...)
#Gather string data from esac. Possibly too complicated. Need either more html experience or a way to scrape webpage data directly.

#Completed: Update function to take in any lat-lon.
#Completed: Create function to print important data (maybe daily hi/low, wind/wind direction, clouds, etc...) to .csv or .xls



API_OWM = api.API_KEY_OWM
API_WINDY = api.API_KEY_WINDY

def city_weather():
    while True:
        try:
            city = str(input('City Name: ')).casefold().strip()
            state = str(input('State Code: ')).casefold().strip()
            country = str(input('Country Code: ')).casefold().strip()
            break
        except KeyboardInterrupt:
            break

    web_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city_url = f'q={city}'
    state_url = f',{state}'
    country_url = f',{country}'
    api_url = f'&appid={API_OWM}'

    units_url = units()

    url = web_url + city_url + state_url + country_url + units_url + api_url
    print(url)

    check_data(url)
    main()

def lat_long_weather():
    while True:
        try:
            lat = float(input('Enter Latitude ("xx.xx"): '))
            lat = str(lat)
            lon = float(input('Enter Longitude ("xxx.xx"): '))
            lon = str(lon)
            #lat = str(37.65)
            #lon = str(-118.97)
            break
        except KeyboardInterrupt:
            break
        except:
            pass

    web_url = 'http://api.openweathermap.org/data/2.5/weather?'
    lat_url = f'&lat={lat}'
    lon_url = f'&lon={lon}'

    units_url = units()
    api_url = f'&appid={API_OWM}'

    url = web_url + lat_url + lon_url + units_url + api_url
    print(url)

    check_data(url)
    main()

def units():
    print('Please select your preferred units. Defaults to metric:')
    while True:
        try:
            units = str(input('Standard/kelvin (s), Metric (m), or Imperial (i): ')).casefold().strip()
            if units == 's':
                units = 'standard'
            elif units == 'm':
                units = 'metric'
            elif units == 'i':
                units = "imperial"
            else:
                units = 'metric'
            units_address = f'&units={units}'
        except KeyboardInterrupt:
            break
        return units_address

def check_data(url):
    json_data: dict = requests.get(url).json()

    #print keys
    #print(*json_data)

    utc_to_date(json_data)

    for key,value in json_data.items():
       print(key, value)

       #Check if value is a list or dictionary
        #if isinstance(item, dict):
            #...
        #elif isinstance(item, list):
            #...

    make_csv(json_data)

def make_csv(json_data):
    df = pd.json_normalize(json_data)
    transpose_df = df.T
    transpose_df.to_csv('Weather.csv')

#The manual way. icky... Works for forecast data only. Check structure of json data.
#def call_data(url):
#    print(url)

#    json_data = requests.get(url).json()

#    utc_to_date(json_data)

#    print(json_data)

#    #lat/lon data
#    coord_lon = json_data['coord']['lon']
#    coord_lat = json_data['coord']['lat']
#    print(coord_lat)
#    print(coord_lon)


    #for forecast data
    #temp = json_data['list'][0]['main']['temp']
    #sky = json_data['list'][0]['weather'][0]['main']

    #print(sky)
    #print(temp)



def utc_to_date(json_data):
    #timestamp = json_data['dt']
    #dt_object = datetime.fromtimestamp(timestamp)

    json_data['dt'] = datetime.fromtimestamp(json_data['dt'])
    print(json_data['dt'])

#currently only working for forecast data, not weather data
#def utc_to_date(json_data):
#    timestamp = json_data['list'][0]['dt']
#    dt_object = datetime.fromtimestamp(timestamp)
#    print(dt_object)



#-----------------------------------------------Program UI-----------------------------------------------#


def main():
    print("---Weather Forecast---")
    while True:
        try:
            choice = str(input("Choose forecast location. Lat/Long (LL) or City, State, Country (CSC). Press 'q' to exit: " )).casefold().strip()
            if choice == 'll':
                lat_long_weather()
                break
            elif choice == 'csc':
                city_weather()
                break
            elif choice == 'q':
                exit()
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
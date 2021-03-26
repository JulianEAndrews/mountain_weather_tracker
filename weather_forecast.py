import requests
from datetime import datetime
import pandas as pd
import api

#To-do List
#Completed: Update function to take in any lat-lon.

#In Progress: Update user input functionality to prevent errors or crashes.
#In Progress: Create function to print important data (maybe daily hi/low, wind/wind direction, clouds, etc...) to .csv or .xls

#Make compatible with rasppi (query at 'x' time, update frequency, etc...)
#Compare data from multiple websites and create one output file with cross-referenced data points
#Gather string data from esac


api = api.API_KEY

def units():
    print('Please select your preferred units:')
    units = str(input('Standard/kelvin (s), Metric (m), or Imperial (i): '))
    if units == 's':
        units = 'standard'
    elif units == 'm':
        units = 'metric'
    elif units == 'i':
        units = "imperial"
    else:
        units = 'imperial'
    units_address = '&units=' + units
    return units_address

def city_weather():
    city = str(input('City Name: '))
    state = str(input('State Code: '))
    country = str(input('Country Code: '))

    web_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city_url = f'q={city}'
    state_url = f',{state}'
    country_url = f',{country}'
    api_url = f'&appid={api}'

    units_url = units()



    url = web_url + city_url + state_url + country_url + units_url + api_url

    check_data(url)
    #call_data(url)

def lat_long_weather():
    lat = str(input('Enter Latitude: '))
    lon = str(input('Enter Longitude: '))
    #lat = str(37.65)
    #lon = str(-118.97)

    web_url = 'http://api.openweathermap.org/data/2.5/weather?'
    lat_url = f'&lat={lat}'
    lon_url = f'&lon={lon}'

    units_url = units()
    api_url = f'&appid={api}'

    url = web_url + lat_url + lon_url + units_url + api_url
    check_data(url)

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

#The manual way. icky...
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

#print("---Weather Forecast---")
#while True:
#    choice = str(input("Choose forecast location. Lat/Long (LL) or City, State, Country (CSC): " )).casefold()
#    if choice == 'll':
#        lat_long_weather()
#        break
#    elif choice == 'csc':
#        city_weather()
#        break
#    elif choice == 'q':
#        break

def main():
    print("---Weather Forecast---")
    while True:
        try:
            choice = str(input("Choose forecast location. Lat/Long (LL) or City, State, Country (CSC): " )).casefold()
            if choice == 'll':
                lat_long_weather()
                break
            elif choice == 'csc':
                city_weather()
                break
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
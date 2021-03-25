import requests
from datetime import datetime

#Update function to take in any lat-lon.
#Create function to print important data (maybe daily hi/low, wind/wind direction, clouds, etc...) to .csv or .xls
#Make compatible with rasppi (query at 'x' time, update frequency, etc...)
#Compare data from multiple websites and create one output file with cross-referenced data points
#Gather string data from esac

api = '7be72a293f9455cbf0f2099277ca32aa'

def units():
    print("Please select your preferred units:")
    units = str(input("Standard/kelvin (s), Metric (m), or Imperial (i): "))
    if units == "s":
        units = "standard"
    elif units == "m":
        units = "metric"
    elif units == "i":
        units = "imperial"
    else:
        units = "imperial"
    units_address = "&units=" + units
    return units_address

def city_weather():
    city = str(input("City Name: "))
    state = str(input("State Code: "))
    country = str(input("Country Code: "))

    website_address = 'http://api.openweathermap.org/data/2.5/forecast?'
    city_address = 'q=' + city
    state_address = ',' + state
    country_address = ',' + country
    api_address = '&appid=' + api

    units_address = units()

    url = website_address + city_address + state_address + country_address + units_address + api_address
    call_data(url)

def lat_long_weather():
    # api = str(input("Enter API Key: "))
    lat = str(input("Enter Latitude: "))
    lon = str(input("Enter Longitude: "))
    #lat = str(37.65)
    #lon = str(-118.97)

    api_address = 'http://api.openweathermap.org/data/2.5/forecast?appid=' + api
    lat_address = '&lat=' + lat
    lon_address = '&lon=' + lon

    units_address = units()

    url = api_address + lat_address + lon_address + units_address
    call_data(url)

def call_data(url):
    #How do I get this function to take url var as input?
    print(url)
    json_data = requests.get(url).json()

    utc_to_date(json_data)

    #print(json_data)
    temp = json_data['list'][0]['main']['temp']
    sky = json_data['list'][0]['weather'][0]['main']

    print(sky)
    print(temp)

def utc_to_date(json_data):
    timestamp = json_data['list'][0]['dt']
    dt_object = datetime.fromtimestamp(timestamp)
    print(dt_object)



#-----------------------------------------------Program UI-----------------------------------------------#


print("---Weather Forecast---")
choice = input("Choose forecast location. Lat/Long (LL) or City, State, Country (CSC): " )

if choice == "LL":
    lat_long_weather()
elif choice == "CSC":
    city_weather()
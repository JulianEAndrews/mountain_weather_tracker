import requests

#Update function to take in any lat-lon.
#Create function to print important data (maybe daily hi/low, wind/wind direction, clouds, etc...) to .csv or .xls
#Make compatible with rasppi (query at 'x' time, update frequency, etc...)
#Compare data from multiple websites and create one output file with cross-referenced data points
#Gather string data from esac


def grab_location_data():
    # api = str(input("Enter API Key: "))
    # lat = str(input("Enter Latitude: "))
    # lon = str(input("Enter Longitude: "))
    api = '7be72a293f9455cbf0f2099277ca32aa'
    lat = str(37.65)
    lon = str(-118.97)

    api_address = 'http://api.openweathermap.org/data/2.5/forecast?appid=' + api
    lat_address = '&lat=' + lat
    lon_address = '&lon=' + lon
    url = api_address + lat_address + lon_address

    print(url)

    json_data = requests.get(url).json()
    formatted_data = json_data['list'][0]['weather'][0]['main']

    print(formatted_data)

grab_location_data()
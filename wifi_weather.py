# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

from sys import implementation
from os import uname
from pydos_wifi import Pydos_wifi

def wifi_weather():

    _URL = "https://api.weather.gov/gridpoints/BOX/70,76/forecast"
    headers = {"user-agent": "RetiredWizard@"+implementation.name.lower()+uname()[2]}

    try:
        _scrWidth = int(envVars.get('_scrWidth',80))
    except:
        _scrWidth = 80

    # Get wifi details and more from a settings.toml file
    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    print("Connecting to %s" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))

    if Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')):
        print("Connected to %s!" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))
    else:
        print("Problem connecting to  %s!" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))
    print("My IP address is", Pydos_wifi.ipaddress)
    print("Fetching text from %s" % _URL)

    response = Pydos_wifi.get(_URL,headers)

    response_window = []
    for i in range(8):
        try:
            response_window.append(Pydos_wifi.next(256))
        except:
            break

    response.close()
    forecast = (b''.join(response_window))[0:1800].decode('utf-8')

    print("\nText Response:")
    print("-" * _scrWidth)
    for pline in [forecast[i:i+_scrWidth] for i in range(0, len(forecast), _scrWidth)]:
        print(pline)
    print("-" * _scrWidth)
    del forecast
    del response_window

    print("Fetching JSON data from %s" % _URL)
    
    response = Pydos_wifi.get(_URL,headers,True)
    json_response = Pydos_wifi.json()

    print("-" * _scrWidth)
    print("JSON Response: ")
    for prop in json_response['properties']:
        if prop != 'periods':
            print(prop,":",json_response['properties'][prop])
    print()
    print("-" * _scrWidth)
    print()
    for forecaststruct in json_response['properties']['periods']:
        print(forecaststruct['name'])
        print()
        forecast = forecaststruct['detailedForecast']
        nLines = int(len(forecast)/_scrWidth)
        if len(forecast) != nLines*_scrWidth:
            nLines += 1
        for i in range(nLines):
            print(forecast[i*_scrWidth:min(((i+1)*_scrWidth)-1,len(forecast))])
        print("\n")
    print()
    print("-" * _scrWidth)
    print()
    print(json_response['properties']['periods'][0]['name'])
    print()
    forecast = json_response['properties']['periods'][0]['detailedForecast']
    nLines = int(len(forecast)/_scrWidth)
    if len(forecast) != nLines*_scrWidth:
        nLines += 1
    for i in range(nLines):
        print(forecast[i*_scrWidth:min(((i+1)*_scrWidth)-1,len(forecast))])

    Pydos_wifi.close()
    del forecast
    del json_response
    
if __name__ == "PyDOS":
    wifi_weather()
else:
    print("Enter 'wifi_weather.wifi_weather()' in the REPL or PEXEC command to run.")
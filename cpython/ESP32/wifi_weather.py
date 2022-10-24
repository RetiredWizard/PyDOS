# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

# adafruit_requests usage with a CircuitPython socket
# this has been tested with Adafruit Metro ESP32-S2 Express

import ssl
import wifi
import socketpool
from os import getenv

import adafruit_requests as requests

def wifi_weather():

    try:
        _scrWidth = int(envVars.get('_scrWidth',80))
    except:
        _scrWidth = 80

    # Get wifi details and more from a .env file
    if getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in .env, please add them there by using setenv.py!")

    print("Connecting to %s" % getenv('CIRCUITPY_WIFI_SSID'))
    wifi.radio.connect(getenv('CIRCUITPY_WIFI_SSID'), getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to %s!" % getenv('CIRCUITPY_WIFI_SSID'))
    print("My IP address is", wifi.radio.ipv4_address)

    socket = socketpool.SocketPool(wifi.radio)
    https = requests.Session(socket, ssl.create_default_context())

    _URL = "https://api.weather.gov/gridpoints/BOX/70,76/forecast"
    headers = {"user-agent": "RetiredWizard@circuitpython/7.1.0b0"}

    print("Fetching text from %s" % _URL)
    response = https.get(_URL,headers=headers)

    response_window = []
    for _ in range(8):
        response_window.append(next(iter(response.iter_content(chunk_size=256))))

    response.close()

    forecast = (b''.join(response_window))[0:1800].decode()

    print("\nText Response:")
    print("-" * _scrWidth)
    for pline in [forecast[i:i+_scrWidth] for i in range(0, len(forecast), _scrWidth)]:
        print(pline)
    print("-" * _scrWidth)

    print("Fetching JSON data from %s" % _URL)
    response = https.get(_URL,headers=headers)
    print("-" * _scrWidth)

    print("JSON Response: ")
    for prop in response.json()['properties']:
        if prop != 'periods':
            print(prop,":",response.json()['properties'][prop])
    print()
    print("-" * _scrWidth)
    print()
    for forecaststruct in response.json()['properties']['periods']:
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
    print(response.json()['properties']['periods'][0]['name'])
    print()
    forecast = response.json()['properties']['periods'][0]['detailedForecast']
    nLines = int(len(forecast)/_scrWidth)
    if len(forecast) != nLines*_scrWidth:
        nLines += 1
    for i in range(nLines):
        print(forecast[i*_scrWidth:min(((i+1)*_scrWidth)-1,len(forecast))])

    https._free_sockets()
    response.close()
    del response
    del response_window
    del forecast
    del socket
    del https

if __name__ == "PyDOS":
    wifi_weather()
else:
    print("Enter 'wifi_weather.wifi_weather()' in the REPL or PEXEC command to run.")
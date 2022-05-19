# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

# adafruit_requests usage with a CircuitPython socket
# this has been tested with Adafruit Metro ESP32-S2 Express

import ssl
import wifi
import socketpool

import adafruit_requests as requests


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

TEXT_URL = "https://api.weather.gov/gridpoints/BOX/70,76/forecast"
JSON_GET_URL = "https://api.weather.gov/gridpoints/BOX/70,76/forecast"
headers = {"user-agent": "RetiredWizard@circuitpython/7.1.0b0"}

print("Fetching text from %s" % TEXT_URL)
response = https.get(TEXT_URL,headers=headers)
print("-" * 40)
print("Text Response: ", response.text)
print("-" * 40)
response.close()

print("Fetching JSON data from %s" % JSON_GET_URL)
response = https.get(JSON_GET_URL,headers=headers)
print("-" * 40)

print("JSON Response: ", response.json())
print("-" * 40)
print()
print(response.json()['properties']['periods'][0]['detailedForecast'])

https._free_sockets()

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

TEXT_URL = "https://money.cnn.com/data/markets"
headers = {"user-agent": "RetiredWizard@circuitpython/7.1.0b0"}

print("Fetching text from %s" % TEXT_URL)
response = https.get(TEXT_URL)
print("-" * 40)
print("Text Response: ", response.text[0:800])
print("-" * 40)
response.close()
print()
nasdaq = response.text.find('data-ticker-name="Nasdaq"')
pct = response.text[nasdaq:].find('%')
pctst = response.text[nasdaq+35:].find('>')
pctend = response.text[nasdaq+35:].find('<')-1
print("Nasdaq: ",response.text[nasdaq+36+pctst:nasdaq+36+pctend])

https._free_sockets()

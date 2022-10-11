# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

# adafruit_requests usage with a CircuitPython socket
# this has been tested with Adafruit Metro ESP32-S2 Express

import ssl
import wifi
import socketpool
from os import getenv

import adafruit_requests as requests

def wifi_finance():

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

    #TEXT_URL = "https://money.cnn.com/data/markets"
    TEXT_URL = "https://finance.yahoo.com/quote/%5EIXIC"
    headers = {"user-agent": "RetiredWizard@circuitpython/8.0.0A1"}

    print("Fetching text from %s" % TEXT_URL)
    response = https.get(TEXT_URL)
    response_window = []
    for _ in range(4):
        response_window.append(next(iter(response.iter_content(chunk_size=256))))

    sample_resp = (b''.join(response_window))[0:800].decode()

    print("\nText Response:")
    print("-" * _scrWidth)
    for pline in [sample_resp[i:i+_scrWidth] for i in range(0, len(sample_resp), _scrWidth)]:
        print(pline)
    print("-" * _scrWidth)

    print()
    #nasdaq = response.text.find('data-ticker-name="Nasdaq"')
    #pct = response.text[nasdaq:].find('%')
    #pctst = response.text[nasdaq+35:].find('>')
    #pctend = response.text[nasdaq+35:].find('<')-1

    nasdaq = str(b''.join(response_window)).find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')
    while nasdaq == -1:
        for i in range(3):
            response_window[i] = response_window[i+1]
        response_window[3] = next(iter(response.iter_content(chunk_size=256)))

        nasdaq = str(b''.join(response_window)).find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')

    for _ in range(4):
        response_window.append(next(iter(response.iter_content(chunk_size=256))))
    response.close()

    found_window = str(b''.join(response_window))
    nasdaq = found_window.find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')

    #nasdaq = response.text.find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')
    pct = found_window[nasdaq:].find('%)')
    pctst = found_window[nasdaq+pct-15:].find('>')
    pctend = found_window[nasdaq+pct:].find('<')


    #print("Nasdaq: ",response.text[nasdaq+36+pctst:nasdaq+36+pctend])
    print("Nasdaq: ",found_window[nasdaq+pct-14+pctst:nasdaq+pct+pctend])
    print()

    https._free_sockets()
    del response
    del response_window
    del found_window
    del socket
    del https

if __name__ == "PyDOS":
    wifi_finance()
else:
    print("Enter 'wifi_finance.wifi_finance()' in the REPL or PEXEC command to run.")
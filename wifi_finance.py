# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

from sys import implementation
from os import uname
from pydos_wifi import Pydos_wifi

def wifi_finance():
    try:
        _scrWidth = int(envVars.get('_scrWidth',80))
    except:
        _scrWidth = 80

    # Get wifi details and more from a .env file
    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    print("Connecting to %s" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))

    Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD'))

    print("My IP address is", Pydos_wifi.ipaddress)

    #TEXT_URL = "https://money.cnn.com/data/markets"
    TEXT_URL = "https://finance.yahoo.com/quote/%5EIXIC"
    HOST = "finance.yahoo.com"
    PORT = 443
    headers = {"user-agent": "RetiredWizard@"+implementation.name.lower()+uname()[2]}

    print("Fetching text from %s" % TEXT_URL)
    response = Pydos_wifi.get(TEXT_URL)
    response_window = []
    for _ in range(4):
        response_window.append(Pydos_wifi.next(256))

    sample_resp = (b''.join(response_window))[0:800].decode().replace('\n','').replace('\r','')

    print("\nText Response:")
    print("-" * _scrWidth)
    for pline in [sample_resp[i:i+_scrWidth] for i in range(0, len(sample_resp), _scrWidth)]:
        print(pline)
    print("-" * _scrWidth)

    nasdaq = str(b''.join(response_window)).find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')
    iKount = 0
    while nasdaq == -1 and iKount<800:
        iKount +=1
        if iKount % 10 == 0:
            print(".",end="")
        for i in range(3):
            response_window[i] = response_window[i+1]
        try:
            response_window[3] = Pydos_wifi.next(256)
        except:
            for i in [3,2,1]:
                response_window[i+1] = response_window[i]

        nasdaq = str(b''.join(response_window)).find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')
    print("*")

    for _ in range(2):
        response_window.append(Pydos_wifi.next(256))

    found_window = str(b''.join(response_window))
    nasdaq = found_window.find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')

    pct = found_window[nasdaq:].find('%)')
    pctst = found_window[nasdaq+pct-15:].find('>')
    pctend = found_window[nasdaq+pct:].find('<')

    if nasdaq != -1:
        print("Nasdaq: %s\n" % found_window[nasdaq+pct-14+pctst:nasdaq+pct+pctend])
    else:
        print("Nasdaq symbol not found\n")

    Pydos_wifi.close()
    del response_window
    del found_window

if __name__ == "PyDOS":
    wifi_finance()
else:
    print("Enter 'wifi_finance.wifi_finance()' in the REPL or PEXEC command to run.")
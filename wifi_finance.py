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

    if not Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')):
        raise Exception("Unable to connect to WiFi!")

    print("My IP address is", Pydos_wifi.ipaddress)

    #TEXT_URL = "https://money.cnn.com/data/markets"
    #TEXT_URL = "https://finance.yahoo.com/quote/%5EIXIC"
    #search_string = 'data-symbol="^IXIC" data-field="regularMarketChangePercent"'
    #TEXT_URL = "https://finance.yahoo.com/lookup"
    #search_string = 'data-symbol="^IXIC" data-field="regularMarketChangePercent"'
    #TEXT_URL = "https://www.moneycontrol.com/us-markets"
    #search_string = '<!-- -->Nasdaq<!-- -->'

    TEXT_URL = "https://www.google.com/search?q=nasdaq+price&oq=nasdaq+price++"
    search_string = 'Nasdaq Inc'

    #headers = {"user-agent": "RetiredWizard@"+implementation.name.lower()+uname()[2]}

    print("Fetching text from %s" % TEXT_URL)
    response = Pydos_wifi.get(TEXT_URL)
    response_window = []
    for _ in range(4):
        tmp = Pydos_wifi.next(256)
        response_window.append(tmp)
        if len(tmp) != 256:
            break

    try:
        sample_resp = (b''.join(response_window))[0:800].decode().replace('\n','').replace('\r','')
    except:
        sample_resp = (b''.join(response_window))[0:800].replace(b'\n',b'').replace(b'\r',b'')

    print("\nText Response:")
    print("-" * _scrWidth)
    for pline in [sample_resp[i:i+_scrWidth] for i in range(0, len(sample_resp), _scrWidth)]:
        print(pline)
    print("-" * _scrWidth)

    nasdaq = str(b''.join(response_window)).find(search_string)
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
            iKount=800

        nasdaq = str(b''.join(response_window)).find(search_string)
    print("*")

    if iKount < 800:
        for _ in range(2):
            response_window.append(Pydos_wifi.next(256))

    found_window = str(b''.join(response_window))
    nasdaq = found_window.find(search_string)

    pct = found_window[nasdaq:].find('%)')
    pctst = found_window[nasdaq+pct-17:].find('">')+2
    pctend = found_window[nasdaq+pct:].find('<')
    #print("Debug: %s\n" % found_window[nasdaq:nasdaq+pct+pctend])

    if nasdaq != -1:
        print(f'Nasdaq: {found_window[nasdaq+pct-17+pctst:nasdaq+pct+pctend].replace("<","")}\n')
    else:
        print("Nasdaq symbol not found\n")

    Pydos_wifi.close()
    del response_window
    del found_window

if __name__ == "PyDOS":
    wifi_finance()
else:
    print("Enter 'wifi_finance.wifi_finance()' in the REPL or PEXEC command to run.")
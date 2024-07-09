# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

from sys import implementation
from os import uname
from pydos_wifi import Pydos_wifi

def wifi_finance(symbol):
    try:
        _scrWidth = int(envVars.get('_scrWidth',80))
    except:
        _scrWidth = 80

    if not symbol:
        symbol = "IXIC"
    else:
        symbol = symbol.upper()
    prt_sym = symbol
    srch_sym = symbol

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

    TEXT_URL = f"https://www.google.com/search?q={symbol.replace('&','%26')}+stock+price"
    search_string = symbol

    #headers = {"user-agent": "RetiredWizard@"+implementation.name.lower()+uname()[2]}

    print("Fetching text from %s" % TEXT_URL)
    response = Pydos_wifi.get(TEXT_URL)
    response_window = []
    for _ in range(4):
        response_window.append(Pydos_wifi.next(256))
        if len(response_window[-1]) != 256:
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

    print("Identifying symbol",end="")
    name_loc = -1
    iKount = 0
    while name_loc == -1 and iKount<800:
        iKount +=1
        if iKount % 10 == 0:
            print(".",end="")

        found_window = str(b''.join(response_window))

        name_loc = found_window.find(' Inc. is')
        if name_loc == -1:
            name_loc = found_window.find(' Inc., commonly')
        if name_loc == -1:
            name_loc = found_window.find(' is a stock market ')
        if name_loc != -1:
            if found_window[:name_loc].rfind('or simply the ') != -1:
                srch_sym = found_window[found_window[:name_loc].rfind('or simply the ')+14:name_loc]
            elif found_window[:name_loc].rfind('>') != -1:
                srch_sym = found_window[found_window[:name_loc].rfind('>')+1:name_loc]
            srch_sym = srch_sym.replace(',','')
            prt_sym = srch_sym.replace('&amp;','&')
            prt_sym = prt_sym.replace('amp;','')
            if srch_sym[0:4].upper() == 'THE ':
                srch_sym = srch_sym[4:]
            print(f'* {search_string} * {srch_sym} * {prt_sym}',end="")

        if iKount<800:
            for i in range(3):
                response_window[i] = response_window[i+1]
            try:
                response_window[3] = Pydos_wifi.next(256)
                if len(response_window[3]) != 256:
                    print('X',end="")
                    iKount=800
            except:
                iKount=800
    print()

    print("Locating price data",end="")
    response.close()
    response = Pydos_wifi.get(TEXT_URL)
    response_window = []
    iKount = 0
    for _ in range(4):
        response_window.append(Pydos_wifi.next(256))
        if len(response_window[-1]) != 256:
            iKount = 799
            break

    nasdaq = -1
    while nasdaq == -1 and iKount<800:
        iKount +=1
        if iKount % 10 == 0:
            print(".",end="")

        found_window = str(b''.join(response_window))
        nasdaq = found_window.upper().find(search_string)
        if nasdaq == -1:
            nasdaq = found_window.upper().find(srch_sym.upper())
        if nasdaq == -1:
            for i in range(3):
                response_window[i] = response_window[i+1]
            try:
                response_window[3] = Pydos_wifi.next(256)
                if len(response_window[3]) != 256:
                    print('X',end="")
                    iKount=800
            except:
                print('X',end="")
                iKount=800
        else:
            if iKount < 800:
                for _ in range(2):
                    response_window.append(Pydos_wifi.next(256))
                    if len(response_window[-1]) != 256:
                        print('X',end="")
                        iKount = 800
                        break

                found_window = str(b''.join(response_window))
                pct = found_window[nasdaq:].find('%)')
                if pct == -1 and iKount<800:
                    response_window[0] = response_window[2]
                    response_window[1] = response_window[3]
                    response_window[3] = response_window.pop()
                    response_window[2] = response_window.pop()
                    nasdaq = -1

    print("*\n")
    found_window = str(b''.join(response_window))
    nasdaq = found_window.upper().find(search_string)
    if nasdaq == -1:
        nasdaq = str(b''.join(response_window)).upper().find(srch_sym.upper())

    pct = found_window.find('%)')
    pctst = found_window[:pct].rfind('>')+1
    pctend = pct + found_window[pct:].find('<')
    #print("Debug: %s\n" % found_window[nasdaq:pctend])
    pricest = found_window[:pctst-2].rfind('>')+1
    priceend = pricest + found_window[pricest:].find('<')

    if nasdaq != -1:
        print(f'{prt_sym}: {found_window[pricest:priceend]} {found_window[pctst:pctend].replace("<","")}\n')
    else:
        print(f"{prt_sym} symbol not found\n")

    Pydos_wifi.close()
    del response_window
    del found_window

if __name__ == "PyDOS":
    wifi_finance(passedIn)
else:
    print('Enter "wifi_finance.wifi_finance("symbol")" in the REPL or PEXEC command to run.')
    print('    A null symbol ("") will default to the Nasdaq Index')
# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

from sys import implementation
from os import uname
from pydos_wifi import Pydos_wifi
import time

def wifi_finance(symbol):
    try:
        _scrWidth = int(envVars.get('_scrWidth',80))
    except:
        _scrWidth = 80

    if not symbol:
        symbol = ".IXIC:INDEXNASDAQ"
    else:
        symbol = symbol.upper()
    prt_sym = symbol[:symbol.find(':')]
    srch_sym = symbol[:symbol.find(':')]
    search_attempts = 5000

    # Get wifi details and more from a .env file
    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    print("Connecting to %s" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))

    res = False
    for i in range(2):
        try:
            res = Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD'))
            break
        except:
            print('Retrying....')
    if not res:
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
    #TEXT_URL = f"https://www.google.com/search?q={symbol.replace('&','%26')}+stock+price"
    #search_string = symbol
    #Id_Symbol = True
    #price_ident = '%)'
    #window_depth=4

    TEXT_URL = f"https://www.google.com/finance/quote/{symbol.replace('&','%26')}"
    search_string = symbol
    Id_Symbol = False
    price_ident = 'data-last-price'
    window_depth = 5

    #headers = {"user-agent": "RetiredWizard@"+implementation.name.lower()+uname()[2]}

    print("Fetching text from %s" % TEXT_URL)
    response = Pydos_wifi.get(TEXT_URL)
    response_window = []
    for _ in range(window_depth):
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

    iKount = 0
    if Id_Symbol:
        print("Identifying symbol",end="")
        name_loc = -1
        while name_loc == -1 and iKount<search_attempts:
            iKount +=1
            if iKount % 10 == 0:
                print(".",end="")

            found_window = str(b''.join(response_window))

            name_loc = found_window.find(' Inc. is')
            if name_loc == -1:
                name_loc = found_window.find(' Inc., commonly')
            if name_loc == -1:
                name_loc = found_window.find(' is a stock market ')
            if name_loc == -1:
                name_strt = found_window.find('Company Name')
                if name_strt != -1:
                    print(f'{name_strt} {found_window[:name_strt]}') 
                    name_loc = found_window[:name_start].find('<')+name_start+1
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

            if iKount<search_attempts:
                for i in range(window_depth-1):
                    response_window[i] = response_window[i+1]
                try:
                    response_window[window_depth-1] = Pydos_wifi.next(256)
                    if len(response_window[window_depth-1]) != 256:
                        print('X',end="")
                        iKount=search_attempts
                except:
                    iKount=search_attempts
        print()

        response.close()
        response = Pydos_wifi.get(TEXT_URL)
        response_window = []
        iKount = 0
        for _ in range(window_depth):
            response_window.append(Pydos_wifi.next(256))
            if len(response_window[-1]) != 256:
                iKount = search_attempts-1
                break

    print(f"Locating price data for {search_string} * {srch_sym} * {prt_sym}",end="")

    nasdaq = -1
    while nasdaq == -1 and iKount<search_attempts:
        iKount +=1
        if iKount % 10 == 0:
            print(".",end="")

        found_window = str(b''.join(response_window))
        nasdaq = found_window.upper().find(search_string)
        if nasdaq == -1:
            nasdaq = found_window.upper().find(srch_sym.upper())
        if nasdaq == -1:
            for i in range(window_depth-1):
                response_window[i] = response_window[i+1]
            try:
                response_window[window_depth-1] = Pydos_wifi.next(256)
                if len(response_window[window_depth-1]) != 256:
                    print('X',end="")
                    iKount=search_attempts
            except:
                print('X',end="")
                iKount=search_attempts
        else:
            if iKount < search_attempts:
                for _ in range(window_depth-2):
                    response_window.append(Pydos_wifi.next(256))
                    if len(response_window[-1]) != 256:
                        print('X',end="")
                        iKount = search_attempts
                        break

                found_window = str(b''.join(response_window))
                pct = found_window[nasdaq:].find(price_ident)
                if pct == -1 and iKount<search_attempts:
                    for i in range(2):
                        response_window[i] = response_window[i+(window_depth-2)]
                    for i in range(window_depth-2):
                        response_window[(window_depth-1)-i] = response_window.pop()
                    nasdaq = -1

    print("*\n")
    found_window = str(b''.join(response_window))
    nasdaq = found_window.upper().find(search_string)
    if nasdaq == -1:
        nasdaq = str(b''.join(response_window)).upper().find(srch_sym.upper())

    if nasdaq != -1:
# Final scrape logic
#       Google Search
#        pct = found_window.find(price_ident)
#        pctst = found_window[:pct].rfind('>')+1
#        pctend = pct + found_window[pct:].find('<')
#        print("Debug: %s\n" % found_window[nasdaq:pctend])
#        pricest = found_window[:pctst-2].rfind('>')+1
#        priceend = pricest + found_window[pricest:].find('<')

#       Google finance
        pricest = found_window.find(price_ident)+len(price_ident)+2
        priceend = pricest + found_window[pricest:].find('"')
        pctst = -1

        #print(f'Debug: start loc: {pricest} end loc: {priceend}\n{found_window[nasdaq:]}')

        print(f'{prt_sym}: {found_window[pricest:priceend]}',end="")
        if pctst != -1:
            print(f' {found_window[pctst:pctend].replace("<","")}\n')
        else:
            print('\n')
    else:
        print(f"{prt_sym} symbol not found\n")

    Pydos_wifi.close()
    del response_window
    del found_window

print('\nDemonstration Web "scraping" program. The web sites being used in the')
print('demonstration will often change and break the algorithm used to locate a')
print('stock price. When that happens this program needs to be updated to work')
print('with the new web site or find a new one.\n')
print('The current web site being used is: https://www.google.com/finance\n')
print('With this site the symbol passed to wifi_finance must be formatted as')
print('follows: symbol:exchange. So for Apple Inc, you would enter AAPL:NASDAQ')
print('or for AT&T enter T:NYSE. To retrieve the price of an index format the')
print('symbol as follows: .indexsymbol:INDEXsymbol. For example Nasdaq:')
print('.IXIC:INDEXNASDAQ, Dow Jones: .DJI:INDEXDJX, S&P 500: .INX:INDEXSP. The')
print('index symbols can be retrieved by going to the www.google.com/finance page')
print("and selecting the index you're inerested in. The formatted symbol will be")
print('updated at the end of the URL (not the symbol displayed in the search box.')

if __name__ == "PyDOS":
    wifi_finance(passedIn)
else:
    print('Enter "wifi_finance.wifi_finance("symbol")" in the REPL or PEXEC command to run.')
    print('    A null symbol ("") will default to the Nasdaq Index')


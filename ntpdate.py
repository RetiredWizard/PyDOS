import sys

if sys.implementation.name.upper() == 'MICROPYTHON':
    import network
    import ntptime
    import time
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import socketpool
    import wifi
    import adafruit_ntp
    import rtc
    from os import getenv

def ntpdate(passedIn=""):
    if passedIn == "":
        my_tz_offset = -4
    else:
        my_tz_offset = int(passedIn)

    if sys.implementation.name.upper() == "MICROPYTHON":
        # Get wifi details and more from a .env file
        config = {}
        envfound = True
        try:
            envfile = open('/settings.toml')
        except:
            envfound = False

        if envfound:
            for line in envfile:
                try:
                    config[line.split('=')[0].strip()] = line.split('=')[1].strip().replace('"','')
                except:
                    pass
            envfile.close()

        if config.get('CIRCUITPY_WIFI_SSID',None) is None:
            raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

        wlan = network.WLAN(network.STA_IF)
        if not wlan.active():
            # Init wlan module and connect to network
            print("Connecting to %s, Note this may take a while..." % config['CIRCUITPY_WIFI_SSID'])

            wlan.active(True)
            wlan.connect(config['CIRCUITPY_WIFI_SSID'], config['CIRCUITPY_WIFI_PASSWORD'])

        # Wait until wifi is connected
        while not wlan.isconnected():
            pass

        # We should have a valid IP now via DHCP
        print("Wi-Fi Connected ", wlan.ifconfig()[0])
        print("Attempting to set Date/Time")

        success = False
        for i in range(10):
            try:
                ntptime.settime()
                success = True
                break
            except:
                time.sleep(2)
            print(".",end="")
        if not success:
            print(".")
            ntptime.settime()
        ltime = time.mktime(time.gmtime()) + my_tz_offset*3600
        inTime = time.localtime(ltime)

        machine.RTC().datetime(tuple([inTime[i] for i in [0,1,2,6,3,4,5,7]]))

    elif sys.implementation.name.upper() == "CIRCUITPYTHON":
        # Get wifi details and more from a .env file
        if getenv('CIRCUITPY_WIFI_SSID') is None:
            raise Exception("WiFi secrets are kept in .env, please add them there by using setenv.py!")

        print("Connecting to %s" % getenv('CIRCUITPY_WIFI_SSID'))
        wifi.radio.connect(getenv('CIRCUITPY_WIFI_SSID'), getenv('CIRCUITPY_WIFI_PASSWORD'))
        print("Connected to %s!" % getenv('CIRCUITPY_WIFI_SSID'))
        print("My IP address is", wifi.radio.ipv4_address)

        socket = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(socket, server='pool.ntp.org', tz_offset=my_tz_offset)

        success = False
        for i in range(5):
            print(".",end="")
            try:
                rtc.RTC().datetime = ntp.datetime
                success = True
                break
            except:
                pass
        if not success:
            print(".")
            rtc.RTC().datetime = ntp.datetime

    print("\nTime and Date successfully set")

if __name__ != "PyDOS":
    passedIn = ""

ntpdate(passedIn)

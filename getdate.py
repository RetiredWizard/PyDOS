import sys
import os
import time
import json
from pydos_wifi import Pydos_wifi

if sys.implementation.name.upper() == 'MICROPYTHON':
    import ntptime
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    try:
        import adafruit_ntp
    except:
        pass
    import rtc

def getdate(passedIn=""):
    envVars['errorlevel'] = '1'

    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    if not Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')):
        raise Exception("Wifi Connection Error")

    print("Connected to %s!" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))
    # We should have a valid IP now via DHCP
    print("My IP address is", Pydos_wifi.ipaddress)

    print("Attempting to set Date/Time",end="")

    try:
        print( "Trying NTP...",end="")

        if passedIn == "":
            tz_hour_offset = -4
        else:
            tz_hour_offset = eval(passedIn)

        if sys.implementation.name.upper() == "MICROPYTHON":
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
            unixtime = time.mktime(time.gmtime()) + tz_hour_offset*3600
            ltime = time.localtime(unixtime)

            machine.RTC().datetime(tuple([ltime[i] for i in [0,1,2,6,3,4,5,7]]))
            print("\nTime and Date successfully set",end="")
            envVars['errorlevel'] = '0'

        elif sys.implementation.name.upper() == "CIRCUITPYTHON":
            ntp = None
            #if not hasattr(Pydos_wifi.radio,'get_time'):
            try:
                ntp = adafruit_ntp.NTP(Pydos_wifi._pool, server='pool.ntp.org', tz_offset=tz_hour_offset)
            except:
                pass

            success = False
            for i in range(5):
                print(".",end="")
                if ntp:
                    try:
                        rtc.RTC().datetime = ntp.datetime
                        success = True
                        break
                    except:
                        pass
                #else:
                strtTime = time.time()
                while time.time() < strtTime+5 and not success:
                    try:
                        rtc.RTC().datetime = time.localtime(Pydos_wifi.radio.get_time()[0] + tz_hour_offset*3600)
                        success = True
                        break
                    except:
                        time.sleep(.5)

    # One more try, this time display the exception if we fail
            if not success:
                print(".")
                if ntp:
                    try:
                        rtc.RTC().datetime = ntp.datetime
                        success = True
                    except:
                        pass
                #else:
                if not success:
                    rtc.RTC().datetime = time.localtime(Pydos_wifi.radio.get_time()[0] + tz_hour_offset*3600)

            print("\nTime and Date successfully set",end="")
            envVars['errorlevel'] = '0'

    except:

        print("FAILED. Trying http worldtimeapi.org...",end="")
        Pydos_wifi.timeout = 1000
        response = Pydos_wifi.get("http://worldtimeapi.org/api/ip",None,True)
        time_data = Pydos_wifi.json()

        if passedIn == "":
            tz_hour_offset = int(time_data['utc_offset'][0:3])
            tz_min_offset = int(time_data['utc_offset'][4:6])
            if (tz_hour_offset < 0):
                tz_min_offset *= -1
        else:
            tz_hour_offset = int(passedIn)
            tz_min_offset = 0

        unixtime = int(time_data['unixtime'] + (tz_hour_offset * 60 * 60)) + (tz_min_offset * 60)
        ltime = time.localtime(unixtime)

        if sys.implementation.name.upper() == "MICROPYTHON":
            machine.RTC().datetime(tuple([ltime[0]-(time.localtime(0)[0]-1970)]+[ltime[i] for i in [1,2,6,3,4,5,7]]))
        else:
            rtc.RTC().datetime = ltime

        print("\nTime and Date successfully set",end="")
        envVars['errorlevel'] = '0'

    print()
    Pydos_wifi.close()

# ----------------------------------------------------------------------------------
# This is the main entry point for the getdate.py script.


# optional configuration file for speaker/headphone setting, check current and root directory
if __name__ != "PyDOS":
    launcher_config = {}
    if "launcher.conf.json" in os.listdir("/"):
        with open("/launcher.conf.json", "r") as f:
            launcher_config = json.load(f)
    if 'inetclock' in launcher_config:
        launcher_config = launcher_config['inetclock']

    if 'tz_offset' in launcher_config:
        if type(launcher_config['tz_offset']) is str:
            passedIn = launcher_config['tz_offset']
        else:
            passedIn = str(launcher_config['tz_offset'])
    else:
        passedIn = input("Enter your current timezone offset (enter for default): ")

    if 'envVars' not in dir():
        envVars = {}

getdate(passedIn)

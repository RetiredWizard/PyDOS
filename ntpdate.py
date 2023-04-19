import sys
import time
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

def ntpdate(passedIn="-4"):
    if passedIn == "":
        my_tz_offset = -4
    else:
        my_tz_offset = int(passedIn)
        
    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    if Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')):
        print("Connected to %s!" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))
        # We should have a valid IP now via DHCP
        print("My IP address is", Pydos_wifi.ipaddress)
        print("Attempting to set Date/Time")

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
            ltime = time.mktime(time.gmtime()) + my_tz_offset*3600
            inTime = time.localtime(ltime)

            machine.RTC().datetime(tuple([inTime[i] for i in [0,1,2,6,3,4,5,7]]))

        elif sys.implementation.name.upper() == "CIRCUITPYTHON":
            if Pydos_wifi.esp == None:
                ntp = adafruit_ntp.NTP(Pydos_wifi._socket, server='pool.ntp.org', tz_offset=my_tz_offset)

            success = False
            for i in range(5):
                print(".",end="")
                if Pydos_wifi.esp:
                    strtTime = time.time()
                    while time.time() < strtTime+5 and not success:
                        try:
                            rtc.RTC().datetime = time.localtime(Pydos_wifi.esp.get_time()[0] + my_tz_offset*3600)
                            success = True
                        except:
                            pass
                    if success:
                        break
                else:
                    try:
                        rtc.RTC().datetime = ntp.datetime
                        success = True
                        break
                    except:
                        pass
            if not success:
                print(".")
                if Pydos_wifi.esp:
                    rtc.RTC().datetime = time.localtime(Pydos_wifi.esp.get_time()[0])
                else:
                    rtc.RTC().datetime = ntp.datetime

        print("\nTime and Date successfully set")
    else:
        print("Wifi Connection Error")

    Pydos_wifi.close()

if __name__ != "PyDOS":
    passedIn = input("Enter your current timezone: ")

ntpdate(passedIn)

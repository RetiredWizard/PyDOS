import rtc
import socketpool
import wifi
import adafruit_ntp
from os import getenv

def ntpdate(passedIn=""):
    if passedIn == "":
        my_tz_offset = -4
    else:
        my_tz_offset = int(passedIn)

    # Get wifi details and more from a .env file
    if getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in .env, please add them there by using setenv.py!")

    print("Connecting to %s" % getenv('CIRCUITPY_WIFI_SSID'))
    wifi.radio.connect(getenv('CIRCUITPY_WIFI_SSID'), getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to %s!" % getenv('CIRCUITPY_WIFI_SSID'))
    print("My IP address is", wifi.radio.ipv4_address)

    socket = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(socket, tz_offset=my_tz_offset)

    sucess = False
    for i in range(5):
        print(".",end="")
        try:
            rtc.RTC().datetime = ntp.datetime
            sucess = True
            break
        except:
            pass
    if not sucess:
        print(".",end="")
        rtc.RTC().datetime = ntp.datetime
    print("\nTime and Date successfully set")

if __name__ != "PyDOS":
    passedIn = ""

ntpdate(passedIn)
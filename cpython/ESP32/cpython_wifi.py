# esp32s2-test.py -- small WiFi test program for ESP32-S2 CircuitPython 6
# taken from https://www.reddit.com/r/circuitpython/comments/ianpm8/using_wifi_when_running_on_esp32s2saola1_board/
#
import time
import ipaddress
import wifi
import socketpool
import ssl
import adafruit_requests

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
ssid=secrets["ssid"]
passwd=secrets["password"]

print('Hello World!')

for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")
print(wifi.radio.connect(ssid=ssid,password=passwd))
# the above gives "ConnectionError: Unknown failure" if ssid/passwd is wrong

print("my IP addr:", wifi.radio.ipv4_address)

print("pinging 1.1.1.1...")
ip1 = ipaddress.ip_address("1.1.1.1")
print("ip1:",ip1)
print("ping:", wifi.radio.ping(ip1))


pool = socketpool.SocketPool(wifi.radio)
request = adafruit_requests.Session(pool, ssl.create_default_context())

print("Fetching wifitest.adafruit.com...");
response = request.get("http://wifitest.adafruit.com/testwifi/index.html")
print(response.status_code)
print(response.text)

print("Fetching https://httpbin.org/get...");
response = request.get("https://httpbin.org/get")
print(response.status_code)
print(response.json())

response.close()
request._free_sockets()

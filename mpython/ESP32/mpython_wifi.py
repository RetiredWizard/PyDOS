import network
import socket

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    response = ""
    while True:
        data = s.recv(100)
        if data:
            response = response + str(data, 'utf8')
        else:
            break
    s.close()

    return response

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Check secrets.py has updated credentials
if secrets['ssid'] == 'your-ssid-here':
    assert False, ("WiFi secrets are kept in secrets.py, please add them there!")

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
if not wlan.active():
    wlan.active(True)

    # Connect to WiFi router
    print ("Connecting to WiFi: {}".format( secrets['ssid'] ) )
    wlan.connect( secrets['ssid'], secrets['password'])

# Wait until wifi is connected
while not wlan.isconnected():
    pass

print("Fetching text from", TEXT_URL)
r = http_get(TEXT_URL)
print("-" * 40)
print(r)
print("-" * 40)

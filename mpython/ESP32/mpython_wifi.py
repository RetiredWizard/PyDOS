import network, json
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

# Read config
with open('config.json') as f:
    config = json.load(f)

# Check config.json has updated credentials
if config['ssid'] == 'Enter_Wifi_SSID':
    assert False, ("config.json has not been updated with your unique keys and data")

# Create WiFi connection and turn it on
wlan = network.WLAN(network.STA_IF)
if not wlan.active():
    wlan.active(True)

    # Connect to WiFi router
    print ("Connecting to WiFi: {}".format( config['ssid'] ) )
    wlan.connect( config['ssid'], config['ssid_password'])

# Wait until wifi is connected
while not wlan.isconnected:
    pass

print("Fetching text from", TEXT_URL)
r = http_get(TEXT_URL)
print("-" * 40)
print(r)
print("-" * 40)

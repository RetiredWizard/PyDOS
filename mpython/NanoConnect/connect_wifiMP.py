import network, socket

config = {}
envfound = True
try:
    envfile = open('/.env')
except:
    envfound = False

if envfound:
    for line in envfile:
        try:
            config[line.split('=')[0].strip()] = line.split('=')[1].strip()
        except:
            pass
    envfile.close()

# Check .env has updated credentials
if not envfound or config.get('CIRCUITPY_WIFI_SSID','') == '':
    assert False, ("/.env has not been updated with your unique keys and data")

# AP info
SSID=config['CIRCUITPY_WIFI_SSID'] # Network SSID
KEY=config['CIRCUITPY_WIFI_PASSWORD']  # Network key

PORT = 80
HOST = "www.google.com"

# Init wlan module and connect to network
print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

# We should have a valid IP now via DHCP
print("Wi-Fi Connected ", wlan.ifconfig())

# Get addr info via DNS
addr = socket.getaddrinfo(HOST, PORT)[0][4]
print(addr)

# Create a new socket and connect to addr
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

# Set timeout
client.settimeout(3.0)

# Send HTTP request and recv response
client.send("GET / HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))
print((client.recv(1024)).decode())
# Close socket
client.close()


HOST = 'wifitest.adafruit.com'
# Get addr info via DNS
addr = socket.getaddrinfo(HOST, PORT)[0][4]
print(addr)

# Create a new socket and connect to addr
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

# Set timeout
client.settimeout(3.0)

# Send HTTP request and recv response
client.send("GET /testwifi/index.html HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))
print("-" * 40)
print((client.recv(1024)).decode())
print("-" * 40)


# Close socket
client.close()

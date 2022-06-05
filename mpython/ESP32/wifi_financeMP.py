import network,gc
try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# AP info
SSID=secrets['ssid'] # Network SSID
KEY=secrets['password']  # Network key

PORT = 443
HOST = "money.cnn.com"
#HOST2 = "www.money.cnn.com/data/markets"

wlan = network.WLAN(network.STA_IF)
if not wlan.active():
    # Init wlan module and connect to network
    print("Trying to connect. Note this may take a while...")

    wlan.active(True)
    wlan.connect(SSID, KEY)

# Wait until wifi is connected
while not wlan.isconnected():
    pass


# We should have a valid IP now via DHCP
print("Wi-Fi Connected ", wlan.ifconfig())

# Get addr info via DNS
addr = _socket.getaddrinfo(HOST, PORT)[0][4]
print("Connecting to: ",addr)

# Create a new socket and connect to addr
#client = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
client = _socket.socket()
client.connect(addr)

client = ssl.wrap_socket(client)
print(client)

# Set timeout
#client.settimeout(3.0)

# Send HTTP request and recv response
print("Fetching text from %s/data/markets" % HOST)
client.write("GET /data/markets HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))

print("-" * 40)
response = client.read(800).decode('utf-8')
print("Text Response: ", response[0:800])
print("-" * 40)
print()

nasdaq = -1
while nasdaq == -1:
    gc.collect()
    response = client.read(4096).decode('utf-8')

    nasdaq = response.find('data-ticker-name="Nasdaq"')
    pct = response[nasdaq:].find('%')
    pctst = response[nasdaq+35:].find('>')
    pctend = response[nasdaq+35:].find('<')-1

print("Nasdaq: ",response[nasdaq+36+pctst:nasdaq+36+pctend])

# Close socket
#sslclient.close()
client.close()

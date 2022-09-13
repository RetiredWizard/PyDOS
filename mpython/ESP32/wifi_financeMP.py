import network,gc
try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl
import time

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

PORT = 443
#HOST = "money.cnn.com"
#HOST2 = "www.money.cnn.com/data/markets"
HOST = "finance.yahoo.com"

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
print("Fetching text from %s/quote/%%5EIXIC" % HOST)
#client.write("GET /data/markets HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))
client.write("GET /quote/%%5EIXIC HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))

print("-" * 40)
response = client.read(800).decode('utf-8')
print("Text Response: ", response[0:800])
print("-" * 40)
print()

nasdaq = -1
strtime = time.ticks_ms()
timer = 0
while nasdaq == -1 and timer < 60000:
    gc.collect()
    #response = client.read(4096).decode('utf-8')
    encresponse = client.read(4096)
    decerror = False
    try:
        response = encresponse.decode()
    except:
        decerror = True
        
    if decerror:
        response = ""
        for chresp in encresponse:
            try:
                response += chr(chresp)
            except:
                pass
        
    #nasdaq = response.find('data-ticker-name="Nasdaq"')
    nasdaq = response.find('data-symbol="^IXIC" data-field="regularMarketChangePercent"')
    pct = response[nasdaq:].find('%)')
    pctst = response[nasdaq+pct-15:].find('>')
    pctend = response[nasdaq+pct:].find('<')
    
    timedelta = time.ticks_ms() - strtime
    if timedelta > 0:
        timer += timedelta
        strtime += timedelta
    else:
        strtime = time.ticks_ms()
    
if nasdaq == -1:
    print("Timeout fetching Web data")
else:
    print("Nasdaq: ",response[nasdaq+pct-14+pctst:nasdaq+pct+pctend])

# Close socket
#sslclient.close()
client.close()

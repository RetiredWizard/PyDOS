import wifi,socketpool,ssl
import adafruit_requests
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("FeatherS2 (esp32s2) Connect webclient test")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

ntrys = 0
while wifi.radio.ipv4_address == None and ntrys < 3:
    if ntrys == 0:
        print("Connecting to AP...")
    ntrys += 1
    try:
        wifi.radio.connect(ssid=secrets['ssid'],password=secrets['password'])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue


if wifi.radio.ipv4_address != None:
    print(wifi.radio.hostname,"connected to",secrets['ssid'])
    print("My IP address is", wifi.radio.ipv4_address)

    #print("IP lookup adafruit.com: %s" % esp.pretty_ip(esp.get_host_by_name("adafruit.com")))

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    print("Fetching text from", TEXT_URL)
    r = requests.get(TEXT_URL)
    print("-" * 40)
    print(r.text)
    print("-" * 40)
    r.close()

else:
    print("Connection to {} failed".format(secrets['ssid']))

print("Done!")
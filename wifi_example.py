# SPDX-FileCopyrightText: 2021 jfabernathy for Adafruit Industries
# SPDX-License-Identifier: MIT

# MicroPython/CircuitPython ESP32 family, Pico W and (Nano Connect on MicroPython only) 
# For example code using the Arduino Nano Connect on CircuitPython see pydos_wifi.py

import sys
from os import uname
try:
    import ussl as ssl
except:
    import ssl

if sys.implementation.name.upper() == 'MICROPYTHON':
    try:
        import usocket as _socket
    except:
        import _socket
    import urequests as https
    import network,json,select,time,ctypes,struct,random
    def getenv(tomlKey):
        config = {}
        envfound = True
        try:
            with open('/settings.toml') as envfile:
                for line in envfile:
                    try:
                        config[line.split('=')[0].strip()] = line.split('=')[1].strip().replace('"','')
                    except:
                        pass
        except:
            pass
        
        return config.get(tomlKey,None)

    def checksum(data):
        if len(data) & 0x1: # Odd number of bytes
            data += b'\0'
        cs = 0
        for pos in range(0, len(data), 2):
            b1 = data[pos]
            b2 = data[pos + 1]
            cs += (b1 << 8) + b2
        while cs >= 0x10000:
            cs = (cs & 0xffff) + (cs >> 16)
        cs = ~cs & 0xffff
        return cs

elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import socketpool
    import wifi
    from os import getenv
    import adafruit_requests as requests
    import ipaddress

# Get wifi details and more from a .env file
if getenv('CIRCUITPY_WIFI_SSID') is None:
    raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

ssid=getenv('CIRCUITPY_WIFI_SSID')
passwd=getenv('CIRCUITPY_WIFI_PASSWORD')

print('\nThis program demonstrates various methods of performing web queries and posts')
print('in both CircuitPython and MicroPython....\n')

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    for network in wifi.radio.start_scanning_networks():
        print(network, network.ssid, network.channel)
    wifi.radio.stop_scanning_networks()

elif sys.implementation.name.upper() == 'MICROPYTHON':
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    for network in wlan.scan():
        if network[0].decode() != '':
            print("<Network>",network[0].decode(),network[2])

print("Connecting to %s" % ssid)
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    wifi.radio.connect(ssid, passwd)
    ipadd = wifi.radio.ipv4_address
elif sys.implementation.name.upper() == 'MICROPYTHON':
    if not wlan.active() or not wlan.isconnected():
        wlan.connect(getenv('CIRCUITPY_WIFI_SSID'),getenv('CIRCUITPY_WIFI_PASSWORD'))
    while not wlan.isconnected():
        pass

    ipadd = wlan.ifconfig()[0]

print("Connected to %s!" % ssid)
print("My IP address is", ipadd)

#
#            PING OPERATION
#
print("pinging 1.1.1.1...")
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    ip1 = ipaddress.ip_address("1.1.1.1")
    print("ip1:",ip1)
    print("ping:", wifi.radio.ping(ip1))
elif sys.implementation.name.upper() == 'MICROPYTHON':
    host = '1.1.1.1'
    count = 4
    timeout = 5000
    interval = 10
    quiet = False
    size = 64
    # prepare packet
    pkt = b'Q'*size
    pkt_desc = {
        "type": ctypes.UINT8 | 0,
        "code": ctypes.UINT8 | 1,
        "checksum": ctypes.UINT16 | 2,
        "id": ctypes.UINT16 | 4,
        "seq": ctypes.INT16 | 6,
        "timestamp": ctypes.UINT64 | 8,
    } # packet header descriptor
    h = ctypes.struct(ctypes.addressof(pkt), pkt_desc, ctypes.BIG_ENDIAN)
    h.type = 8 # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    #h.id = urandom.randint(0, 65535)
    h.id = random.getrandbits(16)
    h.seq = 1

    # init socket
    sock = _socket.socket(_socket.AF_INET, _socket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout/1000)
    addr = _socket.getaddrinfo(host, 1)[0][-1][0] # ip address
    sock.connect((addr, 1))
    poller = select.poll()
    poller.register(sock, select.POLLIN)
    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count+1)) 
    c = 1
    tStart = time.ticks_ms()
    t = 0
    n_trans = 0
    n_recv = 0
    finish = False
    while t < timeout:
        if (t>=interval and c<=count) or t==0:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = time.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0 # reset timeout
                tStart = time.ticks_ms()
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        t = time.ticks_ms() - tStart 
        if t < 0:
            t = time.time_ms() + 1
        while t < timeout/3:
            socks = poller.poll(1000)
            if socks:
                resp = socks[0][0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = ctypes.struct(ctypes.addressof(resp_mv[20:]), pkt_desc, ctypes.BIG_ENDIAN)
                # TODO: validate checksum (optional)
                seq = h2.seq
                if h2.type==0 and h2.id==h.id and (seq in seqs): # 0: ICMP_ECHO_REPLY
                    t_elasped = (time.ticks_us()-h2.timestamp) / 1000
                    ttl = struct.unpack('!B', resp_mv[8:9])[0] # time-to-live
                    n_recv += 1
                    not quiet and print("%u bytes from %s: icmp_seq=%u, ttl=%u, time=%.2f ms" % (len(resp), addr, seq, ttl, t_elasped))
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                    break
            t = time.ticks_ms() - tStart 
            if t < 0:
                t = time.time_ms() + 1

        if finish:
            break

        t = time.ticks_ms() - tStart 
        if t < 0:
            t = time.time_ms() + 1

    # close
    poller.unregister(sock)
    sock.close()
    not quiet and print("%u packets transmitted, %u packets received" % (n_trans, n_recv))

TEXT_URL = "https://httpbin.org/get"
JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"
PORT = 443
HOST = "httpbin.org"
headers = {"user-agent": "RetiredWizard@"+sys.implementation.name.lower()+uname()[2]}

#
#             HTTP GET OPERATION FROM PORT 80, NOT ENCRYPTED
#
print("\n\nFetching wifitest.adafruit.com...\n");
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    socket = socketpool.SocketPool(wifi.radio)
    https = requests.Session(socket, ssl.create_default_context())
    response = https.get("http://wifitest.adafruit.com/testwifi/index.html")
    print(response.status_code)
    print(response.text)
    response.close()
elif sys.implementation.name.upper() == 'MICROPYTHON':
    # Get addr info via DNS
    addr = _socket.getaddrinfo('wifitest.adafruit.com', 80)[0][4]
    # Create a new socket and connect to addr
    client = _socket.socket()
    client.connect(addr)
    # Send HTTP request and recv response
    client.write('GET /testwifi/index.html HTTP/1.1\r\nHost: wifitest.adafruit.com\r\n\r\n')
    # socket not wrapped in SSL ends properly at end of data so length(4096) > data works
    print(client.recv(4096).decode()) 
    client.close()

#
#             HTTPS GET OPERATION FROM PORT 443, SSL ENCRYPTED
# 
print("\n\nFetching text from %s\n" % TEXT_URL)
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    response = https.get(TEXT_URL)
    print("-" * 40)
    print("Text Response: ", response.text)
    print("-" * 40)
    response.close()
elif sys.implementation.name.upper() == 'MICROPYTHON':
    # Get addr info via DNS
    addr = _socket.getaddrinfo(HOST, PORT)[0][4]
    # Create a new socket and connect to addr
    client = _socket.socket()
    client.connect(addr)
    response = ssl.wrap_socket(client)
    # Send HTTP request and recv response
    response.write('GET /get HTTP/1.1\r\nHost: %s\r\n\r\n'%HOST)

    poller = select.poll()
    poller.register(response, select.POLLIN)
    res = poller.poll(1000)
    while res:
        # socket wrapped in SSL doesn't close at end of data so must read single byte
        # and continually check if more data is available
        print(res[0][0].read(1).decode(),end="")
        res = poller.poll(500)
    poller.unregister(response)
    response.close()
    client.close()

#
#            HTTPS GET FROM PORT 443 OF JSON DATA micropython uses urequests
#
print("\n\nFetching JSON data from %s\n" % JSON_GET_URL)
# micropython urequests and circuitpython requests have same parameters/format
# micropython urequests somehow manages to detect the end of socket data properly
response = https.get(JSON_GET_URL)
print("-" * 40)
print("JSON Response: ", response.json())
print("-" * 40)
response.close()

#
#            HTTPS POST TO PORT 443 OF JSON DATA
#
data = "31F"
json_data = {"Date": "July 25, 2019"}
print("\n\nPOSTing data to {0}: {1}\n".format(JSON_POST_URL, data))
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    response = https.post(JSON_POST_URL, data=data)
    print("-" * 40)

    json_resp = response.json()
    # Parse out the 'data' key from json_resp dict.
    print("Data received from server:", json_resp["data"])
    print("-" * 40)

elif sys.implementation.name.upper() == 'MICROPYTHON':
    # Get addr info via DNS
    addr = _socket.getaddrinfo(HOST, PORT)[0][4]
    # Create a new socket and connect to addr
    client = _socket.socket()
    client.connect(addr)
    response = ssl.wrap_socket(client)
    # Send HTTP request and recv response
    response.write('POST /post HTTP/1.1\r\nHost: %s\r\nContent-Length: 10\r\n\r\ndata=%s\r\n'%(HOST,data))

    poller = select.poll()
    poller.register(response, select.POLLIN)
    json_response = ""
    startjson = False
    iKount = 0
    res = poller.poll(1000)
    while res:
        iKount += 1
        if iKount % 1000 == 0:
            print(".",end="")
        json_response += res[0][0].read(1).decode()
        if not startjson:
            if json_response[-1] != '{':
                json_response = ""
            else:
                startjson = True
        res = poller.poll(500)

    print("-" * 40)
    print("Data received from server:", json.loads(json_response)["data"].replace('\n','').replace('\r',''))
    print("-" * 40)
    poller.unregister(response)
    response.close()
    client.close()

#
#            HTTPS POST TO PORT 443 OF JSON DATA micropython uses urequests
#
print("\n\nPOSTing data to {0}: {1}\n".format(JSON_POST_URL, json_data))
response = https.post(JSON_POST_URL, json=json_data)
print("-" * 40)

json_resp = response.json()
# Parse out the 'json' key from json_resp dict.
print("JSON Data received from server:", json_resp["json"])
print("-" * 40)

response.close()
if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    https._free_sockets()

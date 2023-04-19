PyDOS_wifi_VER = "1.20"

import os
import time
from sys import implementation

if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import adafruit_requests as requests

    if board.board_id == 'arduino_nano_rp2040_connect':
        import busio
        from digitalio import DigitalInOut
        from adafruit_esp32spi import adafruit_esp32spi
        import adafruit_esp32spi.adafruit_esp32spi_socket as socket
    else:
        import ssl
        import socketpool
        import wifi

elif implementation.name.upper() == 'MICROPYTHON':
    try:
        import ussl as ssl
    except:
        import ssl
    try:
        import usocket as socket
    except:
        import socket
    import network
    try:
        import urequests as https
    except:
        print("***NOTE*** urequests library not available, json queries may not complete")
        print("https://github.com/micropython/micropython-lib/tree/master/python-ecosys \n")
        import json
    import select

class PyDOS_wifi:

    _esp32_cs = None
    _esp32_ready = None
    _esp32_reset = None

    def __init__(self,timeout=15000):

        self.timeout = 15000
        self.wlan = None
        self.esp = None
        self.ipaddress = None
        self.response = None
        self._spi = None
        self._socket = None
        self._https = None
        self._poller = None

        if implementation.name.upper() == "CIRCUITPYTHON":
            if board.board_id == 'arduino_nano_rp2040_connect':
                self._https = requests
        elif implementation.name.upper() == 'MICROPYTHON':
            self._socket = socket
            try:
                self._https = https
            except:
                self._https = None

    def getenv(self,tomlKey):
        if implementation.name.upper() == "CIRCUITPYTHON":
            retVal = os.getenv(tomlKey)
        elif implementation.name.upper() == "MICROPYTHON":
            config = {}
            envfound = True
            envFile = None
            if 'settings.toml' in os.listdir('/'):
                envFile = '/settings.toml'
            elif '.env' in os.listdir('/'):
                envFile = '/.env'

            if envFile:
                with open('/settings.toml') as envfile:
                    for line in envfile:
                        try:
                            config[line.split('=')[0].strip()] = line.split('=')[1].strip().replace('"','')
                        except:
                            print("*ERROR* Invalid "+envFile+" parameter format:\n"+line)
            
            retVal = config.get(tomlKey,None)

        return retVal

    @property
    def is_connected(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if board.board_id == 'arduino_nano_rp2040_connect':
                if self.esp != None:
                    retVal = self.esp.is_connected
                else:
                    retVal = False
            else:
                retVal = wifi.radio.ipv4_address is not None
        elif implementation.name.upper() == "MICROPYTHON":
            if self.wlan != None:
                retVal = self.wlan.isconnected()
            else:
                retVal = False

        return retVal


    def connect(self,ssid,passwd,espspi_debug=False):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if board.board_id == 'arduino_nano_rp2040_connect':
                if not self.is_connected:
                    #  ESP32 pins
                    self._esp32_cs = DigitalInOut(board.CS1)
                    self._esp32_ready = DigitalInOut(board.ESP_BUSY)
                    self._esp32_reset = DigitalInOut(board.ESP_RESET)

                    #  uses the secondary SPI connected through the ESP32
                    self._spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

                    self.esp = adafruit_esp32spi.ESP_SPIcontrol(self._spi, self._esp32_cs, \
                        self._esp32_ready, self._esp32_reset, debug=espspi_debug)
                    self._https.set_socket(socket, self.esp)

                    ntrys = 0
                    while not self.is_connected and ntrys < 3:
                        if ntrys == 0:
                            print("Connecting to AP...")
                        ntrys += 1
                        try:
                            self.esp.connect_AP(self.getenv('CIRCUITPY_WIFI_SSID'), self.getenv('CIRCUITPY_WIFI_PASSWORD'))
                        except RuntimeError as e:
                            print("could not connect to AP, retrying: ", e)

                    self.ipaddress = self.esp.pretty_ip(self.esp.ip_address)
                retVal = self.is_connected
            else:
                wifi.radio.connect(self.getenv('CIRCUITPY_WIFI_SSID'), self.getenv('CIRCUITPY_WIFI_PASSWORD'))
                self._socket = socketpool.SocketPool(wifi.radio)
                self._https = requests.Session(self._socket, ssl.create_default_context())

                self.ipaddress = wifi.radio.ipv4_address
                retVal = self.is_connected

        elif implementation.name.upper() == "MICROPYTHON":
            self.wlan = network.WLAN(network.STA_IF)
            if not self.wlan.active():
                # Init wlan module and connect to network
                print("Setting up Network connection")

                self.wlan.active(True)
                self.wlan.connect(self.getenv('CIRCUITPY_WIFI_SSID'),self.getenv('CIRCUITPY_WIFI_PASSWORD'))

            # Wait until wifi is connected
            tStamp = time.ticks_ms()
            if not self.is_connected:
                print("Trying to connect. Note this may take a while...")
            while not self.is_connected:
                try:
                    self.wlan.connect(self.getenv('CIRCUITPY_WIFI_SSID'),self.getenv('CIRCUITPY_WIFI_PASSWORD'))
                except:
                    pass
                tElapse = time.ticks_ms() - tStamp
                if tElapse < 0:
                    tStamp = time.ticks_ms()
                    tElapse = tStamp
                if tElapse > self.timeout:
                    break

            retVal = self.is_connected
            self.ipaddress = self.wlan.ifconfig()[0]

        return retVal

#  response types
#  MicroPython: JSON - urequest|SSL - ssl.wrap_socket(socket library)|Non-SSL - socket library
#  (close,text,raw,content,json)|(close,read,readinto,readline,write)|(close,read/into/line,
#          write,recv/from,send/to/all,accept,connect,listen,makefile,setblocking,settimeout)
#  CircuitPython: Nano - requests library(set_socket)|All else - requests libary.Session
#      (close,json,iter_content,content,text)|(close,json,iter_content,content,text)
    def get(self,text_url,headers=None,getJSON=False):
        if implementation.name.upper() == 'CIRCUITPYTHON':
            self.response = self._https.get(text_url,headers=headers,timeout=self.timeout)
        elif implementation.name.upper() == 'MICROPYTHON':
            if not getJSON or not self._https:
                if len(text_url.split('/',3)) == 4:
                    PROTO, _, HOST, QUERY = text_url.split('/',3)
                    QUERY = "/"+QUERY
                else:
                    PROTO, _, HOST = text_url.split('/',3)
                    QUERY = '/'

                if PROTO.upper() == 'HTTPS:':
                    PORT = 443
                else:
                    PORT = 80
                # Get addr info via DNS
                addr = self._socket.getaddrinfo(HOST, PORT)[0][4]
                # Create a new socket and connect to addr
                client = self._socket.socket()
                client.connect(addr)
                if PORT == 443:
                    self.response = ssl.wrap_socket(client)
                else:
                    self.response = client
                headStr = ""
                if headers:
                    for headKey in headers:
                        headStr += (headKey + ": " + headers[headKey] + "\r\n")
                # Send HTTP request and recv response
                #print('GET %s HTTP/1.1\r\nHost: %s\r\n%s\r\n'%(QUERY,HOST,headStr))
                self.response.write('GET %s HTTP/1.1\r\nHost: %s\r\n%s\r\n'%(QUERY,HOST,headStr))

                self._poller = select.poll()
                self._poller.register(self.response, select.POLLIN)
            else:
                if not headers:
                    headers = {}
                # urequests response used for json
                self.response = self._https.get(text_url,headers=headers,timeout=self.timeout)
                self._poller = None

        return self.response

    def json(self):
        retVal = None
        if implementation.name.upper() == 'CIRCUITPYTHON':
            retVal = self.response.json()
        elif implementation.name.upper() == 'MICROPYTHON':
            if 'json' in dir(self.response):
                retVal = self.response.json()
            else:
                foundStart = False
                retVal = ''
                nxtByte = None
                while nxtByte != b'':
                    nxtByte = self.next(1)
                    if foundStart or nxtByte.decode('utf-8') == '{':
                        retVal += nxtByte.decode('utf-8')
                        foundStart = True

                if foundStart:
                    retVal = json.loads(retVal)
                else:
                    retVal = {}

        return retVal


    def next(self,size=256):
        if implementation.name.upper() == 'CIRCUITPYTHON':
# Hack because Adafruit library doesn't seem to return requested chunk_size
            remainSize = size
            retVal = b""
            while remainSize > 0:
                try:
                    thisChunk = next(iter(self.response.iter_content(chunk_size=remainSize)))
                except StopIteration:
                    break
                retVal += thisChunk
                remainSize -= len(thisChunk)
        elif implementation.name.upper() == 'MICROPYTHON':
            if 'recv' in dir(self.response):
                retVal = self.response.recv(size)
            else:
                res = self._poller.poll(self.timeout)
                if res:
# socket wrapped in SSL doesn't close at end of data so may be reading single byte
                    retVal = res[0][0].read(size)
                else:
                    retVal = b''

        return retVal

    def close(self):
        if implementation.name.upper() == 'CIRCUITPYTHON':
            if board.board_id == 'arduino_nano_rp2040_connect':
                self.esp.disconnect()
                self.esp = None
                self._esp32_cs.deinit()
                self._esp32_ready.deinit()
                self._esp32_reset.deinit()
                self._spi.deinit()
            else:
                self._https._free_sockets()
                self._https = None
                self._socket = None
                #self.response.close()  Takes too long, effectivly hangs....
                self.response = None
        else:
            if self.response is not None:
                if self._poller is not None:
                    self._poller.unregister(self.response)
                self.response.close()
            self._poller = None
        self.response = None

Pydos_wifi = PyDOS_wifi()
PyDOS_wifi_VER = "1.36"

import os
import time
from sys import implementation

if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import adafruit_requests
    import adafruit_connection_manager

    if board.board_id == 'arduino_nano_rp2040_connect' or hasattr(board,'ESP_CS'):
        import busio
        from digitalio import DigitalInOut
        from adafruit_esp32spi import adafruit_esp32spi
    else:
        import wifi

elif implementation.name.upper() == 'MICROPYTHON':
    import ssl
    import socket
    import network
    try:
        import requests
    except:
        print("***NOTE*** requests library not available, json queries may not complete")
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
        self.radio = None
        self.ipaddress = None
        self.response = None
        self._spi = None
        self._pool = None
        self._requests = None
        self._poller = None

        if implementation.name.upper() == 'MICROPYTHON':
            self._pool = socket
            try:
                self._requests = requests
            except:
                self._requests = None

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
            if self.radio != None:
                retVal = self.radio.is_connected if hasattr(self.radio,'is_connected') else self.radio.connected
            else:
                retVal = False
        elif implementation.name.upper() == "MICROPYTHON":
            if self.wlan != None:
                retVal = self.wlan.isconnected()
            else:
                retVal = False

        return retVal


    def connect(self,ssid,passwd,espspi_debug=False):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if board.board_id in ['arduino_nano_rp2040_connect'] or 'ESP_CS' in dir(board):
                if not self.is_connected:
                    #  ESP32 pins
                    if 'ESP_CS' in dir(board):
                        self._esp32_cs = DigitalInOut(board.ESP_CS)
                    else:
                        self._esp32_cs = DigitalInOut(board.CS1)
                    self._esp32_ready = DigitalInOut(board.ESP_BUSY)
                    self._esp32_reset = DigitalInOut(board.ESP_RESET)

                    if 'SCK1' in dir(board):
                        #  uses the secondary SPI connected through the ESP32
                        self._spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
                    else:
                        self._spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

                    self.radio = adafruit_esp32spi.ESP_SPIcontrol(self._spi, self._esp32_cs, \
                        self._esp32_ready, self._esp32_reset, debug=espspi_debug)

                    ntrys = 0
                    while not self.is_connected and ntrys < 3:
                        if ntrys == 0:
                            print("Connecting to AP...")
                        ntrys += 1
                        try:
                            self.radio.connect_AP(self.getenv('CIRCUITPY_WIFI_SSID'), self.getenv('CIRCUITPY_WIFI_PASSWORD'))
                        except RuntimeError as e:
                            print("could not connect to AP, retrying: ", e)

                    self.ipaddress = self.radio.pretty_ip(self.radio.ip_address)
            else:
                self.radio = wifi.radio
                self.radio.connect(self.getenv('CIRCUITPY_WIFI_SSID'), self.getenv('CIRCUITPY_WIFI_PASSWORD'))

                self.ipaddress = wifi.radio.ipv4_address

            self._pool = adafruit_connection_manager.get_radio_socketpool(self.radio)
            self._requests = adafruit_requests.Session(self._pool, \
                adafruit_connection_manager.get_radio_ssl_context(self.radio))                    
            retVal = self.is_connected

        elif implementation.name.upper() == "MICROPYTHON":
            self.wlan = network.WLAN(network.STA_IF)
            if not self.wlan.active():
                # Init wlan module and connect to network
                print("Setting up Network connection")
                self.wlan.active(True)

            # Wait until wifi is connected
            tStamp = time.ticks_ms()
            if not self.is_connected:
                print("Trying to connect. Note this may take a while...",end="")
                self.wlan.connect(self.getenv('CIRCUITPY_WIFI_SSID'),self.getenv('CIRCUITPY_WIFI_PASSWORD'))
            while not self.is_connected:
                time.sleep(.5)
                print(".",end="")
                tElapse = time.ticks_ms() - tStamp
                if tElapse < 0:
                    tStamp = time.ticks_ms()
                    tElapse = tStamp
                if tElapse > self.timeout:
                    break

            print("")
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
            self.response = self._requests.get(text_url,headers=headers,timeout=self.timeout)
        elif implementation.name.upper() == 'MICROPYTHON':
            if not getJSON or not self._requests:
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
                addr = self._pool.getaddrinfo(HOST, PORT)[0][4]
                # Create a new socket and connect to addr
                client = self._pool.socket()
                client.connect(addr)
                if PORT == 443:
                    self.response = ssl.wrap_socket(client)
                else:
                    self.response = client
                headStr = ""
                if headers:
                    for headKey in headers:
                        headStr += f'{headKey}: {headers[headKey]}\r\n'
                # Send HTTP request and recv response
                #print('GET %s HTTP/1.1\r\nHost: %s\r\n%s\r\n'%(QUERY,HOST,headStr))
                self.response.write(f'GET {QUERY} HTTP/1.1\r\nHost: {HOST}\r\n{headStr}\r\n')

                self._poller = select.poll()
                self._poller.register(self.response, select.POLLIN)
            else:
                if not headers:
                    headers = {}
                # urequests response used for json
                self.response = self._requests.get(text_url,headers=headers,timeout=self.timeout)
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
                retVal = b''
                if res and res[0][1] == select.POLLIN:
# socket wrapped in SSL doesn't close at end of data so may be reading single byte
# ESP32-S2 seems to have WiFi issues, reading single bytes seems to help a little
                    if 'ESP32S2' in implementation._machine.upper() or \
                       'ESP32-S2' in implementation._machine.upper():
                        loopcnt = size
                        while loopcnt > 0 and res and res[0][1] == select.POLLIN:
                            loopcnt -= 1
                            try:
                                retVal += res[0][0].read(1)
                            except:
                                break
                            res = self._poller.poll(self.timeout)
                    else:
                        retVal = res[0][0].read(size)

        return retVal

    def close(self):
        if implementation.name.upper() == 'CIRCUITPYTHON':
            if self.response:
                # Maybe fixed.... self.response.close()  Takes too long, effectivly hangs....
                self.response.close()
            self.response = None
            adafruit_connection_manager.connection_manager_close_all(release_references=True)
            if board.board_id in ['arduino_nano_rp2040_connect'] or 'ESP_CS' in dir(board):
                self.radio.disconnect()
                self.radio = None
                self._esp32_cs.deinit()
                self._esp32_ready.deinit()
                self._esp32_reset.deinit()
                self._spi.deinit()
                self._requests = None
                self._pool = None
            else:
                # Temporary until CP 8.x no longer supported
                try:
                    self._requests._free_sockets()
                except:
                    pass
                self._requests = None
                self._pool = None
        else:
            if self.response is not None:
                if self._poller is not None:
                    self._poller.unregister(self.response)
                self.response.close()
            self._poller = None
        self.response = None

Pydos_wifi = PyDOS_wifi()

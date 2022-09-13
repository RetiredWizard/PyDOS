'''Adapted from the Adafruit_CircuitPython_ESP32SPI
library example esp32spi_simpletest.py:
https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI/
blob/master/examples/esp32spi_simpletest.py '''

import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from os import getenv

# Get wifi details and more from a .env file
if getenv('CIRCUITPY_WIFI_SSID') is None:
    raise Exception("WiFi secrets are kept in .env, please add them there!")

print("Arduino Nano RP2040 Connect webclient test")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

#  ESP32 pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

#  uses the secondary SPI connected through the ESP32
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

#This disconnects from AP
#for ap in esp.scan_networks():
    #print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))

ntrys = 0
while not esp.is_connected and ntrys < 3:
    if ntrys == 0:
        print("Connecting to AP...")
    ntrys += 1
    try:
        esp.connect_AP(getenv('CIRCUITPY_WIFI_SSID'), getenv('CIRCUITPY_WIFI_PASSWORD'))
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue

if esp.is_connected:
    print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
    print("My IP address is", esp.pretty_ip(esp.ip_address))

    try:
        print(
            "IP lookup adafruit.com: %s" % esp.pretty_ip(esp.get_host_by_name("adafruit.com"))
        )
    except:
        print("*ERROR* Exception: Failed to request hostname")

    print("Fetching text from", TEXT_URL)
    try:
        r = requests.get(TEXT_URL)
        print("-" * 40)
        print(r.text)
        print("-" * 40)
        r.close()
    except:
        print("*ERROR* Exception: ESP32 not responding")


print("Done!")

esp32_cs.deinit()
esp32_ready.deinit()
esp32_reset.deinit()
spi.deinit()

# Rainbow algorithm adapted from
# https://learnembeddedsystems.co.uk/using-the-rgb-led-on-the-arduino-nano-rp2040-connect

import time
import supervisor
import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

def kbdInterrupt():

    cmnd = ""
    sba = False

    if supervisor.runtime.serial_bytes_available:
        cmnd = input().strip()
        if cmnd == "":
            sba = False
        else:
            sba = True

    return sba, cmnd

#  Nano LED Pins
LEDG = 25
LEDB = 26
LEDR = 27

OUT = 1   # I/O Direction

#  ESP32 pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

#  uses the secondary SPI connected through the ESP32
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

esp.set_pin_mode(LEDR,OUT)
esp.set_pin_mode(LEDG,OUT)
esp.set_pin_mode(LEDB,OUT)

rgbValues = [255,0,0]
upIndex = 0
downIndex = 1

# Cycle colours.
print("listening... 'q' to quit")

while True:

    kbdInt, cmnd = kbdInterrupt()
    if kbdInt:
        if cmnd == "q":
            break

    rgbValues[upIndex] += 1
    rgbValues[downIndex] -= 1

    if rgbValues[upIndex] > 255:
        rgbValues[upIndex] = 255
        upIndex = (upIndex + 1) % 3

    if rgbValues[downIndex] < 0:
        rgbValues[downIndex] = 0
        downIndex = (downIndex + 1) % 3

    esp.set_analog_write(LEDR,rgbValues[0]/255)
    esp.set_analog_write(LEDG,rgbValues[1]/255)
    esp.set_analog_write(LEDB,rgbValues[2]/255)

    time.sleep(0.005)

esp32_cs.deinit()
esp32_ready.deinit()
esp32_reset.deinit()
spi.deinit()
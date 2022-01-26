# Example using PIO to drive a WS2812 LED
# // Copy and paste directly into REPL from TeraTerm
# // Make sure baudrate is set to 115200 bps

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

# attempt to balance colors
MAXRED = 120
MAXGREEN = 165
MAXBLUE = 255

# Cycle colours.
icolor = 0
transition = [-4,1,2,-1,4,1,-2,-1]
cmnd = ""
steps = 100
r = 0
g = 0
b = 0

print("listening... Enter value to alter speed, 'q' to quit")

while True:

    kbdInt, cmnd = kbdInterrupt()
    if kbdInt:
        if cmnd.upper() == "Q":
            break
        if cmnd.isdigit():
            steps = max(1,min(800,int(cmnd)))
            print("New STEP value: ",steps)
        elif cmnd != None:
            print(cmnd)

    icolor = (icolor + 1) % 8

    for k in range(steps):
        r += ((abs(transition[icolor]) & 1)/transition[icolor]) * (MAXRED / steps)
        b += ((abs(transition[icolor]) & 2)/transition[icolor]) * (MAXBLUE / steps)
        g += ((abs(transition[icolor]) & 4)/transition[icolor]) * (MAXGREEN / steps)
        r = max(0,min(MAXRED,r))
        b = max(0,min(MAXBLUE,b))
        g = max(0,min(MAXGREEN,g))

        esp.set_analog_write(LEDR,(255-int(r))/255)
        esp.set_analog_write(LEDG,(255-int(g))/255)
        esp.set_analog_write(LEDB,(255-int(b))/255)

        time.sleep(0.5/steps)

    #time.sleep(0.5)

esp32_cs.deinit()
esp32_ready.deinit()
esp32_reset.deinit()
spi.deinit()
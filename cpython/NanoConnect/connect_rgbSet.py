# Example using PIO to drive a WS2812 LED
# // Copy and paste directly into REPL from TeraTerm
# // Make sure baudrate is set to 115200 bps

import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

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


if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    ans = input("R,G,B: ")
else:
    ans = passedIn

if len(ans.split(",")) == 3:
    r = 255 - max(0,min(255,int((ans.split(',')[0] if ans.split(",")[0].isdigit() else 0))))
    g = 255 - max(0,min(255,int((ans.split(',')[1] if ans.split(",")[1].isdigit() else 0))))
    b = 255 - max(0,min(255,int((ans.split(',')[2] if ans.split(",")[2].isdigit() else 0))))
else:
    r = 0
    g = 0
    b = 0

esp.set_pin_mode(LEDR,OUT)
esp.set_pin_mode(LEDG,OUT)
esp.set_pin_mode(LEDB,OUT)

esp.set_analog_write(LEDR,r/255)
esp.set_analog_write(LEDG,g/255)
esp.set_analog_write(LEDB,b/255)

esp32_cs.deinit()
esp32_ready.deinit()
esp32_reset.deinit()
spi.deinit()
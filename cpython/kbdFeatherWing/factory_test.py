from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
from adafruit_stmpe610 import Adafruit_STMPE610_SPI
import adafruit_ili9341
import adafruit_sdcard
import digitalio
import displayio
import neopixel
import storage
import board
import time
import os

# Optional Qwiic test
try:
    import adafruit_pct2075
except Exception as e:
    print('Skipping Qwiic test,', e)

all_passed = True

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
touch_cs = board.D6
sd_cs = board.D5
neopix_pin = board.D11

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

print('Display: Pass? (you tell me)')

# Touch Screen
print('Touch the screen')
try:
    touch = Adafruit_STMPE610_SPI(spi, digitalio.DigitalInOut(touch_cs))
    while touch.buffer_empty:
        pass

    print('Touch: Pass,', touch.read_data())
except Exception as e:
    print('Touch: Fail,', e)
    all_passed = False

# SD Card
try:
    sdcard = adafruit_sdcard.SDCard(spi, digitalio.DigitalInOut(sd_cs))
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, '/sd')

    # Expect at least one file on the card
    if len(os.listdir('/sd/')) > 0:
        print('SD-Card: Pass')
    else:
        raise Exception('No files')
except Exception as e:
    print('SD-Card: Fail,', e)
    all_passed = False

# Neopixel test, pink!
try:
    pixels = neopixel.NeoPixel(neopix_pin, 1)
    pixels[0] = 0xFF00FF
    time.sleep(0.3)
    pixels.brightness = 0.1
    print('Neopixel: Pass')
except Exception as e:
    print('Neopixel: Fail,', e)
    all_passed = False

try:
    i2c = board.I2C()
except Exception as e:
    print('I2C: Fail,', e)
    all_passed = False

# Optional
try:
    pct = adafruit_pct2075.PCT2075(i2c)
    print('Temperature: %.2f C' % pct.temperature)
except Exception as e:
    print('Qwiic: Fail (might be fine),', e)

# Keyboard test helper
def await_key(kbd, key, name=''):
    if name == '':
        name = key

    print('Press %s' % name)

    while kbd.key_count < 2:
        pass

    keys = kbd.keys
    res = (keys[0] == (1, key) and keys[1] == (3, key))
    if not res:
        raise Exception('Expected %s but got %s' % (name, keys))

# Keyboard
try:
    kbd = BBQ10Keyboard(i2c)

    # Test a key from each column
    await_key(kbd, 'q')
    await_key(kbd, 's')
    await_key(kbd, 'p')
    await_key(kbd, 'b')
    await_key(kbd, 'm')
    await_key(kbd, 'f')

    # All the extra keys
    await_key(kbd, '\x06', 'L1')
    await_key(kbd, '\x11', 'L2')
    await_key(kbd, '\x07', 'R1')
    await_key(kbd, '\x12', 'R2')
    await_key(kbd, '\x01', 'UP')
    await_key(kbd, '\x02', 'DOWN')
    await_key(kbd, '\x03', 'LEFT')
    await_key(kbd, '\x04', 'RIGHT')

    print('Keyboard: Pass')
except Exception as e:
    print('Keyboard: Fail', e)
    all_passed = False

if all_passed:
    print('All tests passed!')
else:
    print('Some fails!')

import sys
try:
    from pydos_ui import input
except:
    pass

if sys.implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import busio
    from circuitpython_i2c_lcd import I2cLcd
    from pydos_ui import PyDOS_UI
else:
    import machine
    from os import uname
    import lcd2004


# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def lcdPrint(passedIn):

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        i2c = PyDOS_UI.I2C()

        # circuitpython seems to require locking the i2c bus
        while i2c.try_lock():
            pass

        if DEFAULT_I2C_ADDR not in i2c.scan():
            print("LCD not found at address: ",hex(DEFAULT_I2C_ADDR))
            i2c.unlock()
            return

        # 2 lines, 16 characters per line
        lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

        # smiley faces as custom characters
        happy = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
        heart = bytearray([0x00,0x00,0x0A,0X15,0X11,0X0A,0X04,0X00])
        grin = bytearray([0x00,0x00,0x0A,0x00,0x1F,0x11,0x0E,0x00])
        lcd.custom_char(0, happy)
        lcd.custom_char(1, heart)
        lcd.custom_char(2, grin)

    else:

        if uname().machine == 'TinyPICO with ESP32-PICO-D4':
            SCL=22
            SDA=21
        elif uname().machine == 'SparkFun Thing Plus RP2040 with RP2040':
            # Sparkfun thingplus QWIC SCL=7 SDA=6
            SCL=7
            SDA=6
        else:
            # Raspberry PI Pico SCL = GPIO3,pin5 SDA = GPIO2,pin4
            SCL=3
            SDA=2

        ID=1
        i2c=machine.I2C(ID,scl=machine.Pin(SCL),sda=machine.Pin(SDA),freq=400000)
        lcd=lcd2004.lcd(ID,39,SCL,SDA)
        lcd.lcd_backlight(True)
        lcd.lcd_clear()

    mess = passedIn
    if mess == "":
        mess = input("Say what?: ")

    if mess == "":
        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            lcd.backlight_off()
        else:
            lcd.lcd_backlight(False)
    else:

        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            mess = mess.replace("<3",chr(1))
            mess = mess.replace(":)",chr(0))
            mess = mess.replace("(:",chr(0))
            mess = mess.replace(":-)",chr(0))
            mess = mess.replace("(-:",chr(0))
            mess = mess.replace(":D",chr(2))

            lcd.move_to(0,0)
            lcd.putstr(mess)
        else:
            lcd.lcd_print(mess,1,0)

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        i2c.unlock()
        #i2c.deinit()


if __name__ != "PyDOS":
    passedIn = ""

lcdPrint(passedIn)

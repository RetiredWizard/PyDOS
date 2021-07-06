import machine
import sys
import uselect
import time
import lcd2004

def lcdPrint():

    SCL=7
    SDA=6
    ID=1
    i2c=machine.I2C(ID,scl=machine.Pin(SCL),sda=machine.Pin(SDA),freq=400000)
    lcd=lcd2004.lcd(ID,39,SCL,SDA)
    lcd.lcd_backlight(True)
    lcd.lcd_clear()
    print(passedIn)
    argv = passedIn
    if argv == "":
        argv = input("Say what?: ")
    if argv == "":
        lcd.lcd_backlight(False)
    else:
        lcd.lcd_print(argv,1,0)

lcdPrint()

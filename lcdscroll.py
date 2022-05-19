import sys
from time import sleep
from pydos_hw import PyDOS_HW
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

if sys.implementation.name.upper() == "CIRCUITPYTHON":
    import supervisor
    from circuitpython_i2c_lcd import I2cLcd
else:
    import lcd2004
    import uselect


# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def lcdScroll(argv):

    i2c = PyDOS_HW.I2C()

    if sys.implementation.name.upper() == "CIRCUITPYTHON":

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

        ID=1
        lcd=lcd2004.lcd(DEFAULT_I2C_ADDR,i2c)
        lcd.lcd_backlight(True)
        lcd.lcd_clear()

    if argv == "":
        if envVars.get("stopthread","") == "":
            if envVars.get("_UI","") == "Keyboard FeatherWing":
                i2c.unlock()
            argv = input("Say what?: ")
            if envVars.get("_UI","") == "Keyboard FeatherWing":
                while i2c.try_lock():
                    pass
        else:
            print('\nUse "passedIn" environment variable to define text for threaded run.')

    if argv == "":
        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            lcd.backlight_off()
        else:
            lcd.lcd_backlight(False)
    else:

        print("\nPress q to quit or set stopthread=stop...")

        mess = " "*max(0,16-len(argv))+argv+" "*max(0,(14-max(0,16-len(argv))))
        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            mess = mess.replace("<3",chr(1))
            mess = mess.replace(":)",chr(0))
            mess = mess.replace("(:",chr(0))
            mess = mess.replace(":-)",chr(0))
            mess = mess.replace("(-:",chr(0))
            mess = mess.replace(":D",chr(2))
        if len(argv) != 1:
            mess =  " " + mess
        for i in range(16):
            if ((" "*(15-i))+mess[0:i+1]).strip() != "":
                if sys.implementation.name.upper() == "CIRCUITPYTHON":
                    lcd.move_to(0,0)
                    lcd.putstr((" "*(15-i))+mess[0:i+1])
                else:
                    lcd.lcd_print((" "*(15-i))+mess[0:i+1],1,0)
                sleep(.25)

        i = 0
        lastCell = 15
        envVars["stopthread"] = "go"
        cmnd = ""

        while cmnd.upper() != "Q" and envVars.get("stopthread") == "go":

            if envVars.get("_UI","") == "Keyboard FeatherWing":
                i2c.unlock()
            while Pydos_ui.serial_bytes_available():
                cmnd = Pydos_ui.read_keyboard(1)
                print(cmnd, end="", sep="")
                if cmnd in "qQ":
                    break

            if envVars.get("_UI","") == "Keyboard FeatherWing":
                while i2c.try_lock():
                    pass

            i += 1
            if i >= len(mess):
                i = 0

            line = mess[i:min(i+16,len(mess))]+mess[0:max(0,(i+16)-len(mess))]
            #lcd.lcd_clear()
            #lcd.lcd_print(line,1,0)
            lastCell += 1
            if lastCell > 39:
                lastCell = 0
            # Scroll Left
            if sys.implementation.name.upper() == "CIRCUITPYTHON":
                lcd.hal_write_command(0x10 | 0x8)
                lcd.move_to(lastCell,0)
                lcd.putstr(line[-1])
            else:
                lcd.lcd_write(0x10 | 0x8)
                lcd.lcd_print(line[-1],1,lastCell)
            sleep(.35)

        if "stopthread" in envVars.keys():
            envVars.pop("stopthread")

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        i2c.unlock()
        #i2c.deinit()

if __name__ != "PyDOS":
    passedIn = ""
    global envVars
    envVars = {}

lcdScroll(passedIn)

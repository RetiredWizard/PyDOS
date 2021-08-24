import sys
from time import sleep

if sys.implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import busio
    import supervisor
    from circuitpython_i2c_lcd import I2cLcd
else:
    import machine
    import lcd2004
    import uselect


# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def lcdScroll(argv):

    def kbdInterrupt():

        cmnd = ""
        sba = False

        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            if supervisor.runtime.serial_bytes_available:
                cmnd = input().strip()
        else:
            spoll = uselect.poll()
            spoll.register(sys.stdin,uselect.POLLIN)
            cmnd = sys.stdin.read(1) if spoll.poll(0) else ""
            spoll.unregister(sys.stdin)

        if cmnd == "":
            sba = False
        else:
            sba = True

        return sba,cmnd

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        i2c = busio.I2C(board.SCL, board.SDA)

        # circuitpython seems to require locking the i2c bus
        while i2c.try_lock():
            pass

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

        # Sparkfun thingplus QWIC SCL=7 SDA=6
        SCL=7
        SDA=6
        # Raspberry PI Pico SCL = GPIO3,pin5 SDA = GPIO2,pin4
        #SCL=3
        #SDA=2
        ID=1
        i2c=machine.I2C(ID,scl=machine.Pin(SCL),sda=machine.Pin(SDA),freq=400000)
        lcd=lcd2004.lcd(ID,39,SCL,SDA)
        lcd.lcd_backlight(True)
        lcd.lcd_clear()

    if argv == "":
        if envVars.get("stopthread","") == "":
            argv = input("Say what?: ")
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
            kbdInt, cmnd = kbdInterrupt()

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
        i2c.deinit()

if __name__ != "PyDOS":
    passedIn = ""
    global envVars
    envVars = {}

lcdScroll(passedIn)
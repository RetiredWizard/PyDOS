import time,sys
from pydos_hw import Pydos_hw
from pydos_ui import Pydos_ui
from sys import implementation
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    import lcd2004
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from microcontroller import cpu
    from circuitpython_i2c_lcd import I2cLcd
    try:
        from pydos_ui import input
    except ImportError:
        pass

def displayTemp(argv):

    lcdavail = True
    # The PCF8574 has a jumper selectable address: 0x20 - 0x27
    DEFAULT_I2C_ADDR = 0x27

    try:
        i2c = Pydos_hw.I2C()
    except:
        lcdavail = False

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        if 'temperature' not in dir(cpu):
            print("Temperature sensor not found")
            return

        if lcdavail:
            # circuitpython seems to require locking the i2c bus
            while i2c.try_lock():
                pass

            if DEFAULT_I2C_ADDR not in i2c.scan():
                print("LCD not found at address: ",hex(DEFAULT_I2C_ADDR))
                i2c.unlock()
                lcdavail = False
            else:
                # 2 lines, 16 characters per line
                lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
                lcd.move_to(0,0)
                lcd.putstr("Temperature:")
    else:
        if 'ADC' not in dir(machine):
            print("Temperature sensor not found")
            return

        try:
            ID=1
            lcd=lcd2004.lcd(DEFAULT_I2C_ADDR,i2c)
            lcd.lcd_backlight(True)
            lcd.lcd_clear()
            lcd.lcd_print("Temperature:",1,0)
        except:
            lcdavail = False

    print("q to quit...")

    if sys.implementation.name.upper() == "MICROPYTHON":
        tempsensor = machine.ADC(4)
        conversionFact = 3.3 /65535

    if argv == "":
        avgCount = 50
    else:
        avgCount = int(argv)

    cmd = ""
    while cmd.upper() != "Q":

        tempread = 0
        for i in range(avgCount):
            if sys.implementation.name.upper() == "MICROPYTHON":
                tempread += tempsensor.read_u16()/avgCount
            elif sys.implementation.name.upper() == "CIRCUITPYTHON":
                tempread += cpu.temperature/avgCount

        if sys.implementation.name.upper() == "MICROPYTHON":
            currVoltage = tempread * conversionFact
            temp = 27 - ((currVoltage - 0.706)/0.001721)
        elif sys.implementation.name.upper() == "CIRCUITPYTHON":
            temp = tempread
        temp = (temp * 9 / 5) + 32

        print("Temperature:%6.2f deg F" % (temp))
        if lcdavail:
            if sys.implementation.name.upper() == "CIRCUITPYTHON":
                lcd.move_to(0,1)
                lcd.putstr(" "*16)
                lcd.move_to(0,1)
                lcd.putstr("%6.2f deg F" % (temp))
            else:
                lcd.lcd_print((" "*16),2,0)
                lcd.lcd_print(("%6.2f deg F" % (temp)),2,0)

        time.sleep(5)
        if Pydos_hw.KFW:
            i2c.unlock()
        while Pydos_ui.serial_bytes_available():
            cmd = Pydos_ui.read_keyboard(1)
            print(cmd, end="", sep="")
            if cmd.upper() == "Q":
                break
        if Pydos_hw.KFW:
            while i2c.try_lock():
                pass

if __name__ != "PyDOS":
    passedIn = ""

displayTemp(passedIn)

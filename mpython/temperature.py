import machine
import sys
import uselect
import time
import lcd2004

def displayTemp(passedIn):

    def kbdInterrupt():

        spoll = uselect.poll()
        spoll.register(sys.stdin,uselect.POLLIN)

        cmnd = sys.stdin.read(1) if spoll.poll(0) else None

        spoll.unregister(sys.stdin)

        return(cmnd)

    # Sparkfun thingplus QWIC SCL=7 SDA=6
    #SCL=7
    #SDA=6
    # Raspberry PI Pico SCL = GPIO3,pin5 SDA = GPIO2,pin4
    SCL=3
    SDA=2
    ID=1
    i2c=machine.I2C(ID,scl=machine.Pin(SCL),sda=machine.Pin(SDA),freq=400000)
    lcd=lcd2004.lcd(ID,39,SCL,SDA)
    lcd.lcd_backlight(True)
    lcd.lcd_clear()
    lcd.lcd_print("Temperature:",1,0)

    print("q to quit...")

    tempsensor = machine.ADC(4)
    conversionFact = 3.3 /65535

    if passedIn == "":
        avgCount = 50
    else:
        avgCount = int(passedIn)

    cmd = ""
    while cmd != "Q" and cmd != "q":

        tempread = 0
        for i in range(avgCount):
            tempread += tempsensor.read_u16()/avgCount

        currVoltage = tempread * conversionFact
        temp = 27 - ((currVoltage - 0.706)/0.001721)
        temp = (temp * 9 / 5) + 32

        print("Temperature:%6.2f deg F" % (temp))
        lcd.lcd_print((" "*16),2,0)
        lcd.lcd_print(("%6.2f deg F" % (temp)),2,0)

        time.sleep(5)
        cmd = kbdInterrupt()

if __name__ != "PyDOS":
    passedIn = ""

displayTemp(passedIn)
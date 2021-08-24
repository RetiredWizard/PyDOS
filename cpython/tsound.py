import time,pwmio
foundPin = True
try:
    #A5 is GPIO D19 on Nano Connect
    from board import A5 as sndPin
except:
    foundPin = False
if not foundPin:
    foundPin = True
    try:
        #MOSI is D19 on Feather
        from board import MOSI as sndPin
    except:
        foundPin = False

piezo = pwmio.PWMOut(sndPin,duty_cycle=0,frequency=440,variable_frequency=True)

cmnd = "Y"
while cmnd.upper() == "Y":
    for f in (200, 300, 400, 500, 600, 700, 800, 900):
        piezo.frequency = f
        piezo.duty_cycle = 65535 // 3
        time.sleep(0.25)
        piezo.duty_cycle = 0
        time.sleep(0.05)
    time.sleep(0.5)

    cmnd = input("Again (y/n): ")

piezo.deinit()
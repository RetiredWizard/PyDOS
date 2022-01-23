import time,pwmio
foundPin = True
from board import board_id

foundPin = True
if board_id == "arduino_nano_rp2040_connect":
    #A5 is GPIO D19 on Nano Connect
    from board import A5 as sndPin
elif board_id == "raspberry_pi_pico":
    #D12 is GP11 on the Raspberry PICO
    try:
        from cyt_mpp_board import SNDPIN as sndPin
    except:
        from board import GP11 as sndPin
elif board_id == "cytron_maker_pi_rp2040":
    from board import GP22 as sndPin
else:
    try:
        #Use D12 on Feathers
        from board import D12 as sndPin
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

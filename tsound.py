import time
import sys
from pydos_hw import Pydos_hw
from pydos_hw import quietSnd
try:
    import synthio
    import audiobusio
except:
    pass

if Pydos_hw.sndPin == None and Pydos_hw.i2sSCK == None:
    print("Sound Pin not found")
else:
    if sys.implementation.name.upper() == "MICROPYTHON":
        import machine
        try:
            # Check if alternate PWM mode (nrf boards) is being used
            piezo=machine.PWM(0,period=10000,pin=Pydos_hw.sndPin,freq=200,duty=50)
        except:
            piezo=machine.PWM(Pydos_hw.sndPin)
    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        if Pydos_hw.i2sSCK:
            noteMS = 375
            i2s = audiobusio.I2SOut(Pydos_hw.i2sSCK,Pydos_hw.i2sWS,Pydos_hw.i2sDATA)
            synth = synthio.Synthesizer(sample_rate=22050)
            e = synthio.Envelope(attack_time=.0001,decay_time=.0001,release_time=0,attack_level=.5,sustain_level=.5)
            i2s.play(synth)
        else:
            from pwmio import PWMOut
            Pydos_hw.sndGPIO.deinit() # Workaround for ESP32-S2 GPIO issue
            piezo = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)

    cmnd = "Y"
    while cmnd.upper() == "Y":
        for f in (200, 300, 400, 500, 600, 700, 800, 900):
            if sys.implementation.name.upper() == "MICROPYTHON":
                oldPWM = False
                piezo.freq(f)
                if 'duty_u16' in dir(piezo):
                    piezo.duty_u16(65535 // 3)
                else:
                    try:
                        piezo=machine.PWM(0,period=(1000-f)*20,pin=Pydos_hw.sndPin,freq=250,duty=33)
                        piezo.init()
                        oldPWM = True
                    except:
                        piezo.duty(int(((65535 // 3)/65535)*1023))
                time.sleep(0.25)
                if oldPWM:
                    piezo.deinit()
                elif 'duty_u16' in dir(piezo):
                    piezo.duty_u16(0)
                else:
                    piezo.duty(0)
            elif sys.implementation.name.upper() == "CIRCUITPYTHON":
                if Pydos_hw.i2sSCK:
                    note = synthio.Note(frequency=f,envelope=e)
                    synth.press(note)
                    time.sleep(0.25)
                    synth.release(note)
                else:
                    piezo.frequency = f
                    piezo.duty_cycle = 65535 // 3
                    time.sleep(0.25)
                    piezo.duty_cycle = 0

            time.sleep(0.05)
        time.sleep(0.5)

        cmnd = input("Again (y/n): ")

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        if Pydos_hw.i2sSCK:
            synth.deinit()
            i2s.deinit()
        else:
            piezo.deinit()
            quietSnd() # Workaround for ESP32-S2 GPIO issue

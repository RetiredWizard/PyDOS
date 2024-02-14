import sys
from pydos_ui import Pydos_ui
from pydos_hw import Pydos_hw
from pydos_hw import quietSnd

if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from time import ticks_ms,sleep
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from time import sleep
    from supervisor import ticks_ms
    from pwmio import PWMOut
    from board import board_id
    try:
        import synthio
        import audiobusio
    except:
        pass

def piano():

    noteMS = 500
    if sys.implementation.name.upper() == 'MICROPYTHON':
        oldPWM = False
        try:
            # Check if alternate PWM mode (nrf boards) is being used
            pwm=machine.PWM(0,period=10000,pin=Pydos_hw.sndPin,freq=250,duty=0)
            oldPWM = True
        except:
            pwm=machine.PWM(Pydos_hw.sndPin)
    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        if Pydos_hw.i2sSCK:
            noteMS = 375
            i2s = audiobusio.I2SOut(Pydos_hw.i2sSCK,Pydos_hw.i2sWS,Pydos_hw.i2sDATA)
            synth = synthio.Synthesizer(sample_rate=22050)
            e = synthio.Envelope(attack_time=.0001,decay_time=.0001,release_time=0,attack_level=.5,sustain_level=.5)
            i2s.play(synth)
        else:
            Pydos_hw.sndGPIO.deinit() # Workaround for ESP32-S2 GPIO issue
            pwm=PWMOut(Pydos_hw.sndPin, duty_cycle=0, frequency=440, variable_frequency=True)

    print ("\nPress +/- to change volume, 'q' to quit...")

    volume = 400
    lastVol = 400
    cmnd = None
    press = False
    noneAt = ticks_ms()
    firstNone = True
    note = 0
    rnote = 0.0
    lastNote = -1
    while cmnd != "q":
        if Pydos_ui.serial_bytes_available() != 0:
            cmnd = Pydos_ui.read_keyboard(1)
            #print("->"+cmnd+"<- : ",ord(cmnd[0]))
            firstNone = True
            if cmnd=="h": # middle C
                rnote=261.6256
                press = True
            elif cmnd == "a": # E
                rnote=164.8138
                press = True
            elif cmnd == "s": # F
                rnote=174.6141
                press = True
            elif cmnd == "d": # G
                rnote=195.9977
                press = True
            elif cmnd == "r": # G sharp/A flat
                rnote=207.6523
                press = True
            elif cmnd == "f": # A
                rnote=220.0
                press = True
            elif cmnd == "t": # A sharp/B flat
                rnote=233.0819
                press = True
            elif cmnd == "g": # B
                rnote=246.9417
                press = True
            elif cmnd == "u": # C sharp/D flat
                rnote=277.1826
                press = True
            elif cmnd == "j": # D
                rnote=293.6648
                press = True
            elif cmnd == "k": # E
                rnote=329.6276
                press = True
            elif cmnd == "l": # F
                rnote=349.2262
                press = True
            elif cmnd == "o": # F sharp/G flat
                rnote=369.9944
                press = True
            elif cmnd == ";": # G
                rnote=391.9954
                press = True
            elif cmnd == "q":
                break
            if press:
                note = int(rnote+.5)

            if cmnd == "+":
                volume += 100
            elif cmnd == "-":
                volume -= 100
        else:
            if firstNone:
                noneAt = ticks_ms()
                firstNone = False
            else:
                if ticks_ms() > noneAt+noteMS:
                    firstNone = True
                    press = False

        if press:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                pwm.freq(note)
                if oldPWM:
                    pwm=machine.PWM(0,period=(1000-note)*20,pin=Pydos_hw.sndPin,freq=250, \
                        duty=int((volume/65535)*200))
                    pwm.init()
                if 'duty_u16' in dir(pwm):
                    pwm.duty_u16(volume)
                else:
                    pwm.duty(int((volume/65535)*1023))
                if "ESP32" in sys.implementation._machine or "S2" in sys.implementation._machine:
                    sleep(.1)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                if Pydos_hw.i2sSCK:
                    if lastNote != rnote:
                        if lastNote != -1:
                            synth.release(snote)
                        volume = max(0,min(1000,volume))
                        if lastVol != volume:
                            lastVol = volume
                            e = synthio.Envelope(attack_time=.0001,decay_time=.0001,release_time=0,attack_level=volume/1000,sustain_level=volume/1000)
                        snote = synthio.Note(frequency=rnote,envelope=e)
                        synth.press(snote)
                        lastNote = rnote
                else:
                    if pwm.frequency != note:
                        pwm.frequency = note
                    if pwm.duty_cycle != volume:
                        pwm.duty_cycle = volume
                    if "s2" in board_id or "s3" in board_id:
                        sleep(.1)

        else:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                if oldPWM:
                    pwm.deinit()
                elif 'duty_u16' in dir(pwm):
                    pwm.duty_u16(0)
                else:
                    pwm.duty(0)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                if Pydos_hw.i2sSCK:
                    if lastNote != -1:
                        synth.release(snote)
                        lastNote = -1
                else:
                    if pwm.duty_cycle != 0:
                        pwm.duty_cycle = 0

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        if Pydos_hw.i2sSCK:
            synth.deinit()
            i2s.deinit()
        else:
            pwm.deinit()
            quietSnd() # Workaround for ESP32-S2 GPIO issue

if Pydos_hw.sndPin or Pydos_hw.i2sSCK:
    piano()
else:
    print("Sound Pin not found")

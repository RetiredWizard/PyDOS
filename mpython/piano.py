import sys, uselect, machine, time

def piano():

    def kbdInterrupt():

        spoll = uselect.poll()
        spoll.register(sys.stdin,uselect.POLLIN)

        if not spoll.poll(0):
            cmnd = None
        else:
            while spoll.poll(0):
                cmnd = sys.stdin.read(1)

        spoll.unregister(sys.stdin)

        return(cmnd)


    pwm=machine.PWM(machine.Pin(19))

    print ("\nPress +/- to change volume, 'q' to quit...")

    volume = 400
    cmnd = None
    press = False
    noneAt = time.ticks_ms()
    firstNone = True
    while cmnd != "q":
        cmnd = kbdInterrupt()
        if cmnd != None:
            #print("->"+cmnd+"<- : ",ord(cmnd[0]))
            firstNone = True
            if cmnd=="h": # middle C
                pwm.freq(int(261.6256+.5))
                press = True
            elif cmnd == "a": # E
                pwm.freq(int(164.8138+.5))
                press = True
            elif cmnd == "s": # F
                pwm.freq(int(174.6141+.5))
                press = True
            elif cmnd == "d": # G
                pwm.freq(int(195.9977+.5))
                press = True
            elif cmnd == "r": # G sharp/A flat
                pwm.freq(int(207.6523+.5))
                press = True
            elif cmnd == "f": # A
                pwm.freq(int(220))
                press = True
            elif cmnd == "t": # A sharp/B flat
                pwm.freq(int(233.0819+.5))
                press = True
            elif cmnd == "g": # B
                pwm.freq(int(246.9417+.5))
                press = True
            elif cmnd == "u": # C sharp/D flat
                pwm.freq(int(277.1826+.5))
                press = True
            elif cmnd == "j": # D
                pwm.freq(int(293.6648+.5))
                press = True
            elif cmnd == "k": # E
                pwm.freq(int(329.6276+.5))
                press = True
            elif cmnd == "l": # F
                pwm.freq(int(349.2262+.5))
                press = True
            elif cmnd == "o": # F sharp/G flat
                pwm.freq(int(369.9944+.5))
                press = True
            elif cmnd == ";": # G
                pwm.freq(int(391.9954+.5))
                press = True
            elif cmnd == "q":
                break

            if cmnd == "+":
                volume += 100
            elif cmnd == "-":
                volume -= 100
        else:
            if firstNone:
                noneAt = time.ticks_ms()
                firstNone = False
            else:
                if time.ticks_ms() > noneAt+500:
                    firstNone = True
                    press = False

        if press:
            pwm.duty_u16(volume)
            #time.sleep(.1)
            #cmnd = kbdInterrupt()
            #while cmnd != None:
                #cmnd = kbdInterrupt()
            #pressedat = time.time()
        else:
            pwm.duty_u16(0)
            #print("Release")

piano()
import time
from sys import implementation
if implementation.name.upper() == 'MICROPYTHON':
    import machine
elif implementation.name.upper() == 'CIRCUITPYTHON':
    try:
        from pydos_ui import input
    except:
        pass

def setdate(newDate):
    clockavail = True
    if implementation.name.upper() == 'CIRCUITPYTHON':
        try:
            from rtc import RTC
        except:
            clockavail = False

    if clockavail:
        mdays = [0,31,29,31,30,31,30,31,31,30,31,30,31]

        if newDate == "":
            print("The current date is: %2.2i/%2.2i/%4.4i" % (time.localtime()[1], time.localtime()[2], time.localtime()[0]))
            newDate = input("Enter the new date (mm-dd-yy): ").replace("/","-")
        if newDate != "":
            inDate = newDate.split('-')

            if len(inDate) != 3:
                print("Bad Date format")
            elif int(inDate[0]) not in range(1,13):
                print("Invalid month entered (1-12)")
            elif int(inDate[1]) not in range(1,mdays[int(inDate[0])]+1):
                print("invalid day entered (1-",mdays[int(inDate[0])],")")
            elif int(inDate[2]) not in range(21,32):
                print("invalid year entered (21-31)")
            else:
                if implementation.name.upper() == 'MICROPYTHON':
                    machine.RTC().datetime(tuple([2000+int(inDate[2]),int(inDate[0]),int(inDate[1])] + \
                        [time.localtime()[i] for i in [6,3,4,5,7]]))
                        
                elif implementation.name.upper() == 'CIRCUITPYTHON':
                    RTC().datetime = time.struct_time((2000+int(inDate[2]),int(inDate[0]),int(inDate[1]), \
                        RTC().datetime[3],RTC().datetime[4],RTC().datetime[5],RTC().datetime[6],-1,-1))
    else:
        print("Real Time Clock (rtc) not available on board")

if __name__ != "PyDOS":
    passedIn = ""

setdate(passedIn)

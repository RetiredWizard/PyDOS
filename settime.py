import time
from sys import implementation
if implementation.name.upper() == 'MICROPYTHON':
    import machine
elif implementation.name.upper() == 'CIRCUITPYTHON':
    try:
        from pydos_ui import input
    except:
        pass

def settime(newTime):

    def iweekDay():
        offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        month = time.localtime()[1]
        day = time.localtime()[2]
        year = time.localtime()[0]
        afterFeb = 1
        if month > 2: afterFeb = 0
        aux = year - 1700 - afterFeb
        # dayOfWeek for 1700/1/1 = 5, Friday
        dayOfWeek  = 5
        # partial sum of days betweem current date and 1700/1/1
        dayOfWeek += (aux + afterFeb) * 365
        # leap year correction
        dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
        # sum monthly and day offsets
        dayOfWeek += offset[month - 1] + (day - 1)
        dayOfWeek %= 7
        return int(dayOfWeek)

    clockavail = True
    if implementation.name.upper() == 'CIRCUITPYTHON':
        try:
            from rtc import RTC
        except:
            clockavail = False

    if clockavail:

        if newTime == "":
            print("The current time is: %2.2i:%2.2i:%2.2i" % (time.localtime()[3], time.localtime()[4], time.localtime()[5]))
            newTime = input("Enter the new time (hh:mm:ss): ")

        if newTime != "":
            inTime = newTime.split(':')

            if len(inTime) != 3:
                print("Bad time format")
            elif int(inTime[0]) not in range(0,25):
                print("Invalid hour entered (0-24)")
            elif int(inTime[1]) not in range(0,61):
                print("invalid minute entered (0-60)")
            elif int(inTime[2]) not in range(0,61):
                print("invalid seconds entered (0-60)")
            else:
                if implementation.name.upper() == 'MICROPYTHON':
                    machine.RTC().datetime(tuple([time.localtime()[i] for i in [0,1,2,6]] + \
                        [int(inTime[0]), int(inTime[1]), int(inTime[2]), time.localtime()[7]]))

                elif implementation.name.upper() == 'CIRCUITPYTHON':
                    RTC().datetime = time.struct_time((RTC().datetime[0],RTC().datetime[1],RTC().datetime[2], \
                        int(inTime[0]),int(inTime[1]),int(inTime[2]),RTC().datetime[6],-1,-1))
    else:
        print("Real Time Clock (rtc) not available on board")

if __name__ != "PyDOS":
    passedIn = ""

settime(passedIn)

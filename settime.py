import machine, time

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


rtcBase=0x4005c000
atomicBSet=0x2000

print("The current time is: %2.2i:%2.2i:%2.2i" % (time.localtime()[3], time.localtime()[4], time.localtime()[5]))
newDate = input("Enter the new time (hh:mm:ss): ")

if newDate != "":
    inDate = newDate.split(':')

    if len(inDate) != 3:
        print("Bad time format")
    elif int(inDate[0]) not in range(0,25):
        print("Invalid hour entered (0-24)")
    elif int(inDate[1]) not in range(0,61):
        print("invalid minute entered (0-60)")
    elif int(inDate[2]) not in range(0,61):
        print("invalid seconds entered (0-60)")
    else:
        machine.mem32[rtcBase+8] = (int(inDate[0]) << 16) | (int(inDate[1]) << 8) | int(inDate[2]) | iweekDay() << 24
        machine.mem32[rtcBase+atomicBSet+0xc] = 0x10
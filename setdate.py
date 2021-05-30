import machine, time

mdays = [0,31,29,31,30,31,30,31,31,30,31,30,31]
rtcBase=0x4005c000
atomicBSet=0x2000

print("The current date is: %2.2i/%2.2i/%4.4i" % (time.localtime()[1], time.localtime()[2], time.localtime()[0]))
newDate = input("Enter the new date (mm-dd-yy): ")
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
        machine.mem32[rtcBase+4] = ((2000+int(inDate[2])) << 12) | (int(inDate[0]) << 8) | int(inDate[1])
        machine.mem32[rtcBase+atomicBSet+0xc] = 0x10
import time

try:
    from pydos_ui import Pydos_ui
except:
    import select
    from sys import stdin
    Pydos_ui = None

x = 10; y = 10; d = 1; e = 1
m='⬤'
try:
    width = int(envVars.get('_scrWidth',80))
    height = int(envVars.get('_scrHeight',24))
except:
    width=80
    height=24

# Add top, bottom and side borders with hashtags
print(f'\033[2J\033[H{"█"*(max(0,(width-30))//2)}{" Bouncing Ball by DuckyPolice "[:width]}' +\
    f'{"█"*(max(0,width-30)-(max(0,(width-30))//2))}\033[2;0H',end="")
for r in range(height-2):
    print('██' + ' '*(width-4) + '██')
print(f'{"█"*(max(0,(width-17))//2)}{" Press Q to exit "[:width]}' +\
    f'{"█"*(max(0,width-17)-(max(0,(width-17))//2))}\033[2;0H',end="")

cmnd = ""
while cmnd.upper() != 'Q':

    if Pydos_ui:
        if Pydos_ui.serial_bytes_available():
            cmnd = Pydos_ui.read_keyboard(1)
    else:
        spoll = select.poll()
        spoll.register(stdin,select.POLLIN)

        if spoll.poll(1):
            cmnd = stdin.read(1)

        spoll.unregister(stdin)


    time.sleep(.05)
    x1=x;y1=y
    x+=d;y+=e
    if x%(width-5)<1:d=-d
    if y%(height-3)<1:e=-e
    print(f'\033[{y1+2};{x1+3}H \033[{y+2};{x+3}H{m}\033[{height-1};{width-2}H')

print("\n")

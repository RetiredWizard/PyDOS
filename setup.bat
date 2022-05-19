@echo off
:tryagain
set/p _ans = (C)ircuit Python or (M)icropython: 
if %_ans% == c goto cpython
if %_ans% == C goto cpython
if %_ans% == m goto mpython
if %_ans% == M goto mpython
echo Invalid selection (C or M)
goto tryagain

:cpython
set _ans = C
copy/y /cpython/* /
if not exist /lib mkdir /lib
copy /cpython/lib/* /lib/
goto board
:mpython
set _ans=M
copy/y /mpython/* /
if not exist /lib mkdir /lib
copy /mpython/lib/* /lib/

:board
set/p _ans2 = (N)anoConnect, (E) ESP32 board, (O)ther RP2040 board:
if %_ans2% == N goto nanoconnect
if %_ans2% == n goto nanoconnect
if %_ans2% == e goto tinypico
if %_ans2% == E goto tinypico
if %_ans2% == o goto other
if %_ans2% == O goto other
echo Invalid selection (N,E or O)
goto board

:nanoconnect
set _ans2 = N
if %_ans% == M goto nanoconnectMP
copy /cpython/NanoConnect/* /
if not exist /lib mkdir /lib
copy /cpython/NanoConnect/lib/* /lib/
if not exist /lib/adafruit_esp32spi mkdir /lib/adafruit_esp32spi
copy /cpython/NanoConnect/lib/adafruit_esp32spi/* /lib/adafruit_esp32spi/
if not exist /lib/adafruit_bus_device mkdir /lib/adafruit_bus_device
copy /cpython/NanoConnect/lib/adafruit_bus_device/* /lib/adafruit_bus_device/
goto other
:nanoconnectMP
copy /mpython/NanoConnect/* /
if not exist /lib mkdir /lib
copy /mpython/NanoConnect/lib/* /lib/
goto other

:tinypico
set _ans2 = E
if %_ans% == C goto tinypicoCP
copy /mpython/ESP32/* /
goto other
:tinypicoCP
copy/y /cpython/ESP32/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32/lib/* /lib/

:other
if %_ans2% == o set _ans2 = O
if %_ans% == M goto Cytron
set/p _ans3 = Are you using a Keyboard FeatherWing (Y/N)?:
if %_ans3% == N goto Cytron
if %_ans3% == n goto Cytron
if %_ans3% == Y goto kbdFeatherW
if %_ans3% == y goto kbdFeatherW
echo Invalid Selection (Y or N)
goto other

:kbdFeatherW
copy/y /cpython/kbdFeatherWing/* /
if not exist /lib mkdir /lib
copy/y /cpython/kbdFeatherWing/lib/* /lib/
copy /lib/pydos_ui.py /lib/pydos_ui_uart.py
copy/y /lib/pydos_ui_kfw.py /lib/pydos_ui.py
if not exist /PyBasic mkdir /PyBasic
copy/y /cpython/kbdFeatherWing/PyBasic/* /PyBasic
if %_ans2% == O del /lib/kfw_s2_board.py
if %_ans2% == E del /lib/kfw_pico_board.py
goto done

:Cytron
if not %_ans2% == O goto done
set/p _ans3 = Are you using a Cytron Maker Pi Pico (Y/N)?:
if %_ans3% == N goto done
if %_ans3% == n goto done
if %_ans3% == Y goto MakerPiPico
if %_ans3% == y goto MakerPiPico
echo Invalid Selection (Y or N)
goto Cytron

:MakerPiPico
if %_ans% == C goto CPCytron
if not exist /lib mkdir /lib
copy/y /mpython/CytronMPP/lib/* /lib/
goto done

:CPCytron
if not exist /lib mkdir /lib
copy/y /cpython/CytronMPP/lib/* /lib/

:done
set _ans=
set _ans2=
set _ans3=
reboot

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
copy /cpython/* /
if not exist /lib mkdir /lib
copy /cpython/lib/* /lib/
goto board
:mpython
set _ans=M
copy /mpython/* /
if not exist /lib mkdir /lib
copy /mpython/lib/* /lib/
:board
@echo (T)hingPlus RP2040, (F)eather RP2040, (N)anoConnect, 
set/p _ans2 =  (S)FeatherS2, (E)Feather ESP32-S2, (P)ESP32-S2 TinyPico, (O)ther:
if %_ans2% == t goto thingplus
if %_ans2% == T goto thingplus
if %_ans2% == f goto feather
if %_ans2% == F goto feather
if %_ans2% == s goto s2feather
if %_ans2% == S goto s2feather
if %_ans2% == e goto ESPs2feather
if %_ans2% == E goto ESPs2feather
if %_ans2% == n goto nanoconnect
if %_ans2% == N goto nanoconnect
if %_ans2% == p goto tinypico
if %_ans2% == p goto tinypico
if %_ans2% == o goto other
if %_ans2% == O goto other
echo Invalid selection (T,F,N,S,P or O)
goto board
:tinypico
set _ans2 = P
if %_ans% == C goto tinypicoCP
copy /mpython/TinyPico/* /
goto other
:tinypicoCP
copy /cpython/ESP32S2/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32S2/lib/* /lib/
goto other
:thingplus
set _ans2 = T
if %_ans% == C goto other
copy /mpython/ThingPlus/* /
goto other
:feather
set _ans2 = F
if %_ans% == M goto other
copy /cpython/Feather/* /
if not exist /lib mkdir /lib
copy /cpython/Feather/lib/* /lib/
goto other
:s2feather
set _ans2 = S
if %_ans% == M goto other
copy /cpython/ESP32S2/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32S2/lib/* /lib/
goto feather
:ESPs2feather
set _ans2 = E
if %_ans% == M goto other
copy /cpython/ESP32S2/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32S2/lib/* /lib/
goto feather
:nanoconnect
set _ans2 = N
if %_ans% == M goto other
copy /cpython/NanoConnect/* /
if not exist /lib mkdir /lib
copy /cpython/NanoConnect/lib/* /lib/
if not exist /lib/adafruit_esp32spi mkdir /lib/adafruit_esp32spi
copy /cpython/NanoConnect/lib/adafruit_esp32spi/* /lib/adafruit_esp32spi/
if not exist /lib/adafruit_bus_device mkdir /lib/adafruit_bus_device
copy /cpython/NanoConnect/lib/adafruit_bus_device/* /lib/adafruit_bus_device/
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
if not exist /PyBasic mkdir /PyBasic
copy/y /cpython/kbdFeatherWing/PyBasic/* /PyBasic
if %_ans2% == O del /lib/kfw_s2_board.py
if %_ans2% == S del /lib/kfw_pico_board.py
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
copy/y /mpython/CytronMPP/* /
if not exist /lib mkdir /lib
copy/y /mpython/CytronMPP/lib/* /lib/
goto done
:CPCytron
copy/y /cpython/CytronMPP/* /
if not exist /lib mkdir /lib
copy/y /cpython/CytronMPP/lib/* /lib/
:done
set _ans=
set _ans2=
set _ans3=
reboot

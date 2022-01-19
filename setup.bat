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
@echo (T)hingPlus RP2040, (F)eather RP2040 or KB2040, (N)anoConnect, 
set/p _ans2 =  (S)FeatherS2 or Feather ESP32-S2, (P)TinyPico, (O)ther:
if %_ans2% == t goto thingplus
if %_ans2% == T goto thingplus
if %_ans2% == f goto feather
if %_ans2% == F goto feather
if %_ans2% == s goto s2
if %_ans2% == S goto s2
if %_ans2% == n goto nanoconnect
if %_ans2% == N goto nanoconnect
if %_ans2% == p goto tinypico
if %_ans2% == p goto tinypico
if %_ans2% == o goto other
if %_ans2% == O goto other
echo Invalid selection (T,F,N,S,P or O)
goto board
:tinypico
if %_ans% == C goto tinypicoCP
copy /mpython/TinyPico/* /
goto other
:tinypicoCP
copy /cpython/ESP32S2/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32S2/lib/* /lib/
goto other
:thingplus
if %_ans% == C goto other
copy /mpython/ThingPlus/* /
goto other
:feather
if %_ans% == M goto other
copy /cpython/Feather/* /
if not exist /lib mkdir /lib
copy /cpython/Feather/lib/* /lib/
goto other
:s2
if %_ans% == M goto other
copy /cpython/ESP32S2/* /
if not exist /lib mkdir /lib
copy /cpython/ESP32S2/lib/* /lib/
goto feather
:nanoconnect
if %_ans% == M goto other
copy /cpython/NanoConnect/* /
if not exist /lib mkdir /lib
copy /cpython/NanoConnect/lib/* /lib/
if not exist /lib/adafruit_esp32spi mkdir /lib/adafruit_esp32spi
copy /cpython/NanoConnect/lib/adafruit_esp32spi/* /lib/adafruit_esp32spi/
if not exist /lib/adafruit_bus_device mkdir /lib/adafruit_bus_device
copy /cpython/NanoConnect/lib/adafruit_bus_device/* /lib/adafruit_bus_device/
goto other
:other
set/p _ans3 = Are you using a Keyboard FeatherWing (Y/N)?:
if %_ans3% == N goto done
if %_ans3% == n goto done
if %_ans3% == Y goto kbdFeatherW
if %_ans3% == y goto kbdFeatherW
echo Invalid Selection (Y or N)
goto other
:kbdFeatherW
del /lib/pydos_ui.py
copy /cpython/kbdFeatherWing/* /
if not exist /lib mkdir /lib
if exist /lib/neopixel.mpy del /lib/neopixel.mpy 
copy /cpython/kbdFeatherWing/lib/* /lib/
if not exist /PyBasic mkdir /PyBasic
del /PyBasic/eliza.bas
del /PyBasic/startrek.bas
copy /cpython/kbdFeatherWing/PyBasic/* /PyBasic
:done
set _ans=
set _ans2=
set _ans3=
